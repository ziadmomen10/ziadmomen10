"""Profile visuals v2 — hero, about editor, cards, marquee, footer. Pure CSS/SMIL, no JS.

Run:  python assets/_generate.py   (v1 visuals)  then  python assets/_generate_v2.py
"""
import re
import textwrap
from html import escape
from pathlib import Path

from _generate import C, MONO, SANS, OUT, shadow, lift  # shared palette + fonts + light-theme lift

W = 880


def wrap(text, width_px, size, factor=0.47):
    return textwrap.wrap(text, max(8, int(width_px / (size * factor))))


def sweep_rect(x, y, w, h, rx, grad, delay=0.0, dur=6.0, width=1.6):
    """Light that travels around a card border."""
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="none" stroke="url(#{grad})" '
            f'stroke-width="{width}" pathLength="1000" stroke-dasharray="140 860" stroke-linecap="round">'
            f'<animate attributeName="stroke-dashoffset" from="0" to="-1000" dur="{dur}s" begin="{-delay:.2f}s" '
            f'repeatCount="indefinite"/></rect>')


def grads():
    return (f'<linearGradient id="gb" x1="0" x2="1" y1="0" y2="1"><stop offset="0" stop-color="{C["blue"]}"/>'
            f'<stop offset="1" stop-color="{C["purple"]}"/></linearGradient>'
            f'<linearGradient id="gp" x1="0" x2="1" y1="0" y2="1"><stop offset="0" stop-color="{C["violet"]}"/>'
            f'<stop offset="1" stop-color="{C["pink"]}"/></linearGradient>'
            f'<linearGradient id="gg" x1="0" x2="1" y1="0" y2="1"><stop offset="0" stop-color="{C["green"]}"/>'
            f'<stop offset="1" stop-color="{C["blue"]}"/></linearGradient>'
            f'<linearGradient id="go" x1="0" x2="1" y1="0" y2="1"><stop offset="0" stop-color="{C["orange"]}"/>'
            f'<stop offset="1" stop-color="{C["pink"]}"/></linearGradient>')


def save(name, svg):
    (OUT / name).write_text(svg, encoding="utf-8")


# ─────────────────────────────── HERO ───────────────────────────────
def hero():
    Wh, Hh = 1200, 400
    hz = 268  # horizon
    vx = Wh / 2
    grid = []
    for k in range(-14, 15):  # converging verticals
        grid.append(f'<line x1="{vx + k * 18}" y1="{hz}" x2="{vx + k * 150}" y2="{Hh}"/>')
    hl = []
    for k in range(9):  # horizontal lines that scroll toward the viewer
        hl.append(f'<line x1="0" x2="{Wh}" y1="{hz}" y2="{hz}">'
                  f'<animate attributeName="y1" values="{hz};{Hh}" keyTimes="0;1" keySplines=".55 0 1 .45" calcMode="spline" dur="4.5s" begin="{-k * .5:.2f}s" repeatCount="indefinite"/>'
                  f'<animate attributeName="y2" values="{hz};{Hh}" keyTimes="0;1" keySplines=".55 0 1 .45" calcMode="spline" dur="4.5s" begin="{-k * .5:.2f}s" repeatCount="indefinite"/>'
                  f'<animate attributeName="stroke-opacity" values="0;.9;.2" dur="4.5s" begin="{-k * .5:.2f}s" repeatCount="indefinite"/></line>')
    import random
    rnd = random.Random(7)
    parts = []
    for i in range(46):
        x, y = rnd.uniform(20, Wh - 20), rnd.uniform(14, hz - 10)
        r = rnd.choice([0.8, 1.1, 1.5, 2])
        d = rnd.uniform(2, 6)
        col = rnd.choice([C["blue"], C["glow"], C["purple"], C["glow"]])
        parts.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{r}" fill="{col}">'
                     f'<animate attributeName="opacity" values="0;1;0" dur="{d:.1f}s" begin="{-rnd.uniform(0, d):.1f}s" repeatCount="indefinite"/>'
                     f'<animate attributeName="cy" values="{y:.0f};{y - 18:.0f}" dur="{d * 2:.1f}s" repeatCount="indefinite"/></circle>')
    blobs = "".join(
        f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{col}" opacity=".55">'
        f'<animate attributeName="cx" values="{cx};{cx + dx};{cx}" dur="{d}s" repeatCount="indefinite"/>'
        f'<animate attributeName="cy" values="{cy};{cy + dy};{cy}" dur="{d * 1.3:.1f}s" repeatCount="indefinite"/></circle>'
        for cx, cy, r, col, dx, dy, d in [(260, 120, 170, C["blue2"], 120, 40, 14), (900, 110, 190, C["violet"], -140, 50, 17),
                                          (600, 260, 150, C["teal"], 80, -40, 12)])
    chips = [(t, c, len(t) * 8.6 + 44) for t, c in [("   shipping at UltaHost", C["green"]), ("Zaude™ · open source", C["blue"]), ("Egypt", C["purple"])]]
    total = sum(w for *_, w in chips) + 16 * (len(chips) - 1)
    cx = (Wh - total) / 2
    chip_svg = []
    for i, (label, col, w) in enumerate(chips):
        chip_svg.append(
            f'<g class="chip" style="animation-delay:{1.1 + i * .2:.1f}s">'
            f'<rect x="{cx}" y="236" width="{w}" height="34" rx="17" fill="{col}" fill-opacity=".1" stroke="{col}" stroke-opacity=".6"/>'
            f'<text x="{cx + w / 2}" y="258" text-anchor="middle" class="chipt" fill="{col}">{escape(label)}</text></g>')
        if i == 0:
            chip_svg.append(f'<circle cx="{cx + 24}" cy="253" r="4" fill="{C["green"]}"/><circle cx="{cx + 24}" cy="253" r="9" fill="none" stroke="{C["green"]}">'
                            f'<animate attributeName="r" values="5;13" dur="1.6s" repeatCount="indefinite"/>'
                            f'<animate attributeName="opacity" values=".9;0" dur="1.6s" repeatCount="indefinite"/></circle>')
        cx += w + 16
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{Wh}" height="{Hh}" viewBox="0 0 {Wh} {Hh}" role="img" aria-label="Ziad Momen — Director of Product and Engineering at UltaHost, Creator of Zaude">
<defs>
<clipPath id="cl"><rect width="{Wh}" height="{Hh}" rx="18"/></clipPath>
<filter id="blur" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="70"/></filter>
<filter id="glow" x="-20%" y="-50%" width="140%" height="200%"><feGaussianBlur stdDeviation="10" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
<linearGradient id="name" x1="0" x2="1" gradientUnits="objectBoundingBox">
<stop offset="0" stop-color="{C["title"]}"/><stop offset=".3" stop-color="{C["blue"]}"/><stop offset=".55" stop-color="{C["lilac"]}"/><stop offset=".8" stop-color="{C["blue"]}"/><stop offset="1" stop-color="{C["title"]}"/>
<animateTransform attributeName="gradientTransform" type="translate" values="-.5 0;.5 0;-.5 0" dur="8s" repeatCount="indefinite"/></linearGradient>
<linearGradient id="fade" x1="0" x2="0" y1="0" y2="1"><stop offset="0" stop-color="#000"/><stop offset=".25" stop-color="#fff"/></linearGradient>
<mask id="fm"><rect y="{hz}" width="{Wh}" height="{Hh - hz}" fill="url(#fade)"/></mask>
<linearGradient id="bd" x1="0" x2="1"><stop offset="0" stop-color="{C["blue"]}"/><stop offset="1" stop-color="{C["purple"]}"/></linearGradient>
</defs>
<style>
.name{{font-family:{SANS};font-size:92px;font-weight:800;letter-spacing:-1px}}
.sub{{font-family:{SANS};font-size:17px;font-weight:600;letter-spacing:5px;fill:{C["dim"]}}}
.chipt{{font-family:{SANS};font-size:16px;font-weight:600;white-space:pre}}
.in{{opacity:0;animation:in 1s cubic-bezier(.2,.8,.2,1) forwards}}
.chip{{opacity:0;animation:in .8s cubic-bezier(.2,.8,.2,1) forwards}}
@keyframes in{{from{{opacity:0;transform:translateY(16px)}}to{{opacity:1;transform:none}}}}
</style>
<g clip-path="url(#cl)">
<rect width="{Wh}" height="{Hh}" fill="{C["hero_bg"]}"/>
<g filter="url(#blur)">{blobs}</g>
<g mask="url(#fm)" stroke="{C["blue"]}" stroke-opacity=".35" stroke-width="1">{"".join(grid)}</g>
<g mask="url(#fm)" stroke="{C["blue"]}" stroke-width="1.2">{"".join(hl)}</g>
<line x1="0" x2="{Wh}" y1="{hz}" y2="{hz}" stroke="{C["blue"]}" stroke-opacity=".6"/>
{"".join(parts)}
<g fill="none" stroke-width="1" opacity=".5">
<ellipse cx="110" cy="130" rx="70" ry="70" stroke="{C["blue"]}" stroke-dasharray="4 10"><animateTransform attributeName="transform" type="rotate" from="0 110 130" to="360 110 130" dur="30s" repeatCount="indefinite"/></ellipse>
<ellipse cx="1090" cy="130" rx="56" ry="56" stroke="{C["purple"]}" stroke-dasharray="2 8"><animateTransform attributeName="transform" type="rotate" from="360 1090 130" to="0 1090 130" dur="24s" repeatCount="indefinite"/></ellipse>
<circle cx="180" cy="130" r="4" fill="{C["blue"]}" stroke="none"><animateTransform attributeName="transform" type="rotate" from="0 110 130" to="360 110 130" dur="10s" repeatCount="indefinite"/></circle>
<circle cx="1146" cy="130" r="3.5" fill="{C["purple"]}" stroke="none"><animateTransform attributeName="transform" type="rotate" from="360 1090 130" to="0 1090 130" dur="8s" repeatCount="indefinite"/></circle>
</g>
<g class="in" style="animation-delay:.2s"><text x="{Wh / 2}" y="140" text-anchor="middle" class="name" fill="url(#name)"{' filter="url(#glow)"' if C["mode"] == "dark" else ''}>Ziad Momen</text></g>
<g class="in" style="animation-delay:.7s"><text x="{Wh / 2}" y="196" text-anchor="middle" class="sub">DIRECTOR OF PRODUCT &amp; ENGINEERING · ULTAHOST · CREATOR OF ZAUDE™</text></g>
{"".join(chip_svg)}
</g>
<rect x="1" y="1" width="{Wh - 2}" height="{Hh - 2}" rx="18" fill="none" stroke="{C["border"]}"/>
{sweep_rect(1, 1, Wh - 2, Hh - 2, 18, "bd", dur=9, width=2)}
</svg>'''
    save("hero.svg", svg)


# ─────────────────────────────── ABOUT (code editor) ───────────────────────────────
def about():
    K, S, P, F, D, N = "#ff7b72", "#a5d6ff", "#79c0ff", "#d2a8ff", C["dim"], C["text"]
    L = [
        [("const ", K), ("ziad", F), (" = {", N)],
        [("  role", P), (":     ", N), ('"Director of Product & Engineering"', S), (",", N)],
        [("  company", P), (":  ", N), ('"UltaHost"', S), (",", N), ("          // org admin", D)],
        [("  location", P), (": ", N), ('"Egypt"', S), (",", N)],
        [("  shipping", P), (": [", N), ('"Zaude™"', S), (", ", N), ('"AI Hosting Assistant"', S), (", ", N), ('"Supabase Platform"', S), (", ", N), ('"CommunityOS"', S), ("],", N)],
        [("  inProd", P), (":   [", N), ('"AtomOS"', S), (", ", N), ('"AI Product UI"', S), ("],", N)],
        [("  stack", P), (": {", N)],
        [("    web", P), (":   [", N), ('"React 19"', S), (", ", N), ('"Next.js"', S), (", ", N), ('"Vite"', S), (", ", N), ('"Tailwind"', S), (", ", N), ('"Expo"', S), ("],", N)],
        [("    api", P), (":   [", N), ('"NestJS"', S), (", ", N), ('"Hono"', S), (", ", N), ('"Bun"', S), (", ", N), ('"Prisma"', S), (", ", N), ('"Drizzle"', S), ("],", N)],
        [("    data", P), (":  [", N), ('"PostgreSQL"', S), (", ", N), ('"Supabase"', S), (", ", N), ('"Redis"', S), (", ", N), ('"MongoDB"', S), ("],", N)],
        [("    infra", P), (": [", N), ('"Docker"', S), (", ", N), ('"GitHub Actions"', S), (", ", N), ('"Caddy"', S), (", ", N), ('"Proxmox"', S), ("],", N)],
        [("    ai", P), (":    [", N), ('"Claude API"', S), (", ", N), ('"Claude Code"', S), (", ", N), ('"5-model review"', S), ("],", N)],
        [("  },", N)],
        [("  done", P), (": () ", N), ("=>", K), (" greenBuild ", N), ("&&", K), (" zeroCritical ", N), ("&&", K), (" liveVerified", N), (",", N)],
        [("} ", N), ("satisfies ", K), ("Engineer", F), (";", N)],
    ]
    T = 16.0
    x0, y0, lh = 74, 92, 24
    css, rows = [], []
    for i, segs in enumerate(L):
        t = .3 + i * .28
        cls = f"l{i}"
        css.append(f"@keyframes {cls}{{0%,{t / T * 100:.2f}%{{opacity:0;transform:translateX(-8px)}}"
                   f"{(t + .3) / T * 100:.2f}%,{(T - 1.2) / T * 100:.2f}%{{opacity:1;transform:none}}"
                   f"{(T - .6) / T * 100:.2f}%,100%{{opacity:0}}}}.{cls}{{animation:{cls} {T}s ease-out infinite}}")
        y = y0 + i * lh
        rows.append(f'<text x="40" y="{y}" class="ln" text-anchor="end">{i + 1}</text>'
                    f'<text class="{cls}" x="{x0}" y="{y}">'
                    + "".join(f'<tspan fill="{c}">{escape(t_)}</tspan>' for t_, c in segs) + "</text>")
    n = len(L)
    Hh = y0 + n * lh + 24
    cur_t = .3 + n * .28
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{Hh}" viewBox="0 0 {W} {Hh}" role="img" aria-label="ziad.ts — role: Director of Product and Engineering at UltaHost, Egypt. Shipping Zaude, AI Hosting Assistant, Supabase Platform, CommunityOS. Stack: React, Next.js, NestJS, Hono, Bun, PostgreSQL, Supabase, Docker, Claude.">
<defs>{grads()}<clipPath id="c"><rect width="{W}" height="{Hh}" rx="12"/></clipPath></defs>
<style>
text{{font-family:{MONO};font-size:13.5px;white-space:pre}}
.ln{{fill:#484f58}}
.tab{{font-family:{SANS};font-size:13px}}
.cur{{animation:cur 1s steps(1) infinite}}@keyframes cur{{50%{{opacity:0}}}}
{"".join(css)}
</style>
<g clip-path="url(#c)">
<rect width="{W}" height="{Hh}" fill="{C["bg"]}"/>
<rect width="{W}" height="42" fill="{C["panel"]}"/>
<circle cx="22" cy="21" r="6" fill="#ff5f57"/><circle cx="42" cy="21" r="6" fill="#febc2e"/><circle cx="62" cy="21" r="6" fill="#28c840"/>
<rect x="90" y="8" width="118" height="34" rx="6" fill="{C["bg"]}"/>
<rect x="90" y="8" width="118" height="2" fill="url(#gb)"/>
<text x="112" y="30" class="tab" fill="#ffffff">◆ ziad.ts</text>
<text x="232" y="30" class="tab" fill="{C["dim"]}">stack.json</text>
<text x="330" y="30" class="tab" fill="{C["dim"]}">principles.md</text>
<line x1="56" y1="42" x2="56" y2="{Hh}" stroke="{C["border"]}"/>
{"".join(rows)}
<rect class="cur" x="{x0 + 1}" y="{y0 + n * lh - 15}" width="8" height="17" fill="{C["blue"]}" opacity="0">
<animate attributeName="opacity" values="0;1" keyTimes="0;1" dur="{cur_t}s" fill="freeze"/></rect>
</g>
<rect x=".5" y=".5" width="{W - 1}" height="{Hh - 1}" rx="12" fill="none" stroke="{C["border"]}"/>
{sweep_rect(.5, .5, W - 1, Hh - 1, 12, "gb", dur=8)}
</svg>'''
    save("about.svg", svg)


# ─────────────────────────────── generic card grid ───────────────────────────────
def card_grid(name, label, cards, cols, card_h, icon_fn=None, gap=18, title_size=17):
    """cards: dicts(title, body, accent, grad, [kicker], [status], [metric], [chips], [icon])"""
    P = C["pad"]
    cw = (W - 2 * P - gap * (cols - 1)) / cols
    rows_n = (len(cards) + cols - 1) // cols
    Hh = rows_n * card_h + (rows_n - 1) * gap + 2 + 2 * P + (8 if P else 0)
    out = []
    for i, c in enumerate(cards):
        r, k = divmod(i, cols)
        x, y = P + k * (cw + gap) + 1, P + r * (card_h + gap) + 1
        d = .15 + i * .14
        acc = c["accent"]
        g = [f'<g class="card" style="animation-delay:{d:.2f}s">',
             f'<rect x="{x}" y="{y}" width="{cw - 2}" height="{card_h - 2}" rx="14" fill="{C["panel"]}" stroke="{acc if C["mode"] == "light" else C["border"]}" stroke-opacity="{.3 if C["mode"] == "light" else 1}"{lift(f"sd{i}")}/>',
             f'<rect x="{x}" y="{y}" width="{cw - 2}" height="{card_h - 2}" rx="14" fill="url(#sh{i})"/>',
             sweep_rect(x, y, cw - 2, card_h - 2, 14, c["grad"], delay=i * 1.3, dur=7)]
        cy = y + 34
        tx = x + 22
        if c.get("icon") and icon_fn:
            g.append(icon_fn(c["icon"], x + 22, y + 22, acc))
            tx = x + 22
            cy = y + 92
        if c.get("status"):
            st, scol = c["status"]
            sw = len(st) * 7.2 + 34
            g.append(f'<rect x="{x + cw - sw - 18}" y="{y + 16}" width="{sw}" height="24" rx="12" fill="{scol}" fill-opacity=".12" stroke="{scol}" stroke-opacity=".5"/>'
                     f'<circle cx="{x + cw - sw - 4}" cy="{y + 28}" r="4" fill="{scol}"><animate attributeName="opacity" values="1;.25;1" dur="1.8s" repeatCount="indefinite"/></circle>'
                     f'<text x="{x + cw - sw + 6}" y="{y + 32.5}" class="st" fill="{scol}">{escape(st)}</text>')
        if c.get("kicker"):
            g.append(f'<text x="{tx}" y="{cy - 6}" class="kick" fill="{acc}">{escape(c["kicker"])}</text>')
            cy += 18
        g.append(f'<text x="{tx}" y="{cy}" class="tt" style="font-size:{title_size}px">{escape(c["title"])}</text>')
        cy += 24
        for line in wrap(c["body"], cw - 46, 13)[:5]:
            g.append(f'<text x="{tx}" y="{cy}" class="bd">{escape(line)}</text>')
            cy += 19
        if c.get("metric"):
            cy += 6
            for line in wrap(c["metric"], cw - 46, 13, .52)[:2]:
                g.append(f'<text x="{tx}" y="{cy}" class="mt" fill="{acc}">{escape(line)}</text>')
                cy += 19
        if c.get("chips"):
            cx_, cy_ = tx, y + card_h - 38
            for chip in c["chips"]:
                w = len(chip) * 6.9 + 18
                if cx_ + w > x + cw - 18:
                    break
                g.append(f'<rect x="{cx_}" y="{cy_}" width="{w}" height="22" rx="6" fill="{acc}" fill-opacity=".1" stroke="{acc}" stroke-opacity=".35"/>'
                         f'<text x="{cx_ + w / 2}" y="{cy_ + 15}" text-anchor="middle" class="chip" fill="{acc}">{escape(chip)}</text>')
                cx_ += w + 7
        g.append("</g>")
        out.append("".join(g))
    shades = "".join(
        f'<radialGradient id="sh{i}" cx="0" cy="0" r="1"><stop offset="0" stop-color="{c["accent"]}" stop-opacity=".14"/>'
        f'<stop offset=".6" stop-color="{c["accent"]}" stop-opacity="0"/></radialGradient>{shadow(f"sd{i}", c["accent"])}' for i, c in enumerate(cards))
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{Hh}" viewBox="0 0 {W} {Hh}" role="img" aria-label="{escape(label)}">
<defs>{grads()}{shades}</defs>
<style>
.tt{{font-family:{SANS};font-weight:700;fill:{C["title"]}}}
.bd{{font-family:{SANS};font-size:13px;fill:{C["text"]}}}
.mt{{font-family:{SANS};font-size:13px;font-weight:700}}
.kick{{font-family:{MONO};font-size:11.5px;letter-spacing:1.5px;font-weight:700}}
.st{{font-family:{SANS};font-size:11.5px;font-weight:700}}
.chip{{font-family:{MONO};font-size:11.5px}}
.card{{opacity:0;animation:up .8s cubic-bezier(.2,.8,.2,1) forwards}}
@keyframes up{{from{{opacity:0;transform:translateY(14px)}}to{{opacity:1;transform:none}}}}
.trace{{stroke-dasharray:12 88;opacity:.9;animation:trace 3.2s linear infinite}}
@keyframes trace{{to{{stroke-dashoffset:-100}}}}
</style>
{"".join(out)}
</svg>'''
    save(name, svg)
    return Hh


ICON_PATHS = {
    # simple 48x48 line icons
    "bot": "M14 18h20a4 4 0 0 1 4 4v12a4 4 0 0 1-4 4H22l-6 5v-5h-2a4 4 0 0 1-4-4V22a4 4 0 0 1 4-4zM24 10v8M19 27h.01M29 27h.01M19 32h10",
    "cloud": "M15 36h20a8 8 0 0 0 1-16 11 11 0 0 0-21-2 8 8 0 0 0 0 18zM24 24v8M20 28l4-4 4 4",
    "gauge": "M8 34a16 16 0 1 1 32 0M24 34l8-10M14 34h.01M34 34h.01M24 16v3M13 21l2 2M35 21l-2 2",
    "team": "M17 22a5 5 0 1 0 0-10 5 5 0 0 0 0 10zM31 22a5 5 0 1 0 0-10 5 5 0 0 0 0 10zM8 38c0-6 4-10 9-10s9 4 9 10M22 38c0-6 4-10 9-10s9 4 9 10",
    "brain": "M18 10a6 6 0 0 0-6 6 6 6 0 0 0-2 11 6 6 0 0 0 8 9 6 6 0 0 0 6-2V12a6 6 0 0 0-6-2zM30 10a6 6 0 0 1 6 6 6 6 0 0 1 2 11 6 6 0 0 1-8 9 6 6 0 0 1-6-2",
    "lock": "M14 22h20v16H14zM18 22v-6a6 6 0 0 1 12 0v6M24 28v4",
    "route": "M10 36h8a6 6 0 0 0 6-6V18a6 6 0 0 1 6-6h8M34 8l4 4-4 4M10 12h8M34 32l4 4-4 4M24 30a6 6 0 0 0 6 6h8",
    "scale": "M24 8v32M14 40h20M10 14h28M10 14l-6 14a6 6 0 0 0 12 0zM38 14l-6 14a6 6 0 0 0 12 0z",
    "ruler": "M8 34L34 8l6 6-26 26zM14 28l3 3M19 23l3 3M24 18l3 3M29 13l3 3",
    "flask": "M19 8h10M21 8v12L10 38a2 2 0 0 0 2 3h24a2 2 0 0 0 2-3L27 20V8M15 30h18",
    "search": "M21 34a13 13 0 1 0 0-26 13 13 0 0 0 0 26zM31 31l9 9",
    "ban": "M24 40a16 16 0 1 0 0-32 16 16 0 0 0 0 32zM13 13l22 22",
    "shield": "M24 6l14 6v10c0 9-6 16-14 20-8-4-14-11-14-20V12zM18 24l4 4 8-8",
    "eye": "M4 24s7-12 20-12 20 12 20 12-7 12-20 12S4 24 4 24zM24 29a5 5 0 1 0 0-10 5 5 0 0 0 0 10z",
}


def line_icon(key, x, y, col):
    return (f'<rect x="{x}" y="{y}" width="52" height="52" rx="12" fill="{col}" fill-opacity=".1" stroke="{col}" stroke-opacity=".4"/>'
            f'<g transform="translate({x + 2} {y + 2})" fill="none" stroke="{col}" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">'
            f'<path d="{ICON_PATHS[key]}"/>'
            f'<path class="trace" pathLength="100" stroke="{C["glow"]}" stroke-width="2.6" d="{ICON_PATHS[key]}"/></g>')


def ultahost_areas():
    P = "#a371f7"
    cards = [
        dict(icon="bot", title="AI Hosting Assistant", accent=P, grad="gp",
             body="Chat-driven server management that plans, authorizes, runs and verifies work on real customer servers."),
        dict(icon="cloud", title="Hosting Platform", accent=C["blue"], grad="gb",
             body="Moves apps onto self-hosted Supabase: provisioning, data sync and production review gates."),
        dict(icon="gauge", title="DevOps & Monitoring", accent=C["green"], grad="gg",
             body="Infrastructure control panel, CI/CD with auto-rollback, Prometheus + Grafana observability."),
        dict(icon="team", title="Internal Tools", accent=C["orange"], grad="go",
             body="HR, marketing, referral and offer-generation apps used by UltaHost teams every day."),
    ]
    card_grid("ultahost-areas.svg", "UltaHost work areas: AI Hosting Assistant, Hosting Platform, DevOps and Monitoring, Internal Tools",
              cards, 4, 222, line_icon, gap=14, title_size=15.5)


def zaude_features():
    cards = [
        dict(icon="brain", title="Persistent memory", accent=C["purple"], grad="gp",
             body="Hooks load each project's vault (state, decisions, session logs) at start. The next session picks up where the last one stopped, with its reasons."),
        dict(icon="lock", title="Signed lifecycle", accent=C["blue"], grad="gb",
             body="A hash-chained, HMAC-signed state machine runs review → verify → ship and gates Claude Code's own tools. Steps can't be skipped, only waived and logged."),
        dict(icon="route", title="Intent routing", accent=C["green"], grad="gg",
             body="Say what you want in plain language. It routes to the right flow with a safety mode (auto / propose / confirm). No commands to memorize."),
        dict(icon="scale", title="5-model review panel", accent=C["orange"], grad="go",
             body="Claude, Codex, OpenCode, Kimi and GLM review every change independently. Different models catch different bugs: one seat alone caught 8 real HIGH issues."),
    ]
    card_grid("zaude-features.svg", "Zaude features: persistent memory, signed lifecycle, intent routing, 5-model review panel",
              cards, 2, 192, line_icon)


def principles():
    cards = [
        dict(icon="ruler", title="Design the whole thing first", accent=C["blue"], grad="gb",
             body="Data model and architecture are reviewed before code. One deep, correct system beats a pile of MVPs."),
        dict(icon="flask", title="Evidence, not claims", accent=C["green"], grad="gg",
             body="Real exit codes, real test runs, a live check of the running app. Every report says what wasn't tested."),
        dict(icon="eye", title="Many models, one standard", accent=C["orange"], grad="go",
             body="Several AI models review every change. Each finding is checked against the real code before it's accepted."),
        dict(icon="search", title="Fix the root cause", accent=C["purple"], grad="gp",
             body="Find the actual cause and fix it at system level. \"It works now\" without knowing why is a failure."),
        dict(icon="ban", title="Real data only", accent=C["pink"], grad="go",
             body="No mocks, placeholders or hardcoded fallbacks. An empty state is better than fake data."),
        dict(icon="shield", title="Guardrails enforced by machines", accent=C["blue"], grad="gb",
             body="CI guards and ratchets tighten, never loosen. A tested rollback exists before any risky change."),
    ]
    card_grid("principles.svg", "How I work: design first, evidence not claims, multi-model review, root-cause fixes, real data only, machine-enforced guardrails",
              cards, 3, 206, line_icon, gap=14, title_size=15)


def projects():
    LIVE, ACT, SHIP = ("LIVE", C["green"]), ("ACTIVE", C["blue"]), ("SHIPPED", C["purple"])
    cards = [
        dict(kicker="ULTAHOST", status=ACT, title="AI Server-Management Assistant", accent=C["purple"], grad="gp",
             body="A chat interface that plans, authorizes, executes, verifies and repairs work on real customer servers through an on-server agent.",
             metric="Multi-service · authorization gate on every action",
             chips=["TypeScript", "PostgreSQL", "Event streaming", "LLM gateway", "Docker"]),
        dict(kicker="ULTAHOST", status=ACT, title="Self-Hosted Supabase Platform", accent=C["blue"], grad="gb",
             body="Multi-tenant platform that moves apps from Supabase Cloud to self-hosted Supabase: onboarding wizard, schema/function/storage sync, production review gate.",
             metric="6,085 tests in CI · 129 OpenAPI operations with drift gates",
             chips=["Bun", "TypeScript", "Postgres 16", "BullMQ", "Redis", "React 19"]),
        dict(kicker="CLIENT", status=LIVE, title="AtomOS", accent=C["green"], grad="gg",
             body="The operating system for a coworking venue: check-in, time-based billing, subscriptions, POS, cash reconciliation, bookings and analytics.",
             metric="25+ data models · race-safe dual-ledger wallet",
             chips=["Next.js", "React 19", "Prisma 7", "NextAuth", "Tailwind 4", "Docker"]),
        dict(kicker="COLLABORATION", status=ACT, title="CommunityOS", accent=C["orange"], grad="go",
             body="Multi-tenant community and course platform with courses, events, billing, messaging, RBAC, full Arabic RTL and signed S3 video delivery.",
             metric="47/47 security findings fixed · 175 E2E + 113 backend tests",
             chips=["NestJS 11", "TypeORM", "PostgreSQL", "React", "Caddy", "S3"]),
        dict(kicker="ULTAHOST", status=SHIP, title="AI Product UI Rebuild", accent=C["pink"], grad="go",
             body="Rebuilt a production AI product's interface from Figma while keeping all business logic; merged 35 production-only commits without losing a feature.",
             metric="776 tests green · tsc clean · zero regressions",
             chips=["React", "TypeScript", "Tailwind", "shadcn/Radix", "Supabase"]),
        dict(kicker="PERSONAL SAAS", status=LIVE, title="Masir", accent=C["blue"], grad="gb",
             body="CV builder with a deterministic ATS engine. The PDF is rendered from the exact preview the user sees, in English or Arabic.",
             metric="36 ATS rules · 10 industry profiles · 7-part job match",
             chips=["Next.js", "Supabase + RLS", "Zod", "Zustand", "Playwright"]),
    ]
    card_grid("projects.svg", "Projects: AI Server-Management Assistant, Self-Hosted Supabase Platform, AtomOS, CommunityOS, AI Product UI Rebuild, Masir",
              cards, 2, 226)


# ─────────────────────────────── STACK MARQUEE ───────────────────────────────
def fetch_icon(i, theme="dark"):
    import os
    import subprocess
    cache = Path(os.environ.get("ICON_CACHE", OUT / ".icons")) / (f"icon_{i}.svg" if theme == "dark" else f"icon_{i}_{theme}.svg")
    if cache.exists():  # pre-fetch with: curl -s "https://skillicons.dev/icons?i=<id>" > icon_<id>.svg
        raw = cache.read_text(encoding="utf-8")
    else:
        raw = subprocess.run(["curl", "-s", "-m", "30", f"https://skillicons.dev/icons?i={i}&theme={theme}"],
                             capture_output=True, check=True).stdout.decode()
    inner = re.search(r'<svg[^>]*width="256"[^>]*>(.*)</svg>\s*</g>', raw, re.S)
    body = inner.group(1) if inner else raw
    body = re.sub(r'\bid="([^"]+)"', lambda m: f'id="{i}_{m.group(1)}"', body)
    body = re.sub(r'url\(#([^)]+)\)', lambda m: f'url(#{i}_{m.group(1)})', body)
    body = re.sub(r'href="#([^"]+)"', lambda m: f'href="#{i}_{m.group(1)}"', body)
    return f'<symbol id="ic_{i}" viewBox="0 0 256 256">{body}</symbol>'


def stack(theme="dark", name="stack.svg"):
    rows = [
        ("LANGUAGES & FRONTEND", ["ts", "js", "py", "bash", "powershell", "react", "nextjs", "vite", "tailwind", "figma"], 1),
        ("BACKEND & DATA", ["nodejs", "bun", "nestjs", "express", "prisma", "postgres", "supabase", "redis", "mongodb", "sqlite"], -1),
        ("INFRA & QUALITY", ["docker", "githubactions", "nginx", "linux", "ubuntu", "git", "github", "jest", "vitest", "vscode"], 1),
    ]
    pills = ["Claude Code", "Claude API", "Playwright", "n8n", "Proxmox", "Caddy", "Tailscale", "OpenAPI", "Expo", "BullMQ", "Drizzle", "LiteLLM"]
    syms = "".join(fetch_icon(i, theme) for _, ids, _ in rows for i in ids)
    size, gap = 54, 22
    y = 46
    body = []
    for ri, (label, ids, direction) in enumerate(rows):
        unit = len(ids) * (size + gap)
        icons = "".join(
            f'<use href="#ic_{i}" x="{k * (size + gap) + rep * unit}" y="0" width="{size}" height="{size}"/>'
            for rep in range(3) for k, i in enumerate(ids))
        frm, to = ("0", f"-{unit}") if direction > 0 else (f"-{unit}", "0")
        body.append(f'<text x="{W / 2}" y="{y - 12}" text-anchor="middle" class="lab">{escape(label)}</text>'
                    f'<g transform="translate(0 {y})"><g>{icons}<animateTransform attributeName="transform" type="translate" '
                    f'from="{frm} 0" to="{to} 0" dur="{unit / 32:.1f}s" repeatCount="indefinite"/></g></g>')
        y += size + 48
    # pill row
    pw = [len(p) * 8.2 + 30 for p in pills]
    unit = sum(pw) + 12 * len(pills)
    xs, acc = [], 0
    for w in pw:
        xs.append(acc)
        acc += w + 12
    cols = [C["orange"], C["blue"], C["green"], C["pink"], C["purple"]]
    pill_svg = "".join(
        f'<g transform="translate({xs[k] + rep * unit} 0)"><rect width="{pw[k]}" height="34" rx="17" fill="{cols[k % 5]}" fill-opacity=".1" stroke="{cols[k % 5]}" stroke-opacity=".5"/>'
        f'<text x="{pw[k] / 2}" y="22" text-anchor="middle" class="pill" fill="{cols[k % 5]}">{escape(p)}</text></g>'
        for rep in range(3) for k, p in enumerate(pills))
    body.append(f'<text x="{W / 2}" y="{y - 12}" text-anchor="middle" class="lab">AI &amp; TOOLING</text>'
                f'<g transform="translate(0 {y})"><g>{pill_svg}<animateTransform attributeName="transform" type="translate" '
                f'from="-{unit:.0f} 0" to="0 0" dur="{unit / 32:.1f}s" repeatCount="indefinite"/></g></g>')
    Hh = y + 34 + 26
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="{W}" height="{Hh}" viewBox="0 0 {W} {Hh}" role="img" aria-label="Tech stack: TypeScript, JavaScript, Python, React, Next.js, Vite, Tailwind, Node.js, Bun, NestJS, Prisma, PostgreSQL, Supabase, Redis, MongoDB, Docker, GitHub Actions, Nginx, Linux, Jest, Vitest, Claude Code, Playwright, n8n, Proxmox">
<defs>{grads()}{syms}
<linearGradient id="edge" x1="0" x2="1"><stop offset="0" stop-color="#000"/><stop offset=".12" stop-color="#fff"/><stop offset=".88" stop-color="#fff"/><stop offset="1" stop-color="#000"/></linearGradient>
<mask id="m"><rect width="{W}" height="{Hh}" fill="url(#edge)"/></mask>
<clipPath id="c"><rect width="{W}" height="{Hh}" rx="14"/></clipPath>
</defs>
<style>
.lab{{font-family:{MONO};font-size:11.5px;letter-spacing:3px;fill:{C["dim"]};font-weight:700}}
.pill{{font-family:{SANS};font-size:14px;font-weight:600}}
</style>
<g clip-path="url(#c)"><rect width="{W}" height="{Hh}" fill="{C["bg"]}"/>
<g mask="url(#m)">{"".join(body)}</g></g>
<rect x=".5" y=".5" width="{W - 1}" height="{Hh - 1}" rx="14" fill="none" stroke="{C["border"]}"/>
{sweep_rect(.5, .5, W - 1, Hh - 1, 14, "gb", dur=10)}
</svg>'''
    save(name, svg)


# ─────────────────────────────── FOOTER ───────────────────────────────
def footer():
    Wf, Hf = 1200, 240

    def wave(amp, length, y, n=4):
        d = f"M0 {y}"
        for k in range(n * 2):
            x1 = k * length / 2
            d += f" Q{x1 + length / 4} {y - amp if k % 2 == 0 else y + amp} {x1 + length / 2} {y}"
        return d + f" V{Hf} H0 Z"

    waves = []
    for amp, length, y, col, op, dur, rev in [(16, 600, 168, C["blue2"], .16, 14, False),
                                              (20, 400, 184, C["violet"], .16, 10, True),
                                              (12, 300, 204, C["blue"], .22, 7, False)]:
        frm, to = ("0", f"-{length}") if not rev else (f"-{length}", "0")
        waves.append(f'<path d="{wave(amp, length, y, n=int(Wf / length) + 2)}" fill="{col}" fill-opacity="{op * C["wave_k"]:.2f}">'
                     f'<animateTransform attributeName="transform" type="translate" from="{frm} 0" to="{to} 0" dur="{dur}s" repeatCount="indefinite"/></path>')
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{Wf}" height="{Hf}" viewBox="0 0 {Wf} {Hf}" role="img" aria-label="Don't vibe code. Zaude code.">
<defs>
<linearGradient id="t" x1="0" x2="1"><stop offset="0" stop-color="{C["blue"]}"/><stop offset=".5" stop-color="{C["title"]}"/><stop offset="1" stop-color="{C["purple"]}"/>
<animateTransform attributeName="gradientTransform" type="translate" values="-.6 0;.6 0;-.6 0" dur="7s" repeatCount="indefinite"/></linearGradient>
<linearGradient id="bgf" x1="0" x2="0" y1="0" y2="1"><stop offset="0" stop-color="{C["bg"]}" stop-opacity="0"/><stop offset="1" stop-color="{C["hero_bg"]}"/></linearGradient>
</defs>
<style>
.q{{font-family:{SANS};font-size:40px;font-weight:800;letter-spacing:-.5px}}
.s{{font-family:{MONO};font-size:13px;letter-spacing:3px;fill:{C["dim"]}}}
</style>
<clipPath id="fc"><rect width="{Wf}" height="{Hf}" rx="18"/></clipPath>
<g clip-path="url(#fc)"><rect width="{Wf}" height="{Hf}" fill="{C["hero_bg"]}"/>
{"".join(waves)}</g>
<rect x="1" y="1" width="{Wf - 2}" height="{Hf - 2}" rx="18" fill="none" stroke="{C["border"]}"/>
<text x="{Wf / 2}" y="70" text-anchor="middle" class="q" fill="url(#t)">Don't vibe code. Zaude code.</text>
<text x="{Wf / 2}" y="104" text-anchor="middle" class="s">THANKS FOR STOPPING BY · LET'S BUILD SOMETHING REAL</text>
</svg>'''
    save("footer.svg", svg)


if __name__ == "__main__":
    import _generate as v1
    v1.terminal(); v1.pipeline(); v1.ultahost(); v1.divider()
    hero(); about(); ultahost_areas(); zaude_features(); principles(); projects(); stack(); footer()
    for f in sorted(OUT.glob("*.svg")):
        print(f"{f.name:24} {f.stat().st_size:>8,} B")
