import requests
word =  'sarcasm'
url = "https://api.dictionaryapi.dev/api/v2/entries/en/"

response = requests.get(url+word)
if response.status_code == 200:
    data = response.json()[0]
    print("The word is : ",data['word'])
    print(f"The Definition is : {data['meanings'][0]['definitions'][0]['definition']}")
    print(f"synonyms : {data['meanings'][0]['definitions'][0]['synonyms']}")
    print(f"antonyms : {data['meanings'][0]['definitions'][0]['antonyms']}")

