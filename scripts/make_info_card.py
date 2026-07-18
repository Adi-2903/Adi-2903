import os

def generate_info_card(output_path="info-card.svg"):
    user = "adi@github"
    host = "Adi-2903"
    
    data = [
        ("Role", "Software Engineer / Student"),
        ("Stack", "Python, TypeScript, React, Node.js"),
        ("Focus", "Web Development & AI Integrations"),
        ("Location", "Earth"),
        ("Hobbies", "Coding, Gaming, Coffee"),
    ]
    
    line_height = 24
    padding = 30
    width = 490
    height = padding * 2 + (len(data) + 3) * line_height
    
    is_static = os.environ.get("STATIC") == "1"
    
    if is_static:
        anim_css = ".anim { opacity: 1; }"
    else:
        anim_css = """
        @keyframes fadeIn {
            0% { opacity: 0; transform: translateX(-10px); }
            100% { opacity: 1; transform: translateX(0); }
        }
        .anim {
            opacity: 0;
            animation: fadeIn 0.5s ease-out forwards;
        }"""

    svg_header = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}">
    <style>
        .text {{
            font-family: "Courier New", Courier, monospace;
            font-size: 16px;
            fill: #c9d1d9;
        }}
        .key {{ fill: #58a6ff; font-weight: bold; }}
        .title {{ fill: #3fb950; font-weight: bold; }}
        .sep {{ fill: #8b949e; }}
        .bg {{ fill: #0d1117; }}
        {anim_css}
    </style>
    <rect class="bg" width="{width}" height="{height}" rx="6" />
    <g class="text">
'''

    svg_body = ""
    
    y = padding + line_height
    svg_body += f'''
        <g class="anim" style="animation-delay: 0.2s">
            <text x="{padding}" y="{y}"><tspan class="title">{user}</tspan><tspan class="sep">@</tspan><tspan class="title">{host}</tspan></text>
        </g>
'''
    y += line_height
    svg_body += f'''
        <g class="anim" style="animation-delay: 0.4s">
            <text x="{padding}" y="{y}">-------------------------</text>
        </g>
'''
    
    delay = 0.6
    for key, value in data:
        y += line_height
        val_escaped = value.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
        svg_body += f'''
        <g class="anim" style="animation-delay: {delay}s">
            <text x="{padding}" y="{y}"><tspan class="key">{key}</tspan><tspan class="sep">: </tspan><tspan>{val_escaped}</tspan></text>
        </g>
'''
        delay += 0.2
        
    svg_footer = '''
    </g>
</svg>'''
    
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(svg_header + svg_body + svg_footer)

if __name__ == "__main__":
    generate_info_card()
    print("Generated info-card.svg")
