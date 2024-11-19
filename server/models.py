from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.ext.associationproxy import association_proxy

from config import db



# Models go here!
class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)

    # Relationship to Rides (on-to-many, hauler)
    rides = db.relationship('Ride', back_populates='user')

    # Relationship to Horses(one-to-many, owner)
    horses = db.relationship('Horse', back_populates='owner')

    def __repr__(self):
        return f'<User {self.id}, {self.username}>'
    

class Ride(db.Model):
    __tablename__ = 'rides'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    pickup_time = db.Column(DateTime, nullable=False)
    spaces = db.Column(db.Integer)
    destination = db.Column(db.String)

    #Relationship to User(one-to-many)
    user = db.relationship('User', back_populates='rides')

    #Relationship to horses(many-to-many)
    horses = db.relationship('Horse', secondary='bookings', back_populates='rides')

    def __repr__(self):
        return f'<Ride {self.id}, {self.name}>'
    

class Horse(db.Model):
    __tablename__ = 'horses'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    age = db.Column(db.Integer)
    weight = db.Column(db.Integer)
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    # Relationship to User (one-to-many)
    owner = db.relationship('User', back_populates='horses')

    # Relationship to Rides (many-to-many)
    rides = db.relationship('Ride', secondary='bookings', back_populates='horses')

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
    horse_id = db.Column(db.Integer, db.ForeignKey('horses.id '))
    status = db.Column(Enum(BookingStatus), default=BookingStatus.PENDING)

    ride = db.relationship('Ride')
    horse = db.relationship('Horse')

    def __repr__(self):
        return f'<Booking {self.id}, Ride: {self.ride_id}. Horse: {self.horse_id}, Status: {self.status.value}>'
    