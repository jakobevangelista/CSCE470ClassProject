import json
import string
from textblob import TextBlob 
import nltk
#necessary the first time
#nltk.download('stopwords')
#nltk.download('punkt')
from nltk.corpus import stopwords

stp = stopwords.words('english')
table = str.maketrans('', '', string.punctuation)

#constants that add up to 1
k1 = .7
k2 = .3

first_name = 'kanye'
last_name = 'west'

first_name = input("Enter first name: ").lower();
last_name = input("Enter last name: ").lower();
file = 'testcode/' + first_name + "_" + last_name + ".json"
with open(file, 'r') as f:
  data = json.load(f)

overall_score = 0;
generic_score = 0;
total_retweets = 0;
total_favorites = 0;
total_num_tweets = 100;
vocab = {}
for tweet in data:
    total_retweets += tweet["retweet_count"];
    total_favorites += tweet["favorite_count"];

avg_retweets = total_retweets/total_num_tweets;
avg_favorites = total_favorites/total_num_tweets;
for tweet in data:
    text = tweet["full_text"];
    retweets = tweet["retweet_count"];
    favorites = tweet["favorite_count"];
    replies = tweet["reply_count"];
    sent_analysis = TextBlob(text).sentiment.polarity
    tweet_score = sent_analysis*(k1*retweets/avg_retweets + k2*favorites/avg_favorites)
    text = text.replace('’',' ');
    text = text.replace('"',' ');
    text = text.replace('‘',' ');
    text = text.replace('”', ' ');
    text = text.replace('https','');
    text = text.replace('.', ' ') #get rid of periods
    text = text.replace(',', ' ') #get rid of commas
    text = text.replace('?', ' ') #get rid of question marks
    text = text.replace('!', ' ') #get rid of exclamation marks
    text = text.replace(';', ' ') #get rid of semicolons
    words = TextBlob(text).words
    for word in words:
        if word.lower() not in stp:
            if first_name not in word.lower() and last_name not in word.lower():
                if word.lower() in vocab:
                    vocab[word.lower()] += 1
                else:
                    vocab[word.lower()] = 1
    
    # L + ratio
    if(replies > 5*favorites):
        tweet_score = -tweet_score

    overall_score += tweet_score

sorted_vocab = sorted(vocab.items(), key=lambda kv: kv[1], reverse = True) #vocab of tweets with term frequency

print(overall_score/total_num_tweets)
