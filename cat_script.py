from smtp_config import to_mail, from_mail, password, server_name
import requests
import os
import json
import smtplib
import time


FILE_NAME = 'cat_facts.json'     # Файл для сохранения фактов
NUM_FACTS = 2                   # Количество фактов
OLDNESS = 5                     # Время в минутах


# Получаем факты
res = requests.get(f'https://cat-fact.herokuapp.com/facts/random?animal_type=cat&amount={NUM_FACTS}')


# Проверка для ислючения ошибок, если файл пуст или файла не существует
if os.path.isfile(FILE_NAME):
    if os.path.getsize(FILE_NAME):
        with open(FILE_NAME, 'r') as file:      # Забираем данные, которые уже есть в файле
            fact_data = json.load(file)
    else:
        fact_data = []
else:
    with open(FILE_NAME, 'w') as file:
        fact_data = []


# Формируем факт и данные о нем, с которыми мы будем работать
for fact in res.json():
    new_fact = {
        'fact': fact['text'],
        'mail': 'Did`t sent',
        'norm_time': time.ctime(time.time()),
        'time': time.time()
    }
    fact_data.append(new_fact)


# Цикл для подсчета фактов для почты(и времени)
pos_first_mail_fact = -1        # Первый неотправленный по почте факт
pos_last_time_fact = 0          # Последний устаревший факт
mail_facts = 0                  # Количество неотправленных фактов
for i in range(len(fact_data)):
    if fact_data[i]['mail'] == 'Did`t sent':
        mail_facts += 1
        if pos_first_mail_fact == -1:
            pos_first_mail_fact = i
    if time.time() - fact_data[i]['time'] > OLDNESS * 60:
        pos_last_time_fact += 1


print(pos_first_mail_fact)
print(pos_last_time_fact)
print(mail_facts)


# Отпаравляем факты
if mail_facts > 10:
    smtp_server = smtplib.SMTP(server_name)
    smtp_server.starttls()
    smtp_server.login(from_mail, password)
    message = json.dumps(fact_data[pos_first_mail_fact:], indent=2)
    smtp_server.sendmail(from_mail, to_mail, message)
    smtp_server.quit()
    for i in range(pos_first_mail_fact, len(fact_data)):
        fact_data[i]['mail'] = 'Sent'


if pos_last_time_fact != 0:
    del fact_data[0:pos_last_time_fact]


# Записываем обновленные данные в файл
with open(FILE_NAME, 'w') as updated_file:
    json.dump(fact_data, updated_file, indent=2)
