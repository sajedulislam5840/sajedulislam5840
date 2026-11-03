from PIL import Image

RAMP = "$@B%8&WM#*oahkbdpqwmZO0QLCJYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,\"^`'. "
RAMP = RAMP[::-1] # Dark to bright inverted for black background

WIDTH = 95

def image_to_ascii(image_path="source-prepped.png"):
    img = Image.open(image_path)
    aspect_ratio = img.height / img.width
    height = int(WIDTH * aspect_ratio * 0.45)
    img = img.resize((WIDTH, height), Image.Resampling.LANCZOS)
    
    lines = []
    for y in range(height):
        line = "".join(RAMP[int((img.getpixel((x, y)) / 255) * (len(RAMP) - 1))] for x in range(WIDTH))
        lines.append(line)
    return lines

def generate_svg(lines, output_path="sajedul-ascii.svg"):
    char_w, char_h, font_size = 4.6, 8.2, 7.8
    svg_w = int(WIDTH * char_w) + 20
    svg_h = int(len(lines) * char_h) + 25
    
    rows = []
    for i, line in enumerate(lines):
        safe_line = line.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace(" ", "&#160;")
        y = 20 + (i * char_h)
        rows.append(f"""<g opacity="0"><text x="10" y="{y:.1f}" fill="#58a6ff" font-family="monospace" font-size="{font_size}px">{safe_line}</text><animate attributeName="opacity" from="0" to="1" dur="0.03s" begin="{i * 0.02:.2f}s" fill="freeze" /></g>""")
        
    svg_code = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{svg_w}" height="{svg_h}" viewBox="0 0 {svg_w} {svg_h}"><rect width="100%" height="100%" fill="#0d1117" rx="8" stroke="#30363d" stroke-width="1.5"/>{''.join(rows)}</svg>"""
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(svg_code)
    print(f"[+] Re-rendered: {output_path}")

if __name__ == "__main__":
    generate_svg(image_to_ascii())
