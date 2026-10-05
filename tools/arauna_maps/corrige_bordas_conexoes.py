#!/usr/bin/env python3
"""Corrige as bordas entre mapas vizinhos: o GBA desenha a faixa do vizinho
com os tilesets do mapa atual. Para cada celula de borda que o vizinho
renderiza diferente, cria um metatile novo (mesmo ID nos dois lados): no
tileset do dono e clone exato; nos tilesets de quem enxerga, os tiles e as
cores sao transplantados. Uso: corrige_bordas.py [--aplicar]"""
import json,re,os,struct,sys,collections,glob
from pathlib import Path
from PIL import Image
R=Path(os.environ.get("ARAUNA_REPO",".")).resolve(); os.chdir(R)
sys.path.insert(0,os.environ["PREP"])
import validar_integracao as V
from fieldmap_connection_cache_v2 import rectangle
from render_native_map import Renderer as RGBR
APLICAR="--aplicar" in sys.argv
hdr=open("src/data/tilesets/headers.h").read(); met=open("src/data/tilesets/metatiles.h").read()
def tdir(n):
    m=re.search(r"const struct Tileset %s =\s*\{(.*?)\};"%n,hdr,re.S); a=re.search(r"\.metatiles\s*=\s*(\w+)",m.group(1)).group(1)
    return os.path.dirname(re.search(r"%s\[\] = INCBIN_U16\(\"([^\"]+)\""%a,met).group(1))
# --- reservas: slots de animacao de secundarios e IDs de METATILE_* usados no codigo
anim=open("src/tileset_anims.c").read()
CORPOS=dict(re.findall(r"\n(?:static )?void (\w+)\([^)]*\)\n\{(.*?)\n\}",anim,re.S))
TABS=dict(re.findall(r"(\w+)\[\]\s*=\s*\{(.*?)\};",anim,re.S))
def reserva(cb):
    if cb in (None,"NULL") or cb not in CORPOS: return set()
    vistos=set(); fila=[cb]; out=set()
    while fila:
        f=fila.pop()
        if f in vistos or f not in CORPOS: continue
        vistos.add(f); b=CORPOS[f]
        fila+=re.findall(r"(TilesetAnim_\w+|QueueAnimTiles_\w+)",b)
        for n,k in re.findall(r"NUM_TILES_IN_PRIMARY \+ (\d+)\)\), *(\d+) \* TILE_SIZE_4BPP",b): out|=set(range(int(n),int(n)+int(k)))
        for tb in re.findall(r"(s\w+|g\w+)\[",b):
            if tb in TABS:
                for n in re.findall(r"NUM_TILES_IN_PRIMARY \+ (\d+)\)",TABS[tb]): out|=set(range(int(n),int(n)+8))
        for n in re.findall(r"NUM_TILES_IN_PRIMARY \+ (\d+)\)",b): out|=set(range(int(n),int(n)+8))
    return out
def cb_de(n):
    m=re.search(r"const struct Tileset %s =\s*\{(.*?)\};"%n,hdr,re.S); c=re.search(r"\.callback\s*=\s*(\w+)",m.group(1))
    return c.group(1) if c else "NULL"
lab=dict((n,int(v,16)) for n,v in re.findall(r"#define (METATILE_\w+)\s+(0x[0-9A-Fa-f]+)",open("include/constants/metatile_labels.h").read()))
cod="".join(open(f,errors="ignore").read() for f in glob.glob("src/*.c")+glob.glob("data/scripts/*.inc")+glob.glob("data/maps/*/scripts.inc"))
RES_M={lab[n] for n in set(re.findall(r"METATILE_\w+",cod)) if n in lab}
layouts=json.load(open("data/layouts/layouts.json"))["layouts"]; L={l["id"]:l for l in layouts if l}
maps={json.load(open(p))["id"]:json.load(open(p)) for p in glob.glob("data/maps/*/map.json")}
# --- banco em memoria
class Banco:
    def __init__(s,nome):
        s.nome=nome; s.d=tdir(nome); s.meta=bytearray(open(s.d+"/metatiles.bin","rb").read()); s.attr=bytearray(open(s.d+"/metatile_attributes.bin","rb").read())
        s.im=Image.open(s.d+"/tiles.png"); s.im.load(); s.W=s.im.size[0]//8; s.NT=(s.im.size[1]//8)*s.W; s.px=s.im.load()
        s.pal={}
        for i in range(16):
            f=f"{s.d}/palettes/{i:02d}.pal"
            if os.path.exists(f): Lr=open(f).read().split(); s.pal[i]=[tuple(int(x) for x in Lr[3+3*k:6+3*k]) for k in range(16)]
        s.mud=False; s.pal_mud=set()
    def nmeta(s): return len(s.meta)//16
    def ents(s,i): return list(struct.unpack_from("<8H",s.meta,i*16))
    def tile(s,t): return tuple(s.px[(t%s.W)*8+x,(t//s.W)*8+y] for y in range(8) for x in range(8))
    def set_tile(s,t,v):
        for k,c in enumerate(v): s.px[(t%s.W)*8+k%8,(t//s.W)*8+k//8]=c
    def salva(s):
        if not s.mud: return
        open(s.d+"/metatiles.bin","wb").write(s.meta); open(s.d+"/metatile_attributes.bin","wb").write(s.attr); s.im.save(s.d+"/tiles.png")
        for i in s.pal_mud: open(f"{s.d}/palettes/{i:02d}.pal","wb").write(("JASC-PAL\r\n0100\r\n16\r\n"+"".join("%d %d %d\r\n"%c for c in s.pal[i])).encode())
B={}
def banco(n):
    if n not in B: B[n]=Banco(n)
    return B[n]
# --- usos por secundario
def layouts_de(sec): return [l for l in L.values() if l["secondary_tileset"]==sec]
VISTO=collections.defaultdict(set)   # secundario receptor -> ids que ele desenha nas bordas
def ids_usados(sec):
    u=set(VISTO.get(sec,()))
    for l in layouts_de(sec):
        for fp in (l["blockdata_filepath"],l["border_filepath"]):
            for (b,) in struct.iter_unpack("<H",open(fp,"rb").read()): u.add(b&0x3FF)
    return u
def estado_sec(sec):
    """tiles locais usados e indices de cor usados por slot, considerando o
    secundario e todos os primarios com que ele aparece"""
    s=banco(sec); prims={l["primary_tileset"] for l in layouts_de(sec)}
    tus=set(); cor=collections.defaultdict(set)
    for b in [s]+[banco(p) for p in prims]:
        for i in range(b.nmeta()):
            for e in b.ents(i):
                t,p=e&0x3FF,e>>12
                if t>=512:
                    tus.add(t-512)
                    if 6<=p<=12 and t-512<s.NT: cor[p]|=set(s.tile(t-512))-{0}
                elif 6<=p<=12:
                    for pn in prims:
                        pbx=banco(pn)
                        if t<pbx.NT: cor[p]|=set(pbx.tile(t))-{0}
    # primarios usando paletas 6-12 com tiles primarios
    for pn in prims:
        pb=banco(pn)
        for i in range(pb.nmeta()):
            for e in pb.ents(i):
                t,p=e&0x3FF,e>>12
                if t<512 and 6<=p<=12 and t<pb.NT: cor[p]|=set(pb.tile(t))-{0}
    return tus,cor
# --- falhas
R2={};G={};SIG={}
def get(mid):
    m=maps[mid]; l=L[m["layout"]]; k=(l["primary_tileset"],l["secondary_tileset"])
    if k not in R2: R2[k]=V.Renderer(V.resolve_bank(R,k[0]),V.resolve_bank(R,k[1]))
    if m["layout"] not in G: G[m["layout"]]=V.words(R/l["blockdata_filepath"])
    return l,R2[k],G[m["layout"]]
def sig(r,mid):
    k=(str(r.primary),str(r.secondary),mid)
    if k not in SIG: SIG[k]=V.normalized(r,mid)
    return SIG[k]
celulas=collections.defaultdict(lambda:{"ruim":False,"rec":set()})  # (layoutB,x,y) -> receptores
for mid,m in maps.items():
    for c in m.get("connections") or []:
        if c["direction"] in ("dive","emerge"): continue
        cur,cr,_=get(mid); oth,pr,grid=get(c["map"])
        if cur["secondary_tileset"].startswith("gTileset_BattleFrontier"): continue
        for x,y in rectangle(cur["width"],cur["height"],oth["width"],oth["height"],c["offset"],c["direction"]):
            t=grid[y*oth["width"]+x]&1023
            try: ok=sig(cr,t)==sig(pr,t) and V.bank_words(cr,t,True)==V.bank_words(pr,t,True)
            except ValueError: ok=False
            k=(oth["id"],x,y); celulas[k]["rec"].add((cur["primary_tileset"],cur["secondary_tileset"]))
            VISTO[cur["secondary_tileset"]].add(t)
            if not ok: celulas[k]["ruim"]=True
ruins={k:v for k,v in celulas.items() if v["ruim"]}
RGB={}
def rgb(par,mid):
    if par not in RGB: RGB[par]=RGBR(V.resolve_bank(R,par[0]),V.resolve_bank(R,par[1]))
    try: return (RGB[par].metatile(mid).convert("RGB").tobytes(),V.bank_words(R2.get(par) or get_r(par),mid,True))
    except Exception: return None
def get_r(par):
    if par not in R2: R2[par]=V.Renderer(V.resolve_bank(R,par[0]),V.resolve_bank(R,par[1]))
    return R2[par]
def ja_bom(par_rec,par_dono,mid):
    a=rgb(par_rec,mid); b=rgb(par_dono,mid)
    if a is None or b is None or a[1]!=b[1]: return False
    return max(abs(x-y) for x,y in zip(a[0],b[0]))<=48
print("celulas a corrigir:",len(ruins))
# --- agrupa por (layoutB, id original, conjunto de receptores)
grupos=collections.defaultdict(list)
for (lid,x,y),v in ruins.items():
    t=G[lid][y*L[lid]["width"]+x]&1023
    grupos[(lid,t,frozenset(v["rec"]))].append((x,y))
print("grupos (id novo cada):",len(grupos))
usados_cache={}
def mortos(sec):
    if sec not in usados_cache: usados_cache[sec]=ids_usados(sec)
    return usados_cache[sec]
reservados_novos=collections.defaultdict(set)
estados={}
def est(sec):
    if sec not in estados: estados[sec]=estado_sec(sec)
    return estados[sec]
def livre_id(secs):
    for cand in range(0x200,0x400):
        if cand in RES_M: continue
        ok=True
        for s in secs:
            b=banco(s)
            if cand in mortos(s) or cand in reservados_novos[s]: ok=False; break
        if ok: return cand
    return None
def transplanta(dst_p,dst_s,src_p,src_s,t_src_meta):
    """define em dst_s um metatile que reproduz t_src_meta de (src_p,src_s); devolve 8 entradas"""
    sp,ss=banco(src_p),banco(src_s); ds=banco(dst_s)
    sb=sp if t_src_meta<512 else ss; ents=sb.ents(t_src_meta%512)
    tus,cor=est(dst_s)
    novas=[]; aprox=0
    for e in ents:
        t,fl,p=e&0x3FF,e&0x0C00,e>>12
        tb=sp if t<512 else ss; tl=t%512
        pix=tb.tile(tl) if tl<tb.NT else (0,)*64
        pal=(sp.pal if p<6 else ss.pal).get(p,[(0,0,0)]*16)
        need=sorted(set(pix)-{0})
        melhor=None
        for q in range(6,13):
            if q not in ds.pal: continue
            usados=cor[q]; livres=[i for i in range(1,16) if i not in usados]
            mapa={}; erro=0; novos=[]
            for ix in need:
                c=pal[ix]; ex=next((i for i in usados if ds.pal[q][i]==c),None)
                if ex is None and livres: ex=livres.pop(0); novos.append((ex,c))
                if ex is None:
                    ex=min(usados,key=lambda i:sum((a-b)**2 for a,b in zip(ds.pal[q][i],c))); erro+=sum((a-b)**2 for a,b in zip(ds.pal[q][ex],c))
                mapa[ix]=ex
            chave=(erro,len(novos))
            if melhor is None or chave<melhor[0]: melhor=(chave,q,mapa,novos)
        (erro,_),q,mapa,novos=melhor
        if erro: aprox+=1
        for i,c in novos: ds.pal[q][i]=c; cor[q].add(i); ds.pal_mud.add(q)
        v=tuple(mapa.get(c,0) if c else 0 for c in pix)
        # reaproveita tile identico ja existente com mesma paleta
        alvo=None
        for cand in range(ds.NT):
            if cand in tus and ds.tile(cand)==v: alvo=cand; break
        if alvo is None:
            rt=reserva(cb_de(dst_s)); alvo=next((c for c in range(1,ds.NT) if c not in tus and c not in rt),None)
            if alvo is None: raise Falta("sem tile livre em "+dst_s)
            ds.set_tile(alvo,v); tus.add(alvo)
        for k2 in (q,): cor[k2]|=set(v)-{0}
        novas.append(fl|(q<<12)|(alvo+512))
    ds.mud=True
    return novas,aprox
tot_aprox=0; feitos=0; pulados=[]
grids_mod={}
class Falta(Exception): pass
def poe(b,i,ents8,a):
    i-=0x200
    while b.nmeta()<i: b.meta+=struct.pack("<8H",*([0]*8)); b.attr+=struct.pack("<H",0)
    if i==b.nmeta(): b.meta+=struct.pack("<8H",*ents8); b.attr+=struct.pack("<H",a)
    else: struct.pack_into("<8H",b.meta,i*16,*ents8); struct.pack_into("<H",b.attr,2*i,a)
    b.mud=True
def aplica_grupo(lid,t,recs,cels,secs,nid,lb,secB,primB):
    global tot_aprox
    bB=banco(secB); srcb=banco(primB) if t<512 else bB
    ents=srcb.ents(t%512); at=struct.unpack_from("<H",srcb.attr,2*(t%512))[0]
    compartilhado=[(rp,rs) for (rp,rs) in recs if rs==secB and rp!=primB]
    if compartilhado:
        # dono e receptor dividem o secundario: uma so definicao, com tiles e
        # paletas do secundario, serve aos dois -- desde que as cores sejam exatas
        rp,rs=compartilhado[0]
        novas,ap=transplanta(rp,rs,primB,secB,t)
        if ap: raise Falta("cor aproximada em secundario compartilhado "+secB)
        poe(bB,nid,novas,at)
    else:
        poe(bB,nid,ents,at)
    for (rp,rs) in sorted(recs):
        if rs==secB: continue
        if ja_bom((rp,rs),(primB,secB),t):
            # este receptor ja via a celula bem: clona o proprio metatile dele
            src=banco(rp) if t<512 else banco(rs)
            poe(banco(rs),nid,src.ents(t%512),struct.unpack_from("<H",src.attr,2*(t%512))[0])
            continue
        novas,ap=transplanta(rp,rs,primB,secB,t); tot_aprox+=ap
        poe(banco(rs),nid,novas,at)
    g=grids_mod.setdefault(lid,bytearray(open(lb["blockdata_filepath"],"rb").read()))
    for x,y in cels:
        i=y*lb["width"]+x; b=struct.unpack_from("<H",g,2*i)[0]; struct.pack_into("<H",g,2*i,(b&0xFC00)|nid)
for (lid,t,recs),cels in sorted(grupos.items()):
    lb=L[lid]; secB=lb["secondary_tileset"]; primB=lb["primary_tileset"]
    secs=[secB]+sorted({r[1] for r in recs})
    nid=livre_id(secs)
    if nid is None:
        pulados.append((lid,hex(t),"sem id")); continue
    envolvidos=set(secs)
    foto={s:(bytes(banco(s).meta),bytes(banco(s).attr),banco(s).im.copy(),{k:list(v) for k,v in banco(s).pal.items()},set(banco(s).pal_mud),banco(s).mud) for s in envolvidos}
    foto_est={s:(set(est(s)[0]),{k:set(v) for k,v in est(s)[1].items()}) for s in envolvidos}
    grid_antes=bytes(grids_mod[lid]) if lid in grids_mod else None
    try:
        aplica_grupo(lid,t,recs,cels,secs,nid,lb,secB,primB)
        for s in secs: reservados_novos[s].add(nid)
        feitos+=1
    except Falta as e:
        for s,(m,a,im,pal,pm,md) in foto.items():
            b=banco(s); b.meta=bytearray(m); b.attr=bytearray(a); b.im=im; b.px=im.load(); b.pal=pal; b.pal_mud=pm; b.mud=md
        for s,(tu,co) in foto_est.items(): estados[s]=(tu,collections.defaultdict(set,co))
        if grid_antes is not None: grids_mod[lid]=bytearray(grid_antes)
        else: grids_mod.pop(lid,None)
        pulados.append((lid,hex(t),str(e)))
print("grupos corrigidos:",feitos,"pulados:",len(pulados),"tiles com cor aproximada:",tot_aprox)
for p_ in pulados: print("   pulado",p_)
print("bancos alterados:",sorted(n[9:] for n,b in B.items() if b.mud))
if APLICAR:
    for b in B.values(): b.salva()
    for lid,g in grids_mod.items(): open(L[lid]["blockdata_filepath"],"wb").write(g)
    print("aplicado")
