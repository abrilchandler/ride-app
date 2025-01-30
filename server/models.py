from sqlalchemy_serializer import SerializerMixin
from sqlalchemy import Enum, Float, DateTime 
from config import db

import enum
#nancy buckets = rides
#nancy items = bookings

# Models go here!
class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)

    rides = db.relationship('Ride', secondary='bookings', viewonly=True)
    

    def __repr__(self):
        return f'<User {self.id}, {self.username}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username
        }

class Ride(db.Model):
    __tablename__ = 'rides'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    pickup_time = db.Column(db.DateTime, nullable=False)
    spaces = db.Column(db.Integer, nullable=False, default=1)
    destination = db.Column(db.String, nullable=False)
    duration = db.Column(db.Integer, nullable=False)
    mileage = db.Column(db.Integer, nullable=False)

    bookings = db.relationship('Booking', backref='ride', lazy=True)


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
            'mileage': self.mileage
        }
    

class BookingStatus(enum.Enum):
    PENDING = "Pending"
    CONFIRMED = "Confirmed"
    CANCELLED = "Cancelled"
    COMPLETED = "Completed"
    REJECTED = "Rejected"
    IN_PROGRESS = "In Progress"
    
    def __str__(self):
        return self.value


class Booking(db.Model):
    __tablename__ = 'bookings'

    id = db.Column(db.Integer, primary_key=True)
    ride_id = db.Column(db.Integer, db.ForeignKey('rides.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    status = db.Column(Enum(BookingStatus), default=BookingStatus.PENDING)


    def __repr__(self):
        return f'<Booking {self.id}, Ride: {self.ride_id}, User: {self.user_id}, Status: {self.status.value}>'

    def to_dict(self):
        return {
            'id': self.id,
            'ride_id': self.ride_id,
            'user_id': self.user_id,
            'status': str(self.status)
        }