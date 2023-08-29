import requests
from bs4 import BeautifulSoup
import json
from flask import Flask,render_template,request
import random

with open("dailyword.json", "r") as file:
    data = json.load(file)

def thought():
    with open('quotes.json', 'r',encoding='utf-8') as json_file:
        data = json.load(json_file)
        quote = random.choice(list(data.keys()))
        meaning = data[quote]
        return quote,meaning


def define(word):
    response = requests.get("https://www.merriam-webster.com/dictionary/"+word)

    if response.status_code == requests.codes.ok:
        soup  = BeautifulSoup(response.content, "html.parser")
        data = soup.find('div',class_ = 'sense-content w-100')
        definition = data.text
        return definition
    else:
        return None

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
    quote,meaning = thought()
    return render_template('index.html',data = data,quote=quote,meaning=meaning)


@app.route('/search',methods = ["GET","POST"])
def search_word():
    if request.method == 'POST':
        word = request.form.get('word')
        definition = define(word)
        if definition != None:
            return render_template('result.html',word= word,definition = definition)
        else:
            return render_template('error.html')
    else:
        return render_template('search.html')


if __name__ == '__main__':
    app.run(debug=True)