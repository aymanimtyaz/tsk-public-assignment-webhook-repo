from flask import Flask

from app.webhook.routes import webhook
from app.ui.routes import frontend_bp
from app.api.routes import api_bp

from .extensions import mongo


#       Creating our flask app
def create_app():

    app = Flask(__name__)

    #       Database is named tsx, and the collection is github_events
    app.config['MONGO_URI'] = 'mongodb://localhost:27017/tsx'


    mongo.init_app(app)
    
    #       registering all the blueprints
    app.register_blueprint(webhook)
    app.register_blueprint(frontend_bp)
    app.register_blueprint(api_bp)
    
    return app
