#!/usr/bin/env python3
"""Base-specific Trainer Hill source overlay, binary patch and Git bundle."""
import argparse,hashlib,json,shutil,subprocess,zipfile
from pathlib import Path
from trainer_hill_06a_common import ROOT,BASE,OUT

def package(destination,staged=False):
    destination=Path(destination);destination.mkdir(parents=True,exist_ok=True)
    cmd=['git','diff','--name-only']+(['--cached'] if staged else [])+[BASE]+([] if staged else ['HEAD'])
    files=subprocess.check_output(cmd,cwd=ROOT,text=True).splitlines();assert files;entries=[]
    for rel in files:
        raw=(ROOT/rel).read_bytes();before=subprocess.run(['git','show',BASE+':'+rel],cwd=ROOT,capture_output=True);assert before.returncode in (0,128)
        f=destination/'source'/rel;f.parent.mkdir(parents=True,exist_ok=True);f.write_bytes(raw)
        entries.append({'path':rel,'step':'06A','bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest(),'before_sha256':hashlib.sha256(before.stdout).hexdigest() if before.returncode==0 else None})
    commit=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()
    manifest={'package':'Arauna — Trainer Hill checkpoint 06A V1','base_commit':BASE,'checkpoint_commits':{} if staged else {'06A':commit},'functional_contract':'review/trainer_hill_06a/functional_contract.json','files':entries}
    (destination/'manifest.json').write_text(json.dumps(manifest,indent=2,ensure_ascii=False)+'\n');shutil.copyfile(ROOT/'tools/arauna_maps/install_trainer_hill_06a.py',destination/'install.py')
    diff=['git','diff','--binary','--full-index']+(['--cached'] if staged else [])+[BASE]+([] if staged else ['HEAD'])
    (destination/'changes.patch').write_bytes(subprocess.check_output(diff,cwd=ROOT))
    if not staged:
        subprocess.run(['git','bundle','create',str(destination/'checkpoint_TrainerHill_06A.bundle'),'HEAD','^'+BASE],cwd=ROOT,check=True)
        shutil.copyfile(OUT/'install_test.json',destination/'INSTALL_TEST.json')
        checks=json.loads((OUT/'install_test.json').read_text())['checks']
        (destination/'LEIA_ME.md').write_text(f'''# Arauna — Trainer Hill 06A V1

Base exata: `{BASE}`. Checkpoint: `{commit}`.

Sete mapas: recepção, quatro andares, cobertura e elevador. Arte nativa indexada de pedra, madeira e ardósia; preserva os 16 desafios dinâmicos e mantém a Battle Tower intacta. A base contém Safari, Dive e a manutenção de Petalburg/Oldale de 08/10/2026. O main consultado estava 88 commits atrás; não aplicar sobre ele.

Escolha uma forma de aplicar: instalador, patch ou bundle.

```sh
python3 install.py /caminho/do/repositorio --check
python3 install.py /caminho/do/repositorio
```

O instalador verifica todo o payload, 18.105 arquivos de jogo e 183 dependências antes de escrever. Rejeita bases desconhecidas, alterações locais e corrupção; cria backup, reverte falhas e reaplica sem novas escritas. Não altera HEAD nem publica no GitHub. Passaram {checks}/{checks} casos reais de instalação isolada.

Patch alternativo, em checkout limpo da base:

```sh
git apply --check changes.patch
git apply changes.patch
```

Bundle alternativo, em checkout limpo da base:

```sh
git bundle verify checkpoint_TrainerHill_06A.bundle
git fetch checkpoint_TrainerHill_06A.bundle HEAD:codex/checkpoint-trainer-hill-06a
git switch codex/checkpoint-trainer-hill-06a
```

Verificação e prévias reproduzíveis (Python 3, Pillow e compilador C do host):

```sh
python3 tools/arauna_maps/validate_trainer_hill_06a.py --base /checkout-limpo-d665dc34dd
python3 tools/arauna_maps/render_trainer_hill_06a.py --base /checkout-limpo-d665dc34dd
```

Leia `source/docs/TRAINER_HILL_CHECKPOINT_06A.md`. Renders nativos sem sprites, não capturas de emulador. Testes de C usam serviços simulados no host. Build ARM/mGBA pendentes para o integrador. Sem ROM, ELF, save ou harness de ROM. Manutenção geral e remoção de bancos não fazem parte deste checkpoint.
''')
        hashes={p.relative_to(destination).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(destination.rglob('*')) if p.is_file() and p.name!='SHA256_FILES.json'}
        (destination/'SHA256_FILES.json').write_text(json.dumps(hashes,indent=2)+'\n')
        output=destination.parent/'Arauna_Checkpoint_06A_TrainerHill_V1.zip'
        with zipfile.ZipFile(output,'w',zipfile.ZIP_DEFLATED,9) as z:
            for p in sorted(destination.rglob('*')):
                if p.is_file():z.write(p,p.relative_to(destination))
        print(json.dumps({'package':str(output),'files':len(entries),'commit':commit,'bytes':output.stat().st_size,'sha256':hashlib.sha256(output.read_bytes()).hexdigest()}))
    return manifest

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('destination',type=Path);ap.add_argument('--staged',action='store_true');a=ap.parse_args();package(a.destination.resolve(),a.staged)
