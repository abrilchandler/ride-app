import React, { useState } from 'react';
import { useFormik } from 'formik';
import * as Yup from 'yup';


// pull your submitHandler out here. now you can put this on line 62 instead of having it all typed out down there
const submitHandler = (values) => {
    {
        const newRide = {
            ...values,
            pickupTime: new Date(values.pickupTime).toISOString(),
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
                throw new Error('Network response was not okay')
            }
            return response.json();
        })
        .then(data => {
            console.log('Ride Created', data);
        })
        .catch(error => {
            console.error('Error creating ride:', error);
        });
    }
}

// you could do the same with initial values but that's not as long so it matters less

function RideForm() {
    // you shouldn't need any of these anymore because formik handles it!

    // const [name, setName] = useState('');
    // const [pickupTime, setPickupTime] = useState('')
    // const [spaces, setSpaces] = useState(0)
    // const [destination, setDestination] = useState('')
    // const [duration, setDuration] = useState(0)
    // const [mileage, setMileage] = useState(0)

    const validationSchema = Yup.object({
        name: Yup.string().required("Ride name is required"),
        pickupTime: Yup.date().required('Pickup Time is required'),
        spaces: Yup.number().min(1, 'At least 1 space is required').required('Spaces are required'),
        destination: Yup.string().required('Destination is required'),
        duration: Yup.number().max(16, 'Duration cannot exceed 16 hours').required('Duration is required'),
        mileage: Yup.number().required('Miles covered is required'),
    });

    const formik = useFormik({
        initialValues: {
            name:'',
            pickupTime:'',
            spaces: 1, // since validation requires this to be min 1 let's set it to 1 instead of 0
            destination: '',
            duration: 0,
            mileage: 0,
        },
        validationSchema: validationSchema,
        onSubmit: (values) => {
            const newRide = {
                ...values,
                pickupTime: new Date(values.pickupTime).toISOString(),
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
                    throw new Error('Network response was not okay')
                }
                return response.json();
            })
            .then(data => {
                console.log('Ride Created', data);
            })
            .catch(error => {
                console.error('Error creating ride:', error);
            });
        },
    });
    // const handleSubmit = (e) => {
    //     e.preventDefault();

    //     const newRide = {
    //             name: name,
    //             pickupTime: new Date(pickupTime).toISOString(),
    //             spaces: parseInt(spaces, 10),
    //             destination: destination,
    //             duration: parseInt(duration, 16)
    //     };

    //     fetch('/api/rides', {
    //         method: 'POST',
    //         headers: {
    //             'Content-Type': 'application/json',
    //         },
    //         body: JSON.stringify(newRide),
    //     })
    //     .then(response => {
    //         if (!response.ok) {
    //             throw new Error('Network response was not ok')
    //         }
    //         return response.json();
    //     })
    //     .then(data => {
    //         console.log('Ride Created', data);
            
    //     })
    //     .catch(error => {
    //         console.error('Error creating ride:', error);
    //     });
    //     setName('');
    //     setPickupTime('');
    //     setSpaces(0);
    //     setDestination('');
    //     setDuration(0);
    //     setMileage(0);
    // }

    return (
        <div>
            <h1>Let's create a ride</h1>
            <section>
                <form onSubmit={formik.handleSubmit} method='post'>
                    <div className='container-one'>
                        <label>
                            Ride Name:
                            <input
                                type='text'
                                name='name'
                                value={formik.values.name}
                                onChange={formik.handleChange}
                                onBlur={formik.handleBlur}
                                required />
                            {formik.touched.name && formik.errors.name ? <div>{formik.errors.name}</div> : null}
                        </label>
                    </div>
                    <div className='container-two'>
                        <label>
                            Pickup Time:
                            <input
                                type='datetime-local'
                                name='pickupTime'
                                value={formik.values.pickupTime}
                                onChange={formik.handleChange}
                                onBlur={formik.handleBlur}
                                required />
                            {formik.touched.pickupTime && formik.errors.pickupTime ? <div>{formik.errors.pickupTime}</div> : null}
                        </label>
                    </div>
                    <div className='container-three'>
                        <label>
                            Available Spaces:
                            <input
                                type='number'
                                name='spaces'
                                value={formik.values.spaces}
                                onChange={formik.handleChange}
                                onBlur={formik.handleBlur}
                                required
                                min='1' />
                            {formik.touched.spaces && formik.errors.spaces ? <div>{formik.errors.spaces}</div> : null}
                        </label>
                    </div>
                    <div className='container-four'>
                        <label>
                            Destination:
                            <input
                                type='text'
                                name='destination'
                                value={formik.values.destination}
                                onChange={formik.handleChange}
                                onBlur={formik.handleBlur}
                                required />
                            {formik.touched.destination && formik.errors.destination ? <div>{formik.errors.destination}</div> : null}
                        </label>
                    </div>
                    <div className='container-five'>
                        <label>
                            Duration:
                            <input
                                type="number" max="16"
                                name='duration'
                                value={formik.values.duration}
                                onChange={formik.handleChange}
                                onBlur={formik.handleBlur}
                                required />
                            {formik.touched.duration && formik.errors.duration ? <div>{formik.errors.duration}</div> : null}
                        </label>
                    </div>
                    <div className='container-six'> 
                        <label>
                            Miles Covered:
                            <input
                                type='number'
                                name='mileage'
                                value={formik.values.mileage}
                                onChange={formik.handleChange}
                                onBlur={formik.handleBlur}
                                required />
                            {formik.touched.mileage && formik.errors.mileage ? <div>{formik.errors.mileage}</div> : null}
                        </label>
                    </div>
                    
                    <button type='submit'
                    value='Submit'>Create Ride</button>
                </form>
            </section>
        </div>
    )
}

export default RideForm;