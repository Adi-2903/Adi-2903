#!/usr/bin/env python3
"""Simple XP badge generator.
Reads `.xp` file (single integer). Writes `assets/xp-badge.svg` with current XP and level.
"""
import os
ROOT = os.path.dirname(os.path.dirname(__file__))
XP_FILE = os.path.join(ROOT, '.xp')
OUT = os.path.join(ROOT, 'assets', 'xp-badge.svg')

try:
    xp = int(open(XP_FILE, 'r').read().strip())
except Exception:
    xp = 0

level = xp // 100
next_xp = (level + 1) * 100
pct = int((xp - level*100) / (next_xp - level*100) * 100) if next_xp>0 else 0

svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="260" height="64" viewBox="0 0 260 64" preserveAspectRatio="xMidYMid">
  <style>
    .bg{{fill:#0b1020}}
    .label{{font:600 12px 'Segoe UI', Roboto, sans-serif; fill:#9aa4b2}}
    .val{{font:700 18px 'Segoe UI', Roboto, sans-serif; fill:#00d9ff}}
    .barbg{{fill:#0f172a}}
    .bar{{fill:url(#g1)}}
  </style>
  <defs>
    <linearGradient id="g1" x1="0" x2="1"><stop offset="0%" stop-color="#00d9ff"/><stop offset="100%" stop-color="#7c3aed"/></linearGradient>
  </defs>
  <rect class="bg" width="100%" height="100%" rx="8"/>
  <text x="16" y="24" class="label">Level</text>
  <text x="16" y="44" class="val">{level}</text>
  <g transform="translate(120,20)">
    <rect class="barbg" x="0" y="6" width="120" height="12" rx="6"/>
    <rect class="bar" x="0" y="6" width="{int(1.2*pct)}" height="12" rx="6"/>
  </g>
  <text x="248" y="40" class="label">{xp} XP</text>
</svg>'''

os.makedirs(os.path.dirname(OUT), exist_ok=True)
open(OUT, 'w', encoding='utf-8').write(svg)
print('Wrote', OUT)
