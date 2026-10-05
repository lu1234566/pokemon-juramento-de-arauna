#!/usr/bin/env python3
"""Create the additive Fogueira scene patch with owned baselines and hashes."""
import argparse, hashlib, json, re, shutil, zipfile
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
TITLE = 'Pokemon_Juramento_de_Arauna_Fogueira_Roda_V1'

def sha(path): return hashlib.sha256(path.read_bytes()).hexdigest()

def main():
    parser = argparse.ArgumentParser(); parser.add_argument('--output-dir', type=Path, default=ROOT.parent / 'output'); args = parser.parse_args()
    package = args.output_dir / TITLE
    if package.exists(): shutil.rmtree(package)
    (package / 'payload').mkdir(parents=True)
    baseline = ROOT / 'review/fogueira_roda_v1/baseline'
    owned = [p.relative_to(baseline).as_posix() for p in baseline.rglob('*') if p.is_file()]
    support = [
        'docs/FOGUEIRA_RODA_V1.md',
        'tools/arauna_maps/validate_fogueira_roda_v1.py',
        'tools/arauna_maps/render_fogueira_roda_v1.py',
        'tools/arauna_maps/check_interiors_native_encoding_v1.py',
        'tools/arauna_maps/instalar_fogueira_roda_v1.py',
        'tools/arauna_maps/package_fogueira_roda_v1.py',
        'tools/arauna_maps/test_fogueira_roda_package_v1.py',
    ] + [p.relative_to(ROOT).as_posix() for p in baseline.rglob('*') if p.is_file()]
    manifest = {'version': 1, 'title': TITLE, 'files': {}, 'dependencies': {}}
    for relative in sorted(owned + support):
        src = ROOT / relative; dst = package / 'payload' / relative
        dst.parent.mkdir(parents=True, exist_ok=True); shutil.copy2(src, dst)
        manifest['files'][relative] = {'before': sha(baseline / relative) if relative in owned else None, 'after': sha(src)}
    layouts = {l['id']: l for l in json.loads((ROOT / 'data/layouts/layouts.json').read_text())['layouts']}
    for suffix in ('Entrada', 'Memorial', 'Salao'):
        rel = 'data/maps/Arauna_CasaFogueira_' + suffix + '/map.json'
        m = json.loads((ROOT / rel).read_text()); l = layouts[m['layout']]
        for path in (l['blockdata_filepath'], l['border_filepath']): manifest['dependencies'][path] = sha(ROOT / path)
        if suffix != 'Salao': manifest['dependencies'][rel] = sha(ROOT / rel)
    for p in (ROOT / 'data/tilesets/secondary/arauna_fogueira').rglob('*'):
        if p.is_file():
            relative = p.relative_to(ROOT).as_posix()
            if relative not in owned: manifest['dependencies'][relative] = sha(p)
    text = (ROOT / 'include/constants/flags.h').read_text()
    manifest['flags_block'] = re.search(r'// BEGIN ARAUNA FOGUEIRA RODA V1.*?// END ARAUNA FOGUEIRA RODA V1', text, re.S)[0]
    (package / 'manifest.json').write_text(json.dumps(manifest, indent=2) + '\n')
    shutil.copy2(ROOT / 'tools/arauna_maps/instalar_fogueira_roda_v1.py', package / 'instalar_fogueira_roda_v1.py')
    shutil.copy2(ROOT / 'docs/FOGUEIRA_RODA_V1.md', package / 'LEIA_FOGUEIRA_RODA_V1.md')
    review = package / 'revisao'; review.mkdir()
    for name in ('validation.json', 'native_encoding_37_banks.json', 'package_validation.json'):
        shutil.copy2(ROOT / 'review/fogueira_roda_v1' / name, review / name)
    shutil.copy2(args.output_dir / 'Arauna_Fogueira_Roda_V1_Comparacao.png', review / 'Arauna_Fogueira_Roda_V1_Comparacao.png')
    shutil.copy2(args.output_dir / 'fogueira_concept_reference.png', review / 'concept_fornecido.png')
    checksums = {p.relative_to(package).as_posix(): sha(p) for p in package.rglob('*') if p.is_file()}
    (package / 'SHA256_MANIFEST.json').write_text(json.dumps(checksums, indent=2) + '\n')
    archive = args.output_dir / (TITLE + '.zip')
    with zipfile.ZipFile(archive, 'w', zipfile.ZIP_DEFLATED) as z:
        for p in sorted(package.rglob('*')):
            if p.is_file(): z.write(p, TITLE + '/' + p.relative_to(package).as_posix())
    print(json.dumps({'archive': str(archive), 'bytes': archive.stat().st_size, 'sha256': sha(archive), 'owned_files': len(owned), 'dependencies': len(manifest['dependencies'])}, indent=2))

if __name__ == '__main__': main()
