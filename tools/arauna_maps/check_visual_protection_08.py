#!/usr/bin/env python3
"""Check corrections frozen at a594b3e1e6 before accepting the next art package."""
import argparse
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repo', type=Path, default=ROOT)
    args = parser.parse_args()
    contract = json.loads((ROOT / 'review/aceitacao_08_auditoria/protected_files.json').read_text())
    failed = []
    for relative, expected in contract['protected_hashes'].items():
        path = args.repo / relative
        actual = hashlib.sha256(path.read_bytes()).hexdigest() if path.is_file() else 'missing'
        if actual != expected:
            failed.append(relative)
    if failed:
        for relative in failed:
            print('FAIL: protected correction changed:', relative)
        return 1
    print('PASS:', len(contract['protected_hashes']), 'protected files from', contract['base_commit'][:10])
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
