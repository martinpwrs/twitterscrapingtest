#scrape.py code snippet using tweepy and json
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

#Ran this in bash for about 45 minutes to gather tweets. 

    python scrape.py > data.txt

#Copy file to what will be a final json file

    cp data.txt tweets.json

#This file now has lines of json objects but not in a readable format. Every other line is blank, there are no comma separators, and no starting "[" or ending "]" brackets. I ran these commands to get these in place so I can load it in python as a json object

    sed -i '/^$/d' tweets.json # Remove blank lines
    sed -i '$!s/$/,/' tweets.json #Add a comma to the end of each line except the last line. This adds a ^M carriage return before the comma for some reason.
    sed -i '1s/^/[/' tweets.json # Add a open square bracket to the start of the file.
    sed -i '$ a\ ]' tweets.json # Add a close square bracket to the end of the file.

#tweets.json can now be loaded as a json file using json.load()
#I did a counting loop on the json to find how many times each keyword was used

    tweets_keywords_count = dict()
    tweets_keywords = ["nest", "ecobee", "rebate", "thermostat", "smart", "honeywell", "marketplace", "store", "retroactive"]
    with open("tweets.json") as input_file:
        data = json.load(input_file)
    for tweet in data:
        for keyword in tweets_keywords:
            if keyword in tweet["text"]:
                tweets_keywords_count[keyword] = tweets_keywords_count.get(keyword, 0) + 1

    print "Total json objects: " + str(len(data))
    print "Keyword counts: " + str(tweets_keywords_count)

#Which results in: 

    Total json objects: 11717
    Keyword counts: {'marketplace': 54, 'thermostat': 18, 'nest': 80, 'rebate': 23, 'honeywell': 1, 'smart': 2503, 'store': 1941}
    
#I found that the python string matching was case-sensitive so I changed it to this:
    
    if keyword in tweet["text"].lower():

#which results in:

    Total json objects: 11717
    Keyword counts: {'marketplace': 160, 'thermostat': 28, 'nest': 122, 'rebate': 29, 'honeywell': 3, 'smart': 4267, 'store': 2832, 'retroactive': 1}

#Since we still are not seeing the counts match up, I made a flag to catch tweets that have no keywords and add them to a separate list:

    tweets_keywords_count = dict()
    tweets_keywords = ["nest", "ecobee", "rebate", "thermostat", "smart", "honeywell", "marketplace", "store", "retroactive"]
    tweets_without_keywords = []
    with open("tweets.json") as input_file:
        data = json.load(input_file)
    for tweet in data:
        no_keywords = True
        for keyword in tweets_keywords:
            if keyword in tweet["text"].lower():
                tweets_keywords_count[keyword] = tweets_keywords_count.get(keyword, 0) + 1
                no_keywords = False
        if no_keywords:
            tweets_without_keywords.append(tweet)

    print "Total json objects: " + str(len(data))
    print "Keyword counts: " + str(tweets_keywords_count)
    print "Total keyword tweets: " + str(sum(tweets_keywords_count.values()))
    print "Total no-keyword tweets: " + str(len(tweets_without_keywords))

#Which prints: 
	
    Total json objects: 11717
    Keyword counts: {'marketplace': 160, 'thermostat': 28, 'nest': 122, 'rebate': 29, 'honeywell': 3, 'smart': 4267, 'store': 2832, 'retroactive': 1}
    Total keyword tweets: 7442
    Total no-keyword tweets: 4312

#The 37 tweet difference between the keyword and no-keyword count, I beleive is due to multiple keywords in one tweet. 
#To find out why the tweets with no keywords were gathered in the first place, I added a print command at the end of the script to examine the json object of a tweet with no keywords:

    print json.dumps(tweets_without_keywords[0], indent=2)

#I piped this output into a grep command to do a quick manual check if any keywords show up:

    python reader.py | grep store

#Which gave this output showing that tweepy catches search keywords in the expanded URL of a tweet's short-URL
      
      "expanded_url": "https://store.sixxammusic.com/collections/gift-guide", 
          "display_url": "store.sixxammusic.com/collections/gi\u2026"
      "expanded_url": "https://store.sixxammusic.com/collections/gift-guide", 
          "display_url": "store.sixxammusic.com/collections/gi\u2026"

#Knowing that these tweets are not relevant to the search, I want to remove them from our json file. I made a backup of tweets.json. I added this loop to the script to delete the tweets with no keywords in the actual tweet text and then overwrite tweets.json with the cultivated tweets.

    for tweet in tweets_without_keywords:
        data.remove(tweet)
    with open("tweets.json", "w") as output_file:
        json.dump(data, output_file)

