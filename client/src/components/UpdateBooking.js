import React, { useState, useEffect } from 'react';
import { useHistory, useParams } from 'react-router-dom';
import { Formik, Field, Form } from 'formik';

function UpdateBooking() {
  const { bookingId } = useParams();
  const history = useHistory();
  const [booking, setBooking] = useState(null);

  // Fetch booking details when component mounts
  useEffect(() => {
    fetch(`/api/bookings/${bookingId}`)
      .then((response) => response.json())
      .then((data) => setBooking(data))
      .catch((error) => console.error('Error fetching booking:', error));
  }, [bookingId]);

  if (!booking) {
    return <div>Loading...</div>;
  }

  const handleSubmit = (values) => {
    fetch(`/api/bookings/${bookingId}`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        status: values.status,
        feedback: values.feedback,  // Update feedback if provided
      }),
    })
      .then((response) => response.json())
      .then((data) => {
        console.log('Booking updated:', data);
        history.push('/my-bookings');  // Redirect to the booking list after updating
      })
      .catch((error) => {
        console.error('Error updating booking:', error);
      });
  };

  return (
    <div>
      <h2>Update Booking</h2>
      <Formik
        initialValues={{
          status: booking.status,
          feedback: booking.feedback || '',
        }}
        onSubmit={handleSubmit}
      >
        <Form>
          <div>
            <label htmlFor="status">Status</label>
            <Field as="select" name="status">
              <option value="Pending">Pending</option>
              <option value="Confirmed">Confirmed</option>
              <option value="Cancelled">Cancelled</option>
              <option value="Completed">Completed</option>
            </Field>
          </div>

          <div>
            <label htmlFor="feedback">Feedback</label>
            <Field
              as="textarea"
              name="feedback"
              placeholder="Leave your feedback here"
            />
          </div>

          <button type="submit">Update Booking</button>
        </Form>
      </Formik>
    </div>
  );
}

export default UpdateBooking;