#!/usr/bin/env python3
"""Increment on 7e9 plus history reconciliation from the recovered 06C2."""
import argparse,hashlib,json,shutil,subprocess,zipfile
from pathlib import Path
from frontier_07a_common import ROOT,BASE,PREVIOUS,OUT

def package(destination,staged=False):
    destination=Path(destination);destination.mkdir(parents=True,exist_ok=True)
    args=['git','diff','--name-only','-z']+(['--cached'] if staged else [])+[BASE]+([] if staged else ['HEAD'])
    files=[n for n in subprocess.check_output(args,cwd=ROOT).decode().split('\0') if n];assert files,'No staged or committed checkpoint files';entries=[]
    for rel in files:
        raw=(ROOT/rel).read_bytes();before=subprocess.run(['git','show',BASE+':'+rel],cwd=ROOT,capture_output=True);assert before.returncode in (0,128)
        p=destination/'source'/rel;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(raw)
        entries.append({'path':rel,'step':'07A','bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest(),'before_sha256':hashlib.sha256(before.stdout).hexdigest() if before.returncode==0 else None})
    commit=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()
    manifest={'package':'Arauna — Battle Frontier 07A: Battle Tower V1','base_commit':BASE,'previous_checkpoint':PREVIOUS,'checkpoint_commits':{} if staged else {'07A':commit},'functional_contract':'review/frontier_07a/functional_contract.json','files':entries}
    (destination/'manifest.json').write_text(json.dumps(manifest,indent=2,ensure_ascii=False)+'\n');shutil.copyfile(ROOT/'tools/arauna_maps/install_frontier_07a.py',destination/'install.py')
    args=['git','diff','--binary','--full-index']+(['--cached'] if staged else [])+[BASE]+([] if staged else ['HEAD'])
    (destination/'changes.patch').write_bytes(subprocess.check_output(args,cwd=ROOT))
    if staged:return manifest
    for name,base in (('checkpoint_BattleFrontier_07A.bundle',BASE),('cumulative_from_06C2_07A.bundle',PREVIOUS)):
        subprocess.run(['git','bundle','create',str(destination/name),'HEAD','^'+base],cwd=ROOT,check=True)
    shutil.copyfile(OUT/'install_test.json',destination/'INSTALL_TEST.json')
    (destination/'LEIA_ME.md').write_text(f'''# Arauna — Battle Frontier 07A / Battle Tower V1

Checkpoint `{commit}` sobre `{BASE}`. Sete mapas concluídos dos 47 da Battle Frontier. Seis layouts mantêm IDs, ordem, grids e bordas. Bancos privados de madeira, pedra e bronze. Scripts, eventos, colisões, progresso, Multi/link e dados de batalha ficam preservados.

## Sobre a base atual 7e9d29dc5f

Em checkout limpo dessa base, use o histórico:

```sh
git bundle verify checkpoint_BattleFrontier_07A.bundle
git fetch checkpoint_BattleFrontier_07A.bundle HEAD:codex/arauna-frontier-07a
git switch codex/arauna-frontier-07a
```

Ou aplique o incremento com verificação e backup:

```sh
python3 install.py /caminho/do/repositorio --check
python3 install.py /caminho/do/repositorio
```

O instalador conserva HEAD, protege as 23.003 dependências anteriores por hash, rejeita corrupção e edições locais, reverte falhas e reaplica sem novas escritas. Testes reais em INSTALL_TEST.json. Alternativa: `git apply --check changes.patch`, depois `git apply changes.patch`.

## Sobre o checkpoint 06C2 / 989c33c94f

Este cumulativo também inclui o commit 7e9d29dc5f, suas duas imagens de portas, o gerador e a documentação. Preserva as mudanças em field_door.c e overworld.c integralmente:

```sh
git bundle verify cumulative_from_06C2_07A.bundle
git fetch cumulative_from_06C2_07A.bundle HEAD:codex/arauna-frontier-07a
git switch codex/arauna-frontier-07a
```

O incremento source/ e changes.patch exige 7e9; não aplicar diretamente sobre 989 ou main. Se houver trabalho divergente já iniciado em 989, concilie o histórico em uma branch usando 7e9 como pai e preserve os arquivos de engine. O pacote não envia mensagens nem faz push.

## Reprodução

```sh
python3 tools/arauna_maps/validate_frontier_07a.py --base /checkout-limpo-7e9d29dc5f
python3 tools/arauna_maps/render_frontier_07a.py --base /checkout-limpo-7e9d29dc5f
```

Requer Python 3, Pillow e compilador C do host. Auditoria oficial de mapas e static readiness PASS; compilação ARM, sessão mGBA e batalhas/link continuam pendentes. Prévias são renders nativos RGB555 sem atores, não capturas de emulador. Os estados abertos são fixtures de revisão, não alterações de grids.

Leia source/docs/BATTLE_FRONTIER_CHECKPOINT_07A.md e source/review/frontier_07a/checkpoint_plan.json. Próximo: 07B, quatro mapas do Battle Dome. Restam 40 mapas. CUMULATIVE_TEST.json demonstra os imports reais e hashes de checkout; SHA256_FILES.json cobre cada arquivo do pacote.
''')
    return manifest

def finalize(destination):
    destination=Path(destination);hashes={p.relative_to(destination).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(destination.rglob('*')) if p.is_file() and p.name!='SHA256_FILES.json'}
    (destination/'SHA256_FILES.json').write_text(json.dumps(hashes,indent=2)+'\n');output=destination.parent/'Arauna_Checkpoint_07A_BattleFrontier_Tower_V1.zip'
    with zipfile.ZipFile(output,'w',zipfile.ZIP_DEFLATED,9) as z:
        for p in sorted(destination.rglob('*')):
            if p.is_file():z.write(p,p.relative_to(destination))
    return output

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('destination',type=Path);ap.add_argument('--staged',action='store_true');a=ap.parse_args();manifest=package(a.destination.resolve(),a.staged)
    if not a.staged:print(finalize(a.destination.resolve()))
