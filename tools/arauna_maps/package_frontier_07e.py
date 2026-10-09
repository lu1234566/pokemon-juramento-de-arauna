#!/usr/bin/env python3
"""Exact-base Pike increment and cumulative Git bundles for five known histories."""
import argparse,hashlib,json,shutil,subprocess,zipfile
from pathlib import Path
from frontier_07e_common import ROOT,BASE,PREVIOUS,EARLIER,OLDER,GITHUB_9F,OUT
BUNDLES=(('checkpoint_BattleFrontier_07E.bundle',BASE),('cumulative_from_07D_07E.bundle',PREVIOUS),('cumulative_from_8d_07E.bundle',EARLIER),('cumulative_from_GitHub_9f_07E.bundle',GITHUB_9F),('cumulative_from_06C2_07E.bundle',OLDER))

def package(destination,staged=False):
    destination=Path(destination);destination.mkdir(parents=True,exist_ok=True)
    args=['git','diff','--name-only','-z']+(['--cached'] if staged else [])+[BASE]+([] if staged else ['HEAD'])
    files=[n for n in subprocess.check_output(args,cwd=ROOT).decode().split('\0') if n];assert files,'No checkpoint payload';entries=[]
    for rel in files:
        raw=(ROOT/rel).read_bytes();before=subprocess.run(['git','show',BASE+':'+rel],cwd=ROOT,capture_output=True);assert before.returncode in (0,128)
        p=destination/'source'/rel;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(raw)
        entries.append({'path':rel,'step':'07E','bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest(),'before_sha256':hashlib.sha256(before.stdout).hexdigest() if before.returncode==0 else None})
    commit=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()
    manifest={'package':'Arauna — Battle Frontier 07E: Battle Pike V1','base_commit':BASE,'previous_checkpoint':PREVIOUS,'earlier_github':EARLIER,'github_9f':GITHUB_9F,'older_checkpoint':OLDER,'checkpoint_commits':{} if staged else {'07E':commit},'functional_contract':'review/frontier_07e/functional_contract.json','files':entries}
    (destination/'manifest.json').write_text(json.dumps(manifest,indent=2,ensure_ascii=False)+'\n');shutil.copyfile(ROOT/'tools/arauna_maps/install_frontier_07e.py',destination/'install.py')
    args=['git','diff','--binary','--full-index']+(['--cached'] if staged else [])+[BASE]+([] if staged else ['HEAD'])
    (destination/'changes.patch').write_bytes(subprocess.check_output(args,cwd=ROOT))
    if staged:return manifest
    for name,base in BUNDLES:subprocess.run(['git','bundle','create',str(destination/name),'HEAD','^'+base],cwd=ROOT,check=True)
    shutil.copyfile(OUT/'install_test.json',destination/'INSTALL_TEST.json')
    protected=len(json.loads((OUT/'functional_contract.json').read_text())['protected_hashes'])
    (destination/'LEIA_ME.md').write_text(f'''# Arauna — Battle Frontier 07E / Battle Pike V1

Checkpoint `{commit}`. Pai direto/base `{BASE}`. Seis mapas: Lobby, Corridor, ThreePathRoom, RoomNormal, RoomFinal e RoomWildMons. **26/47 mapas Frontier concluídos**; restam 21. RoomUnused é apenas um layout sem mapa e fica intacto. Não houve push.

Pedra escura, cobre, cortinas vinho, detalhes jade e uma espiral serpentina na sala final. Os caminhos e objetos conservam as coordenadas originais. As imagens são renders RGB555 nativos sem sprites, não capturas de emulador.

## Preservação

Os 754 layouts mantêm IDs, ordem e compartilhamento. Só os seis do Pike trocam referências para um par privado de bancos 4bpp. Grids, bordas, colisões, atributos, máscaras, scripts, eventos, warps e movimentos permanecem exatos. O Pike mantém RNG e dicas de salas, status, cura, encontros selvagens, seleção do grupo, níveis, partidas, Lucy, pontos, saves e progressão. Os 36 IDs usados pelo C da cortina e os estados nomeados mantêm IDs/atributos; três atualizações nos ticks 4, 8 e 12, com retomada do script. Building conserva o callback e quadros nativos; o secundário conserva NULL. field_door.c, overworld.c, field_specials.c e battle_pike.c não são editados. As portas da Tower, a água corrigida 0x226 do Palace e a integração oficial 07D permanecem exatas.

## Retomada por histórico

| Bundle | Base de origem |
|---|---|
| checkpoint_BattleFrontier_07E.bundle | GitHub atual / 38d7879ae1 |
| cumulative_from_07D_07E.bundle | 07D do autor / 2a1838d000 |
| cumulative_from_8d_07E.bundle | GitHub antes do 07D / 8d7cafa5d7 |
| cumulative_from_GitHub_9f_07E.bundle | GitHub anterior / 9f0a056e90 |
| cumulative_from_06C2_07E.bundle | 06C2 / 989c33c94f |

Em checkout limpo da base 38d, a partir da pasta extraída:

```sh
git -C /caminho/do/repositorio bundle verify "$PWD/checkpoint_BattleFrontier_07E.bundle"
git -C /caminho/do/repositorio fetch "$PWD/checkpoint_BattleFrontier_07E.bundle" HEAD:codex/arauna-frontier-07e
git -C /caminho/do/repositorio switch codex/arauna-frontier-07e
```

Nos históricos anteriores, substitua o nome pelo cumulativo correspondente. Eles incluem as etapas e a manutenção oficial que faltam. Concilie trabalho divergente numa branch. main estava 104 commits atrás da base: não usar main como ponto de partida do incremento.

## Incremento na base atual

source/, changes.patch e install.py exigem `{BASE}`. Nas bases antigas use os bundles acima. Na base atual:

```sh
python3 install.py /caminho/do/repositorio --check
python3 install.py /caminho/do/repositorio
```

O instalador protege {protected} dependências, rejeita edições e corrupção antes de escrever, mantém HEAD, faz backup/rollback e reaplica sem novas escritas. Alternativa: git apply --check changes.patch e git apply changes.patch dentro do repositório.

## Reprodução e limites

```sh
python3 tools/arauna_maps/validate_frontier_07e.py --base /checkout-limpo-38d7879ae1
python3 tools/arauna_maps/render_frontier_07e.py --base /checkout-limpo-38d7879ae1
```

Python 3, Pillow e compilador C do host. Auditoria oficial de mapas e static readiness executam nesta etapa. O gate estático omite explicitamente compilação ARM. Funções C originais de seletores, cortina, portas, Building, General e Dome foram executadas no host com serviços explícitos. Scripts e a lógica Pike estão preservados por hash, sem executar batalhas ou o interpretador de scripts. Compilação ARM e testes jogáveis no mGBA permanecem pendentes neste ambiente. A nota oficial INTEGRACAO_07D.md relata build/mGBA do 07D pelo integrador; isso não valida o novo 07E.

INSTALL_TEST.json documenta instalação real, rejeição de bases/edições/corrupção, rollback e idempotência. CUMULATIVE_TEST.json documenta importação dos cinco bundles em receptores independentes, árvore, ancestralidade, hashes e patch. SHA256_FILES.json cobre os arquivos do ZIP. Documentação: source/docs/BATTLE_FRONTIER_CHECKPOINT_07E.md. Próximo: 07F, três mapas Battle Pyramid, com geração procedural a revisar.
''')
    return manifest

def finalize(destination):
    destination=Path(destination)
    for n in ('INSTALL_TEST.json','CUMULATIVE_TEST.json'):assert json.loads((destination/n).read_text())['status']=='PASS'
    hashes={p.relative_to(destination).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(destination.rglob('*')) if p.is_file() and p.name!='SHA256_FILES.json'}
    (destination/'SHA256_FILES.json').write_text(json.dumps(hashes,indent=2)+'\n')
    output=destination.parent/'Arauna_Checkpoint_07E_BattleFrontier_Pike_V1.zip'
    with zipfile.ZipFile(output,'w',zipfile.ZIP_DEFLATED,9) as z:
        for p in sorted(destination.rglob('*')):
            if p.is_file():z.write(p,p.relative_to(destination))
    return output

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('destination',type=Path);ap.add_argument('--staged',action='store_true');a=ap.parse_args();package(a.destination.resolve(),a.staged)
    print('Package staged for installation checks.' if a.staged else 'Package prepared; run cumulative checks before finalize.')
