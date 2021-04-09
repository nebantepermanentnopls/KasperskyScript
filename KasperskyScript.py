import requests
import os
import json

file_name = 'CatFacts.json'
res = requests.get("https://cat-fact.herokuapp.com/facts/random?animal_type=cat&amount=2")

if os.path.isfile(file_name):
    if os.path.getsize(file_name):
        with open(file_name, 'r') as file:
            fact_data = json.load(file)
    else:
        fact_data = []
else:
    with open(file_name, 'w') as file:
        fact_data = []

for fact in res.json():
    new_fact = {
        'fact': fact['text'],
        'mail': False,
        'time': False
    }
    fact_data.append(new_fact)

with open(file_name, 'w') as updated_file:
    json.dump(fact_data, updated_file, indent=2)
