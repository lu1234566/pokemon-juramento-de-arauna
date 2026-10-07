#!/usr/bin/env python3
"""Give the 111 blocked ground cells a dense bush; preserve all native grids."""
from __future__ import annotations

import argparse
import hashlib
import json
import struct
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
BASE = '7d40f7345ab2d84b4d8710edee30cf128c346166'
PLAN = {
    'data/tilesets/secondary/arauna_border_route103_uivo_v1/metatiles.bin': {723: 565, 790: 737},
    'data/tilesets/secondary/arauna_border_oldale_town_uivo_v1/metatiles.bin': {837: 802, 838: 802},
    'data/tilesets/secondary/arauna_border_route110_uivo_v1/metatiles.bin': {986: 983},
}


def replacement(raw: bytes, changes: dict[int, int]) -> bytes:
    entries = list(struct.unpack(f'<{len(raw) // 2}H', raw))
    original = entries[:]
    for target, source in changes.items():
        # Only the four upper tiles change. Ground and native attributes stay.
        i, j = (target % 512) * 8 + 4, (source % 512) * 8 + 4
        entries[i:i + 4] = original[j:j + 4]
    return struct.pack(f'<{len(entries)}H', *entries)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--base', type=Path, required=True)
    args = parser.parse_args()
    from subprocess import check_output
    base = args.base.resolve()
    if check_output(['git', 'rev-parse', 'HEAD'], cwd=base, text=True).strip() != BASE:
        raise ValueError('Use the exact recovered base ' + BASE)
    pending = []
    report = {'base_commit': BASE, 'files': []}
    for relative, changes in PLAN.items():
        original = (base / relative).read_bytes()
        final = replacement(original, changes)
        current = (ROOT / relative).read_bytes()
        if current not in (original, final):
            raise ValueError('Unknown local edit: ' + relative)
        pending.append((ROOT / relative, final))
        report['files'].append({
            'path': relative, 'upper_layers': {str(k): v for k, v in changes.items()},
            'before_sha256': hashlib.sha256(original).hexdigest(),
            'after_sha256': hashlib.sha256(final).hexdigest(),
        })
    # Preflight every file before writing any of them.
    for path, data in pending:
        path.write_bytes(data)
    out = ROOT / 'review/route103_v12/build.json'
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, indent=2) + '\n')
    print('Route 103 V1.2: 5 foreground entries in 3 private banks; native grids unchanged.')


if __name__ == '__main__':
    main()
