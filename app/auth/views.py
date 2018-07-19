from flask import Flask, abort, request, jsonify
from config import app_config, SECRET_KEY
from app.models import User, Ride, Request
import jwt
import datetime
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash
import re
from flask import Blueprint
from app import validate


Users = User('username', 'email', 'password', 'role')
Rides = Ride('category', 'pick_up', 'drop_off', 
    'date_time', 'ride_status', 'creator_id' )
Requests = Request('request_description',
    'request_priority', 'request_status', 'ride_id')


auth_blueprint = Blueprint('auth', __name__)

# Decorator function to check for jwt token in the headers
def login_required(f):
    """ Function checks and validates jwt token"""
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if 'access-token' in request.headers:
            token = request.headers['access_token']

        else:
            token = request.headers.get('token')

        if not token:
            return jsonify(
                {'message': 'token is missing'}), 401 

        try:
            data = jwt.decode(token, SECRET_KEY)

            kwargs['current_user_id'] = data['user_id']

        except:
            return jsonify(
                {'message': 'Invalid token'}), 401
        return f(*args, **kwargs)
    return decorated


@auth_blueprint.route("/api/v2/auth/signup", methods=["POST"])
def register_user():
    """ Method creates a user account using email, username and password"""
    if request.json:
        print(request.json)
        new_user = {
            "email": request.json['email'],
            "username": request.json['username'].lower(),
            "password": request.json['password']
        }
        # get all user accounts from the database
        users = Users.get_all_users()  # retirns a list 
        all_users = []  # create a list (empty first)
        for user in users:  # loop through users each time append to list
            all_users.append(user[0])

        if value_none(**new_user):

            result = value_none(**new_user)

            return jsonify(result), 406

        if if_empty_string(**new_user):

            result = if_empty_string(**new_user)

            return jsonify(result), 406
        val_pass = has_whitespace(request.json['username'])
        if val_pass:
            return jsonify(
                {'message': 'Username cannot contain white spaces'}), 406
        val_length = pass_length(request.json['password'])
        if val_length:
            return jsonify(
                {'message':
                'Password is weak! Must have atleast 8 characters'}), 406
        val_email = validate_email_ptn(request.json['email'])

        if val_email:
            return jsonify(
                {'message':
                    'Email format is user@example.com'}), 406

        if new_user['username'] in all_users:

            return jsonify({'message': 'User already registered'}), 406

        hashed_pswd = generate_password_hash(new_user['password'])

        Users.create_user(
            new_user['username'], new_user['email'],
            hashed_pswd)
        return jsonify({'message': 'Sign up successful'}), 201

# User can login using email and password
@auth_blueprint.route("/api/v2/auth/login", methods=["POST"])
def login():
    """ Function logs in a user after
    validating username and password inputs"""
    if request.json:
        username = request.json["username"].lower()
        password = request.json["password"]

    if username == "" or password == "":

        return jsonify({'message': 'Please fill all fields'}), 400

    users = Users.login(username, password)
    if users:
        for user in users:
            if user['username'] == username and \
            check_password_hash(user['password'], password):

                token = jwt.encode(
                    {"user_id": user['user_id'],
                    'exp': datetime.datetime.utcnow() + \
                    datetime.timedelta(minutes=30)}, SECRET_KEY)
                role = Users.get_role(user['user_id'])[0][0]
                return jsonify(
                    {'token': token.decode('UTF-8')},
                    {'message': 'Login successful'},
                    {'role': role}), 200
    return jsonify(
        {"message": "no valid user"}), 401
