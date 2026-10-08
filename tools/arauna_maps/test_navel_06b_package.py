#!/usr/bin/env python3
"""Exercise the actual shipped installer in an isolated base worktree."""
import argparse,hashlib,importlib.util,json,shutil,subprocess,sys,tempfile
from pathlib import Path
from navel_06b_common import ROOT,BASE,GITHUB_BASE,OUT
sys.dont_write_bytecode=True


def main():
    ap=argparse.ArgumentParser();ap.add_argument('package',type=Path);a=ap.parse_args();pkg=a.package.resolve();manifest=json.loads((pkg/'manifest.json').read_text());checks=[]
    target=Path(tempfile.mkdtemp(prefix='installer-test-navel06b-',dir=ROOT.parent))
    subprocess.run(['git','worktree','add','--detach',str(target),BASE],cwd=ROOT,check=True,capture_output=True)
    rels=[e['path'] for e in manifest['files']]
    initial={rel:(target/rel).read_bytes() if (target/rel).is_file() else None for rel in rels}
    def run(extra=()):return subprocess.run([sys.executable,str(pkg/'install.py'),str(target),*extra],text=True,capture_output=True)
    def intact():return all(((target/p).read_bytes() if (target/p).is_file() else None)==raw for p,raw in initial.items())
    def ok(cond,label):assert cond,label;checks.append(label)
    try:
        result=run(['--check']);ok(result.returncode==0 and json.loads(result.stdout)['written']==0 and intact(),'Dry run verifies all dependencies and writes nothing')
        result=subprocess.run(['git','apply','--check',str(pkg/'changes.patch')],cwd=target,capture_output=True);ok(result.returncode==0,'Binary patch applies cleanly to base')
        rel=manifest['files'][0]['path'];p=pkg/'source'/rel;raw=p.read_bytes();p.write_bytes(raw+b'corrupt')
        result=run();p.write_bytes(raw);ok(result.returncode!=0 and intact() and 'Corrupted package payload' in result.stderr,'Corrupt payload rejected before writes')
        for rel in ['data/layouts/layouts.json', 'data/maps/NavelRock_Down11/map.json', 'data/maps/NavelRock_Harbor/map.json', 'data/maps/NavelRock_Top/scripts.inc', 'data/maps/NavelRock_Bottom/scripts.inc', 'data/layouts/NavelRock_Fork/map.bin', 'data/layouts/NavelRock_LadderRoom1/map.bin', 'src/field_door.c', 'src/script_menu.c', 'src/metatile_behavior.c', 'data/scripts/gift_mystic_ticket.inc', 'src/data/wild_encounters.json', 'data/layouts/AraunaSulPetalburgCityV1/border.bin', 'data/layouts/Underwater_SealedChamber/border.bin', 'data/tilesets/primary/arauna_border_route103_uivo_v1/metatiles.bin', 'review/dive_04/visual_grids/Underwater_Route127.bin', 'review/trainer_hill_06a/functional_contract.json', 'data/tilesets/primary/arauna_trainerhill06a_pavilion/metatiles.bin']:
            p=target/rel;raw=p.read_bytes();p.write_bytes(raw+b'\nLOCAL EDIT\n');result=run();p.write_bytes(raw)
            ok(result.returncode!=0 and intact() and ('Unknown local edit' in result.stderr or 'Changed gameplay dependency' in result.stderr),'Unknown local edit rejected: '+rel)
        entry=next(e for e in manifest['files'] if e['before_sha256'] is None);p=target/entry['path'];p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(b'unknown');result=run();p.unlink()
        ok(result.returncode!=0 and intact() and 'Unknown local edit' in result.stderr,'Unknown existing new-file target rejected')
        main_commit=subprocess.check_output(['git','rev-parse','979fb6c1b6731561f3c993efd6045a9bbf096c54'],cwd=ROOT,text=True).strip()
        subprocess.run(['git','update-ref','HEAD',main_commit],cwd=target,check=True);result=run();subprocess.run(['git','update-ref','HEAD',BASE],cwd=target,check=True)
        ok(result.returncode!=0 and intact() and 'Checkout must be' in result.stderr,'Stale GitHub main refused')
        subprocess.run(['git','update-ref','HEAD',GITHUB_BASE],cwd=target,check=True);result=run();subprocess.run(['git','update-ref','HEAD',BASE],cwd=target,check=True)
        ok(result.returncode!=0 and intact() and 'Checkout must be' in result.stderr,'GitHub integrator without required 06A refused for incremental install')
        spec=importlib.util.spec_from_file_location('checkpoint_install',pkg/'install.py');module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module);original=module.write_atomic
        first_new=next(i+1 for i,e in enumerate(manifest['files']) if e['before_sha256'] is None)
        for failure_at,label in ((3,'Interrupted third write restores old payload files'),(first_new+1,'Interrupted write after creating a new file restores old files and removes new files')):
            counter=[0]
            def interrupted(path,raw):
                counter[0]+=1
                if counter[0]==failure_at:raise OSError('simulated interrupted write')
                original(path,raw)
            module.write_atomic=interrupted;oldargv=sys.argv;sys.argv=['install.py',str(target)]
            try:module.main();raise AssertionError('Injected write failure did not fire')
            except OSError as e:assert str(e)=='simulated interrupted write'
            finally:sys.argv=oldargv
            ok(intact(),label)
        result=run();ok(result.returncode==0 and all(hashlib.sha256((target/e['path']).read_bytes()).hexdigest()==e['sha256'] for e in manifest['files']),'Installation succeeds with complete payload SHA-256')
        backups=list((target/'.arauna-checkpoint-backups').iterdir());result=run();ok(result.returncode==0 and json.loads(result.stdout)['written']==0 and list((target/'.arauna-checkpoint-backups').iterdir())==backups,'Second installation is idempotent, no new backup')
        head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=target,text=True).strip();ok(head==BASE,'Installer preserves Git HEAD')
        contract=json.loads((pkg/'source'/manifest['functional_contract']).read_text());ok(all(hashlib.sha256((target/p).read_bytes()).hexdigest()==sha for p,sha in {**contract['protected_hashes'], **contract.get('dependency_hashes',{})}.items()),'All frozen gameplay and tracked dependencies survive installation')
        result=subprocess.run([sys.executable,'tools/arauna_maps/validate_navel_06b.py','--base',str(ROOT.parent/'arauna-base-06b')],cwd=target,capture_output=True,text=True)
        ok(result.returncode==0,'Installed payload passes native and real-C Navel Rock/selector validation: '+result.stderr[-300:] if result.returncode else 'Installed payload passes native and real-C Navel Rock/selector validation')
        original_hashes={e['path']:hashlib.sha256((target/e['path']).read_bytes()).hexdigest() for e in manifest['files']}
        result=subprocess.run([sys.executable,'tools/arauna_maps/build_navel_06b.py','--base',str(ROOT.parent/'arauna-base-06b')],cwd=target,capture_output=True,text=True)
        ok(result.returncode==0 and all(hashlib.sha256((target/p).read_bytes()).hexdigest()==sha for p,sha in original_hashes.items()),'Installed builder is deterministic and idempotent')
        report={'status':'PASS','checks':len(checks),'cases':checks,'base_commit':BASE,'installer_source':'tools/arauna_maps/install_navel_06b.py','worktree_isolated':True,'protected_gameplay_files':len(contract['protected_hashes']),'other_tracked_dependencies':len(contract['dependency_hashes'])}
        (OUT/'install_test.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
    finally:
        result=subprocess.run(['git','worktree','remove','--force',str(target)],cwd=ROOT,capture_output=True,text=True)
        if result.returncode:
            # Git can unregister the tree before a transient directory-removal
            # failure. Only our unregistered temporary directory may be retried.
            registered=subprocess.check_output(['git','worktree','list','--porcelain'],cwd=ROOT,text=True)
            if 'worktree '+str(target)+'\n' in registered:raise RuntimeError(result.stderr)
            if target.exists():shutil.rmtree(target)
if __name__=='__main__':main()
