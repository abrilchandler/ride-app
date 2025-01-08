from config import app, db
from models import Booking

with app.app_context():
    try:
        bookings = Booking.query.all()
        print("Bookings fetched successfully:", bookings)
    except Exception as e:
        print("Error fetching bookings:", e)