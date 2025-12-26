import os
import cv2
import pickle
import numpy as np
import xgboost as xgb
import h5py
from feature_extraction import extract_features

def debug():
    # Paths
    base_path = os.getcwd()
    model_path = os.path.join(base_path, "models/face_real_vs_ai_model.h5")
    scaler_path = os.path.join(base_path, "models/scaler.pkl")
    # Test Image (Captured from User Upload)
    img_path = os.path.join(base_path, "debug_image.jpg")
    
    print(f"--- DEBUGGING {img_path} ---")
    
    # 1. Load Scaler
    with open(scaler_path, "rb") as f:
        scaler = pickle.load(f)
    
    print("\n[Scaler Stats]")
    print(f"Mean (first 10): {scaler.mean_[:10]}")
    print(f"Scale (first 10): {scaler.scale_[:10]}")
    
    # 2. Extract Features
    image = cv2.imread(img_path)
    if image is None:
        print("Failed to load image")
        return

    print("\n[Feature Extraction]")
    # CRITICAL FIX: Resize to 128x128 to match training data
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image = cv2.resize(image, (128, 128))
    features = extract_features(image)
    features_arr = np.array(features).reshape(1, -1)
    
    print(f"Raw Features Shape: {features_arr.shape}")
    print(f"Raw Min: {features_arr.min():.4f}, Max: {features_arr.max():.4f}, Mean: {features_arr.mean():.4f}")
    print(f"Raw Sample (first 10): {features_arr[0][:10]}")
    
    # 3. Transform
    features_scaled = scaler.transform(features_arr)
    print("\n[Scaled Features]")
    print(f"Scaled Min: {features_scaled.min():.4f}, Max: {features_scaled.max():.4f}, Mean: {features_scaled.mean():.4f}")
    print(f"Scaled Sample (first 10): {features_scaled[0][:10]}")
    
    # 4. Load Model
    print("\n[Model Prediction]")
    with h5py.File(model_path, 'r') as f:
        model_bytes = f['model_bytes'][()].tobytes()
        if 'best_threshold' in f.attrs:
            print(f"Model Threshold: {f.attrs['best_threshold']}")
    
    xgb_model = xgb.Booster()
    xgb_model.load_model(bytearray(model_bytes))
    
    dtest = xgb.DMatrix(features_scaled)
    prob = xgb_model.predict(dtest)[0]
    print(f"Inference Probability (Fakeness): {prob:.6f}")

if __name__ == "__main__":
    debug()
