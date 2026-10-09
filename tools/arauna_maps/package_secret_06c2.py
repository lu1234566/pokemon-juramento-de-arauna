#!/usr/bin/env python3
"""Protected incremental overlay and cumulative 06A+06B+06C1+06C2 history."""
import argparse,hashlib,json,shutil,subprocess,zipfile
from pathlib import Path
from secret_06c2_common import ROOT,BASE,GITHUB_BASE,OUT,PREVIOUS

def package(destination,staged=False):
    destination=Path(destination);destination.mkdir(parents=True,exist_ok=True)
    cmd=['git','diff','--name-only','-z']+(['--cached'] if staged else [])+[BASE]+([] if staged else ['HEAD'])
    files=subprocess.check_output(cmd,cwd=ROOT).decode().rstrip('\0').split('\0');assert files;entries=[]
    for rel in files:
        raw=(ROOT/rel).read_bytes();before=subprocess.run(['git','show',BASE+':'+rel],cwd=ROOT,capture_output=True);assert before.returncode in (0,128)
        f=destination/'source'/rel;f.parent.mkdir(parents=True,exist_ok=True);f.write_bytes(raw)
        entries.append({'path':rel,'step':'06C2','bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest(),'before_sha256':hashlib.sha256(before.stdout).hexdigest() if before.returncode==0 else None})
    commit=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()
    manifest={'package':'Arauna — Secret Bases checkpoint 06C2 V1','base_commit':BASE,'cumulative_bundle_base':GITHUB_BASE,'previous_checkpoint':PREVIOUS,'checkpoint_commits':{} if staged else {'06C2':commit},'functional_contract':'review/secret_bases_06c2/functional_contract.json','files':entries}
    (destination/'manifest.json').write_text(json.dumps(manifest,indent=2,ensure_ascii=False)+'\n');shutil.copyfile(ROOT/'tools/arauna_maps/install_secret_06c2.py',destination/'install.py')
    diff=['git','diff','--binary','--full-index']+(['--cached'] if staged else [])+[BASE]+([] if staged else ['HEAD'])
    (destination/'changes.patch').write_bytes(subprocess.check_output(diff,cwd=ROOT))
    if staged:return manifest
    for name,base in (('checkpoint_SecretBases_06C2.bundle',BASE),('cumulative_06A_06B_06C1_06C2.bundle',GITHUB_BASE),('cumulative_from_06C1_06C2.bundle',PREVIOUS)):
        subprocess.run(['git','bundle','create',str(destination/name),'HEAD','^'+base],cwd=ROOT,check=True)
    shutil.copyfile(OUT/'install_test.json',destination/'INSTALL_TEST.json')
    (destination/'LEIA_ME.md').write_text(f'''# Arauna — Bases Secretas 06C2 V1

Checkpoint `{commit}`. Base incremental reconciliada `{BASE}`: 06C1 `{PREVIOUS}` + manutenção do GitHub `{GITHUB_BASE}`. A integração preserva a remoção dos 26 bancos antigos e os pacotes 06A/06B/06C1.
Main `979fb6c1b6731561f3c993efd6045a9bbf096c54` continua 89 commits atrás do integrador. Nenhum push é feito por este pacote.

8 interiores de árvores/arbustos: madeira envelhecida, terra sombreada e folhagem de mata. Dois bancos secundários privados; os 754 layouts mantêm IDs/ordem. Preservados computador, catálogo de decorações, colisões, scripts, eventos, saves, progressão e retorno dinâmico. As 75 entradas externas e os 16 interiores de cavernas do 06C1 permanecem intactos.

## Partindo do GitHub integrador 872f56e86

Use o cumulativo completo em checkout limpo com o histórico do integrador (incluindo seu pai d665):

```sh
git bundle verify cumulative_06A_06B_06C1_06C2.bundle
git fetch cumulative_06A_06B_06C1_06C2.bundle HEAD:codex/arauna-checkpoint-06c2
git switch codex/arauna-checkpoint-06c2
```

Contém Trainer Hill 06A, Navel Rock 06B, as 16 cavernas 06C1, a conciliação da manutenção e as oito bases 06C2. Em clone raso de apenas um commit, recupere também o pai d665 antes da verificação.

## Partindo do checkpoint 06C1 0098c5c3b

Este bundle acrescenta a manutenção e o 06C2, preservando o 06C1:

```sh
git bundle verify cumulative_from_06C1_06C2.bundle
git fetch cumulative_from_06C1_06C2.bundle HEAD:codex/arauna-checkpoint-06c2
git switch codex/arauna-checkpoint-06c2
```

## Incremento somente sobre a base reconciliada 6cfba8c79b

O diretório source, changes.patch e o instalador são o incremento 06C2. Não aplicar diretamente sobre main, d665, 872 ou o 06C1 ainda sem conciliação. Se houver commits posteriores, integre o histórico em uma branch e revise os conflitos.

```sh
python3 install.py /caminho/do/repositorio --check
python3 install.py /caminho/do/repositorio
```

O instalador verifica o payload e 22.920 dependências existentes antes de escrever. Rejeita corrupção, edição local e base desconhecida, mantém HEAD, cria backup, reverte falha e reaplica sem novas escritas. Testes reais em INSTALL_TEST.json.

Alternativas, sobre checkout limpo da base reconciliada:

```sh
git apply --check changes.patch
git apply changes.patch
```

```sh
git bundle verify checkpoint_SecretBases_06C2.bundle
git fetch checkpoint_SecretBases_06C2.bundle HEAD:codex/arauna-secret-bases-06c2
git switch codex/arauna-secret-bases-06c2
```

## Revisão e reprodução

Leia source/docs/SECRET_BASES_CHECKPOINT_06C2.md e as três montagens de source/review/secret_bases_06c2. São renders RGB555 nativos sem atores/clima, não capturas de emulador. As cenas decoradas são fixtures e não alteram saves/grids.

```sh
python3 tools/arauna_maps/validate_secret_06c2.py --base /checkout-limpo-6cfba8c79b
python3 tools/arauna_maps/render_secret_06c2.py --base /checkout-limpo-6cfba8c79b
```

Requer Python 3, Pillow e compilador C do host. Compilação ARM, sessão mGBA, sprites e record mixing em link continuam pendentes. Sem ROM, ELF ou saves. As 24 Bases Secretas estão concluídas em 06C1+06C2. Próximo ciclo: Battle Frontier, 47 mapas, dividido em checkpoints por instalação.
''')
    finalize(destination)
    print(json.dumps({'package':str(destination.parent/'Arauna_Checkpoint_06C2_SecretBases_V1.zip'),'files':len(entries),'commit':commit}))
    return manifest

def finalize(destination):
    hashes={p.relative_to(destination).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(destination.rglob('*')) if p.is_file() and p.name!='SHA256_FILES.json'}
    (destination/'SHA256_FILES.json').write_text(json.dumps(hashes,indent=2)+'\n')
    output=destination.parent/'Arauna_Checkpoint_06C2_SecretBases_V1.zip'
    with zipfile.ZipFile(output,'w',zipfile.ZIP_DEFLATED,9) as z:
        for p in sorted(destination.rglob('*')):
            if p.is_file():z.write(p,p.relative_to(destination))
    return output

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('destination',type=Path);ap.add_argument('--staged',action='store_true');a=ap.parse_args();package(a.destination.resolve(),a.staged)
