#!/usr/bin/env python3
"""Import each cumulative checkpoint and verify its complete tracked tree."""
import argparse
import json
import subprocess
import tempfile
from pathlib import Path
from islands_08d import ROOT,BASE,FIXES,sha,dump
from package_islands_08d import BUNDLES


def test(package,output):
    package=Path(package).resolve();manifest=json.loads((package/'manifest.json').read_text());commit=manifest['checkpoint_commits']['08D']
    expected_tree=subprocess.check_output(['git','rev-parse',commit+'^{tree}'],cwd=ROOT,text=True).strip()
    contract=json.loads((package/'source'/manifest['functional_contract']).read_text());payload={e['path']:e['sha256'] for e in manifest['files']}
    expected={**contract['protected_hashes'],**payload};results=[]
    for index,(name,base) in enumerate(BUNDLES):
        target=Path(tempfile.mkdtemp(prefix='islands08d-bundle-'+str(index)+'-',dir=ROOT.parent));target.rmdir()
        subprocess.run(['git','worktree','add','-q','--detach',str(target),base],cwd=ROOT,check=True)
        try:
            r=subprocess.run(['git','bundle','verify',str(package/name)],cwd=target,capture_output=True,text=True);assert r.returncode==0,(name,r.stderr)
            ref='refs/checkpoint-tests/islands08d-'+str(index)
            subprocess.run(['git','fetch','--no-tags',str(package/name),'HEAD:'+ref],cwd=target,capture_output=True,check=True)
            subprocess.run(['git','switch','-q','--detach',ref],cwd=target,check=True)
            assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=target,text=True).strip()==commit
            assert subprocess.check_output(['git','rev-parse','HEAD^{tree}'],cwd=target,text=True).strip()==expected_tree
            assert subprocess.run(['git','merge-base','--is-ancestor',base,'HEAD'],cwd=target).returncode==0
            tracked=set(subprocess.check_output(['git','ls-files','-z'],cwd=target).decode().rstrip('\0').split('\0'));assert tracked==set(expected),(name,tracked^set(expected))
            for relative,h in expected.items():assert sha((target/relative).read_bytes())==h,(name,relative)
            for relative,h in FIXES.items():assert sha((target/relative).read_bytes())==h
            assert not subprocess.check_output(['git','status','--porcelain'],cwd=target)
            results.append({'bundle':name,'status':'PASS','base_commit':base,'result_commit':commit,'result_tree':expected_tree,
                'tracked_files_verified':len(tracked),'seven_protected_fixes':'PASS','clean_checkout':True})
        finally:subprocess.run(['git','worktree','remove','--force',str(target)],cwd=ROOT,check=True)
    report={'status':'PASS','result_commit':commit,'result_tree':expected_tree,'bundle_count':3,'bundles':results,
        'method':'isolated detached worktrees, shared repository object store; verify/fetch/checkouts/full tracked byte hashes, not an empty clone or recovery from main'}
    dump(Path(output),report);print(json.dumps(report,indent=2))


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('package');p.add_argument('output');a=p.parse_args();test(a.package,a.output)
