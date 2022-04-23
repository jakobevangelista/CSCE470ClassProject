import os
import tweepy
import pandas as pd
import json
import requests

consumer_key = '5A1vDXpaO5Nb7IjvhlOKGJYHJ'
consumer_secret = '3Bdy4gQSbKusUcrhoZEJ33sFgJP9uraZJ5gwPyTHJjoO4GkDXR'
bearer_token = 'AAAAAAAAAAAAAAAAAAAAAFw4aAEAAAAAiF3oT5j8LgGLE%2Bv1S%2Bl0u8vdFwo%3DnuXCRPcOW18vdmRER9UFvC7cbMgCFsh26hA2JOyjOYcTIjm99H'
access_token = '2855531916-lUxyjcAL14zQ1CtiBfhEFolju1uDb7MpPb9BvUR'
access_token_secret = 'bLbIMxgbo366SEkqu4zxxZeQ6IXCK4Rev62Y3u27Cfy9b'

client = tweepy.Client(bearer_token=bearer_token, consumer_key=consumer_key, consumer_secret=consumer_secret, access_token=access_token, access_token_secret=access_token_secret, return_type=requests.Response)

query = "powerlifting -is:retweet"
tweetText = client.search_recent_tweets(query, max_results=10)

tweets_dict = tweetText.json()

tweets_data = tweets_dict['data']

df = pd.json_normalize(tweets_data)

df.to_json("tweets.json")
print(df)
# for tweet in tweetText:
#     json_data.append(tweet)

# with open('tweets.json', 'w') as json_file:
#     json.dump(json_data, json_file)