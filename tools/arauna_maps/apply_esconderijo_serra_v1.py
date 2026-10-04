#!/usr/bin/env python3
"""Install eight Esconderijo da Serra maps into an Arauna tree."""
import argparse
import datetime
import hashlib
import json
import re
import os
import tempfile
import uuid
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
META=ROOT/'review/esconderijo_serra_v1/manifest.json'
MAPS=tuple(p.parent.name for p in sorted((ROOT/'data/maps').glob('MagmaHideout*/map.json')))
IDS=tuple('LAYOUT_ARAUNA_ESCONDERIJO_'+name.split('_',1)[1].upper()+'_V1' for name in MAPS)
PATCHES=(
    ('src/data/tilesets/graphics.h','const u32 gTilesetTiles_AraunaEsconderijoSerra[] =','const u32 gTilesetTiles_AraunaAmanhecer[]'),
    ('src/data/tilesets/metatiles.h','const u16 gMetatiles_AraunaEsconderijoSerra[] =','const u16 gMetatiles_AraunaAmanhecer[]'),
    ('src/data/tilesets/headers.h','const struct Tileset gTileset_AraunaEsconderijoSerra =','const struct Tileset gTileset_AraunaAmanhecer ='),
)


def sha(raw):return hashlib.sha256(raw).hexdigest()
def encode(node):return (json.dumps(node,indent=2,ensure_ascii=False)+'\n').encode()


def declaration_block(source,start,anchor):
    family=re.search(r'_([A-Za-z0-9]+)(?:\[|\s|=)',start).group(1)
    block=source[source.index(start):source.index(anchor)]
    declarations=re.finditer(r'^const[^\n]*?\b(?:gTileset(?:Tiles|Palettes)?_|gMetatiles_|gMetatileAttributes_)([A-Za-z0-9]+)',block,re.M)
    for declaration in declarations:
        if not declaration.group(1).startswith(family):
            return block[:declaration.start()]
    return block


def prepare(target):
    meta=json.loads(META.read_text());edits={}
    for rel in meta['new_files']:
        desired=(ROOT/rel).read_bytes();p=target/rel
        current=p.read_bytes() if p.is_file() else None
        if current==desired:continue
        if current is not None:raise ValueError('Conflito no arquivo novo: '+rel)
        edits[rel]=desired
    for name in MAPS:
        rel=f'data/maps/{name}/map.json'
        desired=(ROOT/rel).read_bytes();current=(target/rel).read_bytes()
        if current!=desired:
            if sha(current)!=meta['map_baselines'][name]:
                raise ValueError('Conflito nos eventos: '+rel)
            edits[rel]=desired
    for rel,start,anchor in PATCHES:
        source=(ROOT/rel).read_text()
        current=edits.get(rel,(target/rel).read_bytes()).decode()
        assert source.count(start)==source.count(anchor)==1,(rel,'package source')
        block=declaration_block(source,start,anchor)
        if start in current:
            if current.count(start)!=1 or not current[current.index(start):].startswith(block):
                raise ValueError('Conflito na declaração: '+rel)
            continue
        if current.count(anchor)!=1:raise ValueError('Ponto de inserção ausente: '+rel)
        edits[rel]=current.replace(anchor,block+anchor).encode()
    rel='data/layouts/layouts.json'
    node=json.loads((target/rel).read_text())
    source=json.loads((ROOT/rel).read_text())
    for id in IDS:
        record=next(item for item in source['layouts'] if item['id']==id)
        found=[item for item in node['layouts'] if item['id']==id]
        if not found:node['layouts'].append(record)
        elif len(found)!=1 or found[0]!=record:raise ValueError('Conflito no layout: '+id)
    value=encode(node)
    if value!=(target/rel).read_bytes():edits[rel]=value
    return edits


def apply(target,edits):
    if not edits:return None
    stamp=datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%SZ')+'-'+uuid.uuid4().hex[:8]
    backup=target/'.arauna_backups'/('esconderijo_serra_v1-'+stamp)
    before={rel:(target/rel).read_bytes() if (target/rel).is_file() else None for rel in edits}
    backup.mkdir(parents=True)
    for rel,raw in before.items():
        if raw is not None:
            p=backup/rel;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(raw)
    (backup/'manifest.json').write_text(json.dumps({'modified':[rel for rel,raw in before.items() if raw is not None],
                                                     'added':[rel for rel,raw in before.items() if raw is None]},indent=2)+'\n')
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
    parser=argparse.ArgumentParser()
    parser.add_argument('--target',type=Path,required=True)
    parser.add_argument('--check',action='store_true')
    args=parser.parse_args()
    target=args.target.resolve();edits=prepare(target)
    backup=None if args.check else apply(target,edits)
    print(json.dumps({'status':'PASS','changed_files':len(edits),'check_only':args.check,
                      'backup':str(backup) if backup else None,'files':list(edits)},indent=2))


if __name__=='__main__':main()
