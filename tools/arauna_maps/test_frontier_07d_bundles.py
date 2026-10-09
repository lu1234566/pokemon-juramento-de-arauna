#!/usr/bin/env python3
"""Import all Factory bundles into independent receivers and prove corrected history."""
import argparse,hashlib,json,subprocess,tempfile
from pathlib import Path
from frontier_07d_common import BASE,PREVIOUS,EARLIER,OLDER,ROOT
from package_frontier_07d import BUNDLES

def main():
    ap=argparse.ArgumentParser();ap.add_argument('package',type=Path);pkg=ap.parse_args().package.resolve();manifest=json.loads((pkg/'manifest.json').read_text());commit=manifest['checkpoint_commits']['07D'];cases=[]
    def ok(cond,label):assert cond,label;cases.append(label)
    expected=subprocess.check_output(['git','rev-parse',commit+'^{tree}'],cwd=ROOT,text=True).strip()
    with tempfile.TemporaryDirectory(prefix='arauna-bundle07d-',dir='/tmp') as tmp:
        for name,base in BUNDLES:
            receiver=Path(tmp)/('receiver-'+base[:8]+'.git');subprocess.run(['git','init','--bare','--quiet',str(receiver)],check=True)
            def git(*args,check=True):return subprocess.run(['git',*args],cwd=receiver,capture_output=True,text=True,check=check)
            required=[]
            with (pkg/name).open('rb') as f:
                assert f.readline().startswith(b'# v')
                for line in f:
                    if line==b'\n':break
                    if line.startswith(b'-'):required.append(line[1:].split(b' ')[0].decode())
            for prerequisite in required:assert subprocess.run(['git','merge-base','--is-ancestor',prerequisite,base],cwd=ROOT,capture_output=True).returncode==0
            git('fetch','--quiet','--depth='+str(1 if base==OLDER else 2),str(ROOT),base);git('update-ref','refs/heads/base',base)
            for prerequisite in required:
                if git('cat-file','-e',prerequisite,check=False).returncode:git('fetch','--quiet','--depth=1',str(ROOT),prerequisite)
            ok(True,'Prerequisites are ancestors of the declared base and present in independent receiver')
            ok(git('cat-file','-e',commit,check=False).returncode!=0,'Independent '+base[:10]+' receiver starts without 07D')
            if base!=BASE:ok(git('cat-file','-e',BASE,check=False).returncode!=0,'Receiver starts without official Palace water repair')
            if base==EARLIER:ok(git('cat-file','-e',PREVIOUS,check=False).returncode!=0,'9f receiver starts without 07C')
            if base==OLDER:ok(all(git('cat-file','-e',x,check=False).returncode!=0 for x in (PREVIOUS,EARLIER)),'06C2 receiver starts without newer checkpoints')
            ok(git('bundle','verify',str(pkg/name)).returncode==0,name+' verifies against its base ancestry')
            git('fetch','--quiet',str(pkg/name),'HEAD:refs/heads/checkpoint')
            ok(git('rev-parse','checkpoint').stdout.strip()==commit and git('rev-parse','checkpoint^{tree}').stdout.strip()==expected,'Import reaches exact 07D commit and complete tree')
            ok(git('rev-parse',commit+'^').stdout.strip()==BASE and git('rev-parse',BASE+'^').stdout.strip()==PREVIOUS,'07D directly follows official 8d maintenance after original 07C')
            checkout=Path(tmp)/('checkout-'+base[:8]);git('worktree','add','--quiet','--detach',str(checkout),commit)
            for e in manifest['files']:assert hashlib.sha256((checkout/e['path']).read_bytes()).hexdigest()==e['sha256'],e['path']
            ok(True,'Actual checkout matches every payload hash including CRLF palettes')
            contract=json.loads((checkout/manifest['functional_contract']).read_text())
            for rel,h in contract['protected_hashes'].items():assert hashlib.sha256((checkout/rel).read_bytes()).hexdigest()==h,rel
            ok(True,'Actual checkout preserves all dependencies, Palace water and previous door repairs')
            if base==BASE:
                patch=Path(tmp)/'patch';git('worktree','add','--quiet','--detach',str(patch),BASE);subprocess.run(['git','apply',str(pkg/'changes.patch')],cwd=patch,capture_output=True,check=True)
                for e in manifest['files']:assert hashlib.sha256((patch/e['path']).read_bytes()).hexdigest()==e['sha256'],('patch',e['path'])
                ok(True,'Actual binary patch reproduces every payload hash on 8d');git('worktree','remove','--force',str(patch))
            git('worktree','remove','--force',str(checkout));print(json.dumps({'receiver':base[:10],'checks_so_far':len(cases)}),flush=True)
        report={'status':'PASS','checks':len(cases),'cases':cases,'base_commit':BASE,'previous_checkpoint':PREVIOUS,'earlier_github':EARLIER,'checkpoint_commit':commit,'tree':expected,'payload_files':len(manifest['files']),'scope':'Independent receivers seeded with base and required ancestors, without fetching unavailable older partial-clone blobs. Actual verify/fetch, direct parent, tree, checkout hashes and binary patch. No ARM build or emulator.'}
    (pkg/'CUMULATIVE_TEST.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({'status':'PASS','checks':len(cases)}))

if __name__=='__main__':main()
