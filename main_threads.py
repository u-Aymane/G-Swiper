import os
import gspread
from selenium import webdriver
import threading


def get_worksheets(sheet_url):
    gc = gspread.service_account()
    sh = gc.open_by_url(sheet_url)
    ans = []
    for wk in sh.worksheets():
        ans.append(wk.title)

    return ans


def remove_duplicates(l):
    temp = []
    for i in l:
        if i not in temp:
            temp.append(i)

    return temp


def remove_checked_rows(l_lines, targeted_indexes):
    # print(targeted_indexes)
    temp_data = []
    cols_ = [[], [], []]
    for row in l_lines:
        if 'Keep' not in row and 'Remove' not in row and 'Invalid' not in row:
            temp_data.append(row)

    for i in temp_data:
        for j in range(0, 3):
            cols_[j].append(i[targeted_indexes[j] - 1])

    return cols_


t = []


def spreadsheet_companies(sheet_url, worksheet):
    gc = gspread.service_account()
    sh = gc.open_by_url(sheet_url)
    wk = sh.worksheet(worksheet)
    header = wk.row_values(1)
    tageted_headers_id = ['Website', 'Company', 'Description']
    global t
    t = []
    for i in tageted_headers_id:
        try:
            t.append(header.index(i) + 1)
        except:
            t.append(-1)

    data = remove_checked_rows(wk.get_all_values(), t)

    return {
        "Websites": remove_duplicates(data[0])[1:],
        "Companies": remove_duplicates(data[1])[1:],
        "Description": remove_duplicates(data[2])[1:]
    }


def get_first_empty_index(l):
    for i in range(len(l)):
        if l[i] == '' and l[i + 1] == '' or l[i] == 'Sorting':
            return i + 1

    return len(l) + 1


def Tinder(choice, website, sheet_url, worksheet):
    if website == 'http://example.com/':
        return -1
    gc = gspread.service_account()
    sh = gc.open_by_url(sheet_url)
    wk = sh.worksheet(worksheet)
    website = website.replace('http://www.', '').replace('/', '')
    location = wk.findall(website)
    first_empty = get_first_empty_index(wk.row_values(1))
    for r in location:
        wk.update_cell(r.row, first_empty, choice)

def surf(url):
    driver.get(url)

if __name__ == '__main__':
    driver = webdriver.Firefox(executable_path='./geckodriver')
    os.system('clear')
    gsheet = input('Google Sheet URL (Make the sheet PUBLIC): ')
    worksheets = get_worksheets(gsheet)
    print('Please choose a number:')
    for i in range(0, len(worksheets)):
        print(f'    {i}: {worksheets[i]}')

    choice = int(input('Choice: '))
    all_data = spreadsheet_companies(gsheet, worksheets[choice])
    for i in range(len(all_data['Websites'])):
        website, company, description = all_data['Websites'][i], all_data['Companies'][i], all_data['Description'][i]
        try:
            os.system('clear')
            print(f'Company name: {company}\n\n')
            print(f'Description: {description}')
            T = threading.Thread(target=surf, args=[f"http://{website}"])
            T.setDaemon(True)
            T.start()
            c = input(f'\n\nKeep (Leave it blank) - Remove (Type r) and hit Enter: ')
            if c == "r":
                T = threading.Thread(target=Tinder, args=['Remove', website, gsheet, worksheets[choice]])
                T.setDaemon(True)
                T.start()
            else:
                T = threading.Thread(target=Tinder, args=['Keep', website, gsheet, worksheets[choice]])
                T.setDaemon(True)
                T.start()
        except Exception as e:
            T = threading.Thread(target=Tinder, args=['Invalid', website, gsheet, worksheets[choice]])
            T.setDaemon(True)
            T.start()
            os.system('clear')






