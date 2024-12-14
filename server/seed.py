#!/usr/bin/env python3

# Standard library imports
from random import randint, choice as rc, uniform

# Remote library imports
from faker import Faker

# Local imports
from app import app
from models import db, User, Ride, Horse, Booking, BookingStatus

if __name__ == '__main__':
    fake = Faker()
    with app.app_context():

        Ride.query.delete()
        Horse.query.delete()
        User.query.delete()
        Booking.query.delete()

        users = [
            User(username=fake.name()
            ) for _ in range(10)
        ]
        db.session.add_all(users)
        db.session.commit()

        rides = [
            Ride(
                name=fake.city(),
                user_id=rc(users).id,
                pickup_time=fake.future_datetime(),
                spaces=randint(1, 5),
                destination=fake.city(),
                duration=randint(1, 5),
                mileage=round(uniform(1.0, 100.0), 2)
            ) for _ in range(20)
        ]
        db.session.add_all(rides)
        db.session.commit()

        horses = [
            Horse(
                name=fake.first_name(),
                age=randint(1, 15),
                weight=randint(800, 1400),
                owner_id=rc(users).id
            ) for _ in range(50)
        ]
        db.session.add_all(horses)
        db.session.commit()

        bookings = [
            Booking(
                ride_id=rc(rides).id,
                horse_id=rc(horses).id,
                status=rc(list(BookingStatus))
            ) for _ in range(30)
        ]

        db.session.add_all(bookings)
        db.session.commit()

        print("Starting seed...")
        # Seed code goes here!
