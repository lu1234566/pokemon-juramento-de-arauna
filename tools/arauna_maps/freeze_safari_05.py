#!/usr/bin/env python3
"""Freeze the integrated Dive and all gameplay before Safari editing."""
import argparse,hashlib,json,re,subprocess
from pathlib import Path
from safari_05_common import BASE,ROOT,OUT,MUTABLE,NAMES,inventory

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--base',type=Path,required=True);base=ap.parse_args().base.resolve()
 assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=base,text=True).strip()==BASE
 _,ls,maps=inventory(base);files=subprocess.check_output(['git','ls-files','data','src','include','graphics'],cwd=base,text=True).splitlines()
 extra={rel for p in (base/'src').rglob('*.h') for rel in re.findall(r'INCBIN_\w+\("([^"]+)"\)',p.read_text(errors='ignore')) if rel.startswith('review/') and (base/rel).is_file()}
 extra.update(p.relative_to(base).as_posix() for p in (base/'docs/referencias/bible_concepts_recuperados').rglob('*') if p.is_file())
 extra.update(p.relative_to(base).as_posix() for p in (base/'art').rglob('*') if p.is_file())
 sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
 data={'base_commit':BASE,'protected_hashes':{n:sha(base/n) for n in files if n not in MUTABLE},'dependency_hashes':{n:sha(base/n) for n in sorted(extra)},'maps':{n:{'map':maps[n],'layout':ls[maps[n]['layout']]} for n in NAMES},'scope':'All native words, map borders, behaviors, flags, encounters, Safari mechanics, scripts, animations and prior checkpoint assets frozen. Only eight bank assignments and additive tileset declarations change.'}
 OUT.mkdir(parents=True,exist_ok=True);f=OUT/'functional_contract.json';raw=json.dumps(data,indent=2,sort_keys=True)+'\n'
 if f.exists():assert f.read_text()==raw,'Frozen contract mismatch'
 else:f.write_text(raw)
 print(json.dumps({'protected_files':len(data['protected_hashes']),'dependencies':len(extra),'maps':len(NAMES)}))

if __name__=='__main__':main()
