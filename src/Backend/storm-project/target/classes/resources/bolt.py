#ece 4813 team 10 final project
#this is the storm bolt that will take
#the emitted data from the spout and place it on the dynamo_db table

import storm
from storm import Bolt
from datetime import date
import time
import datetime
import boto3
import json
import re

AWS_KEY="AKIAJ4F3PFWDDGST5AWQ"
AWS_SECRET="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"
REGION="us-east-2"

today = date.today()

#Connect to DynamoDB
conn_db = boto3.resource('dynamodb', aws_access_key_id=AWS_KEY,
                            aws_secret_access_key=AWS_SECRET,
                            region_name=REGION)
twitter_table = conn_db.Table("final_project")

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
           if not data:
              storm.emit([data])
              return

           output = analyzeData(data["data"])

           result= "Result: "+ str(output)


           item_data = {
               "movie" : str(data["movie"]),
               "state" : str(data["state"]),
               "prediction" : str(output)
           }

           #new_entry = {}

           #get the existing entry in table
           state = str(data["state"].replace(" ", "").strip())
           result = twitter_table.get_item(Key={"state": state})
           if "Item" in result:
              result = result["Item"]
           else:
              result = {}

           if not result:
              new_entry = {"state": data["state"],
                            "list": [
                                     {
                                      data["movie"]: str(1),
                                        "sentiment": str(int(output))
                                     }
                                    ]
                          }
              twitter_table.put_item(
                 Item=new_entry
              )
           else:
              found = False
              index = 0
              for thing in result["list"]:
                # thing = json.loads(str(thing))
                 if data["movie"] in thing.keys():
                    thing[data["movie"]] = str(int(thing[data["movie"]]) + int(1))
                    thing["sentiment"] = str(int(thing["sentiment"]) + int(output))
                    result["list"][index] = thing
                    twitter_table.put_item(
                        Item=result
                    )
                    found = True
                    break
                 index = index + 1
              if found == False:
                 new_entry = {data["movie"]: str(1), "sentiment": str(int(output))}
                 result["list"].append(new_entry)
                 twitter_table.put_item(
                    Item=result
                 )




           storm.emit([item_data])
           time.sleep(5)

MyBolt().run()
