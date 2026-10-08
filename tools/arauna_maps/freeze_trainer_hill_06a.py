#!/usr/bin/env python3
"""Freeze the integrated Safari and the October maintenance before native art."""
import argparse,hashlib,json,re,subprocess
from trainer_hill_06a_common import BASE,ROOT,OUT,NAMES,MUTABLE,inventory,floors

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--base',required=True,type=__import__('pathlib').Path);base=ap.parse_args().base.resolve()
    assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=base,text=True).strip()==BASE
    _,ls,maps=inventory(base)
    files=subprocess.check_output(['git','ls-files','data','src','include','graphics'],cwd=base,text=True).splitlines()
    extra={rel for p in (base/'src').rglob('*.h') for rel in re.findall(r'INCBIN_\w+\("([^"]+)"\)',p.read_text(errors='ignore')) if rel.startswith('review/') and (base/rel).is_file()}
    for folder in ('docs/referencias/bible_concepts_recuperados','art'):
        extra.update(p.relative_to(base).as_posix() for p in (base/folder).rglob('*') if p.is_file())
    sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
    data={'base_commit':BASE,'protected_hashes':{n:sha(base/n) for n in files if n not in MUTABLE},'dependency_hashes':{n:sha(base/n) for n in sorted(extra)},'maps':{n:{'map':maps[n],'layout':ls[maps[n]['layout']]} for n in (*NAMES,'BattleFrontier_BattleTowerElevator')},'runtime_floors':floors(base),'scope':'Only six existing layouts have their bank pair reassigned; a private appended elevator layout reuses original grid/border paths. TrainerHill_Elevator changes only its layout reference. All events, scripts, dynamic floor input bytes, code, previous packages, door animation, attributes and original banks stay frozen.'}
    OUT.mkdir(parents=True,exist_ok=True);p=OUT/'functional_contract.json';raw=json.dumps(data,indent=2,sort_keys=True)+'\n'
    if p.exists():assert p.read_text()==raw,'Existing functional contract differs'
    else:p.write_text(raw)
    print(json.dumps({'protected':len(data['protected_hashes']),'dependencies':len(extra),'maps':len(NAMES),'live_runtime_combinations':len(data['runtime_floors'])}))

if __name__=='__main__':main()
