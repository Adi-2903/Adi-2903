import cv2
import numpy as np
import os
from PIL import Image
import io

def get_foreground_rgba(input_path="source-photo.jpg"):
    from rembg import remove
    with open(input_path, "rb") as i:
        input_data = i.read()
    subject_data = remove(input_data)
    img = Image.open(io.BytesIO(subject_data)).convert("RGBA")
    return np.array(img)

def generate_dot_matrix(rgba_img, output_path="avi-dotmatrix.svg"):
    target_w = 60
    h, w = rgba_img.shape[:2]
    target_h = int((h / w) * target_w)
    
    resized = cv2.resize(rgba_img, (target_w, target_h))
    
    dot_size = 6
    width = target_w * dot_size
    height = target_h * dot_size
    
    svg_body = ""
    for y in range(target_h):
        for x in range(target_w):
            r, g, b, a = resized[y, x]
            if a < 50:
                continue
            
            brightness = 0.299*r + 0.587*g + 0.114*b
            radius = (brightness / 255.0) * (dot_size / 2.0)
            
            if radius > 0.5:
                cx = x * dot_size + dot_size/2
                cy = y * dot_size + dot_size/2
                delay = (y * 0.05)
                svg_body += f'''
        <circle cx="{cx}" cy="{cy}" r="0" fill="#c9d1d9">
            <animate attributeName="r" from="0" to="{radius}" begin="{delay}s" dur="0.5s" fill="freeze" />
        </circle>
'''

    svg_header = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}">
    <rect width="{width}" height="{height}" rx="6" fill="#0d1117" />
    <g>
'''
    svg_footer = "</g></svg>"
    
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(svg_header + svg_body + svg_footer)

if __name__ == "__main__":
    print("Generating Dot-Matrix portrait...")
    rgba = get_foreground_rgba("source-photo.jpg")
    generate_dot_matrix(rgba)
    print("Done! Generated avi-dotmatrix.svg")
