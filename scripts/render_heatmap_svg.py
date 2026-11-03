import json

PALETTE = ["#161b22", "#0e4429", "#006d32", "#26a641", "#39d353", "#69f0a0"]

def render_heatmap(input_path="data/contributions.json", output_path="contrib-heatmap.svg"):
    with open(input_path, "r", encoding="utf-8") as file_handle:
        data = json.load(file_handle)
        
    days = data.get("days", [])
    total = data.get("total", 0)
    
    svg_width = 860
    svg_height = 175
    box_size = 11
    gap = 3
    start_x = 35
    start_y = 45
    
    rects = []
    for idx, day in enumerate(days):
        col = idx // 7
        row = idx % 7
        x = start_x + (col * (box_size + gap))
        y = start_y + (row * (box_size + gap))
        color = PALETTE[min(day.get("level", 0), len(PALETTE) - 1)]
        delay = (col * 0.015) + (row * 0.02)
        
        rect = f"""<rect x="{x}" y="{y}" width="{box_size}" height="{box_size}" rx="2" fill="{color}" opacity="0">
            <animate attributeName="opacity" from="0" to="1" dur="0.2s" begin="{delay:.2f}s" fill="freeze" />
            <animateTransform attributeName="transform" type="translate" from="0, -5" to="0, 0" dur="0.2s" begin="{delay:.2f}s" fill="freeze" />
        </rect>"""
        rects.append(rect)
        
    svg_content = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{svg_width}" height="{svg_height}" viewBox="0 0 {svg_width} {svg_height}">
    <rect width="100%" height="100%" fill="#0d1117" rx="8" stroke="#30363d" stroke-width="1.5" />
    <circle cx="25" cy="20" r="5" fill="#ff5f56"/>
    <circle cx="42" cy="20" r="5" fill="#ffbd2e"/>
    <circle cx="59" cy="20" r="5" fill="#27c93f"/>
    <text x="85" y="24" fill="#8b949e" font-family="monospace" font-size="12">contributions --graph (last 53 weeks)</text>
    {''.join(rects)}
    <text x="35" y="155" fill="#8b949e" font-family="monospace" font-size="11">{total:,} contributions in the last year</text>
    <text x="730" y="155" fill="#8b949e" font-family="monospace" font-size="11">Less</text>
    <rect x="765" y="146" width="9" height="9" rx="2" fill="{PALETTE[0]}" />
    <rect x="778" y="146" width="9" height="9" rx="2" fill="{PALETTE[1]}" />
    <rect x="791" y="146" width="9" height="9" rx="2" fill="{PALETTE[2]}" />
    <rect x="804" y="146" width="9" height="9" rx="2" fill="{PALETTE[3]}" />
    <rect x="817" y="146" width="9" height="9" rx="2" fill="{PALETTE[4]}" />
    <text x="832" y="155" fill="#8b949e" font-family="monospace" font-size="11">More</text>
</svg>"""

    with open(output_path, "w", encoding="utf-8") as out_file:
        out_file.write(svg_content)
    print(f"[+] Generated: {output_path}")

if __name__ == "__main__":
    render_heatmap()
