#!/usr/bin/env python3
"""Base-specific Safari checkpoint overlay, binary patch and prerequisite bundle."""
import argparse,hashlib,json,shutil,subprocess,zipfile
from pathlib import Path
from safari_05_common import ROOT,BASE,OUT

def package(destination,staged=False):
 destination=Path(destination);destination.mkdir(parents=True,exist_ok=True)
 cmd=['git','diff','--name-only']+(['--cached'] if staged else [])+[BASE]+([] if staged else ['HEAD'])
 files=subprocess.check_output(cmd,cwd=ROOT,text=True).splitlines();assert files;entries=[]
 for rel in files:
  raw=(ROOT/rel).read_bytes();before=subprocess.run(['git','show',BASE+':'+rel],cwd=ROOT,capture_output=True);assert before.returncode in (0,128)
  f=destination/'source'/rel;f.parent.mkdir(parents=True,exist_ok=True);f.write_bytes(raw)
  entries.append({'path':rel,'step':5,'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest(),'before_sha256':hashlib.sha256(before.stdout).hexdigest() if before.returncode==0 else None})
 commit=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()
 manifest={'package':'Arauna — Safari checkpoint 05 V1','base_commit':BASE,'checkpoint_commits':{} if staged else {'05':commit},'functional_contract':'review/safari_05/functional_contract.json','files':entries}
 (destination/'manifest.json').write_text(json.dumps(manifest,indent=2,ensure_ascii=False)+'\n');shutil.copyfile(ROOT/'tools/arauna_maps/install_safari_05.py',destination/'install.py')
 diff=['git','diff','--binary','--full-index']+(['--cached'] if staged else [])+[BASE]+([] if staged else ['HEAD'])
 (destination/'changes.patch').write_bytes(subprocess.check_output(diff,cwd=ROOT))
 if not staged:
  subprocess.run(['git','bundle','create',str(destination/'checkpoint_Safari_05.bundle'),'HEAD','^'+BASE],cwd=ROOT,check=True)
  shutil.copyfile(OUT/'install_test.json',destination/'INSTALL_TEST.json')
  checks=json.loads((OUT/'install_test.json').read_text())['checks']
  (destination/'LEIA_ME.md').write_text(f'''# Arauna — Safari 05 V1

Base: `{BASE}`. Checkpoint: `{commit}`.

Seis setores externos + casa de descanso + recepção da Rota 121. Overlay incremental para o Dive **integrado** em 5d0b14e46e. Preserva as correções do topo de Altering e das 12 bordas submersas. Não aplicar sobre main nem sobre o antigo bundle do Dive.

Escolha uma forma de aplicar: instalador, patch ou bundle.

```sh
python3 install.py /caminho/do/repositorio --check
python3 install.py /caminho/do/repositorio
```

O instalador verifica o payload inteiro, 18.010 arquivos de jogo e 183 dependências antes de escrever. Rejeita bases desconhecidas, alterações locais e corrupção; cria backup, reverte falhas e reaplica sem novas escritas. Não altera HEAD nem publica no GitHub. Passaram {checks}/{checks} testes de instalação isolada.

Patch alternativo, em checkout limpo da base:

```sh
git apply --check changes.patch
git apply changes.patch
```

Bundle alternativo, em checkout limpo da base:

```sh
git bundle verify checkpoint_Safari_05.bundle
git fetch checkpoint_Safari_05.bundle HEAD:codex/checkpoint-safari-05
git switch codex/checkpoint-safari-05
```

Checks e prévias reproduzíveis:

```sh
python3 tools/arauna_maps/validate_safari_05.py --base /checkout-limpo-5d0b14e46e
python3 tools/arauna_maps/render_safari_05.py --base /checkout-limpo-5d0b14e46e
```

Leia `source/docs/SAFARI_CHECKPOINT_05.md`. Renders nativos sem sprites, não capturas de emulador. Build ARM/mGBA pendentes para o integrador. Não contém ROM, save nem harness de ROM. A manutenção posterior ficou reservada ao usuário.
''')
  hashes={p.relative_to(destination).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(destination.rglob('*')) if p.is_file() and p.name!='SHA256_FILES.json'}
  (destination/'SHA256_FILES.json').write_text(json.dumps(hashes,indent=2)+'\n')
  output=destination.parent/'Arauna_Checkpoint_05_Safari_V1.zip'
  with zipfile.ZipFile(output,'w',zipfile.ZIP_DEFLATED,9) as z:
   for p in sorted(destination.rglob('*')):
    if p.is_file():z.write(p,p.relative_to(destination))
  print(json.dumps({'package':str(output),'files':len(entries),'commit':commit,'bytes':output.stat().st_size,'sha256':hashlib.sha256(output.read_bytes()).hexdigest()}))
 return manifest

if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('destination',type=Path);ap.add_argument('--staged',action='store_true');a=ap.parse_args();package(a.destination.resolve(),a.staged)
