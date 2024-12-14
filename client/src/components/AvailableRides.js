import React, { useEffect, useState } from 'react';
import { useHistory } from 'react-router-dom';

function AvailableRides({userId}) {
    const [rides, setRides] = useState([]);
    const history = useHistory();

    useEffect(() => {
        fetchRides();
    }, []);

    const fetchRides = async () => {
        const response = await fetch('/api/available_rides');
        const data = await response.json();
        setRides(data);
    };

    const handleClaim = async (rideId) => {
        const username = 'username';
        const response = await fetch('/api/claim_ride', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json'},
            body: JSON.stringify({ride_id: rideId, username: username}),
        });
        const data = await response.json();

        if (response.ok) {
            history.pushState('/claimed_rides');
        } else {
            alert(data.error);
        }
    };

    return (
        <div>
            <h2>Available Rides</h2>
            <ul>
                {rides.map(ride => (
                    <li key={ride.id}>
                        {ride.name}: {ride.pickup_time} to {ride.destination} for {ride.duration} hours and {ride.mileage} miles |<br></br>| Spaces left: {ride.spaces} 
                    <button onClick={() => handleClaim(ride.id)}>Claim Ride</button>
                    <br></br>
                    <br></br>
                    </li>
                ))}
            </ul>
        </div>
    )
    
}


export default AvailableRides;