from flask import Flask, abort, request, jsonify
from config import app_config
from app.models import User, Ride, Request
import jwt
import datetime
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash
import re


def create_app(config_name):
    """ Creates a falsk app based on config passed:
    development, testing, production"""

    # enables relative parameter passing
    app = Flask(__name__)
    app.config.from_object(app_config[config_name])
    app.config.from_object("config")

    from app.auth.views import auth_blueprint
    app.register_blueprint(auth_blueprint)
    from app.rides.views import rides_blueprint
    app.register_blueprint(rides_blueprint)
    from app.requests.views import requests_blueprint
    app.register_blueprint(requests_blueprint)


    return app