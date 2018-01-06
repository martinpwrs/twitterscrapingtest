#!/usr/bin/env python

# Import the necessary methods from tweepy library
import tweepy
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import json

#Variables that contains the user credentials to access Twitter API
access_token = "15079501-BusZvp5a2Y7ME1iW6g2uFMsoU8sax9V1CNCVQEqVT"
access_token_secret = "PK82xrtAiVpXeyBwbhbEoPUVZUUlLw0OXAg002ctDVRnR"
consumer_key = "5sanDvfq293rjyvMp8tznCsUb"
consumer_secret = "59Kd70IhYgPKElcFPAtisqPfyy2gj1ClFlyluvd8DVAYaDwqj5"


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