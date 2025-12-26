import xgboost as xgb
import numpy as np
import h5py
import pickle
import matplotlib.pyplot as plt
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix, roc_curve, auc, precision_recall_curve, ConfusionMatrixDisplay
import os
from data_loader import load_dataset

def load_model_from_h5(path):
    print(f"Loading model from {path}...")
    with h5py.File(path, 'r') as f:
        model_bytes = f['model_bytes'][()].tobytes()
    
    model = xgb.Booster()
    model.load_model(bytearray(model_bytes))
    return model

def plot_metrics(history_path):
    if not os.path.exists(history_path):
        print(f"Warning: {history_path} not found. Skipping training plots.")
        return

    with open(history_path, 'rb') as f:
        history = pickle.load(f)
    
    # history structure: {'train': {'logloss': [...], 'error': [...]}, 'valid': ...}
    epochs = len(history['train']['logloss'])
    x_axis = range(1, epochs + 1)
    
    # Plot Loss
    plt.figure()
    plt.plot(x_axis, history['train']['logloss'], label='Train')
    plt.plot(x_axis, history['valid']['logloss'], label='Validation')
    plt.title('Training vs Validation Loss (Logloss)')
    plt.xlabel('Epochs')
    plt.ylabel('Logloss')
    plt.legend()
    plt.savefig('plots/loss_curve.png')
    plt.close()
    
    # Plot Accuracy (Converted from error) if available
    try:
        print(f"Train keys: {history['train'].keys()}")
        if 'error' in history['train']:
            train_acc = [1 - x for x in history['train']['error']]
            valid_acc = [1 - x for x in history['valid']['error']]
            
            plt.figure()
            plt.plot(x_axis, train_acc, label='Train')
            plt.plot(x_axis, valid_acc, label='Validation')
            plt.title('Training vs Validation Accuracy')
            plt.xlabel('Epochs')
            plt.ylabel('Accuracy')
            plt.legend()
            plt.savefig('plots/accuracy_curve.png')
            plt.close()
        else:
            print("Warning: 'error' metric not found in history. Skipping accuracy curve.")
    except Exception as e:
        print(f"Error plotting accuracy: {e}")

def evaluate():
    # Load Model
    model_path = "models/face_real_vs_ai_model.h5"
    scaler_path = "models/scaler.pkl"
    
    if not os.path.exists(model_path):
        print("Model not found. Run train.py first.")
        return

    model = load_model_from_h5(model_path)
    
    # Load Scaler
    if not os.path.exists(scaler_path):
        print("Scaler not found. Run train.py first.")
        return
        
    with open(scaler_path, "rb") as f:
        scaler = pickle.load(f)
    
    # Load Test Data
    # Using 2000 for quick eval
    print("Loading test data (limit=2000)...")
    X_test, y_test = load_dataset("test", max_samples=2000, use_face_detection=False)
    
    # Normalize features
    print("Normalizing test features...")
    X_test = scaler.transform(X_test)
    
    dtest = xgb.DMatrix(X_test)
    
    # Predict
    print("Predicting...")
    y_probs = model.predict(dtest)
    y_pred = (y_probs > 0.5).astype(int)
    
    # Metrics
    acc = accuracy_score(y_test, y_pred)
    prec = precision_score(y_test, y_pred)
    rec = recall_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred)
    
    print("-" * 30)
    print(f"Accuracy: {acc:.4f}")
    print(f"Precision: {prec:.4f}")
    print(f"Recall:    {rec:.4f}")
    print(f"F1-Score:  {f1:.4f}")
    print("-" * 30)
    
    # Ensure plots dir exists
    os.makedirs("plots", exist_ok=True)
    
    # 1. Confusion Matrix
    cm = confusion_matrix(y_test, y_pred)
    disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=['REAL', 'AI-GENERATED'])
    disp.plot(cmap=plt.cm.Blues)
    plt.title('Confusion Matrix')
    plt.savefig('plots/confusion_matrix.png')
    plt.close()
    
    # 2. ROC Curve
    fpr, tpr, _ = roc_curve(y_test, y_probs)
    roc_auc = auc(fpr, tpr)
    plt.figure()
    plt.plot(fpr, tpr, color='darkorange', lw=2, label=f'ROC curve (area = {roc_auc:.2f})')
    plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--')
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title('Receiver Operating Characteristic')
    plt.legend(loc="lower right")
    plt.savefig('plots/roc_curve.png')
    plt.close()
    
    # 3. Precision-Recall Curve
    precision, recall, _ = precision_recall_curve(y_test, y_probs)
    plt.figure()
    plt.plot(recall, precision, color='blue', lw=2, label='PR curve')
    plt.xlabel('Recall')
    plt.ylabel('Precision')
    plt.title('Precision-Recall Curve')
    plt.legend()
    plt.savefig('plots/precision_recall_curve.png')
    plt.close()
    
    # 4 & 5. Accuracy & Loss Curves (from history)
    plot_metrics("models/training_history.pkl")
    
    print("All evaluation plots saved to 'plots/' directory.")

if __name__ == "__main__":
    evaluate()
