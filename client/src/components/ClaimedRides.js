import React, { useState, useEffect } from 'react';

function ClaimedRides() {
    const [claimedRides, setClaimedRides] = useState([]);

    useEffect(() => {
        fetchClaimedRides();
    },[]);

    const fetchClaimedRides = async () => {
        const response = await fetch('/api/claimed_rides');
        const data = await response.json();
        setClaimedRides(data);
    };

    return (
        <div>
            <h1>Claimed Rides</h1>
            <ul>
                {claimedRides.map((ride) => (
                    <li key={ride.id}>
                        {ride.name} - {ride.destination} ({ride.status})
                    </li>
                ))}
            </ul>
        </div>
    );
}

export default ClaimedRides;