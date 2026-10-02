"""Profile visuals v3 — animated section headers, 2026 ship-log timeline, and LIGHT variants of everything.

Run (from assets/):  ICON_CACHE=<dir with icon_<id>.svg + icon_<id>_light.svg> python _generate_v3.py
Every visual is written twice: name.svg (dark) and name-light.svg (light). The README swaps them with <picture>.
"""
import re
from html import escape

import _generate as v1
import _generate_v2 as v2
from _generate import C, MONO, SANS, OUT

W = 880

v2.ICON_PATHS.update({
    "user": "M24 22a7 7 0 1 0 0-14 7 7 0 0 0 0 14zM10 40c0-8 6-13 14-13s14 5 14 13",
    "building": "M10 40V12l14-6v34M24 40V18l14 5v17M6 40h36M15 16h4M15 22h4M15 28h4M29 26h4M29 32h4",
    "star": "M24 6l5.5 11.2 12.3 1.8-8.9 8.7 2.1 12.3L24 34.2 13 40l2.1-12.3-8.9-8.7 12.3-1.8z",
    "clock": "M24 42a18 18 0 1 0 0-36 18 18 0 0 0 0 36zM24 14v10l7 5",
    "rocket": "M28 8c6 0 12 6 12 12L26 34l-12-12zM14 22l-6 2 4 6M26 34l-2 6-6-4M18 30l-6 6M31 17h.01",
    "bolt": "M27 4L10 27h12l-3 17 17-23H24z",
    "chart": "M8 40h32M12 34V24M20 34V14M28 34V20M36 34V10",
})

# ─────────────────────────────── SECTION HEADERS ───────────────────────────────
SECTIONS = lambda: [
    ("about", "01", "WHO I AM", "About Me", "user", C["blue"], C["purple"]),
    ("ultahost", "02", "DAY JOB", "At UltaHost", "building", C["purple"], C["pink"]),
    ("zaude", "03", "OPEN SOURCE", "Flagship — Zaude™", "star", C["orange"], C["pink"]),
    ("shiplog", "04", "TIMELINE", "2026 Ship Log", "clock", C["green"], C["blue"]),
    ("projects", "05", "PROJECTS", "What I Build", "rocket", C["blue"], C["green"]),
    ("stack", "06", "TOOLKIT", "Tech Stack", "bolt", C["yellow"], C["orange"]),
    ("work", "07", "PRINCIPLES", "How I Work", "eye", C["pink"], C["purple"]),
    ("activity", "08", "ACTIVITY", "GitHub Activity", "chart", C["green"], C["blue"]),
]


def section_header(key, num, kicker, title, icon, c1, c2):
    Hh = 100  # solid dark panel: identical in GitHub light and dark mode
    tw = len(title) * 17.5 + 10
    # dark mode: solid dark panel. light mode: no panel — the title blends into GitHub's white page.
    panel = ("" if C["mode"] == "light" else
             f'<rect width="{W}" height="{Hh}" rx="14" fill="{C["bg"]}"/>'
             f'<rect x=".5" y=".5" width="{W - 1}" height="{Hh - 1}" rx="14" fill="none" stroke="{C["border"]}"/>')
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{Hh}" viewBox="0 0 {W} {Hh}" role="img" aria-label="{escape(title)}">
<defs>
<linearGradient id="tg" x1="0" x2="1" gradientUnits="objectBoundingBox"><stop offset="0" stop-color="{c1}"/><stop offset=".5" stop-color="{C["title"]}"/><stop offset="1" stop-color="{c2}"/>
<animateTransform attributeName="gradientTransform" type="translate" values="-.7 0;.7 0;-.7 0" dur="6s" repeatCount="indefinite"/></linearGradient>
<linearGradient id="ul" gradientUnits="userSpaceOnUse" x1="0" x2="{W}"><stop offset="0" stop-color="{c1}"/><stop offset=".4" stop-color="{c2}"/><stop offset="1" stop-color="{c2}" stop-opacity="0"/></linearGradient>
<radialGradient id="dot"><stop offset="0" stop-color="{C["glow"]}"/><stop offset=".35" stop-color="{c1}"/><stop offset="1" stop-color="{c1}" stop-opacity="0"/></radialGradient>
</defs>
<style>
.k{{font-family:{MONO};font-size:12px;font-weight:700;letter-spacing:3px}}
.t{{font-family:{SANS};font-size:31px;font-weight:800;letter-spacing:-.3px}}
.trace{{stroke-dasharray:12 88;opacity:.9;animation:trace 3s linear infinite}}
@keyframes trace{{to{{stroke-dashoffset:-100}}}}
.in{{opacity:0;animation:in .9s cubic-bezier(.2,.8,.2,1) forwards}}
@keyframes in{{from{{opacity:0;transform:translateX(-12px)}}to{{opacity:1;transform:none}}}}
</style>
<clipPath id="hc"><rect width="{W}" height="{Hh}" rx="14"/></clipPath>
{panel}
<g clip-path="url(#hc)"><g transform="translate(16 6)">
<circle cx="32" cy="40" r="30" fill="none" stroke="{c1}" stroke-width="1.5">
<animate attributeName="r" values="27;38" dur="2.4s" repeatCount="indefinite"/><animate attributeName="opacity" values=".8;0" dur="2.4s" repeatCount="indefinite"/></circle>
<circle cx="32" cy="40" r="27" fill="{c1}" fill-opacity=".12" stroke="{c1}" stroke-opacity=".6"/>
<g transform="translate(8 16)" fill="none" stroke="{c1}" stroke-width="2.3" stroke-linecap="round" stroke-linejoin="round"><path d="{v2.ICON_PATHS[icon]}"/><path class="trace" pathLength="100" stroke="{C["glow"]}" stroke-width="2.6" d="{v2.ICON_PATHS[icon]}"/></g>
<g class="in" style="animation-delay:.1s"><text x="78" y="32" class="k" fill="{c1}">{num} — {escape(kicker)}</text></g>
<g class="in" style="animation-delay:.3s"><text x="76" y="66" class="t" fill="url(#tg)">{escape(title)}</text></g>
<rect x="78" y="80" width="{W - 120}" height="2" rx="1" fill="url(#ul)" opacity=".35"/>
<rect x="78" y="80" width="{min(tw, 420):.0f}" height="2" rx="1" fill="url(#ul)"/>
<ellipse cy="81" rx="34" ry="5" fill="url(#dot)"><animate attributeName="cx" values="60;{W + 40}" dur="4s" repeatCount="indefinite"/></ellipse>
</g></g>
</svg>'''
    v2.save(f"h-{key}.svg", svg)


# ─────────────────────────────── 2026 SHIP LOG ───────────────────────────────
MILESTONES = lambda: [  # all dates/facts from the project vault
    ("APR 17", "Zaude is born", "extracted from my own", "Claude Code setup", C["orange"]),
    ("APR 29", "AI product UI live", "776 tests green,", "zero regressions", C["pink"]),
    ("MAY 19", "AtomOS v1.1", "live at a real", "coworking venue", C["green"]),
    ("MAY 19", "AI hiring POC", "10 CVs screened", "in 71 seconds", C["purple"]),
    ("JUN 21", "Zaude 3 ships", "autonomous +", "intent-routed", C["orange"]),
    ("JUL 06", "5-model panel", "Claude · Codex · OpenCode", "· Kimi · GLM", C["blue"]),
    ("SEP", "6,085 CI tests", "Supabase platform", "grouped lane", C["blue"]),
    ("OCT", "1,750+ commits", "across 23", "UltaHost repos", C["purple"]),
]


def shiplog():
    Hh, T = 300, 10.0
    ly = 150
    x0, x1 = 96, W - 96
    step = (x1 - x0) / (len(MILESTONES()) - 1)
    parts = []
    for i, (date, title, l1, l2, col) in enumerate(MILESTONES()):
        x = x0 + i * step
        t = .4 + i * (T * .6 / len(MILESTONES()))
        on = t / T * 100
        up = i % 2 == 0
        ty = ly - 92 if up else ly + 44
        conn_y1, conn_y2 = (ly - 30, ly - 12) if up else (ly + 12, ly + 30)
        parts.append(f'''
<style>@keyframes m{i}{{0%,{on:.2f}%{{opacity:0;transform:translateY({8 if up else -8}px)}}{on + 4:.2f}%,94%{{opacity:1;transform:none}}98%,100%{{opacity:0}}}}
.m{i}{{animation:m{i} {T}s cubic-bezier(.2,.8,.2,1) infinite}}
@keyframes n{i}{{0%,{on:.2f}%{{transform:scale(0)}}{on + 2:.2f}%{{transform:scale(1.6)}}{on + 4:.2f}%,94%{{transform:scale(1)}}98%,100%{{transform:scale(0)}}}}
.n{i}{{animation:n{i} {T}s ease-out infinite;transform-origin:{x:.1f}px {ly}px}}</style>
<circle cx="{x:.1f}" cy="{ly}" r="7" fill="{col}" class="n{i}"/>
<circle cx="{x:.1f}" cy="{ly}" r="12" fill="none" stroke="{col}" stroke-opacity=".5" class="m{i}"/>
<g class="m{i}">
<line x1="{x:.1f}" x2="{x:.1f}" y1="{conn_y1}" y2="{conn_y2}" stroke="{col}" stroke-opacity=".6" stroke-dasharray="2 3"/>
<text x="{x:.1f}" y="{ty}" text-anchor="middle" class="d" fill="{col}">{escape(date)}</text>
<text x="{x:.1f}" y="{ty + 22}" text-anchor="middle" class="tt">{escape(title)}</text>
<text x="{x:.1f}" y="{ty + 41}" text-anchor="middle" class="s">{escape(l1)}</text>
<text x="{x:.1f}" y="{ty + 57}" text-anchor="middle" class="s">{escape(l2)}</text>
</g>''')
    prog_end = .4 + T * .6
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{Hh}" viewBox="0 0 {W} {Hh}" role="img" aria-label="2026 ship log: Apr 17 Zaude born; Apr 29 AI product UI live with 776 tests; May 19 AtomOS v1.1 live; May 19 AI hiring POC; Jun 21 Zaude 3; Jul 06 5-model review panel; Sep 6,085 CI tests; Oct 1,750+ UltaHost commits">
<defs>{v2.grads()}
<linearGradient id="pl" gradientUnits="userSpaceOnUse" x1="{x0}" x2="{x1}"><stop offset="0" stop-color="{C["orange"]}"/><stop offset=".35" stop-color="{C["green"]}"/><stop offset=".7" stop-color="{C["blue"]}"/><stop offset="1" stop-color="{C["purple"]}"/></linearGradient>
<radialGradient id="hd"><stop offset="0" stop-color="{C["glow"]}"/><stop offset=".4" stop-color="{C["blue"]}"/><stop offset="1" stop-color="{C["blue"]}" stop-opacity="0"/></radialGradient>
</defs>
<style>
.d{{font-family:{MONO};font-size:12px;font-weight:700;letter-spacing:2px}}
.tt{{font-family:{SANS};font-size:14.5px;font-weight:700;fill:{C["title"]}}}
.s{{font-family:{SANS};font-size:11.5px;fill:{C["dim"]}}}
@keyframes prog{{0%,4%{{stroke-dashoffset:1000}}{prog_end / T * 100:.1f}%,94%{{stroke-dashoffset:0}}98%,100%{{stroke-dashoffset:1000;opacity:0}}}}
.prog{{stroke-dasharray:1000;animation:prog {T}s linear infinite}}
@keyframes head{{0%,4%{{transform:translateX(0)}}{prog_end / T * 100:.1f}%,100%{{transform:translateX({x1 - x0}px)}}}}
.head{{animation:head {T}s linear infinite}}
</style>
<rect width="{W}" height="{Hh}" rx="14" fill="{C["bg"]}"/>
<rect x=".5" y=".5" width="{W - 1}" height="{Hh - 1}" rx="14" fill="none" stroke="{C["border"]}"/>
{v2.sweep_rect(.5, .5, W - 1, Hh - 1, 14, "gb", dur=10)}
<line x1="{x0}" x2="{x1}" y1="{ly}" y2="{ly}" stroke="{C["border"]}" stroke-width="3" stroke-linecap="round"/>
<line x1="{x0}" x2="{x1}" y1="{ly}" y2="{ly}" stroke="url(#pl)" stroke-width="3" stroke-linecap="round" pathLength="1000" class="prog"/>
<g class="head"><ellipse cx="{x0}" cy="{ly}" rx="22" ry="9" fill="url(#hd)"/></g>
{"".join(parts)}
</svg>'''
    v2.save("shiplog.svg", svg)


# ─────────────────────────────── BUILD BOTH THEMES ───────────────────────────────
def build_all(theme):
    v1.terminal(); v1.pipeline(); v1.ultahost(); v1.divider()
    v2.hero(); v2.about(); v2.ultahost_areas(); v2.zaude_features(); v2.principles(); v2.projects()
    v2.stack(theme=theme); v2.footer()
    for sec in SECTIONS():
        section_header(*sec)
    shiplog()


KEEP_DARK = {"zaude-terminal", "about"}  # code surfaces stay dark on light pages, by design


if __name__ == "__main__":
    for old in OUT.glob("*.svg"):
        old.unlink()
    # One design for both GitHub themes (operator decision 2026-10-02: the dark design reads best
    # in light mode too). The light theme tokens stay in _generate.py if a light set is ever wanted.
    v1.set_theme("dark"); build_all("dark")
    # Only the section titles follow GitHub's theme; every other visual is the same dark design in both.
    dark_h = {f.stem: f.read_text(encoding="utf-8") for f in OUT.glob("h-*.svg")}
    v1.set_theme("light")
    for sec in SECTIONS():
        section_header(*sec)
    for stem, svg in dark_h.items():
        (OUT / f"{stem}.svg").replace(OUT / f"{stem}-light.svg")
        (OUT / f"{stem}.svg").write_text(svg, encoding="utf-8")
    v1.set_theme("dark")
    files = sorted(OUT.glob("*.svg"))
    print(len(files), "SVGs written")
