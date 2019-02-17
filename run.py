from flask import Flask, jsonify, request, Response
from flask_pymongo import PyMongo
from bson.json_util import dumps
import datetime

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/sessiondb"
mongo = PyMongo(app)

@app.route('/')
def home():
    return 'Hello World!'

@app.route('/sessions/learner/<learnerid>')
def getSessionsByLearnerId(learnerid):
    learner_sessions = mongo.db.sessioncollections.find({'learnerId': learnerid})
    return dumps(learner_sessions)

@app.route('/sessions/host/<hostid>')
def getSessionsByHostId(hostid):
    host_sessions = mongo.db.sessioncollections.find({'hostId': hostid})
    return dumps(host_sessions)

@app.route('/sessions/status/<status>')
def getSessionsByStatus(status):
    sessions = mongo.db.sessioncollections.find({'status': status})
    return dumps(sessions)

@app.route('/sessions/date')
def getSessionsByDateRange():
    st_dt_str = request.args.get('startDate')
    end_dt_str = request.args.get('endDate')
    st_dt = datetime.datetime.strptime(st_dt_str, "%Y%m%d")
    query = {'lastUpdatedDate': {'$gte': st_dt}}

    if end_dt_str is not None:
        end_dt = datetime.datetime.strptime(end_dt_str, "%Y%m%d")
        query = {'lastUpdatedDate': {'$gte': st_dt, '$lt': end_dt}}

    sessions = mongo.db.sessioncollections.find(query)
    return dumps(sessions)

if __name__ == '__main__':
    app.run(port=5000)