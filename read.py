#!/usr/bin/env python
import json
import pandas as pd

tweets_keywords_count = dict()
tweets_keywords = ["nest", "ecobee", "rebate", "thermostat", "smart", "honeywell", "marketplace", "store", "retroactive"]
tweets_without_keywords = []
with open("tweets.json") as input_file:
    data = json.load(input_file)

#pd_data = pd.read_json("tweets.json", lines=True) #, orient='columns')
pd_data = pd.io.json.json_normalize(data)

for tweet in data:
    no_keywords = True
    for keyword in tweets_keywords:
        if keyword in tweet["text"].lower():
            tweets_keywords_count[keyword] = tweets_keywords_count.get(keyword, 0) + 1
            no_keywords = False
    if no_keywords:
        tweets_without_keywords.append(tweet)

# for tweet in tweets_without_keywords:
#     data.remove(tweet)

# with open("tweets.json", "w") as output_file:
#     json.dump(data, output_file)

print "Total json objects: " + str(len(data))
print "Keyword counts: " + str(tweets_keywords_count)
print "Total keyword tweets: " + str(sum(tweets_keywords_count.values()))
print "Total no-keyword tweets: " + str(len(tweets_without_keywords))


print pd_data["place.name"].value_counts()