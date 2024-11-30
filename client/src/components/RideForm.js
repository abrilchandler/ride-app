import React, { useState } from 'react';

function RideForm() {
    const [name, setName] = useState('');
    const [pickupTime, setPickupTime] = useState('')
    const [spaces, setSpaces] = useState(0)
    const [destination, setDestination] = useState('')
    const [duration, setDuration] = useState(0)
    const [mileage, setMileage] = useState(0)


    const handleSubmit = (e) => {
        e.preventDefault();

        const newRide = {
                name: name,
                pickupTime: new Date(pickupTime).toISOString(),
                spaces: parseInt(spaces, 10),
                destination: destination,
                duration: parseInt(duration, 16)
        };

        fetch('/api/rides', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(newRide),
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok')
            }
            return response.json();
        })
        .then(data => {
            console.log('Ride Created', data);
            
        })
        .catch(error => {
            console.error('Error creating ride:', error);
        });
        setName('');
        setPickupTime('');
        setSpaces(0);
        setDestination('');
        setDuration(0);
        setMileage(0);
    }

    return (
        <div>
            <h1>Let's create a ride</h1>
            <section>
                <form onSubmit={handleSubmit} method='post'>
                    <div class='container-one'>
                        <label>
                            Ride Name:
                            <input
                                type='text'
                                value={name}
                                onChange={(e) => setName(e.target.value)}
                                required />
                        </label>
                    </div>
                    <div class='container-two'>
                        <label>
                            Pickup Time:
                            <input
                                type='datetime-local'
                                value={pickupTime}
                                onChange={(e) => setPickupTime(e.target.value)}
                                required />
                        </label>
                    </div>
                    <div class='container-three'>
                        <label>
                            Available Spaces:
                            <input
                                type='number'
                                value={spaces}
                                onChange={(e) => setSpaces(e.target.value)}
                                required
                                min='1' />
                        </label>
                    </div>
                    <div class='container-four'>
                        <label>
                            Destination:
                            <input
                                type='text'
                                value={destination}
                                onChange={(e) => setDestination(e.target.value)}
                                required />
                        </label>
                    </div>
                    <div class='container-five'>
                        <label>
                            Duration:
                            <input
                                type="number" max="16"
                                value={duration}
                                onChange={(e) => setDuration(e.target.value)}
                                required />
                        </label>
                    </div>
                    <div class='container-six'> 
                        <label>
                            Miles Covered:
                            <input
                                type='number'
                                value={mileage}
                                onChange={(e) => setMileage(e.target.value)}
                                required />
                        </label>
                    </div>
                    
                    <button type='submit'
                    value='Submit' onSubmit={handleSubmit}>Create Ride</button>
                </form>
            </section>
        </div>
    )
}

export default RideForm;