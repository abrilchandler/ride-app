from sqlalchemy_serializer import SerializerMixin
from sqlalchemy import Enum, Float, DateTime 
from config import db

import enum
#nancy buckets = rides
#nancy items = bookings

# Models go here!
class User(db.Model, SerializerMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)

    rides = db.relationship('Ride', secondary='bookings', back_populates='users')
    
   # rides = db.relationship('Ride', back_populates='user')
# this is a direct relationship, but i need a through relationship
# my user has many items, and a bucket has many items, so a user has many buckets through items
    
    #rides  db.relationship('Ride, secondary='booking')
    # user has many bookings through rides?

    # user has many rides through booking
    # i should be able to get models by myself i think. I more so need what i just texteed you for the front end

    #my rides should be sent rides that i have booked using the button on available rides

    def __repr__(self):
        return f'<User {self.id}, {self.username}>'
    

class Ride(db.Model):
    __tablename__ = 'rides'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
   # user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    pickup_time = db.Column(db.DateTime, nullable=False)
    spaces = db.Column(db.Integer, nullable=False, default=1)
    destination = db.Column(db.String, nullable=False)
    duration = db.Column(db.Integer, nullable=False)
    mileage = db.Column(db.Integer, nullable=False)

    # Relationship to User (one-to-many)
    # user = db.relationship('User', back_populates='rides')
        # Many-to-many relationship through 'Booking' model
    users = db.relationship('User', secondary='bookings', back_populates='rides')


    def __repr__(self):
        return f'<Ride {self.id}, {self.name}>'

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'pickup_time': self.pickup_time.strftime('%Y-%m-%d %H:%M:%S'),
            'spaces': self.spaces,
            'destination': self.destination,
            'duration': self.duration,
            'mileage': self.mileage,
            'user_id': self.user_id 
        }
    

class BookingStatus(enum.Enum):
    PENDING = "Pending"
    CONFIRMED = "Confirmed"
    CANCELLED = "Cancelled"
    COMPLETED = "Completed"
    REJECTED = "Rejected"
    IN_PROGRESS = "In Progress"

class Booking(db.Model):
    __tablename__ = 'bookings'

    id = db.Column(db.Integer, primary_key=True)
    ride_id = db.Column(db.Integer, db.ForeignKey('rides.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    status = db.Column(Enum(BookingStatus), default=BookingStatus.PENDING)

    ride = db.relationship('Ride', back_populates='bookings')
    user = db.relationship('User', back_populates='bookings')

    def __repr__(self):
        return f'<Booking {self.id}, Ride: {self.ride_id}, User: {self.user_id}, Status: {self.status.value}>'

    def to_dict(self):
        return {
            'id': self.id,
            'ride_id': self.ride_id,
            'user_id': self.user_id,
            'status': self.status
        }