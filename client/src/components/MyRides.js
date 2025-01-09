import React, { useEffect, useState } from 'react';
import UpdateBooking from './UpdateBooking';

function MyRides() {
    const [rides, setRides] = useState([]);
    const [updatingRideId, setUpdatingRideId] = useState(null);    
    
    useEffect(() => {
        fetchRides();
    }, []);

    const fetchRides = async () => {
        const response = await fetch('/api/my_rides');
        const data = await response.json();
        setRides(data);
    };
    const handleDelete = async (rideId) => {
        const response = await fetch(`/api/rides/${rideId}/delete`, {
            method: 'DELETE',
        });
        if (response.ok) {
            alert("Ride deleted successfully");
            fetchRides();
        } else {
            alert("Failed to delete the ride");
        }
    };

    const handleUpdate = (rideId) => {
        setUpdatingRideId(rideId);
    }
    const handleCancelUpdate = () => {
        setUpdatingRideId(null);
    };

    return (
        <div>
            <h1>My Rides</h1>
            <h2>Rides that you have created</h2>
            <ul>
                {rides.map(ride => (
                    <li key={ride.id}>
                        {ride.name}: {ride.pickup_time} to {ride.destination} for {ride.duration} hours: {ride.mileage} miles || Spaces left: {ride.spaces}
                        <br></br>
                        <button onClick={() => handleUpdate(ride.id)}>Update any changes</button>
                        <br></br>
                        <button onClick={() => handleDelete(ride.id)}>Delete Ride</button>
                        <br></br>
                        <br></br>
                    </li>
                ))}
            </ul>
            {updatingRideId && (
                <UpdateBooking
                    rideId={updatingRideId}
                    onUpdate={fetchRides}
                    onCancel={handleCancelUpdate}
                />
            )}
        </div>
    )
}

export default MyRides;