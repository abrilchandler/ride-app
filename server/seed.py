#!/usr/bin/env python3

# Standard library imports
from random import randint, choice as rc

# Remote library imports
from faker import Faker

# Local imports
from app import app
from models import db

if __name__ == '__main__':
    fake = Faker()
    with app.app_context():

        fake = Faker()

        Ride.query.delete()
        Horse.query.delete()
        User.query.delete()
        print("Starting seed...")
        # Seed code goes here!
