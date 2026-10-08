"""Indexed rock strata and salt/weathered wood, with native layer silhouettes."""
from PIL import Image
from trainer_hill_06a_art import native_layers
from native_visuals_v2 import Pair

class NavelPair(Pair):
    """Reserve Dewford's live flag destination before compacting static tiles."""
    def __init__(self,repo,layout):
        super().__init__(repo,layout,repack=False)
        if self.callbacks[1]=='InitTilesetAnim_Dewford':
            self.dynamic.update(range(682,688))
        source=dict(self.tiles)
        self.tiles={i:raw for i,raw in source.items() if i in self.dynamic}
        self.tiles[0]=bytes(64);self.tile_cache={bytes(64):0}
        self.free=[i for i in [*range(1,432),*range(512,992)] if i not in self.dynamic]
        remap={}
        for entries in self.meta:
            for j,e in enumerate(entries):
                t=e&1023
                if t in self.dynamic:continue
                if t not in remap:remap[t]=self.tile(Image.frombytes('L',(8,8),source.get(t,bytes(64))))
                entries[j]=(e&~1023)|remap[t]

RAMPS={
 'coast':[(24,32,32),(40,48,48),(56,64,64),(72,88,88),(96,112,104),(120,136,128),(152,168,152),(184,200,176),(224,232,208)],
 'gallery':[(24,32,32),(40,48,48),(56,72,72),(80,88,80),(104,120,104),(128,144,120),(160,176,144),(192,208,176),(224,232,200)],
 'ascent':[(32,32,24),(56,56,40),(80,80,56),(112,104,72),(136,128,88),(160,152,112),(192,184,144),(224,216,176),(248,240,208)],
 'summit':[(40,40,24),(64,56,32),(96,88,48),(128,112,72),(160,144,96),(184,168,120),(216,200,152),(240,224,184),(248,240,216)],
 'depth1':[(16,24,32),(24,40,48),(40,56,64),(56,80,88),(80,104,112),(104,128,136),(128,160,160),(160,192,184),(200,216,208)],
 'depth2':[(16,24,32),(24,32,48),(32,48,64),(48,64,80),(64,88,104),(88,112,128),(112,144,152),(144,176,176),(184,208,200)],
 'abyss':[(8,16,24),(16,24,40),(24,40,56),(32,56,72),(48,72,88),(64,96,112),(88,128,144),(120,168,176),(176,208,208)],
 'dock':[(24,32,32),(40,48,48),(56,72,72),(80,88,88),(104,120,112),(128,144,128),(160,176,152),(192,208,184),(224,232,208)]}

def material(theme):
    sky=(112,184,240) if theme=='summit' else (128,176,200)
    return [(0,0,0),*RAMPS[theme],(48,32,24),(96,64,40),(152,112,64),(32,104,128),(176,216,216),sky]

def palettes(pals,theme):
    result=[list(p) for p in pals];ramp=RAMPS[theme]
    for q,pal in enumerate(result):
        for i,(r,g,b) in enumerate(pal):
            if not i:continue
            lum=(r+g+b)//3
            if theme=='summit' and tuple(c>>3<<3 for c in (r,g,b))==(112,184,240):color=(112,184,240)
            elif b>r*1.2 and b>g*.97:color=(int(lum*.42),int(lum*.92),min(248,int(lum*1.12)))
            elif g>r*1.12 and g>b*1.12:color=(int(lum*.68),int(lum*.82),int(lum*.55))
            elif r>g*1.15 and g>b*1.06:color=(int(lum*1.13),int(lum*.92),int(lum*.63))
            elif max(r,g,b)-min(r,g,b)<32 and lum>220:color=(r,g,b)
            else:color=ramp[min(8,max(0,int(lum/28)-1))]
            result[q][i]=tuple(max(0,min(248,c))//8*8 for c in color)
    result[12]=material(theme)
    return result

def planes(reader,mid,theme,floor=False,wood=False,ladder=False,rim=False):
    result=[]
    for layer,native in enumerate(native_layers(reader,mid)):
        pixels=[]
        for i,(r,g,b,a) in enumerate(native.getdata()):
            if not a:pixels.append(0);continue
            if theme=='summit' and tuple(c>>3<<3 for c in (r,g,b))==(112,184,240):
                pixels.append(15);continue
            lum=(r+g+b)//3;x,y=i%16,i//16
            v=min(9,max(1,int(lum/26)))
            if rim:
                v=7 if y<2 else 5 if y<7 else 3 if y<12 else 1
                if (x,y) in ((3,2),(11,3),(7,9)):v=min(8,v+1)
            elif wood:
                v=11
                if y in (0,8):v=12
                if y in (7,15) or (x==(5 if y<8 else 13) and y not in (0,8)):v=10
                if (x,y) in ((2,3),(10,10)):v=12
            elif floor:
                # Natural bedrock with two sparse fractures and a salt chip.
                v=6 if lum<200 else 7
                if (y==4 and 2<=x<=5) or (y==12 and 10<=x<=13):v=5
                if (x,y) in ((3,5),(10,11)):v=8
                if theme in ('depth1','depth2','abyss') and (x,y)==(13,3):v=8
            elif not ladder and v>=4:
                # Mineral strata occupy existing rock pixels only; transparency
                # and the native wall/crag silhouette remain byte-identical.
                if y in (5,13) and x%7 not in (0,1):v=max(3,v-1)
                if (x,y)==(3,8):v=min(9,v+1)
            pixels.append(v)
        im=Image.new('L',(16,16));im.putdata(pixels);result.append(im)
    return result
