#!/usr/bin/env python3
"""Install the Fogueira V1 scene over its existing Encruzilhada interiors.

Preflight every dependency, file hash and reserved flag before any write.
Existing user edits cause a conflict; reapplication is a no-op. Backups retain
all replaced bytes. No ROM, save file or external service is touched.
"""
import argparse, datetime, hashlib, json, os, re, shutil, sys, tempfile
from pathlib import Path

BEGIN = '// BEGIN ARAUNA FOGUEIRA RODA V1'
END = '// END ARAUNA FOGUEIRA RODA V1'

def sha(raw): return hashlib.sha256(raw).hexdigest()

def safe(root, relative):
    path = (root / relative).resolve()
    if root != path and root not in path.parents: raise ValueError('path outside target: ' + relative)
    return path

def main():
    parser = argparse.ArgumentParser(); parser.add_argument('--target', type=Path, required=True); parser.add_argument('--check', action='store_true'); parser.add_argument('--package', type=Path, default=Path(__file__).resolve().parent); args = parser.parse_args()
    target, package = args.target.resolve(), args.package.resolve()
    manifest = json.loads((package / 'manifest.json').read_text()); errors = []; updates = []
    for relative, expected in manifest['dependencies'].items():
        p = safe(target, relative)
        if not p.is_file() or sha(p.read_bytes()) != expected: errors.append('base incompatível: ' + relative)
    for relative, item in manifest['files'].items():
        src = safe(package / 'payload', relative); dst = safe(target, relative)
        if not src.is_file() or sha(src.read_bytes()) != item['after']:
            errors.append('pacote corrompido: ' + relative); continue
        old = dst.read_bytes() if dst.exists() else None
        if old is not None and sha(old) == item['after']: continue
        if old is not None and sha(old) != item['before']: errors.append('edição local em conflito: ' + relative)
        elif old is None and item['before'] is not None: errors.append('arquivo base ausente: ' + relative)
        else: updates.append((dst, src.read_bytes(), old))
    flags_path = target / 'include/constants/flags.h'
    if not flags_path.is_file(): errors.append('cabeçalho de flags ausente')
    else:
        raw = flags_path.read_bytes(); text = raw.decode(); block = manifest['flags_block']
        pattern = re.escape(BEGIN) + r'.*?' + re.escape(END)
        matches = list(re.finditer(pattern, text, re.S))
        if text.count(BEGIN) != len(matches) or text.count(END) != len(matches) or len(matches) > 1:
            errors.append('marcadores de flags ambíguos')
        elif matches and matches[0][0] != block: errors.append('bloco de flags editado localmente')
        outside = re.sub(pattern, '', text, flags=re.S)
        for suffix in ('040', '041', '042'):
            alias = re.search(r'^\s*#define\s+(FLAG_\w+)\s+.*?FLAG_UNUSED_0x' + suffix + r'\b', outside, re.M)
            if alias: errors.append('flag já reservada: ' + alias[1])
            slot = re.search(r'^#define FLAG_UNUSED_0x' + suffix + r'\s+(0x[0-9A-Fa-f]+)\b', outside, re.M)
            if not slot or int(slot[1], 16) != int(suffix, 16): errors.append('slot de flag incompatível: ' + suffix)
        if re.search(r'^#define FLAG_ARAUNA_FOGUEIRA_\w+', outside, re.M): errors.append('nome de flag já usado fora do bloco')
        if not matches:
            marker = '#endif // GUARD_CONSTANTS_FLAGS_H'
            if text.count(marker) != 1: errors.append('fim do cabeçalho de flags ambíguo')
            else: updates.append((flags_path, text.replace(marker, block + '\n\n' + marker).encode(), raw))
    if errors:
        print(json.dumps({'status': 'CONFLICT', 'errors': errors, 'written_files': 0}, ensure_ascii=False, indent=2)); return 2
    if args.check:
        print(json.dumps({'status': 'PASS', 'mode': 'check', 'pending_files': len(updates), 'written_files': 0})); return 0
    backup = target / '.arauna_backups' / ('fogueira_roda_v1_' + datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%S%fZ'))
    if updates:
        backup.mkdir(parents=True)
        log = []
        for dst, new, old in updates:
            rel = dst.relative_to(target); log.append({'path': str(rel), 'previously_exists': old is not None})
            if old is not None:
                p = backup / rel; p.parent.mkdir(parents=True, exist_ok=True); p.write_bytes(old)
        (backup / 'backup_manifest.json').write_text(json.dumps(log, indent=2) + '\n')
        for dst, new, old in updates:
            dst.parent.mkdir(parents=True, exist_ok=True)
            with tempfile.NamedTemporaryFile(dir=dst.parent, delete=False) as temp: temp.write(new); tmp_path = temp.name
            os.replace(tmp_path, dst)
    print(json.dumps({'status': 'PASS', 'written_files': len(updates), 'backup': str(backup) if updates else None})); return 0

if __name__ == '__main__': sys.exit(main())
