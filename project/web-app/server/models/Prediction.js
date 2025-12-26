const mongoose = require('mongoose');

const PredictionSchema = new mongoose.Schema({
    imageName: {
        type: String,
        required: true
    },
    predictionLabel: {
        type: String,
        required: true,
        enum: ['REAL', 'AI-GENERATED']
    },
    confidence: {
        type: Number,
        required: true
    },
    userId: {
        type: String,
        required: false
    },
    timestamp: {
        type: Date,
        default: Date.now
    }
});

module.exports = mongoose.model('Prediction', PredictionSchema);
