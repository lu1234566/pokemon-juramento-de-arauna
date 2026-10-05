#!/usr/bin/env python3
"""Tira os tiles de tilesets secundarios das paletas 13-15, que o overworld
nao carrega (NUM_PALS_TOTAL = 13). Para cada paleta alta usada, procura um
slot 6-12 onde as cores de que esses tiles precisam caibam -- reaproveitando
cores identicas ou indices que nenhum tile usa naquele slot -- e reindexa os
pixels. Tile compartilhado com outra paleta e duplicado num slot vago. As
cores finais na tela sao exatamente as do arquivo .pal original.
Uso: corrige_pal13.py [--aplicar] [tileset...]"""
import json,re,struct,os,sys,collections
from PIL import Image
R=os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))); os.chdir(R)
hdr=open("src/data/tilesets/headers.h").read(); met=open("src/data/tilesets/metatiles.h").read()
RESERVA={"gTileset_AraunaLigaVozes":set(range(480,484))|{504}}  # animacao EliteFour
def tdir(name):
    m=re.search(r"const struct Tileset %s =\s*\{(.*?)\};"%name,hdr,re.S)
    a=re.search(r"\.metatiles\s*=\s*(\w+)",m.group(1)).group(1)
    return os.path.dirname(re.search(r"%s\[\] = INCBIN_U16\(\"([^\"]+)\""%a,met).group(1))
def le_pal(p):
    L=open(p).read().split(); n=int(L[2])
    return [tuple(int(x) for x in L[3+3*k:6+3*k]) for k in range(n)]
def grava_pal(p,cs):
    open(p,"wb").write(("JASC-PAL\r\n0100\r\n%d\r\n"%len(cs)+"".join("%d %d %d\r\n"%c for c in cs)).encode())
def q(c): return tuple(x>>3 for x in c)   # o GBA ve RGB555
def corrige(ts,aplicar):
    d=tdir(ts); meta=bytearray(open(d+"/metatiles.bin","rb").read())
    im=Image.open(d+"/tiles.png"); assert im.mode=="P",im.mode
    W=im.size[0]//8; NT=(im.size[1]//8)*W; px=im.load()
    pal={i:le_pal(f"{d}/palettes/{i:02d}.pal") for i in range(16) if os.path.exists(f"{d}/palettes/{i:02d}.pal")}
    def tile(t): return [px[(t%W)*8+x,(t//W)*8+y] for y in range(8) for x in range(8)]
    def set_tile(t,v):
        for k,c in enumerate(v): px[(t%W)*8+k%8,(t//W)*8+k//8]=c
    ents=[struct.unpack_from("<H",meta,2*i)[0] for i in range(len(meta)//2)]
    usos=collections.defaultdict(set)  # tile local -> paletas
    for e in ents:
        t,p=e&0x3FF,e>>12
        if t>=512: usos[t-512].add(p)
    usado_idx=collections.defaultdict(set)  # slot -> indices de cor usados
    for t,ps in usos.items():
        ix=set(tile(t))-{0}
        for p in ps: usado_idx[p]|=ix
    vazios=[t for t in range(NT) if t not in usos and t not in RESERVA.get(ts,set()) and t!=0 and not any(tile(t))]
    altos=sorted({e>>12 for e in ents if e>>12>=13})
    base_usado={k:set(usado_idx.get(k,set())) for k in range(16)}
    for s in range(6,13): pal.setdefault(s,[(0,0,0)]*16)
    def aloca(ordem):
      global_plano={}; npal={k:list(v) for k,v in pal.items()}; uidx={k:set(v) for k,v in base_usado.items()}
      lidx={s:[i for i in range(1,16) if i not in uidx[s]] for s in range(6,13)}
      for a in ordem:
        tiles_a=sorted(t for t,ps in usos.items() if a in ps)
        precisa=sorted(set().union(*[set(tile(t)) for t in tiles_a])-{0})
        melhor=None
        for s in range(6,13):
            if s==a or (s in ordem and s not in global_plano): continue
            mapa={}; livres=list(lidx[s]); okk=True
            for ix in precisa:
                c=q(pal[a][ix])
                alvo=next((i for i in uidx[s] if q(npal[s][i])==c),None)
                if alvo is None:
                    if not livres: okk=False; break
                    alvo=livres.pop(0)
                mapa[ix]=alvo
            if okk:
                gasto=len(lidx[s])-len(livres)
                if melhor is None or gasto<melhor[1]: melhor=(s,gasto,mapa,livres)
        if melhor is None: return None,a,len(precisa)
        s,gasto,mapa,livres=melhor
        for ix,alvo in mapa.items():
            npal[s][alvo]=pal[a][ix]; uidx[s].add(alvo)
        lidx[s]=livres
        global_plano[a]=(s,mapa,tiles_a)
        if a<13:  # slot realocado fica vazio
            uidx[a]=set(); lidx[a]=list(range(1,16))
      return (global_plano,npal),None,None
    res,falhou,ncores=aloca(altos)
    if res is None:
        # tenta esvaziar os slots 6-12 menos usados, um ou dois
        cont=collections.Counter(e>>12 for e in ents)
        cands=sorted(range(6,13),key=lambda s:cont[s])
        for k in (1,2):
            for extra in [cands[:k]]:
                r2,_,_=aloca(extra+altos)
                if r2: res=r2; break
            if res: break
    if res is None: return ts,"SEM ESPACO para paleta %d (%d cores)"%(falhou,ncores)
    plano,novas_pal=res
    for a in []:
        tiles_a=sorted(t for t,ps in usos.items() if a in ps)
        precisa=sorted(set().union(*[set(tile(t)) for t in tiles_a])-{0})
        melhor=None
        for s in range(6,13):
            if s not in novas_pal: continue
            cores_s={q(c):i for i,c in enumerate(novas_pal[s]) if i in usado_idx[s] or i==0}
            mapa={}; livres=list(livre_idx[s]); okk=True
            for ix in precisa:
                c=q(pal[a][ix])
                alvo=next((i for i in usado_idx[s] if q(novas_pal[s][i])==c),None)
                if alvo is None:
                    if not livres: okk=False; break
                    alvo=livres.pop(0)
                mapa[ix]=alvo
            if okk:
                gasto=len(livre_idx[s])-len(livres)
                if melhor is None or gasto<melhor[1]: melhor=(s,gasto,mapa,livres)
        if melhor is None: return ts,"SEM ESPACO para paleta %d (%d cores)"%(a,len(precisa))
        s,gasto,mapa,livres=melhor
        for ix,alvo in mapa.items():
            novas_pal[s][alvo]=pal[a][ix]; usado_idx[s].add(alvo)
        livre_idx[s]=livres
        plano[a]=(s,mapa,tiles_a)
    # tiles: reindexa (ou duplica se compartilhado)
    novo_tile={}  # (tile, pal alta) -> tile local novo
    dup=0
    for a,(s,mapa,tiles_a) in plano.items():
        for t in tiles_a:
            v=[mapa.get(c,0) if c else 0 for c in tile(t)]
            if usos[t]=={a} and all(x==a for x in [a]):
                novo_tile[(t,a)]=t; pend=(t,v)
            else:
                if not vazios: return ts,"sem tile vago para duplicar"
                n=vazios.pop(0); novo_tile[(t,a)]=n; pend=(n,v); dup+=1
            novo_tile[("v",t,a)]=pend
    if aplicar:
        for k,v in list(novo_tile.items()):
            if k[0]=="v": set_tile(*v)
        for i,e in enumerate(ents):
            t,p=e&0x3FF,e>>12
            if p in plano and t>=512:
                s=plano[p][0]; n=novo_tile[(t-512,p)]
                e=(e&0x0C00)|(s<<12)|(n+512)
                struct.pack_into("<H",meta,2*i,e)
        open(d+"/metatiles.bin","wb").write(meta); im.save(d+"/tiles.png")
        for s in range(6,13):
            if novas_pal.get(s)!=pal.get(s): grava_pal(f"{d}/palettes/{s:02d}.pal",novas_pal[s])
    return ts,"OK "+", ".join("pal %d->%d (%d tiles)"%(a,v[0],len(v[2])) for a,v in plano.items())+(", %d duplicados"%dup if dup else "")
if __name__=="__main__":
    aplicar="--aplicar" in sys.argv
    alvos=[a for a in sys.argv[1:] if not a.startswith("--")]
    if not alvos:
        L=[l for l in json.load(open("data/layouts/layouts.json"))["layouts"] if l]
        alvos=sorted({l["secondary_tileset"] for l in L if l["secondary_tileset"].startswith("gTileset_Arauna")})
    for ts in alvos:
        d=tdir(ts); meta=open(d+"/metatiles.bin","rb").read()
        if not any(e>>12>=13 for (e,) in struct.iter_unpack("<H",meta)): continue
        print("%-36s %s"%corrige(ts,aplicar))
