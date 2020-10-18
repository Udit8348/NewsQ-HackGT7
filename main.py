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


nltk.download('punkt')
nltk.download('stopwords')

LOG = True

class Gsearch_python:
    def getSiteText(self, url):
        try:
            scraped_data = urllib.request.urlopen(url)
            article = scraped_data.read()
            parsed_article = bs.BeautifulSoup(article,'lxml')
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

            return article_text, len(links)
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
        # scores = []
        prov = []
        with open('check_data.csv') as csvfile:
            fileReader = csv.reader(csvfile, delimiter=',')
            for line in fileReader:
                prov.append(line[0])
                link = line[1].rstrip("\n")
                urls.append(link)
                # scores.append(float(line[2]))
        if(LOG):
            # print(urls)
            # print(scores)
            print()
        return urls, prov
        
        '''
        for u in f:
            swearWord = swearWord.rstrip("\n")
            swearWord = swearWord.rstrip(" ")
            
                return True
        return False
        '''

if __name__=='__main__':
    # https://www.huffpost.com/entry/fukushima-contaminated-water_n_5f894ae4c5b6dc2d17f5a36e
    # https://teenshealth.org/en/teens/healthy-relationship.html?WT.ac=t-feat
    # good: nytimes, cnn, science news, ap news
    # nogo: huff, 
    # https://apnews.com/article/election-2020-joe-biden-russia-024b553e9a4ffb2716286dd134876f8a
    # https://www.babbel.com/en/magazine/why-do-we-swear
    
    '''
        x: [quotationCount, joyScore, fearScore, sadnessScore, angerScore, analyticalScore, confidentScore, tentativeScore, numTypo, numSwearWords]
        y: Sneha's prediction
    '''

    gs = Gsearch_python()
    count = 0
    dictionary = dict()
    rescsv = gs.getUrls()
    urls = rescsv[0]
    # scores = rescsv[1]
    provider = rescsv[1]
    xVals = []
    yVals = []
    articleVals = []

    for url in urls:
        # print(url)
        res = gs.getSiteText(url)
        if res != None:
            text = res[0]
            if len(text.encode('utf-8')) < 131072:
                numLinks = res[1]
                print(numLinks)

            
                quotationCount = 0
                for char in text:
                    if  (not char.isalpha()) and char == '”' or char == '“':
                        quotationCount += 1
                if(quotationCount % 2 == 1):
                    quotationCount += 1
                quotationCount /= 2

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
                articleVals.append([provider[count], url])
                xVals.append([quotationCount, joyScore, fearScore, sadnessScore, angerScore, analyticalScore, confidentScore, tentativeScore, numTypo, numSwearWords, numLinks, wordCount])
                # yVals.append(scores[count])
        count += 1

    dictionary['ARTICLES'] = articleVals
    dictionary['X'] = xVals
    # dictionary['Y'] = yVals
    
    with open("json_check_data.json", "w") as outfile:
        json.dump(dictionary, outfile, sort_keys=True, indent=4)

    print(dictionary)