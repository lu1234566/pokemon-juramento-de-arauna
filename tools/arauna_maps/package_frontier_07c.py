#!/usr/bin/env python3
"""Native increment on official GitHub 9f; four history-preserving bundles."""
import argparse,hashlib,json,shutil,subprocess,zipfile
from pathlib import Path
from frontier_07c_common import ROOT,BASE,PREVIOUS,GITHUB,OLDER,OUT
BUNDLES=(('checkpoint_BattleFrontier_07C.bundle',BASE),('cumulative_from_07B_07C.bundle',PREVIOUS),('cumulative_from_GitHub_52e_07C.bundle',GITHUB),('cumulative_from_06C2_07C.bundle',OLDER))

def package(destination,staged=False):
    destination=Path(destination);destination.mkdir(parents=True,exist_ok=True)
    args=['git','diff','--name-only','-z']+(['--cached'] if staged else [])+[BASE]+([] if staged else ['HEAD'])
    files=[n for n in subprocess.check_output(args,cwd=ROOT).decode().split('\0') if n];assert files,'No staged or committed checkpoint files';entries=[]
    for rel in files:
        raw=(ROOT/rel).read_bytes();before=subprocess.run(['git','show',BASE+':'+rel],cwd=ROOT,capture_output=True);assert before.returncode in (0,128)
        p=destination/'source'/rel;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(raw)
        entries.append({'path':rel,'step':'07C','bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest(),'before_sha256':hashlib.sha256(before.stdout).hexdigest() if before.returncode==0 else None})
    commit=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()
    manifest={'package':'Arauna — Battle Frontier 07C: Battle Palace + Arena V1','base_commit':BASE,'github_base':GITHUB,'previous_checkpoint':PREVIOUS,'older_checkpoint':OLDER,'checkpoint_commits':{} if staged else {'07C':commit},'functional_contract':'review/frontier_07c/functional_contract.json','files':entries}
    (destination/'manifest.json').write_text(json.dumps(manifest,indent=2,ensure_ascii=False)+'\n');shutil.copyfile(ROOT/'tools/arauna_maps/install_frontier_07c.py',destination/'install.py')
    args=['git','diff','--binary','--full-index']+(['--cached'] if staged else [])+[BASE]+([] if staged else ['HEAD'])
    (destination/'changes.patch').write_bytes(subprocess.check_output(args,cwd=ROOT))
    if staged:return manifest
    for name,base in BUNDLES:
        subprocess.run(['git','bundle','create',str(destination/name),'HEAD','^'+base],cwd=ROOT,check=True)
    shutil.copyfile(OUT/'install_test.json',destination/'INSTALL_TEST.json')
    contract=json.loads((OUT/'functional_contract.json').read_text())
    (destination/'LEIA_ME.md').write_text(f'''# Arauna — Battle Frontier 07C / Palace + Arena V1

Checkpoint `{commit}`. Seis mapas novos: Lobby, Corridor e BattleRoom de Palace e Arena. 17/47 mapas Frontier concluídos; restam 30. Jardins de água, terracota, pedra, madeira e tapete de fibra. IDs, atributos, grids, bordas, scripts, eventos, warps, autonomia Palace, julgamento Arena, saves e progressão permanecem exatos.

## Retomada do 07B ou GitHub

O 07C parte diretamente da integração oficial `{BASE}`, que já reúne o 07B `{PREVIOUS}` e a manutenção Tower `{GITHUB}`. A documentação docs/INTEGRACAO_07B.md, field_door.c, overworld.c, os metatiles e as animações Tower ficam protegidos por hash. Nenhum push.

| Bundle | Histórico de origem |
|---|---|
| cumulative_from_07B_07C.bundle | 07B / 868226c157 |
| cumulative_from_GitHub_52e_07C.bundle | GitHub / 52e6f87e1 |
| cumulative_from_06C2_07C.bundle | 06C2 / 989c33c94f |
| checkpoint_BattleFrontier_07C.bundle | GitHub atual / 9f0a056e90 |

Em um checkout limpo com o histórico da base correspondente, use o bundle apropriado. Sobre a base atual 9f:

```sh
git bundle verify checkpoint_BattleFrontier_07C.bundle
git fetch checkpoint_BattleFrontier_07C.bundle HEAD:codex/arauna-frontier-07c
git switch codex/arauna-frontier-07c
```

O bundle da base atual acrescenta o 07C sobre 9f. O cumulativo do 07B inclui a manutenção 52e, a integração oficial 9f e o 07C. O cumulativo do GitHub antigo 52e inclui o 07B, sua integração e o 07C. O de 989 inclui as etapas anteriores e ambas as linhas de histórico. Os testes usam receptores independentes que têm a base declarada e os ancestrais que o bundle exige. Nenhum bundle sobrescreve trabalho local divergente: concilie conflitos numa branch.

## Incremento de arte na base integrada

source/, changes.patch e install.py exigem `{BASE}`; não aplicar diretamente no 07B antigo, 52e isolado, antigo baseline 8fb ou main. Os bundles cumulativos acima importam o resultado completo nas bases indicadas. Em checkout limpo de 9f:

```sh
python3 install.py /caminho/do/repositorio --check
python3 install.py /caminho/do/repositorio
```

O instalador protege {len(contract['protected_hashes']):,} dependências por hash, rejeita edições/corrupção, conserva HEAD, cria backup e rollback e reaplica sem novas escritas. Alternativa: `git apply --check changes.patch`, depois `git apply changes.patch`.

## Reprodução e provas

```sh
python3 tools/arauna_maps/validate_frontier_07c.py --base /checkout-limpo-9f0a056e90
python3 tools/arauna_maps/render_frontier_07c.py --base /checkout-limpo-9f0a056e90
```

Python 3, Pillow e compilador C do host. Auditoria oficial e static readiness PASS. Seletores, portas, fila de animação General e fade anterior do Dome executados no C do host. Palace/Arena e seus scripts são preservados por hash. Compilação ARM, batalhas/saves/sprites e execução completa no mGBA continuam pendentes. As prévias são renders RGB555 nativos sem atores.

INSTALL_TEST.json demonstra instalação real, corrupção, alterações locais, rollback, idempotência e reconstrução determinística. CUMULATIVE_TEST.json demonstra importação real dos quatro bundles, árvore, checkout SHA e patch binário. SHA256_FILES.json cobre todos os arquivos. Documentação em source/docs/BATTLE_FRONTIER_CHECKPOINT_07C.md. Próximo: 07D, três mapas de Battle Factory.
''')
    return manifest

def finalize(destination):
    destination=Path(destination);assert json.loads((destination/'CUMULATIVE_TEST.json').read_text())['status']=='PASS';hashes={p.relative_to(destination).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(destination.rglob('*')) if p.is_file() and p.name!='SHA256_FILES.json'}
    (destination/'SHA256_FILES.json').write_text(json.dumps(hashes,indent=2)+'\n');output=destination.parent/'Arauna_Checkpoint_07C_BattleFrontier_Palace_Arena_V1.zip'
    with zipfile.ZipFile(output,'w',zipfile.ZIP_DEFLATED,9) as z:
        for p in sorted(destination.rglob('*')):
            if p.is_file():z.write(p,p.relative_to(destination))
    return output

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('destination',type=Path);ap.add_argument('--staged',action='store_true');a=ap.parse_args();package(a.destination.resolve(),a.staged)
    if not a.staged:print('Package prepared; run bundle checks before finalize.')
