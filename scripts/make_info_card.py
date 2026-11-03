def generate_info_card(output_path="info-card.svg"):
    items = [
        ("user", "sajedulislam5840@github"),
        ("os", "Arch Linux x86_64 / RISC-V"),
        ("host", "BRAC University (B.Sc. CSE)"),
        ("role", "Data Specialist & Systems Dev"),
        ("stack", "C++17, Verilog, Python, Next.js"),
        ("data", "SQL, PostgreSQL, NumPy, OpenCV"),
        ("focus", "Edge AI Inference, Hardware Acceleration"),
        ("contact", "Dhaka, Bangladesh")
    ]
    
    card_width = 490
    card_height = 360
    start_y = 75
    line_step = 28
    
    rows_svg = []
    for i, (key, val) in enumerate(items):
        y = start_y + (i * line_step)
        delay = 0.2 + (i * 0.12)
        row = f"""
        <g opacity="0">
            <text x="35" y="{y}" fill="#58a6ff" font-family="monospace" font-size="13" font-weight="bold">{key.upper()}:</text>
            <text x="125" y="{y}" fill="#c9d1d9" font-family="monospace" font-size="13">{val}</text>
            <animate attributeName="opacity" from="0" to="1" dur="0.25s" begin="{delay:.2f}s" fill="freeze" />
            <animateTransform attributeName="transform" type="translate" from="0, 5" to="0, 0" dur="0.25s" begin="{delay:.2f}s" fill="freeze" />
        </g>
        """
        rows_svg.append(row)
        
    svg_content = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{card_width}" height="{card_height}" viewBox="0 0 {card_width} {card_height}">
    <rect width="100%" height="100%" fill="#0d1117" rx="8" stroke="#30363d" stroke-width="1.5" />
    
    <!-- Terminal header dots -->
    <circle cx="25" cy="25" r="5" fill="#ff5f56"/>
    <circle cx="42" cy="25" r="5" fill="#ffbd2e"/>
    <circle cx="59" cy="25" r="5" fill="#27c93f"/>
    <text x="85" y="29" fill="#8b949e" font-family="monospace" font-size="12">neofetch --profile</text>
    <line x1="15" y1="45" x2="{card_width - 15}" y2="45" stroke="#21262d" stroke-width="1"/>
    
    {''.join(rows_svg)}
</svg>"""

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(svg_content)
    print(f"[+] Generated: {output_path}")

if __name__ == "__main__":
    generate_info_card()
