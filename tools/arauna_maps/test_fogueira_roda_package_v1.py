#!/usr/bin/env python3
"""Exercise installation from an extracted ZIP on an isolated working copy."""
import argparse, hashlib, json, re, shutil, subprocess, tempfile, zipfile
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
TITLE = 'Pokemon_Juramento_de_Arauna_Fogueira_Roda_V1'

def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()

def main():
    parser = argparse.ArgumentParser(); parser.add_argument('--archive', type=Path, default=ROOT.parent / 'output' / (TITLE + '.zip')); parser.add_argument('--output', type=Path, default=ROOT / 'review/fogueira_roda_v1/package_validation.json'); args = parser.parse_args()
    checks = []
    with tempfile.TemporaryDirectory(prefix='arauna-fogueira-', dir=ROOT.parent) as tmp:
        tmp = Path(tmp)
        with zipfile.ZipFile(args.archive) as z:
            assert all(not Path(n).is_absolute() and '..' not in Path(n).parts for n in z.namelist())
            z.extractall(tmp)
        package = tmp / TITLE
        sums = json.loads((package / 'SHA256_MANIFEST.json').read_text())
        assert all(sha(package / rel) == value for rel, value in sums.items()); checks.append('all extracted files match SHA256 manifest')
        target = tmp / 'target'
        shutil.copytree(ROOT, target, ignore=shutil.ignore_patterns('.git', '.arauna_backups', '__pycache__', 'node_modules'))
        manifest = json.loads((package / 'manifest.json').read_text())
        for rel, item in manifest['files'].items():
            p = target / rel
            if item['before'] is not None: shutil.copy2(package / 'payload/review/fogueira_roda_v1/baseline' / rel, p)
            elif p.exists(): p.unlink()
        flags = target / 'include/constants/flags.h'
        flags.write_text(re.sub(r'// BEGIN ARAUNA FOGUEIRA RODA V1.*?// END ARAUNA FOGUEIRA RODA V1', '', flags.read_text(), flags=re.S) + '\n#define ARAUNA_PACKAGE_QA_PRESERVED 1234\n')
        watched = list(manifest['files']) + ['include/constants/flags.h']
        def fingerprint(): return {rel: sha(target / rel) if (target / rel).exists() else None for rel in watched}
        def install(check=False):
            cmd = ['python3', str(package / 'instalar_fogueira_roda_v1.py'), '--target', str(target)] + (['--check'] if check else [])
            result = subprocess.run(cmd, capture_output=True, text=True)
            return result.returncode, json.loads(result.stdout)
        before = fingerprint(); code, result = install(True)
        assert code == 0 and result['pending_files'] > 0 and fingerprint() == before; checks.append('preflight leaves target unchanged')
        conflict = target / 'data/maps/Arauna_CasaFogueira_Salao/scripts.inc'
        baseline = conflict.read_bytes(); conflict.write_bytes(baseline + b'\n@ local edit\n')
        edited = fingerprint(); code, result = install()
        assert code == 2 and result['written_files'] == 0 and fingerprint() == edited; checks.append('modified script rejected before all mutations')
        conflict.write_bytes(baseline)
        flags_before = flags.read_bytes(); flags.write_bytes(flags_before + b'\n#define FLAG_QA_OTHER_OWNER FLAG_UNUSED_0x040\n')
        edited = fingerprint(); code, result = install()
        assert code == 2 and result['written_files'] == 0 and fingerprint() == edited; checks.append('reserved flag conflict rejected without writes')
        flags.write_bytes(flags_before)
        code, result = install(); assert code == 0
        assert 'ARAUNA_PACKAGE_QA_PRESERVED 1234' in flags.read_text()
        assert all(sha(target / rel) == item['after'] for rel, item in manifest['files'].items())
        backup = Path(result['backup'])
        for rel, item in manifest['files'].items():
            if item['before'] is not None: assert sha(backup / rel) == item['before']
        assert (backup / 'include/constants/flags.h').read_bytes() == flags_before
        checks.append('installation merges own flags and backs up original bytes')
        installed = fingerprint(); code, result = install()
        assert code == 0 and result['written_files'] == 0 and fingerprint() == installed; checks.append('reapplication is a no-op')
        validation = subprocess.run(['python3', str(target / 'tools/arauna_maps/validate_fogueira_roda_v1.py')], cwd=target, capture_output=True, text=True)
        assert validation.returncode == 0, validation.stderr
        scene = json.loads((target / 'review/fogueira_roda_v1/validation.json').read_text())
        reference = json.loads((ROOT / 'review/fogueira_roda_v1/validation.json').read_text())
        assert scene == reference; checks.append('extracted package reproduces all 224 scene paths and event bytes')
        assets = subprocess.run(['python3', str(target / 'tools/arauna_maps/check_interiors_native_encoding_v1.py')], cwd=target, capture_output=True, text=True)
        assert assets.returncode == 0, assets.stderr; checks.append('37-bank format validation passes on restored target')
        checks.append('foreign header content preserved')
        runtime_manifest_sha256 = sha(package / 'manifest.json')
    report = {'status': 'PASS', 'runtime_manifest_sha256': runtime_manifest_sha256, 'checks': checks}
    args.output.write_text(json.dumps(report, indent=2) + '\n'); print(json.dumps(report, indent=2))

if __name__ == '__main__': main()
