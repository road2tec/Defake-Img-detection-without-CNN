import React, { useEffect, useState, useContext } from 'react';
import axios from 'axios';
import { AuthContext } from '../context/AuthContext';
import { motion } from 'framer-motion';

const History = () => {
    const [history, setHistory] = useState([]);
    const { user } = useContext(AuthContext);

    useEffect(() => {
        const fetchHistory = async () => {
            try {
                if (user) {
                    const res = await axios.get(`http://localhost:5000/api/history?userId=${user.id}`);
                    setHistory(res.data);
                }
            } catch (err) {
                console.error(err);
            }
        };
        fetchHistory();
    }, [user]);

    return (
        <div style={{ maxWidth: '900px', margin: '3rem auto', padding: '0 2rem' }}>
            <motion.h2
                initial={{ opacity: 0, x: -10 }}
                animate={{ opacity: 1, x: 0 }}
                style={{ marginBottom: '2rem' }}
            >
                Your Prediction History
            </motion.h2>

            <div className="card" style={{ padding: '0', overflow: 'hidden' }}>
                <table className="history-table">
                    <thead>
                        <tr style={{ backgroundColor: '#f8fafc' }}>
                            <th style={{ paddingLeft: '2rem' }}>Date</th>
                            <th>Image</th>
                            <th>Result</th>
                            <th>Confidence</th>
                        </tr>
                    </thead>
                    <tbody>
                        {history.map(item => (
                            <tr key={item._id}>
                                <td style={{ paddingLeft: '2rem' }}>{new Date(item.timestamp).toLocaleDateString()}</td>
                                <td>{item.imageName}</td>
                                <td>
                                    <span className={`badge ${item.predictionLabel === 'REAL' ? 'badge-real' : 'badge-fake'}`}>
                                        {item.predictionLabel}
                                    </span>
                                </td>
                                <td style={{ fontFamily: 'monospace' }}>{(item.confidence * 100).toFixed(2)}%</td>
                            </tr>
                        ))}
                    </tbody>
                </table>
                {history.length === 0 && <p style={{ textAlign: 'center', padding: '3rem', color: '#94a3b8' }}>No history found.</p>}
            </div>
        </div>
    );
};

export default History;
