"""
Module for initializing and exporting extensions to our app.

The extensions are defined here as global variable as can be imported
from files where they are needed.

Global Variables
----------------
mongo: flask_pymongo.PyMongo
    A PyMongo connection object that is used to connect to mongodb.
"""

from flask_pymongo import PyMongo

mongo = PyMongo()


