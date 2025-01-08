#!/usr/bin/env python3

# Standard library imports

# Remote library imports
from datetime import datetime
from dateutil import parser
from flask import request, jsonify, session
from flask_restful import Resource, Api
from sqlalchemy.exc import IntegrityError

# Local imports
from config import app, db
from models import Ride, User, Booking, BookingStatus

# Flask-RESTful API setup
api = Api(app)

class CheckSession(Resource):
    def get(self):
        user_id = session.get('user_id')
        if user_id:
            user = User.query.get(user_id)
            if user:
                return {"message": "User is logged in", "username": user.username}, 200
        return {"message": "No user logged in"}, 401

# Register a new user
class Register(Resource):
    def post(self):
        data = request.json
        username = data.get('username')

        if User.query.filter_by(username=username).first():
            return jsonify({'error': 'Username already exists'}), 400
        
        new_user = User(username=username)

        db.session.add(new_user)
        db.session.commit()

        return {"username": new_user.username}, 201

# Login a user
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

# Log out a user
class Logout(Resource):
    def delete(self):
        session['user_id'] = None
        return {'message': 'Logged out successfully'}, 204

# View all rides (public route)
class Get_Rides(Resource):
    def get(self):
        rides = Ride.query.all()
        rides_list = [{'id': ride.id, 'name': ride.name, 'spaces': ride.spaces, 'destination': ride.destination, 'duration': ride.duration, 'mileage': ride.mileage} for ride in rides]
        return jsonify(rides_list)

# Submit a new ride (requires user authentication)
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
            return jsonify({'error': 'Internal Server Error'}), 500

# Get all rides for the authenticated user
# this myRides should be check_session, it runs when the app starts and sends the user, with an attribute of rides: and nested bookings inside the rides
class MyRides(Resource):
    def get(self):
        user_id = check_session()
        
        rides = Ride.query.filter_by(user_id=user_id).all()
        return jsonify([ride.to_dict() for ride in rides])

# Update a ride (requires user authentication)
class Update_Ride(Resource):
    def put(self, ride_id):
        data = request.json
        user_id = session.get('user_id')
        if not user_id:
            return {"error": "Unauthorized"}, 401
        
        ride = Ride.query.get(ride_id)
        if not ride:
            return {"error": "Ride not found"}, 404
        
        ride.name = data.get('name', ride.name)
        ride.pickup_time = parser.isoparse(data.get('pickupTime', ride.pickup_time.isoformat()))
        ride.spaces = data.get('spaces', ride.spaces)
        ride.destination = data.get('destination', ride.destination)
        ride.duration = data.get('duration', ride.duration)
        ride.mileage = data.get('mileage', ride.mileage)

        db.session.commit()

        return {"message": "Ride updated successfully"}, 200

# Delete a ride (requires user authentication)
class Delete_Ride(Resource):
    def delete(self, ride_id):
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

class MyBooking(Resource):
    # GET all bookings
    def get(self):
        print("GET /api/bookings called")
        user_id = session.get('user_id')
        print(f"User ID from session: {user_id}")
        if not user_id:
            return {"error": "Unauthorized"}, 401

        try:
            print(f"Booking model: {Booking}")
            bookings = Booking.query.filter_by(user_id=user_id).all()
            print(f"Bookings found: {bookings}")
            return jsonify([booking.to_dict() for booking in bookings])
        except Exception as e:
            print(f"Error querying bookings: {e}")
            return {"error": "Internal Server Error"}, 500

    # CREATE a new booking
    def post(self):
        data = request.get_json()
        ride_id = data.get('ride_id')
        user_id = data.get('user_id')
        status = data.get('status', 'Pending')

        # Check for required fields
        if not ride_id or not user_id:
            return {'message': 'ride_id and user_id are required'}, 400

        # Check if the ride and user exist
        ride = Ride.query.get(ride_id)
        user = User.query.get(user_id)

        if not ride:
            return {'message': 'Ride not found'}, 404

        if not user:
            return {'message': 'User not found'}, 404

        # Create the booking
        booking = Booking(ride_id=ride.id, user_id=user.id, status=status)
        db.session.add(booking)
        db.session.commit()

        return {'message': 'Booking created successfully', 'booking': booking.to_dict()}, 201

class BookingById(Resource):
    # GET a specific booking by ID
    def get(self, booking_id):
        booking = Booking.query.get(booking_id)
        if not booking:
            return {"error": "Booking not found"}, 404
        return jsonify(booking.to_dict())

    # PUT (Update) a booking
    def put(self, booking_id):
        booking = Booking.query.get(booking_id)
        if not booking:
            return {"error": "Booking not found"}, 404

        data = request.get_json()

        # Update booking status if provided
        status = data.get('status')
        if status:
            booking.status = status

        # Optionally, update other fields like feedback
        feedback = data.get('feedback')
        if feedback:
            booking.feedback = feedback

        db.session.commit()

        return jsonify(booking.to_dict()), 200

    # DELETE a booking
    def delete(self, booking_id):
        booking = Booking.query.get(booking_id)
        if not booking:
            return {"error": "Booking not found"}, 404

        db.session.delete(booking)
        db.session.commit()

        return {"message": "Booking deleted successfully"}, 200


# API Endpoints
api.add_resource(CheckSession, '/api/check_session')
api.add_resource(Register, '/api/register')
api.add_resource(Login, '/api/login')
api.add_resource(Logout, '/api/logout')
api.add_resource(Submit_Ride, '/api/rides')
api.add_resource(Get_Rides, '/api/rides')
api.add_resource(MyRides, '/api/my_rides')
api.add_resource(Update_Ride, '/api/rides/<int:ride_id>')
api.add_resource(Delete_Ride, '/api/rides/<int:ride_id>/delete')
api.add_resource(MyBooking, '/api/bookings')
api.add_resource(BookingById, '/api/bookings/<int:booking_id>')



if __name__ == '__main__':
    app.run(port=5555, debug=True)