import numpy as np
import tensorflow as tf
from tensorflow.python.keras.backend import set_session
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import MinMaxScaler
from typing import Tuple, List, Optional
import json

sess = tf.Session()
set_session(sess)
graph = tf.get_default_graph() 

def getModel() -> Optional[tf.keras.Sequential]:
    ARTICLES = []
    X = []
    Y = []
    try:
        with open("json_training_data_2.json", "r") as f:
            data = json.load(f)
            ARTICLES = data["ARTICLES"]
            X = np.array(data["X"])
            Y = np.array(data["Y"])
    except IOError:
        return None
    scaler = MinMaxScaler()
    scaler.fit(X)
    normalizedX = scaler.transform(X)
    model = tf.keras.Sequential([
        tf.keras.layers.Dense(units = 1, input_shape=(normalizedX.shape[1],), activation='sigmoid'),
    ])
    model.compile(optimizer='sgd', loss='mse')
    train_history = model.fit(normalizedX, Y, epochs=20000)
    return model, scaler

model, scaler = getModel()

import requests
import bs4 as bs
import urllib.request
import re
import nltk
import csv
from ibm_watson import ToneAnalyzerV3
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
import json
import string
from spellchecker import SpellChecker
from nltk.tokenize import word_tokenize 

quoteRegex = re.compile('“|”|‘|’\s|’[.,;:!?]')

nltk.download('punkt')
nltk.download('stopwords')

LOG = True

class Gsearch_python:
    def getSiteText(self, url):
        try:
            scraped_data = requests.get(url)
            article = scraped_data.text
            parsed_article = bs.BeautifulSoup(str.encode(article),'html.parser')
            #BBC Covid: Confusion over fresh talks in Manchester tier row - BBC News
            #New Scientist: Covid-19 news: Remdesivir has little effect on survival, finds WHO | New Scientist
            #GOV.UK: Coronavirus (COVID-19): guidance and support - GOV.UK
            #CDC: COVID-19 in the United Kingdom - Warning - Level 3, Avoid Nonessential Travel - Travel Health Notices | Travelers' Health | CDC
            #Express: Jeremy Corbyn HUMILIATION: Former Labour leader flouts COVID rules at ‘memorial carnival’  | UK | News | Express.co.uk
            #Daily Mail: Global coronavirus cases rise by more than 400,000 in one day for the first time | Daily Mail Online
            #Daily Star: Brits told to self-isolate by NHS Test and Trace may have details handed to police - Daily Star
            #London Evening Standard: UK coronavirus deaths up by 150 as cases jump by 16,171 | London Evening Standard
            #Financial Times: Colombia after Covid-19 | Financial Times
            #The Guardian: Coronavirus: 1 million young Britons ‘face jobs crisis within weeks’ | Coronavirus | The Guardian
            #Metro News: More than 220 Cambridge students told to self-isolate after 18 cases in halls | Metro News
            #CNN: Britain's BAME communities cherished multigenerational living. But Covid-19 has changed all that - CNN
            #Independent: Coronavirus has made me into an undocumented immigrant in my home country
            #The Sun Hope Hicks joins Trump at rally after both recovered from Covid-19 and jokes 'now we can share a microphone'
            title = ""
            try:
                titletag = parsed_article.find_all('title')
                title = titletag[0].text
                firstHyphen = title.find(" - ")
                firstPipe = title.find("|")
                if firstHyphen == -1 and firstPipe == -1:
                    title = title.strip()
                elif firstPipe == -1:
                    title = title[:firstHyphen].strip()
                elif firstHyphen == -1:
                    title = title[:firstPipe].strip()
                else:
                    title = title[:min(firstHyphen, firstPipe)].strip()
            except:
                if LOG: print("Bad title")
            everything = parsed_article.find_all('div')
            paragraphs = parsed_article.find_all('p')
            links = parsed_article.find_all('a')
            article_text = ""
            everything_text = ""

            for p in paragraphs:
                article_text += p.text
                article_text += "\n"

            for x in everything:
                everything_text += x.text
                everything_text += "\n"

            return article_text, len(links), title
        except:
            return None
    
    def isSwearWord(self, word):
        f = open("swearWordsList.txt", "r")
        for swearWord in f:
            swearWord = swearWord.rstrip("\n")
            swearWord = swearWord.rstrip(" ")
            if swearWord.lower() == word.lower():
                return True
        return False

    """
    Anger
    Fear
    Joy
    Sadness
    Analytical
    Confident
    Tentative
    """
    def getTones(self, text):
        TONE_API = {
            "apikey": "QReFQmlHOdwOU2hUiWPOR42hwi6__BKZFhcfw911Io69",
            "iam_apikey_description": "Auto-generated for key 96589917-9846-4122-ad95-d7a60221dac8",
            "iam_apikey_name": "Auto-generated service credentials",
            "iam_role_crn": "crn:v1:bluemix:public:iam::::serviceRole:Manager",
            "iam_serviceid_crn": "crn:v1:bluemix:public:iam-identity::a/15b5a37df3ea5dc8f6602c7a241775d5::serviceid:ServiceId-3c75134f-9b47-417d-8894-6410345ea2f7",
            "url": "https://api.us-south.tone-analyzer.watson.cloud.ibm.com/instances/0c24a35a-1e1a-4363-9e72-44535d4d5eb1"
        }
        authenticator = IAMAuthenticator(TONE_API["apikey"])
        toneAnalyzer = ToneAnalyzerV3(
            version='2017-09-21',
            authenticator=authenticator
        )
        toneAnalyzer.set_service_url(TONE_API["url"])
        return toneAnalyzer.tone(
            {'text': text},
            content_type='application/json'
        ).get_result()

    def getUrls(self):
        urls = []
        scores = []
        prov = []
        with open('training_data_2.csv') as csvfile:
            fileReader = csv.reader(csvfile, delimiter=',')
            for line in fileReader:
                prov.append(line[0])
                link = line[1].rstrip("\n")
                urls.append(link)
                scores.append(float(line[2]))
        if(LOG):
            # print(urls)
            # print(scores)
            print()
        return urls, prov, scores
        
        '''
        for u in f:
            swearWord = swearWord.rstrip("\n")
            swearWord = swearWord.rstrip(" ")
            
                return True
        return False
        '''

def runUrl(url):
    gs = Gsearch_python()
    dictionary = dict()
    xVals = []
    articleVals = []
    res = gs.getSiteText(url)
    if res != None:
        text = res[0]
        if len(text.encode('utf-8')) < 131072 or True:
            numLinks = res[1]
            if LOG: print(numLinks)
            title = res[2]
        
            quotationCount = 0

            for i in range(len(text)-1):
                quotationCount += len(re.findall(quoteRegex, text[i:i+1]))
            quotationCount += len(re.findall(quoteRegex, text[-1]))
            """
            for char in text:
                if  (not char.isalpha()) and char == '”' or char == '“':
                    quotationCount += 1
            """
            if(quotationCount % 2 == 1):
                quotationCount += 1
            quotationCount /= 2
            if LOG: print(url, quotationCount)

            # Tone analyzation
            
            joyScore = float(0.00)
            fearScore = float(0.00)
            sadnessScore = float(0.00)
            angerScore = float(0.00)
            analyticalScore = float(0.00)
            confidentScore = float(0.00)
            tentativeScore = float(0.00)
            for tone in gs.getTones(text)['document_tone']['tones']:
                if tone['tone_name'] == "Joy":
                    joyScore = float(tone['score'])
                elif tone['tone_name'] == "Fear":
                    fearScore = float(tone['score'])
                elif tone['tone_name'] == "Sadness":
                    sadnessScore = float(tone['score'])
                if tone['tone_name'] == "Anger":
                    angerScore = float(tone['score'])
                if tone['tone_name'] == "Analytical":
                    analyticalScore = float(tone['score'])
                if tone['tone_name'] == "Confident":
                    confidentScore = float(tone['score'])
                if tone['tone_name'] == "Tentative":
                    tentativeScore = float(tone['score'])

            
            textListFull = word_tokenize(text)
            textList = [word for word in textListFull if word.isalpha()]


            # figure out reader mode
            # [done] run things like the mood sentiment, get those scores
                # Joy, Fear, Sadness, Anger, Analytical, Confident, and Tentative
            # [done] hyperlinks (count the number of <a href> tags), is this possible in reader modes?
            # [done] find number of swear words. just .contains off of a pre-existed text file
            # [done] typo count. go through english dictionary, if word is not there then consider it type - binary search, maybe scratch
            # [done] quotation count, just go through and count lol
            # top word frequency - use nltk
            # input it into a json and give that json to ignacio
                # each score/data point is a separate column
            # [done] get a list of working websites (we can start with out existing ones)

            numSwearWords = 0
            numTypo = 0
            spell = SpellChecker()
            spell.word_frequency.load_words(['covid', 'quarantining', 'sanitizing', 'hospitalizations', 'website', 'COVID-19'])
            wordCount = len(textList)

            for word in textList:
                numTypo += len(spell.unknown([word]))
                if gs.isSwearWord(word):
                    numSwearWords += 1
            xVals.append([quotationCount, joyScore, fearScore, sadnessScore, angerScore, analyticalScore, confidentScore, tentativeScore, numTypo, numSwearWords, numLinks, wordCount])
        newX = scaler.transform(np.array([xVals[0]]))
        global graph
        global sess
        set_session(sess)
        print(newX)
        try:
            with graph.as_default():
                Y = model.predict(newX)
        except ex:
            print(ex)
        print("GOT Y")
        return {
            "url": url,
            "title": title,
            "score": float(Y[0][0])
        }
    return {}


from flask import Flask
from flask import render_template, request, jsonify
from flask_restful import Api, Resource

app = Flask(__name__)
app._static_folder = "./"
api = Api(app)

# flask requires this to be in a subdirectory called templates/
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/evaluate/')
def evaluate():
    try:
        response = runUrl(request.args.get("url"))
        return json.dumps(response)
    except:
        return "An error has occurred"

# Classes
class HelloWorld(Resource):
    # override
    def get(self):
        # return as json object
        return {None}

# Resources

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port = 80, use_reloader=False)
    #app.run(debug=True)