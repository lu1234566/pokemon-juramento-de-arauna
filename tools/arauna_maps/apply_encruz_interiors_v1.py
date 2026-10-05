#!/usr/bin/env python3
"""Install fourteen Encruz do Sal interiors without overwriting unrelated layout records."""
import argparse,datetime,hashlib,json,os,tempfile,uuid
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
MANIFEST=ROOT/'review/encruz_interiors_v1/manifest.json'
MARK='ENCRUZ_INTERIORS_V1'
SHARED=('data/layouts/layouts.json','src/data/tilesets/graphics.h','src/data/tilesets/metatiles.h','src/data/tilesets/headers.h')
def sha(raw):return hashlib.sha256(raw).hexdigest()
def encoded(node):return (json.dumps(node,indent=2,ensure_ascii=False)+'\n').encode()

def prepare(target):
 meta=json.loads(MANIFEST.read_text());edits={}
 for rel in meta['new_files']:
  desired=(ROOT/rel).read_bytes();p=target/rel;current=p.read_bytes() if p.is_file() else None
  if current==desired:continue
  if current is not None:raise ValueError('Conflito em arquivo novo: '+rel)
  edits[rel]=desired
 for rel,expected in meta['map_baselines'].items():
  desired=(ROOT/rel).read_bytes();current=(target/rel).read_bytes()
  if current==desired:continue
  if sha(current)!=expected:raise ValueError('Conflito em eventos do mapa: '+rel)
  edits[rel]=desired
 rel=SHARED[0];node=json.loads((target/rel).read_text());source=json.loads((ROOT/rel).read_text())
 for identity in meta['new_layout_ids']:
  desired=next(x for x in source['layouts'] if x['id']==identity)
  current=[x for x in node['layouts'] if x['id']==identity]
  if not current:node['layouts'].append(desired)
  elif len(current)!=1 or current[0]!=desired:raise ValueError('Conflito no layout: '+identity)
 value=encoded(node)
 if value!=(target/rel).read_bytes():edits[rel]=value
 for rel in SHARED[1:]:
  current=(target/rel).read_text();desired=(ROOT/rel).read_text()
  start='// '+MARK+'_BEGIN\n';end='// '+MARK+'_END\n'
  assert desired.count(start)==desired.count(end)==1
  body=desired.split(start,1)[1].split(end,1)[0];block=start+body+end
  if block in current:
   if current.count(block)!=1:raise ValueError('Bloco duplicado: '+rel)
   continue
  if start in current or end in current or any(symbol in current for symbol in ('AraunaEncruzCasas','AraunaEncruzOficina','AraunaEncruzJogos','AraunaEncruzCasaEletrica','AraunaEncruzCentro','AraunaEncruzVenda')):
   raise ValueError('Conflito no registro de tileset: '+rel)
  edits[rel]=(current.rstrip()+'\n\n'+block).encode()
 return edits

def apply(target,edits):
 if not edits:return None
 stamp=datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%SZ')+'-'+uuid.uuid4().hex[:8]
 backup=target/'.arauna_backups'/('encruz_interiors_v1-'+stamp)
 before={rel:(target/rel).read_bytes() if (target/rel).is_file() else None for rel in edits}
 backup.mkdir(parents=True)
 for rel,raw in before.items():
  if raw is not None:
   p=backup/rel;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(raw)
 (backup/'manifest.json').write_text(json.dumps({'modified':[x for x,b in before.items() if b is not None],
                                                 'added':[x for x,b in before.items() if b is None]},indent=2)+'\n')
 written=[]
 try:
  for rel,raw in edits.items():
   p=target/rel;p.parent.mkdir(parents=True,exist_ok=True)
   with tempfile.NamedTemporaryFile(dir=p.parent,delete=False) as stream:
    tmp=Path(stream.name);stream.write(raw)
   try:os.replace(tmp,p)
   finally:tmp.unlink(missing_ok=True)
   written.append(rel)
 except Exception:
  for rel in reversed(written):
   p=target/rel
   if before[rel] is None:p.unlink(missing_ok=True)
   else:p.write_bytes(before[rel])
  raise
 return backup

def main():
 parser=argparse.ArgumentParser();parser.add_argument('--target',type=Path,required=True)
 parser.add_argument('--check',action='store_true');args=parser.parse_args()
 target=args.target.resolve();edits=prepare(target)
 backup=None if args.check else apply(target,edits)
 print(json.dumps({'status':'PASS','changed_files':len(edits),'check_only':args.check,
                   'backup':str(backup) if backup else None,'files':list(edits)},indent=2))
if __name__=='__main__':main()
