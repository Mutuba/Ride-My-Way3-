
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


rides_blueprint = Blueprint('ride', __name__)

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


@rides_blueprint.route("/api/v2/rides", methods=["POST"])
@login_required
def create_ride(current_user_id):
    """ Function creates a ride offer based on ride details"""
    if not request.json:
        abort(404)
    new_ride = {
        "category": request.json['category'],
        "pick_up": request.json['pick_up'],
        "drop_off": request.json['drop_off'],
        "date_time": request.json['date_time'],
        "ride_status": "Pending",
        "creator_id": current_user_id
    }

    for values in new_ride.values():
        if values == "":
            return jsonify({'message': 'Please fill all fields'}), 500

    rides = Rides.get_user_rides(current_user_id)
    categories = [request['category'] for request in rides]
    if new_ride['category'] in categories:
        return jsonify(
            {'message': 'Failed, Ride already made'}), 406

    Rides.create_ride(
        new_ride['category'], new_ride['pick_up'],
        new_ride['drop_off'], new_ride['date_time'],
        new_ride['ride_status'], new_ride['creator_id'])
    return jsonify(
        {'message': 'Ride created successfully'}), 201

@rides_blueprint.route("/api/v2/rides/<id>", methods=["GET"])
@login_required
def get_ride(current_user_id, id):
    """ Function returns a single ride for the current user"""
    try:
        int(id)
    except ValueError:
        return jsonify(
            {'message': 'Please provide a valid ride Id'}), 400
    ride = Rides.get_a_ride(id)
    if ride:
        return jsonify(ride), 200

    return jsonify({'message': 'Ride not found'}), 404

# Update a specific request
@rides_blueprint.route("/api/v2/rides/<id>", methods=["PUT"])
@login_required
def update_ride(current_user_id, id):
    """ Function updates details of a ride specified by an id"""
    try:
        int(id)
    except ValueError:
        return jsonify(
            {'message': 'Please provide a valid ride Id'}), 400
    if not request.json:
        abort(404)
    category = request.json['category']
    pick_up = request.json['pick_up']
    drop_off = request.json['drop_off']

    if category == "" or pick_up == "" or drop_off == "":

        return jsonify(
            {'message': 'Please fill all fields'}), 400

    message = Rides.update_a_ride(id, category, pick_up, drop_off)
    if message:

        return jsonify(message), 201
    else:
        return ({'message': 'update failed'}), 400

# Delete a specific request
@rides_blueprint.route("/api/v2/rides/<id>", methods=["DELETE"])
@login_required
def delete_ride(current_user_id, id):
    """ Function deletes a ride specified by a given id"""
    try:
        int(id)
    except ValueError:
        return jsonify(
            {'message': 'Please provide a valid ride Id'}), 400
    ride = Rides.get_a_ride(int(id))
    if len(ride) < 1:
        return jsonify({'message': 'ride not found'}), 400
    else:

        del_id = int(id)
        message = Rides.delete_a_ride(del_id)

        print(message)
        if message:
            return jsonify(message), 200
        else:
            return jsonify({'message': 'deleting failed'}), 404

@rides_blueprint.route("/api/v2/rides")
@login_required
def get_all_rides(current_user_id):
    """ Function returns all rides from the database"""
    ride = Rides.get_all_rides()
    if len(ride) > 0:
        return jsonify(ride), 200
    return jsonify({'message': 'no rides found'}), 404

