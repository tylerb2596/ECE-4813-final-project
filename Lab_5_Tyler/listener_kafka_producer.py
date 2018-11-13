#ECE 4813 Lab 5
#Tyler Brown (903017579)

#this is the code for listening to twitter for tweets
#using the tweepy library and publishing the data to kafka

#Import the necessary methods from tweepy library
#and the kafka library
from tweepy import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from random import randrange
import time
import datetime
import urllib3
import json
from kafka import KafkaClient
from kafka.producer import KafkaProducer
from kafka import SimpleProducer

urllib3.disable_warnings()

#Get Twitter API keys from Twitter developer account
access_token = "1241997110-gRViHQuzCYqDdccZvVuLVEIm8W91ngTy3Z8WW5m"
access_token_secret = "hPi51Uoh9jsZpkujnNHF9E0o4dK6AjCij158FGIYBvYcz"
consumer_key = "IHzljiFLv66AhpUIvfctyeWnv"
consumer_secret = "EpdUFb1IVdOu69CmWd1FjppXUMALp8bbxdUOcyp5PRvGbf0XgY"

#Connect to Kafka
client = KafkaClient("ip-172-31-3-170.us-east-2.compute.internal:6667")
producer = SimpleProducer(client)

#Implement this function to publish data to Kafka topic
def publish(data):
    data = json.dumps(data).encode('ascii')
    producer.send_messages('election', data)

#This is a basic listener that publishes data to the kafka topic
class KafkaListener(StreamListener):

    def on_data(self, data):
        #publish data
        publish(data)
        return True

    def on_error(self, status):
        print(status)


if __name__ == '__main__':
    print( 'Listening...')
    #This handles Twitter authetification and the connection to Twitter Streaming API
    listener = KafkaListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    stream = Stream(auth, listener)

    #This line filter Twitter Streams to capture data by the keywords
    stream.filter(track=['election'])





