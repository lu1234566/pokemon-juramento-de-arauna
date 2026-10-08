#!/usr/bin/env python3
"""Immutable base contract for Dive, surface endpoints and prior checkpoints."""
import argparse,hashlib,json,re,subprocess
from pathlib import Path
from dive_04_common import BASE,ROOT,OUT,MUTABLE,NAMES,inventory

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--base',type=Path,required=True);a=ap.parse_args();base=a.base.resolve()
 assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=base,text=True).strip()==BASE
 node,ls,maps=inventory(base);files=subprocess.check_output(['git','ls-files','data','src','include','graphics'],cwd=base,text=True).splitlines()
 data={'base_commit':BASE,'protected_hashes':{n:hashlib.sha256((base/n).read_bytes()).hexdigest() for n in files if n not in MUTABLE},'mutable_baseline_hashes':{n:hashlib.sha256((base/n).read_bytes()).hexdigest() for n in sorted(MUTABLE)},'maps':{n:{'map':maps[n],'layout':ls[maps[n]['layout']]} for n in NAMES+('Route103','Route111','Route107')},'dependency_hashes':{}}
 extra=set()
 for p in (base/'src').rglob('*.h'):
  extra.update(rel for rel in re.findall(r'INCBIN_\w+\("([^"]+)"\)',p.read_text(errors='ignore')) if rel.startswith('review/') and (base/rel).is_file())
 extra.add('art/cavernas_03a/minerais_atlas.png')
 # All reference assets remain exact; no invented canonicity for new motifs.
 extra.update(p.relative_to(base).as_posix() for p in (base/'docs/referencias/bible_concepts_recuperados').rglob('*') if p.is_file())
 data['dependency_hashes']={rel:hashlib.sha256((base/rel).read_bytes()).hexdigest() for rel in sorted(extra)}
 data['items']=[{'map':n,**e} for n in NAMES for e in maps[n]['bg_events'] if e['type']=='hidden_item']
 data['scope']='Native maps, collision/elevation/behaviors, events, scripts, Dive/emerge endpoints, flags, items, encounters and all previous banks stay byte-identical. Controlled draw-only assets and two scoped rendering hooks are audited separately.'
 OUT.mkdir(parents=True,exist_ok=True);target=OUT/'functional_contract.json';raw=json.dumps(data,indent=2,sort_keys=True)+'\n'
 if target.exists():assert target.read_text()==raw,'Different frozen contract'
 else:target.write_text(raw)
 print(json.dumps({'protected':len(data['protected_hashes']),'dependencies':len(data['dependency_hashes']),'dive_maps':len(NAMES),'hidden_items':len(data['items'])}))

if __name__=='__main__':main()
