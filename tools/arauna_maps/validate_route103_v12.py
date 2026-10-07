#!/usr/bin/env python3
"""Audit the real native data and C border selector against the recovered base."""
from __future__ import annotations

import argparse
import collections
import ctypes
import json
import subprocess
import tempfile
from pathlib import Path

from bancos_nativos import bank_words, resolve_bank
from build_route103_v12 import BASE, PLAN, ROOT
from render_native_map import Renderer, words
from validate_border_visuals_119_118 import compile_connections
from validate_grutas_bordas_v2 import animated
import host_visual_selector_v2 as host


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--base', type=Path, required=True)
    parser.add_argument('--output', type=Path, default=ROOT / 'review/route103_v12/validation.json')
    args = parser.parse_args()
    base = args.base.resolve()
    assert subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=base, text=True).strip() == BASE
    maps = {m['name']: m for p in (ROOT / 'data/maps').glob('*/map.json') for m in [json.loads(p.read_text())]}
    by_id = {m['id']: m for m in maps.values()}
    layouts = {l['id']: l for l in json.loads((ROOT / 'data/layouts/layouts.json').read_text())['layouts']}
    # Every existing gameplay/engine/graphic file except the three declared banks
    # must remain byte-identical. This includes all scripts, grid words, attributes,
    # events, encounters, palette rows, animation sources and save migration code.
    protected = 0
    for name in subprocess.check_output(['git', 'ls-files', 'data', 'src', 'include', 'graphics'], cwd=base, text=True).splitlines():
        if name in PLAN:
            continue
        assert (base / name).read_bytes() == (ROOT / name).read_bytes(), ('protected file changed', name)
        protected += 1
    renderers, pixels = {}, {}

    def renderer(which: int, name: str, frame: int = 0):
        l = layouts[maps[name]['layout']]
        key = which, l['primary_tileset'], l['secondary_tileset'], frame
        if key not in renderers:
            repo = (base, ROOT)[which]
            r = Renderer(*[resolve_bank(repo, l[k]) for k in ('primary_tileset', 'secondary_tileset')])
            r.palettes = [[tuple(v >> 3 << 3 for v in c) for c in row] for row in r.palettes]
            renderers[key] = animated(r, repo, frame)
        return renderers[key]

    def pix(which: int, name: str, mid: int, frame: int = 0):
        r = renderer(which, name, frame)
        key = id(r), mid
        if key not in pixels:
            pixels[key] = r.metatile(mid).tobytes()
        return pixels[key]

    route = layouts[maps['Route103']['layout']]
    grid = words(ROOT / route['blockdata_filepath'])
    # The contract identifies two blocked ground families, independently from
    # builder replacements. Tree bases and surf banks are contextual graphics.
    expected = {i for i, v in enumerate(grid) if (v & 1023) in (723, 790)}
    assert len(expected) == 111
    assert collections.Counter(grid[i] & 1023 for i in expected) == {723: 68, 790: 43}
    before_ground = {pix(0, 'Route103', v & 1023) for v in grid if not v & 0xC00}
    after_ground = {pix(1, 'Route103', v & 1023) for v in grid if not v & 0xC00}
    changed = set()
    for i, v in enumerate(grid):
        mid = v & 1023
        assert bank_words(renderer(0, 'Route103'), mid, True) == bank_words(renderer(1, 'Route103'), mid, True)
        if pix(0, 'Route103', mid) != pix(1, 'Route103', mid):
            changed.add(i)
        if i in expected:
            assert v & 0xC00 and bank_words(renderer(1, 'Route103'), mid, True) & 255 == 0
            assert pix(0, 'Route103', mid) in before_ground
            assert pix(1, 'Route103', mid) not in after_ground
    assert changed == expected, ('unexpected changed cells', len(changed ^ expected))
    # Every layout that actually uses a touched bank is checked, including inactive
    # variants. Imported border IDs must not affect the receiver's own scenery.
    changed_banks = {str((ROOT / p).parent) for p in PLAN}
    own = []
    for l in layouts.values():
        if l['secondary_tileset'] == '0':
            continue
        bank = resolve_bank(ROOT, l['secondary_tileset'])
        if str(bank) not in changed_banks:
            continue
        names = [n for n, m in maps.items() if m['layout'] == l['id']]
        assert names, ('unreviewed inactive user', l['id'])
        name = names[0]
        count = 0
        for field in ('blockdata_filepath', 'border_filepath'):
            for v in words(ROOT / l[field]):
                mid = v & 1023
                difference = pix(0, name, mid) != pix(1, name, mid)
                assert not difference or (name == 'Route103' and field == 'blockdata_filepath' and mid in (723, 790))
                assert bank_words(renderer(0, name), mid, True) == bank_words(renderer(1, name), mid, True)
                count += difference
        own.append({'map': name, 'changed_cells': count})
    codes = {119: 'Route119', 118: 'Route118'}
    codes = {n: c for c, n in codes.items()}
    for path in ('review/grutas_bordas_v2/borders_build.json', 'review/sul_pampa_v1/borders_build.json', 'review/uivo_norte_v1/borders_build.json'):
        codes.update({n: d['code'] for n, d in json.loads((ROOT / path).read_text())['maps'].items()})
    regions = json.loads((ROOT / 'review/uivo_norte_v1/borders_build.json').read_text())['regions']
    exact = {(r['receiver'], r['source']) for r in regions}
    directions, comparisons, border_changes = [], 0, 0
    with tempfile.TemporaryDirectory(prefix='arauna-route103-v12-') as tmp:
        folder = Path(tmp)
        host.ROOT = ROOT
        selector = host.compile_selector(folder)
        copier = compile_connections(folder)
        for name, m in maps.items():
            l = layouts[m['layout']]
            for c in m['connections'] or []:
                if c['direction'] not in ('up', 'down', 'left', 'right'):
                    continue
                source = by_id[c['map']]['name']
                sl = layouts[maps[source]['layout']]
                sg = words(ROOT / sl['blockdata_filepath'])
                buf = (ctypes.c_int * 50000)()
                count = copier(('up', 'down', 'left', 'right').index(c['direction']), l['width'], l['height'], sl['width'], sl['height'], c['offset'], buf)
                differences = 0
                for j in range(count):
                    sx, sy, x, y = buf[j * 4:j * 4 + 4]
                    mid = sg[sy * sl['width'] + sx] & 1023
                    alias = selector(codes.get(name, 0), x, y, mid)
                    for frame in range(8):
                        old, new = pix(0, name, alias, frame), pix(1, name, alias, frame)
                        allowed = source == 'Route103' and mid in (723, 790)
                        assert (old != new) == allowed, ('border scope', name, source, sx, sy, frame)
                        if (name, source) in exact:
                            assert new == pix(1, source, mid, frame), ('border RGB555', name, source, sx, sy, frame)
                            assert bank_words(renderer(1, name), alias, True) == bank_words(renderer(1, source), mid, True)
                        comparisons += 1
                    differences += old != new
                border_changes += differences
                directions.append({'receiver': name, 'source': source, 'cells': count, 'changed_cells': differences})
    report = {
        'status': 'PASS', 'base_commit': BASE, 'protected_files_unchanged': protected,
        'route103_changed_cells': 111, 'route103_unintended_changes': 0,
        'grid_collision_elevation_behavior_events_scripts_unchanged': True,
        'native_grids_changed': 0, 'new_tiles_palettes_or_metatiles': 0,
        'own_maps': own, 'directions_checked': len(directions),
        'eight_frame_border_comparisons': comparisons, 'border_changed_cells': border_changes,
        'unrelated_border_changes': 0, 'connections': directions,
        'changed_coordinates': [[i % route['width'], i // route['width']] for i in sorted(changed)],
        'rom_build': 'pending', 'emulator': 'pending',
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps({k: v for k, v in report.items() if k not in ('connections', 'changed_coordinates', 'own_maps')}, indent=2))


if __name__ == '__main__':
    main()
