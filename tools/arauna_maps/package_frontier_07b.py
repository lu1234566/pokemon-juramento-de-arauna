#!/usr/bin/env python3
"""Increment on 07A, cumulatives on GitHub 7e9 and recovered 06C2/989."""
import argparse,hashlib,json,shutil,subprocess,zipfile
from pathlib import Path
from frontier_07b_common import ROOT,BASE,PREVIOUS,OUT
OLDER='989c33c94fb89b92c5f608f78233fdd8deded4c4'

def package(destination,staged=False):
    destination=Path(destination);destination.mkdir(parents=True,exist_ok=True)
    args=['git','diff','--name-only','-z']+(['--cached'] if staged else [])+[BASE]+([] if staged else ['HEAD'])
    files=[n for n in subprocess.check_output(args,cwd=ROOT).decode().split('\0') if n];assert files,'No staged or committed checkpoint files';entries=[]
    for rel in files:
        raw=(ROOT/rel).read_bytes();before=subprocess.run(['git','show',BASE+':'+rel],cwd=ROOT,capture_output=True);assert before.returncode in (0,128)
        p=destination/'source'/rel;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(raw)
        entries.append({'path':rel,'step':'07B','bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest(),'before_sha256':hashlib.sha256(before.stdout).hexdigest() if before.returncode==0 else None})
    commit=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()
    manifest={'package':'Arauna — Battle Frontier 07B: Battle Dome V1','base_commit':BASE,'github_base':PREVIOUS,'older_checkpoint':OLDER,'checkpoint_commits':{} if staged else {'07B':commit},'functional_contract':'review/frontier_07b/functional_contract.json','files':entries}
    (destination/'manifest.json').write_text(json.dumps(manifest,indent=2,ensure_ascii=False)+'\n');shutil.copyfile(ROOT/'tools/arauna_maps/install_frontier_07b.py',destination/'install.py')
    args=['git','diff','--binary','--full-index']+(['--cached'] if staged else [])+[BASE]+([] if staged else ['HEAD'])
    (destination/'changes.patch').write_bytes(subprocess.check_output(args,cwd=ROOT))
    if staged:return manifest
    for name,base in (('checkpoint_BattleFrontier_07B.bundle',BASE),('cumulative_from_GitHub_7e9_07B.bundle',PREVIOUS),('cumulative_from_06C2_07B.bundle',OLDER)):
        subprocess.run(['git','bundle','create',str(destination/name),'HEAD','^'+base],cwd=ROOT,check=True)
    shutil.copyfile(OUT/'install_test.json',destination/'INSTALL_TEST.json')
    contract=json.loads((OUT/'functional_contract.json').read_text())
    (destination/'LEIA_ME.md').write_text(f'''# Arauna — Battle Frontier 07B / Battle Dome V1

Checkpoint `{commit}` sobre o 07A `{BASE}`. Quatro mapas concluídos: Lobby, Corridor, PreBattleRoom e BattleRoom. O ciclo Frontier tem agora 11/47 mapas prontos; faltam 36. Bancos privados com pedra azulada, madeira escura, bronze e inscrição ARAUNA CIRCUIT. IDs, atributos, grids, bordas, atores, scripts, warps, torneio, saves e progresso preservados.

## Incremento sobre o 07A / fc408a604b

Em checkout limpo do 07A:

```sh
git bundle verify checkpoint_BattleFrontier_07B.bundle
git fetch checkpoint_BattleFrontier_07B.bundle HEAD:codex/arauna-frontier-07b
git switch codex/arauna-frontier-07b
```

Alternativa com preflight, backup e rollback:

```sh
python3 install.py /caminho/do/repositorio --check
python3 install.py /caminho/do/repositorio
```

O instalador preserva HEAD, verifica as {len(contract['protected_hashes']):,} dependências anteriores e reaplica sem novas escritas. Outra alternativa: `git apply --check changes.patch`, depois `git apply changes.patch`. source/ e changes.patch exigem o 07A completo.

## Cumulativo sobre o GitHub / 7e9d29dc5f

O integrador do GitHub ainda estava em `{PREVIOUS}` quando conferido. Este bundle inclui 07A e 07B, preservando as correções existentes da engine:

```sh
git bundle verify cumulative_from_GitHub_7e9_07B.bundle
git fetch cumulative_from_GitHub_7e9_07B.bundle HEAD:codex/arauna-frontier-07b
git switch codex/arauna-frontier-07b
```

## Histórico sobre 06C2 / 989c33c94f

Este terceiro bundle inclui também 7e9, com field_door.c, overworld.c e as portas do Trainer Hill:

```sh
git bundle verify cumulative_from_06C2_07B.bundle
git fetch cumulative_from_06C2_07B.bundle HEAD:codex/arauna-frontier-07b
git switch codex/arauna-frontier-07b
```

Cada bundle exige seu commit de origem. O main está 95 commits atrás de 7e9 e não recebe diretamente o incremento. Trabalho divergente deve ser conciliado em uma branch com esse histórico; os testes verificam bases compatíveis e não substituem uma resolução de conflitos local. Nenhum push foi feito.

## Reprodução e evidências

```sh
python3 tools/arauna_maps/validate_frontier_07b.py --base /checkout-limpo-07a
python3 tools/arauna_maps/render_frontier_07b.py --base /checkout-limpo-07a
```

Python 3, Pillow e compilador C do host. A paleta animada 8, seus quatro quadros e as posições dos índices 13/15 ficam exatos. Callbacks de luz, fade RGB555 e transição executados a partir do C original; portas nativas e seletores também executados no host. Scripts e lógica do torneio ficam preservados por hash. Compilação ARM e batalhas/sprites no mGBA continuam pendentes.

INSTALL_TEST.json demonstra instalação, rejeição de edições, corrupção, rollback e idempotência. CUMULATIVE_TEST.json demonstra importação real dos três bundles, hashes do checkout e aplicação do patch. SHA256_FILES.json cobre todos os arquivos do pacote. Leia source/docs/BATTLE_FRONTIER_CHECKPOINT_07B.md. Próximo: 07C, seis mapas de Battle Palace e Battle Arena.
''')
    return manifest

def finalize(destination):
    destination=Path(destination);hashes={p.relative_to(destination).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(destination.rglob('*')) if p.is_file() and p.name!='SHA256_FILES.json'}
    (destination/'SHA256_FILES.json').write_text(json.dumps(hashes,indent=2)+'\n');output=destination.parent/'Arauna_Checkpoint_07B_BattleFrontier_Dome_V1.zip'
    with zipfile.ZipFile(output,'w',zipfile.ZIP_DEFLATED,9) as z:
        for p in sorted(destination.rglob('*')):
            if p.is_file():z.write(p,p.relative_to(destination))
    return output

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('destination',type=Path);ap.add_argument('--staged',action='store_true');a=ap.parse_args();package(a.destination.resolve(),a.staged)
    if not a.staged:print(finalize(a.destination.resolve()))
