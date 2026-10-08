#!/usr/bin/env python3
"""Build a base-specific overlay, binary patch and prerequisite Git bundle."""
import argparse,hashlib,json,shutil,subprocess,zipfile
from pathlib import Path
from build_cavernas_03b import ROOT,BASE


def package(destination,staged=False):
    destination=Path(destination);destination.mkdir(parents=True,exist_ok=True)
    cmd=['git','diff','--name-only']+(['--cached'] if staged else [])+[BASE]+([] if staged else ['HEAD'])
    files=subprocess.check_output(cmd,cwd=ROOT,text=True).splitlines();assert files
    entries=[]
    for rel in files:
        raw=(ROOT/rel).read_bytes()
        before=subprocess.run(['git','show',BASE+':'+rel],cwd=ROOT,capture_output=True)
        assert before.returncode in (0,128)
        p=destination/'source'/rel;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(raw)
        entries.append({'path':rel,'step':3,'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest(),'before_sha256':hashlib.sha256(before.stdout).hexdigest() if before.returncode==0 else None})
    commit=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()
    manifest={'package':'Arauna — checkpoint 03B, Sealed Chamber + Ancient Tomb + Island Cave','base_commit':BASE,'checkpoint_commits':{} if staged else {'03B':commit},'functional_contract':'review/cavernas_03b/functional_contract.json','files':entries}
    (destination/'manifest.json').write_text(json.dumps(manifest,indent=2,ensure_ascii=False)+'\n')
    shutil.copyfile(ROOT/'tools/arauna_maps/install_cavernas_03b.py',destination/'install.py')
    diff=['git','diff','--binary','--full-index']+(['--cached'] if staged else [])+[BASE]+([] if staged else ['HEAD'])
    (destination/'changes.patch').write_bytes(subprocess.check_output(diff,cwd=ROOT))
    if not staged:
        subprocess.run(['git','bundle','create',str(destination/'checkpoint03B.bundle'),'HEAD','^'+BASE],cwd=ROOT,check=True)
        shutil.copyfile(ROOT/'review/cavernas_03b/install_test.json',destination/'INSTALL_TEST.json')
        (destination/'LEIA_ME.md').write_text(f'''# Arauna — checkpoint 03B

Base: `{BASE}`. Commit: `{commit}`.

Este é um overlay incremental para a base com o 03A instalado, não para o main atrasado. Escolha **uma** forma de aplicar: instalador, patch ou bundle. Não aplique os três sucessivamente.

Instalador (sem alterar HEAD):

```bash
python3 install.py /caminho/do/repositorio --check
python3 install.py /caminho/do/repositorio
```

O preflight verifica todos os bytes do payload e 17.785 arquivos de jogo protegidos antes de escrever. A instalação cria backup, reverte falhas e permite reaplicação sem novas escritas. Local edits ou base desconhecidos são recusados. Leia `source/docs/CAVERNAS_CHECKPOINT_03B.md` e `INSTALL_TEST.json`.

Alternativa patch, em checkout limpo da base:

```bash
git apply --check changes.patch
git apply changes.patch
```

Alternativa bundle, em checkout limpo da base:

```bash
git bundle verify checkpoint03B.bundle
git fetch checkpoint03B.bundle HEAD:codex/checkpoint-03b
git switch codex/checkpoint-03b
```

Validação, após gerar os pré-requisitos oficiais de mapas no checkout instalado:

```bash
python3 tools/arauna_maps/prepare_route103_host_checks.py
python3 tools/arauna_maps/validate_cavernas_03b.py --base /checkout-limpo-da-base-7cb02987e8
```

Renders de host e relatórios estão em `source/review/cavernas_03b/`. A compilação ARM e mGBA do 03B ainda precisam da validação do integrador. O ZIP contém código e assets; não contém ROM.
''')
        hashes={p.relative_to(destination).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(destination.rglob('*')) if p.is_file() and p.name!='SHA256_FILES.json'}
        (destination/'SHA256_FILES.json').write_text(json.dumps(hashes,indent=2)+'\n')
        output=destination.parent/'Arauna_Checkpoint_03B_Regis.zip'
        with zipfile.ZipFile(output,'w',zipfile.ZIP_DEFLATED,9) as z:
            for p in sorted(destination.rglob('*')):
                if p.is_file():z.write(p,p.relative_to(destination))
        print(json.dumps({'package':str(output),'files':len(entries),'commit':commit,'bytes':output.stat().st_size,'sha256':hashlib.sha256(output.read_bytes()).hexdigest()}))
    return manifest

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('destination',type=Path);ap.add_argument('--staged',action='store_true');a=ap.parse_args();package(a.destination.resolve(),a.staged)
