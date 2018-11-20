#ece 4813 team 10 final project
#this is the storm spout used to take data off
#of the kafka queue and emit it to the bolt

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
consumer = KafkaConsumer(bootstrap_servers=['ip-172-31-3-170.us-east-2.compute.internal:6667'], value_deserializer=lambda m: json.loads(m.decode('ascii')), auto_offset_reset='earliest', group_id="final_project")

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



