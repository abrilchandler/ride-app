#!/usr/bin/env python3

# Standard library imports

# Remote library imports
from functools import wraps
from flask import request, jsonify, session, redirect, url_for
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError
# Local imports

from config import app, db, api, bcrypt
# Add your model imports
from models import Ride, User, Horse, Booking, BookingStatus, user_ride_table

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



@app.route('/register', methods=['POST'])
def register():
    data = request.json
    user = User(username=data['username'], email=data['email'])
    user.set_password(data['password'])
    db.session.add(user)
    db.session.commit()
    return jsonify({'message': 'User registered success'}), 201

@app.route('/login', methods=['POST'])
def login():
    data=request.json
    user = User.query.filter_by(username=data['username']).first()
    if user and user.check_password(data['password']):
        session['user_id'] = user.id
        return jsonify({'message': 'Logged in successfully'})
    else:
        return jsonify({'message': "Invalid login"}), 401
    

            

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

@app.route('/api/claim_ride', methods=['POST'])
def claim_ride():
    data = request.get_json()
    ride_id = data.get('ride_id')
    user_id = data.get('user_id')

    try:
        ride = Ride.query.get(ride_id)
        user = User.query.get(user_id)

        if not ride or not user:
            return jsonify({'error': 'Ride or User not found'}), 404
        
        if len(ride.claimers) >= ride.spaces:
            return jsonify({'error': 'Ride or User not found'}), 400
        
        ride.claimers.append(user)
        db.session.commit()

        return jsonify({'message': 'Ride claimed successfully'}), 200

    except IntegrityError:
        db.session.rollback()
        return jsonify({'error': 'User has already claimed this ride'}), 400
    except Exception as e:
        db.session.rollback()
        print(f"Error claiming ride: {e}")
        return jsonify({'error': 'Internal Server Error'}), 500
    
@app.route('/api/cancel_reservation', methods=['POST'])
def cancel_reservation():
    data = request.get_json()
    ride_id = data.get('ride_id')
    user_id = data.get('user_id')

    try:
        ride = Ride.query.get(ride_id)
        user = User.query.get(user_id)

        if not ride or not user:
            return jsonify({'error': 'Ride or User not found'}), 404
        
        ride.claimers.remove(user)
        db.session.commit()

        return jsonify({'message': 'Reservation cancelled'}), 200
    
    except Exception as e:
        db.session.rollbacl()
        print(f'Error cancelling reservatio: {e}')
        return jsonify({'error': 'Internal Server Error'}), 500



if __name__ == '__main__':
    app.run(port=5555, debug=True)

