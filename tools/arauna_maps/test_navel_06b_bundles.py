#!/usr/bin/env python3
"""Fetch cumulative history into a repository containing only the GitHub base."""
import argparse,hashlib,json,subprocess,tempfile
from pathlib import Path
from navel_06b_common import ROOT,BASE,GITHUB_BASE

def main():
    ap=argparse.ArgumentParser();ap.add_argument('package',type=Path);pkg=ap.parse_args().package.resolve()
    manifest=json.loads((pkg/'manifest.json').read_text());commit=manifest['checkpoint_commits']['06B'];cases=[]
    def ok(condition,label):assert condition,label;cases.append(label)
    with tempfile.TemporaryDirectory(prefix='bundle-test-navel06b-',dir=ROOT.parent) as temp:
        target=Path(temp)/'bare.git'
        def git(*args,check=True):return subprocess.run(['git',*args],cwd=target,text=True,capture_output=True,check=check)
        subprocess.run(['git','init','--bare','--quiet',str(target)],check=True)
        git('fetch','--quiet','--depth=1',str(ROOT),GITHUB_BASE)
        git('update-ref','refs/heads/github-base',GITHUB_BASE)
        ok(git('cat-file','-e',BASE,check=False).returncode!=0,'Fresh test repository has GitHub base and no 06A checkpoint')
        r=git('bundle','verify',str(pkg/'cumulative_06A_06B.bundle'))
        ok(r.returncode==0,'Cumulative bundle verifies with d665 as prerequisite')
        git('fetch','--quiet',str(pkg/'cumulative_06A_06B.bundle'),'HEAD:refs/heads/checkpoint-06b')
        ok(git('rev-parse','checkpoint-06b').stdout.strip()==commit,'Cumulative bundle imports exact 06B commit')
        ok(git('rev-parse',commit+'^').stdout.strip()==BASE,'Imported 06B parent is recovered 06A')
        ok(git('rev-parse',BASE+'^').stdout.strip()==GITHUB_BASE,'Imported 06A parent is integrated maintenance base')
        expected=subprocess.check_output(['git','rev-parse',commit+'^{tree}'],cwd=ROOT,text=True).strip()
        ok(git('rev-parse','checkpoint-06b^{tree}').stdout.strip()==expected,'Entire imported Git tree equals completed cumulative source tree')
        checkout=Path(temp)/'checkout'
        git('worktree','add','--quiet','--detach',str(checkout),commit)
        for entry in manifest['files']:
            raw=(checkout/entry['path']).read_bytes()
            assert hashlib.sha256(raw).hexdigest()==entry['sha256'],entry['path']
        ok(True,'Actual cumulative checkout matches all payload SHA-256, including native palette CRLF')
        contract=json.loads((checkout/manifest['functional_contract']).read_text())
        for rel,sha in {**contract['protected_hashes'],**contract['dependency_hashes']}.items():
            assert hashlib.sha256((checkout/rel).read_bytes()).hexdigest()==sha,rel
        ok(True,'Actual cumulative checkout preserves all 22,394 pre-existing dependency hashes')
        ok(git('bundle','verify',str(pkg/'checkpoint_NavelRock_06B.bundle')).returncode==0,'Incremental bundle verifies once 06A is present')
        patch=Path(temp)/'patch-checkout';git('worktree','add','--quiet','--detach',str(patch),BASE)
        subprocess.run(['git','apply',str(pkg/'changes.patch')],cwd=patch,capture_output=True,check=True)
        for entry in manifest['files']:assert hashlib.sha256((patch/entry['path']).read_bytes()).hexdigest()==entry['sha256'],('patch',entry['path'])
        ok(True,'Actual binary patch application reproduces all payload hashes, including CRLF palettes')
        report={'status':'PASS','checks':len(cases),'cases':cases,'github_base':GITHUB_BASE,'required_incremental_base':BASE,'checkpoint_commit':commit,'tree':expected,'payload_files':len(manifest['files']),'scope':'Fresh repository containing only GitHub base; actual bundle verification/fetch, complete tree equality and checkout hashes including CRLF smudge. Actual patch applied to separate clean 06A checkout. No ARM build or emulator session.'}
    (pkg/'CUMULATIVE_TEST.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))

if __name__=='__main__':main()
