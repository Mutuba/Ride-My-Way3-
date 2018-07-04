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
            "/api/v2/auth/register",
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
        self.assertEquals(response.status_code, 200) ######
        self.headers = {'token': data[0]['token']}

    def test_api_create_ride_missing_category(self):
        """ Test returns true in ride creation"""
        response = self.client().post(
            "/api/v2/rides",
            data=json.dumps(self.ride2),
            headers=self.headers,
            content_type='application/json')
        self.assertEquals(response.status_code, 500)

    def test_api_create_ride_token_missing(self):
        """ Test api for missing token"""
        response = self.client().post(
            "/api/v2/rides",
            data=json.dumps(self.ride),
            content_type='application/json')

        self.assertEquals(response.status_code, 401)
        data = json.loads(response.data.decode())
        self.assertEquals(data['message'], 'token is missing')

    # def test_api_to_view_a_ride(self):
    #     """Test api to return a single ride given an id"""
    #     response = self.client().get(
    #         "/api/v2/rides/1",
    #         headers=self.headers)
    #     self.assertEquals(response.status_code, 200)

    def test_api_to_view_a_ride_not_found(self):
        """Test api to return a single ride given an id"""
        response = self.client().get(
            "/api/v2/rides/50",
            headers=self.headers)
        self.assertEquals(response.status_code, 404)

    def test_view_ride_not_int(self):
        response = self.client().get(
            '/api/v2/rides/n',
            headers=self.headers)
        data = json.loads(response.data.decode())
        self.assertEquals(response.status_code, 400)
        self.assertEquals(
            data['message'], 'Please provide a valid ride Id')


    def test_api_to_update_a_ride(self):
        """ Test api to update a ride given an id. Should pass"""
        response = self.client().put(
            "/api/v2/rides/1",
            data=json.dumps(self.ride),
            headers=self.headers,
            content_type='application/json')
        self.assertEquals(response.status_code, 201)

    def test_update_ride_not_int(self):
        response = self.client().put(
            '/api/v2/rides/n',
            headers=self.headers)
        data = json.loads(response.data.decode())
        self.assertEquals(response.status_code, 400)
        self.assertEquals(
            data['message'], 'Please provide a valid ride Id')


    def test_delete_ride_not_int(self):
        response = self.client().delete(
            '/api/v2/rides/n',
            headers=self.headers)
        data = json.loads(response.data.decode())
        self.assertEquals(response.status_code, 400)
        self.assertEquals(
            data['message'], 'Please provide a valid ride Id')


if __name__ == "__main__":
    unittest.main()
