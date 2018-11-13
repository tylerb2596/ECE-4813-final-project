#ECE 4813 Lab 5
#Tyler Brown (903017579)

#this code is used to grab data from Kafka
#and publish it to storm as a spout

from random import randrange
import time
import datetime
import json
from kafka.consumer import KafkaConsumer
from kafka import KafkaClient
from kafka import SimpleConsumer
from kafka import KafkaConsumer
from storm import Spout, emit, log
import urllib3

urllib3.disable_warnings()

#Connect to Kafka
client = KafkaClient("ip-172-31-3-170.us-east-2.compute.internal:6667")
consumer = KafkaConsumer(bootstrap_servers=['ip-172-31-3-170.us-east-2.compute.internal:6667'], value_deserializer=lambda m: json.loads(m.decode('ascii')), auto_offset_reset='earliest', group_id="Lab5-group")

consumer.subscribe(consumer.topics())

def getData():
    try:
       data = []
       for message in consumer:
          data.append(json.loads(str(message.value)))
          if len(data) == 20:
             break
       return data
    except:
       return [{}]

class MySpout(Spout):
    def nextTuple(self):
        data = getData()
        emit([data])


MySpout().run()



