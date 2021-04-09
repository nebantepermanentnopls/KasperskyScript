import requests
import os
import json

# Файл для сохранения фактов
file_name = 'CatFacts.json'
# Получаем факты(задание 1)
res = requests.get("https://cat-fact.herokuapp.com/facts/random?animal_type=cat&amount=2")

# Проверка для ислючения ошибок, если файл пуст или файла не существует
if os.path.isfile(file_name):
    if os.path.getsize(file_name):
        with open(file_name, 'r') as file:      # Забираем данные, которые уже есть в файле
            fact_data = json.load(file)
    else:
        fact_data = []
else:
    with open(file_name, 'w') as file:
        fact_data = []

# Формируем факт и данные о нем, с которыми нам будет удобно работать
for fact in res.json():
    new_fact = {
        'fact': fact['text'],
        'mail': False,
        'time': False
    }
    fact_data.append(new_fact)

# Записываем обновленные данные в файл
with open(file_name, 'w') as updated_file:
    json.dump(fact_data, updated_file, indent=2)
