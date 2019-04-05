from flask import Flask, jsonify, request, Response
from flask_pymongo import PyMongo
from bson.json_util import dumps
import datetime
from utils.helper import Helper
import urllib.parse

#Load config file & access
import os
from dotenv import load_dotenv
load_dotenv()

MONGO_URI = os.environ.get('MONGO_URI') if os.getenv("MONGO_URI") is None else os.getenv("MONGO_URI")
PORT = os.environ.get('PORT') if os.getenv("PORT") is None else os.getenv("PORT")
MONGO_USERNAME = os.environ.get('MONGO_USR_NAME') if os.getenv("MONGO_USR_NAME") is None else os.getenv("MONGO_USR_NAME")
MONGO_PASSWORD = os.environ.get('MONGO_PASSWORD') if os.getenv("MONGO_PASSWORD") is None else os.getenv("MONGO_PASSWORD")

#App Insights
from applicationinsights.requests import WSGIApplication

app = Flask(__name__)
mongo_username = urllib.parse.quote_plus(MONGO_USERNAME)
mongo_password = urllib.parse.quote_plus(MONGO_PASSWORD)
print(MONGO_URI)
app.config["MONGO_URI"] = MONGO_URI
mongo = PyMongo(app)

#Home
@app.route('/')
def home():
    return 'Welcome to Ge Coach Utiltity Service!'

#Get sessions learnerId
@app.route('/sessions/learner/<learnerid>')
def getSessionsByLearnerId(learnerid):
    learner_sessions = mongo.db.sessioncollections.find({'learnerId': learnerid})
    return dumps(learner_sessions)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=PORT, debug=True)