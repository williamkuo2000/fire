import json
import pyautogui as pag
import datetime

from get_names import get_freeze_names, get_sz_names, get_rl_names, get_dg_names, get_gj_names, get_fire_names_with_time, get_jg_names

PRINT = 1

today = datetime.date.today()

with open('prev_fire_names.json', encoding='utf-8') as json_file:
    fire_prev = json.load(json_file)

name = pag.prompt(text='', title='姓名查詢' , default='').replace(' ', '')
print(name)

while name:
    if name not in fire_prev: pag.alert(text='火化資料查無此人', title='姓名查詢', button='OK')
    else:
        date = fire_prev[name]

        jg_names = get_jg_names()
        fr_names = get_freeze_names()
        sz_names = get_sz_names()
        rl_names = get_rl_names(str(today.year - 1911) + date, 10)
        dg_names = get_dg_names(str(today.year - 1911) + date, 10)
        gj_names = get_gj_names(str(today.year - 1911) + date, 10)
        fi_names = get_fire_names_with_time(str(today.year - 1911) + date)
        
        if PRINT:
            print("fr_names:")
            print(fr_names)
            print()
            
            print("sz_names:")
            print(sz_names)
            print()
            
            print("rl_names:")
            print(rl_names)
            print()
            
            print("dg_names:")
            print(dg_names)
            print()
            
            print("gj_names:")
            print(gj_names)
            print()
            
            print("fi_names:")
            print(fi_names)
            print()

        text = name + ': '
        if name in jg_names: text += ("寄棺:[" + jg_names[name] + ']; ')
        if name in fr_names: text += ("冷凍:[" + fr_names[name] + ']; ')
        if name in sz_names: text += ("神主:[" + sz_names[name] + ']; ')
        if name in rl_names: text += ("入殮室:[" + str(rl_names[name][0]) + '] 日期[' + str(rl_names[name][-1]) + '] 時間[' + str(rl_names[name][1]) + ']; ')
        if name in dg_names: text += ("多功能室:[" + str(dg_names[name][0]) + '] 日期[' + str(dg_names[name][-1]) + '] 時間[' + str(dg_names[name][1]) + ']; ')
        if name in gj_names: text += ("公祭日期:[" + str(gj_names[name][2][4:]).replace('/', '') + '] 時間[' + str(gj_names[name][3]) + '] 地點[' + str(gj_names[name][4]) + ']; ')
        if name in fi_names: text += ("火化日期:[" + date + '] 時間[' + str(fi_names[name]) + ']\n')
        print(text)
        pag.alert(text=text, title='結果', button='OK')


    name = pag.prompt(text='', title='姓名查詢' , default='')