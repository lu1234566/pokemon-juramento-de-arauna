#!/usr/bin/env python3
"""Actual cumulative imports from GitHub maintenance and the prior checkpoint."""
import argparse,hashlib,json,subprocess,tempfile
from pathlib import Path
from secret_06c2_common import ROOT,BASE,GITHUB_BASE,PREVIOUS

def main():
    ap=argparse.ArgumentParser();ap.add_argument('package',type=Path);pkg=ap.parse_args().package.resolve()
    manifest=json.loads((pkg/'manifest.json').read_text());commit=manifest['checkpoint_commits']['06C2'];cases=[]
    def ok(condition,label):assert condition,label;cases.append(label)
    with tempfile.TemporaryDirectory(prefix='bundle-test-secret06c2-',dir=ROOT.parent) as temp:
        target=Path(temp)/'github.git';subprocess.run(['git','init','--bare','--quiet',str(target)],check=True)
        def git(*args,check=True):return subprocess.run(['git',*args],cwd=target,text=True,capture_output=True,check=check)
        # GitHub maintenance and its d665 parent; no locally delivered checkpoints.
        git('fetch','--quiet','--depth=2',str(ROOT),GITHUB_BASE);git('update-ref','refs/heads/github-base',GITHUB_BASE)
        ok(all(git('cat-file','-e',h,check=False).returncode!=0 for h in (BASE,PREVIOUS)),'Fresh repository has GitHub maintenance and its parent, without 06C1 or reconciled base')
        ok(git('bundle','verify',str(pkg/'cumulative_06A_06B_06C1_06C2.bundle')).returncode==0,'Full cumulative bundle verifies from GitHub maintenance history')
        git('fetch','--quiet',str(pkg/'cumulative_06A_06B_06C1_06C2.bundle'),'HEAD:refs/heads/checkpoint-06c2')
        ok(git('rev-parse','checkpoint-06c2').stdout.strip()==commit,'Full cumulative bundle imports exact 06C2 commit')
        ok(git('rev-parse',commit+'^').stdout.strip()==BASE,'06C2 parent is the reconciled base')
        ok(git('rev-parse',BASE+'^').stdout.strip()==PREVIOUS,'Reconciliation retains exact recovered 06C1 as first parent')
        ok(git('rev-parse',BASE+'^2').stdout.strip()==GITHUB_BASE,'Reconciliation includes exact GitHub maintenance as second parent')
        ok(git('rev-parse',PREVIOUS+'^').stdout.strip()=='2449e12b0645f9aa37ef261ba2d3ce71df93254a' and git('rev-parse',PREVIOUS+'^^').stdout.strip()=='29ae94cdc2309d099cd0f8ac4fecc4775a6aef72','Imported history retains recovered 06B and 06A')
        expected=subprocess.check_output(['git','rev-parse',commit+'^{tree}'],cwd=ROOT,text=True).strip()
        ok(git('rev-parse','checkpoint-06c2^{tree}').stdout.strip()==expected,'Complete imported tree equals completed cumulative source')
        checkout=Path(temp)/'checkout';git('worktree','add','--quiet','--detach',str(checkout),commit)
        for e in manifest['files']:assert hashlib.sha256((checkout/e['path']).read_bytes()).hexdigest()==e['sha256'],e['path']
        ok(True,'Actual checkout matches every payload hash, including native palette CRLF')
        contract=json.loads((checkout/manifest['functional_contract']).read_text());frozen={**contract['protected_hashes'],**contract['dependency_hashes']}
        for rel,h in frozen.items():assert hashlib.sha256((checkout/rel).read_bytes()).hexdigest()==h,rel
        ok(True,f'Actual checkout preserves all {len(frozen)} reconciled dependencies')
        ok(git('bundle','verify',str(pkg/'checkpoint_SecretBases_06C2.bundle')).returncode==0,'Incremental bundle verifies once the reconciled base is present')
        patch=Path(temp)/'patch';git('worktree','add','--quiet','--detach',str(patch),BASE)
        subprocess.run(['git','apply',str(pkg/'changes.patch')],cwd=patch,capture_output=True,check=True)
        for e in manifest['files']:assert hashlib.sha256((patch/e['path']).read_bytes()).hexdigest()==e['sha256'],('patch',e['path'])
        ok(True,'Actual binary patch reproduces every incremental payload hash')
        # Independent receiver with 06C1 history but without the new maintenance.
        previous_target=Path(temp)/'previous.git';subprocess.run(['git','init','--bare','--quiet',str(previous_target)],check=True)
        def prior(*args,check=True):return subprocess.run(['git',*args],cwd=previous_target,text=True,capture_output=True,check=check)
        prior('fetch','--quiet','--depth=4',str(ROOT),PREVIOUS);prior('update-ref','refs/heads/previous',PREVIOUS)
        ok(prior('cat-file','-e',GITHUB_BASE,check=False).returncode!=0,'Independent 06C1 receiver starts without GitHub maintenance')
        ok(prior('bundle','verify',str(pkg/'cumulative_from_06C1_06C2.bundle')).returncode==0,'Prior-checkpoint cumulative bundle verifies from raw 06C1')
        prior('fetch','--quiet',str(pkg/'cumulative_from_06C1_06C2.bundle'),'HEAD:refs/heads/checkpoint-06c2')
        ok(prior('rev-parse','checkpoint-06c2').stdout.strip()==commit and prior('rev-parse','checkpoint-06c2^{tree}').stdout.strip()==expected,'Prior-checkpoint import reaches the same final commit and entire tree')
        report={'status':'PASS','checks':len(cases),'cases':cases,'github_base':GITHUB_BASE,'previous_checkpoint':PREVIOUS,'required_incremental_base':BASE,'checkpoint_commit':commit,'tree':expected,'payload_files':len(manifest['files']),'scope':'Two independent receivers: GitHub maintenance plus parent, and raw 06C1 history without maintenance. Actual bundle verification/fetch, complete tree equality, checkout hashes including CRLF and actual binary patch. No ARM build or emulator.'}
    (pkg/'CUMULATIVE_TEST.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
if __name__=='__main__':main()
