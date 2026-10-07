#!/usr/bin/env python3
"""Render exact native full maps and four before/after 240x160 review views."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
from bancos_nativos import resolve_bank
from render_native_map import Renderer, render_map
from validate_grutas_bordas_v2 import animated

ROOT = Path(__file__).resolve().parents[2]


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--base', type=Path, required=True)
    args = parser.parse_args()
    out = ROOT / 'review/route103_v12'
    out.mkdir(exist_ok=True, parents=True)
    l = next(l for l in json.loads((ROOT / 'data/layouts/layouts.json').read_text())['layouts']
             if l['id'] == 'LAYOUT_ARAUNA_ROUTE103_SUL_PAMPA_V1')
    views = [('rio_norte', 24, 0), ('rio_sul', 24, 12), ('faixa_leste', 65, 12), ('borda_sul', 0, 12)]
    for repo, name in [(args.base.resolve(), 'before'), (ROOT, 'after')]:
        r = Renderer(*[resolve_bank(repo, l[k]) for k in ('primary_tileset', 'secondary_tileset')])
        r.palettes = [[tuple(v >> 3 << 3 for v in c) for c in row] for row in r.palettes]
        animated(r, repo, 0)
        im = render_map(r, repo / l['blockdata_filepath'], l['width'], l['height'])
        im.save(out / f'Route103_{name}.png')
        for label, x, y in views:
            im.crop((x * 16, y * 16, x * 16 + 240, y * 16 + 160)).save(out / f'{label}_{name}_240x160.png')
    try:
        font = ImageFont.truetype('DejaVuSans.ttf', 20)
    except OSError:
        font = ImageFont.load_default(size=20)
    sheet = Image.new('RGB', (1016, 4 * 368 + 78), '#f0f2ef')
    d = ImageDraw.Draw(sheet)
    d.text((20, 12), 'ROTA 103 V1.2 | RENDERS DOS DADOS NATIVOS', font=font, fill='#263f2b')
    d.text((20, 43), 'ANTES', font=font, fill='#263f2b')
    d.text((526, 43), 'DEPOIS', font=font, fill='#263f2b')
    for row, label in enumerate(['faixa_leste', 'rio_norte', 'rio_sul', 'borda_sul']):
        y = 78 + row * 368
        d.text((20, y), label.replace('_', ' ').upper(), font=font, fill='#263f2b')
        for col, name in enumerate(['before', 'after']):
            im = Image.open(out / f'{label}_{name}_240x160.png').convert('RGB')
            sheet.paste(im.resize((480, 320), Image.Resampling.NEAREST), (20 + col * 506, y + 30))
    sheet.save(out / 'Route103_V12_Comparacao.png')
    print('Native renders ready; these are not emulator captures.')


if __name__ == '__main__':
    main()
