import React, { useState } from 'react';
import { useHistory } from 'react-router-dom';
import { Formik, Field, Form } from 'formik';

function CreateBooking({ rideId, userId }) {
  const [status, setStatus] = useState("Pending"); // Default status is 'Pending'
  const [message, setMessage] = useState(null); // To show booking success/failure message
  const history = useHistory();

  // Handle form submission
  const handleSubmit = async (values) => {
    try {
      // Make the API call to create a new booking
      const response = await fetch('/api/bookings', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          ride_id: rideId, // Ride being booked
          user_id: userId, // User booking the ride
          status: values.status, // Booking status from the form
        }),
      });

      // Check if the response is successful
      if (!response.ok) {
        throw new Error('Failed to create booking');
      }

      const data = await response.json();
      console.log('Booking created:', data);

      // Set success message and redirect
      setMessage('Booking created successfully!');
      history.push('/my-bookings'); // Redirect after successful booking
    } catch (error) {
      // Handle errors
      console.error('Error creating booking:', error);
      setMessage('Failed to create booking, please try again.');
    }
  };

  return (
    <div>
      <h2>Create Booking</h2>

      {/* Show success/failure message */}
      {message && <p>{message}</p>}

      <Formik
        initialValues={{ status }} // Initial status from the state
        onSubmit={handleSubmit} // Handle form submission
      >
        <Form>
          <div>
            <label htmlFor="status">Booking Status:</label>
            <Field as="select" name="status" id="status">
              <option value="Pending">Pending</option>
              <option value="Confirmed">Confirmed</option>
              <option value="Cancelled">Cancelled</option>
            </Field>
          </div>

          <div>
            <button type="submit">Create Booking</button>
          </div>
        </Form>
      </Formik>
    </div>
  );
}

export default CreateBooking;