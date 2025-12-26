import xgboost as xgb
import numpy as np
import h5py
import pickle
import os
from sklearn.preprocessing import StandardScaler
from data_loader import load_dataset

def train_model():
    # Load data
    display_limit = 8000
    print(f"Loading data (limit={display_limit} per class)...")
    X_train, y_train = load_dataset("train", max_samples=8000, use_face_detection=False)
    X_valid, y_valid = load_dataset("valid", max_samples=2000, use_face_detection=False)
    
    print(f"Training data shape: {X_train.shape}")
    print(f"Validation data shape: {X_valid.shape}")
    
    # 1. Feature Normalization (StandardScaler)
    print("Normalizing features...")
    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train)
    X_valid = scaler.transform(X_valid)
    
    # Save Scaler
    os.makedirs("models", exist_ok=True)
    with open("models/scaler.pkl", "wb") as f:
        pickle.dump(scaler, f)
        
    # 2. Class Imbalance Handling
    num_real = np.sum(y_train == 0)
    num_fake = np.sum(y_train == 1)
    
    # MANDATORY CHECK: Ensure both classes are present
    assert num_real > 0 and num_fake > 0, "Training data MUST contain both REAL and FAKE classes"
    
    scale_pos_weight = num_real / num_fake
    print(f"Class balance: Real={num_real}, Fake={num_fake}, weight={scale_pos_weight:.2f}")

    # 3. XGBoost Hyperparameters (Optimized)
    params = {
        'objective': 'binary:logistic',
        'eval_metric': ['logloss', 'error'],
        'max_depth': 6,
        'learning_rate': 0.05,
        'subsample': 0.8,
        'colsample_bytree': 0.8,
        'reg_alpha': 0.1,
        'reg_lambda': 1.0,
        'scale_pos_weight': scale_pos_weight,
        'random_state': 42,
        'use_label_encoder': False
    }
    
    # Create DMatrix
    dtrain = xgb.DMatrix(X_train, label=y_train)
    dvalid = xgb.DMatrix(X_valid, label=y_valid)
    
    # Watchlist for monitoring
    watchlist = [(dtrain, 'train'), (dvalid, 'valid')]
    
    # Train with Early Stopping
    print("Starting training (v2 - Fixed Pipeline)...")
    evals_result = {}
    model = xgb.train(
        params,
        dtrain,
        num_boost_round=100, # Increased for better convergence
        evals=watchlist,
        evals_result=evals_result,
        verbose_eval=10,
        early_stopping_rounds=10
    )
    
    # --- POST-TRAINING CHECKS ---
    print("\n--- Post-Training Diagnostic ---")
    val_probs = model.predict(dvalid)
    print(f"Validation Probability Stats: Min={val_probs.min():.4f}, Max={val_probs.max():.4f}, Mean={val_probs.mean():.4f}")
    
    if val_probs.max() < 0.4:
         print("CRITICAL WARNING: Model is not predicting FAKE class confidently!")
    
    # Calculate Optimal Threshold (Youden's J statistic)
    from sklearn.metrics import roc_curve
    fpr, tpr, thresholds = roc_curve(y_valid, val_probs)
    J = tpr - fpr
    ix = np.argmax(J)
    best_thresh = thresholds[ix]
    print(f"Optimal Threshold (ROC): {best_thresh:.4f}")
    
    # Ensure directories exist
    os.makedirs("models", exist_ok=True)
    os.makedirs("plots", exist_ok=True)
    
    # Save Model to H5
    model_path = "models/face_real_vs_ai_model.h5"
    print(f"Saving model to {model_path}...")
    
    model_bytes = model.save_raw()
    
    with h5py.File(model_path, 'w') as f:
        f.create_dataset('model_bytes', data=np.void(model_bytes))
        f.attrs['feature_size'] = X_train.shape[1]
        f.attrs['label_mapping'] = str({0: 'REAL', 1: 'AI-GENERATED'})
        f.attrs['config'] = str(params)
        f.attrs['best_threshold'] = float(best_thresh) # Save threshold
    
    # Save training history for plot generation
    history_path = "models/training_history.pkl"
    with open(history_path, 'wb') as f:
        pickle.dump(evals_result, f)
        
    print("Training complete. Artifacts and Threshold saved.")

if __name__ == "__main__":
    train_model()
