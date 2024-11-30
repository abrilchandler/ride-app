import React, { useEffect, useState } from 'react';

function AvailableRides() {
    const [rides, setRides] = useState([]);

    useEffect(() => {
        fetchRides();
    }, []);

    const fetchRides = async () => {
        const response = await fetch('api/rides/');
        const data = await response.json();
        setRides(data);
    };

    return (
        <div>
            <h2>Available Rides</h2>
            <ul>
                {rides.map(ride => (
                    <li key={ride.id}>
                        {ride.name}: {ride.pickup_time} to {ride.destination} for {ride.duration}
                        {ride.mileage} miles
                    </li>
                ))}
            </ul>
        </div>
    )
    
}


export default AvailableRides;