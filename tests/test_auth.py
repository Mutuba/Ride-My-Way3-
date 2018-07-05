import os
import unittest
import json
from app import create_app
import psycopg2


class TestAuth(unittest.TestCase):

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

    def test_user_registration(self):
        """ test for user registration"""
        response = self.client().post(
            '/api/v2/auth/signup',
            data=json.dumps(self.user),
            content_type='application/json')
        self.assertEquals(response.status_code, 406)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertEqual(
            response_msg["message"],
            "Password is weak! Must have atleast 8 characters")

    # def test_user_registration_successful(self):
    #     """ test for user registration"""
    #     response = self.client().post(
    #         '/api/v2/auth/signup',
    #         data=json.dumps(self.user5),
    #         content_type='application/json')
    #     self.assertEquals(response.status_code, 406)
    #     response_msg = json.loads(response.data.decode("UTF-8"))
    #     self.assertEqual(
    #         response_msg["message"],
    #         "Signup successful")

    def test_user_registration_username_contain_spaces(self):
        """ test for user registration"""
        response = self.client().post(
            '/api/v2/auth/signup',
            data=json.dumps(self.user7),
            content_type='application/json')
        self.assertEquals(response.status_code, 406)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertEqual(
            response_msg["message"],
            "Username cannot contain white spaces")

    def test_user_registration_username_exists(self):
        """ test for user registration"""
        response = self.client().post(
            '/api/v2/auth/signup',
            data=json.dumps(self.user8),
            content_type='application/json')
        self.assertEquals(response.status_code, 406)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertEqual(
            response_msg["message"],
            "User already registered")

    def test_valid_user_login(self):
        """test api for user login successful """
        response = self.client().post(
            '/api/v2/auth/login',
            data=json.dumps(self.user5),
            content_type='application/json')
        data = json.loads(response.data.decode())
        self.assertTrue(data[0]["token"])

    def test_invalid_user_login(self):
        """ Test for invalid user login. Should fail"""
        response = self.client().post(
            '/api/v2/auth/login',
            data=json.dumps(self.user2),
            content_type='application/json')
        self.assertEquals(response.status_code, 401)

    def test_invalid_password_length(self):
        """ test for invalid password passing. Should fail"""
        response = self.client().post(
            '/api/v2/auth/login',
            data=json.dumps(self.user3),
            content_type='application/json')
        data = json.loads(response.data.decode())
        self.assertEquals(data['message'],
                          'no valid user')

    def test_invalid_user_email(self):
        """ test api for invalid email"""
        response = self.client().post(
            '/api/v2/auth/signup',
            data=json.dumps(self.user6),
            content_type='application/json')
        data = json.loads(response.data.decode())
        self.assertEquals(
            data['message'], 'Email format is user@example.com')


if __name__ == "__main__":
    unittest.main()
