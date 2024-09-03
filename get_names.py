from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from datetime import datetime, timedelta

driver = webdriver.Chrome()

def get_fire_names(date):
    url = "https://mort.kcg.gov.tw/04/P04S03A-view.aspx?mp=Fmok&Day="
    driver.get(url + str(date))
    rows = driver.find_element(By.ID, "tResult")
    data = rows.text.split()

    names = set()
    for i in range(8, len(data) - 2):
        if not data[i][0].isdigit(): names.add(data[i])
    return names

def get_fire_names_30(date):
    url_1 = "https://mort.kcg.gov.tw/04/P04S03A-view.aspx?mp=Fmok&Day="
    url_2 = "&Days=30"
    url = url_1 + str(date) + url_2
    print(url)
    driver.get(url)
    rows = driver.find_element(By.ID, "tResult")
    data = rows.text.split()
    print(data)

def get_fire_names_ND(date, days):
    url = "https://mort.kcg.gov.tw/04/P04S03A-view.aspx?mp=Fmok&Day="

    start = datetime(int(date[0:3]) + 1911, int(date[3:5]), int(date[5:7]))
    add = timedelta(days=1)

    names = {}

    day = 0
    while day < days:
        day += 1

        td = ""
        if start.month < 10: td += '0'
        td += str(start.month)
        if start.day < 10: td += '0'
        td += str(start.day)
        print(url + str(start.year - 1911) + td)

        driver.get(url + str(start.year - 1911) + td)
        rows = driver.find_element(By.ID, "tResult")
        data = rows.text.split()

        for i in range(8, len(data) - 2):
            if not data[i][0].isdigit() and data[i][0] != '※' and data[i][0] != '●' and not data[i][-1].isdigit():
                if '、' in data[i]:
                    temp = data[i].split('、')
                    for t in temp: names[t] = td
                else: names[data[i]] = td

        start += add
    
    return names

def get_fire_names_with_time(date):
    url = "https://mort.kcg.gov.tw/04/P04S03A-view.aspx?mp=Fmok&Day="
    driver.get(url + str(date))
    rows = driver.find_element(By.ID, "tResult")
    data = rows.text.split()

    names = {}
    for i in range(8, len(data) - 2):
        if data[i][0].isdigit(): time = data[i]
        else: names[data[i]] = time
    return names

def get_freeze_names():
    driver.get("https://mort.kcg.gov.tw/04/P04S02.aspx?mp=Fmok")
    rows = driver.find_element(By.ID, "matter_tResult")
    data = rows.text.split()

    names = {}
    i = 10
    while i < len(data) - 2:
        if data[i][0].isdigit() and not data[i + 1][0].isdigit():
            if data[i + 1] != "無名屍":
                if data[i][-1] == '特': data[i] = data[i].rstrip(data[i][-1])
                    
                names[data[i + 1]] = data[i]
                i += 2
        i += 1

    return names

def get_jg_names():
    driver.get("https://mort.kcg.gov.tw/04/P04S09.aspx?mp=Fmok")
    rows = driver.find_element(By.XPATH, "/html/body/div/section/div/div[3]/form/div[5]/table")
    data = rows.text.split()

    name_id = {}
    for i in range(len(data)):
        if data[i] == '男' or data[i] == '女':
            if ':' in data[i - 2]: data[i - 2] = data[i - 8]
            name_id[data[i - 1]] = data[i - 2]
    
    return name_id

def get_sz_names():
    url = "https://mort.kcg.gov.tw/04/P04S08.aspx?mp=Fmok"
    driver.get(url)
    table = driver.find_element(By.XPATH, "//*[@id='matter_tResult']/tbody")
    row_list = [row.text for row in table.find_elements(By.TAG_NAME, "tr")]

    name_id = {}
    prev = 0

    for i in range(2, len(row_list) + 1):
        person = driver.find_element(By.XPATH, "//*[@id='matter_tResult']/tbody/tr[" + str(i) + "]")
        data = person.find_elements(By.TAG_NAME, "td")
        data_split = [d.text for d in data]
        # print(data_split)

        if len(data_split) == 5 and data_split[1] != '':
            prev = data_split[0]
            name_id[data_split[1]] = prev
        elif len(data_split) == 4:
            name_id[data_split[0]] = prev
    
    return name_id

print(get_sz_names())


def get_rl_names(date, days):
    url = "https://mort.kcg.gov.tw/04/P04S12-view.aspx?mp=Fmok&Day="

    start = datetime(int(date[0:3]) + 1911, int(date[3:5]), int(date[5:7]))
    add = timedelta(days=1)

    names = {}
    
    day = 0
    while day < days:
        day += 1

        td = ""
        if start.month < 10: td += '0'
        td += str(start.month)
        if start.day < 10: td += '0'
        td += str(start.day)
        # print(url + str(start.year - 1911) + td)

        driver.get(url + str(start.year - 1911) + td)
        for i in range(3, 15):
            for j in range(2, 14):
                name = driver.find_element(By.XPATH, "//*[@id='tResult']/tbody/tr[" + str(i) + "]/td[" + str(j) + "]").text
                if name != "": names[name] = [i - 2, str((j - 2) * 2) + ':00-' + str((j - 2) * 2 + 2) + ':00', td]
    
        start += add

    return names

def get_dg_names(date, days):
    url = "https://mort.kcg.gov.tw/04/P04S14-view.aspx?mp=Fmok&Day="

    start = datetime(int(date[0:3]) + 1911, int(date[3:5]), int(date[5:7]))
    add = timedelta(days=1)

    names = {}

    day = 0
    while day < days:
        day += 1

        td = ""
        if start.month < 10: td += '0'
        td += str(start.month)
        if start.day < 10: td += '0'
        td += str(start.day)
        # print(url + str(start.year - 1911) + td)

        driver.get(url + str(start.year - 1911) + td)

        for i in range(3, 7):
            for j in range(2, 11):
                name = driver.find_element(By.XPATH, "//*[@id='tResult']/tbody/tr[" + str(i) + "]/td[" + str(j) + "]").text
                if name != "": names[name] = [i - 2, str(j + 5) + ':00-' + str(j + 5) + ':50', td]

        start += add
    return names

def get_gj_names(date, days):
    url = "https://mort.kcg.gov.tw/04/P04S10-view.aspx?mp=Fmok&Day="

    start = datetime(int(date[0:3]) + 1911, int(date[3:5]), int(date[5:7]))
    add = timedelta(days=1)

    names = {}

    day = 0
    while day < days:
        day += 1

        td = ""
        if start.month < 10: td += '0'
        td += str(start.month)
        if start.day < 10: td += '0'
        td += str(start.day)
        # print(url + str(start.year - 1911) + td + str(start.year - 1911) + td)

        driver.get(url + str(start.year - 1911) + td + str(start.year - 1911) + td)

        rows = driver.find_element(By.ID, "tResult")
        data = rows.text.split()

        for i in range(0, len(data)):
            if data[i] == '男' or data[i] == '女':
                names[data[i - 1]] = [data[i], data[i - 5], data[i - 4], data[i - 3], data[i - 2], data[i + 2]]
        start += add
    
    return names

