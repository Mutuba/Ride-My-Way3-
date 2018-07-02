from flask import Flask, abort, request, jsonify
from instance.config import app_config, SECRET_KEY
from V2.models import User, Ride, Request
import jwt
import datetime
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash
import re


Users = User()
Rides = Ride()
Requests = Request()


def create_app(config_name):
    """ Creates a falsk app based on config passed:
    development, testing, production"""

    # enables relative parameter passing
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile("config.py")

    def empty(**data):
        '''method to validate username input'''
        messages = {}
        for key in data:
            newname = re.sub(r'\s+', '', data[key])
            if not newname:
                message = {'message': key + ' cannot be an empty string'}
                messages.update({key + '-Error:': message})
        return messages

    def whitespace(data):
        '''method to validate white'''
        newname = re.sub(r'\s+', '', data)
        afterlength = len(newname)
        actuallength = len(data)
        if afterlength != actuallength:
            return True

    def val_none(**data):
        '''method to check none'''
        messages = {}
        for key in data:
            if data[key] is None:
                message = {'message': key + ' cannot be missing'}
                messages.update({key + '-Error:': message})
        return messages

    def pass_length(data):
        if len(data) < 8:
            return True

    def email_prtn(data):
        pattern = re.match(
            r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", data)
        if not pattern:
            return True

    # Decorator function to check for jwt token in the headers
    def login_required(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            token = None

            if 'access-token' in request.headers:
                token = request.headers['access_token']

            else:
                token = request.headers.get('token')

            if not token:
                return jsonify({'message': 'token is missing'}), 401

            try:
                data = jwt.decode(token, SECRET_KEY)

                kwargs['current_user_id'] = data['user_id']

            except:
                return jsonify({'message': 'Invalid token'}), 401
            return f(*args, **kwargs)
        return decorated

    @app.route("/api/v2/auth/register", methods=["POST"])
    def register_user():
        """ Method creates a user account using email, username and password"""
        if request.json:
            print(request.json)
            new_user = {
                "email": request.json['email'],
                "username": request.json['username'],
                "password": request.json['password']
            }
            # get all user accounts from the database
            users = Users.get_all_users() # retirns a list 
            all_users = []  # create a list (empty first)
            for user in users:  # loop through users each time append to list
                all_users.append(user[0])

            # dict_data = {'email': email, 'username': username, 'password': password}

            if val_none(**new_user):

                result = val_none(**new_ride)

                return jsonify(result), 406

            if empty(**new_user):

                result = empty(**new_user)

                return jsonify(result), 406
            val_pass = whitespace(request.json['username'])
            if val_pass:
                return jsonify(
                    {'message': 'Username cannot contain white spaces'}), 406
            val_length = pass_length(request.json['password'])
            if val_length:
                return jsonify(
                    {'message':
                    'Password is weak! Must have atleast 8 characters'}), 406
            val_email = email_prtn(request.json['email'])

            if val_email:
                return jsonify(
                    {'message':
                        'Email format is user@example.com'}), 406

            if new_user['username'] in all_users:

                return jsonify({'message': 'User already registered'}), 400

            hashed_pswd = generate_password_hash(new_user['password'])

            Users.create_user(
                new_user['username'], new_user['email'],
                hashed_pswd)
            return jsonify({'message': 'User created successfully'}), 201

    # User can login using email and password
    @app.route("/api/v2/auth/login", methods=["POST"])
    def login():
        """ Function logs in a user after
        validating username and password inputs"""
        if request.json:
            username = request.json["username"]
            password = request.json["password"]

        if username == "" or password == "":

            return jsonify({'message': 'Please fill all fields'})

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
                        {'role': role}), 201
        return jsonify(
            {"message": "no valid user"}), 401

    @app.route("/api/v2/rides", methods=["POST"])
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
                {'message': 'Failed, Request already made'}), 201

        Rides.create_ride(
            new_ride['category'], new_ride['pick_up'],
            new_ride['drop_off'], new_ride['date_time'],
            new_ride['ride_status'], new_ride['creator_id'])
        return jsonify(
            {'message': 'Ride created successfully'}), 201

    @app.route("/api/v2/users/rides/<int:id>", methods=["GET"])
    @login_required
    def get_ride(current_user_id, id):
        """ Function returns a single ride for the current user"""
        my_ride_id = int(id)
        ride = Rides.get_a_ride(my_ride_id)
        if ride:
            if ride[0]['creator_id'] == current_user_id:
                return jsonify(ride), 200
            return jsonify({'message': 'Not authorized to view ride'})
        return jsonify({'message': 'Ride not found'}), 200

    # Update a specific request
    @app.route("/api/v2/users/rides/<int:id>", methods=["PUT"])
    @login_required
    def update_ride(current_user_id, id):
        """ Function updates details of a ride specified by an id"""
        if not request.json:
            abort(404)
        category = request.json['category']
        pick_up = request.json['pick_up']
        drop_off = request.json['drop_off']

        if category == "" or pick_up == "" or drop_off == "":

            return jsonify({'message': 'Please fill all fields'})

        message = Rides.update_a_ride(id, category, pick_up, drop_off)
        if message:
            return jsonify(message), 201
        else:
            return ({'message': 'update failed'})

    # Delete a specific request
    @app.route("/api/v2/users/rides/<int:id>", methods=["DELETE"])
    @login_required
    def delete_ride(current_user_id, id):
        """ Function deletes a ride specified by a given id"""
        ride = Rides.get_a_ride(int(id))
        if len(ride) < 1:
            return jsonify({'message': 'ride not found'})
        else:
            del_id = int(id)
            message = Rides.delete_a_ride(del_id)

            print(message)
            if message:
                return jsonify(message), 200
            else:
                return jsonify({'message': 'deleting failed'})

    @app.route("/api/v2/users/rides")
    @login_required
    def get_all_rides(current_user_id):
        """ Function returns all rides from the database"""
        ride = Rides.get_all_rides()
        print(ride)
        if len(ride) > 0:
            return jsonify(ride), 200
        return jsonify({'message': 'no rides found'})

    # ride requests endpoints
    @app.route("/api/v2/rides/<int:id>/requests", methods=["POST"])
    @login_required
    def create_request(current_user_id, id):
        """ Function enables a user to create a request for a ride"""
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

            return jsonify({'message': 'Failed, Request already made'}), 201

        Requests.create_request(req['request_description'],
                                req['request_priority'],
                                req['request_status'], req['requester_id'],
                                req['ride_id'])
        return jsonify({'message': 'Request created successfully'}), 201

    # View a specific request
    @app.route("/api/v2/rides/requests/<int:id>", methods=["GET"])
    @login_required
    def get_request(current_user_id, id):
        """ FUnction returns a ride request by id"""
        req_id = int(id)
        request = Requests.get_a_request(req_id)
        if request:
            if request[0]['requester_id'] == current_user_id:
                return jsonify(request), 200
            return jsonify({'message': 'Not authorized to view request'})
        return jsonify({'message': 'Request not found'}), 200

    # Update a specific request
    @app.route("/api/v2/rides/requests/<int:id>", methods=["PUT"])
    @login_required
    def update_request(current_user_id, id):
        """ Function updated a ride request"""
        if not request.json:
            abort(404)
        description = request.json['request_description']
        priority = request.json['request_priority']

        if priority == "" or description == "":

            return jsonify({'message': 'Please fill all fields'})

        message = Requests.update_a_request(id, description, priority)
        if message:
            return jsonify(message), 201
        else:
            return ({'message': 'update failed'})

    # Delete a specific request
    @app.route("/api/v2/rides/requests/<int:id>", methods=["DELETE"])
    @login_required
    def delete_request(current_user_id, id):
        """ Function deletes a ride request from the database"""
        request = Requests.get_a_request(int(id))

        if len(request) < 1:
            return jsonify({'message': 'Request not found'})
        else:
            del_id = int(id)
            message = Requests.delete_a_request(del_id)
            print(message)
            if message:
                return jsonify(message), 200
            else:
                return jsonify({'message': 'deleting failed'})

    # User can view all available requests
    @app.route("/api/v2/rides/requests")
    @login_required
    def get_all_requests(current_user_id):
        """ Function gets all ride requests available in the database"""
        request = Requests.get_all_requests()
        print(request)
        if len(request) > 0:
            return jsonify(request), 200

        return jsonify({'message': 'no requests found'})

    # Accept a ride request
    @app.route("/api/v2/rides/requests/<int:id>/accept", methods=["PUT"])
    @login_required
    def accept_request(current_user_id, id):
        """ Function enables a user to accept a ride request offer"""
        status_list = Requests.get_status(id)
        print(status_list)
        if len(status_list) == 0:
            return jsonify({'message': 'No request found'}), 200
        status = status_list[0][0].lower()
        if status == "open":
            message = Requests.accept_a_request(id)
            return jsonify(message), 200
        elif status == 'rejected':
            return jsonify({'message': 'Request already Rejected'})

    # Reject a request for a ride. Driver action
    @app.route("/api/v2/rides/requests/<int:id>/reject", methods=["PUT"])
    @login_required
    def reject_request(current_user_id, id):
        """if Users.get_role(current_user_id)[0][0]:
        Function enables a user to reject a ride request"""
        status_list = Requests.get_status(id)
        print(status_list)
        if len(status_list) == 0:
            return jsonify({'message': 'No request found'}), 200
        status = status_list[0][0].lower()

        print(status)
        if status == "pending":
            message = Requests.reject_a_request(id)
            return jsonify(message), 201
        elif status == 'approved':
            return jsonify(
                {'message': 'Request already accepted'})
        # return jsonify({'message': 'Only allowed for the driver'})



    return app
