#!/usr/bin/env python3
"""Install the two native space-center floors with narrowly scoped JSON merges."""
import argparse,datetime,hashlib,json,os,tempfile,uuid
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
MANIFEST=ROOT/'review/missoes_ceu_space_center_v1/manifest.json'
MARK='MISSOES_CEU_SPACE_CENTER_V1'
SHARED=('data/layouts/layouts.json','src/data/tilesets/graphics.h','src/data/tilesets/metatiles.h','src/data/tilesets/headers.h')

def sha(raw):return hashlib.sha256(raw).hexdigest()
def encoded(node):return (json.dumps(node,indent=2,ensure_ascii=False)+'\n').encode()

def prepare(target):
 meta=json.loads(MANIFEST.read_text());changes={}
 for rel in meta['new_files']:
  desired=(ROOT/rel).read_bytes();p=target/rel;current=p.read_bytes() if p.is_file() else None
  if current==desired:continue
  if current is not None:raise ValueError('Conflito em arquivo novo: '+rel)
  changes[rel]=desired
 rel=SHARED[0];node=json.loads((target/rel).read_text());desired=json.loads((ROOT/rel).read_text())
 for key,baseline in meta['layout_baselines'].items():
  record=next(x for x in node['layouts'] if x['id']==key)
  after=next(x for x in desired['layouts'] if x['id']==key)
  if record==after:continue
  if record!=baseline:raise ValueError('Conflito no layout: '+key)
  record.clear();record.update(after)
 value=encoded(node)
 if value!=(target/rel).read_bytes():changes[rel]=value
 for rel in SHARED[1:]:
  current=(target/rel).read_text();desired=(ROOT/rel).read_text()
  start='// '+MARK+'_BEGIN\n';end='// '+MARK+'_END\n'
  assert desired.count(start)==desired.count(end)==1
  body=desired.split(start,1)[1].split(end,1)[0]
  block=start+body+end
  if block in current:
   if current.count(block)!=1:raise ValueError('Bloco duplicado: '+rel)
   continue
  if start in current or end in current or 'AraunaMissoesCeuSpaceCenterV1' in current:
   raise ValueError('Conflito no registro de tileset: '+rel)
  changes[rel]=(current.rstrip()+'\n\n'+block).encode()
 return changes

def apply(target,changes):
 if not changes:return None
 stamp=datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%SZ')+'-'+uuid.uuid4().hex[:8]
 backup=target/'.arauna_backups'/('missoes_ceu_space_center_v1-'+stamp)
 original={rel:(target/rel).read_bytes() if (target/rel).is_file() else None for rel in changes}
 backup.mkdir(parents=True)
 for rel,raw in original.items():
  if raw is not None:
   p=backup/rel;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(raw)
 (backup/'manifest.json').write_text(json.dumps({'modified':[x for x,b in original.items() if b is not None],
                                                 'added':[x for x,b in original.items() if b is None]},indent=2)+'\n')
 written=[]
 try:
  for rel,raw in changes.items():
   p=target/rel;p.parent.mkdir(parents=True,exist_ok=True)
   with tempfile.NamedTemporaryFile(dir=p.parent,delete=False) as stream:
    temp=Path(stream.name);stream.write(raw)
   try:os.replace(temp,p)
   finally:temp.unlink(missing_ok=True)
   written.append(rel)
 except Exception:
  for rel in reversed(written):
   p=target/rel
   if original[rel] is None:p.unlink(missing_ok=True)
   else:p.write_bytes(original[rel])
  raise
 return backup

def main():
 parser=argparse.ArgumentParser();parser.add_argument('--target',type=Path,required=True)
 parser.add_argument('--check',action='store_true');args=parser.parse_args()
 target=args.target.resolve();changes=prepare(target)
 backup=None if args.check else apply(target,changes)
 print(json.dumps({'status':'PASS','changed_files':len(changes),'check_only':args.check,
                   'backup':str(backup) if backup else None,'files':list(changes)},indent=2))
if __name__=='__main__':main()
