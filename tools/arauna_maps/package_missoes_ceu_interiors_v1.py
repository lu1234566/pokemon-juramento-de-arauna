#!/usr/bin/env python3
"""Package and sequence-test seven Missões do Céu domestic/service interiors."""
import hashlib,json,shutil,subprocess,sys,tempfile,zipfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];OUT=ROOT.parent/'output'
NAME='Pokemon_Juramento_de_Arauna_Missoes_do_Ceu_Interiores_V1_Concept_review'
EXTERIOR=ROOT.parent/'recovered/Pokemon_Juramento_de_Arauna_Missoes_do_Ceu_V2_Concept_review.zip'
CENTER=OUT/'Pokemon_Juramento_de_Arauna_Missoes_do_Ceu_Centro_Espacial_V1_Concept_review.zip'
SHARED=['data/layouts/layouts.json']+[f'src/data/tilesets/{x}.h' for x in ('graphics','metatiles','headers')]
def sha(data):return hashlib.sha256(data).hexdigest()
def run(cmd,cwd):
 p=subprocess.run(cmd,cwd=cwd,capture_output=True,text=True)
 if p.returncode:raise RuntimeError(f'{cmd}: {p.stdout}\n{p.stderr}')
 return p.stdout
def stage(dest):
 meta=json.loads((ROOT/'review/missoes_ceu_interiors_v1/manifest.json').read_text())
 for rel in meta['new_files']+list(meta['map_baselines'])+SHARED:
  p=dest/rel;p.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(ROOT/rel,p)
 for src,dst in [('missoes_ceu_interiors_v1_7_ambientes.png','MISSOES_CEU_SET_INTERIORES_V1.png'),
                 ('missoes_ceu_interiors_v1_comparison.png','MISSOES_CEU_INTERIORES_V1_COMPARACAO.png')]:
  shutil.copy2(OUT/src,dest/dst)
def unpack(path,dest):
 with zipfile.ZipFile(path) as z:assert z.testzip() is None;z.extractall(dest)
 return next(dest.iterdir())
def archive(folder,dest):
 with zipfile.ZipFile(dest,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
  for p in sorted(folder.rglob('*')):
   if p.is_file():z.write(p,str(Path(NAME)/p.relative_to(folder)))
def check_install(package,target):
 installer=package/'tools/arauna_maps/apply_missoes_ceu_interiors_v1.py'
 before=json.loads(run([sys.executable,str(installer),'--target',str(target),'--check'],package))
 assert before['changed_files']>=60
 after=json.loads(run([sys.executable,str(installer),'--target',str(target)],package))
 assert after['changed_files']==before['changed_files'] and Path(after['backup']).is_dir()
 assert json.loads(run([sys.executable,str(installer),'--target',str(target),'--check'],package))['changed_files']==0
 run(['python3','tools/arauna_maps/validate_missoes_ceu_space_center_v1.py'],target)
 run(['python3','tools/arauna_maps/validate_missoes_ceu_interiors_v1.py'],target)
 output=target.parent/'mapjson';output.mkdir(exist_ok=True)
 names=[f'MossdeepCity_House{i}' for i in range(1,5)]+['MossdeepCity_Mart','MossdeepCity_PokemonCenter_1F','MossdeepCity_PokemonCenter_2F']
 for name in names:
  run([str(ROOT/'tools/mapjson/mapjson'),'map','emerald',f'data/maps/{name}/map.json',
       'data/layouts/layouts.json',str(output)+'/'],target)
 run(['python3','tools/arauna_maps/build_missoes_ceu_interiors_v1.py'],target)
 assert json.loads(run([sys.executable,str(installer),'--target',str(target),'--check'],package))['changed_files']==0
 conflict=target/'data/maps/MossdeepCity_House1/map.json';conflict.write_bytes(conflict.read_bytes()+b'conflict')
 p=subprocess.run([sys.executable,str(installer),'--target',str(target),'--check'],cwd=package,capture_output=True,text=True)
 assert p.returncode and 'Conflito' in p.stderr
 return {'changed_files':after['changed_files'],'backup':True,'idempotence':True,
         'conflict_rejected':True,'mapjson_7':True,'native_path_validation':True}
def integration(package):
 with tempfile.TemporaryDirectory(prefix='arauna-missoes-interiors-install-') as temp:
  root=Path(temp);center=unpack(CENTER,root/'center')
  exterior=unpack(EXTERIOR,root/'exterior') if EXTERIOR.is_file() else None
  variants=[('center_only',False)]
  if exterior:variants.append(('exterior_then_center',True))
  reports={}
  for label,with_exterior in variants:
   target=root/label
   run(['git','worktree','add','--detach',str(target),'HEAD'],ROOT)
   try:
    if with_exterior:
     run([sys.executable,str(exterior/'tools/arauna_maps/apply_missoes_ceu_v2.py'),'--target',str(target)],exterior)
    run([sys.executable,str(center/'tools/arauna_maps/apply_missoes_ceu_space_center_v1.py'),'--target',str(target)],center)
    reports[label]=check_install(package,target)
   finally:run(['git','worktree','remove','--force',str(target)],ROOT)
  return {'status':'PASS','sequences':reports,'rom_build':False,'emulator_test':False}
def main():
 OUT.mkdir(exist_ok=True)
 with tempfile.TemporaryDirectory(prefix='arauna-missoes-interiors-pack-') as temp:
  staged=Path(temp)/NAME;stage(staged)
  result=integration(staged)
  report=ROOT/'review/missoes_ceu_interiors_v1/integration.json';report.write_text(json.dumps(result,indent=2)+'\n')
  shutil.copy2(report,staged/'review/missoes_ceu_interiors_v1/integration.json')
  hashes={str(p.relative_to(staged)):sha(p.read_bytes()) for p in staged.rglob('*') if p.is_file()}
  (staged/'SHA256_MANIFEST.json').write_text(json.dumps(hashes,indent=2)+'\n')
  dest=OUT/(NAME+'.zip');archive(staged,dest)
  with zipfile.ZipFile(dest) as z:
   assert z.testzip() is None
   assert all(sha(z.read(NAME+'/'+rel))==h for rel,h in hashes.items())
  print(json.dumps({'archive':str(dest),'bytes':dest.stat().st_size,
                    'sha256':sha(dest.read_bytes()),'integration':result},indent=2))
if __name__=='__main__':main()
