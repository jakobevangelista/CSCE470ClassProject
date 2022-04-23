import os
import tweepy
import pandas as pd
import json
import requests
import config

consumer_key = config.consumer_key
consumer_secret = config.consumer_secret
bearer_token = config.bearer_token
access_token = config.access_token
access_token_secret = config.access_token_secret

# client = tweepy.Client(bearer_token=bearer_token, consumer_key=consumer_key, consumer_secret=consumer_secret, access_token=access_token, access_token_secret=access_token_secret, return_type=requests.Response)
client = tweepy.Client(bearer_token=bearer_token, consumer_key=consumer_key, consumer_secret=consumer_secret, access_token=access_token, access_token_secret=access_token_secret, return_type=requests.Response)

query = "powerlifting"
finalQuery = query + str(" -is:retweet")

tweets = client.search_recent_tweets(finalQuery, tweet_fields=['public_metrics'],sort_order="relevancy" ,max_results=100)

tweets_dict = tweets.json()

tweets_data = tweets_dict['data']
df = pd.json_normalize(tweets_data)
df.to_json("tweets.json")
print(df)
