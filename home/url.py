# -*- coding: utf-8 -*-
"""URL.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1jAtpy-dWvO1qwbDty7SyyJ5q7yYb8P4x
"""

# Commented out IPython magic to ensure Python compatibility.
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
# %matplotlib inline

# import module
import requests
import pandas as pd
from bs4 import BeautifulSoup
  
def getdata(x):
    r = requests.get(x)
    soup = BeautifulSoup(r.text, 'html.parser')
    data = ''
    article = ''
    for data in soup.find_all("p"):
        article=article+(data.get_text())
    return article
# link for extract html data
if __name__ == "__main__":

    article=''
    url = "https://www.hellomagazine.com/royalty/20230114161788/    prince-william-princess-kate-travel-to-greece-constantine-funeral/"
    htmldata = getdata(url)
    soup = BeautifulSoup(htmldata, 'html.parser')
    data = ''

    for data in soup.find_all("p"):
        article=article+(data.get_text())

    article
    print(article)

    """##Summarizer"""

def summarizer(article, x):
    import torch
    from transformers import AutoTokenizer, AutoModelWithLMHead

    #Downloading tokenizer and model:

    tokenizer = AutoTokenizer.from_pretrained('t5-base')
    model = AutoModelWithLMHead.from_pretrained('t5-base', return_dict=True)


    import torch
    from transformers import AutoTokenizer, AutoModelWithLMHead

    #Downloading tokenizer and model:

    tokenizer = AutoTokenizer.from_pretrained('t5-base')
    model = AutoModelWithLMHead.from_pretrained('t5-base', return_dict=True)

    import string
    import re
    def review_cleaning(text):
        '''Make text lowercase, remove text in square brackets,remove links,remove punctuation
        and remove words containing numbers.'''
        # text = str(text).lower()
        text = re.sub('\[.*?\]', ' ', text)
        text = re.sub('https?://\S+|www\.\S+', ' ', text)
        text = re.sub('<.*?>+', ' ', text)
        text = re.sub('[%s]' % re.escape(string.punctuation), ' ', text)
        text = re.sub('\n', ' ', text)
        text = re.sub("'",' ',text)
        # text = re.sub('\w*\d\w*', '', text)
        return text

    article=review_cleaning(article)
    article
    maxi=x

    sequence = article
    inputs = tokenizer.encode('summarize: '+ sequence, return_tensors='pt', max_length = 512, truncation = True)
    outputs = model.generate(inputs,min_length = 80, max_length = maxi,length_penalty = 5, num_beams=2)
    summary = tokenizer.decode(outputs[0])
    length = len(summary)
    return (summary[6:length-4])

    # text_to_speech=summary[6:length-4]

    # from gtts import gTTS
    # from IPython.display import Audio
    # tts = gTTS(text_to_speech)
    # tts.save('1.wav')
    # sound_file = '1.wav'
    # Audio(sound_file, autoplay=True)

    """##Fake News """
def fake_news_detection(article):
    import re
    import nltk
    from nltk.corpus import stopwords
    from nltk import WordNetLemmatizer
    from nltk.tokenize import word_tokenize

    nltk.download('stopwords')
    nltk.download('wordnet')
    nltk.download('omw-1.4')
    nltk.download('punkt')
    nltk.download('averaged_perceptron_tagger')

    print('hello')
    lemmatizer = WordNetLemmatizer()
    from nltk.corpus import wordnet
    # Define function to lemmatize each word with its POS tag
    print('hello1')
    # POS_TAGGER_FUNCTION : TYPE 1
    def pos_tagger(nltk_tag):
        if nltk_tag.startswith('J'):
            return wordnet.ADJ
        elif nltk_tag.startswith('V'):
            return wordnet.VERB
        elif nltk_tag.startswith('N'):
            return wordnet.NOUN
        elif nltk_tag.startswith('R'):
            return wordnet.ADV
        else:         
            return None

    pos_tagged = nltk.pos_tag(nltk.word_tokenize(article)) 
    print('hello2')
    wordnet_tagged = list(map(lambda x: (x[0], pos_tagger(x[1])), pos_tagged))

    lemmatized_sentence = []
    for word, tag in wordnet_tagged:
        if tag is None:
            # if there is no available tag, append the token as is
            lemmatized_sentence.append(word)
        else:       
            # else use the tag to lemmatize the token
            lemmatized_sentence.append(lemmatizer.lemmatize(word, tag))
    lemmatized_sentence = " ".join(lemmatized_sentence)

    print(lemmatized_sentence)

    import string
    def review_cleaning(text):
        '''Make text lowercase, remove text in square brackets,remove links,remove punctuation
        and remove words containing numbers.'''
        text = str(text).lower()
        text = re.sub('\[.*?\]', '', text)
        text = re.sub('https?://\S+|www\.\S+', '', text)
        text = re.sub('<.*?>+', '', text)
        text = re.sub('[%s]' % re.escape(string.punctuation), '', text)
        text = re.sub('\n', '', text)
        text = re.sub("'",'',text)
        text = re.sub('\w*\d\w*', '', text)
        return text

    article=review_cleaning(lemmatized_sentence)
    print(article)

    import re
    pattern = re.compile(r'\b(' + r'|'.join(stopwords.words('english')) + r')\b\s*')
    text = pattern.sub('', lemmatized_sentence)

    #Removing additional whitespaces 
    article = re.sub('\s+', ' ', text)

    print(article)
    print("imp joblib")
    import joblib

    print("init vectorizer")

    vectorizer = joblib.load('C:\\Users\\hp\\Documents\\Git\\SyntaxError2023\\Sceptique\\PythonNoteBooks\\Model\\Tfidf_vectorizer.sav')
    print("lets vectorize")
    X_test = vectorizer.transform([article])

    print("get model")

    model=joblib.load('C:\\Users\\hp\\Documents\\Git\\SyntaxError2023\\Sceptique\\PythonNoteBooks\\Model\\finalized_model.sav')
    
    print("make predict")

    prediction = model.predict(X_test)
    print(prediction)

    if (prediction[0]==0):
      print('The news is Real')
    else:
      print('The news is Fake')

    """##Sentiment Analysis"""


    
def score_flair(text1):
    import nltk
    nltk.download('punkt')

    import torch
    import flair

    from flair.models import TextClassifier
    from flair.data import Sentence
    from segtok.segmenter import split_single
    classifier = TextClassifier.load('en-sentiment')

    str(text1)
    sentence = Sentence(text1)
    classifier = TextClassifier.load('en-sentiment')
    classifier.predict(sentence)
    score = sentence.labels[0].score
    value = sentence.labels[0].value
    return score, value

def sentiment_analysis(text):
    return ("Sentiment Analysis of the given article is "+score_flair(text)[1])