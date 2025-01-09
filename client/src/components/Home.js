import React, { useEffect, useState } from "react";
import CreateBooking from './CreateBooking';  // Assuming CreateBooking component
import { useHistory } from "react-router-dom";

function Home({ user }) {
  const [rides, setRides] = useState([]);
  const [selectedRide, setSelectedRide] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchRides();
  }, []);

  const fetchRides = async () => {
    setLoading(true);
    try {
      const response = await fetch("/api/rides");
      if (!response.ok) {
        throw new Error('Failed to fetch rides');
      }
      const data = await response.json();
      setRides(data);
    } catch (error) {
      setError(error.message);
    } finally {
      setLoading(false);
    }
  };

  const handleBookRide = (rideId) => {
    const userId = user.id;  // Assuming user is already logged in
  
    if (!userId) {
      console.log("User is not logged in");
      return;
    }
  
    const payload = {
      ride_id: rideId,  // Ride ID
      user_id: userId   // User ID (ensure this is available and valid)
    };
  
    fetch('/api/bookings', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(payload),
    })
    .then(response => {
      if (response.ok) {
        return response.json();
      } else {
        throw new Error('Failed to book ride');
      }
    })
    .then(data => {
      console.log('Ride booked successfully:', data);
      // Optionally update the UI
    })
    .catch(error => {
      console.error('Error booking ride:', error);
    });
  };
  console.log(user, "user") // check to make sure this is present
  console.log(rides) // make sure each ride has an id and it can be accessed by ride.id
  return (
    <div>
      <h1>Available Rides</h1>

      {/* Show loading or error message */}
      {loading && <p>Loading rides...</p>}
      {error && <p style={{ color: 'red' }}>{error}</p>}

      <ul>
        {rides.map((ride) => (
          <li key={ride.id}>
            <h3>{ride.name}</h3>
            <p>Destination: {ride.destination}</p>
            <p>Spaces Left: {ride.spaces}</p>

            {/* Button to book the ride */}
            <button onClick={() => handleBookRide(ride.id)}>
              Book this Ride
            </button>
          </li>
        ))}
      </ul>

      {/* Conditionally render CreateBooking if a ride is selected */}
      {selectedRide && user && (
        <CreateBooking rideId={selectedRide} userId={user.id} />
      )}
    </div>
  );
}

export default Home;