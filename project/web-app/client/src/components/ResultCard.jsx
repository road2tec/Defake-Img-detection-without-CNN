import React from 'react';
import { motion } from 'framer-motion';

const ResultCard = ({ result, imagePreview, onReset }) => {
    const isReal = result.label === 'REAL';

    return (
        <motion.div
            initial={{ opacity: 0, scale: 0.95 }}
            animate={{ opacity: 1, scale: 1 }}
            className="card"
            style={{ width: '100%', maxWidth: '480px', textAlign: 'center' }}
        >
            <div style={{ marginBottom: '1.5rem', position: 'relative' }}>
                <img
                    src={imagePreview}
                    alt="Analyzed Face"
                    style={{
                        width: '160px',
                        height: '160px',
                        borderRadius: '50%',
                        objectFit: 'cover',
                        border: '4px solid rgba(255, 255, 255, 0.1)',
                        boxShadow: '0 10px 30px rgba(0,0,0,0.5)',
                        margin: '0 auto',
                        display: 'block'
                    }}
                />
            </div>

            <h2 style={{ fontSize: '1.5rem', fontWeight: '700', marginBottom: '0.5rem', color: 'white' }}>Analysis Complete</h2>

            <div style={{ display: 'flex', justifyContent: 'center', gap: '1rem', marginBottom: '2rem' }}>
                <span className={`badge ${isReal ? 'badge-real' : 'badge-fake'}`} style={{ fontSize: '1rem', padding: '0.5rem 1.5rem' }}>
                    {result.label}
                </span>
            </div>

            <div style={{ background: 'rgba(0,0,0,0.2)', borderRadius: '12px', padding: '1.5rem', marginBottom: '2rem', border: '1px solid var(--glass-border)' }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '0.75rem', fontSize: '0.9rem', fontWeight: '500', color: 'var(--text-muted)' }}>
                    <span>Confidence Score</span>
                    <span style={{ fontFamily: 'monospace', color: 'white' }}>{(result.confidence * 100).toFixed(2)}%</span>
                </div>
                <div style={{ width: '100%', background: 'rgba(255,255,255,0.1)', borderRadius: '999px', height: '12px', overflow: 'hidden', marginBottom: '1.5rem' }}>
                    <motion.div
                        initial={{ width: 0 }}
                        animate={{ width: `${result.confidence * 100}%` }}
                        transition={{ duration: 0.8, ease: "easeOut" }}
                        style={{
                            height: '100%',
                            background: isReal ? '#34d399' : '#f87171',
                            boxShadow: isReal ? '0 0 10px 2px rgba(52, 211, 153, 0.3)' : '0 0 10px 2px rgba(248, 113, 113, 0.3)'
                        }}
                    ></motion.div>
                </div>

                {result.explanation && (
                    <div style={{ textAlign: 'left', borderTop: '1px solid var(--glass-border)', paddingTop: '1rem' }}>
                        <p style={{ fontSize: '0.85rem', color: 'var(--text-muted)', marginBottom: '0.25rem' }}>Analysis Insight:</p>
                        <p style={{ fontSize: '0.95rem', color: 'white', fontWeight: '500' }}>{result.explanation}</p>
                    </div>
                )}
            </div>

            <button onClick={onReset} className="primary" style={{ width: '100%' }}>
                Analyze Another Image
            </button>
        </motion.div>
    );
};

export default ResultCard;
