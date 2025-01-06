from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy import Enum, Float, DateTime 
from config import db
# from werkzeug.security import generate_password_hash, check_password_hash

import enum

user_ride_table = db.Table('user_ride', 
    db.Column('user_id', db.Integer, db.ForeignKey('users.id'), primary_key=True),
    db.Column('ride_id', db.Integer, db.ForeignKey('rides.id'), primary_key=True),
    db.Column('status', db.String, nullable=False, default='pending'),  # Example user-submittable attribute

)
# Models go here!
class User(db.Model, SerializerMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)

    # Relationship to Rides (one-to-many, hauler)
    rides = db.relationship('Ride', back_populates='user')

    # Many-to-many relationship to Rides with a user-submittable 'status' attribute
    claimed_rides = db.relationship('Ride', secondary=user_ride_table, back_populates='claimers')

    def __repr__(self):
        return f'<User {self.id}, {self.username}>'
    
    
class Ride(db.Model):
    __tablename__ = 'rides'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    pickup_time = db.Column(db.DateTime, nullable=False)
    spaces = db.Column(db.Integer, nullable=False, default=1)
    destination = db.Column(db.String, nullable=False)
    duration = db.Column(db.Integer, nullable=False)
    mileage = db.Column(db.Integer, nullable=False)

    # Relationship to User (one-to-many)
    user = db.relationship('User', back_populates='rides')

    # Many-to-many relationship with User (with a status)
    claimers = db.relationship('User', secondary=user_ride_table, back_populates='claimed_rides')

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
    feedback = db.Column(db.String(500))  # User-submittable feedback

    ride = db.relationship('Ride')
    user = db.relationship('User')

    def __repr__(self):
        return f'<Booking {self.id}, Ride: {self.ride_id}, User: {self.user_id}, Status: {self.status.value}>'
