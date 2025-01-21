#!/usr/bin/env python3

# Standard library imports

# Remote library imports
from datetime import datetime
from dateutil import parser
from flask import request, jsonify, session
from flask_restful import Resource, Api
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

# Local imports
from config import app, db
from models import Ride, User, Booking, BookingStatus

# Flask-RESTful API setup
api = Api(app)

class CheckSession(Resource):
    def get(self):
        user_id = session.get('user_id')
        if user_id:
            # If user is logged in, return the user details as a JSON response
            user = User.query.get(user_id)  # Get user info from the database
            if user:
                user_data = user.to_dict()  # Return user details as JSON
              #  user['rides'] = []
                user_data['rides'] = []


                for ride in user.rides:
                    ride_data = ride.to_dict()
                    ride_data['bookings'] = []

                    for booking in ride.bookings:
                        ride_data['bookings'].append({
                            'id': booking.id,
                            'status': booking.status,
                            'user_id': booking.user_id
                        })
                    user_data['rides'].append(ride_data)

                return user_data, 200
        else:
            # If no user_id in session, return error response
            return {"error": "Not logged in"}, 401   
        
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

        # Check for authentication
        if not user_id:
            return {"error": "Unauthorized"}, 401

        try:
            # Parse the pickup time from the string and validate
            pickup_time_str = data.get('pickupTime')
            if not pickup_time_str:
                return jsonify({'error': 'pickupTime is required'}), 400

            try:
                pickup_time = parser.isoparse(pickup_time_str)
            except ValueError:
                return jsonify({'error': 'Invalid date format for pickupTime'}), 400

            # Create the new ride
            new_ride = Ride(
                name=data['name'],
                pickup_time=pickup_time,
                spaces=data['spaces'],
                destination=data['destination'],
                duration=data['duration'],
                mileage=data['mileage']
            )

            # Add the new ride to the session and commit to generate the ride id
            db.session.add(new_ride)
            db.session.commit()

            print(f"Ride {new_ride.id} created successfully")  # Log ride creation
            return {'message': 'Ride Created Successfully!'}, 201
        
        except SQLAlchemyError as e:
            db.session.rollback()  # Rollback if there's any issue with the transaction
            return jsonify({'error': str(e.orig)}), 500
        except ValueError as e:
            db.session.rollback()
            return jsonify({'error': 'Invalid data provided'}), 400
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': 'Internal Server Error'}), 500
# Get all rides for the authenticated user
# this myRides should be check_session, it runs when the app starts and sends the user, with an attribute of rides: and nested bookings inside the rides


# class MyRides(Resource):
#    def get(self):
 #       # Get the user ID from the session
  #      user_id = session.get('user_id')
      
   #     if not user_id:
    #        return {"error": "Unauthorized"}, 401
        
        # Get all the rides the user has booked (via Booking model)
     #   user = User.query.get(user_id)
        
        # If the user doesn't exist (which should not happen if user_id is valid)
      #  if not user:
       #     return {"error": "User not found"}, 404
        
       # print(user.rides.bookings, "USER rides")
        # Now we need to include bookings within the rides
        #booked_rides = []
        #for booking in user.bookings:
         #   ride = booking.ride  # Each booking has a corresponding ride
          #  booked_rides.append({
           #     "id": ride.id,
           #     "name": ride.name,
           #     "destination": ride.destination,
           #     "pickup_time": ride.pickup_time.strftime('%Y-%m-%d %H:%M:%S'),
           #     "status": booking.status.name  # Booking status (Pending, Confirmed, etc.)
           # })

        #return booked_rides


class UpdateBooking(Resource):
    def put(self, booking_id):
        # Fetch the booking from the database
        booking = Booking.query.get(booking_id)
        if not booking:
            return {"error": "Booking not found"}, 404

        # Get data from the request
        data = request.json

        # Update the booking status and optional feedback
        if 'status' in data:
            booking.status = data['status']
        
        if 'feedback' in data:
            booking.feedback = data['feedback']

        try:
            # Commit the changes to the database
            db.session.commit()

            return {"message": "Booking updated successfully"}, 200

        except SQLAlchemyError as e:
            db.session.rollback()  # Rollback in case of an error
            return {"error": str(e.orig)}, 500
        
# Delete a ride (requires user authentication)
class Delete_Booking(Resource):
    def delete(self, ride_id):
        print(ride_id)
        user_id = session.get('user_id')
        if not user_id:
            return {"error": "Unauthorized"}, 401
        
        ride = Ride.query.get(ride_id)
        if not ride:
            return {"Error": "Ride not found"}, 404
        
        # Check if the user has any booking for this ride
        booking = Booking.query.filter_by(ride_id=ride_id, user_id=user_id).first()
        if not booking:
            return {"error": "You can only delete rides you've created"}, 403
        
        # If the booking exists, we can proceed to delete the ride
        db.session.delete(ride)
        db.session.commit()


class MyBooking(Resource):
    # GET all bookings for the logged-in user
    def get(self):
        print("GET /api/bookings called")
        user_id = session.get('user_id')  # Get the user ID from session
        print(f"User ID from session: {user_id}")
        
        if not user_id:
            return {"error": "Unauthorized"}, 401  # User is not authenticated

        try:
            print(f"Querying bookings for user ID: {user_id}")
            bookings = Booking.query.filter_by(user_id=user_id).all()  # Get all bookings for the logged-in user
            print(f"Bookings found: {bookings}")
            return jsonify([booking.to_dict() for booking in bookings])  # Return the bookings as JSON
        except Exception as e:
            print(f"Error querying bookings: {e}")
            return {"error": "Internal Server Error"}, 500  # Handle any internal errors

    # POST to create a new booking
    def post(self):
        data = request.json  # Get data from the incoming request

        # Validate required fields
        ride_id = data.get('ride_id')
        if not ride_id:
            return {"error": "ride_id is required"}, 400  # Bad request if ride_id is missing

        user_id = session.get('user_id')  # Get user ID from session
        if not user_id:
            return {"error": "Unauthorized"}, 401  # Unauthorized if user is not logged in

        # Check if the ride exists in the database
        ride = Ride.query.get(ride_id)
        if not ride:
            return {"error": "Ride not found"}, 404  # Return 404 if ride doesn't exist

        try:
            # Create a new booking
            new_booking = Booking(
                ride_id=ride_id,
                user_id=user_id,
                status=BookingStatus.PENDING  # Or your default status
            )
            db.session.add(new_booking)  # Add the booking to the session
            db.session.commit()  # Commit the changes to the database

            return {"message": "Booking successful"}, 200  # Return success message
        except Exception as e:
            print(f"Error creating booking: {e}")
            db.session.rollback()  # Rollback the session in case of any error
            return {"error": "Internal Server Error"}, 500 
        

class BookingById(Resource):
    # GET a specific booking by ID
    def get(self, booking_id):
        booking = Booking.query.get(booking_id)
        if not booking:
            return {"error": "Booking not found"}, 404
        return booking.to_dict()

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
        print(booking_id)
        booking = Booking.query.get(booking_id)
        print(booking)
        print(booking_id)
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
#api.add_resource(MyRides, '/api/my_rides')
api.add_resource(UpdateBooking, '/api/bookings/<int:booking_id>')
api.add_resource(Delete_Booking, '/api/bookings/<int:ride_id>')
api.add_resource(MyBooking, '/api/bookings')
api.add_resource(BookingById, '/api/bookings/<int:booking_id>')



if __name__ == '__main__':
    app.run(port=5555, debug=True)