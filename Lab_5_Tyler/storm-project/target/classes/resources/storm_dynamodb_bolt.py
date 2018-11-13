#ECE 4813 Lab 5
#Tyler Brown (903017579)

#this code is an apache storm bolt that
#reads tweets from the spout and performs a
#sentiment analysis on them.
#It then puts the data on a dynamoDB table.


import storm
from storm import Bolt
from datetime import date
import time
import datetime
import boto3
import json
import re

AWS_KEY="AKIAIFZU2ZB6OB2SEZQQ"
AWS_SECRET="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"
REGION="us-east-2"

today = date.today()

#Connect to DynamoDB
conn_db = boto3.resource('dynamodb', aws_access_key_id=AWS_KEY,
                            aws_secret_access_key=AWS_SECRET,
                            region_name=REGION)
twitter_table = conn_db.Table("tweetsentiment")

TERMS={}

#-------- Load Sentiments Dict ----
sent_file = open('AFINN-111.txt')
sent_lines = sent_file.readlines()
for line in sent_lines:
	s = line.split("\t")
	TERMS[s[0]] = s[1]

sent_file.close()

#-------- Find Sentiment  ----------
def findsentiment(tweet):
    sentiment=0.0

    if tweet.has_key('text'):
        text = tweet['text']
        text=re.sub('[!@#$)(*<>=+/:;&^%#|\{},.?~`]', '', text)
        splitTweet=text.split()

        for word in splitTweet:
            if TERMS.has_key(word):
                sentiment = sentiment+ float(TERMS[word])

    return sentiment


def analyzeData(data):
    #Add your code for data analysis here
    return findsentiment(data)

class MyBolt(storm.BasicBolt):
    def process(self, tup):
        for data in tup.values[0]:

           if not data or not ("timestamp_ms" in data):
              storm.emit([data])
              return

           output = analyzeData(data)

           result= "Result: "+ str(output)

           #Store analyzed results in DynamoDB
           item_data = {
               "date" : str(datetime.datetime.fromtimestamp(int(data['timestamp_ms'])/1000)),
               "timestamp" : str(int(data['timestamp_ms'])/1000),
               "data" : data['text'],
               "prediction" : str(output),
           }

           if item_data["prediction"] == "0.0":
               storm.emit([data])
               return

           twitter_table.put_item(
              Item=item_data
            )


           storm.emit([result])
           time.sleep(5)

MyBolt().run()
