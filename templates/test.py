import json
import random


def quote():
    with open('quotes.json', 'r',encoding='utf-8') as json_file:
        data = json.load(json_file)
        quote = random.choice(list(data.keys()))
        meaning = data[quote]
        return quote,meaning

print(quote())