#!/usr/bin/env python3
"""Convert all SVGs in `assets/` to PNG fallbacks using cairosvg.
Creates same-name .png files next to SVGs.
"""
import os
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / 'assets'

svgs = list(ASSETS.glob('*.svg'))
if not svgs:
    print('No SVGs found in', ASSETS)
    raise SystemExit(1)

try:
    import cairosvg
except Exception as e:
    print('cairosvg not installed:', e)
    raise

for s in svgs:
    out = s.with_suffix('.png')
    try:
        cairosvg.svg2png(url=str(s), write_to=str(out), output_width=round( (800 if 'hero' in s.name else 600) ))
        print('Wrote', out)
    except Exception as e:
        print('Failed', s, '->', e)
