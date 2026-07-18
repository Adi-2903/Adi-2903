import json
import os

PALETTE = ["#161b22", "#0e4429", "#006d32", "#26a641", "#39d353", "#69f0a0"]

def render_heatmap():
    try:
        with open("data/contributions.json", "r", encoding="utf-8") as f:
            data = json.load(f)
    except FileNotFoundError:
        print("data/contributions.json not found. Run fetch_contributions.py first.")
        return
        
    if not data:
        print("No data found.")
        return
        
    box_size = 11
    gap = 4
    padding = 20
    
    weeks = []
    current_week = []
    for day in data:
        current_week.append(day)
        if len(current_week) == 7:
            weeks.append(current_week)
            current_week = []
            
    if current_week:
        weeks.append(current_week)
        
    num_weeks = len(weeks)
    if num_weeks == 0:
        return
        
    width = padding * 2 + num_weeks * (box_size + gap) - gap
    height = padding * 2 + 7 * (box_size + gap) - gap + 40
    
    svg_header = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}">
    <style>
        .bg {{ fill: #0d1117; }}
        .day {{ rx: 2; ry: 2; }}
        .text {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif;
            font-size: 12px;
            fill: #7d8590;
        }}
        @keyframes slideDown {{
            0% {{ opacity: 0; transform: translateY(-10px); }}
            100% {{ opacity: 1; transform: translateY(0); }}
        }}
        .anim {{
            opacity: 0;
            animation: slideDown 0.6s ease-out forwards;
        }}
    </style>
    <rect class="bg" width="{width}" height="{height}" rx="6" />
    <g transform="translate({padding}, {padding})">
'''
    
    svg_body = ""
    
    for w_idx, week in enumerate(weeks):
        x = w_idx * (box_size + gap)
        for d_idx, day in enumerate(week):
            y = d_idx * (box_size + gap)
            level = min(day.get("level", 0), len(PALETTE) - 1)
            color = PALETTE[level]
            
            delay = (w_idx + d_idx) * 0.02
            
            svg_body += f'''
        <rect class="day anim" x="{x}" y="{y}" width="{box_size}" height="{box_size}" fill="{color}" style="animation-delay: {delay}s" />
'''

    total_count = sum(d.get("count", 0) for d in data)
    y_footer = 7 * (box_size + gap) + 20
    
    legend_svg = ""
    legend_x = num_weeks * (box_size + gap) - gap - (5 * (box_size + gap) + 70)
    if legend_x < 200:
        legend_x = 200
        
    legend_svg += f'<text class="text anim" x="{legend_x}" y="{y_footer}" style="animation-delay: 1.5s">Less</text>'
    
    for i, color in enumerate(PALETTE[:5]):
        lx = legend_x + 35 + i * (box_size + gap)
        legend_svg += f'<rect class="day anim" x="{lx}" y="{y_footer - 9}" width="{box_size}" height="{box_size}" fill="{color}" style="animation-delay: 1.5s" />'
        
    legend_svg += f'<text class="text anim" x="{legend_x + 35 + 5 * (box_size + gap)}" y="{y_footer}" style="animation-delay: 1.5s">More</text>'
    
    svg_footer = f'''
        <text class="text anim" x="0" y="{y_footer}" style="animation-delay: 1.5s">{total_count} contributions in the last year</text>
        {legend_svg}
    </g>
</svg>'''
    
    with open("contrib-heatmap.svg", "w", encoding="utf-8") as f:
        f.write(svg_header + svg_body + svg_footer)
    
    print("Generated contrib-heatmap.svg")

if __name__ == "__main__":
    render_heatmap()
