"""
This module contains REST endpoints for fetching data from the backend.

Functions
---------
get_events()

Global Variables
----------------
api_bp
"""

from bson.objectid import ObjectId

from flask import Blueprint, jsonify, request
from flask_pymongo import PyMongo

from app.extensions import mongo
from app.utils import GithubEvent

api_bp = Blueprint("api", __name__)

@api_bp.route("/events", methods  =["GET"])
def get_events():
    """
    Fetch and return GitHub event data from the database.

    Cursor based pagination is used to get event data on subsequent
    calls to the API. If the API is called without the 'after' param
    in the query string, data pertaining to 5 of the latest events 
    is fetched and sent back. Otherwise, if the 'after' param is 
    present in the query string, only events having an oid greater than
    it are fetched and sent back.
    """
    # variable 'after' stores the pagination cursor
    after = request.args.get("after")
    if not after:
        mongo_events = mongo.db.github_events.find().sort("_id", -1).limit(5)
    else:
        mongo_events = mongo.db.github_events.find(
            {"_id": {"$gt": ObjectId(after)}}).sort("_id", -1)
    events = []
    for event in mongo_events:
        events.append(GithubEvent(
            request_id=event["request_id"], author=event["author"], 
            action=event["action"], to_branch=event["to_branch"], 
            timestamp=event["timestamp"], _id=str(event["_id"]),
            from_branch=event["from_branch"]).event_object_to_dict())
        
    return jsonify(events), 200