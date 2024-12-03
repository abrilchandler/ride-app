from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy import Enum, Float, DateTime 
from config import db
from werkzeug.security import generate_password_hash, check_password_hash

import enum

user_ride_table = db.Table('user_ride', 
    db.Column('user_id', db.Integer, db.ForeignKey('users.id'), primary_key=True),
    db.Column('ride_id', db.Integer, db.ForeignKey('rides.id'), primary_key=True)
)
# Models go here!
class User(db.Model, SerializerMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)

    # Relationship to Rides (on-to-many, hauler)
    rides = db.relationship('Ride', back_populates='user')

    # Relationship to Horses(one-to-many, owner)
    horses = db.relationship('Horse', back_populates='owner')

    claimed_rides = db.relationship('Ride', secondary=user_ride_table, back_populates='claimers')

 #   def set_password(self, password):
  #      self.password_hash = generate_password_hash(password)

  #  def check_password(self, password):
   #    return check_password_hash(self.password_hash, password)



    def __repr__(self):
        return f'<User {self.id}, {self.username}>'
    

class Ride(db.Model, SerializerMixin):
    __tablename__ = 'rides'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    pickup_time = db.Column(db.DateTime, nullable=False)
    spaces = db.Column(db.Integer, nullable=False, default=1)
    destination = db.Column(db.String, nullable=False)
    duration = db.Column(db.Integer, nullable=False)
    mileage = db.Column(db.Float, nullable=False)

    #Relationship to User(one-to-many)
    user = db.relationship('User', back_populates='rides')

    #Relationship to horses(many-to-many)
    horses = db.relationship('Horse', secondary='bookings', back_populates='rides', overlaps='users, rides')

    claimers = db.relationship('User', secondary=user_ride_table, back_populates='claimed_rides')

    def __repr__(self):
        return f'<Ride {self.id}, {self.name}>'
    

class Horse(db.Model, SerializerMixin):
    __tablename__ = 'horses'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    age = db.Column(db.Integer)
    weight = db.Column(db.Integer)
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    # Relationship to User (one-to-many)
    owner = db.relationship('User', back_populates='horses')

    # Relationship to Rides (many-to-many)
    rides = db.relationship('Ride', secondary='bookings', back_populates='horses', overlaps='rides,horses')

    def __repr__(self):
        return f'<Horse {self.name}, {self.age}, {self.weight}>'
    

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
    horse_id = db.Column(db.Integer, db.ForeignKey('horses.id'))
    status = db.Column(Enum(BookingStatus), default=BookingStatus.PENDING)

    horses = db.relationship('Horse', secondary='bookings', back_populates='rides')


    def __repr__(self):
        return f'<Booking {self.id}, Ride: {self.ride_id}. Horse: {self.horse_id}, Status: {self.status.value}>'
    