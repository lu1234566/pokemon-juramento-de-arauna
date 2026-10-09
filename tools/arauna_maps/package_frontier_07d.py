#!/usr/bin/env python3
"""Native Factory increment on GitHub 8d and four history-preserving bundles."""
import argparse,hashlib,json,shutil,subprocess,zipfile
from pathlib import Path
from frontier_07d_common import ROOT,BASE,PREVIOUS,EARLIER,OLDER,OUT
BUNDLES=(('checkpoint_BattleFrontier_07D.bundle',BASE),('cumulative_from_07C_07D.bundle',PREVIOUS),('cumulative_from_GitHub_9f_07D.bundle',EARLIER),('cumulative_from_06C2_07D.bundle',OLDER))

def package(destination,staged=False):
    destination=Path(destination);destination.mkdir(parents=True,exist_ok=True)
    args=['git','diff','--name-only','-z']+(['--cached'] if staged else [])+[BASE]+([] if staged else ['HEAD'])
    files=[n for n in subprocess.check_output(args,cwd=ROOT).decode().split('\0') if n];assert files,'No checkpoint payload';entries=[]
    for rel in files:
        raw=(ROOT/rel).read_bytes();before=subprocess.run(['git','show',BASE+':'+rel],cwd=ROOT,capture_output=True);assert before.returncode in (0,128)
        p=destination/'source'/rel;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(raw)
        entries.append({'path':rel,'step':'07D','bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest(),'before_sha256':hashlib.sha256(before.stdout).hexdigest() if before.returncode==0 else None})
    commit=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()
    manifest={'package':'Arauna — Battle Frontier 07D: Battle Factory V1','base_commit':BASE,'previous_checkpoint':PREVIOUS,'earlier_github':EARLIER,'older_checkpoint':OLDER,'checkpoint_commits':{} if staged else {'07D':commit},'functional_contract':'review/frontier_07d/functional_contract.json','files':entries}
    (destination/'manifest.json').write_text(json.dumps(manifest,indent=2,ensure_ascii=False)+'\n');shutil.copyfile(ROOT/'tools/arauna_maps/install_frontier_07d.py',destination/'install.py')
    args=['git','diff','--binary','--full-index']+(['--cached'] if staged else [])+[BASE]+([] if staged else ['HEAD'])
    (destination/'changes.patch').write_bytes(subprocess.check_output(args,cwd=ROOT))
    if staged:return manifest
    for name,base in BUNDLES:subprocess.run(['git','bundle','create',str(destination/name),'HEAD','^'+base],cwd=ROOT,check=True)
    shutil.copyfile(OUT/'install_test.json',destination/'INSTALL_TEST.json')
    contract=json.loads((OUT/'functional_contract.json').read_text())
    (destination/'LEIA_ME.md').write_text(f'''# Arauna — Battle Frontier 07D / Battle Factory V1

Checkpoint `{commit}`. Base `{BASE}`. Três mapas: Lobby, PreBattleRoom e BattleRoom. **20/47 mapas Frontier concluídos**; restam 27. Pedra escura, cobre, painéis jade e marca de calibração na arena. Os objetos e os trajetos do atendente continuam nas coordenadas originais.

## Base integrada e manutenção

A base 8d já inclui o 07C `{PREVIOUS}` e corrige a margem de água 0x226 do Palace. Essa correção, docs/INTEGRACAO_07C.md, seu gerador e todas as alterações de portas Tower permanecem exatas. field_door.c e overworld.c não são editados. Não houve push.

IDs, ordem dos 754 layouts, grids, bordas, colisões, atributos, máscaras, scripts, objetos, eventos, warps, aluguel, escolha e troca de Pokémon, modos de nível, batalhas, Noland, recompensas, saves e progressão ficam protegidos por hash. Somente três layouts mudam as referências para um par privado de bancos 4bpp. Building conserva o callback e os quadros nativos; o secundário permanece sem callback.

## Retomada por histórico

| Bundle | Base de origem |
|---|---|
| checkpoint_BattleFrontier_07D.bundle | GitHub atual / 8d7cafa5d7 |
| cumulative_from_07C_07D.bundle | 07C do autor / 638d523c08 |
| cumulative_from_GitHub_9f_07D.bundle | GitHub anterior / 9f0a056e90 |
| cumulative_from_06C2_07D.bundle | 06C2 / 989c33c94f |

Em checkout limpo da base atual 8d:

```sh
git bundle verify checkpoint_BattleFrontier_07D.bundle
git fetch checkpoint_BattleFrontier_07D.bundle HEAD:codex/arauna-frontier-07d
git switch codex/arauna-frontier-07d
```

O cumulativo do autor 07C acrescenta a correção Palace do GitHub e o 07D. O de 9f inclui o 07C, sua manutenção e o 07D. O de 989 inclui as etapas e ambas as linhas de histórico anteriores. Os testes usam receptores independentes com a base e os ancestrais exigidos pelo bundle, sem atravessar blobs ausentes do antigo checkout parcial. Concilie trabalho divergente numa branch.

## Incremento na base atual

source/, changes.patch e install.py exigem `{BASE}`. Não aplicar diretamente em 638, 9f, 989 ou main. Nesses históricos, use o bundle cumulativo indicado acima. Na base 8d:

```sh
python3 install.py /caminho/do/repositorio --check
python3 install.py /caminho/do/repositorio
```

O instalador protege {len(contract['protected_hashes']):,} dependências, rejeita alterações e corrupção antes de escrever, conserva HEAD, cria backup/rollback e reaplica sem novas escritas. Alternativa: git apply --check changes.patch e git apply changes.patch.

## Reprodução e limites

```sh
python3 tools/arauna_maps/validate_frontier_07d.py --base /checkout-limpo-8d7cafa5d7
python3 tools/arauna_maps/render_frontier_07d.py --base /checkout-limpo-8d7cafa5d7
```

Python 3, Pillow e compilador C do host. Auditoria oficial de mapas e static readiness PASS. O gate estático executa a composição oficial e pula explicitamente a compilação ARM. Funções C originais de seletores, portas, Building, General e fade Dome foram executadas no host com serviços explícitos. A lógica Factory é preservada por bytes; aluguel, troca, partidas, Noland, saves e sprites ainda exigem uma ROM e testes no emulador. Compilação ARM e mGBA permanecem pendentes neste ambiente. As prévias são renders RGB555 sem atores.

INSTALL_TEST.json documenta instalação real, rejeição de edições/corrupção/bases incorretas, rollback, idempotência e reconstrução determinística. CUMULATIVE_TEST.json prova importação dos quatro bundles, ancestralidade, árvore, hashes do checkout e patch binário. SHA256_FILES.json cobre todos os arquivos. Documentação em source/docs/BATTLE_FRONTIER_CHECKPOINT_07D.md. Próximo: 07E, seis mapas de Battle Pike.
''')
    return manifest

def finalize(destination):
    destination=Path(destination);assert json.loads((destination/'CUMULATIVE_TEST.json').read_text())['status']=='PASS'
    hashes={p.relative_to(destination).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(destination.rglob('*')) if p.is_file() and p.name!='SHA256_FILES.json'}
    (destination/'SHA256_FILES.json').write_text(json.dumps(hashes,indent=2)+'\n');output=destination.parent/'Arauna_Checkpoint_07D_BattleFrontier_Factory_V1.zip'
    with zipfile.ZipFile(output,'w',zipfile.ZIP_DEFLATED,9) as z:
        for p in sorted(destination.rglob('*')):
            if p.is_file():z.write(p,p.relative_to(destination))
    return output

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('destination',type=Path);ap.add_argument('--staged',action='store_true');a=ap.parse_args();package(a.destination.resolve(),a.staged)
    if not a.staged:print('Package prepared; run bundle checks before finalize.')
