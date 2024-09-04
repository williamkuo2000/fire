from get_names import get_freeze_names, get_fire_names, get_jg_names, get_sz_names, get_fire_names_ND

import json
import datetime
import requests

import os
from dotenv import load_dotenv
load_dotenv()



SEND_JAMES = 1
SEND_WILLK = 1
WRITE_FILE = 1


today = datetime.date.today()
date = str(today.year - 1911)
if today.month < 10: date += "0"
date += str(today.month)
if today.day < 10: date += "0"
date += str(today.day)
print("Date: " + date)

prev_fire_names = set()
with open('prev_fire_names.json', encoding='utf-8') as json_file:
    pfn = json.load(json_file)
for name, d in pfn.items():
    prev_fire_names.add(name)

print("prev_fire_name:")
print(prev_fire_names)
print()

curr_fire_names = get_fire_names_ND(date, 30)
print("curr_fire_name:")
print(curr_fire_names)
print()

enter = set()
for name, d in curr_fire_names.items():
    if name not in prev_fire_names: enter.add(name)

leave = set()
for name in prev_fire_names:
    if name not in curr_fire_names: leave.add(name)

print("enter:")
print(enter)
print()

print("leave:")
print(leave)
print()

dict_fr_nameid = get_freeze_names()
dict_jg_nameid = get_jg_names()
dict_sz_nameid = get_sz_names()


# 寄棺移出比對
jg_out = []
with open('prev_jg_names.json', encoding='utf-8') as json_file:
    jg_prev = json.load(json_file)
for name, id in jg_prev.items():
    if name not in dict_jg_nameid and name in curr_fire_names:
        if curr_fire_names[name] != str(date)[3:]: jg_out.append(name)

# 神主移出比對
sz_out = []
with open('prev_sz_names.json', encoding='utf-8') as json_file:
    sz_prev = json.load(json_file)
for name, id in sz_prev.items():
    if name not in dict_sz_nameid and name in curr_fire_names:
        if curr_fire_names[name] != str(date)[3:]: sz_out.append(name)

# 冷凍移出比對
fr_out = []
with open('prev_freeze_names.json', encoding='utf-8') as json_file:
    fr_prev = json.load(json_file)
for name, id in fr_prev.items():
    if name not in dict_fr_nameid and name in curr_fire_names:
        if curr_fire_names[name] != str(date)[3:]: fr_out.append(name)




print("----------移出----------")
print("冷凍:")
print(fr_out)
print()

print("寄棺:")
print(jg_out)
print()

print("神主:")
print(sz_out)
print()


# 火化寄棺比對
jg = []
for name in enter.copy():
    if name in dict_jg_nameid:
        jg.append([int(dict_jg_nameid[name]), name, curr_fire_names[name]])
        enter.discard(name)

# 火化神主比對
sz = []
for name in enter.copy():
    if name in dict_sz_nameid:
        sz.append([int(dict_sz_nameid[name]), name, curr_fire_names[name]])
        enter.discard(name)

# 火化冷凍比對
fr = []
for name in enter.copy():
    if name in dict_fr_nameid:
        fr.append([int(dict_fr_nameid[name]), name, curr_fire_names[name]])
        enter.discard(name)

print("----------新增----------")
print("冷凍:")
print(fr)
print()

print("寄棺:")
print(jg)
print()

print("神主:")
print(sz)
print()

print("待查:")
print(enter)
print()

nl = 2

text = "Date: " + str(date[0:3]) + '/' + str(date[3:5]) + '/' + str(date[5:]) + '\n\n'
text += "------------移出------------"


text += "\n寄棺：\n"
i = 1
for person in jg_out:
    text += (person + ' (' + curr_fire_names[person] + ') ')
    if i % nl == 0: text += '\n'
    i += 1

text += "\n\n神主：\n"
i = 1
for person in sz_out:
    text += (person + ' (' + curr_fire_names[person] + ') ')
    if i % nl == 0: text += '\n'
    i += 1

text += "\n\n冷凍：\n"
i = 1
for person in fr_out:
    if person in jg_out or person in sz_out: text += '*'
    text += (person + ' (' + curr_fire_names[person] + ') ')
    if i % nl == 0: text += '\n'
    i += 1


text += "\n------------新增------------"


text += "\n寄棺：\n"
i = 1
for person in sorted(jg, key=lambda x: x[0]): 
    text += (str(person[0]) + ' ' + str(person[1]) + ' (' + curr_fire_names[person[1]] + ') ')
    if i % nl == 0: text += '\n'
    i += 1

text += "\n\n神主：\n"
i = 1
for person in sorted(sz, key=lambda x: x[0]): 
    text += (str(person[0]) + ' ' + str(person[1]) + ' (' + curr_fire_names[person[1]] + ') ')
    if i % nl == 0: text += '\n'
    i += 1

text += "\n\n冷凍：\n"
i = 1
for person in sorted(fr, key=lambda x: x[0]):
    text += (str(person[0]) + ' ' + str(person[1]) + ' (' + curr_fire_names[person[1]] + ') ')
    if i % nl == 0: text += '\n'
    i += 1

text += "\n\n待查：\n"
i = 1
for name in enter: 
    text += (str(name) + ' (' + curr_fire_names[name] + ') ')
    if i % nl == 0: text += '\n'
    i += 1

james1_bearer = os.getenv('james1_bearer')
james1_id = os.getenv('james1_id')
james2_bearer = os.getenv('james2_bearer')
james2_id = os.getenv('james2_id')
william_bearer = os.getenv('william_bearer')
william_id = os.getenv('william_id')

if SEND_JAMES:
    headers = {'Authorization':'Bearer ' + james1_bearer,'Content-Type':'application/json'}
    body = {
        'to':james1_id,
        'messages':[{
                'type': 'text',
                'text': text
            }]
        }
    req = requests.request('POST', 'https://api.line.me/v2/bot/message/push', headers=headers, data=json.dumps(body).encode('utf-8'))
    print(req.text)

    headers = {'Authorization':'Bearer ' + james2_bearer,'Content-Type':'application/json'}
    body = {
        'to':james2_id,
        'messages':[{
                'type': 'text',
                'text': text
            }]
        }
    req = requests.request('POST', 'https://api.line.me/v2/bot/message/push', headers=headers, data=json.dumps(body).encode('utf-8'))
    print(req.text)

if SEND_WILLK:
    headers = {'Authorization':'Bearer ' + william_bearer,'Content-Type':'application/json'}
    body = {
        'to':william_id,
        'messages':[{
                'type': 'text',
                'text': text
            }]
        }
    req = requests.request('POST', 'https://api.line.me/v2/bot/message/push', headers=headers, data=json.dumps(body).encode('utf-8'))
    print(req.text)

if WRITE_FILE:
    with open('prev_fire_names.json', encoding='utf-8') as json_file, open("record.json", 'w', encoding='utf-8') as rec:
        rec.write(json_file.read())

    with open('prev_fire_names.json', 'w', encoding='utf-8') as fp:
        json.dump(curr_fire_names, fp, ensure_ascii=False)

    with open('prev_freeze_names.json', 'w', encoding='utf-8') as fp:
        json.dump(dict_fr_nameid, fp, ensure_ascii=False)
    with open('prev_jg_names.json', 'w', encoding='utf-8') as fp:
        json.dump(dict_jg_nameid, fp, ensure_ascii=False)
    with open('prev_sz_names.json', 'w', encoding='utf-8') as fp:
        json.dump(dict_sz_nameid, fp, ensure_ascii=False)