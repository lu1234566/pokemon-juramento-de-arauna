#!/usr/bin/env python3
"""Freeze the functional inventory before editing the legendary/Dive/Safari maps."""
from __future__ import annotations

import collections
import hashlib
import json
import re
import subprocess
from pathlib import Path

from bancos_nativos import resolve_bank
from script_metatile_dependencies import collect

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / 'review/cavernas_fundo_mar_v1'


def main() -> None:
    maps = {m['name']: m for p in (ROOT / 'data/maps').glob('*/map.json') for m in [json.loads(p.read_text())]}
    layouts = {l['id']: l for l in json.loads((ROOT / 'data/layouts/layouts.json').read_text())['layouts']}
    labels = {k: int(v, 16) for p in (ROOT / 'include/constants').glob('*metatile*.h')
              for k, v in re.findall(r'#define (METATILE_\w+)\s+(0x[\da-fA-F]+)', p.read_text())}
    groups = {
        'cavernas': sorted(n for n in maps if n.startswith(('TerraCave', 'MarineCave', 'SealedChamber', 'AncientTomb', 'IslandCave', 'AlteringCave', 'ArtisanCave'))),
        'dive': sorted(n for n in maps if n.startswith('Underwater_')),
        'safari': sorted(n for n in maps if n.startswith('SafariZone')),
        'correcao_rota103': ['Route103'],
    }
    assert [len(v) for v in groups.values()] == [11, 12, 7, 1]
    report = {'baseline_commit': subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip(),
              'groups': groups, 'maps': {}, 'totals': collections.Counter(),
              'unchanged_perimeter': ['DesertRuins', 'AbandonedShip_Underwater1', 'AbandonedShip_Underwater2',
                                      'BattleFrontier_OutsideEast', 'Route119_WeatherInstitute_1F', 'Route119_WeatherInstitute_2F'],
              'implementation_status': 'Inventory only; no new cave, Dive or Safari graphics implemented.'}
    for group, names in groups.items():
        for name in names:
            m = maps[name]
            l = layouts[m['layout']]
            paths = [ROOT / f'data/maps/{name}/map.json', ROOT / l['blockdata_filepath'], ROOT / l['border_filepath']]
            paths += sorted((ROOT / 'data/maps' / name).glob('*.inc'))
            for field in ('primary_tileset', 'secondary_tileset'):
                bank = resolve_bank(ROOT, l[field])
                paths += [bank / 'metatiles.bin', bank / 'metatile_attributes.bin']
            ids, shared = collect(ROOT, name, labels)
            text = '\n'.join(p.read_text() for p in sorted((ROOT / 'data/maps' / name).glob('*.inc')))
            record = {
                'group': group, 'layout': l, 'map': m,
                'hashes': {p.relative_to(ROOT).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest() for p in paths},
                'script_created_metatile_ids': sorted(ids), 'transitive_script_labels': shared,
                'own_functional_commands': [line.strip() for line in text.splitlines() if re.match(
                    r'\s*(?:setmetatile|setmaplayoutindex|setwarp|setdynamicwarp|setescapewarp|warp|setobject|addobject|removeobject|applymovement|setflag|clearflag|setvar|special|setwildbattle|seteventmon|givemon|call|goto|compare|checkflag)\b', line)],
                'flags': sorted(set(re.findall(r'\bFLAG_\w+', text))),
                'vars': sorted(set(re.findall(r'\bVAR_\w+', text))),
            }
            report['maps'][name] = record
            report['totals']['maps'] += 1
            for key in ('warp_events', 'object_events', 'coord_events', 'bg_events'):
                report['totals'][key] += len(m[key])
            report['totals']['connections'] += len(m['connections'] or [])
    OUT.mkdir(parents=True, exist_ok=True)
    path = OUT / 'functional_inventory.json'
    path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps(dict(report['totals']), indent=2))


if __name__ == '__main__':
    main()
