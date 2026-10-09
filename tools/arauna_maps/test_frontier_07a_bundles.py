#!/usr/bin/env python3
"""Independent bundle receivers on 7e9 and 989, preserving all engine fixes."""
import argparse,hashlib,json,subprocess,tempfile
from pathlib import Path
from frontier_07a_common import BASE,PREVIOUS,ROOT

def main():
    ap=argparse.ArgumentParser();ap.add_argument('package',type=Path);pkg=ap.parse_args().package.resolve();manifest=json.loads((pkg/'manifest.json').read_text());commit=manifest['checkpoint_commits']['07A'];cases=[]
    def ok(cond,label):assert cond,label;cases.append(label)
    expected=subprocess.check_output(['git','rev-parse',commit+'^{tree}'],cwd=ROOT,text=True).strip()
    with tempfile.TemporaryDirectory(prefix='bundle-test-frontier07a-',dir=ROOT.parent) as tmp:
        for base,name in [(BASE,'checkpoint_BattleFrontier_07A.bundle'),(PREVIOUS,'cumulative_from_06C2_07A.bundle')]:
            receiver=Path(tmp)/('receiver-'+base[:8]+'.git');subprocess.run(['git','init','--bare','--quiet',str(receiver)],check=True)
            def git(*args,check=True):return subprocess.run(['git',*args],cwd=receiver,capture_output=True,text=True,check=check)
            git('fetch','--quiet','--depth=1',str(ROOT),base);git('update-ref','refs/heads/base',base)
            ok(git('cat-file','-e',commit,check=False).returncode!=0,'Independent '+base[:10]+' receiver starts without 07A')
            if base==PREVIOUS:ok(git('cat-file','-e',BASE,check=False).returncode!=0,'06C2 receiver starts without 7e9 engine corrections')
            ok(git('bundle','verify',str(pkg/name)).returncode==0,name+' verifies on its exact prerequisite')
            git('fetch','--quiet',str(pkg/name),'HEAD:refs/heads/checkpoint')
            ok(git('rev-parse','checkpoint').stdout.strip()==commit and git('rev-parse','checkpoint^{tree}').stdout.strip()==expected,'Import from '+base[:10]+' reaches exact commit and complete tree')
            ok(git('rev-parse',commit+'^').stdout.strip()==BASE,'07A retains authoritative 7e9 as direct parent')
            checkout=Path(tmp)/('checkout-'+base[:8]);git('worktree','add','--quiet','--detach',str(checkout),commit)
            for e in manifest['files']:assert hashlib.sha256((checkout/e['path']).read_bytes()).hexdigest()==e['sha256'],e['path']
            ok(True,'Actual '+base[:10]+' checkout matches every payload SHA including CRLF palettes')
            contract=json.loads((checkout/manifest['functional_contract']).read_text())
            for rel,h in contract['protected_hashes'].items():assert hashlib.sha256((checkout/rel).read_bytes()).hexdigest()==h,rel
            ok(True,'Actual '+base[:10]+' checkout preserves all frozen dependencies and engine fixes')
            if base==PREVIOUS:
                ok(git('rev-parse',BASE+'^').stdout.strip()==PREVIOUS,'Cumulative retains original 989 → 7e9 → 07A history')
            else:
                patch=Path(tmp)/'patch';git('worktree','add','--quiet','--detach',str(patch),BASE);subprocess.run(['git','apply',str(pkg/'changes.patch')],cwd=patch,capture_output=True,check=True)
                for e in manifest['files']:assert hashlib.sha256((patch/e['path']).read_bytes()).hexdigest()==e['sha256'],('patch',e['path'])
                ok(True,'Actual binary patch reproduces every payload SHA on clean 7e9')
        report={'status':'PASS','checks':len(cases),'cases':cases,'base_commit':BASE,'previous_checkpoint':PREVIOUS,'checkpoint_commit':commit,'tree':expected,'payload_files':len(manifest['files']),'scope':'Independent shallow receivers containing only 7e9 or 989. Actual verify/fetch, tree equality, checkout SHA and binary patch. Engine source and the two Trainer Hill door images survive exact. No ARM build or emulator.'}
    (pkg/'CUMULATIVE_TEST.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({'status':'PASS','checks':len(cases)}))

if __name__=='__main__':main()
