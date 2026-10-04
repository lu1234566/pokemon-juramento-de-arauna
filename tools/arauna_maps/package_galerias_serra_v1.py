#!/usr/bin/env python3
"""Stage, install-test and zip the incremental Route 126 ancestral waters layout."""
import hashlib,json,shutil,subprocess,sys,tempfile,zipfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];OUT=ROOT.parent/'output'
NAME='Pokemon_Juramento_de_Arauna_Galerias_Serra_V1_Concept_review'
def sha(data):return hashlib.sha256(data).hexdigest()
def run(args,cwd):
    p=subprocess.run(args,cwd=cwd,capture_output=True,text=True)
    if p.returncode:raise RuntimeError(f'{args}: {p.stdout}\n{p.stderr}')
    return p.stdout
def stage(dest):
    meta=json.loads((ROOT/'review/galerias_serra_v1/manifest.json').read_text())
    for rel in meta['new_files']+['data/maps/RusturfTunnel/map.json','data/layouts/layouts.json','src/graphics.c','src/data/tilesets/graphics.h','src/data/tilesets/metatiles.h','src/data/tilesets/headers.h']:
        p=dest/rel;p.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(ROOT/rel,p)
    shutil.copy2(OUT/'galerias_serra_v1_comparacao.png',dest/'GALERIAS_SERRA_V1_COMPARACAO.png')
def integration(package):
    with tempfile.TemporaryDirectory(prefix='arauna-route126-install-') as temp:
        target=Path(temp)/'clean_head'
        run(['git','worktree','add','--detach',str(target),'HEAD'],ROOT)
        try:
            installer=package/'tools/arauna_maps/apply_galerias_serra_v1.py'
            before=json.loads(run([sys.executable,str(installer),'--target',str(target),'--check'],package))
            assert before['changed_files']>=50
            after=json.loads(run([sys.executable,str(installer),'--target',str(target)],package))
            assert after['changed_files']==before['changed_files'] and Path(after['backup']).is_dir()
            assert json.loads(run([sys.executable,str(installer),'--target',str(target),'--check'],package))['changed_files']==0
            run(['python3','tools/arauna_maps/validate_galerias_serra_v1.py'],target)
            folder=Path(temp)/'mapjson';folder.mkdir()
            run([str(ROOT/'tools/mapjson/mapjson'),'map','emerald','data/maps/RusturfTunnel/map.json',
                 'data/layouts/layouts.json',str(folder)+'/'],target)
            run(['python3','tools/arauna_maps/build_galerias_serra_v1.py'],target)
            assert json.loads(run([sys.executable,str(installer),'--target',str(target),'--check'],package))['changed_files']==0
            p=target/'data/maps/RusturfTunnel/map.json';p.write_bytes(p.read_bytes()+b'conflict')
            error=subprocess.run([sys.executable,str(installer),'--target',str(target),'--check'],cwd=package,capture_output=True,text=True)
            assert error.returncode and 'Conflito' in error.stderr
            return {'status':'PASS','changed_files':after['changed_files'],'backup':True,
                    'idempotence':True,'conflict_rejected':True,'mapjson':True,
                    'native_validation':True,'rom_build':False,'emulator_test':False}
        finally:run(['git','worktree','remove','--force',str(target)],ROOT)
def main():
    OUT.mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='arauna-route126-pack-') as temp:
        staged=Path(temp)/NAME;stage(staged)
        result=integration(staged)
        report=ROOT/'review/galerias_serra_v1/integration.json';report.write_text(json.dumps(result,indent=2)+'\n')
        shutil.copy2(report,staged/'review/galerias_serra_v1/integration.json')
        hashes={str(p.relative_to(staged)):sha(p.read_bytes()) for p in staged.rglob('*') if p.is_file()}
        (staged/'SHA256_MANIFEST.json').write_text(json.dumps(hashes,indent=2)+'\n')
        dest=OUT/(NAME+'.zip')
        with zipfile.ZipFile(dest,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
            for p in sorted(staged.rglob('*')):
                if p.is_file():z.write(p,str(Path(NAME)/p.relative_to(staged)))
        with zipfile.ZipFile(dest) as z:
            assert z.testzip() is None
            assert all(sha(z.read(NAME+'/'+rel))==h for rel,h in hashes.items())
        print(json.dumps({'archive':str(dest),'bytes':dest.stat().st_size,
                          'sha256':sha(dest.read_bytes()),'integration':result},indent=2))
if __name__=='__main__':main()
