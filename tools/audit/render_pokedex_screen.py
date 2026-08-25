#!/usr/bin/env python3
"""Render the Pokedex info screen exactly as the GBA draws it.

Reads the real assets -- the menu tileset, the info_screen tilemap, the
national palette, the FONT_NORMAL glyph sheet and its width table, the
charmap, and the compiled pokedex_entries.h / pokedex_text.h -- and
composes a 240x160 frame at the same coordinates PrintMonInfo uses.
Height and weight go through the game\x27s own integer conversions.

This lets dex layout be checked without a full playthrough:
  python3 tools/audit/render_pokedex_screen.py 1 25 386 --out shots/
  python3 tools/audit/render_pokedex_screen.py --all --scan
"""
import re,sys
from PIL import Image
ROOT="/home/user/pokemon-juramento-de-arauna/"
vals=[int(x) for x in re.findall(r'\d+',re.search(r'gFontNormalLatinGlyphWidths\[\] = \{(.*?)\};',open(ROOT+'src/fonts.c').read(),re.S).group(1))]
cm={}
for line in open(ROOT+'charmap.txt',encoding='utf-8'):
    line=line.split('@')[0].strip()
    m=re.match(r"^'(\\?.)'\s*=\s*([0-9A-Fa-f]{2})$",line)
    if m:
        ch=m.group(1); ch="'" if ch=="\\'" else ch
        cm[ch]=int(m.group(2),16)
font=Image.open(ROOT+'graphics/fonts/latin_normal.png').convert('RGBA')
def glyph(b):
    r,c=divmod(b,16)
    return font.crop((c*16,r*16,c*16+16,r*16+16))
# palette: idx0 transparent, 1 shadow-dark, 2 mid, 3 white -> recolour to dex look
def draw(img,s,x,y,fg=(64,64,64),sh=(200,200,200)):
    for ch in s:
        b=cm[ch]; g=glyph(b); px=g.load()
        for gy in range(16):
            for gx in range(16):
                r_,g_,b_,a=px[gx,gy]
                # source palette entry 0 = (144,200,255) transparent key
                if (r_,g_,b_)==(56,56,56): col=fg
                elif (r_,g_,b_)==(216,216,216): col=sh
                else: continue
                if 0<=x+gx<240 and 0<=y+gy<160: img.putpixel((x+gx,y+gy),col)
        x+=vals[b]
    return x
def width(s): return sum(vals[cm[c]] for c in s)
import struct
ROOT='/home/user/pokemon-juramento-de-arauna/'
# --- background: menu.png tiles + info_screen.bin tilemap + bg_national.pal
menu=Image.open(ROOT+'graphics/pokedex/menu.png')
pal=[]
for line in open(ROOT+'graphics/pokedex/bg_national.pal'):
    p=line.split()
    if len(p)==3 and all(x.isdigit() for x in p): pal.append(tuple(int(x) for x in p))
tm=open(ROOT+'graphics/pokedex/info_screen.bin','rb').read()
entries=struct.unpack('<%dH'%(len(tm)//2),tm)
mp=menu.convert('P') if menu.mode!='P' else menu
tw=mp.width//8
bg=Image.new('RGB',(256,160),(0,0,0))
for i,e in enumerate(entries):
    tx,ty=i%32,i//32
    if ty>=20: break
    tid=e&0x3FF; hf=(e>>10)&1; vf=(e>>11)&1; pl=(e>>12)&0xF
    t=mp.crop(((tid%tw)*8,(tid//tw)*8,(tid%tw)*8+8,(tid//tw)*8+8))
    if hf: t=t.transpose(Image.FLIP_LEFT_RIGHT)
    if vf: t=t.transpose(Image.FLIP_TOP_BOTTOM)
    px=t.load()
    for y in range(8):
        for x in range(8):
            c=pal[pl*16+px[x,y]] if pl*16+px[x,y]<len(pal) else (0,0,0)
            bg.putpixel((tx*8+y*0+x,ty*8+y),c)
bg=bg.crop((0,0,240,160))

# --- dex id -> species constant -> asset folder + display name
dexh=open(ROOT+'include/constants/pokedex.h').read()
order=re.findall(r'NATIONAL_DEX_(\w+)',dexh)
seen=[];  [seen.append(n) for n in order if n not in seen and n not in ('NONE','COUNT','OLD_UNOWN_B')]
DEX={}
i=0
for n in seen:
    if n in ('NONE',): continue
    i+=1; DEX[i]=n
names={}
for m in re.finditer(r'\[SPECIES_(\w+)\]\s*=\s*_\("([^"]*)"\)',open(ROOT+'src/data/text/species_names.h').read()):
    names[m.group(1)]=m.group(2)
ent=open(ROOT+'src/data/pokemon/pokedex_entries.h').read()
E={}
for m in re.finditer(r'\[NATIONAL_DEX_(\w+)\]\s*=\s*\{(.*?)\n    \}',ent,re.S):
    b=m.group(2)
    E[m.group(1)]=dict(cat=re.search(r'\.categoryName = _\("([^"]*)"\)',b).group(1),
                       h=int(re.search(r'\.height = (\d+)',b).group(1)),
                       w=int(re.search(r'\.weight = (\d+)',b).group(1)),
                       desc=re.search(r'\.description = g(\w+)PokedexText',b).group(1))
txt=open(ROOT+'src/data/pokemon/pokedex_text.h').read()
T={}
for m in re.finditer(r'const u8 g(\w+)PokedexText\[\] = _\(\s*(.*?)\);',txt,re.S):
    T[m.group(1)]=[l.replace('\\n','').replace('\\l','').replace('\\p','').replace("\\'","'")
                   for l in re.findall(r'"((?:[^"\\]|\\.)*)"',m.group(2))]

def sprite(const):
    import os,glob
    slug=const.lower()
    for p in (ROOT+'graphics/pokemon/%s/front.png'%slug,):
        if os.path.exists(p): return p
    g=glob.glob(ROOT+'graphics/pokemon/%s*/front.png'%slug)
    return g[0] if g else None

def ht(dm):
    inches=(dm*10000)//254
    if inches%10>=5: inches+=10
    ft=inches//120; inc=(inches-ft*120)//10
    return "%d\u2019%02d\u201d"%(ft,inc)
def wt(hg):
    lbs=(hg*100000)//4536
    if lbs%10>=5: lbs+=10
    return "%d.%d lbs."%(lbs//100, (lbs%100)//10)

def render(dexno):
    const=DEX[dexno]; e=E[const]
    im=bg.copy()
    sp=sprite(const)
    if sp:
        s=Image.open(sp).convert('RGBA')
        px=s.load(); w0,h0=s.size
        # index 0 of the mon palette is the transparency key
        p0=s.getpixel((0,0))
        for y in range(h0):
            for x in range(w0):
                if px[x,y][:3]!=p0[:3]:
                    X,Y=48-32+x, 56-32+y
                    if 0<=X<240 and 0<=Y<160: im.putpixel((X,Y),px[x,y][:3])
    draw(im,'No.%03d'%dexno,96,25)
    draw(im,names.get(const,const),132,25)
    draw(im,e['cat']+' POKéMON',100,41)
    draw(im,'HT',96,57); draw(im,ht(e['h']),129,57)
    draw(im,'WT',96,73); draw(im,wt(e['w']),129,73)
    lines=T[e['desc']]
    mx=max(width(l) for l in lines); x0=(240-mx)//2
    for j,l in enumerate(lines): draw(im,l,x0,95+j*16)
    return im


def _main(argv):
    import argparse, os
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("dex", nargs="*", type=int, help="national dex numbers to render")
    ap.add_argument("--all", action="store_true", help="every entry, 1..386")
    ap.add_argument("--scan", action="store_true",
                    help="report only lines that overrun the 240px screen")
    ap.add_argument("--out", default=".", help="directory for the PNGs")
    ap.add_argument("--scale", type=int, default=3)
    a = ap.parse_args(argv)

    nums = list(range(1, 387)) if a.all else (a.dex or [1])
    if a.scan:
        worst, bad = (0, None), 0
        for n in nums:
            e = E[DEX[n]]
            for line in T[e["desc"]]:
                w = width(line)
                if w > worst[0]:
                    worst = (w, (n, line))
                if w > 240:
                    print("OVERRUN %3d %4dpx %r" % (n, w, line))
                    bad += 1
        print("widest %dpx on No.%03d %r (screen is 240px)" % (worst[0], worst[1][0], worst[1][1]))
        print("%d overrunning line(s)" % bad)
        return 1 if bad else 0

    os.makedirs(a.out, exist_ok=True)
    for n in nums:
        im = render(n)
        if a.scale > 1:
            im = im.resize((240 * a.scale, 160 * a.scale), Image.NEAREST)
        p = os.path.join(a.out, "dex%03d.png" % n)
        im.save(p)
        print(p)
    return 0


if __name__ == "__main__":
    import sys
    raise SystemExit(_main(sys.argv[1:]))
