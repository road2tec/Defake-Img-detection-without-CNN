const express = require('express');
const mongoose = require('mongoose');
const cors = require('cors');
const multer = require('multer');
const axios = require('axios');
const fs = require('fs');
const FormData = require('form-data');
require('dotenv').config();

const Prediction = require('./models/Prediction');
const authRouter = require('./routes/auth');

const app = express();
const PORT = process.env.PORT || 5000;

// Middleware
app.use(cors());
app.use(express.json());

// MongoDB Connection
mongoose.connect(process.env.MONGODB_URI)
    .then(() => console.log('MongoDB Connected'))
    .catch(err => console.log('MongoDB Connection Error:', err));

// Multer Setup (Memory Limit)
const upload = multer({
    storage: multer.memoryStorage(),
    limits: { fileSize: 5 * 1024 * 1024 } // 5MB limit
});

// Routes
app.get('/', (req, res) => {
    res.send('Face Classification Backend Running');
});

app.use('/api/auth', authRouter);

// History Endpoint
app.get('/api/history', async (req, res) => {
    try {
        const userId = req.query.userId;
        if (!userId) return res.status(400).json({ msg: 'User ID required' });

        const history = await Prediction.find({ userId }).sort({ timestamp: -1 });
        res.json(history);
    } catch (err) {
        res.status(500).json({ error: err.message });
    }
});

// Predict Endpoint
app.post('/api/predict-image', upload.single('image'), async (req, res) => {
    try {
        if (!req.file) {
            return res.status(400).json({ error: 'No image uploaded' });
        }

        const { userId } = req.body; // Get userId from request body
        console.log(`Processing image: ${req.file.originalname} for User: ${userId || 'Guest'}`);

        // Send to ML Service
        const mlServiceUrl = process.env.ML_SERVICE_URL || 'http://localhost:8000';
        const formData = new FormData();
        formData.append('file', req.file.buffer, {
            filename: req.file.originalname,
            contentType: req.file.mimetype
        });

        const mlResponse = await axios.post(`${mlServiceUrl}/predict`, formData, {
            headers: {
                ...formData.getHeaders()
            }
        });

        const { label, confidence, explanation, debug_variance } = mlResponse.data;
        console.log(`Prediction: ${label} (${confidence})`);
        console.log(`Debug: Variance=${debug_variance} | Reason=${explanation}`);

        // Save to Database
        const newPrediction = new Prediction({
            imageName: req.file.originalname,
            predictionLabel: label,
            confidence: confidence,
            userId: userId || null
        });

        await newPrediction.save();
        console.log('Result saved to MongoDB');

        res.json({
            label,
            confidence
        });

    } catch (err) {
        console.error('Error processing request:', err.message);
        if (err.response) {
            console.error('ML Service Error:', err.response.data);
        }
        res.status(500).json({ error: 'Internal Server Error' });
    }
});

// Start Server
app.listen(PORT, () => {
    console.log(`Server running on port ${PORT}`);
});
