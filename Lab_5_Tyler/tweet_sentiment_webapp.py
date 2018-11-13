#ECE 4813 Lab 5
#Tyler Brown (903017579)


from flask import Flask, jsonify
import urllib2
import boto3
app = Flask(__name__)
from datetime import date
today = date.today()
import json

#-------Connect to DynamoDB---------
AWS_KEY="AKIAIFZU2ZB6OB2SEZQQ"
AWS_SECRET="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"
REGION="us-east-2"

conn_db = boto3.resource('dynamodb', aws_access_key_id=AWS_KEY,
                            aws_secret_access_key=AWS_SECRET,
                            region_name=REGION)

table = conn_db.Table('tweetsentiment')
#-----------------------------------

@app.route('/')
def tweet_home():

    #Scan DynamoDB table
    results=table.scan()          

    html = '<html><body><table width=80% border=1 align="center">'+\
            '<tr><td><strong>Timestamp</strong></td><td><strong>Date</strong></td><td><strong>Data</strong></td><td><strong>Prediction</strong></td></tr>'

    for result in results['Items']:
        html+='<td>'+result['timestamp']+'</td><td>'+result['date']+'</td><td>'+result['data']+'</td><td>'+result['prediction']+'</td></tr>'


    html+='</table></body></html>'

    return html

if __name__ == '__main__':
    app.run(host='0.0.0.0')
