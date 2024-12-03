import React, { useEffect, useState } from 'react';

function AvailableRides({userId}) {
    const [rides, setRides] = useState([]);

    useEffect(() => {
        fetchRides();
    }, []);

    const fetchRides = async () => {
        const response = await fetch('api/rides/');
        const data = await response.json();
        setRides(data);
    };

    const claimRide = async (rideId) => {
        try {
            const response = await fetch('/api/claim_ride', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ ride_id: rideId, user_id: userId }),
            });
            if (!response.ok) {
                throw new Error('Failed to claim ride');
            }
            const result = await response.json();
            console.log('Ride claimed successfully:', result);
        } catch (error) {
            console.error('Error claiming ride:', error);
        }
    };

    return (
        <div>
            <h2>Available Rides</h2>
            <ul>
                {rides.map(ride => (
                    <li key={ride.id}>
                        {ride.name}: {ride.pickup_time} to {ride.destination} for {ride.duration}
                        {ride.mileage} miles
                    <button onClick={() => claimRide(ride.id)}>Claim Ride</button>
                    </li>// in here you'll need some kind of button for claiming rides right? clicking it would send a request
                    // to the server with a ride id and a user id or something to make a claimedRide and then you could 
                    // make requests from that e
                ))}
            </ul>
        </div>
    )
    
}


export default AvailableRides;