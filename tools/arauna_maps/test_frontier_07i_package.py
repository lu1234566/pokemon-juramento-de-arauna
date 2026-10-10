#!/usr/bin/env python3
"""Real installation, dependency rejection, rollback and deterministic native art."""
import argparse,hashlib,importlib.util,json,shutil,subprocess,sys,tempfile
from pathlib import Path
from frontier_07i_common import BASE,PREVIOUS,EARLIER,OLDER,ROOT,OUT

def main():
    ap=argparse.ArgumentParser();ap.add_argument('package',type=Path);pkg=ap.parse_args().package.resolve();manifest=json.loads((pkg/'manifest.json').read_text());checks=[]
    target=Path(tempfile.mkdtemp(prefix='arauna-installer07i-',dir='/tmp'));subprocess.run(['git','worktree','add','--detach',str(target),BASE],cwd=ROOT,check=True,capture_output=True)
    rels=[e['path'] for e in manifest['files']];initial={n:(target/n).read_bytes() if (target/n).is_file() else None for n in rels}
    def run(check=False):return subprocess.run([sys.executable,str(pkg/'install.py'),str(target),*(['--check'] if check else [])],capture_output=True,text=True)
    def intact():return all(((target/p).read_bytes() if (target/p).is_file() else None)==raw for p,raw in initial.items())
    def ok(cond,label):assert cond,label;checks.append(label)
    try:
        result=run(True);ok(result.returncode==0 and json.loads(result.stdout)['written']==0 and intact(),'Dry run checks complete dependency contract without writes')
        result=subprocess.run(['git','apply','--check',str(pkg/'changes.patch')],cwd=target,capture_output=True);ok(result.returncode==0,'Binary patch applies to exact base')
        rel=manifest['files'][0]['path'];p=pkg/'source'/rel;raw=p.read_bytes();p.write_bytes(raw+b'corrupt');result=run();p.write_bytes(raw)
        ok(result.returncode!=0 and intact() and 'Corrupted package payload' in result.stderr,'Corrupt payload rejected before writes')
        for rel in ['data/layouts/layouts.json','src/data/tilesets/headers.h','src/field_door.c','src/overworld.c','src/field_specials.c','src/field_control_avatar.c','src/frontier_util.c','src/battle_pyramid.c','src/tileset_anims.c','include/constants/metatile_labels.h','docs/INTEGRACAO_07G.md','docs/BATTLE_FRONTIER_CHECKPOINT_07H.md','data/tilesets/secondary/arauna_frontier07a_tower/metatiles.bin','data/tilesets/secondary/arauna_frontier07c_palace_garden/metatiles.bin','data/tilesets/secondary/arauna_frontier07h_clinic/tiles.png','graphics/door_anims/battle_dome.png','graphics/door_anims/battle_factory.png','graphics/door_anims/battle_tower.png','graphics/door_anims/battle_arena.png','graphics/door_anims/battle_frontier.png','graphics/door_anims/battle_frontier_sliding.png','graphics/door_anims/poke_center.png','graphics/door_anims/poke_mart.png','data/tilesets/secondary/battle_frontier_outside_east/anim/flag/0.png','data/tilesets/secondary/battle_frontier_outside_west/anim/flag/3.png',*['data/maps/'+n+'/'+f for n in ('BattleFrontier_OutsideEast','BattleFrontier_OutsideWest','BattleFrontier_ReceptionGate') for f in ('map.json','scripts.inc')],*['data/layouts/'+n+'/'+f for n in ('BattleFrontier_OutsideEast','BattleFrontier_OutsideWest','BattleFrontier_ReceptionGate') for f in ('map.bin','border.bin')]]:
            p=target/rel;raw=p.read_bytes();p.write_bytes(raw+b'\nLOCAL EDIT\n');result=run();p.write_bytes(raw)
            ok(result.returncode!=0 and intact() and ('Unknown local edit' in result.stderr or 'Changed gameplay dependency' in result.stderr),'Reject local edit: '+rel)
        entry=next(e for e in manifest['files'] if e['before_sha256'] is None);p=target/entry['path'];p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(b'unknown');result=run();p.unlink()
        ok(result.returncode!=0 and intact(),'Reject unknown preexisting new target')
        for commit,label in [('52e6f87e1b9e0b9452de3c40383440622a30f35a','Tower maintenance before later checkpoints'),(PREVIOUS,'531 before 07H services'),(EARLIER,'4122 before official integration'),(OLDER,'06C2 before the later engine fixes'),('979fb6c1b6731561f3c993efd6045a9bbf096c54','stale main')]:
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
        contract=json.loads((pkg/'source'/manifest['functional_contract']).read_text());ok(all(hashlib.sha256((target/p).read_bytes()).hexdigest()==h for p,h in contract['protected_hashes'].items()),'All protected dependencies, official 07G integration, three exterior scripts and Pyramid runtime, Palace water and Tower door repair remain exact')
        base=ROOT.parent/'arauna-base-07i';result=subprocess.run([sys.executable,'tools/arauna_maps/validate_frontier_07i.py','--base',str(base)],cwd=target,capture_output=True,text=True)
        ok(result.returncode==0,'Installed native and production C validation passes: '+result.stderr[-400:] if result.returncode else 'Installed native and production C validation passes')
        hashes={e['path']:hashlib.sha256((target/e['path']).read_bytes()).hexdigest() for e in manifest['files']};result=subprocess.run([sys.executable,'tools/arauna_maps/build_frontier_07i.py','--base',str(base)],cwd=target,capture_output=True,text=True)
        ok(result.returncode==0 and all(hashlib.sha256((target/p).read_bytes()).hexdigest()==h for p,h in hashes.items()),'Installed builder is deterministic and idempotent')
        (OUT/'install_test.json').write_text(json.dumps({'status':'PASS','checks':len(checks),'cases':checks,'base_commit':BASE,'payload_files':len(rels),'protected_files':len(contract['protected_hashes']),'worktree_isolated':True},indent=2)+'\n');print(json.dumps({'status':'PASS','checks':len(checks)}))
    finally:
        result=subprocess.run(['git','worktree','remove','--force',str(target)],cwd=ROOT,capture_output=True,text=True)
        if result.returncode:
            registered=subprocess.check_output(['git','worktree','list','--porcelain'],cwd=ROOT,text=True)
            if 'worktree '+str(target)+'\n' in registered:raise RuntimeError(result.stderr)
            if target.exists():shutil.rmtree(target)

if __name__=='__main__':main()
