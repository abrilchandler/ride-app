import React, { useState } from 'react';

function RideForm() {
    const [name, setName] = useState('');
    const [pickupTime, setPickupTime] = useState('')
    const [spaces, setSpaces] = useState(0)
    const [destination, setDestination] = useState('')

    const handleSubmit = (e) => {
        e.preventDefault();

        const newRide = {
                name: name,
                pickupTime: new Date(pickupTime).toISOString(),
                spaces: parseInt(spaces, 10),
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
                throw new Error('Network response ws not ok')
            }
            return response.json();
        })
        .then(data => {
            console.log('Ride Created', data);
            setName('');
            setPickupTime('');
            setSpaces('');
            setDestination('');
        })
        .catch(error => {
            console.error('Error creating ride:', error);
        });
    }

    return (
        <div>
            <h1>Let's create a ride</h1>
            <section>
                <form onSubmit={handleSubmit} method='post'>
                    <div>
                        <label>
                            Ride Name:
                            <input
                                type='text'
                                value={name}
                                onChange={(e) => setName(e.target.value)}
                                required />
                        </label>
                    </div>
                    <div>
                        <label>
                            Pickup Time:
                            <input
                                type='datetime-local'
                                value={pickupTime}
                                onChange={(e) => setPickupTime(e.target.value)}
                                required />
                        </label>
                    <div>
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
                    <div>
                        <label>
                            Destination:
                            <input
                                type='number'
                                value={spaces}
                                onChange={(e) => setDestination(e.target.value)}
                                required />
                        </label>
                    </div>
                    <button type='submit'>Create Ride</button>
                    </div>
                </form>
            </section>
        </div>
    )
}

export default RideForm;