"""Measure the languages in my public repositories and draw them as an animated SVG card.

Uses the GitHub API (the same numbers GitHub shows on each repository). Runs daily in
.github/workflows/update-profile-art.yml with the workflow's GITHUB_TOKEN.

  python scripts/make_languages_svg.py                  # live data from the API
  python scripts/make_languages_svg.py data/langs.json  # from a saved {"Language": bytes} file
"""
import json
import os
import sys
import urllib.request
from html import escape

USER = "sajedulislam5840"
SKIP_REPOS = {USER}                         # the profile repo itself
SKIP_LANGUAGES = {"Jupyter Notebook"}       # notebook bytes are mostly cell outputs
TOP = 6
COLORS = ["#38bdf8", "#f5a524", "#3fb950", "#a371f7", "#f778ba", "#d29922", "#8b949e"]
OUT = "assets/languages.svg"
MONO = "ui-monospace, SFMono-Regular, 'SF Mono', Menlo, Consolas, 'Liberation Mono', monospace"


def api(path):
    req = urllib.request.Request(f"https://api.github.com{path}", headers={"Accept": "application/vnd.github+json"})
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        req.add_header("Authorization", f"Bearer {token}")
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)


def fetch():
    totals, repos = {}, 0
    for repo in api(f"/users/{USER}/repos?per_page=100&type=owner"):
        if repo["fork"] or repo["name"] in SKIP_REPOS:
            continue
        repos += 1
        for lang, size in api(f"/repos/{USER}/{repo['name']}/languages").items():
            totals[lang] = totals.get(lang, 0) + size
    return totals, repos


def render(totals, repos):
    items = sorted(((k, v) for k, v in totals.items() if k not in SKIP_LANGUAGES), key=lambda kv: -kv[1])
    total = sum(v for _, v in items) or 1
    top = items[:TOP]
    rest = sum(v for _, v in items[TOP:])
    if rest:
        top.append(("Other", rest))

    w, h = 860, 200
    bar_x, bar_y, bar_w = 34, 74, w - 68
    parts, x = [], bar_x
    for i, (lang, size) in enumerate(top):
        seg = bar_w * size / total
        parts.append(f'<rect class="seg" style="animation-delay:{0.15 + i * 0.12:.2f}s" x="{x:.1f}" y="{bar_y}" '
                     f'width="{max(seg - 2, 1):.1f}" height="12" rx="2" fill="{COLORS[i % len(COLORS)]}"/>')
        x += seg
    cols = 4
    for i, (lang, size) in enumerate(top):
        cx = 34 + (i % cols) * 200
        cy = 122 + (i // cols) * 30
        parts.append(f'<g class="r" style="animation-delay:{0.5 + i * 0.08:.2f}s">'
                     f'<circle cx="{cx + 5}" cy="{cy - 4}" r="5" fill="{COLORS[i % len(COLORS)]}"/>'
                     f'<text x="{cx + 18}" y="{cy}" fill="#c9d1d9" font-family="{MONO}" font-size="13">{escape(lang)}</text>'
                     f'<text x="{cx + 170}" y="{cy}" fill="#8b949e" font-family="{MONO}" font-size="13" text-anchor="end">{100 * size / total:.1f}%</text></g>')
    title = f"sajedul@github ~ $ linguist --repos {repos}"
    style = ("@keyframes grow{from{transform:scaleX(0)}to{transform:scaleX(1)}}"
             ".seg{transform-box:fill-box;transform-origin:left;animation:grow .7s ease-out both}"
             "@keyframes fade{from{opacity:0}to{opacity:1}}.r{animation:fade .4s ease-out both}"
             "@media (prefers-reduced-motion: reduce){*{animation:none!important}}")
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="Languages in my public repositories">
<style>{style}</style>
<rect x="0.75" y="0.75" width="{w - 1.5}" height="{h - 1.5}" rx="8" fill="#0d1117" stroke="#30363d" stroke-width="1.5"/>
<circle cx="25" cy="22" r="5" fill="#ff5f56"/><circle cx="42" cy="22" r="5" fill="#ffbd2e"/><circle cx="59" cy="22" r="5" fill="#27c93f"/>
<text x="85" y="26" fill="#8b949e" font-family="{MONO}" font-size="12">{escape(title)}</text>
<line x1="15" y1="42" x2="{w - 15}" y2="42" stroke="#21262d"/>
{''.join(parts)}
<text x="34" y="{h - 16}" fill="#6e7681" font-family="{MONO}" font-size="11">Measured by GitHub from the code in my public repositories (notebooks excluded). Updated daily.</text>
</svg>
"""
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", encoding="utf-8", newline="\n") as f:
        f.write(svg)
    print("wrote", OUT, {k: round(100 * v / total, 1) for k, v in top})


if __name__ == "__main__":
    if len(sys.argv) > 1:
        data = json.load(open(sys.argv[1]))
        render(data["languages"], data.get("repos", 0))
    else:
        render(*fetch())
