#!/usr/bin/env python3

# Standard library imports

# Remote library imports
import uuid
from datetime import datetime
from dateutil import parser
from functools import wraps
from flask import request, jsonify, session, make_response
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError
# Local imports

from config import app, db, api, bcrypt
# Add your model imports
from models import Ride, User, Horse, Booking, BookingStatus, user_ride_table

# Views go here!



# @app.route('/register', methods=['POST'])
class Register(Resource):
    def post(self):
        data = request.json
        username = data.get('username')

        if User.query.filter_by(username=username).first():
            return jsonify({'error': 'Username already exists'})
    
        new_user = User(username=username)

        db.session.add(new_user)
        db.session.commit()

        return {"username": new_user.username}, 201

# @app.route('/api/check_session', methods=['GET'])
class Check_Session(Resource):
    def get(self):
        user_id = session.get('user_id')
        if user_id:
            user = session.get(user_id)
            return {"username": user.username}, 200
        else:
            return '', 401
    
# @app.route('/api/clear_session', methods=['DELETE'])
class Clear_Session(Resource):
    def delete(self):
        session.clear()
        return {}, 204

# @app.route('/api/login', methods=['POST'])
class Login(Resource):
    def post(self):
        data = request.json
        username = data.get('username')
        user = User.query.filter_by(username=username).first()

        if user:
            session['user_id'] = user.id
            return {"username": user.username}, 200
        else:
            return {'message': 'User not found'}, 404
    
# @app.route('/logout', methods=['DELETE'])
class Logout(Resource):
    def delete(self):
        session['user_id'] = None
        return {'message': '204: No Content'}, 204


# @app.route('/api/rides', methods=['POST'])
class Submit_Ride(Resource):
    def post(self):
    
        data = request.json
        user_id = session.get('user_id')
        if not user_id:
            return {"error": "Unauthorized"}, 401
        try:
            
            new_ride = Ride(
                name=data['name'],
                pickup_time=parser.isoparse(data.get('pickupTime')),
                spaces=data['spaces'],
                destination=data['destination'],
                duration=data['duration'],
                mileage=data['mileage'],
                user_id=user_id
            )
            db.session.add(new_ride)
            db.session.commit()

            return jsonify({'message': 'Ride Submitted!'})
        except ValueError as e:
            db.session.rollback()
            print(f'Error submitting ride: {e}')
            return jsonify({'error': 'Internal Server Error'}), 500

# @app.route('/api/rides', methods=['GET'])
class Get_Rides(Resource):
    def get(self):
        rides = Ride.query.all()
        rides_list = [{'id': ride.id, 'name': ride.name, 'spaces': ride.spaces, 'destination': ride.destination, 'duration': ride.duration, 'mileage': ride.mileage} for ride in rides]
        return jsonify(rides_list)


class ClaimedRides(Resource):
    def get(self):
        user_id = session.get('user_id')
        if not user_id:
            return {"error": "Unauthorized"}, 401
        
        user = session.get(user_id)
        if not user:
            return {"error": "User not found"}, 404
        
        claimed_rides = Ride.query.join(user_ride_table).filter(user_ride_table.c.user_id == user.id).all()
        rides_list = [{'id':ride.id, 'name': ride.name, 'destination': ride.destination, 'status': 'claimed'} for ride in claimed_rides]
        return jsonify(rides_list)
    
class Claim_Ride(Resource):
    def post(self):
        data = request.json
        ride_id = data.get('ride_id')
        username = data.get('username')
        
        try:
            ride = Ride.query.filter_by(id=ride_id).first()
            user = User.query.filter_by(username=username).first()

            if not ride or not user:
                return {"error": "Ride or User not found"}, 404
        
            if len(ride.claimers) >= ride.spaces:
                return {"error": "Ride or User not found"}, 400
        
            ride.claimers.append(user)

            user_ride = db.session.query(user_ride_table).filter_by(user_id=user.id, ride_id=ride.id).first()
            if user_ride:
                user_ride.status = 'claimed'
            db.session.commit()

            return {"message": "Ride claimed successfully"}, 200

        except IntegrityError:
            db.session.rollback()
            return {"error": "User has already claimed this ride"}, 400
        except Exception as e:
            db.session.rollback()
            print(f"Error claiming ride: {e}")
            return {"error": "Internal Server Error"}, 500
    
# @app.route('/api/cancel_reservation', methods=['POST'])
class Cancel_Reservation(Resource):
    def delete(self):
        data = request.get_json()
        ride_id = data.get('ride_id')
        user_id = session.get('user_id')


        try:
            ride = Ride.query.get(ride_id)
            user = User.query.get(user_id)

            if not ride or not user:
                return jsonify({'error': 'Ride or User not found'}), 404
        
            ride.claimers.remove(user)
            db.session.commit()

            return jsonify({'message': 'Reservation cancelled'}), 200
    
        except Exception as e:
            db.session.rollback()
            print(f'Error cancelling reservation: {e}')
            return jsonify({'error': 'Internal Server Error'}), 500

class MyRides(Resource):
    def get(self):
        user_id = session.get('user_id')
        
        if not user_id:
            return {"error": "Unauthorized"}, 401
        
        rides = Ride.query.filter_by(user_id=user_id).all()
        return jsonify([ride.to_dict() for ride in rides])
    
class AvailableRides(Resource):
    def get(self):
        rides = Ride.query.filter(
            Ride.spaces > 0,               # Ride must have available spaces
            Ride.pickup_time > datetime.now(),  # Pickup time must be in the future
            ~Ride.claimers.any()           # Ride must have no claimers (empty relationship)
        ).all()

        print(f"Available rides: {rides}")   # Add this for debugging

        if not rides:
            return [], 200
        
        rides_data = [ride.to_dict() for ride in rides]
        
        return rides_data, 200
    
class Update_Ride(Resource):
    def put(self, ride_id):
        data = request.json
        user_id = session.get('user_id')

        if not user_id:
            return {"error": "Unauhorized"}, 401
        
        ride = Ride.query.get(ride_id)

        if not ride:
            return {"error": "Ride not found"}, 404
        
        ride.name = data.get('name', ride.name)
        ride.pickup_time = parser.isoparse(data.get('pickupTime', ride.pickup_time.isoformat()))
        ride.spaces = data.get('spaces', ride.spaces)
        ride.destination = data.get('destination', ride.destination)
        ride.duration = data.get('duration', ride.duration)
        ride.mielage = data.get('mileage', ride.mileage)

        db.session.commit()

        return {"message": "Ride updated successfully"}, 200

class Delete_Ride(Resource):
    def delete(self,ride_id):
        user_id = session.get('user_id')
        if not user_id:
            return {"error": "Unauthorized"}, 401
        
        ride = Ride.query.get(ride_id)

        if not ride:
            return {"Error": "Ride not found"}, 404
        
        if ride.user_id != user_id:
            return {"error": "You can only delete your own rides"}, 403
        
        db.session.delete(ride)
        db.session.commit()

        return {"message": "Ride deleted successfully"}, 200
    

api.add_resource(Register, '/api/register')
api.add_resource(Login, '/api/login')
api.add_resource(Logout, '/api/logout')
api.add_resource(Clear_Session, '/api/clear_session')
api.add_resource(Check_Session, '/api/check_session')
api.add_resource(Cancel_Reservation, '/api/cancel_reservation')
api.add_resource(Claim_Ride, '/api/claim_ride')
api.add_resource(Get_Rides, '/api/rides')
api.add_resource(Submit_Ride, '/api/rides')
api.add_resource(MyRides, '/api/my_rides')
api.add_resource(AvailableRides, '/api/available_rides')
api.add_resource(Update_Ride, '/api/rides/<int:ride_id>')
api.add_resource(Delete_Ride, '/api/rides/<int:ride_id>/delete')
api.add_resource(ClaimedRides, '/api/claimed_rides')


if __name__ == '__main__':
    app.run(port=5555, debug=True)

