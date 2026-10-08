#!/usr/bin/env python3
"""Base-specific checkpoint overlay, complete binary patch and Git bundle."""
import argparse,hashlib,json,shutil,subprocess,zipfile
from pathlib import Path
from dive_04_common import ROOT,BASE,OUT

def package(destination,staged=False):
 destination=Path(destination);destination.mkdir(parents=True,exist_ok=True)
 cmd=['git','diff','--name-only']+(['--cached'] if staged else [])+[BASE]+([] if staged else ['HEAD'])
 files=subprocess.check_output(cmd,cwd=ROOT,text=True).splitlines();assert files
 entries=[]
 for rel in files:
  raw=(ROOT/rel).read_bytes();before=subprocess.run(['git','show',BASE+':'+rel],cwd=ROOT,capture_output=True);assert before.returncode in (0,128)
  path=destination/'source'/rel;path.parent.mkdir(parents=True,exist_ok=True);path.write_bytes(raw)
  entries.append({'path':rel,'step':4,'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest(),'before_sha256':hashlib.sha256(before.stdout).hexdigest() if before.returncode==0 else None})
 commit=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()
 manifest={'package':'Arauna — Dive checkpoint 04, Altering/Mirage and legendary chamber haze','base_commit':BASE,'checkpoint_commits':{} if staged else {'04':commit},'functional_contract':'review/dive_04/functional_contract.json','files':entries}
 (destination/'manifest.json').write_text(json.dumps(manifest,indent=2,ensure_ascii=False)+'\n')
 shutil.copyfile(ROOT/'tools/arauna_maps/install_dive_04.py',destination/'install.py')
 diff=['git','diff','--binary','--full-index']+(['--cached'] if staged else [])+[BASE]+([] if staged else ['HEAD'])
 (destination/'changes.patch').write_bytes(subprocess.check_output(diff,cwd=ROOT))
 if not staged:
  subprocess.run(['git','bundle','create',str(destination/'checkpoint_Dive_04.bundle'),'HEAD','^'+BASE],cwd=ROOT,check=True)
  shutil.copyfile(OUT/'install_test.json',destination/'INSTALL_TEST.json')
  checks=json.loads((OUT/'install_test.json').read_text())['checks']
  (destination/'LEIA_ME.md').write_text(f'''# Arauna — Dive 04

Base: `{BASE}`. Checkpoint: `{commit}`.

12 mapas Dive + boca de Altering + base de Mirage Tower + névoa leve nas duas salas finais. Overlay **incremental** para o 03C/V1.1 já instalado; main está atrasado. Os 12 slots reais estão listados no relatório. Rota 107 não possui slot/ligação Dive nesta base; nenhuma ligação nova foi criada.

Escolha uma forma de aplicar: instalador, patch ou bundle.

```sh
python3 install.py /caminho/do/repositorio --check
python3 install.py /caminho/do/repositorio
```

O instalador verifica o payload inteiro, 17.906 arquivos de jogo e 110 dependências antes de escrever. Rejeita bases desconhecidas, alterações locais e corrupção; cria backup, reverte falhas e reaplica sem novas escritas. Não altera HEAD nem publica no GitHub. Passaram {checks}/{checks} testes da instalação isolada.

Alternativa patch, em checkout limpo da base:

```sh
git apply --check changes.patch
git apply changes.patch
```

Alternativa bundle, em checkout limpo da base:

```sh
git bundle verify checkpoint_Dive_04.bundle
git fetch checkpoint_Dive_04.bundle HEAD:codex/checkpoint-dive-04
git switch codex/checkpoint-dive-04
```

Para reproduzir checks e prévias:

```sh
python3 tools/arauna_maps/prepare_route103_host_checks.py
python3 tools/arauna_maps/validate_dive_04.py --base /checkout-limpo-802d01c341
python3 tools/arauna_maps/render_dive_04.py --base /checkout-limpo-802d01c341
```

Leia `source/docs/DIVE_CHECKPOINT_04.md`. Os PNGs usam dados nativos e código C real em host; não são fotos de emulador. O estudo da névoa ilustra coeficientes GBA; não reproduz a composição completa de sprites/paletas do runtime. Compilação ARM e mGBA pendentes para o integrador. Não há ROM, save ou harness distribuível. Safari é a próxima etapa.
''')
  hashes={p.relative_to(destination).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(destination.rglob('*')) if p.is_file() and p.name!='SHA256_FILES.json'}
  (destination/'SHA256_FILES.json').write_text(json.dumps(hashes,indent=2)+'\n')
  output=destination.parent/'Arauna_Checkpoint_04_Dive_V1.zip'
  with zipfile.ZipFile(output,'w',zipfile.ZIP_DEFLATED,9) as z:
   for p in sorted(destination.rglob('*')):
    if p.is_file():z.write(p,p.relative_to(destination))
  print(json.dumps({'package':str(output),'files':len(entries),'commit':commit,'bytes':output.stat().st_size,'sha256':hashlib.sha256(output.read_bytes()).hexdigest()}))
 return manifest

if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('destination',type=Path);ap.add_argument('--staged',action='store_true');a=ap.parse_args();package(a.destination.resolve(),a.staged)
