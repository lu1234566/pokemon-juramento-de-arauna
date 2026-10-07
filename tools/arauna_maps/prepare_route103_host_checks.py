#!/usr/bin/env python3
"""Generate official map/MIDI prerequisites for static checks without ARM tools."""
from __future__ import annotations

import shlex
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def run(args):
    subprocess.run(args, cwd=ROOT, check=True)


def main():
    for name in ('mapjson', 'mid2agb'):
        run(['make', '-C', f'tools/{name}', '-j2'])
    tool = 'tools/mapjson/mapjson'
    run([tool, 'groups', 'emerald', 'data/maps/map_groups.json', 'data/maps', 'include/constants'])
    run([tool, 'layouts', 'emerald', 'data/layouts/layouts.json', 'data/layouts', 'include/constants'])
    maps = sorted((ROOT / 'data/maps').glob('*/map.json'))
    for p in maps:
        rel = p.relative_to(ROOT)
        run([tool, 'map', 'emerald', str(rel), 'data/layouts/layouts.json', str(rel.parent)])
    run([tool, 'event_constants', 'emerald', *[str(p.relative_to(ROOT)) for p in maps], 'include/constants/map_event_ids.h'])
    songs = ROOT / 'sound/songs/midi'
    count = 0
    for line in (songs / 'midi.cfg').read_text().splitlines():
        if not line.strip():
            continue
        name, args = line.split(':', 1)
        name = name.strip()
        source = songs / (name if name.endswith('.mid') else name + '.mid')
        run(['tools/mid2agb/mid2agb', str(source.relative_to(ROOT)),
             str(source.with_suffix('.s').relative_to(ROOT)), *shlex.split(args)])
        count += 1
    print(f'Official host prerequisites: {len(maps)} maps, {count} songs; no ARM compilation.')


if __name__ == '__main__':
    main()
