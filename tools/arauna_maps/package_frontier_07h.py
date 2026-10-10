#!/usr/bin/env python3
"""Small exact-base increment and five history-preserving cumulative bundles."""
import argparse,hashlib,json,shutil,subprocess,zipfile
from pathlib import Path
from frontier_07h_common import ROOT,BASE,PREVIOUS,EARLIER,OLDER,GITHUB_9F,MAIN,OUT
BUNDLES=(('checkpoint_BattleFrontier_07H.bundle',BASE),('cumulative_from_07G_07H.bundle',PREVIOUS),('cumulative_from_eb_07H.bundle',EARLIER),('cumulative_from_GitHub_9f_07H.bundle',GITHUB_9F),('cumulative_from_06C2_07H.bundle',OLDER))
def package(destination,staged=False):
    destination=Path(destination);destination.mkdir(parents=True,exist_ok=True)
    args=['git','diff','--name-only','-z']+(['--cached'] if staged else [])+[BASE]+([] if staged else ['HEAD'])
    files=[n for n in subprocess.check_output(args,cwd=ROOT).decode().split('\0') if n];assert files;entries=[]
    for rel in files:
        assert not rel.endswith('_draft.png') and '/references/' not in rel
        raw=(ROOT/rel).read_bytes();before=subprocess.run(['git','show',BASE+':'+rel],cwd=ROOT,capture_output=True);assert before.returncode in (0,128)
        p=destination/'source'/rel;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(raw)
        entries.append({'path':rel,'step':'07H','bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest(),'before_sha256':hashlib.sha256(before.stdout).hexdigest() if before.returncode==0 else None})
    commit=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()
    manifest={'package':'Arauna — Battle Frontier 07H: Serviços V1','base_commit':BASE,'previous_checkpoint':PREVIOUS,'earlier_github':EARLIER,'github_9f':GITHUB_9F,'older_checkpoint':OLDER,'github_main':MAIN,'checkpoint_commits':{} if staged else {'07H':commit},'functional_contract':'review/frontier_07h/functional_contract.json','files':entries}
    (destination/'manifest.json').write_text(json.dumps(manifest,indent=2,ensure_ascii=False)+'\n');shutil.copyfile(ROOT/'tools/arauna_maps/install_frontier_07h.py',destination/'install.py')
    args=['git','diff','--binary','--full-index']+(['--cached'] if staged else [])+[BASE]+([] if staged else ['HEAD'])
    (destination/'changes.patch').write_bytes(subprocess.check_output(args,cwd=ROOT))
    if staged:return manifest
    for name,base in BUNDLES:subprocess.run(['git','bundle','create',str(destination/name),'HEAD','^'+base],cwd=ROOT,check=True)
    shutil.copyfile(OUT/'install_test.json',destination/'INSTALL_TEST.json')
    rows=''.join(f'| {name} | `{base[:10]}` |\n' for name,base in BUNDLES)
    (destination/'LEIA_ME.md').write_text(f'''# Arauna — 07H / Serviços V1

Checkpoint `{commit}`, pai/base `{BASE}`. Cinco mapas; Frontier **44/47**. Nenhum push. Leia source/docs/BATTLE_FRONTIER_CHECKPOINT_07H.md para preservação, evidências e limites.

## Retomada

| Bundle | Base |
|---|---|
{rows}
Em checkout limpo da base correspondente, a partir desta pasta extraída:

```sh
git -C /caminho/do/repositorio bundle verify "$PWD/checkpoint_BattleFrontier_07H.bundle"
git -C /caminho/do/repositorio fetch "$PWD/checkpoint_BattleFrontier_07H.bundle" HEAD:codex/arauna-frontier-07h
git -C /caminho/do/repositorio switch codex/arauna-frontier-07h
```

Troque o bundle nas bases antigas. CUMULATIVE_TEST.json comprova importação em receptores independentes, árvore e hashes. O main `{MAIN}` está 110 commits atrás da base 531; não aplique o incremento nele. O pacote compacto começa no checkpoint 06C2 ou posterior; a recuperação anterior de main continua disponível nos quatro volumes entregues com o 07G. O grande bundle de main foi excluído para manter este ZIP abaixo de 30 MB. Não afirma suporte direto de main.

## Incremento

source/, changes.patch e install.py exigem a base 531 ou o checkpoint fornecido. Em histórico divergente faça integração em uma branch preservando as manutenções locais.

```sh
python3 install.py /caminho/do/repositorio --check
python3 install.py /caminho/do/repositorio
```

O instalador verifica o pacote inteiro e os arquivos protegidos antes de escrever, rejeita bases/edições desconhecidas, guarda backup com rollback, conserva HEAD e reaplica sem novas escritas.

## Reprodução

```sh
python3 tools/arauna_maps/validate_frontier_07h.py --base /checkout-limpo-531352ce37
python3 tools/arauna_maps/render_frontier_07h.py --base /checkout-limpo-531352ce37
```

Python 3, Pillow e compilador C do host. Previews são renders RGB555 nativos sem atores. C selecionado executa no host com serviços explícitos. Compilação ARM e execução mGBA pendentes neste ambiente. INSTALL_TEST.json registra instalação real, rollback, rejeições e repetição; SHA256_FILES.json cobre o ZIP. Próximo checkpoint: 07I — três exteriores, com portas animadas.
''')
    return manifest
def finalize(destination):
    destination=Path(destination)
    for n in ('INSTALL_TEST.json','CUMULATIVE_TEST.json'):assert json.loads((destination/n).read_text())['status']=='PASS'
    manifest=json.loads((destination/'manifest.json').read_text());names={'manifest.json','install.py','changes.patch','LEIA_ME.md','INSTALL_TEST.json','CUMULATIVE_TEST.json',*[n for n,b in BUNDLES],*('source/'+e['path'] for e in manifest['files'])}
    hashes={n:hashlib.sha256((destination/n).read_bytes()).hexdigest() for n in sorted(names)};(destination/'SHA256_FILES.json').write_text(json.dumps(hashes,indent=2)+'\n')
    output=destination.parent/'Arauna_Checkpoint_07H_BattleFrontier_Servicos_V1.zip'
    with zipfile.ZipFile(output,'w',zipfile.ZIP_DEFLATED,9) as z:
        for n in sorted(names|{'SHA256_FILES.json'}):z.write(destination/n,n)
    assert output.stat().st_size<30000000,('Package exceeds 30 MB',output.stat().st_size)
    with zipfile.ZipFile(output) as z:
        assert z.testzip() is None
        for n,h in hashes.items():assert hashlib.sha256(z.read(n)).hexdigest()==h,n
    return output
if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('destination',type=Path);ap.add_argument('--staged',action='store_true');a=ap.parse_args();package(a.destination.resolve(),a.staged)
