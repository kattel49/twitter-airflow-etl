import tweepy
import pandas as pd
import json
from datetime import datetime
from dotenv import load_dotenv
import os

load_dotenv()

ACCESS_TOKEN=os.getenv("ACCESS_TOKEN")
ACCESS_SECRET=os.getenv("ACCESS_SECRET")
CONSUMER_KEY=os.getenv("CONSUMER_KEY")
CONSUMER_SECRET=os.getenv("CONSUMER_SECRET")

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET ,ACCESS_TOKEN, ACCESS_SECRET)

api = tweepy.API(auth)

#all public tweets
#public_tweets = api.home_timeline()

elon_tweets = api.user_timeline(screen_name="@elonmusk",
                        # max is 200
                        count=5,
                        # include retweets
                        include_rts=False,
                        # keep full text
                        tweet_mode="extended"
                        )

for tweet in elon_tweets:
    extracted_tweet = {
        "user": tweet.user.screen_name,
        "text": tweet._json["full_text"],
        "favorite_count": tweet.favorite_count,
        "retweet_count" : tweet.retweet_count,
        'created_at' : tweet.created_at
    }

    print(extracted_tweet)