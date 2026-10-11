#!/usr/bin/env python3
"""Compact exact-base source payload and cumulative Git history for 08D."""
import argparse
import json
import shutil
import subprocess
import zipfile
from pathlib import Path
from islands_08d import BASE, PREVIOUS, INTEGRATED, ROOT, OUT, dump, sha

BUNDLES = [('checkpoint_08D.bundle',BASE), ('cumulative_from_08C_08D.bundle',PREVIOUS), ('cumulative_a594_08D.bundle',INTEGRATED)]


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
    dump(destination/'manifest.json',{'package':'Arauna 08D — Ilhas especiais V1',
         'base_commit':BASE,'cumulative_base':INTEGRATED,
         'checkpoint_commits':{} if staged else {'08D':commit},
         'functional_contract':'review/islands_08d/functional_contract.json','files':entries})
    shutil.copyfile(ROOT/'tools/arauna_maps/install_islands_08d.py',destination/'install.py')
    diff=['git','diff','--binary','--full-index']+(['--cached'] if staged else [])+[BASE]+([] if staged else ['HEAD'])
    (destination/'changes.patch').write_bytes(subprocess.check_output(diff,cwd=ROOT))
    if staged:return
    for name,base in BUNDLES:
        subprocess.run(['git','bundle','create',str(destination/name),'HEAD','^'+base],cwd=ROOT,check=True)
    shutil.copyfile(OUT/'install_test.json',destination/'INSTALL_TEST.json')
    (destination/'LEIA_ME.md').write_text(f'''# Arauna — 08D Ilhas especiais V1

Checkpoint `{commit}`. Base `{BASE}`; seis mapas, checkpoints visuais 08D1–08D3.
Leia `source/docs/CHECKPOINT_08D_ILHAS_ESPECIAIS.md` para ambientação e limites.

| Bundle | Checkout de partida |
|---|---|
| checkpoint_08D.bundle | `{BASE}` |
| cumulative_from_08C_08D.bundle | `{PREVIOUS}` |
| cumulative_a594_08D.bundle | `{INTEGRATED}` |

Os cumulativos preservam as sete correções: party_menu.c, field_player_avatar.c,
scrcmd.c e os quatro scripts indicados em docs/INTEGRACAO_08C.md.
O main conferido no GitHub (`979fb6c1b6`) está 126 commits atrás da base;
os bundles não são recuperação direta de main. Não houve push.

## Retomar com histórico

Em checkout limpo da base correspondente e com o ZIP extraído:

```sh
git -C /caminho/do/repo bundle verify "$PWD/checkpoint_08D.bundle"
git -C /caminho/do/repo fetch "$PWD/checkpoint_08D.bundle" HEAD:codex/arauna-islands-08d
git -C /caminho/do/repo switch codex/arauna-islands-08d
```

Desde o 08C do autor, use cumulative_from_08C_08D.bundle; desde a594,
use cumulative_a594_08D.bundle. Alterações locais precisam de integração
em outra branch; não aplique source/ cegamente sobre histórico divergente.

## Instalar somente o incremento

O instalador exige 72b72497ac ou o próprio commit 08D; HEAD não muda.

```sh
python3 install.py /caminho/do/repo --check
python3 install.py /caminho/do/repo
```

Ele verifica todo o payload e os 24.388 arquivos congelados antes de escrever,
recusa edições desconhecidas e gera backup com rollback. Reaplicar escreve zero.
As sete correções, Centro, Palace, field_door.c e overworld.c ficam protegidos.
Não altera os contratos históricos para esconder suas divergências documentadas.

INSTALL_TEST.json e CUMULATIVE_TEST.json registram instalação, rejeições,
rollback e importação dos três bundles com comparação da árvore inteira.
Esses testes usam worktrees com armazenamento de objetos Git compartilhado;
não representam um clone vazio. SHA256_FILES.json cobre o conteúdo do ZIP.
O pacote fica abaixo de 30.000.000 bytes e não inclui ROM ou save.

Os PNGs são renders RGB555 nativos sem atores. Build ARM e aceitação no mGBA
deste 08D pendentes. Próxima etapa: seis mapas de Contests, após integrar `{commit}`.
''')



def finalize(destination):
    destination=Path(destination)
    for name in ('INSTALL_TEST.json','CUMULATIVE_TEST.json'):
        assert json.loads((destination/name).read_text())['status']=='PASS'
    names=sorted(p.relative_to(destination).as_posix() for p in destination.rglob('*') if p.is_file() and p.name!='SHA256_FILES.json')
    hashes={n:sha((destination/n).read_bytes()) for n in names}
    dump(destination/'SHA256_FILES.json',hashes)
    output=destination.parent/'Arauna_Checkpoint_08D_IlhasEspeciais_V1.zip'
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
