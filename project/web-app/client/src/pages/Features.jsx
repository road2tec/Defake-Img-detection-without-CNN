import React from 'react';
import { motion } from 'framer-motion';

const Features = () => {
    return (
        <div style={{ maxWidth: '1000px', margin: '4rem auto', padding: '0 2rem' }}>
            <motion.div
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
            >
                <h2 style={{ textAlign: 'center', marginBottom: '3rem', fontSize: '2.5rem' }} className="text-gradient">Core Features</h2>

                <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))', gap: '2rem' }}>
                    <div className="card">
                        <h3 style={{ color: 'var(--primary)', marginBottom: '1rem' }}>🚀 Advanced AI Model</h3>
                        <p>Powered by XGBoost and optimized feature extraction (HOG, LBP, Color Histograms) for 79%+ accuracy.</p>
                    </div>
                    <div className="card">
                        <h3 style={{ color: 'var(--primary)', marginBottom: '1rem' }}>⚡ Real-Time Analysis</h3>
                        <p>Instant feedback with our high-performance Python FastAPI microservice.</p>
                    </div>
                    <div className="card">
                        <h3 style={{ color: 'var(--primary)', marginBottom: '1rem' }}>🔒 Secure History</h3>
                        <p>Create an account to save and predict your analysis history securely in the cloud.</p>
                    </div>
                    <div className="card">
                        <h3 style={{ color: 'var(--primary)', marginBottom: '1rem' }}>🎨 Modern Design</h3>
                        <p>Experience a clean, professional interface designed for efficiency and clarity.</p>
                    </div>
                </div>
            </motion.div>
        </div>
    );
};

export default Features;
