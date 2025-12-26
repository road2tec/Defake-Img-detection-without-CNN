import React, { useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';

const Register = () => {
    const [formData, setFormData] = useState({ username: '', password: '' });
    const [error, setError] = useState('');
    const navigate = useNavigate();

    const onChange = e => setFormData({ ...formData, [e.target.name]: e.target.value });

    const onSubmit = async e => {
        e.preventDefault();
        try {
            await axios.post('http://localhost:5000/api/auth/register', formData);
            navigate('/login');
        } catch (err) {
            setError(err.response?.data?.msg || 'Registration failed');
        }
    };

    return (
        <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="card"
            style={{ maxWidth: '400px', margin: '4rem auto' }}
        >
            <h2 className="mb-4 text-center text-gradient">Create Account</h2>
            {error && <p className="mb-4 text-center" style={{ color: '#ef4444' }}>{error}</p>}
            <form onSubmit={onSubmit}>
                <div className="mb-4">
                    <label style={{ display: 'block', marginBottom: '0.5rem', fontWeight: '500', fontSize: '0.9rem' }}>Username</label>
                    <input
                        type="text"
                        name="username"
                        value={formData.username}
                        onChange={onChange}
                        required
                    />
                </div>
                <div className="mb-6">
                    <label style={{ display: 'block', marginBottom: '0.5rem', fontWeight: '500', fontSize: '0.9rem' }}>Password</label>
                    <input
                        type="password"
                        name="password"
                        placeholder="Min 6 characters"
                        value={formData.password}
                        onChange={onChange}
                        required
                    />
                </div>
                <button type="submit" className="primary" style={{ width: '100%' }}>Register</button>
            </form>
            <p className="mt-4 text-center text-sm">
                Already have an account? <a href="/login">Login</a>
            </p>
        </motion.div>
    );
};

export default Register;
