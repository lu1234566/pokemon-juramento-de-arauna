#!/usr/bin/env python3
"""Compact exact-base source payload and cumulative Git history for 08B2."""
import argparse
import json
import shutil
import subprocess
import zipfile
from pathlib import Path
from desert_08b2 import BASE, PREVIOUS, INTEGRATED, ROOT, OUT, dump, sha

BUNDLES = [('checkpoint_08B2.bundle',BASE), ('cumulative_from_08B1_08B2.bundle',PREVIOUS), ('cumulative_a594_08B2.bundle',INTEGRATED)]


def package(destination, staged=False):
    destination=Path(destination);destination.mkdir(parents=True,exist_ok=True)
    files=subprocess.check_output(['git','diff','--name-only','-z']+(['--cached'] if staged else [])+[BASE]+([] if staged else ['HEAD']),cwd=ROOT).decode().rstrip('\0').split('\0')
    assert files and all(files)
    entries=[]
    for rel in files:
        raw=(ROOT/rel).read_bytes()
        before=subprocess.run(['git','show',BASE+':'+rel],cwd=ROOT,capture_output=True)
        assert before.returncode in (0,128)
        path=destination/'source'/rel;path.parent.mkdir(parents=True,exist_ok=True);path.write_bytes(raw)
        entries.append({'path':rel,'bytes':len(raw),'sha256':sha(raw),
                        'before_sha256':sha(before.stdout) if before.returncode==0 else None})
    commit=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()
    dump(destination/'manifest.json',{'package':'Arauna 08B2 — DesertUnderpass + ScorchedSlab V1',
         'base_commit':BASE,'cumulative_base':INTEGRATED,
         'checkpoint_commits':{} if staged else {'08B2':commit},
         'functional_contract':'review/desert_08b2/functional_contract.json','files':entries})
    shutil.copyfile(ROOT/'tools/arauna_maps/install_desert_08b2.py',destination/'install.py')
    diff=['git','diff','--binary','--full-index']+(['--cached'] if staged else [])+[BASE]+([] if staged else ['HEAD'])
    (destination/'changes.patch').write_bytes(subprocess.check_output(diff,cwd=ROOT))
    if staged:return
    for name,base in BUNDLES:
        subprocess.run(['git','bundle','create',str(destination/name),'HEAD','^'+base],cwd=ROOT,check=True)
    shutil.copyfile(OUT/'install_test.json',destination/'INSTALL_TEST.json')
    (destination/'LEIA_ME.md').write_text(f'''# Arauna — 08B2 DesertUnderpass + ScorchedSlab V1

Checkpoint `{commit}`. Base `{BASE}`; dois mapas. Leia
`source/docs/CHECKPOINT_08B2_UNDERPASS_SLAB.md` para arte, preservação e limites.

| Bundle | Checkout de partida |
|---|---|
| checkpoint_08B2.bundle | `{BASE}` |
| cumulative_from_08B1_08B2.bundle | `{PREVIOUS}` |
| cumulative_a594_08B2.bundle | `{INTEGRATED}` |

Os cumulativos incorporam as integrações e a correção de party_menu.c. O main do GitHub
`979fb6c1b6` está 118 commits atrás da base: nenhum destes bundles é recuperação
direta de main. Use o checkout cumulativo instalado. Não houve push.

## Retomar com histórico

Em checkout limpo da base correspondente, com este ZIP extraído:

```sh
git -C /caminho/do/repo bundle verify "$PWD/checkpoint_08B2.bundle"
git -C /caminho/do/repo fetch "$PWD/checkpoint_08B2.bundle" HEAD:codex/arauna-desert-08b2
git -C /caminho/do/repo switch codex/arauna-desert-08b2
```

Desde 08B1, use cumulative_from_08B1_08B2.bundle; desde a594, use cumulative_a594_08B2.bundle.
Desde uma branch com alterações locais, integre em outra branch e preserve
as manutenções; não aplique source/ cegamente sobre histórico divergente.

## Instalar somente o incremento

O instalador exige o commit 043 ou o próprio 08B2; HEAD não muda.

```sh
python3 install.py /caminho/do/repo --check
python3 install.py /caminho/do/repo
```

Ele verifica todo o payload e os 24.167 arquivos congelados antes de escrever,
recusa edição desconhecida, mantém backup de arquivos anteriores com lista
de rollback e reaplica sem escrever. Preserve o backup até a aceitação.
party_menu.c corrigido, Centro, Palace, field_door.c e overworld.c ficam protegidos.

INSTALL_TEST.json e CUMULATIVE_TEST.json registram instalação, rejeições,
rollback, importação Git e comparação da árvore. SHA256_FILES.json cobre
os arquivos deste ZIP. O pacote fica abaixo de 30.000.000 bytes.

Os PNGs são renders nativos sem atores; ROM e mGBA ainda pendentes.
Próximo checkpoint: 08B3 — Mirage Tower 1F–4F, sobre `{commit}`.
''')


def finalize(destination):
    destination=Path(destination)
    for name in ('INSTALL_TEST.json','CUMULATIVE_TEST.json'):
        assert json.loads((destination/name).read_text())['status']=='PASS'
    names=sorted(p.relative_to(destination).as_posix() for p in destination.rglob('*') if p.is_file() and p.name!='SHA256_FILES.json')
    hashes={n:sha((destination/n).read_bytes()) for n in names}
    dump(destination/'SHA256_FILES.json',hashes)
    output=destination.parent/'Arauna_Checkpoint_08B2_Underpass_Slab_V1.zip'
    with zipfile.ZipFile(output,'w',zipfile.ZIP_DEFLATED,9) as z:
        for n in names+['SHA256_FILES.json']:z.write(destination/n,n)
    assert output.stat().st_size<30000000
    with zipfile.ZipFile(output) as z:
        assert z.testzip() is None
        for n,h in hashes.items():assert sha(z.read(n))==h,n
    print(output, output.stat().st_size, sha(output.read_bytes()))
    return output


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('destination',type=Path)
    parser.add_argument('--staged',action='store_true')
    args=parser.parse_args();package(args.destination.resolve(),args.staged)
