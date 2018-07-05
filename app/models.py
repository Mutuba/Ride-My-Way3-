# models.py Defines classes for users, rides, and requests
import os
import psycopg2
import datetime


conn = psycopg2.connect(
    host=os.getenv("HOST"), database=os.getenv("DATABASE"),
    user=os.getenv("USER"), password=os.getenv("PASSWORD"))


class User(object):
    def __init__(self, username, email, password, role):
        """ initialization. class constructor"""
        self.username = username
        self.email = email
        self.password = password
        self.role = role

    def create_user(self, username, email, password, role=None):
        """" Function creates a user with a
        username, email, password and role"""
        if role is None:
            role = False
        cur = conn.cursor()
        sql = "INSERT INTO users (username, email, password, role)\
                            VALUES (%s, %s, %s, %s)"
        data = (username, email, password, role)
        cur.execute(sql, data)

        conn.commit()
        cur.close()
        print("New user added to user table")

    def show_users(self):
        """ Function returns all users' id, email, username, password, role"""
        cur = conn.cursor()
        cur.execute("SELECT * FROM users;")
        columns = ('user_id', 'username', 'email', 'password', 'role')
        users = []
        for user in cur.fetchall():
            users.append(dict(zip(columns, user)))
        return users

    def promote_user(self, id):
        """ Function promotes a user's role """
        cur = conn.cursor()
        role = True
        sql = "UPDATE users SET role=(%s) WHERE user_id=(%s);"
        data = (role, id)
        cur.execute(sql, data)
        conn.commit()
        return ({"message": "User promoted"})

    def delete_user(self, id):
        """ Function deletes a user from the database given an id"""
        cur = conn.cursor()
        sql = "DELETE from users WHERE user_id = (%s)"
        data = (id, )
        cur.execute(sql, data)
        return({"message": "User deleted"})

    def login(self, name, pswd):
        """ Function logs in a user after validating user details"""
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE username = (%s)", [name])
        columns = ('user_id', 'username', 'email', 'password', 'role')
        users = []
        for user in cur.fetchall():
            users.append(dict(zip(columns, user)))
        return users

    def get_user(self, id):
        """ Returns a single user by id from the database"""
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE user_id = (%s)", [id])
        columns = ('user_id', 'username', 'email', 'password', 'role')
        users = []
        for user in cur.fetchall():
            users.append(dict(zip(columns, user)))
        return users

    def get_role(self, id):
        """ Returns the role of a user """
        cur = conn.cursor()
        cur.execute("SELECT role FROM users WHERE user_id = (%s)", [id])
        roles = []
        for role in cur.fetchall():
            roles.append(role)
        return roles

    def get_all_users(self):
        cur = conn.cursor()
        cur.execute("SELECT username FROM users")
        users = []
        for user in cur.fetchall():
            users.append(user)
        return users


class Ride(object):

    def __init__(
        self, category, pick_up, drop_off,
        date_time, ride_status, creator_id
    ):
        """ Class initialization."""

        self.category = category
        self.pick_up = pick_up
        self.drop_off = drop_off
        self.date_time = date_time
        self.ride_status = ride_status
        self. creator_id = creator_id

    def create_ride(
        self, category, pick_up,
        drop_off, date_time,
        ride_status, creator_id
    ):
        """ Creates a ride and updates the database"""
        cur = conn.cursor()
        sql = "INSERT INTO rides(ride_date, category, pick_up,\
                                    drop_off, date_time,\
                                     ride_status, creator_id)\
                            VALUES (%s, %s, %s, %s, %s, %s, %s);"
        date = datetime.datetime.now()
        data = (date, category, pick_up, drop_off,
                date_time, ride_status, creator_id)
        cur.execute(sql, data)

        conn.commit()
        cur.close()

        print("New ride added to user table")

    def get_user_rides(self, id):
        """ Function returns current user's rides from the database """
        cur = conn.cursor()
        cur.execute("SELECT * FROM rides WHERE creator_id = (%s)", [id])
        columns = ('ride_id', 'ride_date', 'category',
                   'pick_up', 'drop_off',
                   'date_time', 'ride_status', 'creator_id')
        rides = []
        for ride in cur.fetchall():
            rides.append(dict(zip(columns, ride)))
        return rides

    def get_a_ride(self, id):
        """ Function returns a ride by id from the database"""
        cur = conn.cursor()
        cur.execute("SELECT * FROM rides WHERE ride_id = (%s)", [id])
        columns = ('ride_id', 'ride_date', 'category',
                   'pick_up', 'drop_off',
                   'date_time', 'ride_status', 'creator_id')
        rides = []
        for ride in cur.fetchall():
            print(ride)
            rides.append(dict(zip(columns, ride)))
        return rides

    def update_a_ride(
        self, id, category,
        pick_up, drop_off
    ):
        """ Function updtaes a ride details by id."""
        cur = conn.cursor()
        sql = "UPDATE rides SET category=(%s), pick_up=(%s),\
                 drop_off=(%s) WHERE ride_id = (%s)"
        data = (category, pick_up, drop_off, id)
        cur.execute(sql, data)
        conn.commit()
        return {'message': 'ride updated successfully'}

    def delete_a_ride(self, id):
        """ Function deletes a ride by id from the database"""

        cur = conn.cursor()
        cur.execute("DELETE from rides WHERE ride_id=(%s)", [id])
        conn.commit()
        return {'message': 'ride deleted'}

    def get_all_rides(self):
        """ Function returns all the rides from the database"""
        cur = conn.cursor()
        cur.execute("SELECT * FROM rides;")
        columns = ('ride_id', 'ride_date', 'category',
                   'pick_up', 'drop_off',
                   'date_time', 'ride_status', 'creator_id')
        rides = []
        for ride in cur.fetchall():
            rides.append(dict(zip(columns, ride)))
        return rides

    def get_status(self, id):
        """ Function returns the status of a ride from the database"""
        cur = conn.cursor()
        cur.execute(
            "SELECT ride_status FROM rides WHERE ride_id = (%s)", [id])
        status = []
        for s in cur.fetchall():
            status.append(s)
        return status


class Request(object):

    def __init__(self, request_description,
        request_priority, request_status, ride_id
    ):
        """ Class initialization. An instance of request will have this attributes. """

        self.request_description = request_description
        self.request_priority = request_priority
        self.request_status = request_status
        self.ride_id = ride_id

    def create_request(
        self, request_description,
        request_priority, request_status,
        requester_id, ride_id
    ):
        """ Function creates a ride request and saves to the database"""
        cur = conn.cursor()
        sql = "INSERT INTO requests(request_date, request_description,\
                                    request_priority,\
                                    request_status, requester_id, ride_id)\
                            VALUES (%s, %s, %s, %s, %s, %s);"
        date = datetime.datetime.now()
        data = (date, request_description,
                request_priority, request_status, requester_id, ride_id)
        cur.execute(sql, data)

        conn.commit()
        cur.close()

        print("New request added to user table")

    def get_user_requests(self, id):
        """ Function returns a particular user's ride requests"""
        cur = conn.cursor()
        cur.execute("SELECT * FROM requests WHERE requester_id = (%s)", [id])
        columns = ('request_id', 'request_date',
                   'request_description', 'request_priority',
                   'request_status', 'requester_id', 'ride_id')
        requests = []
        for request in cur.fetchall():

            requests.append(dict(zip(columns, request)))
        return requests

    def get_a_request(self, id):
        """ Function returns a request by id """
        cur = conn.cursor()
        cur.execute("SELECT * FROM requests WHERE request_id = (%s)", [id])
        columns = ('request_id', 'request_date',
                   'request_description', 'request_priority',
                   'request_status', 'requester_id', 'ride_id')
        requests = []

        for request in cur.fetchall():

            print(request)

            requests.append(dict(zip(columns, request)))

        return requests

    def update_a_request(self, id, description, priority):
        """ Function updates a request's description and priority"""
        cur = conn.cursor()

        sql = "UPDATE requests SET request_description=(%s), request_priority=(%s)\
                WHERE request_id = (%s)"

        data = (description, priority, id)

        cur.execute(sql, data)

        conn.commit()

        return {'message': 'request updated successfully'}

    def delete_a_request(self, id):
        """ Function deletes a user request form the databaase"""
        cur = conn.cursor()

        cur.execute("DELETE from requests WHERE request_id=(%s)", [id])

        conn.commit()

        return {'message': 'request deleted'}

    def get_all_requests(self, id):
        """ Function returns all requests from the database"""
        cur = conn.cursor()

        cur.execute("SELECT * FROM requests WHERE ride_id=(%s)", [id])
        columns = ('request_id', 'request_date',
                   'request_description', 'request_priority',
                   'request_status', 'requester_id', 'ride_id')
        requests = []

        for request in cur.fetchall():

            requests.append(dict(zip(columns, request)))
        return requests

    def get_status(self, id):
        """ Function returns the status of a request by id from the database"""
        cur = conn.cursor()
        cur.execute(
            "SELECT request_status FROM requests \
            WHERE request_id = (%s)", [id])
        status = []
        for s in cur.fetchall():
            status.append(s)
        return status

    def accept_a_request(self, id):
        """ Function enables a user to accept a request by id"""
        cur = conn.cursor()
        sql = "UPDATE requests SET request_status=(%s) WHERE request_id=(%s)"
        data = ("Accepted", id)
        cur.execute(sql, data)
        conn.commit()
        return {'message': 'Request approved'}

    def reject_a_request(self, id):
        """ Function enables a user to reject a ride request"""
        cur = conn.cursor()
        sql = "UPDATE requests SET request_status=(%s) WHERE request_id=(%s)"
        data = ('Rejected', id)
        cur.execute(sql, data)
        conn.commit()
        return {'message': 'Request rejected'}

