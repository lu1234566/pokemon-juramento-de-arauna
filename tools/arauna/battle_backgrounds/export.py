#!/usr/bin/env python3
"""Deterministic RGB555/4bpp compiler for the approved Arauna backgrounds.
Requires Pillow and numpy. --concept-dir projects original artwork to native
resolution; without that option recompiles the editable indexed scene.png.
"""
import argparse, hashlib, json, struct, math, subprocess, tempfile, zlib
from pathlib import Path
import numpy as np
from PIL import Image, ImageFile
ROOT = Path(__file__).resolve().parents[3]
HERE = Path(__file__).resolve().parent
GBAGFX = ROOT / 'tools/gbagfx/gbagfx'

def rom_bytes(folder):
    """Quantos bytes de ROM este cenario custa, medidos como o build mede.

    Quem comprime de verdade e o gbagfx, na compilacao, a partir das fontes
    versionadas. O lz77 deste arquivo e uma segunda implementacao: serve para
    conferir a ida e volta, mas sai algumas dezenas de bytes diferente, entao
    medir por ela daria um numero que nao e o da ROM. Aqui a cadeia e a mesma
    do Makefile, e nada e escrito na arvore.
    """
    total = 0
    with tempfile.TemporaryDirectory() as d:
        d = Path(d)
        for origem, meio in [('tiles.png', 'tiles.4bpp'),
                             ('palette.pal', 'palette.gbapal'),
                             ('map.bin', None)]:
            fonte = folder / origem
            if meio:
                alvo = d / meio
                subprocess.run([str(GBAGFX), str(fonte), str(alvo)], check=True)
                fonte = alvo
            packed = d / (fonte.name + '.lz')
            subprocess.run([str(GBAGFX), str(fonte), str(packed)], check=True)
            total += packed.stat().st_size
    return total

def lz77(data):
    out=bytearray(b'\x10'+len(data).to_bytes(3,'little'));positions={};p=0
    while p<len(data):
        flag=len(out);out.append(0)
        for bit in range(7,-1,-1):
            if p==len(data):break
            start=p;best=2;distance=0
            for prev in reversed(positions.get(data[p:p+3],[])[-128:]):
                d=p-prev
                if d>4096:break
                if d<2:continue # BIOS VRAM decompression writes halfwords.
                n=3
                while n<18 and p+n<len(data) and data[prev+n]==data[p+n]:n+=1
                if n>best:best,distance=n,d
                if n==18:break
            if best>=3:
                out[flag]|=1<<bit;v=((best-3)<<12)|(distance-1)
                out.extend((v>>8,v&255));p+=best
            else:out.append(data[p]);p+=1
            for q in range(start,p):positions.setdefault(data[q:q+3],[]).append(q)
    out.extend(bytes(-len(out)%4));return bytes(out)

def decode_lz(data):
    assert data[0]==16
    size=int.from_bytes(data[1:4],'little');out=bytearray();p=4
    while len(out)<size:
        flags=data[p];p+=1
        for bit in range(7,-1,-1):
            if len(out)==size:break
            if flags&(1<<bit):
                v=int.from_bytes(data[p:p+2],'big');p+=2;n=(v>>12)+3;d=(v&4095)+1
                assert 2<=d<=len(out)
                for _ in range(n):out.append(out[-d])
            else:out.append(data[p]);p+=1
    assert len(out)==size
    return bytes(out)

def to555(a):return np.rint(a.astype(float)*31/255).astype(np.int32)
def to888(a):return ((a*255+15)//31).astype(np.uint8)

def read_concept(source, height):
    try:
        im=Image.open(source);im.load()
    except OSError:
        # One restored R118 source lost its bottom PNG tail. Only accept it if
        # ALL scanlines used by our native projection decoded completely.
        data=source.read_bytes();off=8;decoder=zlib.decompressobj();count=0
        while off+8<=len(data):
            n=int.from_bytes(data[off:off+4],'big');kind=data[off+4:off+8];chunk=data[off+8:off+8+n]
            if kind==b'IHDR':w,h,depth,color=struct.unpack('>IIBB',chunk[:10]);assert depth==8 and color in (2,6)
            if kind==b'IDAT':count+=len(decoder.decompress(chunk))
            off+=n+12
        assert count//(w*(4 if color==6 else 3)+1)>=math.ceil(h*128/height)+2, 'Source is missing visible pixels'
        old=ImageFile.LOAD_TRUNCATED_IMAGES
        try:
            ImageFile.LOAD_TRUNCATED_IMAGES=True;im=Image.open(source);im.load()
        finally:ImageFile.LOAD_TRUNCATED_IMAGES=old
    # The box excludes every pixel hidden below the native guard region.
    return im.convert('RGB').resize((240,128),Image.Resampling.BOX,box=(0,0,im.width,im.height*128/height))

def native_image(im):
    pixels=to555(np.array(im.convert('RGB')))
    tiles=pixels.reshape(16,8,30,8,3).transpose(0,2,1,3,4).reshape(-1,8,8,3)
    groups=np.minimum(np.arange(480)//160,2)
    for _ in range(5):
        palettes=[];errors=[];indices=[]
        for bank in range(3):
            selected=tiles[groups==bank]
            if not len(selected):selected=tiles
            q=Image.fromarray(to888(selected).reshape(-1,8,3)).quantize(15,method=Image.Quantize.MEDIANCUT,dither=Image.Dither.NONE)
            colors=to555(np.array(q.getpalette()[:45]).reshape(15,3));palettes.append(colors)
            delta=tiles[:,:,:,None,:].astype(np.float32)-colors[None,None,None,:,:]
            dist=(delta*delta*np.array([2,3,2])).sum(axis=-1);idx=dist.argmin(axis=-1)
            errors.append(np.take_along_axis(dist,idx[...,None],axis=-1).mean(axis=(1,2,3)));indices.append(idx+1)
        groups=np.stack(errors).argmin(axis=0)
    pal=np.zeros((48,3),dtype=np.int32)
    for bank in range(3):pal[bank*16+1:bank*16+16]=palettes[bank]
    indices=np.stack(indices)[groups,np.arange(480)]+groups[:,None,None]*16
    src=indices.reshape(16,30,8,8).transpose(0,2,1,3).reshape(128,240).astype('uint8')
    im=Image.fromarray(src,mode='P');im.putpalette(to888(pal).ravel().tolist()+[0]*624)
    return im

def compile_image(im,folder):
    assert im.mode=='P' and im.size==(240,128)
    pal=to555(np.array(im.getpalette()[:144]).reshape(48,3))
    src=np.array(im);tiles=src.reshape(16,8,30,8).transpose(0,2,1,3).reshape(-1,8,8)
    atlas=[bytes(64)];lookup={bytes(64):0};words=[]
    for tile in tiles:
        banks=np.unique(tile//16);assert len(banks)==1 and banks[0]<3
        local=tile%16;assert np.all(local>0)
        data=local.tobytes();match=lookup.get(data)
        if match is None:
            match=len(atlas);atlas.append(data);lookup[data]=match
            lookup.setdefault(local[:,::-1].tobytes(),match|1024)
            lookup.setdefault(local[::-1,:].tobytes(),match|2048)
            lookup.setdefault(local[::-1,::-1].tobytes(),match|3072)
        words.append(match|((int(banks[0])+2)<<12))
    assert len(atlas)<=512
    grid=np.array(words,dtype='<u2').reshape(16,30)
    screen=np.pad(grid,((0,16),(0,2)),mode='edge');screen[31]=screen[0];screen[:,31]=screen[:,0]
    tilemap=screen.astype('<u2').tobytes()*2
    a=np.array([list(t) for t in atlas],dtype='uint8')
    raw=(a[:,::2]|(a[:,1::2]<<4)).tobytes()
    palette=struct.pack('<48H',*[int(r|(g<<5)|(b<<10)) for r,g,b in pal])
    folder.mkdir(parents=True,exist_ok=True)
    # So map.bin e gravado dos tres fluxos: .4bpp, .gbapal e .lz sao produto de
    # build neste repositorio -- o .gitignore os ignora e o clean-assets do
    # Makefile apaga os tres em toda a arvore, entao grava-los aqui produziria
    # arquivos que nao entram em commit nenhum e somem no primeiro make clean.
    # O compilador os refaz de tiles.png, map.bin e palette.pal. A ida e volta
    # do LZ77 continua sendo conferida, so que sem deixar rastro.
    for name,data in [('tiles.4bpp',raw),('map.bin',tilemap),('palette.gbapal',palette)]:
        assert decode_lz(lz77(data))==data,name
    (folder/'map.bin').write_bytes(tilemap)
    im.save(folder/'scene.png',optimize=True)
    rows=(len(atlas)+15)//16;ta=np.zeros((rows*16,64),dtype='uint8');ta[:len(atlas)]=a
    tilepng=Image.fromarray(ta.reshape(rows,16,8,8).transpose(0,2,1,3).reshape(rows*8,128),mode='P')
    tilepng.putpalette(im.getpalette());tilepng.save(folder/'tiles.png',bits=4)
    (folder/'palette.pal').write_text('JASC-PAL\n0100\n48\n'+'\n'.join(' '.join(map(str,c)) for c in to888(pal))+'\n')
    return dict(tiles=len(atlas),tile_bytes=len(raw),palette_bytes=96,compressed_bytes=rom_bytes(folder))

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--concept-dir',type=Path);parser.add_argument('--only',nargs='*');args=parser.parse_args();manifest=[]
    for c in json.loads((HERE/'concepts.json').read_text()):
        if args.only and c['id'] not in args.only:continue
        folder=ROOT/'graphics/battle_environment/arauna'/c['id'].lower()
        if args.concept_dir:
            source=args.concept_dir/c['source_file'];assert hashlib.sha256(source.read_bytes()).hexdigest()==c['source_sha256']
            # Native projection: opponent base ~y64, player base ~y108.
            image=read_concept(source,c['export_height'])
            image=native_image(image)
        else:image=Image.open(folder/'scene.png')
        stats=compile_image(image,folder);manifest.append(dict(c,**stats));print(c['id'],stats,flush=True)
    common=ROOT/'graphics/battle_environment/arauna/common';common.mkdir(parents=True,exist_ok=True)
    # Transparent entry layer keeps trainer slide/iris timing without recoloring
    # a vanilla grass/water foreground with the unrelated concept palette.
    # Pelo mesmo motivo dos outros fluxos, o que fica versionado sao as fontes:
    # um PNG de um tile vazio e o tilemap zerado. O build faz os .lz.
    entrada=Image.new('P',(8,8),0)
    entrada.putpalette([255,0,255]+[0,0,0]*15)
    entrada.save(common/'entry.png')
    (common/'entry_map.bin').write_bytes(bytes(2048))
    if not args.only:(HERE/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':main()
