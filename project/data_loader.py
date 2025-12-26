import os
import cv2
import numpy as np
from feature_extraction import extract_features
import random

# Dataset paths
BASE_DIR = r"c:\Users\punam\Downloads\archive (5)\real_vs_fake\real-vs-fake"
TRAIN_DIR = os.path.join(BASE_DIR, "train")
VALID_DIR = os.path.join(BASE_DIR, "valid")
TEST_DIR = os.path.join(BASE_DIR, "test")

from concurrent.futures import ProcessPoolExecutor, as_completed
import os
import cv2
import numpy as np
from feature_extraction import extract_features
import random

# Dataset paths
BASE_DIR = r"c:\Users\punam\Downloads\archive (5)\real_vs_fake\real-vs-fake"
TRAIN_DIR = os.path.join(BASE_DIR, "train")
VALID_DIR = os.path.join(BASE_DIR, "valid")
TEST_DIR = os.path.join(BASE_DIR, "test")

def detect_and_crop_face(image):
    """
    Detects face and crops it. Returns resized face or original if no face found.
    """
    # Load Haar Cascade
    cascade_path = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
    face_cascade = cv2.CascadeClassifier(cascade_path)
    
    gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.1, 4)
    
    if len(faces) > 0:
        # Get the largest face
        x, y, w, h = max(faces, key=lambda b: b[2] * b[3])
        # Add a small margin
        margin = int(0.1 * h)
        y1 = max(0, y - margin)
        y2 = min(image.shape[0], y + h + margin)
        x1 = max(0, x - margin)
        x2 = min(image.shape[1], x + w + margin)
        return image[y1:y2, x1:x2]
    return image

def process_single_image(args):
    """
    Helper function for parallel processing.
    """
    img_path, label, image_size, use_face_detection = args
    try:
        img = cv2.imread(img_path)
        if img is None:
            return None
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        
        # Face Detection & Cropping (Optional)
        if use_face_detection:
            img = detect_and_crop_face(img)
        
        img = cv2.resize(img, image_size)
        features = extract_features(img)
        return features, label
    except Exception as e:
        # print(f"Error processing {img_path}: {e}")
        return None

def load_dataset(split="train", image_size=(128, 128), max_samples=None, use_face_detection=True):
    """
    Load dataset using parallel processing.
    """
    if split == "train":
        data_dir = TRAIN_DIR
    elif split == "valid":
        data_dir = VALID_DIR
    elif split == "test":
        data_dir = TEST_DIR
    else:
        raise ValueError("Invalid split")

    categories = {"real": 0, "fake": 1}
    tasks = []
    
    print(f"Preparing file list for {split} from {data_dir}...")
    
    for category, label in categories.items():
        path = os.path.join(data_dir, category)
        if not os.path.exists(path):
            continue
            
        params = os.listdir(path)
        # Random shuffle to get a representative sample if max_samples is used
        random.shuffle(params)
        
        # Pass use_face_detection in args
        current_tasks = [(os.path.join(path, p), label, image_size, use_face_detection) for p in params]
        tasks.extend(current_tasks)
    
    # Global shuffle of tasks
    random.shuffle(tasks)
    
    if max_samples:
        tasks = tasks[:max_samples]
        print(f"Limited to {max_samples} samples.")
    
    print(f"Starting parallel feature extraction for {len(tasks)} images...")
    
    X_list = []
    y_list = []
    
    # Use max workers
    with ProcessPoolExecutor() as executor:
        # Submit all tasks
        # We perform chunked mapping for better performance/progress tracking
        # But map implies order validation which we don't strictly need, but zip is easy.
        
        # Using map
        results = executor.map(process_single_image, tasks)
        
        count = 0
        for result in results:
            if result is not None:
                feat, lab = result
                X_list.append(feat)
                y_list.append(lab)
                count += 1
                if count % 1000 == 0:
                    print(f"Processed {count}/{len(tasks)} images...", end='\r')

    print(f"\nCompleted loading {len(X_list)} samples for {split}.")
    
    X = np.array(X_list)
    y = np.array(y_list)
    return X, y

if __name__ == "__main__":
    # Test
    import time
    start = time.time()
    X, y = load_dataset("train", max_samples=100)
    print(f"Time: {time.time() - start:.2f}s")
    print(f"Shape: {X.shape}")

