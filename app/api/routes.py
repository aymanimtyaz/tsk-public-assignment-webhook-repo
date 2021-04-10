from flask import Blueprint
from flask import jsonify

from app.extensions import mongo
from app.utils import format_date

api_bp = Blueprint('api', __name__)

#       This endpoint is fetched every 15 seconds by the frontend via the JavaScript fetch api.
@api_bp.route('/events', methods  =['GET'])
def get_events():
    #       Using list comprehension to add event data to events list
    events = [{
            'author':event['author'],
            'action':event['action'],
            'from_branch':event.get('from_branch'),
            'to_branch':event['to_branch'],
            'timestamp':format_date(event['timestamp'])
        } for event in mongo.db.github_events.find().sort([('timestamp', -1),('_id', -1)])]
    return jsonify(events), 200