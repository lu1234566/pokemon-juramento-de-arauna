#!/usr/bin/env python3
"""Package and sequence-test sixteen Serra do Uivo interiors."""
import hashlib,json,shutil,subprocess,sys,tempfile,zipfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];OUT=ROOT.parent/'output'
NAME='Pokemon_Juramento_de_Arauna_Serra_do_Uivo_Interiores_V1_Concept_review'
SHARED=['data/layouts/layouts.json']+[f'src/data/tilesets/{x}.h' for x in ('graphics','metatiles','headers')]
def sha(data):return hashlib.sha256(data).hexdigest()
def run(cmd,cwd):
 p=subprocess.run(cmd,cwd=cwd,capture_output=True,text=True)
 if p.returncode:raise RuntimeError(f'{cmd}: {p.stdout}\n{p.stderr}')
 return p.stdout
def stage(dest):
 meta=json.loads((ROOT/'review/serra_interiors_v1/manifest.json').read_text())
 for rel in meta['new_files']+list(meta['map_baselines'])+SHARED:
  p=dest/rel;p.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(ROOT/rel,p)
 shutil.copy2(OUT/'serra_interiors_v1_16_ambientes.png',dest/'SERRA_DO_UIVO_INTERIORES_V1.png')
def unpack(path,dest):
 with zipfile.ZipFile(path) as z:assert z.testzip() is None;z.extractall(dest)
 return next(dest.iterdir())
def archive(folder,dest):
 with zipfile.ZipFile(dest,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
  for p in sorted(folder.rglob('*')):
   if p.is_file():z.write(p,str(Path(NAME)/p.relative_to(folder)))
def check_install(package,target):
 installer=package/'tools/arauna_maps/apply_serra_interiors_v1.py'
 before=json.loads(run([sys.executable,str(installer),'--target',str(target),'--check'],package))
 assert before['changed_files']>=35
 after=json.loads(run([sys.executable,str(installer),'--target',str(target)],package))
 assert after['changed_files']==before['changed_files'] and Path(after['backup']).is_dir()
 assert json.loads(run([sys.executable,str(installer),'--target',str(target),'--check'],package))['changed_files']==0
 run(['python3','tools/arauna_maps/validate_serra_interiors_v1.py'],target)
 output=target.parent/'mapjson';output.mkdir(exist_ok=True)
 names=[p.split('/')[2] for p in json.loads((package/'review/serra_interiors_v1/manifest.json').read_text())['map_baselines']]
 for name in names:
  run([str(ROOT/'tools/mapjson/mapjson'),'map','emerald',f'data/maps/{name}/map.json',
       'data/layouts/layouts.json',str(output)+'/'],target)
 run(['python3','tools/arauna_maps/build_serra_interiors_v1.py'],target)
 assert json.loads(run([sys.executable,str(installer),'--target',str(target),'--check'],package))['changed_files']==0
 conflict=target/'data/maps/RustboroCity_House1/map.json';conflict.write_bytes(conflict.read_bytes()+b'conflict')
 p=subprocess.run([sys.executable,str(installer),'--target',str(target),'--check'],cwd=package,capture_output=True,text=True)
 assert p.returncode and 'Conflito' in p.stderr
 return {'changed_files':after['changed_files'],'backup':True,'idempotence':True,
         'conflict_rejected':True,'mapjson_16':True,'native_path_validation':True}
def integration(package):
 with tempfile.TemporaryDirectory(prefix='arauna-serra-interiors-install-') as temp:
  root=Path(temp);target=root/'clean_head'
  reports={}
  try:
   run(['git','worktree','add','--detach',str(target),'HEAD'],ROOT)
   reports['clean_head']=check_install(package,target)
  finally:
   if target.exists():run(['git','worktree','remove','--force',str(target)],ROOT)
  return {'status':'PASS','sequences':reports,'rom_build':False,'emulator_test':False}
def main():
 OUT.mkdir(exist_ok=True)
 with tempfile.TemporaryDirectory(prefix='arauna-serra-interiors-pack-') as temp:
  staged=Path(temp)/NAME;stage(staged)
  result=integration(staged)
  report=ROOT/'review/serra_interiors_v1/integration.json';report.write_text(json.dumps(result,indent=2)+'\n')
  shutil.copy2(report,staged/'review/serra_interiors_v1/integration.json')
  hashes={str(p.relative_to(staged)):sha(p.read_bytes()) for p in staged.rglob('*') if p.is_file()}
  (staged/'SHA256_MANIFEST.json').write_text(json.dumps(hashes,indent=2)+'\n')
  dest=OUT/(NAME+'.zip');archive(staged,dest)
  with zipfile.ZipFile(dest) as z:
   assert z.testzip() is None
   assert all(sha(z.read(NAME+'/'+rel))==h for rel,h in hashes.items())
  print(json.dumps({'archive':str(dest),'bytes':dest.stat().st_size,
                    'sha256':sha(dest.read_bytes()),'integration':result},indent=2))
if __name__=='__main__':main()
