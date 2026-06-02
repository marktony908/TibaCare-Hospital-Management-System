import React from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { useFormik } from 'formik';
import * as yup from 'yup';
import './BookAppointment.css';

const BookAppointment = () => {
    const { doctorId } = useParams(); // Get doctor ID from URL parameters
    const navigate = useNavigate(); // Initialize navigate function

    console.log("Doctor ID:", doctorId); // Debugging: Check if doctorId is retrieved correctly

    const validationSchema = yup.object().shape({
        date: yup.string().required('Date is required'),
        time: yup.string().required('Time is required'),
    });

    const formik = useFormik({
        initialValues: {
            date: '',
            time: '',
        },
        validationSchema,
        onSubmit: async (values, { resetForm }) => {
            console.log("Submitting form with values:", values); // Debugging: Log form values

            if (!doctorId) {
                alert("Error: Doctor ID is missing.");
                return;
            }

            // Include doctorId with the appointment data
            const appointmentData = { ...values, doctorId };

            try {
                const response = await fetch('http://localhost:3000/appointments', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(appointmentData), // Send form values as JSON
                });

                if (response.ok) {
                    alert('Appointment booked successfully!');
                    resetForm(); // Reset the form after successful submission
                    navigate(-1); // Optionally navigate back after successful form submission
                } else {
                    const errorData = await response.json();
                    console.error("Server Error Response:", errorData);
                    alert('Failed to book appointment. Please try again.');
                }
            } catch (error) {
                console.error("Network or Server Error:", error);
                alert('An error occurred while booking the appointment.');
            }
        },
    });

    return (
        <form onSubmit={formik.handleSubmit} className="appointment-form">
            <div className="form-field">
                <label htmlFor="date">Date:</label>
                <input
                    type="date"
                    id="date"
                    name="date"
                    onChange={formik.handleChange}
                    onBlur={formik.handleBlur}
                    value={formik.values.date}
                />
                {formik.touched.date && formik.errors.date && <p className="errors">{formik.errors.date}</p>}
            </div>

            <div className="form-field">
                <label htmlFor="time">Time:</label>
                <input
                    type="time"
                    id="time"
                    name="time"
                    onChange={formik.handleChange}
                    onBlur={formik.handleBlur}
                    value={formik.values.time}
                />
                {formik.touched.time && formik.errors.time && <p className="errors">{formik.errors.time}</p>}
            </div>

            <div className="form-buttons">
                <button type="submit" className="submit-button">Submit Appointment</button>
                <button
                    type="button"
                    className="back-button"
                    onClick={() => navigate(-1)} // Go back to the previous page
                >
                    Back
                </button>
            </div>
        </form>
    );
};

export default BookAppointment;
