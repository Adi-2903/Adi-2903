import cv2
import numpy as np

RAMP = " .`:-=+*cs#%@"
TARGET_WIDTH = 100
FONT_ASPECT = 0.5

def image_to_ascii(image_path):
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if img is None:
        raise FileNotFoundError(f"Could not read {image_path}")
    
    h, w = img.shape
    new_w = TARGET_WIDTH
    new_h = int((h / w) * new_w * FONT_ASPECT)
    
    if new_h > 53:
        new_h = 53
        new_w = int((w / h) * new_h / FONT_ASPECT)
        
    resized = cv2.resize(img, (new_w, new_h))
    
    ascii_lines = []
    for row in resized:
        line = ""
        for pixel in row:
            index = int((255 - pixel) / 255.0 * (len(RAMP) - 1))
            line += RAMP[index]
        ascii_lines.append(line)
        
    return ascii_lines

def generate_svg(ascii_lines, output_path="avi-ascii.svg"):
    line_height = 14
    char_width = 8.4
    font_size = 14
    padding = 20
    
    width = int(len(ascii_lines[0]) * char_width + 2 * padding)
    height = int(len(ascii_lines) * line_height + 2 * padding)
    
    svg_header = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}">
    <style>
        .ascii {{
            font-family: "Courier New", Courier, monospace;
            font-size: {font_size}px;
            fill: #c9d1d9;
            white-space: pre;
        }}
        .bg {{
            fill: #0d1117;
        }}
    </style>
    <rect class="bg" width="{width}" height="{height}" rx="6" />
    <g class="ascii">
'''
    
    svg_body = ""
    total_time = 4.0
    time_per_line = total_time / len(ascii_lines)
    
    for i, line in enumerate(ascii_lines):
        y = padding + (i + 1) * line_height
        clip_id = f"clip-{i}"
        delay = i * time_per_line
        duration = time_per_line * 2
        
        svg_body += f'''
        <clipPath id="{clip_id}">
            <rect x="{padding}" y="{y - line_height}" height="{line_height+2}" width="0">
                <animate attributeName="width" from="0" to="{width - 2 * padding}" begin="{delay}s" dur="{duration}s" fill="freeze" />
            </rect>
        </clipPath>
        <text x="{padding}" y="{y}" clip-path="url(#{clip_id})">{line.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')}</text>
        <rect y="{y - line_height + 2}" width="{char_width}" height="{line_height - 2}" fill="#c9d1d9" opacity="0">
            <animate attributeName="x" from="{padding}" to="{width - padding}" begin="{delay}s" dur="{duration}s" />
            <animate attributeName="opacity" values="0;1;1;0" keyTimes="0;0.05;0.95;1" begin="{delay}s" dur="{duration}s" />
        </rect>
'''

    svg_footer = '''
    </g>
</svg>'''
    
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(svg_header + svg_body + svg_footer)

if __name__ == "__main__":
    lines = image_to_ascii("source-prepped.png")
    generate_svg(lines)
    print("Generated avi-ascii.svg")
