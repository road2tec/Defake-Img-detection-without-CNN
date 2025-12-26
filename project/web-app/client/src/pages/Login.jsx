import React, { useState, useContext } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import { AuthContext } from '../context/AuthContext';
import { motion } from 'framer-motion';

const Login = () => {
    const [formData, setFormData] = useState({ username: '', password: '' });
    const [error, setError] = useState('');
    const { login } = useContext(AuthContext);
    const navigate = useNavigate();

    const onChange = e => setFormData({ ...formData, [e.target.name]: e.target.value });

    const onSubmit = async e => {
        e.preventDefault();
        try {
            const res = await axios.post('http://localhost:5000/api/auth/login', formData);
            login(res.data.token, res.data.user);
            navigate('/');
        } catch (err) {
            setError(err.response?.data?.msg || 'Login failed');
        }
    };

    return (
        <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="card"
            style={{ maxWidth: '400px', margin: '4rem auto' }}
        >
            <h2 className="mb-4 text-center text-gradient">Login</h2>
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
                        value={formData.password}
                        onChange={onChange}
                        required
                    />
                </div>
                <button type="submit" className="primary" style={{ width: '100%' }}>Sign In</button>
            </form>
            <p className="mt-4 text-center text-sm">
                Don't have an account? <a href="/register">Register</a>
            </p>
        </motion.div>
    );
};

export default Login;
