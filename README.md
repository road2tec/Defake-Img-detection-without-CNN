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

## 🔍 How It Works (Tiered Hybrid Detection V2)

The system employs a sophisticated 3-tier detection pipeline to ensure high accuracy against modern GAN and Diffusion-based AI images:

1.  **Tier 1: Texture Sharpness Analysis (Laplacian Variance)**
    -   AI-generated images often suffer from "unnatural smoothness."
    -   **Rule**: If variance is **< 100**, the image is immediately flagged as **ABSOLUTE FAKE (98% confidence)**.

2.  **Tier 2: suspicious texture + Model Probability**
    -   Moderate smoothness combined with slight model suspicion.
    -   **Rule**: If variance is **< 350** AND XGBoost probability is **> 0.20**, it is flagged as **AI-GENERATED (85% confidence)**.

3.  **Tier 3: XGBoost Booster Model**
    -   A gradient boosted model trained on grayscale signal features.
    -   **Rule**: If XGBoost probability exceeds the **Optimal Threshold (e.g., 0.42)**, it is classified as **AI-GENERATED**.

## 🛠️ Technology Stack

- **Machine Learning**: Python 3.10+, XGBoost, OpenCV, Scikit-Learn.
- **Frontend**: React.js, Vite, Framer Motion, Tailwind CSS (for modern UI).
- **Backend**: Node.js, Express, MongoDB Atlas.
- **ML API**: FastAPI (High-performance async server).

## 🛡️ License

This project is for educational and research purposes.
