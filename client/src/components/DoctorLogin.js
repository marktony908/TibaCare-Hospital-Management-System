import { Link, useNavigate } from "react-router-dom";
import React, { useState, useEffect } from "react";
import { useFormik } from "formik";
import * as yup from 'yup';
import Navbar from "./Navbar";
import { useAuth } from './AuthContext'; 

function DoctorLogin() {
    const [loading, setLoading] = useState(false);
    const [message, setMessage] = useState('');
    const navigate = useNavigate();
    const { setUser } = useAuth(); 

    const loginSchema = yup.object().shape({
        email: yup.string().email("Invalid email format").required('Email is required'),
        password: yup.string().required('Password is required') 
    });

    const formik = useFormik({
        initialValues: {
            email: "",
            password: "",
        },
        validationSchema: loginSchema,
        onSubmit: async (values) => {
            setLoading(true); // Start loading
            try {
                const response = await fetch(`/api/doctorlogin`, {
                    method: "POST",
                    credentials: 'include',
                    headers: {
                        "Content-Type": "application/json"
                    },
                    body: JSON.stringify(values)
                });
                
                const data = await response.json();
                if (response.ok) {
                    setUser(data); // Set user in context
                    navigate("/");
                    setMessage("Login Successful");
                } else {
                    setMessage(data.error || "Invalid username or password"); // Handle specific error from backend
                }
            } catch (error) {
                setMessage("An error occurred during login");
            } finally {
                setLoading(false); // Stop loading
            }
        },
    });

    useEffect(() => {
        if (message) {
            const timer = setTimeout(() => setMessage(''), 5000);
            return () => clearTimeout(timer);
        }
    }, [message]);

    return (
        <>
            <Navbar />
            <div className="login-cont">
                <div className="login">
                    <h1>Login as a Doctor</h1>
                    <form onSubmit={formik.handleSubmit}>
                        <input
                            type="text"
                            placeholder="Email"
                            name="email"
                            value={formik.values.email}
                            onChange={formik.handleChange}
                            onBlur={formik.handleBlur}
                            className={formik.errors.email && formik.touched.email ? "inputError" : ""}
                        />
                        {formik.errors.email && formik.touched.email && <p className="errors">{formik.errors.email}</p>}

                        <input
                            type="password"
                            placeholder="Password"
                            name="password"
                            value={formik.values.password}
                            onChange={formik.handleChange}
                            onBlur={formik.handleBlur}
                            className={formik.errors.password && formik.touched.password ? "inputError" : ""}
                        />
                        {formik.errors.password && formik.touched.password && <p className="errors">{formik.errors.password}</p>}

                        <button type="submit" disabled={loading}>
                            {loading ? 'Logging in...' : 'Login'}
                        </button>
                    </form>

                    {message && <p className="responseMessage">{message}</p>}

                    <p>
                        Don't have an account? <Link to="/signup">Sign Up</Link>
                    </p>
                </div>
            </div>
        </>
    );
}

export default DoctorLogin;
