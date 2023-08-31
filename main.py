import requests
from bs4 import BeautifulSoup
import json
from flask import Flask,render_template,request
import random
from flask_mail import Mail,Message

with open('config.json') as file:
    data = json.load(file)
    params = data['params']

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



app = Flask(__name__)

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = params['email']
app.config['MAIL_PASSWORD'] = params['pass']
app.config['MAIL_DEFAULT_SENDER'] = params['email']

mail = Mail(app)

@app.route('/')
def home():
    word,definition = get_word_of_the_day()
    quote,meaning = thought()
    return render_template('index.html',word=word,definition = definition,quote=quote,meaning=meaning)


@app.route('/search',methods = ["GET","POST"])
def search_word():
    if request.method == 'POST':
        word = request.form.get('word')
        if word:
            definition = define(word)
            if definition != None:
                return render_template('result.html',word= word,definition = definition)
            else:
                return render_template('error.html')
        else:
            return render_template('search.html')
    else:
        return render_template('search.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact',methods = ['GET','POST'])
def contact():
    if request.method =='POST':
        name = request.form.get('name')
        email = request.form.get('email')
        number = request.form.get('phone')
        msg = request.form.get('message')
        message = Message(subject=f'New Mail From {name.capitalize()}',recipients=[params['email']])
        message.body = f'{msg}\n\nNumber:{number}\n\nEmail: {email}'
        mail.send(message)
        return render_template('contact.html')
    else:    
        return render_template('contact.html')

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')