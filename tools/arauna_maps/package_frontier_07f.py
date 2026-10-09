#!/usr/bin/env python3
"""Exact-base Pyramid increment and cumulative Git bundles for five known histories."""
import argparse,hashlib,json,shutil,subprocess,zipfile
from pathlib import Path
from frontier_07f_common import ROOT,BASE,PREVIOUS,EARLIER,OLDER,GITHUB_9F,OUT
BUNDLES=(('checkpoint_BattleFrontier_07F.bundle',BASE),('cumulative_from_07E_07F.bundle',PREVIOUS),('cumulative_from_38d_07F.bundle',EARLIER),('cumulative_from_GitHub_9f_07F.bundle',GITHUB_9F),('cumulative_from_06C2_07F.bundle',OLDER))

def package(destination,staged=False):
    destination=Path(destination);destination.mkdir(parents=True,exist_ok=True)
    args=['git','diff','--name-only','-z']+(['--cached'] if staged else [])+[BASE]+([] if staged else ['HEAD'])
    files=[n for n in subprocess.check_output(args,cwd=ROOT).decode().split('\0') if n];assert files,'No checkpoint payload';entries=[]
    for rel in files:
        raw=(ROOT/rel).read_bytes();before=subprocess.run(['git','show',BASE+':'+rel],cwd=ROOT,capture_output=True);assert before.returncode in (0,128)
        p=destination/'source'/rel;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(raw)
        entries.append({'path':rel,'step':'07F','bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest(),'before_sha256':hashlib.sha256(before.stdout).hexdigest() if before.returncode==0 else None})
    commit=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()
    manifest={'package':'Arauna — Battle Frontier 07F: Battle Pyramid V1','base_commit':BASE,'previous_checkpoint':PREVIOUS,'earlier_github':EARLIER,'github_9f':GITHUB_9F,'older_checkpoint':OLDER,'checkpoint_commits':{} if staged else {'07F':commit},'functional_contract':'review/frontier_07f/functional_contract.json','files':entries}
    (destination/'manifest.json').write_text(json.dumps(manifest,indent=2,ensure_ascii=False)+'\n');shutil.copyfile(ROOT/'tools/arauna_maps/install_frontier_07f.py',destination/'install.py')
    args=['git','diff','--binary','--full-index']+(['--cached'] if staged else [])+[BASE]+([] if staged else ['HEAD'])
    (destination/'changes.patch').write_bytes(subprocess.check_output(args,cwd=ROOT))
    if staged:return manifest
    for name,base in BUNDLES:subprocess.run(['git','bundle','create',str(destination/name),'HEAD','^'+base],cwd=ROOT,check=True)
    shutil.copyfile(OUT/'install_test.json',destination/'INSTALL_TEST.json')
    protected=len(json.loads((OUT/'functional_contract.json').read_text())['protected_hashes'])
    (destination/'LEIA_ME.md').write_text(f'# Arauna — Battle Frontier 07F / Battle Pyramid V1\n\nCheckpoint `{commit}`, pai direto/base `{BASE}`. Lobby, Floor e Top: **29/47 mapas Frontier concluídos**, restam 18. Nenhum push foi feito.\n\nPedra escura e cobre no saguão; alvenaria nos andares; rosa dos ventos e céu de crepúsculo no topo. As imagens são renders RGB555 dos bancos nativos, sem sprites ou simulação da luz; não são fotos do mGBA.\n\n## Preservação e geração\n\n754 layouts mantêm IDs e ordem. Só três trocam referências para o par privado 4bpp. Os 16 módulos de 8×8 mantêm grids, bordas, bancos do editor, eventos e IDs. O gerador original copia os grids para o Floor ativo: 16 módulos por piso, 32×32 células, uma saída. Não tratar o stub 8×8 do Floor como o andar real. Os metatiles 0x28D (piso) e 0x28E (saída), atributos, colisões, elevação e máscaras continuam exatos.\n\nA tarefa original troca a paleta BG6 entre sete pisos. Essa paleta e seus 112 índices continuam nativos; a arte procedural usa BG6. Só BG12 recebe materiais para Lobby/Top. As tochas e sombras conservam os slots VRAM 647–654 e 663–670, callbacks, gráficos animados, flips, paletas e ciclos de oito ticks. A TV mantém Building.\n\nO contrato congela {protected} arquivos. Gerador, sementes, mapa inicial, retorno, encontros, itens, treinadores, bolsa, iluminação, saves, partidas, Brandon, recompensas e progressão não são editados. field_door.c e overworld.c, portas corrigidas da Tower, água corrigida do Palace e os 26 mapas anteriores ficam exatos.\n\n## Retomada por histórico\n\n| Bundle | Base |\n|---|---|\n| checkpoint_BattleFrontier_07F.bundle | GitHub atual / 9a3f9464ea |\n| cumulative_from_07E_07F.bundle | 07E do autor / a679c20843 |\n| cumulative_from_38d_07F.bundle | GitHub antes do 07E / 38d7879ae1 |\n| cumulative_from_GitHub_9f_07F.bundle | GitHub anterior / 9f0a056e90 |\n| cumulative_from_06C2_07F.bundle | 06C2 / 989c33c94f |\n\nEm checkout limpo da base correspondente, a partir da pasta extraída:\n\n```sh\ngit -C /caminho/do/repositorio bundle verify "$PWD/checkpoint_BattleFrontier_07F.bundle"\ngit -C /caminho/do/repositorio fetch "$PWD/checkpoint_BattleFrontier_07F.bundle" HEAD:codex/arauna-frontier-07f\ngit -C /caminho/do/repositorio switch codex/arauna-frontier-07f\n```\n\nTroque o bundle nas bases antigas; os cumulativos carregam as etapas e manutenções faltantes. Concilie histórico divergente em branch. main foi conferido e está 106 commits atrás da base 9a; não é base para o incremento.\n\n## Incremento sobre 9a\n\nsource/, changes.patch e install.py exigem a base 9a. Nas bases antigas use os bundles.\n\n```sh\npython3 install.py /caminho/do/repositorio --check\npython3 install.py /caminho/do/repositorio\n```\n\nO instalador confere o pacote e todas as dependências antes de escrever, rejeita bases/edições desconhecidas, faz backup/rollback, conserva HEAD e reaplica sem novas escritas. A alternativa é git apply --check changes.patch e git apply changes.patch.\n\n## Reprodução e limites\n\n```sh\npython3 tools/arauna_maps/validate_frontier_07f.py --base /checkout-limpo-9a3f9464ea\npython3 tools/arauna_maps/render_frontier_07f.py --base /checkout-limpo-9a3f9464ea\n```\n\nPython 3, Pillow e compilador C do host. 1.848 casos executam o C original de seleção, montagem, posições iniciais e distribuição de objetos contra os grids e eventos reais. Há 1.892.352 células montadas, 15.174 objetos conferidos e 14 casos da tarefa de paleta. Os serviços de header, memória, callback do script e IDs/gráficos de treinadores são fixtures explícitas. Isso não executa a seleção real do elenco, scripts, batalhas, saves ou hardware de iluminação. A lógica completa desses sistemas é protegida por hash.\n\nAuditoria de 528 mapas e todos os gates oficiais de static readiness passaram. O gate estático omite explicitamente o compile ARM. Compilação ROM e testes jogáveis no mGBA **ficam pendentes neste ambiente**, sem essas ferramentas. As notas da integração anterior não validam a nova ROM.\n\nINSTALL_TEST.json cobre instalação real, rollback, rejeições e repetição. CUMULATIVE_TEST.json cobre importação dos cinco bundles em receptores independentes, ancestralidade, árvore, hashes e patch. SHA256_FILES.json cobre o conteúdo do ZIP. Documentação: source/docs/BATTLE_FRONTIER_CHECKPOINT_07F.md.\n\nPróximo checkpoint: **07G — nove lounges e casa de Scott (10 mapas)**.\n')
    return manifest

def finalize(destination):
    destination=Path(destination)
    for n in ('INSTALL_TEST.json','CUMULATIVE_TEST.json'):assert json.loads((destination/n).read_text())['status']=='PASS'
    hashes={p.relative_to(destination).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(destination.rglob('*')) if p.is_file() and p.name!='SHA256_FILES.json'}
    (destination/'SHA256_FILES.json').write_text(json.dumps(hashes,indent=2)+'\n')
    output=destination.parent/'Arauna_Checkpoint_07F_BattleFrontier_Pyramid_V1.zip'
    with zipfile.ZipFile(output,'w',zipfile.ZIP_DEFLATED,9) as z:
        for p in sorted(destination.rglob('*')):
            if p.is_file():z.write(p,p.relative_to(destination))
    return output

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('destination',type=Path);ap.add_argument('--staged',action='store_true');a=ap.parse_args();package(a.destination.resolve(),a.staged)
    print('Package staged for installation checks.' if a.staged else 'Package prepared; run cumulative checks before finalize.')
