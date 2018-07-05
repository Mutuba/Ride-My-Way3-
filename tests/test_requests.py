# Tests for ride request creation, update, rejection, deletion

import os
import unittest
import json
from app import create_app
import psycopg2


class TestRequests(unittest.TestCase):

    def setUp(self):
        # Initialize our variable before test
        self.app = create_app('testing')  # Creates flask app for testing
        self.client = self.app.test_client
        self.user = {"username": 'test', "email": 'test@gmail.com',
                     "password": 'test123'}
        self.user2 = {"username": 'test', "password": 'wrong'}
        self.user3 = {"username": "test2", "email": "test2@gmail.com",
                      "password": "1234"}
        self.user4 = {"username": "test3", "email": "test23@gmail.com",
                      "password": "test123456"}
        self.user5 = {"username": "daniel", "email": "danielmutuba@gmail.com",
                      "password": "baraka11"}

        self.user6 = {"username": "daniel", "email": "danielmu.com",
                      "password": "baraka11"}

        self.user7 = {
            "username": "dan  iel",
            "email": "danielmutuba@gmail.com",
            "password": "baraka11"}

        self.user8 = {
            "username": "daniel", "email": "danmutuba@gmail.com",
            "password": "baraka11"}

        self.request = {
            "request_description": "Testing_update_3 request",
            "request_priority": "High",
            "request_status": "Pending"
        }

        self.ride = {
            "category": "SUVd",
            "pick_up": "Andela",
            "drop_off": "Uthiru",
            "date_time": "2nd July 2000 hrs"
        }
        # category missing
        self.ride2 = {
            "category": "",
            "pick_up": "Andela",
            "drop_off": "Uthiru",
            "date_time": "2nd July 2000 hrs"
        }

        user = self.client().post(
            "/api/v2/auth/signup",
            data=json.dumps(self.user5),
            content_type="application/json")
        # pass successful registration details to login endpoint
        response = self.client().post('/api/v2/auth/login',
                                      data=json.dumps(self.user5),
                                      content_type='application/json')
        data = json.loads(response.data.decode('UTF-8'))
        self.assertTrue(data[0]["token"])
        self.assertEquals(response.status_code, 200)
        self.headers = {'token': data[0]['token']}

        response = self.client().post(
            '/api/v2/auth/login',
            data=json.dumps(self.user5),
            content_type='application/json')
        data = json.loads(response.data.decode('UTF-8'))
        self.assertTrue(data[0]["token"])
        self.assertEquals(response.status_code, 200)
        self.headers = {'token': data[0]['token']}

    def test_api_for_user_create_request(self):
        response = self.client().post("/api/v2/rides/1/requests",
                                      data=json.dumps(self.request),
                                      headers=self.headers,
                                      content_type='application/json')
        self.assertEquals(response.status_code, 201)

    def test_api_to_view_a_request(self):
        """Test api to return a single ride request given an id"""
        response = self.client().get(
            "/api/v2/rides/requests/1",
            headers=self.headers)
        self.assertEquals(response.status_code, 200)

    def test_api_to_view_a_request_not_found(self):
        """Test api to return a single ride given an id"""
        response = self.client().get(
            "/api/v2/rides/requests/50",
            headers=self.headers)
        self.assertEquals(response.status_code, 200)

    def test_api_to_view_requests(self):
        """Test api to return all requests from database"""
        response = self.client().get(
            "/api/v2/rides/requests/1",
            headers=self.headers)
        self.assertEquals(response.status_code, 200)

    def test_view_request_not_int(self):
        response = self.client().get(
            '/api/v2/rides/requests/n',
            headers=self.headers)
        data = json.loads(response.data.decode())
        self.assertEquals(response.status_code, 400)
        self.assertEquals(
            data['message'], 'Please provide a valid request Id')

    def test_api_to_update_a_request(self):
        """ Test api to update a request. Should pass"""
        response = self.client().put(
            "/api/v2/rides/requests/1",
            data=json.dumps(self.request),
            headers=self.headers,
            content_type='application/json')
        self.assertEquals(response.status_code, 201)

    def test_update_request_not_int(self):
        response = self.client().put(
            '/api/v2/rides/requests/n',
            headers=self.headers)
        data = json.loads(response.data.decode())
        self.assertEquals(response.status_code, 400)
        self.assertEquals(
            data['message'], 'Please provide a valid request Id')

    def test_delete_request_not_int(self):
        response = self.client().delete(
            '/api/v2/rides/requests/n',
            headers=self.headers)
        data = json.loads(response.data.decode())
        self.assertEquals(response.status_code, 400)
        self.assertEquals(
            data['message'], 'Please provide a valid request Id')


    def test_reject_request_id_not_int(self):
        response = self.client().put(
            '/api/v2/rides/requests/m/reject',
            headers=self.headers)
        data = json.loads(response.data.decode())
        self.assertEquals(response.status_code, 400)
        self.assertEquals(
            data['message'], 'Please provide a valid request Id')

    def test_accept_request_not_int(self):
        response = self.client().put(
            '/api/v2/rides/requests/n/accept',
            headers=self.headers)
        data = json.loads(response.data.decode())
        self.assertEquals(response.status_code, 400)
        self.assertEquals(
            data['message'], 'Please provide a valid request Id')


if __name__ == "__main__":
    unittest.main()
