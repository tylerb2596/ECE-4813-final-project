#ECE 4813 team 10 final project
#this code is used to listen to tweets and add a location
#tag to them. It will then put the data into a Kafka
#queue to be retrieved later. The tweets coming in are filtered
#based oni the list of current movies in theatres

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
import math
import requests
import random

urllib3.disable_warnings()

#Twitter API keys from Twitter developer account
access_token = "1241997110-gRViHQuzCYqDdccZvVuLVEIm8W91ngTy3Z8WW5m"
access_token_secret = "hPi51Uoh9jsZpkujnNHF9E0o4dK6AjCij158FGIYBvYcz"
consumer_key = "IHzljiFLv66AhpUIvfctyeWnv"
consumer_secret = "EpdUFb1IVdOu69CmWd1FjppXUMALp8bbxdUOcyp5PRvGbf0XgY"

#tmdb api key
tmdb_key = "c156116208ccc0dcefd6ac794628fd1f"

#Connect to Kafka
client = KafkaClient("ip-172-31-3-170.us-east-2.compute.internal:6667")
producer = SimpleProducer(client)

#function to read in a json file as a dictionary
def get_json_from_file(filename):
    with open(filename, 'r') as file:
        json_dictionary = json.load(file)
    return json_dictionary
#fucntion to return a list of movies currently in theatres
def get_current_movies():
    url = "https://api.themoviedb.org/3/movie/now_playing?api_key="
    url = url + tmdb_key + "&language=en-US&page=1"

    response = requests.get(url)
    movies = []
    response = response.json()
    for movie in response["results"]:
        movies.append(movie["title"])
        if len(movies) == 5:
            break
    return movies

#global variables so they are only generated once
current_movies = get_current_movies()
states = get_json_from_file("../../data/states.json")

#return the state in which the tweet was made
def get_state(data):
    if "place" in data and data["place"] != None:
        place = data["place"]
        if place["country"] != "United States":
            #for testing purposes
            return get_random_state()
        for state in states:
            if place["full_name"].find(state["alpha-2"]) >= 0:
                return state["name"]
        #for testing purposes
        return get_random_state()

    if "user" in data and data["user"]["location"] != None:
        for state in states:
            location = fix_word(data["user"]["location"])
            if location.upper().find(" " + state["alpha-2"] + " ") >= 0 or location.find((" " + state["name"] + " ").lower()) >= 0:
                return state["name"]
        #for testing purposes
        return get_random_state()



#function to pick a random state to assign tweets to.
#this fucntion is for testing purposes
def get_random_state():
    return states[random.randint(0, len(states)-1)]["name"]



#helper fucntion to fix a word by removing
#extraneous characters
def fix_word(word):
    word = word.replace(":", "")
    word = word.replace("'", "")
    word = word.replace(",", "")
    word = word.replace(".", "")
    word = word.replace("!", "")
    word = word.lower()
    return word

#function to get the full text associated with the tweet and its hashtags
def get_full_text(data):
    full_text = ""
    if "extended_tweet" in data and "full_text" in data["extended_tweet"]:
        full_text = data["extended_tweet"]["full_text"]
    elif "extended_entities" in data and "full_text" in data["extended_entities"]:
        full_text = data["extended_entities"]["full_text"]
    else:
        full_text = data["text"] if "text" in data else ""

    hashtags = get_hashtags(data)

    if len(hashtags) > 0:
        for item in hashtags:
            full_text = full_text +  " " + item

    full_text = full_text.replace(" of ", " ")
    full_text = full_text.replace(" the ", " ")
    full_text = full_text.replace(" and ", " ")
    full_text = full_text.replace(" for ", " ")
    full_text = full_text.replace(" a ", " ")
    full_text = full_text.replace(" an ", " ")

    return full_text

#find out which movie the tweet corresponds to
def get_movie(text):
    movies = current_movies
    for movie in movies:
        words = movie.split()
        count = 0
        length = len(words)
        for word in words:
            word = fix_word(word)
            if (text.lower().find(word) >= 0):
                count = count + 1
        if count/length >= 0.15:
            return movie
    return 0

#function to split up movie titles to get more data coming through
def get_word_list(list):
    new_list = []
    for thing in list:
        thing = thing.split()
        i = 0
        while i < len(thing):
            thing[i] = fix_word(thing[i])
            new_list.append(str(thing[i]))
            i = i + 1
    return new_list


#get list of hashtags to use in searching for movies
def get_hashtags(data):
    hashtags = []
    if "entities" in data:
        if "hashtags" in data["entities"]:
            for hashtag in data["entities"]["hashtags"]:
                hashtags.append(hashtag["text"])
    return hashtags

#put data in a form we need for analysis
def fix_data(data):
    data = json.loads(data.decode('ascii'))
    new_data = {}


    #########################################
    #for testing
    if not (("place" in data and data["place"] != None) or ("user" in data and data["user"]["location"] != None)):
        data["user"] = {}
        data["user"]["location"] = get_random_state()
    ########################################

    if ("place" in data and data["place"] != None) or ("user" in data and data["user"]["location"] != None):
        full_text = get_full_text(data)
        if get_movie(full_text) != 0:
            new_data["movie"] = get_movie(full_text)
        else:
            return {}

        if get_state(data) != "":
            new_data["state"] = get_state(data)
        else:
            return {}
        new_data["data"] = data;
        return new_data
    else:
        return {}

#Implement this function to publish data to Kafka topic
def publish(data):
    data = json.dumps(data).encode('ascii')
    producer.send_messages('project', data)

#This is a basic listener that publishes data to the kafka topic
class KafkaListener(StreamListener):

    def on_data(self, data):
        data = fix_data(data)
        if data:
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

    #get the list of current movies so that the tweets can be filtered
    #using those movies
    search_list = current_movies

    #This line filter Twitter Streams to capture data by the keywords
    stream.filter(track=search_list)



