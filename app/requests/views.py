
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


requests_blueprint = Blueprint('requests', __name__)

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

# ride requests endpoints
@requests_blueprint.route("/api/v2/rides/<id>/requests", methods=["POST"])
@login_required
def create_request(current_user_id, id):
    """ Function enables a user to create a request for a ride"""
    try:
        int(id)
    except ValueError:
        return jsonify(
            {'message': 'Please provide a valid request Id'}), 400
    if not request.json:
        abort(404)
    req = {
        "request_description": request.json['request_description'],
        "request_priority": request.json['request_priority'],
        "request_status": "Open",
        "requester_id": current_user_id,
        "ride_id": id
    }

    for values in req.values():
        if values == "":

            return jsonify({'message': 'Please fill all fields'})

    requests = Requests.get_user_requests(current_user_id)
    desc = [request['request_description'] for request in requests]
    if req['request_description'] in desc:

        return jsonify({'message': 'Failed, Request already made'}), 400

    Requests.create_request(req['request_description'],
                            req['request_priority'],
                            req['request_status'], req['requester_id'],
                            req['ride_id'])
    return jsonify({'message': 'Request created successfully'}), 201

# View a specific request
@requests_blueprint.route("/api/v2/rides/requests/<id>", methods=["GET"])
@login_required
def get_request(current_user_id, id):
    try:
        int(id)
    except ValueError:
        return jsonify(
            {'message': 'Please provide a valid request Id'}), 400
    """ FUnction returns a ride request by id"""
    req_id = int(id)
    request = Requests.get_a_request(req_id)
    if request:
        if request[0]['requester_id'] == current_user_id:
            return jsonify(request), 200
        return jsonify({'message': 'Not authorized to view request'}), 401

    return jsonify({'message': 'Request not found'})

# Update a specific request
@requests_blueprint.route("/api/v2/rides/requests/<id>", methods=["PUT"])
@login_required
def update_request(current_user_id, id):
    """ Function updated a ride request"""
    try:
        int(id)
    except ValueError:
        return jsonify(
            {'message': 'Please provide a valid request Id'}), 400
    if not request.json:
        abort(404)

    description = request.json['request_description']
    priority = request.json['request_priority']

    if priority == "" or description == "":

        return jsonify({'message': 'Please fill all fields'}), 400

    message = Requests.update_a_request(id, description, priority)
    if message:
        return jsonify(message), 201
    else:
        return ({'message': 'update failed'}), 400

# Delete a specific request
@requests_blueprint.route("/api/v2/rides/requests/<id>", methods=["DELETE"])
@login_required
def delete_request(current_user_id, id):
    """ Function deletes a ride request from the database"""
    try:
        int(id)
    except ValueError:
        return jsonify(
            {'message': 'Please provide a valid request Id'}), 400
    request = Requests.get_a_request(int(id))

    if len(request) < 1:
        return jsonify({'message': 'Request not found'}), 404
    else:

        del_id = int(id)
        message = Requests.delete_a_request(del_id)
        if message:
            return jsonify(message), 200
        else:
            return jsonify({'message': 'deleting failed'}), 400

# User can view all available requests
@requests_blueprint.route("/api/v2/rides/<id>/requests")
@login_required
def get_all_requests(current_user_id, id):
    """ Function gets all ride requests available in the database"""
    try:
        int(id)
    except ValueError:
        return jsonify(
            {'message': 'Please provide a valid request Id'}), 400
    request = Requests.get_all_requests(id)
    if len(request) > 0:
        return jsonify(request), 200

    return jsonify({'message': 'no requests found'}), 404

# Accept a ride request
@requests_blueprint.route("/api/v2/rides/requests/<id>/accept", methods=["PUT"])
@login_required
def accept_request(current_user_id, id):
    """ Function enables a user to accept a ride request offer"""
    try:
        int(id)
    except ValueError:
        return jsonify(
            {'message': 'Please provide a valid request Id'}), 400
    status_list = Requests.get_status(id)
    if len(status_list) == 0:
        return jsonify({'message': 'No request found'}), 404
    status = status_list[0][0].lower()
    if status == "open":
        message = Requests.accept_a_request(id)
        return jsonify(message), 200
    elif status == 'rejected':
        return jsonify({'message': 'Request already Rejected'}), 400

# Reject a request for a ride. Driver action
@requests_blueprint.route("/api/v2/rides/requests/<id>/reject", methods=["PUT"])
@login_required
def reject_request(current_user_id, id):
    """if Users.get_role(current_user_id)[0][0]:
    Function enables a user to reject a ride request"""
    try:
        int(id)
    except ValueError:
        return jsonify(
            {'message': 'Please provide a valid request Id'}), 400
    status_list = Requests.get_status(id)
    if len(status_list) == 0:
        return jsonify({'message': 'No request found'}), 200
    status = status_list[0][0].lower()

    if status == "pending":
        message = Requests.reject_a_request(id)
        return jsonify(message), 201
    elif status == 'approved':
        return jsonify(
            {'message': 'Request already accepted'}), 400