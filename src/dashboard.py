#!flask/bin/python
from flask import Flask, jsonify, abort, request, make_response, url_for
from flask import render_template, redirect
import json
import random

app = Flask(__name__, static_url_path="")

global stateslist

stateslist=[]

statenames = ["Alabama", "Alaska", "Arizona", "Arkansas", "California",
		"Colorado", "Connecticut", "Delaware", "District of Columbia", "Florida", "Georgia",
		"Hawaii", "Idaho", "Illinois", "Indiana", "Iowa",
		"Kansas", "Kentucky", "Louisiana", "Maine", "Maryland",
		"Massachusetts", "Michigan", "Minnesota", "Mississippi", "Missouri",
		"Montana", "Nebraska", "Nevada", "New Hampshire", "New Jersey",
		"New Mexico", "New York", "North Carolina", "North Dakota", "Ohio",
		"Oklahoma", "Oregon", "Pennsylvania", "Rhode Island", "South Carolina",
		"South Dakota", "Tennessee", "Texas", "Utah", "Vermont",
		"Virginia", "Washington", "West Virginia", "Wisconsin", "Wyoming"]

def populate_statelist():
	for i in range(0,len(statenames)):
		state={
			'Name': statenames[i],
			'Movie': "",
			'NumTweets': 0
		}
		stateslist.append(state)

@app.route('/update')
def update():
	for i in range(0,len(statenames)):
		state = stateslist[i]
		state["Movie"] = "" # INSERT MOVIE DATA HERE
		state["NumTweets"] = random.randint(1,99) # INSERT NUMBER OF TWEETS ABOUT THIS MOVIE HERE

	return jsonify(stateslist)

@app.route('/')
def home_page():
	return render_template('index.html', states = stateslist)

if __name__ == '__main__':
	populate_statelist()
    	app.run(host='0.0.0.0', debug=True, port=5000)
    
