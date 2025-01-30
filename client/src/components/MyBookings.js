import React, { useEffect, useState } from 'react';
import UpdateBooking from './UpdateBooking';  // Assuming you have an UpdateBooking component

function MyBookings() {
    const [bookings, setBookings] = useState([]);
    const [updatingBookingId, setUpdatingBookingId] = useState(null);
    const [loading, setLoading] = useState(true); // State to track loading
    const [error, setError] = useState(null); // State to handle errors

    useEffect(() => {
        fetchBookings();
    }, []);

    const fetchBookings = async () => {
        setLoading(true); // Start loading
        try {
            const response = await fetch('/api/bookings');
            if (!response.ok) {
                throw new Error('Failed to fetch bookings');
            }
            const data = await response.json();
            setBookings(data);
        } catch (error) {
            setError(error.message); // Set error message if fetch fails
        } finally {
            setLoading(false); // Stop loading
        }
    };

    const handleDelete = async (bookingId) => {
        if (window.confirm('Are you sure you want to cancel this booking?')) {
            try {
                const response = await fetch(`/api/bookings/${bookingId}`, {
                    method: 'DELETE',
                });
                if (response.ok) {
                    alert('Booking deleted successfully');
                    fetchBookings(); // Refresh the list after deletion
                } else {
                    alert('Failed to delete the booking');
                }
            } catch (error) {
                alert('Error deleting booking: ' + error.message);
            }
        }
    };

    const handleUpdate = (bookingId) => {
        setUpdatingBookingId(bookingId);
    };

    const handleCancelUpdate = () => {
        setUpdatingBookingId(null);
    };

    return (
        <div>
            <h1>My Bookings</h1>
            <h2>Bookings that you have made</h2>

            {loading && <p>Loading your bookings...</p>}
            {error && <p style={{ color: 'red' }}>{error}</p>}

            {!loading && !error && bookings.length === 0 && (
                <p>No bookings found.</p>
            )}

            <ul>
                {bookings.map((booking) => (
                    <li key={booking.id}>
                        Ride ID: {booking.ride_id} - Status: {booking.status}
                        <br />
                        <button onClick={() => handleUpdate(booking.id)}>Update Booking</button>
                        <br />
                        <button onClick={() => handleDelete(booking.id)}>Cancel Booking</button>
                        <br />
                    </li>
                ))}
            </ul>

            {updatingBookingId && (
                <UpdateBooking
                    bookingId={updatingBookingId}
                    onUpdate={fetchBookings} // Refresh bookings after update
                    onCancel={handleCancelUpdate}
                />
            )}
        </div>
    );
}

export default MyBookings;