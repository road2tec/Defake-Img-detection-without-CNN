# AI-Generated vs Real Image Detection (Defake)

A full-stack, end-to-end system for detecting AI-generated images using a hybrid approach of machine learning and texture analysis. This project focuses on identifying realistic fake faces by analyzing image smoothness (Laplacian Variance) and learned features via XGBoost.

## 🚀 Features

- **Hybrid Detection**: Combines an XGBoost model with heuristic texture analysis for higher accuracy on realistic AI-generated images.
- **Full-Stack Web App**: Integrated React frontend, Node.js backend, and Python FastAPI ML service.
- **History Tracking**: Logged-in users can keep track of their previous predictions using MongoDB Atlas.
- **Glassmorphism UI**: A premium, modern interface with dark themes and smooth animations.

## 🛠️ Technology Stack

- **Machine Learning**: Python, XGBoost, OpenCV, Scikit-Learn.
- **Frontend**: React.js, Vite, Framer Motion (for animations).
- **Backend**: Node.js, Express, MongoDB Atlas, Mongoose.
- **ML API**: FastAPI, Uvicorn.

## 📂 Project Structure

```bash
├── project/
│   ├── web-app/
│   │   ├── client/         # React Frontend
│   │   ├── server/         # Node.js API Server
│   │   └── ml_service/     # FastAPI ML Prediction Service
│   ├── models/             # Trained models (.h5) and scalers
│   ├── training/           # Scripts for feature extraction and training
│   └── analyze_signal.py   # Signal processing utilities
└── .gitignore
```

## ⚙️ Setup and Installation

### 1. ML Service (FastAPI)
```bash
cd project/web-app/ml_service
pip install -r requirements.txt
python main.py
```

### 2. Backend Server (Node.js)
```bash
cd project/web-app/server
npm install
# Create a .env file with MONGODB_URI
node index.js
```

### 3. Frontend Client (React)
```bash
cd project/web-app/client
npm install
npm run dev
```

## 🔍 How It Works

The system uses a robust multi-stage analysis process to distinguish between real and AI-generated images:

1.  **Image Preprocessing**: Uploaded images are resized and converted to optimize feature extraction.
2.  **Feature Extraction**: The system analyzes complex patterns, texture descriptors, and grayscale signal components.
3.  **Advanced Classification**: A high-performance XGBoost model processes these features to determine the probability of an image being AI-generated.
4.  **Hybrid Verification**: The model's findings are integrated with texture analysis metrics to provide a final classification with a confidence score.

## 🛠️ Technology Stack

- **Machine Learning**: Python 3.10+, XGBoost, OpenCV, Scikit-Learn.
- **Frontend**: React.js, Vite, Framer Motion, Tailwind CSS (for modern UI).
- **Backend**: Node.js, Express, MongoDB Atlas.
- **ML API**: FastAPI (High-performance async server).

## 🛡️ License

This project is for educational and research purposes.
