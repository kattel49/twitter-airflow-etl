import tweepy
import pandas as pd
import json
from datetime import datetime
from dotenv import load_dotenv
import os
import threading
from TwitterModel import Tweets, session
from sqlalchemy import and_


load_dotenv()

ACCESS_TOKEN=os.getenv("ACCESS_TOKEN")
ACCESS_SECRET=os.getenv("ACCESS_SECRET")
CONSUMER_KEY=os.getenv("CONSUMER_KEY")
CONSUMER_SECRET=os.getenv("CONSUMER_SECRET")


auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET ,ACCESS_TOKEN, ACCESS_SECRET)

api = tweepy.API(auth)

#all public tweets
#public_tweets = api.home_timeline()

tweet_dict = {}

twitter_handle = ['@elonmusk', '@NASA', '@twitter', '@cnnbrk', '@jim_adler', '@mjcavaretta', '@BillGates']
twitter_sname = [x[1:] for x in twitter_handle]

# for count, user in enumerate(twitter_handle):
#     raw_tweets = api.user_timeline(screen_name=user,
#                             # max is 200
#                             count=5,
#                             # include retweets
#                             include_rts=False,
#                             # keep full text
#                             tweet_mode="extended"
#                             )
    
#     if tweet_dict.get(twitter_sname[count]) is None:
#         tweet_dict[twitter_sname[count]] = []

#     for tweet in raw_tweets:
#         extracted_tweet = {
#             "text": tweet._json["full_text"],
#             "favorite_count": tweet.favorite_count,
#             "retweet_count" : tweet.retweet_count,
#             'created_at' : tweet.created_at
#         }
#         tweet_dict[twitter_sname[count]].append(extracted_tweet)

class myThread(threading.Thread):
    def __init__(self, threadId, t_handle, t_sname):
        threading.Thread.__init__(self)
        self.threadId = threadId
        self.t_handle = t_handle
        self.t_sname = t_sname
    
    def run(self):
        # no need to use locks because we access different objs in the dictionary
        extract_tweet(self.t_handle, self.t_sname)

def extract_tweet(t_handle, t_sname):
    raw_tweets = api.user_timeline(screen_name=t_handle,
                            # max is 200
                            count=5,
                            # include retweets
                            include_rts=False,
                            # keep full text
                            tweet_mode="extended"
                            )
    
    if tweet_dict.get(t_sname) is None:
        tweet_dict[t_sname] = []

    for tweet in raw_tweets:
        extracted_tweet = {
            "text": tweet._json["full_text"],
            "favorite_count": tweet.favorite_count,
            "retweet_count" : tweet.retweet_count,
        }
        tweet_dict[t_sname].append(extracted_tweet)

def etl_pipeline():
    threads = []

    for i, t_handle in enumerate(twitter_handle):
        t = myThread(threadId=i, t_handle=t_handle, t_sname=twitter_sname[i])
        t.start()
        threads.append(t)

    for t in threads:
        t.join()
    
    # after all the tweets are extracted

    for key, value in tweet_dict.items():
        for tweet in value:
            # check to see if the tweet exists
            db_tweet = session.query(Tweets).filter(and_(Tweets.user==key, Tweets.text==tweet.get("text"))).first()
            # if tweet does not exist save it to the database
            if db_tweet is None:
                extracted = Tweets(user=key, text=tweet.get("text"), favorite_count=tweet.get("favorite_count"), retweet_count=tweet.get("retweet_count"))
                session.add(extracted)
            else:
            # update the tweet values if it is already in the database
                db_tweet.retweet_count = tweet.get("retweet_count")
                db_tweet.favorite_count = tweet.get("favorite_count")
                session.add(db_tweet)
            
            session.commit()
    session.close()