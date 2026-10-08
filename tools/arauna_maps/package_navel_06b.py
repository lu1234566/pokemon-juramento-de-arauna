#!/usr/bin/env python3
"""Incremental 06B overlay and cumulative 06A+06B Git bundle."""
import argparse,hashlib,json,shutil,subprocess,zipfile
from pathlib import Path
from navel_06b_common import ROOT,BASE,GITHUB_BASE,OUT

def package(destination,staged=False):
    destination=Path(destination);destination.mkdir(parents=True,exist_ok=True)
    cmd=['git','diff','--name-only','-z']+(['--cached'] if staged else [])+[BASE]+([] if staged else ['HEAD'])
    files=subprocess.check_output(cmd,cwd=ROOT).decode().rstrip('\0').split('\0');assert files;entries=[]
    for rel in files:
        raw=(ROOT/rel).read_bytes();before=subprocess.run(['git','show',BASE+':'+rel],cwd=ROOT,capture_output=True);assert before.returncode in (0,128)
        f=destination/'source'/rel;f.parent.mkdir(parents=True,exist_ok=True);f.write_bytes(raw)
        entries.append({'path':rel,'step':'06B','bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest(),'before_sha256':hashlib.sha256(before.stdout).hexdigest() if before.returncode==0 else None})
    commit=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()
    manifest={'package':'Arauna — Navel Rock checkpoint 06B V1','base_commit':BASE,'cumulative_bundle_base':GITHUB_BASE,'checkpoint_commits':{} if staged else {'06B':commit},'functional_contract':'review/navel_06b/functional_contract.json','files':entries}
    (destination/'manifest.json').write_text(json.dumps(manifest,indent=2,ensure_ascii=False)+'\n');shutil.copyfile(ROOT/'tools/arauna_maps/install_navel_06b.py',destination/'install.py')
    diff=['git','diff','--binary','--full-index']+(['--cached'] if staged else [])+[BASE]+([] if staged else ['HEAD'])
    (destination/'changes.patch').write_bytes(subprocess.check_output(diff,cwd=ROOT))
    if staged:return manifest
    for name,base in (('checkpoint_NavelRock_06B.bundle',BASE),('cumulative_06A_06B.bundle',GITHUB_BASE)):
        subprocess.run(['git','bundle','create',str(destination/name),'HEAD','^'+base],cwd=ROOT,check=True)
    shutil.copyfile(OUT/'install_test.json',destination/'INSTALL_TEST.json')
    checks=json.loads((OUT/'install_test.json').read_text())['checks']
    (destination/'LEIA_ME.md').write_text(f'''# Arauna — Navel Rock 06B V1

Checkpoint: `{commit}`. Incremento 06B sobre `{BASE}` (Trainer Hill 06A).
GitHub integrador consultado: `{GITHUB_BASE}`, ainda sem 06A. Main: `979fb6c1b6731561f3c993efd6045a9bbf096c54`, 88 commits atrás do integrador.

21 mapas de Navel Rock + porto dependente. Preserva os 42 warps, scripts, colisão, barco, Mystic Ticket, Ho-Oh/Lugia nível 70 e Sacred Ash. Arte indexada em 16 bancos privados; 9 layouts acrescentados sem deslocar IDs anteriores. O porto de Birth Island fica intacto.

## Se você está no GitHub integrador d665dc34dd, use o cumulativo

Ele contém o histórico completo de **06A (Trainer Hill) + 06B (Navel Rock)** sobre a manutenção integrada depois do Safari. Em checkout limpo:

```sh
git bundle verify cumulative_06A_06B.bundle
git fetch cumulative_06A_06B.bundle HEAD:codex/arauna-checkpoint-06b
git switch codex/arauna-checkpoint-06b
```

O bundle é a entrega cumulativa; o diretório `source` e `changes.patch` são somente o incremento 06B. Não aplicar o incremento sobre d665 ou main. Se houver commits locais posteriores, integrar o histórico em uma branch e revisar os conflitos.

## Se você já tem o 06A 29ae94cdc2, escolha uma alternativa incremental

Instalador protegido:

```sh
python3 install.py /caminho/do/repositorio --check
python3 install.py /caminho/do/repositorio
```

Verifica o payload inteiro e 22.394 dependências existentes antes de escrever. Rejeita base desconhecida, edição local e corrupção; cria backup, reverte falha e reaplica sem novas escritas. Preserva HEAD. Passaram {checks}/{checks} casos reais em checkout isolado; veja `INSTALL_TEST.json`.

Patch em checkout limpo de 29ae:

```sh
git apply --check changes.patch
git apply changes.patch
```

Ou histórico incremental:

```sh
git bundle verify checkpoint_NavelRock_06B.bundle
git fetch checkpoint_NavelRock_06B.bundle HEAD:codex/arauna-navel-06b
git switch codex/arauna-navel-06b
```

## Revisão e reprodução

Leia `source/docs/NAVEL_ROCK_CHECKPOINT_06B.md` e as três montagens em `source/review/navel_06b`. Renders nativos RGB555 sem atores ou clima do motor; não são capturas de emulador. O concept é direção de materiais, não geometria instalada.

Com Python 3, Pillow e compilador C do host:

```sh
python3 tools/arauna_maps/validate_navel_06b.py --base /checkout-limpo-29ae94cdc2
python3 tools/arauna_maps/render_navel_06b.py --base /checkout-limpo-29ae94cdc2
```

Compilação ARM e revisão no mGBA pendentes: ferramentas indisponíveis neste ambiente. Testes de C/eventos usam serviços explícitos de host. Sem ROM, ELF ou save. Este pacote não publica no GitHub. Manutenção geral/remoção de bancos permanece fora deste checkpoint.
''')
    hashes={p.relative_to(destination).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(destination.rglob('*')) if p.is_file() and p.name!='SHA256_FILES.json'}
    (destination/'SHA256_FILES.json').write_text(json.dumps(hashes,indent=2)+'\n')
    output=destination.parent/'Arauna_Checkpoint_06B_NavelRock_V1.zip'
    with zipfile.ZipFile(output,'w',zipfile.ZIP_DEFLATED,9) as z:
        for p in sorted(destination.rglob('*')):
            if p.is_file():z.write(p,p.relative_to(destination))
    print(json.dumps({'package':str(output),'files':len(entries),'commit':commit,'bytes':output.stat().st_size,'sha256':hashlib.sha256(output.read_bytes()).hexdigest()}))
    return manifest

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('destination',type=Path);ap.add_argument('--staged',action='store_true');a=ap.parse_args();package(a.destination.resolve(),a.staged)
