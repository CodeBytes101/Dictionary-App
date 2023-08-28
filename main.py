import requests
from bs4 import BeautifulSoup
import json
from flask import Flask,render_template,request

with open("dailyword.json", "r") as file:
    data = json.load(file)

def define(word):
    response = requests.get("https://api.dictionaryapi.dev/api/v2/entries/en/"+word)

    if response.status_code == 200:
        data = response.json()[0]
        definition = data['meanings'][0]['definitions'][0]['definition']
        synonyms = data['meanings'][0]['definitions'][0]['synonyms']
        antonyms = data['meanings'][0]['definitions'][0]['antonyms']
        return definition ,synonyms,antonyms


def get_word_of_the_day():
    response = requests.get("https://www.merriam-webster.com/word-of-the-day")
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")
        word_element = soup.find("h2", class_="word-header-txt")
        definition_element = soup.find("p")
        
        if word_element :
            word = word_element.get_text().strip()
            definition = definition_element.get_text().strip()
            return word ,definition

def word_inserter(data):
    
    word ,definition = get_word_of_the_day()
    if data['word'] == '' or data['word'] != word:
        daily_word = {"word":word,"definition":definition}
        with open("dailyword.json",'w') as file:
            json.dump(daily_word,file)
            



app = Flask(__name__)

@app.route('/')
def home():
    word_inserter(data)
    return render_template('index.html',data = data)


@app.route('/search',methods = ["GET","POST"])
def search_word():
    if request.method == 'POST':
        word = request.form.get('word')
        definition ,synonyms ,antonyms = define(word)
        return render_template('result.html',word= word , definition = definition,synonyms = synonyms,antonyms=antonyms)
    else:
        return render_template('search.html')

if __name__ == '__main__':
    app.run(debug=True)