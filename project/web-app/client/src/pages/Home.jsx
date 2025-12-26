import React, { useState, useContext } from 'react';
import axios from 'axios';
import { AuthContext } from '../context/AuthContext';
import ImageUpload from '../components/ImageUpload';
import ResultCard from '../components/ResultCard';
import Loader from '../components/Loader';
import { motion } from 'framer-motion';

function Home() {
    const [file, setFile] = useState(null);
    const [imagePreview, setImagePreview] = useState(null);
    const [result, setResult] = useState(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);
    const { user } = useContext(AuthContext);

    const handleImageUpload = async (uploadedFile, previewUrl) => {
        setFile(uploadedFile);
        setImagePreview(previewUrl);
        setLoading(true);
        setError(null);

        const formData = new FormData();
        formData.append('image', uploadedFile);
        if (user) {
            formData.append('userId', user.id);
        }

        try {
            // Call Backend API
            const response = await axios.post('http://localhost:5000/api/predict-image', formData, {
                headers: {
                    'Content-Type': 'multipart/form-data',
                },
            });

            setResult(response.data);
        } catch (err) {
            console.error(err);
            setError('Failed to analyze image. Please try again.');
            setFile(null);
            setImagePreview(null);
        } finally {
            setLoading(false);
        }
    };

    const handleReset = () => {
        setFile(null);
        setImagePreview(null);
        setResult(null);
        setError(null);
    };

    return (
        <div className="container-center">
            <motion.header
                initial={{ opacity: 0, y: -20 }}
                animate={{ opacity: 1, y: 0 }}
                className="text-center"
                style={{ marginBottom: '3rem' }}
            >
                <h1 className="text-gradient">TrueFace AI</h1>
                <p>Advanced ML analysis to detect AI-generated faces</p>
            </motion.header>

            <main style={{ width: '100%', maxWidth: '800px', display: 'flex', justifyContent: 'center' }}>
                {loading ? (
                    <div className="loader-container">
                        <Loader />
                    </div>
                ) : result ? (
                    <ResultCard
                        result={result}
                        imagePreview={imagePreview}
                        onReset={handleReset}
                    />
                ) : (
                    <motion.div
                        className="card"
                        style={{ width: '100%', maxWidth: '600px', display: 'flex', flexDirection: 'column', alignItems: 'center' }}
                        initial={{ opacity: 0, scale: 0.98 }}
                        animate={{ opacity: 1, scale: 1 }}
                    >
                        <ImageUpload onImageUpload={handleImageUpload} />
                        {error && (
                            <div style={{ marginTop: '1rem', padding: '1rem', background: 'rgba(239, 68, 68, 0.2)', color: '#fca5a5', borderRadius: '8px', border: '1px solid rgba(239, 68, 68, 0.3)' }}>
                                {error}
                            </div>
                        )}
                        {!user && (
                            <p style={{ marginTop: '1.5rem', fontSize: '0.9rem' }}>
                                <a href="/login">Login</a> to save your history.
                            </p>
                        )}
                    </motion.div>
                )}
            </main>

            <footer style={{ marginTop: '4rem', opacity: 0.6, fontSize: '0.9rem' }}>
                Powered by Hybrid XGBoost + Texture Analysis Engine
            </footer>
        </div>
    );
}

export default Home;
