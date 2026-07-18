import sys
import cv2
import numpy as np
from PIL import Image
from rembg import remove
import io

def prep_photo(input_path, output_path="source-prepped.png"):
    print(f"Reading {input_path}...")
    with open(input_path, "rb") as i:
        input_data = i.read()
    
    print("Removing background...")
    subject_data = remove(input_data)
    
    # Convert to PIL Image
    subject_img = Image.open(io.BytesIO(subject_data))
    
    # Convert to OpenCV format (numpy array) for CLAHE
    # Convert RGBA to grayscale
    cv_img = cv2.cvtColor(np.array(subject_img), cv2.COLOR_RGBA2GRAY)
    
    # Extract alpha channel
    alpha = np.array(subject_img)[:, :, 3]
    
    print("Applying CLAHE...")
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
    enhanced = clahe.apply(cv_img)
    
    # Composite onto white background
    print("Compositing onto white background...")
    white_bg = np.ones_like(enhanced) * 255
    
    # normalized alpha
    alpha_norm = alpha / 255.0
    
    final_img = (enhanced * alpha_norm + white_bg * (1 - alpha_norm)).astype(np.uint8)
    
    cv2.imwrite(output_path, final_img)
    print(f"Saved to {output_path}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python prep_photo.py <input_image>")
        sys.exit(1)
    prep_photo(sys.argv[1])
