import cv2
import numpy as np
from skimage.feature import local_binary_pattern, hog
from scipy.stats import entropy

def extract_hog_features(image):
    """
    Extract Histogram of Oriented Gradients (HOG) features.
    """
    # Convert to grayscale for HOG
    gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    fd = hog(gray, orientations=9, pixels_per_cell=(8, 8),
             cells_per_block=(2, 2), block_norm='L2-Hys', 
             transform_sqrt=True, visualize=False, channel_axis=None)
    return fd

def extract_lbp_features(image):
    """
    Extract Local Binary Patterns (LBP) features.
    """
    # Convert to grayscale for LBP
    gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    radius = 1
    n_points = 8 * radius
    lbp = local_binary_pattern(gray, n_points, radius, method="uniform")
    (hist, _) = np.histogram(lbp.ravel(), bins=np.arange(0, n_points + 3), range=(0, n_points + 2))
    
    # Normalize the histogram
    hist = hist.astype("float")
    hist /= (hist.sum() + 1e-7)
    return hist

def extract_color_histogram(image):
    """
    Extract RGB Color Histogram features.
    """
    # Calculate histogram for each channel with REDUCED bins (32)
    hist_features = []
    for i in range(3): # R, G, B
        hist = cv2.calcHist([image], [i], None, [32], [0, 256])
        hist = cv2.normalize(hist, hist).flatten()
        hist_features.extend(hist)
    return np.array(hist_features)

def extract_texture_stats(image):
    """
    Extract texture statistics (mean, variance, entropy) for each channel.
    """
    stats = []
    for i in range(3): # R, G, B
        channel = image[:, :, i]
        stats.append(np.mean(channel))
        stats.append(np.var(channel))
        
        # Entropy calculation (Histogram-based)
        # Compute 32-bin histogram for entropy stability
        hist = cv2.calcHist([channel], [0], None, [32], [0, 256])
        hist = hist.flatten()
        hist = hist / (hist.sum() + 1e-7)  # Normalize
        stats.append(entropy(hist, base=2))
        
    return np.array(stats)

def extract_features(image):
    """
    Master function to extract and concatenate all features.
    Input: RGB image arrays (H, W, 3)
    Output: 1D feature vector
    """
    hog_feats = extract_hog_features(image)
    lbp_feats = extract_lbp_features(image)
    color_feats = extract_color_histogram(image)
    texture_feats = extract_texture_stats(image)
    
    # Concatenate all features
    combined_features = np.concatenate([hog_feats, lbp_feats, color_feats, texture_feats])
    return combined_features

if __name__ == "__main__":
    # Simple test
    dummy_img = np.random.randint(0, 255, (128, 128, 3), dtype=np.uint8)
    feats = extract_features(dummy_img)
    print(f"Feature vector shape: {feats.shape}")
