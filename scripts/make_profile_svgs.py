"""Generate the animated SVG cards for the profile README.

Edit the data at the top of this file, then run:  python scripts/make_profile_svgs.py
Writes assets/hero.svg, assets/stack.svg, assets/project-*.svg and profile-card.svg.
The languages card is separate (scripts/make_languages_svg.py) because it needs the GitHub API.
"""
import os
from html import escape

OUT = "assets"

NAME = "Mir Mohammad Sajedul Islam"
TAGLINE = "CSE student at BRAC University. Data Specialist Intern at DataSynthis."
MISSION = "I build AI that runs on cheap hardware, from quantization down to Verilog."

NEOFETCH = [
    ("USER", "sajedulislam5840"),
    ("HOST", "BRAC University, B.Sc. CSE"),
    ("ROLE", "Data Specialist Intern, DataSynthis"),
    ("NOW", "riscv-edge-ai: cycle counts on Spike"),
    ("STACK", "C++17, Python, Verilog, TypeScript"),
    ("DATA", "SQL, PostgreSQL, NumPy, pandas"),
    ("FOCUS", "Edge AI, hardware acceleration"),
    ("LOCATION", "Dhaka, Bangladesh"),
]

STACK = [
    ("Languages", ["C++17", "Python", "Java", "Verilog", "SQL", "TypeScript", "JavaScript", "HTML/CSS"]),
    ("AI and data", ["NumPy", "pandas", "scikit-learn", "OpenCV", "PostgreSQL", "Jupyter"]),
    ("Web", ["Next.js", "React", "FastAPI", "Tailwind CSS"]),
    ("Hardware and tools", ["RISC-V", "Yosys", "Git", "GitHub Actions", "Docker", "Linux", "VS Code"]),
]

PROJECTS = [
    {
        "slug": "riscv", "repo": "riscv-edge-ai",
        "title": "riscv-edge-ai",
        "lines": ["Integer-only neural network engine,", "plus a 4-lane INT8 multiply-accumulate", "instruction designed in Verilog."],
        "stats": ["98.21% INT8 on MNIST (FP32 98.23%)", "25,088 RTL vectors, 0 mismatches"],
        "tags": ["C++17", "Verilog", "Python"],
        "accent": "#38bdf8",
    },
    {
        "slug": "azs", "repo": "AZS-The-Catalyst",
        "title": "AZS: The Catalyst",
        "lines": ["Learning platform for a physics and", "chemistry coaching batch: lectures,", "notes, an AI tutor and fee tracking."],
        "stats": ["Live, in a pilot with real students", "Role-based access control"],
        "tags": ["Next.js", "FastAPI", "PostgreSQL"],
        "accent": "#3fb950",
    },
    {
        "slug": "cse422", "repo": "CSE422",
        "title": "Career switch prediction",
        "lines": ["Machine learning study on 5,000", "candidate profiles, with class", "imbalance handled explicitly."],
        "stats": ["3 models, stratified 5-fold CV", "Best ROC-AUC 0.716"],
        "tags": ["Python", "scikit-learn", "pandas"],
        "accent": "#d29922",
    },
]

# ----------------------------------------------------------------------------- shared style
BG, BORDER, RULE = "#0d1117", "#30363d", "#21262d"
TEXT, MUTED, BLUE = "#c9d1d9", "#8b949e", "#58a6ff"
CYAN, AMBER = "#38bdf8", "#f5a524"
MONO = "ui-monospace, SFMono-Regular, 'SF Mono', Menlo, Consolas, 'Liberation Mono', monospace"
SANS = "-apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif"
REDUCED = "@media (prefers-reduced-motion: reduce){*{animation:none!important}}"


def window(w, h, title, body, style=""):
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="{escape(title)}">
<style>{style}{REDUCED}</style>
<rect x="0.75" y="0.75" width="{w - 1.5}" height="{h - 1.5}" rx="8" fill="{BG}" stroke="{BORDER}" stroke-width="1.5"/>
<circle cx="25" cy="22" r="5" fill="#ff5f56"/><circle cx="42" cy="22" r="5" fill="#ffbd2e"/><circle cx="59" cy="22" r="5" fill="#27c93f"/>
<text x="85" y="26" fill="{MUTED}" font-family="{MONO}" font-size="12">{escape(title)}</text>
<line x1="15" y1="42" x2="{w - 15}" y2="42" stroke="{RULE}"/>
{body}
</svg>
"""


def write(path, svg):
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(svg)
    print("wrote", path)


# ----------------------------------------------------------------------------- hero
def mini_datapath(x0, y0, scale=1.0, accent=CYAN):
    """Four lanes multiplied, summed, accumulated. Dashed wires flow, nodes pulse."""
    s = scale
    lanes = [y0 + i * 34 * s for i in range(4)]
    parts = []
    for i, y in enumerate(lanes):
        parts.append(f'<rect x="{x0:.1f}" y="{y - 10 * s:.1f}" width="{26 * s:.1f}" height="{20 * s:.1f}" rx="3" fill="{RULE}"/>')
        parts.append(f'<text x="{x0 + 13 * s:.1f}" y="{y + 4 * s:.1f}" fill="{TEXT}" font-family="{MONO}" font-size="{10 * s:.1f}" text-anchor="middle">a{i}</text>')
        parts.append(f'<path class="w" d="M{x0 + 26 * s:.1f} {y:.1f} H{x0 + 58 * s:.1f}"/>')
        parts.append(f'<circle class="n" cx="{x0 + 70 * s:.1f}" cy="{y:.1f}" r="{12 * s:.1f}"/>')
        parts.append(f'<text x="{x0 + 70 * s:.1f}" y="{y + 4 * s:.1f}" fill="#f0f6fc" font-family="{MONO}" font-size="{12 * s:.1f}" text-anchor="middle">×</text>')
    mids = [(lanes[0] + lanes[1]) / 2, (lanes[2] + lanes[3]) / 2]
    for k, m in enumerate(mids):
        for y in lanes[2 * k: 2 * k + 2]:
            parts.append(f'<path class="w" d="M{x0 + 82 * s:.1f} {y:.1f} C{x0 + 100 * s:.1f} {y:.1f} {x0 + 100 * s:.1f} {m:.1f} {x0 + 118 * s:.1f} {m:.1f}"/>')
        parts.append(f'<circle class="n" cx="{x0 + 130 * s:.1f}" cy="{m:.1f}" r="{12 * s:.1f}"/>')
        parts.append(f'<text x="{x0 + 130 * s:.1f}" y="{m + 4 * s:.1f}" fill="#f0f6fc" font-family="{MONO}" font-size="{12 * s:.1f}" text-anchor="middle">+</text>')
    c = (mids[0] + mids[1]) / 2
    for m in mids:
        parts.append(f'<path class="w" d="M{x0 + 142 * s:.1f} {m:.1f} C{x0 + 160 * s:.1f} {m:.1f} {x0 + 160 * s:.1f} {c:.1f} {x0 + 178 * s:.1f} {c:.1f}"/>')
    parts.append(f'<circle class="n acc" cx="{x0 + 190 * s:.1f}" cy="{c:.1f}" r="{12 * s:.1f}"/>')
    parts.append(f'<text x="{x0 + 190 * s:.1f}" y="{c + 4 * s:.1f}" fill="#f0f6fc" font-family="{MONO}" font-size="{12 * s:.1f}" text-anchor="middle">+</text>')
    parts.append(f'<path class="w wa" d="M{x0 + 202 * s:.1f} {c:.1f} H{x0 + 226 * s:.1f}"/>')
    parts.append(f'<rect x="{x0 + 226 * s:.1f}" y="{c - 11 * s:.1f}" width="{26 * s:.1f}" height="{22 * s:.1f}" rx="3" fill="{RULE}"/>')
    parts.append(f'<text x="{x0 + 239 * s:.1f}" y="{c + 4 * s:.1f}" fill="{TEXT}" font-family="{MONO}" font-size="{10 * s:.1f}" text-anchor="middle">rd</text>')
    style = (f".w{{fill:none;stroke:{accent};stroke-width:1.6;stroke-dasharray:5 6;animation:flow 1.1s linear infinite}}"
             f".wa{{stroke:{AMBER}}}.n{{fill:#0b3a53;stroke:{accent};stroke-width:1.3;animation:pulse 2.2s ease-in-out infinite}}"
             f".acc{{fill:#3b2a08;stroke:{AMBER}}}"
             "@keyframes flow{to{stroke-dashoffset:-22}}@keyframes pulse{0%,100%{opacity:.6}50%{opacity:1}}")
    return "\n".join(parts), style


def hero():
    w, h = 860, 230
    name_px = 30
    name_w = int(len(NAME) * name_px * 0.6) + 10
    dp, dp_style = mini_datapath(612, 96, 0.88)
    style = (
        f"@keyframes type{{from{{width:0}}to{{width:{name_w}px}}}}"
        "@keyframes blink{50%{opacity:0}}"
        "@keyframes fade{from{opacity:0}to{opacity:1}}"
        f".type{{animation:type 1.6s steps({len(NAME)}) .3s both}}"
        f"@keyframes curmove{{from{{transform:translateX(-{name_w}px)}}to{{transform:translateX(0)}}}}"
        f".cur{{animation:curmove 1.6s steps({len(NAME)}) .3s both,blink 1s step-end 1.9s infinite}}"
        ".r{animation:fade .6s ease-out both}"
        ".d1{animation-delay:2.0s}.d2{animation-delay:2.4s}.d3{animation-delay:2.8s}"
        + dp_style
    )
    body = f"""
<clipPath id="tc"><rect class="type" x="34" y="66" height="44" width="{name_w}"/></clipPath>
<text x="34" y="98" fill="#f0f6fc" font-family="{MONO}" font-size="{name_px}" font-weight="700" clip-path="url(#tc)">{escape(NAME)}</text>
<rect class="cur" x="{34 + name_w + 2}" y="74" width="12" height="30" fill="{CYAN}"/>
<text class="r d1" x="34" y="136" fill="{TEXT}" font-family="{SANS}" font-size="15">{escape(TAGLINE)}</text>
<text class="r d2" x="34" y="162" fill="{MUTED}" font-family="{SANS}" font-size="15">{escape(MISSION)}</text>
<text class="r d3" x="34" y="202" fill="{MUTED}" font-family="{MONO}" font-size="12"><tspan fill="{CYAN}">$</tspan> currently: integer-only inference on a custom RISC-V instruction</text>
<g class="r d1">{dp}</g>
"""
    write(f"{OUT}/hero.svg", window(w, h, "sajedul@github ~ $ ./hello.sh", body, style))


# ----------------------------------------------------------------------------- stack
def text_w(s, px):
    return len(s) * px * 0.6


def stack():
    w = 860
    x0, y = 34, 74
    rows = []
    delay = 0.2
    for label, items in STACK:
        rows.append(f'<text x="{x0}" y="{y}" fill="{BLUE}" font-family="{MONO}" font-size="13" font-weight="bold">{escape(label)}</text>')
        y += 14
        x = x0
        for it in items:
            cw = text_w(it, 13) + 24
            if x + cw > w - 34:
                x = x0
                y += 38
            rows.append(
                f'<g class="r" style="animation-delay:{delay:.2f}s">'
                f'<rect x="{x:.0f}" y="{y}" width="{cw:.0f}" height="28" rx="6" fill="#161b22" stroke="{BORDER}"/>'
                f'<text x="{x + cw / 2:.1f}" y="{y + 18.5}" fill="{TEXT}" font-family="{MONO}" font-size="13" text-anchor="middle">{escape(it)}</text></g>')
            x += cw + 8
            delay += 0.05
        y += 62
    h = y - 18
    style = "@keyframes fade{from{opacity:0}to{opacity:1}}.r{animation:fade .45s ease-out both}"
    write(f"{OUT}/stack.svg", window(w, h, "sajedul@github ~ $ ls ~/stack", "\n".join(rows), style))


# ----------------------------------------------------------------------------- project cards
def project(p):
    w, h = 280, 250
    acc = p["accent"]
    body = [f'<text x="20" y="72" fill="#f0f6fc" font-family="{SANS}" font-size="17" font-weight="600">{escape(p["title"])}</text>']
    for i, line in enumerate(p["lines"]):
        body.append(f'<text x="20" y="{98 + i * 19}" fill="{TEXT}" font-family="{SANS}" font-size="13">{escape(line)}</text>')
    for i, st in enumerate(p["stats"]):
        yy = 168 + i * 19
        body.append(f'<g class="r" style="animation-delay:{0.4 + i * 0.25:.2f}s"><rect x="20" y="{yy - 9}" width="6" height="6" rx="1" fill="{acc}"/>'
                    f'<text x="34" y="{yy}" fill="{MUTED}" font-family="{MONO}" font-size="11">{escape(st)}</text></g>')
    x = 20
    for t in p["tags"]:
        tw = text_w(t, 11) + 16
        body.append(f'<rect x="{x:.0f}" y="212" width="{tw:.0f}" height="22" rx="11" fill="none" stroke="{acc}" stroke-opacity=".6"/>'
                    f'<text x="{x + tw / 2:.1f}" y="227" fill="{acc}" font-family="{MONO}" font-size="11" text-anchor="middle">{escape(t)}</text>')
        x += tw + 6
    body.append(f'<rect class="bar" x="20" y="{h - 8}" width="{w - 40}" height="2" rx="1" fill="{acc}"/>')
    style = ("@keyframes fade{from{opacity:0}to{opacity:1}}.r{animation:fade .5s ease-out both}"
             f"@keyframes sweep{{from{{transform:scaleX(0)}}to{{transform:scaleX(1)}}}}"
             ".bar{transform-origin:20px 0;animation:sweep 1.2s ease-out .2s both}")
    write(f"{OUT}/project-{p['slug']}.svg", window(w, h, f"~/{p['repo']}", "\n".join(body), style))


# ----------------------------------------------------------------------------- neofetch card
def neofetch():
    w, h = 450, 380
    rows = []
    for i, (k, v) in enumerate(NEOFETCH):
        y = 80 + i * 35
        rows.append(f'<g class="r" style="animation-delay:{0.15 + i * 0.1:.2f}s">'
                    f'<text x="30" y="{y}" fill="{BLUE}" font-family="{MONO}" font-size="13" font-weight="bold">{k}:</text>'
                    f'<text x="122" y="{y}" fill="{TEXT}" font-family="{MONO}" font-size="13">{escape(v)}</text></g>')
    style = "@keyframes fade{from{opacity:0}to{opacity:1}}.r{animation:fade .25s ease-out both}"
    write("profile-card.svg", window(w, h, "sajedul@github ~ neofetch", "\n".join(rows), style))


if __name__ == "__main__":
    hero()
    stack()
    for p in PROJECTS:
        project(p)
    neofetch()
