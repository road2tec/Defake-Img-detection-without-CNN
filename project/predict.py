import xgboost as xgb
import numpy as np
import h5py
import cv2
import os
import argparse
import pickle
from feature_extraction import extract_features
# Import face detection
from data_loader import detect_and_crop_face

def load_model_from_h5(path):
    if not os.path.exists(path):
        raise FileNotFoundError(f"Model file not found at {path}")
        
    with h5py.File(path, 'r') as f:
        model_bytes = f['model_bytes'][()].tobytes()
    
    model = xgb.Booster()
    model.load_model(bytearray(model_bytes))
    return model

def predict_face(image_path):
    """
    Predict if a face is REAL or AI-GENERATED.
    """
    model_path = "models/face_real_vs_ai_model.h5"
    scaler_path = "models/scaler.pkl"
    
    # Load Model
    try:
        model = load_model_from_h5(model_path)
    except FileNotFoundError:
        return {"error": "Model not found. Please train the model first."}
    
    # Load Scaler
    try:
        with open(scaler_path, "rb") as f:
            scaler = pickle.load(f)
    except FileNotFoundError:
        return {"error": "Scaler not found. Please train the model first."}

    # Load and Preprocess Image
    if not os.path.exists(image_path):
        return {"error": "Image file not found."}
        
    try:
        img = cv2.imread(image_path)
        if img is None:
            return {"error": "Failed to read image."}
            
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        
        # Face Detection & Cropping with Fallback
        # CRITICAL FIX: Training was done on FULL IMAGES (use_face_detection=False).
        # We must disable crop to match training distribution.
        # cropped = detect_and_crop_face(img)
        # if cropped is not None and cropped.size > 0:
        #     img = cropped
        # else:
        #     pass 
        pass
        
        img = cv2.resize(img, (128, 128))
    except Exception as e:
        return {"error": f"Error preprocessing image: {str(e)}"}
        
    # Extract Features
    try:
        features = extract_features(img)
        # Reshape for XGBoost (1, n_features)
        features = features.reshape(1, -1)
        
        # Safety Check: Feature Dimension Mismatch
        if features.shape[1] != scaler.mean_.shape[0]:
            raise ValueError(f"Feature dimension mismatch: Expected {scaler.mean_.shape[0]}, got {features.shape[1]}")
        
        # Normalize
        features = scaler.transform(features)
        
        dtest = xgb.DMatrix(features)
    except Exception as e:
        return {"error": f"Error extracting features: {str(e)}"}
        
    # Predict
    try:
        prob = model.predict(dtest)[0]
        
        # Strict Threshold Correction: 0.42
        THRESHOLD = 0.42
        label = "AI-GENERATED" if prob > THRESHOLD else "REAL"
        confidence = float(prob) if prob > THRESHOLD else float(1 - prob)
        
        return {
            "label": label,
            "confidence": confidence
        }
    except Exception as e:
        return {"error": f"Prediction error: {str(e)}"}

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Predict if a face is REAL or AI-GENERATED")
    parser.add_argument("--image", type=str, required=True, help="Path to the face image")
    args = parser.parse_args()
    
    result = predict_face(args.image)
    print(result)
