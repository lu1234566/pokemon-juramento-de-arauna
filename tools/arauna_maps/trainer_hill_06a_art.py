"""Native indexed motifs: sandstone, olive canvas and masonry/wood planes."""
from functools import lru_cache
from PIL import Image,ImageDraw

MATERIAL=[(0,0,0),(40,32,24),(72,48,32),(104,72,48),(152,112,72),(192,160,112),(224,200,152),(248,232,184),(56,72,40),(96,112,64),(152,160,96),(32,48,56),(64,80,88),(112,128,136),(184,200,192),(128,160,176)]
PLAIN={0x225,0x226,0x22d,0x22e,0x231,0x235,0x236,0x238,0x239,0x23a,0x23b,0x245,0x25e,0x265,0x267,0x269,0x26d,0x271,0x272,0x273,0x286,0x287,0x28d,0x28e,0x291,0x295,0x296,0x298,0x299,0x29a,0x29b,0x29c,0x2b3,0x2bb,0x2c5,0x2c6,0x2c7,0x2cd,0x2ce,0x2d1,0x2d5,0x2d6,0x2d9,0x2db,0x2e5,0x2e6,0x2ed,0x2ee,0x2f1,0x2f5,0x2f6,0x2f8,0x2f9,0x2fa,0x2fb}
DOORS_STAIRS={0x32c,0x383,0x343,0x334,0x219,0x21e,0x382}
PLINTHS={0x223,0x224,0x22b,0x22c,0x233,0x234,0x263,0x264,0x26c,0x284,0x28b,0x28c,0x294,0x2c3,0x2c4,0x2cb,0x2cc,0x2d4,0x2eb,0x2ec,0x2f4}
SLATE_ROOF={0x358,0x359,0x35a,0x35c,0x35d,0x360,0x361,0x364,0x365,0x367,0x36a}

@lru_cache(None)
def slab(variant=0,family='sand'):
    # Offset joints are sparse, with a two-tone edge and chipped stone corner.
    lo,base,hi={'sand':(4,5,6),'olive':(8,9,10),'ochre':(3,4,5),'clay':(2,3,4),'slate':(11,12,13)}[family]
    im=Image.new('L',(16,16),base);d=ImageDraw.Draw(im)
    d.line((0,0,15,0),fill=hi);d.line((0,15,15,15),fill=lo)
    seam=3 if variant%2 else 11;d.line((seam,1,seam,7),fill=lo);d.line(((seam+8)%16,9,(seam+8)%16,14),fill=lo)
    d.line((0,8,15,8),fill=hi);d.point((seam+1,2),fill=hi)
    d.line((2+variant%3,12,4+variant%3,12),fill=hi)
    return im

@lru_cache(None)
def canvas(variant=0):
    im=Image.new('L',(16,16),9);d=ImageDraw.Draw(im)
    d.rectangle((0,0,15,15),outline=8);d.rectangle((1,1,14,14),outline=10)
    if variant:
        d.polygon([(8,4),(11,8),(8,11),(4,8)],fill=10)
        d.rectangle((7,7,8,8),fill=9)
    return im

@lru_cache(None)
def barrier():
    im=Image.new('L',(16,16),1);d=ImageDraw.Draw(im)
    d.rectangle((0,0,15,9),fill=6);d.line((0,0,15,0),fill=7)
    d.line((0,9,15,9),fill=4);d.rectangle((0,10,15,14),fill=3)
    d.line((0,10,15,10),fill=5);d.line((7,1,7,8),fill=5)
    d.line((3,11,3,14),fill=2);d.line((12,11,12,14),fill=2)
    return im

def recolor(pals):
    result=[list(p) for p in pals]
    # 7 and 9 are used directly by the native elevator door animations.
    for q,pal in enumerate(result):
        if q in (7,9):continue
        for i,(r,g,b) in enumerate(pal):
            if not i:continue
            if g>r*1.06 and g>b*.90:
                light=(r+g+b)//3;r,g,b=int(light*.94),int(light*.89),int(light*.60)
            elif b>r*1.1:r,g,b=int(r*.86),int(g*.92),int(b*.90)
            else:r,g,b=int(r*.95),int(g*.87),int(b*.74)
            result[q][i]=tuple(max(0,min(248,c))//8*8 for c in (r,g,b))
    result[12]=MATERIAL
    return result

def native_layers(reader,mid):
    entries=(reader.primary_metatiles if mid<512 else reader.secondary_metatiles)[mid%512*8:mid%512*8+8]
    result=[]
    for layer in range(2):
        im=Image.new('RGBA',(16,16))
        for j,(dx,dy) in enumerate(((0,0),(8,0),(0,8),(8,8))):
            e=entries[layer*4+j];tile=reader._tile(e&1023)
            if tile is None:continue
            if e&0x400:tile=tile.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
            if e&0x800:tile=tile.transpose(Image.Transpose.FLIP_TOP_BOTTOM)
            pal=reader.palettes[e>>12]
            rgba=Image.new('RGBA',(8,8));rgba.putdata([(*pal[v],255 if v else 0) for v in tile.getdata()])
            im.alpha_composite(rgba,(dx,dy))
        result.append(im)
    return result

def material_planes(reader,mid,roof=False):
    # Keep each native layer's alpha and object footprint. Stone joints only
    # occupy the large mint planes; outlines, windows and equipment remain.
    result=[]
    for native in native_layers(reader,mid):
        im=Image.new('L',(16,16));pixels=[]
        for i,(r,g,b,a) in enumerate(native.getdata()):
            if not a:pixels.append(0);continue
            x,y=i%16,i//16
            plane=g>r*1.12 and b>r*1.04 and g>b*.85
            if plane:
                lum=(r+g+b)//3;v=4 if lum<125 else 5 if lum<180 else 6
                if mid in SLATE_ROOF:
                    v=11 if lum<125 else 12 if lum<180 else 13
                    if y in (4,12):v=max(11,v-1)
                    if x==(3 if y<8 else 11) and lum>115:v=max(11,v-1)
                else:
                    if y in (3,11) and lum>115:v=max(3,v-1)
                    if x==(6 if y<8 else 14) and lum>115:v=max(3,v-1)
                    if x==3 and y==6 and lum>155:v=7
            else:
                if r>g*1.13 and g>b*1.05:target=(r*.94,g*.83,b*.66)
                elif max(r,g,b)-min(r,g,b)<45 and max(r,g,b)>185:target=(min(248,r),min(232,g*.92),min(192,b*.72))
                else:target=(r*.75,g*.8,b*.76)
                candidates=range(1,15)
                v=min(candidates,key=lambda n:sum((MATERIAL[n][j]-target[j])**2 for j in range(3)))
            pixels.append(v)
        im.putdata(pixels);result.append(im)
    return result

def family(mid):
    if 0x2c0<=mid<0x2e0:return 'clay'
    if mid>=0x2e0:return 'slate'
    if 0x280<=mid<0x2a0:return 'ochre'
    if 0x260<=mid<0x280:return 'olive'
    return 'sand'
