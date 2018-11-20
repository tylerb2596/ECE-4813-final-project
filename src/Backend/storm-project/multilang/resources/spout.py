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

consumer.subscribe("project")

def getData():
    try:
       data = []
       for message in consumer:
          data.append(message.value)#json.loads(message.value.decode('ascii')))
          if len(data) == 10:
             break
      # print data
       return data
    except Exception as e:
      # print e
       return [{}]

class MySpout(Spout):
    def nextTuple(self):
        data = getData()
        emit([data])


MySpout().run()



