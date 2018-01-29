#!/usr/bin/env python

# Import the necessary methods from tweepy library
import tweepy
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import json

#Variables that contains the user credentials to access Twitter API
access_token = API_TOKEN
access_token_secret = API_TOKEN_SECRET
consumer_key = KEY
consumer_secret = KEY_SECRET


class listener(StreamListener):

    def on_data(self, data):
        #all_data = json.loads(data)

        print data

        return True

    def on_error(self, status):
        print status


auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

twitterStream = Stream(auth, listener())
twitterStream.filter(track=["nest", "ecobee", "rebate", "thermostat", "smart", "honeywell", "marketplace", "store", "retroactive"])
