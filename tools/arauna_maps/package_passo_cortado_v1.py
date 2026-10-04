#!/usr/bin/env python3
"""Stage, validate, install-test and zip Passo Cortado."""
import hashlib
import json
import shutil
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT.parent/'output'
NAME='Pokemon_Juramento_de_Arauna_Passo_Cortado_V1_Concept_review'
MAPS=('JaggedPass',)


def sha(raw):return hashlib.sha256(raw).hexdigest()


def run(args,cwd):
    process=subprocess.run(args,cwd=cwd,capture_output=True,text=True)
    if process.returncode:raise RuntimeError(f'{args}: {process.stdout}\n{process.stderr}')
    return process.stdout


def stage(dest):
    meta=json.loads((ROOT/'review/passo_cortado_v1/manifest.json').read_text())
    files=meta['new_files']+[f'data/maps/{name}/map.json' for name in MAPS]+[
        'data/layouts/layouts.json','src/data/tilesets/graphics.h',
        'src/data/tilesets/metatiles.h','src/data/tilesets/headers.h']
    for rel in files:
        p=dest/rel;p.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(ROOT/rel,p)
    shutil.copy2(OUT/'passo_cortado_v1_comparacao.png',dest/'PASSO_CORTADO_V1_COMPARACAO.png')


def integration(package):
    with tempfile.TemporaryDirectory(prefix='arauna-passo-install-') as temp:
        target=Path(temp)/'clean_head'
        run(['git','worktree','add','--detach',str(target),'HEAD'],ROOT)
        try:
            installer=package/'tools/arauna_maps/apply_passo_cortado_v1.py'
            before=json.loads(run([sys.executable,str(installer),'--target',str(target),'--check'],package))
            assert before['changed_files']>=35
            after=json.loads(run([sys.executable,str(installer),'--target',str(target)],package))
            assert after['changed_files']==before['changed_files'] and Path(after['backup']).is_dir()
            assert json.loads(run([sys.executable,str(installer),'--target',str(target),'--check'],package))['changed_files']==0
            run(['python3','tools/arauna_maps/validate_passo_cortado_v1.py'],target)
            folder=Path(temp)/'mapjson';folder.mkdir()
            for name in MAPS:
                run([str(ROOT/'tools/mapjson/mapjson'),'map','emerald',f'data/maps/{name}/map.json',
                     'data/layouts/layouts.json',str(folder)+'/'],target)
            run(['python3','tools/arauna_maps/build_passo_cortado_v1.py'],target)
            assert json.loads(run([sys.executable,str(installer),'--target',str(target),'--check'],package))['changed_files']==0
            p=target/'data/maps/JaggedPass/map.json'
            p.write_bytes(p.read_bytes()+b'conflict')
            error=subprocess.run([sys.executable,str(installer),'--target',str(target),'--check'],cwd=package,capture_output=True,text=True)
            assert error.returncode and 'Conflito' in error.stderr
            return {'status':'PASS','changed_files':after['changed_files'],'backup':True,
                    'idempotence':True,'conflict_rejected':True,'mapjson':True,
                    'native_validation':True,'rom_build':False,'emulator_test':False}
        finally:run(['git','worktree','remove','--force',str(target)],ROOT)


def main():
    OUT.mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='arauna-passo-pack-') as temp:
        staged=Path(temp)/NAME;stage(staged)
        result=integration(staged)
        report=ROOT/'review/passo_cortado_v1/integration.json'
        report.write_text(json.dumps(result,indent=2)+'\n')
        shutil.copy2(report,staged/'review/passo_cortado_v1/integration.json')
        hashes={str(p.relative_to(staged)):sha(p.read_bytes()) for p in staged.rglob('*') if p.is_file()}
        (staged/'SHA256_MANIFEST.json').write_text(json.dumps(hashes,indent=2)+'\n')
        dest=OUT/(NAME+'.zip')
        with zipfile.ZipFile(dest,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as archive:
            for p in sorted(staged.rglob('*')):
                if p.is_file():archive.write(p,str(Path(NAME)/p.relative_to(staged)))
        with zipfile.ZipFile(dest) as archive:
            assert archive.testzip() is None
            assert all(sha(archive.read(NAME+'/'+rel))==value for rel,value in hashes.items())
        print(json.dumps({'archive':str(dest),'bytes':dest.stat().st_size,
                          'sha256':sha(dest.read_bytes()),'integration':result},indent=2))


if __name__=='__main__':main()
