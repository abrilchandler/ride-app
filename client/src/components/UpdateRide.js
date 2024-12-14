import React, { useState, useEffect } from 'react';

function UpdateRide({ rideId, onCancel }) {
    const [ride, setRide] = useState({
        name: '',
        pickupTime: '',
        spaces: 1,
        destination: '',
        duration: 0,
        mileage: 0,
    });
    const [loading, setLoading] = useState(true);
    const [formSubmitted, setFormSubmitted] = useState(false);



    useEffect(() => {
        const fetchRide = async () => {
            const response = await fetch(`/api/rides/${rideId}`);
            const data = await response.json();
            setRide({
                name: data.name,
                pickupTime: data.pickup_time,
                spaces: data.spaces,
                destination: data.destination,
                duration: data.duration,
                mileage: data.mileage,
            });
            setLoading(false)
        };

        if (rideId) fetchRide();
    }, [rideId]);

    const handleChange = (e) => {
        const { name, value } = e.target;
        setRide((prevRide) => ({
            ...prevRide,
            [name]: value,
        }));
    };
    
    const handleSubmit = async (e) => {
        e.preventDefault();

        const response = await fetch(`/api/rides/${rideId}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(ride),
        });
        if (response.ok) {
            alert('Ride updated successfully!');
            setFormSubmitted(true)
        } else {
            alert('Failed to update the ride');
        }
    };

    const handleCancel = () => {
        onCancel();
    }
    if (formSubmitted) {
        return (
            <div>
                <h2>Ride Updated successfully</h2>
            </div>
        );
    }
    if (loading) {
        return <p>Loading...</p>
    }

    return (
        <div>
        <h1>Update Ride</h1>
        <form onSubmit={handleSubmit}>
            <input
                type='text'
                name='name'
                value={ride.name}
                onChange={handleChange}
                placeholder="Ride Name"
            />
            <input 
                type="datetime-local"
                name="pickupTime"
                value={ride.pickupTime}
                onChange={handleChange}
            />
            <input 
                type='number'
                name="spaces"
                value={ride.spaces}
                onChange={handleChange}
                placeholder="Spaces"
            />
            <input 
                type='text'
                name='destination'
                value={ride.destination}
                onChange={handleChange}
                placeholder="Destination"
            />
            <input 
                type='number'
                name="duration"
                value={ride.duration}
                onChange={handleChange}
                placeholder='Duration'
            />
            <input 
                type="number"
                name='mileage'
                value={ride.mileage}
                onChange={handleChange}
                placeholder='Mileage'
            />
            <button type="submit" onClick={handleSubmit}>Save</button>
            <button type='button' onClick={handleCancel}>Cancel</button>
        </form>
        </div>
    );
}

export default UpdateRide;