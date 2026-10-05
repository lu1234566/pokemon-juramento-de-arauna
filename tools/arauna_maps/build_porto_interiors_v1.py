#!/usr/bin/env python3
"""Restyle fourteen Porto do Sal rooms while retaining their event geometry."""
import json,struct,shutil,subprocess
from pathlib import Path
from PIL import Image
import render_porto_interiors_native as render
ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'review/porto_interiors_v1'
MARK='PORTO_INTERIORS_V1'
SPECS={
 'AraunaPortoCasas':('generic_building','arauna_porto_casas',547),
 'AraunaPortoEstaleiro':('facility','arauna_porto_estaleiro',514),
 'AraunaPortoMuseu':('oceanic_museum','arauna_porto_museu',513),
 'AraunaPortoClube':('pokemon_fan_club','arauna_porto_clube',513),
 'AraunaPortoPavilhao':('battle_tent','arauna_porto_pavilhao',520),
 'AraunaPortoCentro':('pokemon_center','arauna_porto_centro',514),
 'AraunaPortoVenda':('shop','arauna_porto_venda',513),
}
NAMES=tuple(p.parent.name for p in sorted((ROOT/'data/maps').glob('SlateportCity_*/map.json')))

GRAYS=render.INDEX_GRAYS
def words(path):return render.words(path)
def packed(values):return struct.pack('<%dH'%len(values),*values)
def dump(path,data):path.parent.mkdir(parents=True,exist_ok=True);path.write_text(json.dumps(data,indent=2,ensure_ascii=False)+'\n')
def layout_id(name):return 'LAYOUT_ARAUNA_PORTO_INTERIORS_'+name.removeprefix('SlateportCity_').upper()
def source(symbol):return ROOT/'data/tilesets/secondary'/SPECS[symbol][0]
def target(symbol):return ROOT/'data/tilesets/secondary'/SPECS[symbol][1]
def artwork():
    # Native indexed craft modules, derived from the timber/quay materials in
    # the supplied external concept. These rooms have no individual concept.
    floor=Image.new('L',(32,32))
    floor.putdata([4 if y%8==7 else (3 if x%16==(8 if (y//8)%2 else 0) else
                  (1 if (x*7+y*11)%43==0 else 2)) for y in range(32) for x in range(32)])
    wall=Image.new('L',(48,48))
    wall.putdata([6 if x in (0,1,46,47) else (5 if y in (14,15,30,31,46,47) else
                  (2 if y<30 else 4)) for y in range(48) for x in range(48)])
    table=Image.new('L',(32,32))
    table.putdata([1 if x in (0,31) or y in (0,31) else (4 if y%8==7 else
                  (2 if 4<=x<=27 and 4<=y<=27 else 3)) for y in range(32) for x in range(32)])
    chart=Image.new('L',(32,32))
    chart.putdata([1 if x<2 or x>29 or y<2 or y>29 else (3 if x<4 or x>27 or y<4 or y>27 else
                  (6 if (x+y)%13==0 or x==12 and 8<=y<=23 else (5 if 15<=x<=23 and 10<=y<=20 else 2)))
                  for y in range(32) for x in range(32)])
    crate=Image.new('L',(16,16))
    crate.putdata([1 if x in (0,15) or y in (0,15) else (3 if x==y or x==15-y or y%8==7 else 2)
                  for y in range(16) for x in range(16)])
    wood=[(255,0,255),(82,57,41),(156,107,65),(115,74,49),(131,90,57)]+[(65,49,32)]*11
    plaster=[(255,0,255),(239,230,204),(214,206,181),(184,168,139),(148,120,87),(112,84,60),(78,59,46)]+[(78,59,46)]*9
    furniture=[(255,0,255),(65,41,32),(197,156,98),(115,74,41),(139,98,57),(73,115,131),(57,90,115)]+[(90,65,41)]*9
    sea=[(255,0,255),(41,65,73),(65,98,115),(90,131,148),(123,156,172)]+[(49,74,90)]*11
    return {k:(v,6) for k,v in locals().copy().items() if isinstance(v,Image.Image)}, {6:wood,7:furniture,9:sea,12:plaster}

class Bank:
    def __init__(self,symbol,art,palettes):
        self.symbol=symbol;self.src=source(symbol);self.dst=target(symbol)
        self.dst.mkdir(exist_ok=True);shutil.copytree(self.src/'palettes',self.dst/'palettes',dirs_exist_ok=True)
        self.meta=words(self.src/'metatiles.bin');self.attrs=words(self.src/'metatile_attributes.bin')
        old=Image.open(self.src/'tiles.png');self.image=Image.new('P',(128,256));self.image.putpalette(old.getpalette());self.image.paste(old,(0,0))
        used={v&1023 for v in self.meta};self.pool=sorted(set(range(512,992))-used);self.cache={};self.allocated=[]
        self.art=art;self.palettes=palettes;self.floor=art['floor'][0]
        self.setpal(12,palettes[6]);self.setpal(13,palettes[12]);self.setpal(14,palettes[7]);self.setpal(15,palettes[9])
        # Recolor architectural palettes in aged timber and brass. Device
        # palettes 8/9/11, door IDs, primary water and animation stay intact.
        for slot in (6,7):
            lines=(self.dst/f'palettes/{slot:02}.pal').read_text().splitlines();colors=[]
            for index,line in enumerate(lines[3:19]):
                rgb=tuple(map(int,line.split()));lum=sum(a*b for a,b in zip(rgb,(.299,.587,.114)))
                colors.append(rgb if index==0 else tuple(min(255,round(v)) for v in (lum*.90+12,lum*.75+12,lum*.54+17)))
            self.setpal(slot,colors)
        # Replace the reusable floor quadrants wherever the old bank references them.
        mid=SPECS[symbol][2];entries=self.meta[(mid-512)*8:(mid-512)*8+4]
        floor_palettes={v>>12 for v in entries}
        replacement={}
        for i,entry in enumerate(entries):
            oldid=entry&1023
            if oldid not in replacement:
                x=(i%2)*8;y=(i//2)*8
                replacement[oldid]=self.tile(self.floor.crop((x,y,x+8,y+8)))|(12<<12)
        self.meta=[replacement[v&1023] | (v&0xc00) if v&1023 in replacement and v>>12 in floor_palettes else v for v in self.meta]
        # Reuse the plank quadrants beneath the museum displays; the original
        # alternate floor variants otherwise leave isolated turquoise patches.
        if symbol=='AraunaPortoMuseu':
            for mid in (514,515,579,580,581,582,583,587,589,590,591,594):
                entries=self.meta[(mid-512)*8:(mid-512)*8+4]
                replacement={entry&1023:self.floorq()[i] for i,entry in enumerate(entries)}
                self.meta=[replacement[v&1023]|(v&0xc00) if v&1023 in replacement and v>>12 in {7,8,11} else v for v in self.meta]
        self.redraw()
    def setpal(self,slot,colors):
        assert len(colors)==16
        (self.dst/f'palettes/{slot:02}.pal').write_text('JASC-PAL\n0100\n16\n'+'\n'.join(' '.join(map(str,rgb)) for rgb in colors)+'\n')
    def tile(self,image):
        key=image.tobytes()
        if key not in self.cache:
            assert self.pool,(self.symbol,'tile budget')
            mid=self.pool.pop(0);self.cache[key]=mid;self.allocated.append(mid)
            self.image.paste(image,((mid-512)%16*8,(mid-512)//16*8))
            for transform,flags in ((Image.Transpose.FLIP_LEFT_RIGHT,0x400),(Image.Transpose.FLIP_TOP_BOTTOM,0x800),(Image.Transpose.ROTATE_180,0xc00)):
                self.cache.setdefault(image.transpose(transform).tobytes(),mid|flags)
        return self.cache[key]
    def q(self,image,palette):
        return [self.tile(image.crop((x,y,x+8,y+8)))|(palette<<12) for x,y in ((0,0),(8,0),(0,8),(8,8))]
    def floorq(self):return self.q(self.floor.crop((0,0,16,16)),12)
    def piece(self,mid,image,palette):
        self.meta[(mid-512)*8:(mid-511)*8]=self.floorq()+self.q(image,palette)
    def module(self,name,ids,size,palette=14):
        image=self.art[name][0].resize(size,Image.Resampling.NEAREST)
        for row,items in enumerate(ids):
            for col,mid in enumerate(items):self.piece(mid,image.crop((col*16,row*16,col*16+16,row*16+16)),palette)
    def wall(self,ids):
        for i,mid in enumerate(ids):
            image=self.art['wall'][0].crop(((i%3)*16,0,(i%3+1)*16,16))
            self.piece(mid,image,13)
    def redraw(self):
        if self.symbol=='AraunaPortoCasas':
            self.wall((517,525))
            for ids in (((586,587),(594,595)),((588,589),(596,597))):self.module('table',ids,(32,32))
            for mid in (574,891,892,893,899,901,907,908,909):
                rug=Image.new('L',(16,16));rug.putdata([3 if (x+y)%7==0 else 2 for y in range(16) for x in range(16)])
                self.piece(mid,rug,15)
        elif self.symbol=='AraunaPortoEstaleiro':
            self.wall((537,545,946))
            self.module('chart',((524,525),(532,533)),(32,32))
            for ids in (((576,578),(584,586)),((577,578),(585,586))):self.module('table',ids,(32,32))
            # Raised working deck and dock rail. Retain their original behavior.
            for mid in (552,553,554,550):self.piece(mid,self.floor.crop((0,0,16,16)),12)
            rail=Image.new('L',(16,16));rail.putdata([1 if y in (3,4,10,11) else (2 if x in (2,3,12,13) else 0) for y in range(16) for x in range(16)])
            for mid in (846,854,593,617):self.piece(mid,rail,14)
            # A timber launch on workshop supports replaces the steel boiler.
            hull=Image.new('L',(64,80));pixels=[]
            for y in range(80):
                for x in range(64):
                    inset=max(0,12-y//2) if y<24 else (max(0,(y-55)//2) if y>55 else 0)
                    pixels.append(0 if x<inset or x>=64-inset else
                                  (1 if x in (inset,63-inset) or y in (0,1,78,79) else
                                   (3 if y%16 in (0,1) or x in (8,9,54,55) else (4 if y%8==7 else 2))))
            hull.putdata(pixels)
            ids=((720,721,722,723),(563,564,565,566),(571,572,573,574),(579,580,581,582),(587,588,589,590))
            for y,row in enumerate(ids):
                for x,mid in enumerate(row):self.piece(mid,hull.crop((x*16,y*16,x*16+16,y*16+16)),12)
            for mid in (603,604,611,612,619,620):self.piece(mid,self.art['crate'][0],14)
        elif self.symbol=='AraunaPortoMuseu':
            self.wall((516,524))
            for ids in (((528,529),(536,537)),((534,535),(542,543))):self.module('chart',ids,(32,32))
            # Freestanding chart panels use a continuous timber frame.
            self.module('chart',((556,557),(564,565)),(32,32))
        elif self.symbol=='AraunaPortoClube':
            self.wall((529,541))
            for mid in (*range(552,555),*range(560,565),*range(567,578)):
                rug=Image.new('L',(16,16));rug.putdata([3 if (x+y)%7==0 else 2 for y in range(16) for x in range(16)])
                self.piece(mid,rug,15)
            self.module('table',((604,605,606),(608,609,610)),(48,32))
        elif self.symbol=='AraunaPortoPavilhao':
            self.wall((517,525))
            for mid in (520,521,528,529,538,539,540,547,548,552,554,555):self.piece(mid,self.floor.crop((0,0,16,16)),12)
            # Existing arena/court and counter silhouettes keep collision and
            # event timing, receiving local wood and woven sea-blue surfaces.
            for mid in range(688,726):
                weave=Image.new('L',(16,16));weave.putdata([3 if (x+y)%5==0 else 2 for y in range(16) for x in range(16)])
                self.piece(mid,weave,15)
            for mid in (*range(736,774),778,779,780):
                if mid-512>=len(self.attrs):continue
                weave=Image.new('L',(16,16));weave.putdata([3 if (x+y)%5==0 else 2 for y in range(16) for x in range(16)])
                self.piece(mid,weave,15)
        elif self.symbol=='AraunaPortoCentro':self.wall((523,531))
        else:self.wall((531,539))
    def save(self):
        self.image.save(self.dst/'tiles.png',bits=4)
        (self.dst/'metatiles.bin').write_bytes(packed(self.meta));(self.dst/'metatile_attributes.bin').write_bytes(packed(self.attrs))
        old=words(self.src/'metatiles.bin')
        return {'allocated_tiles':self.allocated,'changed_metatiles':[512+i for i in range(len(self.attrs)) if old[i*8:(i+1)*8]!=self.meta[i*8:(i+1)*8]]}

def main():
    import re
    art,palettes=artwork();banks={symbol:Bank(symbol,art,palettes) for symbol in SPECS}
    node=json.loads((ROOT/'data/layouts/layouts.json').read_text());report={}
    original_symbols={'gTileset_GenericBuilding':'AraunaPortoCasas','gTileset_Facility':'AraunaPortoEstaleiro','gTileset_OceanicMuseum':'AraunaPortoMuseu','gTileset_PokemonFanClub':'AraunaPortoClube','gTileset_BattleTent':'AraunaPortoPavilhao','gTileset_PokemonCenter':'AraunaPortoCentro','gTileset_Shop':'AraunaPortoVenda'}
    for name in NAMES:
        p=ROOT/'data/maps'/name/'map.json';original=json.loads(subprocess.check_output(['git','show','HEAD:data/maps/'+name+'/map.json'],cwd=ROOT))
        template=next(r for r in node['layouts'] if r['id']==original['layout']);symbol=original_symbols[template['secondary_tileset']]
        dest=ROOT/'data/layouts'/(name+'_Arauna');dest.mkdir(exist_ok=True)
        for new,old in (('map.bin','blockdata_filepath'),('border.bin','border_filepath')):shutil.copyfile(ROOT/template[old],dest/new)
        record=dict(template,id=layout_id(name),name=name+'_Arauna_Layout',secondary_tileset='gTileset_'+symbol,
                    blockdata_filepath=str((dest/'map.bin').relative_to(ROOT)),border_filepath=str((dest/'border.bin').relative_to(ROOT)))
        found=next((r for r in node['layouts'] if r['id']==record['id']),None)
        if found:found.update(record)
        else:node['layouts'].append(record)
        event={**original,'layout':record['id']};dump(p,event)
        report[name]={'size':[record['width'],record['height']],'warps':len(event['warp_events']),'objects':len(event['object_events'])}
    dump(ROOT/'data/layouts/layouts.json',node)
    graphics=metatiles=headers=''
    for symbol in SPECS:
        slug=SPECS[symbol][1];prefix='data/tilesets/secondary/'+slug
        graphics+=f'const u32 gTilesetTiles_{symbol}[] = INCGFX_U32("{prefix}/tiles.png", ".4bpp.lz");\nconst u16 gTilesetPalettes_{symbol}[][16] =\n{{\n'+''.join(f'    INCGFX_U16("{prefix}/palettes/{i:02}.pal", ".gbapal"),\n' for i in range(16))+'};\n\n'
        metatiles+=f'const u16 gMetatiles_{symbol}[] = INCBIN_U16("{prefix}/metatiles.bin");\nconst u16 gMetatileAttributes_{symbol}[] = INCBIN_U16("{prefix}/metatile_attributes.bin");\n\n'
        headers+=f'const struct Tileset gTileset_{symbol} =\n{{\n    .isCompressed = TRUE,\n    .isSecondary = TRUE,\n    .tiles = gTilesetTiles_{symbol},\n    .palettes = gTilesetPalettes_{symbol},\n    .metatiles = gMetatiles_{symbol},\n    .metatileAttributes = gMetatileAttributes_{symbol},\n    .callback = NULL,\n}};\n\n'
    for filename,body in (('graphics.h',graphics),('metatiles.h',metatiles),('headers.h',headers)):
        p=ROOT/'src/data/tilesets'/filename;clean=re.sub(r'\n*// '+MARK+r'_BEGIN\n.*?// '+MARK+r'_END\n','',p.read_text(),flags=re.S)
        p.write_text(clean.rstrip()+'\n\n// '+MARK+'_BEGIN\n'+body+'// '+MARK+'_END\n')
    reports={symbol:bank.save() for symbol,bank in banks.items()}
    dump(OUT/'geometry.json',{'maps':report,'banks':reports})
    print(json.dumps({'maps':len(NAMES),'warps':sum(r['warps'] for r in report.values()),'objects':sum(r['objects'] for r in report.values()),'allocated_tiles':{s:len(r['allocated_tiles']) for s,r in reports.items()}}))

if __name__=='__main__':main()
