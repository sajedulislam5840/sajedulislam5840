from PIL import Image

RAMP = " .`:-=+*cs#%@"
WIDTH = 110  # রেজোলিউশন বাড়ানো হলো

def image_to_ascii(image_path="source-prepped.png"):
    img = Image.open(image_path)
    aspect_ratio = img.height / img.width
    height = int(WIDTH * aspect_ratio * 0.50)
    img = img.resize((WIDTH, height), Image.Resampling.LANCZOS)
    
    lines = []
    for y in range(height):
        line = "".join(RAMP[int((255 - img.getpixel((x, y))) / 255 * (len(RAMP) - 1))] for x in range(WIDTH))
        lines.append(line)
    return lines

def generate_svg(lines, output_path="sajedul-ascii.svg"):
    char_width, char_height, font_size = 4.2, 7.5, 7.2
    svg_width = int(WIDTH * char_width) + 20
    svg_height = int(len(lines) * char_height) + 25
    
    svg_rows = []
    for i, line in enumerate(lines):
        safe_line = line.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace(" ", "&#160;")
        y_pos = 20 + (i * char_height)
        svg_rows.append(f"""<g opacity="0"><text x="10" y="{y_pos:.1f}" fill="#c9d1d9" font-family="monospace" font-size="{font_size}px">{safe_line}</text><animate attributeName="opacity" from="0" to="1" dur="0.04s" begin="{i * 0.02:.2f}s" fill="freeze" /></g>""")
        
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(f"""<svg xmlns="http://www.w3.org/2000/svg" width="{svg_width}" height="{svg_height}" viewBox="0 0 {svg_width} {svg_height}"><rect width="100%" height="100%" fill="#0d1117" rx="8" stroke="#30363d" stroke-width="1.5"/>{''.join(svg_rows)}</svg>""")
    print(f"[+] Re-generated: {output_path}")

if __name__ == "__main__":
    generate_svg(image_to_ascii())
