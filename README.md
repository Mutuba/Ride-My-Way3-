# Ride-My-Way3-

## Ride-My-Way2

A Web Application that enable users(CarTax Operators) to create an account and be able to create ride offers. Passengers will be able to view the ride offers and request to join:

- Register an account and Login into it.
- Register, Update and delete a Ride .
- View all Rides.
- View One Rides.
- Post Requests for rides.
- View all Requests for rides
- Change users password

## Prerequisites

- Python 3.6 or a later version

## Installation
Clone the repo.
```
$ git clone https://github.com/mutuba/Ride-My-Way2.git
```
and cd into the folder:
```
$ /Ride-My-Way
```
## Virtual environment
Create a virtual environment:
```
mkvirtualenv <virtual environment name>
```
## Dependencies
Install package requirements to your environment.
```
pip install -r requirements.txt
```

## Testing
To set up unit testing environment:

```
$ pip install nose
$ pip install coverage
```

To run tests perform the following:

```
$ nosetests --with-coverage. Also pytest -v
```


## Start The Server
To start the server run the following command
```
Set environment variable as follows:
$ EXPORT FLASK_APP=V1/__init__.py
Then run:
python manage.py run 
```
The server will run on port: 5000

## Testing API on Postman

*Note* Ensure that after you succesfully login a user, you use the generated token in the authorization header for the endpoints that require authentication. Remeber to add Bearer before the token as shown:
```
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9eyJpYXQiO 
```


### API endpoints

| Endpoint | Method |  Functionality | Authentication |
| --- | --- | --- | --- |
| /api/auth/v1/register | POST | Creates a user account | FALSE
| /api/auth/v1/login | POST | Logs in a user | TRUE
| /api/auth/v1/logout | POST | Logs out a user | TRUE
| /api/auth/v1/change_password | POST | Change user password | TRUE
| /api/v1/rides | POST | Creates a ride | TRUE
| /api/v1/rides | GET | Retrieves all rides | TRUE 
| /api/v1/rides/{ride_id} | GET | Get a ride | TRUE
| /api/v1/rides/{ride_id} | PUT | Update a ride details | TRUE
| /api/v1/rides/{ride_id} | DELETE | Delete a ride | TRUE
| /api/v1/rides/{ride_id}/requests | POST | Request a ride | TRUE
| /api/v1/rides/{ride_id}/requests | GET | Get all requests for a ride | TRUE



## API Documentation

## Authors

* **Daniel Mutuba** - [mutuba](https://github.com/mutuba)

## Acknowledgments