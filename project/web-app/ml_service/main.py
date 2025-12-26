from fastapi import FastAPI, File, UploadFile, HTTPException
import uvicorn
import sys
import os
import cv2
import numpy as np
import pickle
import xgboost as xgb
import h5py

# Add parent directory to path to import existing modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

try:
    from feature_extraction import extract_features
    from data_loader import detect_and_crop_face
except ImportError as e:
    print(f"Error importing modules: {e}")
    sys.exit(1)

app = FastAPI()

# Global variables to hold model and scaler
# Global variable for threshold
THRESHOLD = 0.5

def load_model_from_h5(path):
    global THRESHOLD
    if not os.path.exists(path):
        raise FileNotFoundError(f"Model file not found at {path}")
        
    with h5py.File(path, 'r') as f:
        model_bytes = f['model_bytes'][()].tobytes()
        if 'best_threshold' in f.attrs:
            THRESHOLD = float(f.attrs['best_threshold'])
            print(f"Loaded Optimal Threshold from model: {THRESHOLD:.4f}")
        else:
            print("No threshold found in model, using default 0.42")
            THRESHOLD = 0.42
    
    xgb_model = xgb.Booster()
    xgb_model.load_model(bytearray(model_bytes))
    return xgb_model

@app.on_event("startup")
async def startup_event():
    global model, scaler, THRESHOLD
    try:
        # Paths relative to web-app/ml_service/
        base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))
        model_path = os.path.join(base_path, "models/face_real_vs_ai_model.h5")
        scaler_path = os.path.join(base_path, "models/scaler.pkl")
        
        print(f"Loading model from {model_path}...")
        model = load_model_from_h5(model_path)
        print("Model loaded successfully.")
        
        print(f"Loading scaler from {scaler_path}...")
        with open(scaler_path, "rb") as f:
            scaler = pickle.load(f)
        print("Scaler loaded successfully.")
        
    except Exception as e:
        print(f"CRITICAL ERROR loading artifacts: {e}")
        # We don't exit here to maintain the server process, but predictions will fail
        
@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    global model, scaler
    
    if model is None or scaler is None:
        raise HTTPException(status_code=500, detail="Model or Scaler not loaded.")
    
    try:
        # Read image
        contents = await file.read()
        nparr = np.frombuffer(contents, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        if img is None:
            raise HTTPException(status_code=400, detail="Invalid image file.")
            
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        
        # Preprocessing Pipeline (Identical to Training)
        # Preprocessing Pipeline (Identical to Training)
        # 1. Face Detection & Cropping (Robust Fallback)
        # CRITICAL FIX: Training was done on FULL IMAGES. Disabling crop to match.
        # cropped = detect_and_crop_face(img)
        # if cropped is not None and cropped.size > 0:
        #     img = cropped
        #     print("SUCCESS: Face detected and cropped.")
        # else:
        #     print("WARNING: Face detection failed. Fallback to FULL IMAGE.")
        pass
        
        # 2. Resize
        img_resized = cv2.resize(img, (128, 128))
        
        # 3. Feature Extraction
        features = extract_features(img_resized)
        features = features.reshape(1, -1)
        
        # Safety Check: Feature Dimension Mismatch
        if features.shape[1] != scaler.mean_.shape[0]:
            raise HTTPException(status_code=500, detail=f"Feature dimension mismatch: Expected {scaler.mean_.shape[0]}, got {features.shape[1]}")

        # 4. Normalization
        features = scaler.transform(features)
        
        # Prediction
        dtest = xgb.DMatrix(features)
        xgb_prob = model.predict(dtest)[0]
        
        # --- HYBRID DETECTION LOGIC ---
        # Calculate Laplacian Variance (Sharpness/Noise)
        gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
        lap_var = cv2.Laplacian(gray, cv2.CV_64F).var()
        
        print(f"Laplacian Variance: {lap_var:.2f}")
        
        # --- HYBRID DETECTION LOGIC V2 ---
        # Calculate Laplacian Variance (Sharpness/Noise)
        gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
        lap_var = cv2.Laplacian(gray, cv2.CV_64F).var()
        
        print(f"Laplacian Variance: {lap_var:.2f} | XGB Prob: {xgb_prob:.4f}")
        
        # Heuristic Thresholds
        # 1. ABSOLUTE FAKE: Extremely smooth (Var < 100). Almost certainly AI.
        # 2. SUSPICIOUS: Smooth (Var < 300) AND Model shows some suspicion (Prob > 0.20).
        # 3. UNCERTAIN: If the model is unsure (Prob 0.3-0.5) and it's not sharp (Var < 500), assume AI.
        
        is_absolute_fake = lap_var < 100
        is_suspicious_smooth = (lap_var < 350) and (xgb_prob > 0.20)
        
        if is_absolute_fake:
            label = "AI-GENERATED"
            confidence = 0.98
            explanation = f"Logic: Image is unnaturally smooth (Var {lap_var:.1f} < 100)."
        elif is_suspicious_smooth:
            label = "AI-GENERATED"
            confidence = 0.85
            explanation = f"Logic: Smooth texture (Var {lap_var:.1f}) + Model suspicion ({xgb_prob:.2f})."
        elif xgb_prob > THRESHOLD:
            label = "AI-GENERATED"
            confidence = float(xgb_prob)
            explanation = f"Logic: Model confidence ({xgb_prob:.2f}) > threshold ({THRESHOLD:.2f})"
        else:
            label = "REAL" 
            confidence = float(1 - xgb_prob)
            explanation = f"Logic: Model confidence ({xgb_prob:.2f}) <= threshold ({THRESHOLD:.2f})"
        
        return {
            "label": label,
            "confidence": confidence,
            "explanation": explanation,
            "debug_variance": lap_var,
            "debug_prob": float(xgb_prob)
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction error: {str(e)}")

@app.get("/health")
def health_check():
    return {"status": "running", "model_loaded": model is not None}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
