import cv2
import numpy as np
import os

def get_signal_stats(img_path):
    img = cv2.imread(img_path)
    if img is None:
        return None
    
    # 1. Laplacian Variance (Sharpness/Noise)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    lap_var = cv2.Laplacian(gray, cv2.CV_64F).var()
    
    # 2. FFT Power (High Frequency Content)
    f = np.fft.fft2(gray)
    fshift = np.fft.fftshift(f)
    magnitude_spectrum = 20 * np.log(np.abs(fshift) + 1e-7)
    mean_spectrum = np.mean(magnitude_spectrum)
    
    return {
        "Laplacian Var": lap_var,
        "Mean FFT Power": mean_spectrum
    }

def analyze():
    base_path = os.getcwd()
    
    # User's Failed AI Image
    fake_img = "debug_image.jpg"
    
    # Known Real Image
    real_img = r"c:\Users\punam\Downloads\archive (5)\real_vs_fake\real-vs-fake\test\real\00001.jpg"
    
    print(f"--- ANALYZING SIGNAL STATS ---")
    
    real_dir = r"c:\Users\punam\Downloads\archive (5)\real_vs_fake\real-vs-fake\test\real"
    print(f"\n--- SCANNING REAL IMAGES for LOW VARIANCE ---")
    
    low_var_count = 0
    total = 0
    min_var = 10000
    
    import glob
    files = glob.glob(os.path.join(real_dir, "*.jpg"))[:2000] # Check first 2000
    
    for f in files:
        stats = get_signal_stats(f)
        if stats:
            v = stats['Laplacian Var']
            min_var = min(min_var, v)
            if v < 100:
                print(f"[WARNING] Low Var Real: {v:.2f} - {os.path.basename(f)}")
                low_var_count += 1
            total += 1
            
    print(f"Scanned {total} Real images.")
    print(f"Min Variance Found: {min_var:.2f}")
    print(f"Images below 100: {low_var_count}")

if __name__ == "__main__":
    analyze()
