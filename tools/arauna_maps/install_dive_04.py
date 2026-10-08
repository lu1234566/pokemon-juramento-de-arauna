#!/usr/bin/env python3
"""Install a selected Arauna checkpoint after whole-package hash preflight."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import subprocess
import tempfile
from pathlib import Path

PACKAGE = Path(__file__).resolve().parent


def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def write_atomic(path: Path, raw: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(dir=path.parent, prefix='.arauna-', delete=False) as f:
        temporary = Path(f.name)
        f.write(raw)
    try:
        os.chmod(temporary, (path.stat().st_mode & 0o777) if path.exists() else 0o644)
        os.replace(temporary, path)
    finally:
        temporary.unlink(missing_ok=True)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('target', type=Path)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    args.step = 'Dive 04'
    target = args.target.resolve()
    manifest = json.loads((PACKAGE / 'manifest.json').read_text())
    head = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=target, text=True).strip()
    accepted = {manifest['base_commit'], *manifest['checkpoint_commits'].values()}
    if head not in accepted:
        raise ValueError('Checkout must be at the recovered base or a supplied checkpoint: ' + manifest['base_commit'])
    selected, pending = [], []
    for entry in manifest['files']:
        relative = Path(entry['path'])
        if relative.is_absolute() or '..' in relative.parts:
            raise ValueError('Unsafe package path')
        source = (PACKAGE / 'source' / relative).resolve()
        if not source.is_relative_to((PACKAGE / 'source').resolve()):
            raise ValueError('Unsafe source path')
        raw = source.read_bytes()
        if len(raw) != entry['bytes'] or sha(raw) != entry['sha256']:
            raise ValueError('Corrupted package payload: ' + entry['path'])
        path = target / relative
        if not path.resolve().is_relative_to(target):
            raise ValueError('Target path escapes checkout')
        if path.exists() and not path.is_file():
            raise ValueError('Target is not a file: ' + entry['path'])
        current = path.read_bytes() if path.exists() else None
        current_hash = sha(current) if current is not None else None
        if current_hash not in (entry['before_sha256'], entry['sha256']):
            raise ValueError('Unknown local edit; nothing was written: ' + entry['path'])
        selected.append(entry)
        if current_hash != entry['sha256']:
            pending.append((entry, path, current, raw))
    # Verify all existing gameplay dependencies, including Braille, original
    # puzzle conditions, shared Regi scripts, return warps and encounters.
    # This contract was itself hash-checked in the complete payload preflight.
    contract_path = PACKAGE / 'source' / manifest['functional_contract']
    contract = json.loads(contract_path.read_text())
    if contract['base_commit'] != manifest['base_commit']:
        raise ValueError('Functional contract base does not match the package')
    for relative, expected in {**contract['protected_hashes'], **contract.get('dependency_hashes',{})}.items():
        path = target / relative
        if not path.resolve().is_relative_to(target):
            raise ValueError('Dependency path escapes checkout')
        if not path.is_file() or sha(path.read_bytes()) != expected:
            raise ValueError('Changed gameplay dependency; nothing was written: ' + relative)
    if args.check or not pending:
        print(json.dumps({'status': 'PASS', 'checkpoint': 'Dive 04', 'files': len(selected), 'pending': len(pending), 'written': 0}))
        return
    backup = Path(tempfile.mkdtemp(prefix='checkpoint-Dive-04-', dir=make_backup_parent(target)))
    records = []
    for entry, path, old, raw in pending:
        if old is not None:
            previous = backup / entry['path']
            previous.parent.mkdir(parents=True, exist_ok=True)
            previous.write_bytes(old)
        records.append({'path': entry['path'], 'previously_existed': old is not None})
    (backup / 'rollback_manifest.json').write_text(json.dumps(records, indent=2) + '\n')
    written = []
    try:
        for entry, path, old, raw in pending:
            written.append((path, old))
            write_atomic(path, raw)
            if sha(path.read_bytes()) != entry['sha256']:
                raise IOError('Post-write hash mismatch: ' + entry['path'])
    except BaseException:
        for path, old in reversed(written):
            if old is None:
                path.unlink(missing_ok=True)
            else:
                path.write_bytes(old)
        raise
    print(json.dumps({'status': 'PASS', 'checkpoint': 'Dive 04', 'files': len(selected), 'written': len(pending), 'backup': str(backup)}))


def make_backup_parent(target: Path) -> Path:
    parent = target / '.arauna-checkpoint-backups'
    parent.mkdir(exist_ok=True)
    return parent


if __name__ == '__main__':
    main()
