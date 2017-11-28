# -*- coding: utf-8 -*-
"""
Created on Fri Nov 24 14:46:31 2017

@author: mdlayeeque.urrehman
"""

#!/bin/python

from flask import Flask, jsonify,abort,request
from flask_cors import CORS
import urllib.request
 
from bs4 import BeautifulSoup
app = Flask(__name__)
CORS(app)


tasks = [
    {
        'id': 1,
        'title': u'Buy groceries',
        'description': u'Milk, Cheese, Pizza, Fruit, Tylenol',
        'done': False
    },
    {
        'id': 2,
        'title': u'Learn Python',
        'description': u'Need to find a good Python tutorial on the web',
        'done': False
    }
]

@app.route('/todo/api/v1.0/tasks', methods=['GET'])
def get_tasks():
    return jsonify({'tasks': tasks})

@app.route('/todo/api/v1.0/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    task = [task for task in tasks if task['id'] == task_id]
    if len(task) == 0:
        abort(404)
    return jsonify({'task': task[0]})
	
	
@app.route('/todo/api/v1.0/tasks', methods=['POST'])
def create_task():
    if not request.json or not 'title' in request.json:
        abort(400)
    
    print (request.json['title'])
    
  
    articleURL="http://www.indiacelebrating.com/essay/india-essay/"
    from urllib.request import urlopen

    page=urllib.request.urlopen(articleURL).read().decode('utf8','ignore')
    soup=BeautifulSoup(page,"lxml")
#finding the content in <p> and joining them
    text1=''.join(map(lambda p:p.text,soup.find_all('p')))


    from nltk.tokenize import sent_tokenize,word_tokenize
    from nltk.corpus import stopwords
    from string import punctuation
    text=request.json['title']

#spliting the sentences
    sents=sent_tokenize(text)

#splitting the words
    word_sent=word_tokenize(text.lower())

#removing all the stopwords

    stopwords=set(stopwords.words('english')+list(punctuation))
    word_sent=[word for word in word_sent if word not in stopwords]
#print(word_sent)

#finding the probability of the words and assigning them the score depending upon its occurrence
    from nltk.probability import FreqDist
    freq=FreqDist(word_sent)
#finding the sentence and allocating them score depending upon the scores of the words it is containing

    from heapq import nlargest
#printing top 10 sentences having maximum probability 
    print(nlargest(10,freq,key=freq.get))


    from collections import defaultdict
    ranking = defaultdict(int)
    for i,sent in enumerate(sents):
        for w in word_tokenize(sent.lower()):
            if w in freq:
                ranking[i]+= freq[w]
            
    print(ranking)
    retdat=[]
    
#top 4 sentences are printed
    sents_idx=nlargest(4,ranking,key=ranking.get)
    print(sents_idx)  
    for j in sorted(sents_idx):
        retdat.append(sents[j])
    
    #return jsonify({'task': retdat}), 201 
    return (','.join(retdat))

   
if __name__ == '__main__':   app.run(host='0.0.0.0',debug=True)