from decouple import config
import tweepy
from textblob import TextBlob
# from datetime import date
from replit import db
import json

consumer_key = config('CONSUMER_KEY')
consumer_secret = config('CONSUMER_SECRET')
access_token = config('ACCESS_TOKEN')
access_token_secret = config('ACCESS_TOKEN_SECRET')

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
tweet_api = tweepy.API(auth)


def get_tweets(keyword):
    dictionary_list = []
    public_tweets = tweet_api.search(q=keyword, count=5)

    for tweet in public_tweets:
        my_dict = {
            "Tweet_Text": tweet.text,
            "url": 'https://twitter.com/' + str(tweet.user.id) + '/status/' + str(tweet.id),
            "user_name": tweet.user.name,
            "screen_name": tweet.user.screen_name,
            "created_at": str(tweet.created_at),
            "name": tweet.user.name,
            "profile_image": tweet.user.profile_image_url_https
        }
        dictionary_list.append(my_dict)
    return dictionary_list


def sentiment_value(text):
    analysis = TextBlob(text)

    if analysis.sentiment.polarity > 0:
        return('positive')
    elif analysis.sentiment.polarity < 0:
        return('negative')
    else:
        return('neutral')


def polarity(tweets, keyword):
    pos = 0
    neg = 0
    neu = 0

    num_tweets = len(tweets)

    for tweet in tweets:
        pol = sentiment_value(tweet["Tweet_Text"])
        if pol == 'positive':
            pos = pos + 1
        elif pol == 'negative':
            neg = neg + 1
        else:
            neu = neu + 1

    if num_tweets > 0:
        pos_pct = pos / num_tweets * 100
        neg_pct = neg / num_tweets * 100
        neu_pct = neu / num_tweets * 100

    else:
        print("dude something is very wrong")

    pol_pct_dict = {
        "positive_pct": pos_pct,
        "negative_pct": neg_pct,
        "neutral_pct": neu_pct,
    }

    # # Database code
    db[keyword] = json.dumps(pol_pct_dict)

    return(pol_pct_dict)
