#!/usr/bin/env python3
"""Exercise the shipped installer, hostile inputs, atomic rollback and reapply."""
import argparse
import importlib.util
import json
import subprocess
import sys
from pathlib import Path
from contests_08e import BASE,PREVIOUS,FIXES,sha,dump


def test(package,target,output):
    package=Path(package).resolve();target=Path(target).resolve()
    manifest=json.loads((package/'manifest.json').read_text());contract=json.loads((package/'source'/manifest['functional_contract']).read_text())
    assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=target,text=True).strip()==BASE
    selected={e['path']:e for e in manifest['files']};old={n:(target/n).read_bytes() if (target/n).is_file() else None for n in selected}
    baseline={**contract['protected_hashes'],**{n:sha(raw) if raw is not None else None for n,raw in old.items()}}
    cases=[]
    def unchanged():
        assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=target,text=True).strip()==BASE
        for n,h in baseline.items():
            p=target/n;assert (sha(p.read_bytes()) if p.is_file() else None)==h,('Unexpected write',n)
    def invoke(check=False):
        return subprocess.run([sys.executable,str(package/'install.py'),str(target)]+(['--check'] if check else []),capture_output=True,text=True)
    def reject(label,relative,raw):
        p=target/relative;before=p.read_bytes();p.write_bytes(raw)
        try:
            r=invoke();assert r.returncode!=0 and 'nothing was written' in r.stderr,(label,r.stderr)
        finally:p.write_bytes(before)
        unchanged();cases.append({'case':label,'status':'PASS','written':0})
    r=invoke(True);assert r.returncode==0,r.stderr;info=json.loads(r.stdout);assert info['written']==0;unchanged();cases.append({'case':'preflight writes zero','status':'PASS','files':info['files'],'written':0})
    versions={'src/party_menu.c':'5e51e3b2ba','src/field_player_avatar.c':'646a270fdf','src/scrcmd.c':'646a270fdf',**{n:'5c8f309fd153b707e47a47d2f72780ac12ea0210' for n in FIXES if n.endswith('.inc')}}
    for n,ref in versions.items():
        raw=subprocess.check_output(['git','show',ref+':'+n],cwd=target);assert sha(raw)!=FIXES[n];reject('reject historical '+n,n,raw)
    entry=manifest['files'][0];p=package/'source'/entry['path'];raw=p.read_bytes();p.write_bytes(raw+b'corruption')
    try:
        r=invoke();assert r.returncode!=0 and 'Corrupted package payload' in r.stderr,r.stderr
    finally:p.write_bytes(raw)
    unchanged();cases.append({'case':'reject corrupt source payload','status':'PASS','written':0})
    frozen=json.loads((target/'review/aceitacao_08_auditoria/protected_files.json').read_text())
    clinic='data/tilesets/secondary/arauna_frontier07h_clinic/metatiles.bin'
    assert clinic in contract['protected_hashes'];reject('reject changed protected Clinic',clinic,(target/clinic).read_bytes()+b'bad')
    n='src/contest.c';reject('reject altered contest production code',n,(target/n).read_bytes()+b'bad')
    n='src/data/tilesets/headers.h';reject('reject unknown local registry edit',n,(target/n).read_bytes()+b'bad')
    subprocess.run(['git','switch','--detach',PREVIOUS],cwd=target,capture_output=True,check=True)
    try:
        r=invoke();assert r.returncode!=0 and 'Checkout must be' in r.stderr
    finally:subprocess.run(['git','switch','--detach',BASE],cwd=target,capture_output=True,check=True)
    unchanged();cases.append({'case':'reject obsolete checkout base','status':'PASS','written':0})
    sys.dont_write_bytecode=True
    spec=importlib.util.spec_from_file_location('actual_contests_installer',package/'install.py');module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    atomic=module.write_atomic;calls=0
    def fail_second(path,raw):
        nonlocal calls
        calls+=1
        if calls==2:raise IOError('Injected second write failure')
        atomic(path,raw)
    module.write_atomic=fail_second;argv=sys.argv;sys.argv=[str(package/'install.py'),str(target)]
    try:
        try:module.main()
        except IOError as e:assert 'Injected second write failure' in str(e)
        else:raise AssertionError('Missing injected failure')
    finally:sys.argv=argv
    assert calls==2;unchanged();cases.append({'case':'automatic rollback after second write fails','status':'PASS','restored_entire_checkout':True})
    r=invoke();assert r.returncode==0,r.stderr;info=json.loads(r.stdout);assert info['written']==len(selected),info
    for e in selected.values():assert sha((target/e['path']).read_bytes())==e['sha256']
    for n,h in contract['protected_hashes'].items():assert sha((target/n).read_bytes())==h
    cases.append({'case':'actual installation preserves all dependencies','status':'PASS','written':info['written']})
    r=invoke();assert r.returncode==0,r.stderr;again=json.loads(r.stdout);assert again['written']==0;cases.append({'case':'reapply writes zero','status':'PASS','written':0})
    backup=Path(info['backup']);records=json.loads((backup/'rollback_manifest.json').read_text())
    for record in reversed(records):
        p=target/record['path']
        if record['previously_existed']:p.write_bytes((backup/record['path']).read_bytes())
        else:p.unlink()
    unchanged();cases.append({'case':'manual rollback from shipped backup','status':'PASS','restored_entire_checkout':True})
    result={'status':'PASS','base_commit':BASE,'payload_files':len(selected),'protected_existing_files':len(contract['protected_hashes']),
            'case_count':len(cases),'cases':cases,'head_changed':False,'method':'actual shipped install.py; isolated detached worktree, full before/after file hashes'}
    dump(Path(output),result);print(json.dumps(result,indent=2))


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('package');p.add_argument('target');p.add_argument('output');a=p.parse_args();test(a.package,a.target,a.output)
