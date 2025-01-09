import React, { useState, useEffect } from "react";
import { useHistory } from "react-router-dom";

function Home({ user }) {
  const [rides, setRides] = useState([]);
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
        throw new Error("Failed to fetch rides");
      }
      const data = await response.json();
      setRides(data);
    } catch (error) {
      setError(error.message);
    } finally {
      setLoading(false);
    }
  };

  const handleBookRide = async (rideId) => {
    if (!user) {
      alert("You must be logged in to book a ride!");
      return;
    }

    const payload = {
      ride_id: rideId,
      user_id: user.id,
    };

    try {
      const response = await fetch("/api/bookings", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(payload),
      });

      if (!response.ok) {
        throw new Error("Failed to book ride");
      }

      const data = await response.json();
      console.log("Ride booked successfully:", data);

      // Optionally, you can refresh the "My Rides" section here or just reload the page.
      // You can also trigger the fetch for the user's booked rides from MyRides.js directly.

    } catch (error) {
      console.error("Error booking ride:", error);
    }
  };

  return (
    <div>
      <h1>Available Rides</h1>

      {loading && <p>Loading rides...</p>}
      {error && <p style={{ color: "red" }}>{error}</p>}

      <ul>
        {rides.map((ride) => (
          <li key={ride.id}>
            <h3>{ride.name}</h3>
            <p>Destination: {ride.destination}</p>
            <p>Spaces Left: {ride.spaces}</p>

            {/* Button to book the ride */}
            <button onClick={() => handleBookRide(ride.id)}>Book this Ride</button>
          </li>
        ))}
      </ul>
    </div>
  );
}

export default Home;