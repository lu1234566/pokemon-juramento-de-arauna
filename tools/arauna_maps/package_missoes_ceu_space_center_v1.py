#!/usr/bin/env python3
"""Package and install-test the native space-center interior slice."""
import hashlib,json,shutil,subprocess,sys,tempfile,zipfile
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT.parent/'output'
NAME='Pokemon_Juramento_de_Arauna_Missoes_do_Ceu_Centro_Espacial_V1_Concept_review'
PRIOR=ROOT.parent/'recovered/Pokemon_Juramento_de_Arauna_Missoes_do_Ceu_V2_Concept_review.zip'
SHARED=['data/layouts/layouts.json']+[f'src/data/tilesets/{x}.h' for x in ('graphics','metatiles','headers')]

def sha(data):return hashlib.sha256(data).hexdigest()
def run(args,cwd):
 p=subprocess.run(args,cwd=cwd,text=True,capture_output=True)
 if p.returncode:raise RuntimeError(f'{args}: {p.stdout}\n{p.stderr}')
 return p.stdout
def stage(dest):
 manifest=json.loads((ROOT/'review/missoes_ceu_space_center_v1/manifest.json').read_text())
 for rel in manifest['new_files']+SHARED:
  src=ROOT/rel;dst=dest/rel;dst.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(src,dst)
 shutil.copy2(OUT/'missoes_ceu_space_center_v1_comparison.png',dest/'CENTRO_ESPACIAL_V1_PREVIEW.png')
 return manifest
def archive(stage,path):
 with zipfile.ZipFile(path,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
  for p in sorted(stage.rglob('*')):
   if p.is_file():z.write(p,str(Path(NAME)/p.relative_to(stage)))
def install_check(package,target):
 installer=package/'tools/arauna_maps/apply_missoes_ceu_space_center_v1.py'
 before=json.loads(run([sys.executable,str(installer),'--target',str(target),'--check'],package))
 assert before['changed_files']>=50
 installed=json.loads(run([sys.executable,str(installer),'--target',str(target)],package))
 assert installed['changed_files']==before['changed_files'] and Path(installed['backup']).is_dir()
 assert json.loads(run([sys.executable,str(installer),'--target',str(target),'--check'],package))['changed_files']==0
 for rel in ('data/layouts/MossdeepCity_SpaceCenter_1F_Arauna/map.bin',
             'data/layouts/MossdeepCity_SpaceCenter_2F_Arauna/map.bin'):
  assert (target/rel).read_bytes()==(package/rel).read_bytes()
 run(['python3','tools/arauna_maps/validate_missoes_ceu_space_center_v1.py'],target)
 out=target.parent/'mapjson';out.mkdir(exist_ok=True)
 for floor in ('1F','2F'):
  run([str(ROOT/'tools/mapjson/mapjson'),'map','emerald',f'data/maps/MossdeepCity_SpaceCenter_{floor}/map.json',
       'data/layouts/layouts.json',str(out)+'/'],target)
 run(['python3','tools/arauna_maps/build_missoes_ceu_space_center_v1.py'],target)
 assert json.loads(run([sys.executable,str(installer),'--target',str(target),'--check'],package))['changed_files']==0
 changed=target/'data/layouts/MossdeepCity_SpaceCenter_1F_Arauna/map.bin';changed.write_bytes(changed.read_bytes()+b'conflict')
 p=subprocess.run([sys.executable,str(installer),'--target',str(target),'--check'],cwd=package,text=True,capture_output=True)
 assert p.returncode and 'Conflito' in p.stderr
 return {'new_files':installed['changed_files'],'backup':True,'idempotence':True,'conflict_rejected':True,
         'mapjson':True,'native_path_validation':True}
def integration(package):
 with tempfile.TemporaryDirectory(prefix='arauna-space-center-install-') as temp:
  parent=Path(temp);target=parent/'clean'
  run(['git','worktree','add','--detach',str(target),'HEAD'],ROOT)
  try:
   direct=install_check(package,target)
  finally:run(['git','worktree','remove','--force',str(target)],ROOT)
  prior_status='unavailable'
  if PRIOR.is_file():
   with zipfile.ZipFile(PRIOR) as z:
    assert z.testzip() is None;z.extractall(parent/'prior')
   p=next((parent/'prior').iterdir());target=parent/'after_exterior'
   run(['git','worktree','add','--detach',str(target),'HEAD'],ROOT)
   try:
    exterior=p/'tools/arauna_maps/apply_missoes_ceu_v2.py'
    run([sys.executable,str(exterior),'--target',str(target)],p)
    install_check(package,target);prior_status='PASS'
   except RuntimeError as err:
    prior_status='BLOCKED_BY_PRIOR_BASE: '+str(err).split('\n')[0][:170]
   finally:run(['git','worktree','remove','--force',str(target)],ROOT)
 return {'status':'PASS','clean_main':direct,'after_missoes_exterior_v2':prior_status,
         'rom_build':False,'emulator_test':False}
def main():
 OUT.mkdir(exist_ok=True)
 with tempfile.TemporaryDirectory(prefix='arauna-space-center-pack-') as temp:
  staged=Path(temp)/NAME;stage(staged)
  result=integration(staged)
  report=ROOT/'review/missoes_ceu_space_center_v1/integration.json'
  report.write_text(json.dumps(result,indent=2)+'\n')
  shutil.copy2(report,staged/'review/missoes_ceu_space_center_v1/integration.json')
  manifest={str(p.relative_to(staged)):sha(p.read_bytes()) for p in staged.rglob('*') if p.is_file()}
  (staged/'SHA256_MANIFEST.json').write_text(json.dumps(manifest,indent=2)+'\n')
  dest=OUT/(NAME+'.zip');archive(staged,dest)
  with zipfile.ZipFile(dest) as z:
   assert z.testzip() is None
   assert all(sha(z.read(NAME+'/'+rel))==value for rel,value in manifest.items())
  print(json.dumps({'archive':str(dest),'bytes':dest.stat().st_size,'sha256':sha(dest.read_bytes()),'integration':result},indent=2))
if __name__=='__main__':main()
