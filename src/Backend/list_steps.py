#this is a python script to print out the steps needed
#to complete the backend of the ECE 4813 final project

#just run the script to print out a to do list

steps = "1) Collect currently playing movie data from tmdb.\n"
step = steps + "2) Start collecting tweets using currently playing movie titles as filters.\n"
steps = steps + "3) Analyze tweets and give each a city tag based on cities.json data. Use a radius around each city.\n"
steps = steps + "4) Attribute each city to a list of json objects representing the movie, how many tweets about it and the overall sentiment of the tweets.\n"
steps = steps + " In other words, provide a list of movies in each city along with how many tweets there are about the movie and the total sum of the sentinments in the tweets to the table.\n"
steps = steps + " The table entries will need to be constantly updated based on tweets coming in with new data.\n"

print steps