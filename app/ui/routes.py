"""
This modules contains endpoints that define the frontend of the app.

Functions
---------
index()

Global Variables
----------------
frontend_bp
"""

from flask import Blueprint, render_template

frontend_bp = Blueprint("frontend", __name__)

@frontend_bp.route("/admin", methods = ["GET"])
def admin_page():
    """ Renders the ui for the event logger on the browser """
    return render_template("admin.html")

@frontend_bp.route("/superadmin", methods = ["GET"])
def superadmin_page():
    """ Renders the ui for the event logger on the browser """
    return render_template("superadmin.html")

    

