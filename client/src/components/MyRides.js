import React, { useState, useEffect } from "react";

function MyRides({ user }) {
  const [bookedRides, setBookedRides] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    console.log("useEffect triggered");
    if (user) {
      console.log("User is logged in, fetching booked rides...");
      fetchBookedRides();
    } else {
      console.log("No user found, skipping fetch.");
    }
  }, [user, fetchBookedRides]);

  const fetchBookedRides = async () => {
    console.log("Starting fetchBookedRides...");

    if (!user) {
      alert("You must be logged in to see your booked rides.");
      console.log("User not logged in, fetch aborted.");
      return;
    }

    setLoading(true);
    console.log("Setting loading state to true.");

    try {
      console.log("Sending fetch request to /api/my_rides");
      const response = await fetch("/api/my_rides");

      if (!response.ok) {
        console.error("Failed to fetch, status:", response.status);
        throw new Error("Failed to fetch booked rides");
      }

      const data = await response.json();
      console.log("Data received from API:", data);

      setBookedRides(data);
      console.log("Booked rides state updated:", data);
    } catch (error) {
      console.error("Error while fetching booked rides:", error);
      setError(error.message);
    } finally {
      setLoading(false);
      console.log("Loading state set to false.");
    }
  };

  return (
    <div>
      <h1>My Booked Rides</h1>

      {loading && <p>Loading your rides...</p>}
      {error && <p style={{ color: "red" }}>{error}</p>}

      <ul>
        {bookedRides.length === 0 && !loading && <p>You have not booked any rides yet.</p>}

        {bookedRides.map((ride) => (
          <li key={ride.id}>
            <h3>{ride.name}</h3>
            <p>Destination: {ride.destination}</p>
            <p>Pickup Time: {ride.pickup_time}</p>
            <p>Status: {ride.status}</p>
          </li>
        ))}
      </ul>
    </div>
  );
}

export default MyRides;