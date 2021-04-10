import datetime
import json

from flask import Blueprint, request, jsonify
from app.extensions import mongo

webhook = Blueprint('Webhook', __name__, url_prefix='/webhook')


#       The webhook endpoint. Ngrok.io was used for development and testing.
@webhook.route('/receiver', methods=["POST"])
def receiver():
    #       storing the json body of the request in variable js
    js = request.get_json()

    #       if the 'action' key is present, the event is either a pull request or a merge
    if js.get('action'):
        #       MERGE
        if js['action'] == 'closed' and js['pull_request']['merged'] == True:
            mongo.db.github_events.insert_one({
                "request_id":js['pull_request']['id'],
                "author":js['pull_request']['merged_by']['login'],
                "action":'MERGE',
                "from_branch":js['pull_request']['head']['ref'],
                "to_branch":js['pull_request']['base']['ref'],
                "timestamp":str(datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S'))
            })      
        #       PULL REQUEST
        elif js['action'] == 'opened' and js['pull_request']['merged'] == False:
            mongo.db.github_events.insert_one({
                "request_id":js['pull_request']['id'],
                "author":js['sender']['login'],
                "action":'PULL_REQUEST',
                "from_branch":js['pull_request']['head']['ref'],
                "to_branch":js['pull_request']['base']['ref'],
                "timestamp":str(datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S'))
            })
    #       PUSH
    elif js.get('pusher'):
        #       this document will not have a 'from_branch' key.
        mongo.db.github_events.insert_one({
            "request_id":js['head_commit']['id'],
            "author":js['pusher']['name'],
            "action":'PUSH',
            "to_branch":js['ref'].split('/')[2],
            "timestamp":str(datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S'))
        })
    return 'True'
