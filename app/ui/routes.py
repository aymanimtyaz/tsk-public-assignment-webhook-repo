from flask import render_template
from flask import Blueprint

frontend_bp = Blueprint('frontend', __name__)

#       Frontend Endpoint
@frontend_bp.route('/', methods = ['GET'])
def index():
    return render_template('ui.html')

    

