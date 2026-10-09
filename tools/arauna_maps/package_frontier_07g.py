#!/usr/bin/env python3
"""Exact-base interior increment and six history-preserving Git bundles."""
import argparse,hashlib,json,shutil,subprocess,zipfile
from pathlib import Path
from frontier_07g_common import ROOT,BASE,PREVIOUS,EARLIER,OLDER,GITHUB_9F,MAIN,OUT
BUNDLES=(('checkpoint_BattleFrontier_07G.bundle',BASE),('cumulative_from_07F_07G.bundle',PREVIOUS),('cumulative_from_9a_07G.bundle',EARLIER),('cumulative_from_GitHub_9f_07G.bundle',GITHUB_9F),('cumulative_from_06C2_07G.bundle',OLDER),('cumulative_from_main_07G.bundle',MAIN))

def package(destination,staged=False):
    destination=Path(destination);destination.mkdir(parents=True,exist_ok=True)
    args=['git','diff','--name-only','-z']+(['--cached'] if staged else [])+[BASE]+([] if staged else ['HEAD'])
    files=[n for n in subprocess.check_output(args,cwd=ROOT).decode().split('\0') if n];assert files,'No checkpoint payload';entries=[]
    for rel in files:
        assert not rel.endswith('_draft.png') and '/references/' not in rel
        raw=(ROOT/rel).read_bytes();before=subprocess.run(['git','show',BASE+':'+rel],cwd=ROOT,capture_output=True);assert before.returncode in (0,128)
        p=destination/'source'/rel;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(raw)
        entries.append({'path':rel,'step':'07G','bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest(),'before_sha256':hashlib.sha256(before.stdout).hexdigest() if before.returncode==0 else None})
    commit=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()
    manifest={'package':'Arauna — Battle Frontier 07G: Lounges e Casa de Bento V1','base_commit':BASE,'previous_checkpoint':PREVIOUS,'earlier_github':EARLIER,'github_9f':GITHUB_9F,'older_checkpoint':OLDER,'github_main':MAIN,'checkpoint_commits':{} if staged else {'07G':commit},'functional_contract':'review/frontier_07g/functional_contract.json','files':entries}
    (destination/'manifest.json').write_text(json.dumps(manifest,indent=2,ensure_ascii=False)+'\n');shutil.copyfile(ROOT/'tools/arauna_maps/install_frontier_07g.py',destination/'install.py')
    args=['git','diff','--binary','--full-index']+(['--cached'] if staged else [])+[BASE]+([] if staged else ['HEAD'])
    (destination/'changes.patch').write_bytes(subprocess.check_output(args,cwd=ROOT))
    if staged:return manifest
    for name,base in BUNDLES:subprocess.run(['git','bundle','create',str(destination/name),'HEAD','^'+base],cwd=ROOT,check=True)
    shutil.copyfile(OUT/'install_test.json',destination/'INSTALL_TEST.json')
    protected=len(json.loads((OUT/'functional_contract.json').read_text())['protected_hashes'])
    rows=''.join(f'| {name} | `{base[:10]}` |\n' for name,base in BUNDLES)
    (destination/'LEIA_ME.md').write_text(f'''# Arauna — Battle Frontier 07G / Lounges e Casa de Bento V1

Checkpoint `{commit}`, pai direto/base `{BASE}`. Nove lounges e a casa de Bento (`ScottsHouse` no código): **39/47 mapas Frontier com arte concluída**, restam oito. Commit local; nenhum push.

Pisos de madeira nos lounges estreitos, pedra nos largos e madeira escura na casa. Assentos tecidos, friso de folhas, vegetação e cobre nas entradas. Os dez mapas mantêm três layouts compartilhados. Há 886 células nos dez mapas e 242 células únicas. As prévias são renders RGB555 dos bancos 4bpp nativos, sem atores; não são fotos do mGBA.

## Preservação

754 layouts mantêm IDs e ordem. Só três trocam referências para três pares privados; nenhum layout é acrescentado. Grades, bordas, colisão, elevação, IDs, atributos, máscaras dos dois planos, paletas 0–11 e TV Building permanecem exatos. Apenas a paleta 12 recebe materiais. 30 objetos e 14 warps conservam posições, movimentos, flags e destinos.

O contrato congela {protected} arquivos. Avaliador de IVs, notícias das sete instalações, apostas de pontos, personalidade/natureza, troca, os dois tutores por BP, aprendiz e recompensas de Bento mantêm scripts, condições, preços, limites, flags, diálogos e progressão. field_door.c, overworld.c, portas da Tower, água do Palace, os 29 mapas anteriores e o gerador/paletas/bolsa da Pyramid são preservados.

## 07F conferido

O ZIP 07F V1 recuperado tem SHA256 `03c6eef6b1500794bb451b64f1de2ab583dea192c518e5c6ba9fbac6f4b46f15`; todos os 84 arquivos do incremento coincidem com a base eb. Não há V1.1 corrigida nesse arquivo. eb acrescenta apenas docs/INTEGRACAO_07F.md sobre fd298f4467. Essa nota do integrador registra compilação e fotos de três mapas no mGBA para o 07F; não valida esta nova ROM.

## Retomada por histórico

| Bundle | Base |
|---|---|
{rows}
Em checkout limpo da base correspondente, a partir da pasta extraída:

```sh
git -C /caminho/do/repositorio bundle verify "$PWD/checkpoint_BattleFrontier_07G.bundle"
git -C /caminho/do/repositorio fetch "$PWD/checkpoint_BattleFrontier_07G.bundle" HEAD:codex/arauna-frontier-07g
git -C /caminho/do/repositorio switch codex/arauna-frontier-07g
```

Troque o bundle nas bases antigas. Todos conservam os commits do autor e as integrações intermediárias; CUMULATIVE_TEST.json comprova importação real em receptores independentes. Para histórico divergente, integre em uma branch e preserve as manutenções locais. O main conferido, `{MAIN}`, está 108 commits atrás da base eb; seu cumulativo inclui os checkpoints faltantes.

## Incremento sobre eb

source/, changes.patch e install.py exigem a base eb ou o checkpoint fornecido. Nas bases antigas use os bundles.

```sh
python3 install.py /caminho/do/repositorio --check
python3 install.py /caminho/do/repositorio
```

O instalador confere pacote e todas as dependências antes de escrever, rejeita bases/edições desconhecidas, guarda backup com rollback, conserva HEAD e reaplica sem novas escritas. Alternativa: git apply --check changes.patch e git apply changes.patch. Não aplique o incremento diretamente sobre main.

## Reprodução e limites

```sh
python3 tools/arauna_maps/validate_frontier_07g.py --base /checkout-limpo-eb49778fa8
python3 tools/arauna_maps/render_frontier_07g.py --base /checkout-limpo-eb49778fa8
```

Python 3, Pillow e compilador C do host. Validação dos 1.551 atributos e 3.102 máscaras, selector C em 886 células e 51.200 fallbacks, 53.167 células antigas de cavernas/Dive, animação TV original, portas e animações anteriores. Os 29 mapas anteriores são iguais em 58 renders; mais 14 comparações dos sete pisos gerados da Pyramid preservam suas cores. O C original da Pyramid passa 1.848 casos de geração, 1.892.352 células, 15.174 objetos e 14 tarefas de paleta.

Os serviços de engine usados no host são fixtures explícitas. Scripts de serviços, batalhas, saves e progressão são protegidos por hash; não foram jogados. Auditoria de 528 mapas e gates oficiais de static readiness passaram. O gate estático omite expressamente o compile ARM. **Compilação da ROM e mGBA permanecem pendentes neste ambiente**, sem essas ferramentas.

INSTALL_TEST.json registra instalação real, rollback, rejeições e repetição. CUMULATIVE_TEST.json registra os seis bundles, ancestralidade, árvore, hashes e patch. SHA256_FILES.json cobre o conteúdo do ZIP. Documentação completa: source/docs/BATTLE_FRONTIER_CHECKPOINT_07G.md.

Próximo checkpoint: **07H — cinco mapas de serviços**; depois **07I — três exteriores**.
''')
    return manifest

def finalize(destination):
    destination=Path(destination)
    for n in ('INSTALL_TEST.json','CUMULATIVE_TEST.json'):assert json.loads((destination/n).read_text())['status']=='PASS'
    # Freeze an allowlist, excluding transient Git locks and any stale package files.
    manifest=json.loads((destination/'manifest.json').read_text());names={'manifest.json','install.py','changes.patch','LEIA_ME.md','INSTALL_TEST.json','CUMULATIVE_TEST.json',*[n for n,b in BUNDLES],*('source/'+e['path'] for e in manifest['files'])}
    hashes={n:hashlib.sha256((destination/n).read_bytes()).hexdigest() for n in sorted(names)}
    (destination/'SHA256_FILES.json').write_text(json.dumps(hashes,indent=2)+'\n')
    output=destination.parent/'Arauna_Checkpoint_07G_BattleFrontier_Lounges_Casa_Bento_V1.zip'
    with zipfile.ZipFile(output,'w',zipfile.ZIP_DEFLATED,9) as z:
        for n in sorted(names|{'SHA256_FILES.json'}):z.write(destination/n,n)
    return output

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('destination',type=Path);ap.add_argument('--staged',action='store_true');a=ap.parse_args();package(a.destination.resolve(),a.staged)
    print('Package staged for installation checks.' if a.staged else 'Package prepared; run cumulative checks before finalize.')
