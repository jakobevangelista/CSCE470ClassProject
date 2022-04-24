from flask import Flask,render_template, redirect, url_for, request, flash
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

import string
import os
import tweepy
import pandas as pd
import json
import requests
import config
import re
from textblob import TextBlob 
import nltk
from nltk.corpus import stopwords

consumer_key = config.consumer_key
consumer_secret = config.consumer_secret
bearer_token = config.bearer_token
access_token = config.access_token
access_token_secret = config.access_token_secret

stp = stopwords.words('english')

#constants that add up to 1
k1 = .7
k2 = .3
beta = 0.001

# client = tweepy.Client(bearer_token=bearer_token, consumer_key=consumer_key, consumer_secret=consumer_secret, access_token=access_token, access_token_secret=access_token_secret, return_type=requests.Response)
client = tweepy.Client(bearer_token=bearer_token, consumer_key=consumer_key, consumer_secret=consumer_secret, access_token=access_token, access_token_secret=access_token_secret, return_type=requests.Response)

app = Flask(__name__)

app.config['SECRET_KEY'] = 'C2HWGVoMGfNTBsrYQg8EcMrdTimkZfAb'

Bootstrap(app)
class CelebForm(FlaskForm):
    first_name = StringField("First Name: ", validators = [DataRequired()])
    last_name = StringField("Last Name: ", validators = [DataRequired()])
    submit = SubmitField('Submit')

@app.route("/", methods=('GET', 'POST'))
def index():
    error = None
    form = CelebForm()
    if form.validate_on_submit():
        name1 = form.first_name.data
        name2 = form.last_name.data
        return redirect(url_for('score', n1 = name1, n2 = name2))
    return render_template("index.html", form=form, error = error)


@app.route("/score_<n1>_<n2>")
def score(n1, n2):
    query = n1 + " " + n2
    finalQuery = query + str(" -is:retweet lang:en")
    tweets = client.search_recent_tweets(finalQuery, tweet_fields=['public_metrics'],sort_order="relevancy" ,max_results=100)
    tweets_dict = tweets.json()
    results = tweets_dict["meta"]["result_count"]
    if(results == 0):
        return redirect(url_for('index2'))
    else:
        tweets_data = tweets_dict['data']
        overall_score = 0
        generic_score = 0
        total_retweets = 0
        total_favorites = 0
        total_num_tweets = 100  
        vocab = {}
        for tweet in tweets_data:
            metrics = tweet['public_metrics']
            total_retweets += metrics['retweet_count']
            total_favorites += metrics['like_count']
        avg_retweets = total_retweets/total_num_tweets
        avg_favorites = total_favorites/total_num_tweets
        for tweet in tweets_data:
            metrics = tweet['public_metrics']
            retweets = metrics['retweet_count']
            favorites = metrics['like_count']
            replies = metrics['reply_count']
            text = tweet['text']
            sent_analysis = TextBlob(text).sentiment.polarity
            tweet_score = sent_analysis*(k1*(retweets/avg_retweets) + k2*(favorites/avg_favorites) + beta)

            # L + ratio
            if(replies > 5*favorites):
                tweet_score = -tweet_score

            overall_score += tweet_score

            text = text.replace('’',' ')
            text = text.replace('"',' ')
            text = text.replace('‘',' ')
            text = text.replace('”', ' ')
            text = text.replace('https','')
            text = text.replace('.', ' ') #get rid of periods
            text = text.replace(',', ' ') #get rid of commas
            text = text.replace('?', ' ') #get rid of question marks
            text = text.replace('!', ' ') #get rid of exclamation marks
            text = text.replace(';', ' ') #get rid of semicolons
            text = text.replace('\'', ' ')
            text = text.replace('\“', ' ')
            words = TextBlob(text).words

            for word in words:
                word = re.sub(r'\W+', '', word)
                if word.lower() not in stp:
                    if n1.lower() not in word.lower() and n2.lower() not in word.lower() and len(word)>1:
                        if word.lower() in vocab:
                            vocab[word.lower()] += 1
                        else:
                            vocab[word.lower()] = 1

        sorted_vocab = sorted(vocab.items(), key=lambda kv: kv[1], reverse = True) #vocab of tweets with term frequency
        top_ten = []
        for i in range(10):
            top_ten.append(sorted_vocab[i][0])

        overall_score = overall_score/total_num_tweets
        overall_score = overall_score*20

        if overall_score > 5:
            overall_score = 5

        if overall_score < -5:
            overall_score = -5

        return render_template("score.html", first_name = n1.capitalize(), \
        last_name = n2.capitalize(), \
        word1 = top_ten[0], \
        word2 = top_ten[1], \
        word3 = top_ten[2], \
        word4 = top_ten[3], \
        word5 = top_ten[4], \
        word6 = top_ten[5], \
        word7 = top_ten[6], \
        word8 = top_ten[7], \
        word9 = top_ten[8], \
        word10 = top_ten[9], \
        rating = overall_score)

@app.route("/invalid", methods=('GET', 'POST'))
def index2():
    error = True
    form = CelebForm()
    if form.validate_on_submit():
        name1 = form.first_name.data
        name2 = form.last_name.data
        return redirect(url_for('score', n1 = name1, n2 = name2))
    return render_template("index.html", form=form, error = error)