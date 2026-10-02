"""Generate animated SVGs for the GitHub profile README (pure CSS/SMIL, no JS)."""
from html import escape
from pathlib import Path

OUT = Path(__file__).parent
OUT.mkdir(parents=True, exist_ok=True)

MONO = "ui-monospace, SFMono-Regular, 'Cascadia Code', Consolas, Menlo, monospace"
SANS = "'Segoe UI', system-ui, -apple-system, Helvetica, Arial, sans-serif"
C = dict(bg="#0d1117", panel="#161b22", border="#30363d", text="#c9d1d9", dim="#8b949e",
         blue="#58a6ff", blue2="#1f6feb", green="#3fb950", purple="#a371f7",
         yellow="#d29922", pink="#f778ba", orange="#ffa657")


def pct(t, T):
    return f"{max(0.0, min(100.0, t / T * 100)):.3f}%"


# ───────────────────────────── 1. Zaude terminal ─────────────────────────────
def terminal():
    T = 20.0           # loop length (s)
    W, H = 880, 418
    x0, y0, lh = 34, 82, 27
    cw = 8.45          # approx monospace char width @14px
    css, body = [], []
    n = 0

    def seg_svg(segs):
        return "".join(f'<tspan fill="{col}">{escape(txt)}</tspan>' for txt, col in segs)

    def show(t_on, cls):
        css.append(
            f"@keyframes {cls}{{0%,{pct(t_on, T)}{{opacity:0}}"
            f"{pct(t_on + .18, T)},{pct(T - 1.4, T)}{{opacity:1}}"
            f"{pct(T - .9, T)},100%{{opacity:0}}}}"
            f".{cls}{{animation:{cls} {T}s linear infinite}}")

    def out(row, t, segs, x=None):
        nonlocal n
        n += 1
        cls = f"o{n}"
        show(t, cls)
        xx = x0 + 18 if x is None else x
        body.append(f'<text class="{cls}" x="{xx}" y="{y0 + row * lh}">{seg_svg(segs)}</text>')

    def cmd(row, t, text, t_next):
        """Prompt appears at t, text types out, cursor blinks until t_next."""
        nonlocal n
        n += 1
        g, cv, cu = f"c{n}", f"v{n}", f"u{n}"
        show(t, g)
        tx = x0 + 20
        y = y0 + row * lh
        typ0, typ1 = t + .5, t + .5 + len(text) * .055
        width = len(text) * cw + 14
        css.append(
            f"@keyframes {cv}{{0%,{pct(typ0, T)}{{transform:translateX(0);animation-timing-function:steps({len(text)},end)}}"
            f"{pct(typ1, T)},{pct(T - .3, T)}{{transform:translateX({width:.1f}px)}}100%{{transform:translateX(0)}}}}"
            f".{cv}{{animation:{cv} {T}s linear infinite}}")
        css.append(
            f"@keyframes {cu}{{0%,{pct(t, T)}{{opacity:0}}{pct(t + .01, T)},{pct(t_next, T)}{{opacity:1}}"
            f"{pct(t_next + .01, T)},100%{{opacity:0}}}}"
            f".{cu}{{animation:{cu} {T}s linear infinite}}")
        body.append(
            f'<g class="{g}"><text x="{x0}" y="{y}"><tspan fill="{C["green"]}">❯</tspan></text>'
            f'<text x="{tx}" y="{y}" fill="#ffffff">{escape(text)}</text>'
            f'<g class="{cv}"><rect x="{tx - 2}" y="{y - 16}" width="{W}" height="22" fill="{C["bg"]}"/>'
            f'<g class="{cu}"><rect class="blink" x="{tx - 1}" y="{y - 14}" width="8" height="18" fill="{C["blue"]}"/></g></g></g>')

    # script
    cmd(0, 0.4, "claude", 1.7)
    out(1, 1.5, [("zaude ", C["purple"]), ("▸ vault loaded · last session resumed · decisions intact", C["dim"])])
    cmd(2, 2.4, "add a CSV export of the employee directory for payroll", 6.2)
    out(3, 6.0, [("[route] ", C["yellow"]), ("intent=", C["dim"]), ("/zbuild", C["blue"]),
                 ("  mode=", C["dim"]), ("propose", C["orange"]), ("  → plan · design · build", C["dim"])])
    stages = [("plan     ", 6.9, [("✓ ", C["green"]), ("ordered plan recorded", C["text"])]),
              ("design   ", 7.6, [("✓ ", C["green"]), ("decision logged to vault", C["text"])]),
              ("implement", 8.3, [("✓ ", C["green"]), ("agents wrote the change", C["text"])]),
              ("test     ", 9.0, [("✓ ", C["green"]), ("exit=0 ", C["green"]), ("(real run, kernel-attested)", C["dim"])])]
    row = 4
    for label, t, res in stages:
        out(row, t, [("▸ ", C["blue"]), (label, C["text"])])
        out(row, t + .45, res, x=x0 + 18 + 12 * cw)
        row += 1
    # review panel: seats light up one by one
    out(row, 9.8, [("▸ ", C["blue"]), ("review   ", C["text"])])
    seats = [("claude", C["orange"]), ("codex", C["text"]), ("opencode", C["blue"]),
             ("kimi", C["purple"]), ("glm", C["pink"])]
    sx = x0 + 18 + 12 * cw
    for i, (name, col) in enumerate(seats):
        out(row, 10.2 + i * .35, [(name, col), (" ✓", C["green"])], x=sx)
        sx += (len(name) + 3.4) * cw
    out(row, 12.1, [("0C · 0H", C["green"])], x=sx + 4)
    row += 1
    out(row, 12.6, [("▸ ", C["blue"]), ("verify   ", C["text"])])
    out(row, 13.05, [("✓ ", C["green"]), ("live end-user check passed", C["text"])], x=x0 + 18 + 12 * cw)
    row += 1
    cmd(row, 13.7, "ship it", 15.4)
    row += 1
    n += 1
    show(15.3, f"o{n}")
    body.append(
        f'<g class="o{n}"><rect class="glow" x="{x0 + 12}" y="{y0 + row * lh - 19}" rx="6" width="590" height="27" '
        f'fill="{C["green"]}" fill-opacity=".12" stroke="{C["green"]}" stroke-opacity=".55"/>'
        f'<text x="{x0 + 24}" y="{y0 + row * lh}"><tspan fill="{C["green"]}" font-weight="700">✓ RELEASED</tspan>'
        f'<tspan fill="{C["text"]}">  signed into the trace · </tspan><tspan fill="{C["green"]}">tier-4: done-with-evidence</tspan></text></g>')

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="Animated Zaude session: a plain-language request routed through plan, build, test, a 5-model review panel, verification and a signed release">
<defs>
<linearGradient id="bd" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{C["blue2"]}"/><stop offset=".5" stop-color="{C["purple"]}"/><stop offset="1" stop-color="{C["blue"]}"/></linearGradient>
<clipPath id="clip"><rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="12"/></clipPath>
</defs>
<style>
text{{font-family:{MONO};font-size:14px;white-space:pre}}
.title{{font-family:{SANS};font-size:13px;fill:{C["dim"]}}}
.blink{{animation:blink 1s steps(1) infinite}}@keyframes blink{{50%{{opacity:0}}}}
.glow{{animation:glow 2s ease-in-out infinite}}@keyframes glow{{50%{{fill-opacity:.24;stroke-opacity:1}}}}
.edge{{animation:edge 6s linear infinite}}@keyframes edge{{to{{stroke-dashoffset:-400}}}}
{"".join(css)}
</style>
<g clip-path="url(#clip)">
<rect width="{W}" height="{H}" fill="{C["bg"]}"/>
<rect width="{W}" height="40" fill="{C["panel"]}"/>
<line x1="0" y1="40" x2="{W}" y2="40" stroke="{C["border"]}"/>
<circle cx="24" cy="20" r="6" fill="#ff5f57"/><circle cx="44" cy="20" r="6" fill="#febc2e"/><circle cx="64" cy="20" r="6" fill="#28c840"/>
<text class="title" x="{W / 2}" y="25" text-anchor="middle">zaude — claude code · ~/my-app</text>
{"".join(body)}
</g>
<rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="12" fill="none" stroke="{C["border"]}"/>
<rect class="edge" x="1" y="1" width="{W - 2}" height="{H - 2}" rx="12" fill="none" stroke="url(#bd)" stroke-width="2" stroke-dasharray="120 280" stroke-opacity=".9"/>
</svg>'''
    (OUT / "zaude-terminal.svg").write_text(svg, encoding="utf-8")


# ───────────────────────────── 2. Shipping pipeline ─────────────────────────────
def pipeline():
    W, H, T = 880, 205, 6.0
    xs = [100, 270, 440, 610, 780]
    cy = 78
    nodes = [("01", "DESIGN", "whole system first", C["blue"]),
             ("02", "BUILD", "agents implement", C["purple"]),
             ("03", "REVIEW", "5 models · 0C / 0H", C["orange"]),
             ("04", "VERIFY", "real exit + live check", C["pink"]),
             ("05", "SHIP", "signed · with evidence", C["green"])]
    sx, ex = 30, 850
    path = f"M{sx},{cy} L{ex},{cy}"
    parts = []
    for i, (num, title, sub, col) in enumerate(nodes):
        x = xs[i]
        delay = (x - sx) / (ex - sx) * T
        parts.append(f'''
<g>
  <circle cx="{x}" cy="{cy}" r="34" fill="none" stroke="{col}" stroke-width="2" class="ring" style="animation-delay:{delay:.2f}s;transform-origin:{x}px {cy}px"/>
  <circle cx="{x}" cy="{cy}" r="34" fill="{C["panel"]}" stroke="{col}" stroke-width="2"/>
  <circle cx="{x}" cy="{cy}" r="34" fill="{col}" class="lit" style="animation-delay:{delay:.2f}s"/>
  <text x="{x}" y="{cy + 7}" text-anchor="middle" class="num" fill="{col}">{num}</text>
  <text x="{x}" y="{cy + 66}" text-anchor="middle" class="t">{title}</text>
  <text x="{x}" y="{cy + 88}" text-anchor="middle" class="s">{escape(sub)}</text>
</g>''')
    # review satellites (5 models)
    rx = xs[2]
    sats = "".join(
        f'<circle cx="{rx + 48}" cy="{cy}" r="4" fill="{c}" transform="rotate({k * 72} {rx} {cy})"/>'
        for k, c in enumerate([C["orange"], C["text"], C["blue"], C["purple"], C["pink"]]))
    sat_g = (f'<g>{sats}<animateTransform attributeName="transform" type="rotate" '
             f'from="0 {rx} {cy}" to="360 {rx} {cy}" dur="8s" repeatCount="indefinite"/></g>')
    trail = "".join(
        f'<circle r="{r}" fill="{C["blue"]}" opacity="{o}"><animateMotion dur="{T}s" begin="-{d}s" repeatCount="indefinite" path="{path}" keyPoints="0;1" keyTimes="0;1" calcMode="linear"/></circle>'
        for r, o, d in [(7, 1, 0), (5, .55, .09), (3.5, .3, .18)])
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="How I ship: design, build, 5-model review, verify, ship">
<defs>
<linearGradient id="ln" gradientUnits="userSpaceOnUse" x1="30" y1="0" x2="850" y2="0"><stop offset="0" stop-color="{C["blue"]}"/><stop offset=".5" stop-color="{C["orange"]}"/><stop offset="1" stop-color="{C["green"]}"/></linearGradient>
<filter id="blur"><feGaussianBlur stdDeviation="4"/></filter>
</defs>
<style>
.t{{font-family:{SANS};font-size:15px;font-weight:700;letter-spacing:2px;fill:#ffffff}}
.s{{font-family:{SANS};font-size:12.5px;fill:{C["dim"]}}}
.num{{font-family:{MONO};font-size:20px;font-weight:700}}
.ring{{opacity:0;animation:ring {T}s ease-out infinite}}
@keyframes ring{{0%{{opacity:.9;transform:scale(1)}}22%{{opacity:0;transform:scale(1.45)}}100%{{opacity:0}}}}
.lit{{opacity:0;animation:lit {T}s ease-out infinite}}
@keyframes lit{{0%{{opacity:.35}}25%{{opacity:.06}}100%{{opacity:.06}}}}
.flow{{stroke-dasharray:6 10;animation:flow 1.2s linear infinite}}@keyframes flow{{to{{stroke-dashoffset:-16}}}}
</style>
<rect width="{W}" height="{H}" rx="14" fill="{C["bg"]}"/>
<rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="14" fill="none" stroke="{C["border"]}"/>
<path d="{path}" stroke="url(#ln)" stroke-width="3" opacity=".35"/>
<path d="{path}" stroke="url(#ln)" stroke-width="2" class="flow"/>
<g filter="url(#blur)">{trail}</g>
{trail}
{"".join(parts)}
{sat_g}
</svg>'''
    (OUT / "pipeline.svg").write_text(svg, encoding="utf-8")


# ───────────────────────────── 3. UltaHost stat tiles ─────────────────────────────
def ultahost():
    W, H = 880, 150
    tiles = [("1,750+", "commits", "across the Ulta-Host org"),
             ("23", "repositories", "products & internal tools"),
             ("6,085", "CI tests", "in one grouped lane"),
             ("129", "API operations", "OpenAPI with drift gates")]
    tw, gap = 205, 20
    parts = []
    for i, (big, label, sub) in enumerate(tiles):
        x = i * (tw + gap)
        d = .25 + i * .25
        parts.append(f'''
<g class="tile" style="animation-delay:{d:.2f}s">
  <rect x="{x + .5}" y=".5" width="{tw - 1}" height="{H - 1}" rx="12" fill="{C["panel"]}" stroke="{C["border"]}"/>
  <rect x="{x + 1}" y="1" width="{tw - 2}" height="3" rx="1.5" fill="url(#pu)" class="bar"/>
  <text x="{x + 20}" y="66" class="big">{escape(big)}</text>
  <text x="{x + 20}" y="96" class="lab">{escape(label)}</text>
  <text x="{x + 20}" y="120" class="sub">{escape(sub)}</text>
  <circle cx="{x + tw - 24}" cy="28" r="5" fill="{C["purple"]}" class="dot" style="animation-delay:{d:.2f}s"/>
</g>''')
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="UltaHost footprint: 1,750+ commits, 23 repositories, 6,085 CI tests, 129 API operations">
<defs>
<linearGradient id="pu" x1="0" x2="1"><stop offset="0" stop-color="#7c3aed"/><stop offset=".5" stop-color="{C["purple"]}"/><stop offset="1" stop-color="{C["blue"]}"/>
<animateTransform attributeName="gradientTransform" type="translate" values="-1 0;1 0" dur="3s" repeatCount="indefinite"/></linearGradient>
<linearGradient id="tx" x1="0" x2="1"><stop offset="0" stop-color="#ffffff"/><stop offset="1" stop-color="#d2b8ff"/></linearGradient>
</defs>
<style>
.big{{font-family:{SANS};font-size:38px;font-weight:800;fill:url(#tx)}}
.lab{{font-family:{SANS};font-size:15px;font-weight:600;fill:{C["purple"]};letter-spacing:.5px}}
.sub{{font-family:{SANS};font-size:12.5px;fill:{C["dim"]}}}
.tile{{opacity:0;animation:up .7s cubic-bezier(.2,.8,.2,1) forwards}}
@keyframes up{{from{{opacity:0;transform:translateY(14px)}}to{{opacity:1;transform:translateY(0)}}}}
.dot{{animation:pulse 2.4s ease-in-out infinite}}@keyframes pulse{{50%{{opacity:.25}}}}
</style>
{"".join(parts)}
</svg>'''
    (OUT / "ultahost-stats.svg").write_text(svg, encoding="utf-8")


# ───────────────────────────── 4. Divider ─────────────────────────────
def divider():
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="1000" height="14" viewBox="0 0 1000 14" preserveAspectRatio="none" role="img" aria-label="">
<defs>
<linearGradient id="g" x1="0" x2="1"><stop offset="0" stop-color="{C["blue2"]}" stop-opacity="0"/><stop offset=".5" stop-color="{C["blue"]}"/><stop offset="1" stop-color="{C["purple"]}" stop-opacity="0"/></linearGradient>
<radialGradient id="r"><stop offset="0" stop-color="#ffffff"/><stop offset=".4" stop-color="{C["blue"]}"/><stop offset="1" stop-color="{C["blue"]}" stop-opacity="0"/></radialGradient>
</defs>
<rect x="0" y="6" width="1000" height="2" fill="url(#g)"/>
<ellipse cy="7" rx="60" ry="6" fill="url(#r)"><animate attributeName="cx" values="-60;1060" dur="4s" repeatCount="indefinite"/></ellipse>
</svg>'''
    (OUT / "divider.svg").write_text(svg, encoding="utf-8")


