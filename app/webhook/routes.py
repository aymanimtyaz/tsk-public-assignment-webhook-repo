"""
This module contains the endpoint to receive updates from GitHub via
a webhook

Functions
---------
receiver()

Global Variables
----------------
webhook
"""

import datetime
import json

from flask import Blueprint, request, jsonify

from app.extensions import mongo
from app.utils import GithubEvent

webhook = Blueprint("Webhook", __name__, url_prefix="/webhook")

@webhook.route("/receiver", methods=["POST"])
def receiver():
    """
    Endpoint for the GitHub events webhook.

    The JSON containing the event update is received and parsed for
    the required info. The info is then pushed into the database. 
    
    If the JSON contains the 'action' key, the event is either a merge 
    or a pull request, depending on the value of the 'action' field and 
    the 'merged' field. Otherwise, if the JSON has the 'pusher' key in 
    it, it is a push event.

    The required fields are:
        1. request_id
        2. author
        3. action
        4. from_branch
        5. to_branch
        6. timestamp
    """
    github_event_update = request.get_json()
    timestamp = str(datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"))

    # Pull Request
    # Event is a pull request if 'action' is 'opened' and 'merged' in
    # 'pull_request' is False
    if (github_event_update.get("action") == "opened" and
            github_event_update["pull_request"]["merged"] == False):
        request_id = github_event_update["pull_request"]["id"]
        author = github_event_update["sender"]["login"]
        action = "PULL_REQUEST"
        from_branch = github_event_update["pull_request"]["head"]["ref"]
        to_branch = github_event_update["pull_request"]["base"]["ref"]
    # Merge
    # Event is a merge if 'action' is 'closed' and 'merged' in 
    # 'pull_request' is True
    elif (github_event_update.get("action") == "closed" and
            github_event_update["pull_request"]["merged"] == True):
        request_id = github_event_update["pull_request"]["id"]
        author = github_event_update["pull_request"]["merged_by"]["login"]
        action = "MERGE"
        from_branch = github_event_update["pull_request"]["head"]["ref"]
        to_branch = github_event_update["pull_request"]["base"]["ref"]
    # Push
    # Event is a push if the 'pusher' key is present in the JSON
    elif github_event_update.get("pusher"):
        request_id = github_event_update["head_commit"]["id"]
        author = github_event_update["pusher"]["name"]
        action = "PUSH"
        from_branch = None
        to_branch = github_event_update["ref"].split('/')[2]

    event_object = GithubEvent(
        request_id=request_id, author=author, action=action,
        from_branch=from_branch, to_branch=to_branch, 
        timestamp=timestamp)

    mongo.db.github_events.insert_one(event_object.event_object_to_dict())
    
    return 'True'
