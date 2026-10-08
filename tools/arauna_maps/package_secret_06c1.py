#!/usr/bin/env python3
"""Protected incremental overlay and cumulative 06A+06B+06C1 history."""
import argparse,hashlib,json,shutil,subprocess,zipfile
from pathlib import Path
from secret_06c1_common import ROOT,BASE,GITHUB_BASE,OUT

def package(destination,staged=False):
    destination=Path(destination);destination.mkdir(parents=True,exist_ok=True)
    cmd=['git','diff','--name-only','-z']+(['--cached'] if staged else [])+[BASE]+([] if staged else ['HEAD'])
    files=subprocess.check_output(cmd,cwd=ROOT).decode().rstrip('\0').split('\0');assert files;entries=[]
    for rel in files:
        raw=(ROOT/rel).read_bytes();before=subprocess.run(['git','show',BASE+':'+rel],cwd=ROOT,capture_output=True);assert before.returncode in (0,128)
        f=destination/'source'/rel;f.parent.mkdir(parents=True,exist_ok=True);f.write_bytes(raw)
        entries.append({'path':rel,'step':'06C1','bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest(),'before_sha256':hashlib.sha256(before.stdout).hexdigest() if before.returncode==0 else None})
    commit=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()
    manifest={'package':'Arauna — Secret Bases checkpoint 06C1 V1','base_commit':BASE,'cumulative_bundle_base':GITHUB_BASE,'checkpoint_commits':{} if staged else {'06C1':commit},'functional_contract':'review/secret_bases_06c1/functional_contract.json','files':entries}
    (destination/'manifest.json').write_text(json.dumps(manifest,indent=2,ensure_ascii=False)+'\n');shutil.copyfile(ROOT/'tools/arauna_maps/install_secret_06c1.py',destination/'install.py')
    diff=['git','diff','--binary','--full-index']+(['--cached'] if staged else [])+[BASE]+([] if staged else ['HEAD'])
    (destination/'changes.patch').write_bytes(subprocess.check_output(diff,cwd=ROOT))
    if staged:return manifest
    for name,base in (('checkpoint_SecretBases_06C1.bundle',BASE),('cumulative_06A_06B_06C1.bundle',GITHUB_BASE)):
        subprocess.run(['git','bundle','create',str(destination/name),'HEAD','^'+base],cwd=ROOT,check=True)
    shutil.copyfile(OUT/'install_test.json',destination/'INSTALL_TEST.json')
    (destination/'LEIA_ME.md').write_text(f'''# Arauna — Bases Secretas 06C1 V1

Checkpoint `{commit}`. Base incremental: 06B `{BASE}`.
GitHub integrador consultado: `{GITHUB_BASE}`, sem 06A/06B. Main `979fb6c1b6731561f3c993efd6045a9bbf096c54`, 88 commits atrás do integrador.

16 interiores de cavernas: laterita, arenito, basalto e calcário. Quatro bancos secundários privados; 754 layouts existentes sem novos IDs. Preservados computador, catálogo de decorações, colisão, scripts, eventos, saves e retorno dinâmico às rotas. As 75 entradas externas permanecem intactas.

## Partindo do integrador d665: cumulativo

O bundle contém **06A (Trainer Hill) + 06B (Navel Rock) + 06C1 (16 bases em cavernas)**. Em checkout limpo do integrador:

```sh
git bundle verify cumulative_06A_06B_06C1.bundle
git fetch cumulative_06A_06B_06C1.bundle HEAD:codex/arauna-checkpoint-06c1
git switch codex/arauna-checkpoint-06c1
```

Não aplicar o incremento diretamente sobre main, d665 ou 06A. Se houver commits posteriores, integrar o histórico em uma branch e revisar conflitos.

## Partindo do 06B 2449: incremento

```sh
python3 install.py /caminho/do/repositorio --check
python3 install.py /caminho/do/repositorio
```

O instalador verifica todo o payload e 22.787 dependências antes de escrever. Rejeita corrupção e edição local, mantém HEAD, cria backup e reverte falha de escrita. Veja `INSTALL_TEST.json` para os testes reais.

Alternativas, sobre checkout limpo do 06B:

```sh
git apply --check changes.patch
git apply changes.patch
```

```sh
git bundle verify checkpoint_SecretBases_06C1.bundle
git fetch checkpoint_SecretBases_06C1.bundle HEAD:codex/arauna-secret-bases-06c1
git switch codex/arauna-secret-bases-06c1
```

## Revisão

Leia `source/docs/SECRET_BASES_CHECKPOINT_06C1.md` e as três montagens de `source/review/secret_bases_06c1`. RGB555 nativo sem atores/clima do motor; não são capturas de emulador. As cenas decoradas são fixtures de revisão e não alteram saves nem grids instalados.

```sh
python3 tools/arauna_maps/validate_secret_06c1.py --base /checkout-limpo-2449e12b
python3 tools/arauna_maps/render_secret_06c1.py --base /checkout-limpo-2449e12b
```

Requer Python 3, Pillow e compilador C do host. Compilação ARM, sessão mGBA, sprites e record mixing em link permanecem pendentes. Sem ROM, ELF ou save. O checkpoint não publica no GitHub. Próximo: 06C2, as oito bases em árvores e arbustos; depois Battle Frontier.
''')
    finalize(destination)
    print(json.dumps({'package':str(destination.parent/'Arauna_Checkpoint_06C1_SecretBases_V1.zip'),'files':len(entries),'commit':commit}))
    return manifest

def finalize(destination):
    hashes={p.relative_to(destination).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(destination.rglob('*')) if p.is_file() and p.name!='SHA256_FILES.json'}
    (destination/'SHA256_FILES.json').write_text(json.dumps(hashes,indent=2)+'\n')
    output=destination.parent/'Arauna_Checkpoint_06C1_SecretBases_V1.zip'
    with zipfile.ZipFile(output,'w',zipfile.ZIP_DEFLATED,9) as z:
        for p in sorted(destination.rglob('*')):
            if p.is_file():z.write(p,p.relative_to(destination))
    return output

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('destination',type=Path);ap.add_argument('--staged',action='store_true');a=ap.parse_args();package(a.destination.resolve(),a.staged)
