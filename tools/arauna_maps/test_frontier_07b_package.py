#!/usr/bin/env python3
"""Real installation, dependency rejection, rollback and deterministic native art."""
import argparse,hashlib,importlib.util,json,shutil,subprocess,sys,tempfile
from pathlib import Path
from frontier_07b_common import BASE,PREVIOUS,ROOT,OUT

def main():
    ap=argparse.ArgumentParser();ap.add_argument('package',type=Path);pkg=ap.parse_args().package.resolve();manifest=json.loads((pkg/'manifest.json').read_text());checks=[]
    target=Path(tempfile.mkdtemp(prefix='installer-test-frontier07b-',dir=ROOT.parent));subprocess.run(['git','worktree','add','--detach',str(target),BASE],cwd=ROOT,check=True,capture_output=True)
    rels=[e['path'] for e in manifest['files']];initial={n:(target/n).read_bytes() if (target/n).is_file() else None for n in rels}
    def run(check=False):return subprocess.run([sys.executable,str(pkg/'install.py'),str(target),*(['--check'] if check else [])],capture_output=True,text=True)
    def intact():return all(((target/p).read_bytes() if (target/p).is_file() else None)==raw for p,raw in initial.items())
    def ok(cond,label):assert cond,label;checks.append(label)
    try:
        result=run(True);ok(result.returncode==0 and json.loads(result.stdout)['written']==0 and intact(),'Dry run checks complete dependency contract without writes')
        result=subprocess.run(['git','apply','--check',str(pkg/'changes.patch')],cwd=target,capture_output=True);ok(result.returncode==0,'Binary patch applies to exact base')
        rel=manifest['files'][0]['path'];p=pkg/'source'/rel;raw=p.read_bytes();p.write_bytes(raw+b'corrupt');result=run();p.write_bytes(raw)
        ok(result.returncode!=0 and intact() and 'Corrupted package payload' in result.stderr,'Corrupt payload rejected before writes')
        for rel in ['data/layouts/layouts.json', 'src/data/tilesets/headers.h', 'src/field_door.c', 'src/overworld.c', 'src/battle_dome.c', 'src/frontier_util.c', 'src/record_mixing.c', 'src/trainer_hill.c', 'src/secret_base.c', 'include/global.h', 'include/constants/battle_frontier.h', 'data/maps/BattleFrontier_BattleDomeLobby/map.json', 'data/maps/BattleFrontier_BattleDomeLobby/scripts.inc', 'data/maps/BattleFrontier_BattleDomeCorridor/scripts.inc', 'data/maps/BattleFrontier_BattleDomePreBattleRoom/scripts.inc', 'data/maps/BattleFrontier_BattleDomeBattleRoom/scripts.inc', 'data/layouts/BattleFrontier_BattleDomeLobby/map.bin', 'data/layouts/BattleFrontier_BattleDomeLobby/border.bin', 'data/tilesets/secondary/battle_dome/metatiles.bin', 'data/tilesets/secondary/battle_dome/metatile_attributes.bin', 'data/tilesets/secondary/battle_dome/palettes/08.pal', 'src/tileset_anims.c', 'graphics/battle_frontier/dome_anim1.pal', 'graphics/battle_frontier/dome_anim4.pal', 'graphics/door_anims/battle_dome_pre_battle_room.png', 'graphics/door_anims/arauna_trainer_hill_lobby_elevator.png', 'graphics/door_anims/arauna_trainer_hill_roof_elevator.png', 'review/frontier_07a/functional_contract.json', 'data/tilesets/secondary/arauna_frontier07a_tower/tiles.png', 'review/secret_bases_06c2/functional_contract.json', 'review/navel_06b/functional_contract.json', 'review/trainer_hill_06a/functional_contract.json']:
            p=target/rel;raw=p.read_bytes();p.write_bytes(raw+b'\nLOCAL EDIT\n');result=run();p.write_bytes(raw)
            ok(result.returncode!=0 and intact() and ('Unknown local edit' in result.stderr or 'Changed gameplay dependency' in result.stderr),'Reject local edit: '+rel)
        entry=next(e for e in manifest['files'] if e['before_sha256'] is None);p=target/entry['path'];p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(b'unknown');result=run();p.unlink()
        ok(result.returncode!=0 and intact(),'Reject unknown preexisting new target')
        for commit,label in [(PREVIOUS,'GitHub 7e9 before the required 07A Tower checkpoint'),('979fb6c1b6731561f3c993efd6045a9bbf096c54','stale GitHub main'),('872f56e86f09d3dff41a9e6c7a8bc5640386fe86','old GitHub integrator')]:
            subprocess.run(['git','update-ref','HEAD',commit],cwd=target,check=True);result=run();subprocess.run(['git','update-ref','HEAD',BASE],cwd=target,check=True)
            ok(result.returncode!=0 and intact() and 'Checkout must be' in result.stderr,'Reject incremental overlay on '+label)
        spec=importlib.util.spec_from_file_location('install_frontier',pkg/'install.py');module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module);atomic=module.write_atomic
        first_new=next(i+1 for i,e in enumerate(manifest['files']) if e['before_sha256'] is None)
        for failure_at in (3,max(first_new+2,len(manifest['files'])//2)):
            count=[0]
            def interrupted(path,raw):
                count[0]+=1
                if count[0]==failure_at:raise OSError('simulated interrupted write')
                atomic(path,raw)
            module.write_atomic=interrupted;previous=sys.argv;sys.argv=['install.py',str(target)]
            try:module.main();raise AssertionError('Injected failure did not fire')
            except OSError as e:assert str(e)=='simulated interrupted write'
            finally:sys.argv=previous
            ok(intact(),'Rollback restores old files and removes new files after write '+str(failure_at))
        result=run();ok(result.returncode==0 and all(hashlib.sha256((target/e['path']).read_bytes()).hexdigest()==e['sha256'] for e in manifest['files']),'Actual installation reproduces all payload hashes')
        backups=list((target/'.arauna-checkpoint-backups').iterdir());result=run();ok(result.returncode==0 and json.loads(result.stdout)['written']==0 and list((target/'.arauna-checkpoint-backups').iterdir())==backups,'Idempotent reinstallation makes no writes or backup')
        ok(subprocess.check_output(['git','rev-parse','HEAD'],cwd=target,text=True).strip()==BASE,'Installer preserves Git HEAD')
        contract=json.loads((pkg/'source'/manifest['functional_contract']).read_text());ok(all(hashlib.sha256((target/p).read_bytes()).hexdigest()==h for p,h in contract['protected_hashes'].items()),'All 23,096 protected dependencies, prior Tower art and both engine fixes remain exact')
        base=ROOT.parent/'arauna-base-07b';result=subprocess.run([sys.executable,'tools/arauna_maps/validate_frontier_07b.py','--base',str(base)],cwd=target,capture_output=True,text=True)
        ok(result.returncode==0,'Installed native and production C validation passes: '+result.stderr[-400:] if result.returncode else 'Installed native and production C validation passes')
        hashes={e['path']:hashlib.sha256((target/e['path']).read_bytes()).hexdigest() for e in manifest['files']};result=subprocess.run([sys.executable,'tools/arauna_maps/build_frontier_07b.py','--base',str(base)],cwd=target,capture_output=True,text=True)
        ok(result.returncode==0 and all(hashlib.sha256((target/p).read_bytes()).hexdigest()==h for p,h in hashes.items()),'Installed builder is deterministic and idempotent')
        (OUT/'install_test.json').write_text(json.dumps({'status':'PASS','checks':len(checks),'cases':checks,'base_commit':BASE,'payload_files':len(rels),'protected_files':len(contract['protected_hashes']),'worktree_isolated':True},indent=2)+'\n');print(json.dumps({'status':'PASS','checks':len(checks)}))
    finally:
        result=subprocess.run(['git','worktree','remove','--force',str(target)],cwd=ROOT,capture_output=True,text=True)
        if result.returncode:
            registered=subprocess.check_output(['git','worktree','list','--porcelain'],cwd=ROOT,text=True)
            if 'worktree '+str(target)+'\n' in registered:raise RuntimeError(result.stderr)
            if target.exists():shutil.rmtree(target)

if __name__=='__main__':main()
