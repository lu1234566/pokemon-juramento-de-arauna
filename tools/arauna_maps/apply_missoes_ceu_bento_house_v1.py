#!/usr/bin/env python3
"""Install the additive Casa de Bento layout, with conflict checks and backup."""
import argparse,datetime,hashlib,json,os,tempfile,uuid
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
META=ROOT/'review/missoes_ceu_bento_house_v1/manifest.json'
ID='LAYOUT_ARAUNA_MISSOES_CEU_BENTO_HOUSE'
MARK='MISSOES_CEU_BENTO_HOUSE_V1'
HEADERS=[f'src/data/tilesets/{s}.h' for s in ('graphics','metatiles','headers')]
def sha(raw):return hashlib.sha256(raw).hexdigest()
def encoded(node):return (json.dumps(node,indent=2,ensure_ascii=False)+'\n').encode()
def prepare(target):
    meta=json.loads(META.read_text());edits={}
    for rel in meta['new_files']:
        desired=(ROOT/rel).read_bytes();p=target/rel;current=p.read_bytes() if p.is_file() else None
        if current==desired:continue
        if current is not None:raise ValueError('Conflito em arquivo novo: '+rel)
        edits[rel]=desired
    rel='data/maps/MossdeepCity_StevensHouse/map.json'
    desired=(ROOT/rel).read_bytes();current=(target/rel).read_bytes()
    if current!=desired:
        if sha(current)!=meta['map_baseline']:raise ValueError('Conflito nos eventos da casa: '+rel)
        edits[rel]=desired
    rel='data/layouts/layouts.json';node=json.loads((target/rel).read_text());source=json.loads((ROOT/rel).read_text())
    record=next(r for r in source['layouts'] if r['id']==ID)
    found=[r for r in node['layouts'] if r['id']==ID]
    if not found:node['layouts'].append(record)
    elif len(found)!=1 or found[0]!=record:raise ValueError('Conflito no layout: '+ID)
    value=encoded(node)
    if value!=(target/rel).read_bytes():edits[rel]=value
    for rel in HEADERS:
        current=(target/rel).read_text();desired=(ROOT/rel).read_text()
        start='// '+MARK+'_BEGIN\n';end='// '+MARK+'_END\n'
        assert desired.count(start)==desired.count(end)==1
        body=desired.split(start,1)[1].split(end,1)[0];block=start+body+end
        if block in current:
            if current.count(block)!=1:raise ValueError('Bloco duplicado: '+rel)
            continue
        if start in current or end in current or 'AraunaMissoesCeuBentoHouseV1' in current:
            raise ValueError('Conflito no registro: '+rel)
        edits[rel]=(current.rstrip()+'\n\n'+block).encode()
    return edits
def apply(target,edits):
    if not edits:return None
    stamp=datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%SZ')+'-'+uuid.uuid4().hex[:8]
    backup=target/'.arauna_backups'/('missoes_ceu_bento_house_v1-'+stamp)
    before={rel:(target/rel).read_bytes() if (target/rel).is_file() else None for rel in edits}
    backup.mkdir(parents=True)
    for rel,raw in before.items():
        if raw is not None:
            p=backup/rel;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(raw)
    (backup/'manifest.json').write_text(json.dumps({'modified':[r for r,b in before.items() if b is not None],
                                                     'added':[r for r,b in before.items() if b is None]},indent=2)+'\n')
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
            if before[rel] is None:(target/rel).unlink(missing_ok=True)
            else:(target/rel).write_bytes(before[rel])
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
