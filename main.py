import bs4 as bs
import urllib.request
import re
import nltk
import csv

nltk.download('punkt')
nltk.download('stopwords')

class Gsearch_python:
    def __init__(self,name_search):
      self.name = name_search
    def Gsearch(self):
        returnMe = ""
        count = 0
        try :
            from googlesearch import search
        except ImportError:
            print("No Module named 'google' Found")
        count = 1
        for i in search(query=self.name,tld='co.in',lang='en',num=10,stop=10,pause=2):
            if count == 1:
                returnMe = i
            count += 1
        return returnMe

    def summarize(self, url):
        print("this line worked")
        try:
            scraped_data = urllib.request.urlopen(url)
            article = scraped_data.read()
            parsed_article = bs.BeautifulSoup(article,'lxml')
            paragraphs = parsed_article.find_all('div')
            article_text = ""

            for p in paragraphs:
                article_text += p.text

            # figure out reader mode
            # run things liek the mood sentiment, get those scores
            # hyperlinks (count the number of <a href> tags), is this possible in reader modes
            # find number of swear words. just .contains off of a pre-existed text file
            # typo count. go through english dictionary, if word is not there then consider it type - binary search, maybe scratch
            # quotation count, just go through and count lol
            # top word frequency - use nltk
            # input it into a json and give that json to ignacio
                # each score/data point is a separate column
            # get a list of working websites (we can start with out existing ones)

            article_text = re.sub(r'\[[0-9]*\]', ' ', article_text)
            article_text = re.sub(r'\s+', ' ', article_text)
            formatted_article_text = re.sub('[^a-zA-Z]', ' ', article_text )
            formatted_article_text = re.sub(r'\s+', ' ', formatted_article_text)
            sentence_list = nltk.sent_tokenize(article_text)
            stopwords = nltk.corpus.stopwords.words('english')
            word_frequencies = {}
            for word in nltk.word_tokenize(formatted_article_text):
                if word not in stopwords:
                    if word not in word_frequencies.keys():
                        word_frequencies[word] = 1
                    else:
                        word_frequencies[word] += 1
            maximum_frequncy = max(word_frequencies.values())

            for word in word_frequencies.keys():
                word_frequencies[word] = (word_frequencies[word]/maximum_frequncy)
            sentence_scores = {}
            for sent in sentence_list:
                for word in nltk.word_tokenize(sent.lower()):
                    if word in word_frequencies.keys():
                        if len(sent.split(' ')) < 30:
                            if sent not in sentence_scores.keys():
                                sentence_scores[sent] = word_frequencies[word]
                            else:
                                sentence_scores[sent] += word_frequencies[word]
            import heapq
            summary_sentences = heapq.nlargest(7, sentence_scores, key=sentence_scores.get)

            summary = ' '.join(summary_sentences)
            return summary
        except:
            return "Does not allow scraping"

if __name__=='__main__':
    # https://www.huffpost.com/entry/fukushima-contaminated-water_n_5f894ae4c5b6dc2d17f5a36e
    # https://teenshealth.org/en/teens/healthy-relationship.html?WT.ac=t-feat
    # nytimes, cnn, science news, ap news
    # nogo: huff, 

    url = "https://apnews.com/article/election-2020-joe-biden-russia-024b553e9a4ffb2716286dd134876f8a"
    gs = Gsearch_python(url)
    print(gs.summarize(url))

    # questions = []
    # with open('questions.csv') as csv_file:
    #     csv_reader = csv.reader(csv_file, delimiter=',')
    #     for row in csv_reader:
    #         questions.append(row)
    # for question in questions:
    #     query = question[0]
    #     query.replace("?", "")
    #     query = query + " at age 14"
    #     gs = Gsearch_python(query)
    #     urlToUse = gs.Gsearch()
    #     summary = gs.summarize(urlToUse)
    #     question.append(summary)
    #     question.append(urlToUse)
    # with open('answers.csv', mode='w') as answerfile:
    #     answers = csv.writer(answerfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    #     for row in questions:
    #         answers.writerow(row)
