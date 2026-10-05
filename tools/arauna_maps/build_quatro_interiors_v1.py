#!/usr/bin/env python3
"""Restyle fourteen Quatro do Sal rooms while retaining their event geometry."""
import json,struct,shutil,subprocess
from pathlib import Path
from PIL import Image
import render_quatro_interiors_native as render
ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'review/quatro_interiors_v1'
MARK='QUATRO_INTERIORS_V1'
CITIES={'FallarborTown':('Campo','Campo das Cinzas',8),'LavaridgeTown':('Cinza','Casa da Cinza',7),
        'FortreeCity':('Mata','Mata do Meio',10),'LilycoveCity':('Baia','Baía das Luzes',23)}
BANKS={
 'Campo':{'generic_building':547,'battle_tent':520,'shop':513,'pokemon_center':514},
 'Cinza':{'generic_building':553,'lavaridge_gym':520,'shop':513,'pokemon_center':514},
 'Mata':{'generic_building':985,'fortree_gym':514,'shop':513,'pokemon_center':514},
 'Baia':{'generic_building':547,'shop':513,'pokemon_center':514,'facility':514,
         'contest':608,'lilycove_museum':514,'battle_frontier':605},
}
SPECS={'Arauna'+city+''.join(p.title() for p in slug.split('_')):(slug,'arauna_'+city.lower()+'_'+slug,mid)
       for city,config in BANKS.items() for slug,mid in config.items()}
NAMES=tuple(p.parent.name for prefix in CITIES for p in sorted((ROOT/'data/maps').glob(prefix+'_*/map.json')))
def cityof(symbol):return next(c for c in BANKS if symbol.startswith('Arauna'+c))
EXTRA_FLOORS={'generic_building':(547,553,545),'shop':(513,616,754,756,762,749),
              'lilycove_museum':(514,515,616,617),'contest':(608,625,626),
              'fortree_gym':(513,514,515),'battle_tent':(520,521,528,529,538,539,540,547,548,552,554,555),
              'lavaridge_gym':(513,514,519,520,521,522),'battle_frontier':(605,613)}
WALL_IDS={'generic_building':(517,525),'shop':(531,539),'pokemon_center':(523,531),
          'lavaridge_gym':(515,516,517,518,523,524,525,527,532,534,552,553,554,555,556,557,558,559,560,561,562,564,565),'fortree_gym':(524,527),'facility':(537,545,946),
          'lilycove_museum':(523,531),'contest':(545,553)}

GRAYS=render.INDEX_GRAYS
def words(path):return render.words(path)
def packed(values):return struct.pack('<%dH'%len(values),*values)
def dump(path,data):path.parent.mkdir(parents=True,exist_ok=True);path.write_text(json.dumps(data,indent=2,ensure_ascii=False)+'\n')
def layout_id(name):return 'LAYOUT_ARAUNA_QUATRO_INTERIORS_'+name.upper()
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
        for path in (self.dst/'palettes').glob('*.pal'):path.write_text(path.read_text())
        self.meta=words(self.src/'metatiles.bin');self.attrs=words(self.src/'metatile_attributes.bin')
        old=Image.open(self.src/'tiles.png');self.image=Image.new('P',(128,256));self.image.putpalette(old.getpalette());self.image.paste(old,(0,0))
        used={v&1023 for v in self.meta};self.pool=sorted(set(range(512,992))-used-(set(range(512,512+old.width*old.height//64)) if SPECS[symbol][0] in ('lilycove_museum','contest','battle_frontier') else set()));self.cache={};self.allocated=[]
        self.art=art;self.palettes=palettes;self.floor=art['floor'][0].copy()
        city=cityof(symbol);slug=SPECS[symbol][0]
        if slug not in ('generic_building','facility'):
            self.floor.putdata([4 if y%16==15 or x%16==(8 if (y//16)%2 else 0) else (1 if (x*7+y*11)%71==0 else 2) for y in range(32) for x in range(32)])
        self.setpal(12,palettes[6]);self.setpal(13,palettes[12]);self.setpal(14,palettes[7]);self.setpal(15,palettes[9])
        floors={
          'Campo':[(255,0,255),(213,213,189),(172,181,156),(139,148,131),(106,123,106)]+[(82,98,90)]*11,
          'Cinza':[(255,0,255),(123,115,106),(90,90,90),(65,74,82),(49,57,65)]+[(41,49,57)]*11,
          'Mata':[(255,0,255),(172,139,82),(123,98,57),(90,74,49),(65,57,41)]+[(49,49,32)]*11,
          'Baia':[(255,0,255),(230,230,213),(197,213,213),(164,189,197),(131,156,172)]+[(106,131,148)]*11,
        }
        fabrics={
          'Campo':[(255,0,255),(49,65,41),(90,115,65),(123,139,81)]+[(65,81,49)]*12,
          'Cinza':[(255,0,255),(98,49,41),(148,74,49),(189,106,65)]+[(115,57,41)]*12,
          'Mata':[(255,0,255),(41,57,41),(57,90,57),(90,123,65)]+[(49,74,49)]*12,
          'Baia':palettes[9],
        }
        self.setpal(12,floors[city]);self.setpal(15,fabrics[city])
        if city=='Mata':self.setpal(13,[(255,0,255),(189,172,131),(148,131,98),(115,106,74),(82,74,49),(65,57,41),(41,41,32)]+[(41,41,32)]*9)
        # Painting and dynamic screen palettes remain original. Service device
        # palettes 8/9/11 and primary palettes are always preserved.
        if slug not in ('lilycove_museum','battle_frontier','lavaridge_gym','fortree_gym'):
            for slot in (6,7):
                lines=(self.dst/f'palettes/{slot:02}.pal').read_text().splitlines();colors=[]
                for index,line in enumerate(lines[3:19]):
                    rgb=tuple(map(int,line.split()));lum=sum(a*b for a,b in zip(rgb,(.299,.587,.114)))
                    if index==0:colors.append(rgb);continue
                    tint=(lum*.91+12,lum*.77+12,lum*.55+17) if city in ('Cinza','Campo') else ((lum*.69+12,lum*.77+15,lum*.51+17) if city=='Mata' else (lum*.82+15,lum*.85+19,lum*.90+20))
                    colors.append(tuple(min(255,round(v)) for v in tint))
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
        # Apply the city material to alternate floor variants and underlying
        # furniture tiles using each variant's own palette, never new glyphs.
        original=words(self.src/'metatiles.bin')
        for mid in EXTRA_FLOORS.get(slug,()):
            if mid-512>=len(self.attrs):continue
            entries=original[(mid-512)*8:(mid-512)*8+4];slots={v>>12 for v in entries}-{0}
            replacement={entry&1023:self.floorq()[i] for i,entry in enumerate(entries) if entry>>12 in slots}
            self.meta=[replacement[v&1023]|(v&0xc00) if v&1023 in replacement and v>>12 in slots else v for v in self.meta]
        self.redraw()
        # Script-enabled museum exhibits and hall flaps retain exact metadata.
        protected=range(0x25a,0x264) if slug=='lilycove_museum' else ((0x2d1,0x2d9) if slug=='contest' else ())
        for mid in protected:self.meta[(mid-512)*8:(mid-511)*8]=original[(mid-512)*8:(mid-511)*8]
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
        slug=SPECS[self.symbol][0];city=cityof(self.symbol)
        wallids=WALL_IDS.get(slug,())
        if slug=='generic_building' and city=='Mata':wallids=(969,977)
        self.wall(wallids)
        if slug=='generic_building':
            if city=='Mata':
                # Own timber side panels and corner silhouettes instead of
                # Emerald's orange trapezoid walls around the central trunk.
                for mid in (968,970,976,978):
                    pane=Image.new('L',(16,16));pane.putdata([0 if mid==968 and y<15-x or mid==970 and y<x else (5 if y%8==7 or x in (0,15) else 4) for y in range(16) for x in range(16)])
                    self.meta[(mid-512)*8:(mid-511)*8]=[0]*4+self.q(pane,13)
                for mid in (984,986):
                    pane=Image.new('L',(16,16));pane.putdata([5 if y%8==7 else 4 if (x+y<16 if mid==984 else x>=y) else 0 for y in range(16) for x in range(16)])
                    self.piece(mid,pane,13)
                trunk=Image.new('L',(16,16));trunk.putdata([1 if x in (0,15) else (3 if x%5==0 else 2) for y in range(16) for x in range(16)])
                for mid in (958,959):self.piece(mid,trunk,14)
            else:self.wall((533,541))
            for ids in (((586,587),(594,595)),((588,589),(596,597))):self.module('table',ids,(32,32))
            for mid in (566,574,582,590,792,793,794,795):
                rug=Image.new('L',(16,16));rug.putdata([3 if (x+y)%7==0 else 2 for y in range(16) for x in range(16)])
                self.piece(mid,rug,15)
        elif slug=='battle_tent':
            self.wall((517,525))
            for mid in (*range(688,726),*range(736,774),778,779,780):
                if mid-512>=len(self.attrs):continue
                weave=Image.new('L',(16,16));weave.putdata([3 if (x+y)%5==0 else 2 for y in range(16) for x in range(16)])
                self.piece(mid,weave,15)
        elif slug=='facility':
            rail=Image.new('L',(16,16));rail.putdata([1 if y in (3,4,10,11) else (2 if x in (2,3,12,13) else 0) for y in range(16) for x in range(16)])
            for mid in (846,854,593,617):self.piece(mid,rail,14)
            for mid in (552,553,554,550):self.piece(mid,self.floor.crop((0,0,16,16)),12)
        elif slug=='contest':
            # Native woven stage deck; keep stair variants and stage markers.
            for mid in (625,626):
                weave=Image.new('L',(16,16));weave.putdata([3 if (x+y)%5==0 else 2 for y in range(16) for x in range(16)])
                self.piece(mid,weave,15)
    def save(self):
        self.image.save(self.dst/'tiles.png',bits=4)
        (self.dst/'metatiles.bin').write_bytes(packed(self.meta));(self.dst/'metatile_attributes.bin').write_bytes(packed(self.attrs))
        old=words(self.src/'metatiles.bin')
        return {'allocated_tiles':self.allocated,'changed_metatiles':[512+i for i in range(len(self.attrs)) if old[i*8:(i+1)*8]!=self.meta[i*8:(i+1)*8]]}

def main():
    import re
    art,palettes=artwork();banks={symbol:Bank(symbol,art,palettes) for symbol in SPECS}
    node=json.loads((ROOT/'data/layouts/layouts.json').read_text());report={}

    for name in NAMES:
        p=ROOT/'data/maps'/name/'map.json';original=json.loads(subprocess.check_output(['git','show','HEAD:data/maps/'+name+'/map.json'],cwd=ROOT))
        template=next(r for r in node['layouts'] if r['id']==original['layout'])
        city=CITIES[next(prefix for prefix in CITIES if name.startswith(prefix+'_'))][0]
        symbol='Arauna'+city+template['secondary_tileset'].removeprefix('gTileset_')
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
