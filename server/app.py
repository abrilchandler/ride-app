#!/usr/bin/env python3

# Standard library imports

# Remote library imports
from flask import request, jsonify
from flask_restful import Resource

# Local imports

from config import app, db, api
# Add your model imports
from models import Ride

# Views go here!

@app.route('/')
def index():
    return '<h1>Project Server</h1>'

@app.route('/create-rides')
def create_rides():
    return '<h1></h1>'

@app.route('/my-rides')
def my_rides():
    return '<h1></h1>'

@app.route('/api/rides', methods=['POST'])
def submit_ride():
    data = request.json
    new_ride = Ride(
        name=data['name'],
        spaces=data['spaces'],
        destination=data['destination'],
        duration=data['duration'],
        mileage=['mileage']
    )
    db.session.add(new_ride)
    db.session.commit()
    return jsonify({'message': 'Ride Submitted!'})

@app.route('/api/rides', methods=['GET'])
def get_rides():
    rides = Ride.query.all()
    rides_list = [{'id': ride.id, 'name': ride.name, 'spaces': ride.spaces, 'destination': ride.destination, 'duration': ride.duration, 'mileage': ride.mileage} for ride in rides]
    return jsonify(rides_list)

if __name__ == '__main__':
    app.run(port=5555, debug=True)

