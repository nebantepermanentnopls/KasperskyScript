#!/bin/python3

from smtp_config import TO_MAIL, FROM_MAIL, PASSWORD, SERVER_NAME
from datetime import datetime, timedelta
import requests
import os
import json
import smtplib


FILE_NAME = 'cat_facts.json'        # Файл для сохранения фактов
NUM_FACTS = 2                       # Количество фактов
OLDNESS = 2                         # Время в минутах
MAX_NO_MAIL = 10                    # Максимальное допустимое количество неотправленных фактов


# Проверка для ислючения ошибок, если файл пуст или файла не существует
print('-----------------------------------------------')
if os.path.isfile(FILE_NAME):
    if os.path.getsize(FILE_NAME):
        print(f'File {FILE_NAME} exist, using JSON data from {FILE_NAME}')
        with open(FILE_NAME, 'r') as file:      # Забираем данные, которые уже есть в файле
            fact_data = json.load(file)
    else:
        print(f'File {FILE_NAME} is empty, let\'s start using')
        fact_data = []
else:
    print(f'File {FILE_NAME} does not exist, will created after loading facts')
    fact_data = []


# Получаем факты
print('-----------------------------------------------')
print('Uploading facts...')
res = requests.get(f'https://cat-fact.herokuapp.com/facts/random?animal_type=cat&amount={NUM_FACTS}')
print('Facts uploaded!')

# Формируем факт и данные о нем, с которыми мы будем работать
for fact in res.json():
    new_fact = {
        'fact': fact['text'],
        'mail': 'Did`t sent',
        'time': str(datetime.today())
    }
    fact_data.append(new_fact)


# Цикл для подсчета фактов для почты и времени
print('-----------------------------------------------')

mail_first_fact = -1                # Первый неотправленный по почте факт
outdated_facts = 0                  # Последний устаревший факт
for i in range(len(fact_data)):
    if fact_data[i]['mail'] == 'Did`t sent':
        if mail_first_fact == -1:
            mail_first_fact = i
    if datetime.today() - datetime.strptime(fact_data[i]['time'],
                                            '%Y-%m-%d %H:%M:%S.%f') > timedelta(days=0, minutes=OLDNESS):
        outdated_facts += 1


len_data = len(fact_data)
no_mail_facts = len(fact_data[mail_first_fact:])
print(f'Before upload facts: {len_data - NUM_FACTS}')
print(f'After upload facts: {len_data}')
print(f'Facts not sent by mail: {no_mail_facts}')
print(f'Outdated facts: {outdated_facts}')


# Отправляем факты
if no_mail_facts > MAX_NO_MAIL:
    print('-----------------------------------------------')
    print('Fact mail limit has been exceeded:')
    print(f'Sending a letter with facts to {TO_MAIL} from {FROM_MAIL}...')

    smtp_server = smtplib.SMTP(SERVER_NAME)
    smtp_server.starttls()
    smtp_server.login(FROM_MAIL, PASSWORD)
    message = json.dumps(fact_data[mail_first_fact:], indent=2)
    smtp_server.sendmail(FROM_MAIL, TO_MAIL, message)
    smtp_server.quit()

    print('Facts were sent!!!')
    for i in range(mail_first_fact, len(fact_data)):
        fact_data[i]['mail'] = 'Sent'


# Удаляем устаревшие факты
if outdated_facts != 0:
    print('-----------------------------------------------')
    print('Outdated facts found!')
    print('Deleting outdated facts...')
    del fact_data[0:outdated_facts]
    print('Facts were removed!!!')
    print(f'Facts after remove: {len(fact_data)}')


# Записываем обновленные данные в файл
print('-----------------------------------------------')
print(f'Writing facts to {FILE_NAME}...')
with open(FILE_NAME, 'w') as updated_file:
    json.dump(fact_data, updated_file, indent=2)
print(f'Success!!! Bye bye :)')
