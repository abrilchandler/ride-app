#!/usr/bin/env python3

# Standard library imports
from random import randint, choice as rc

# Remote library imports
from faker import Faker

# Local imports
from app import app
from models import db, User, Ride, Horse

if __name__ == '__main__':
    fake = Faker()
    with app.app_context():

        Ride.query.delete()
        Horse.query.delete()
        User.query.delete()

        users = [User(username=fake.name()) for _ in range(10)]
        db.session.add.all(users)
        db.session.commit()

        rides = [
            Ride(
                name=fake.city(),
                pickup_time=fake.future_datetime(),
                spaces=randint(1, 5),
                user_id=rc(users).id
            ) for _ in range(20)
        ]
        db.session.add_all(rides)
        db.session.commit()

        horses = [
            Horse(
                name=fake.first_name(),
                age=randint(1, 15),
                weight=randint(800, 1400)
            ) for _ in range(50)
        ]
        db.session.add_all(horses)
        db.session.commit()
        
        print("Starting seed...")
        # Seed code goes here!
