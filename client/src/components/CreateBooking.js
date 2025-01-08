import React, { useState } from 'react';
import { useHistory } from 'react-router-dom';
import { Formik, Field, Form } from 'formik';

function CreateBooking({ rideId, userId }) {
  const [status, setStatus] = useState("Pending");
  const history = useHistory();

  const handleSubmit = (values) => {
    fetch('/api/bookings', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        ride_id: rideId,
        user_id: userId,
        status: values.status,
      }),
    })
      .then((response) => response.json())
      .then((data) => {
        console.log('Booking created:', data);
        history.push('/my-bookings'); // Redirect after successful booking
      })
      .catch((error) => {
        console.error('Error creating booking:', error);
      });
  };

  return (
    <Formik
      initialValues={{ status }}
      onSubmit={handleSubmit}
    >
      <Form>
        <div>
          <Field as="select" name="status">
            <option value="Pending">Pending</option>
            <option value="Confirmed">Confirmed</option>
            <option value="Cancelled">Cancelled</option>
          </Field>
        </div>
        <button type="submit">Create Booking</button>
      </Form>
    </Formik>
  );
}

export default CreateBooking;