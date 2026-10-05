#!/usr/bin/env python3
"""Restyle sixteen Serra do Uivo rooms while retaining their event geometry."""
import json,struct,shutil,subprocess
from pathlib import Path
from PIL import Image
import render_serra_interiors_native as render
ROOT=Path(__file__).resolve().parents[2]
ATLAS=ROOT/'art/arauna_serra_interiors_v1/source_atlas.png'
OUT=ROOT/'review/serra_interiors_v1'
MARK='SERRA_INTERIORS_V1'
SPECS={
 'AraunaSerraCasas':('generic_building','arauna_serra_casas',812),
 'AraunaSerraTecnica':('facility','arauna_serra_tecnica',896),
 'AraunaSerraEscola':('pokemon_school','arauna_serra_escola',513),
 'AraunaSerraCentro':('pokemon_center','arauna_serra_centro',514),
 'AraunaSerraVenda':('shop','arauna_serra_venda',513),
}
NAMES=tuple(p.parent.name for p in sorted((ROOT/'data/maps').glob('RustboroCity_*/map.json')) if p.parent.name!='RustboroCity_Gym')
GRAYS=render.INDEX_GRAYS
def words(path):return render.words(path)
def packed(values):return struct.pack('<%dH'%len(values),*values)
def dump(path,data):path.parent.mkdir(parents=True,exist_ok=True);path.write_text(json.dumps(data,indent=2,ensure_ascii=False)+'\n')
def layout_id(name):return 'LAYOUT_ARAUNA_SERRA_INTERIORS_'+name.removeprefix('RustboroCity_').upper()
def source(symbol):return ROOT/'data/tilesets/secondary'/SPECS[symbol][0]
def target(symbol):return ROOT/'data/tilesets/secondary'/SPECS[symbol][1]
def artwork():
    src = Image.open(ATLAS).convert('RGB')
    assert src.width >= 1200 and src.height >= 1200
    configs = [
        ('floor', (32,32),6), ('wall',(48,48),6), ('window',(48,48),11), ('door',(48,48),6),
        ('hearth',(48,48),8), ('table',(48,48),7), ('rug',(48,32),7), ('lantern',(16,32),8),
        ('shelf',(32,32),7), ('bed',(32,32),7), ('chart',(32,32),7), ('stair',(32,32),6),
        ('healer',(64,48),9), ('pc',(32,32),9), ('link',(48,32),9), ('plant',(32,32),10),
    ]
    raw = {}
    for i,(name,size,palette) in enumerate(configs):
        row,col=divmod(i,4)
        x0=round(col*src.width/4)+23; x1=round((col+1)*src.width/4)-22
        y0=round(row*src.height/4)+21; y1=round((row+1)*src.height/4)-20
        part=src.crop((x0,y0,x1,y1)).convert('RGBA')
        part.putdata([(r,g,b,0 if r>160 and b>160 and g<130 else 255) for r,g,b,a in part.getdata()])
        if name != 'floor': part=part.crop(part.getbbox())
        part=part.resize(size,Image.Resampling.NEAREST)
        raw[name]=(part,palette)
    palette_colors={}
    for slot in range(6,13):
        colors=[(r,g,b) for image,s in raw.values() if s==slot for r,g,b,a in image.getdata() if a]
        if not colors: continue
        sample=Image.new('RGB',(len(colors),1));sample.putdata(colors)
        q=sample.quantize(colors=15,method=Image.Quantize.MEDIANCUT).getpalette()[:45]
        palette_colors[slot]=[(255,0,255)]+[tuple(round(c*31/255)*255//31 for c in q[j:j+3]) for j in range(0,45,3)]
    output={}
    dest=ROOT/'art/arauna_serra_interiors_v1/native_assets';dest.mkdir(parents=True,exist_ok=True)
    for name,(im,slot) in raw.items():
        palette=palette_colors[slot]
        indices=[0 if not a else min(range(1,16),key=lambda j:sum((v-w)**2 for v,w in zip((r,g,b),palette[j]))) for r,g,b,a in im.getdata()]
        tile=Image.new('L',im.size);tile.putdata(indices);output[name]=(tile,slot)
        preview=Image.new('RGBA',im.size);preview.putdata([(*palette[index],255 if index else 0) for index in indices]);preview.save(dest/(name+'.png'))
    # Native indexed timber: shallow seams, no transparent gutters.
    floor=Image.new('L',(32,32))
    floor.putdata([4 if y%8==7 else (3 if x%16==(8 if (y//8)%2 else 0) else
                   (1 if (x*7+y*11)%37==0 else 2)) for y in range(32) for x in range(32)])
    output['floor']=(floor,6)
    # Cream plaster over a timber dado; columns repeat at module boundaries.
    wall=Image.new('L',(48,48))
    wall.putdata([6 if x in (0,1,46,47) else
                  (5 if y in (30,31,46,47) else
                   (2 if y<30 else 4))
                  for y in range(48) for x in range(48)])
    output['wall']=(wall,12)
    palette_colors[12]=[(255,0,255),(239,230,204),(214,206,181),(184,168,139),
                       (148,120,87),(112,84,60),(78,59,46)]+[(78,59,46)]*9
    return output,palette_colors

class Bank:
    def __init__(self,symbol,art,palettes):
        self.symbol=symbol;self.src=source(symbol);self.dst=target(symbol)
        self.dst.mkdir(exist_ok=True);shutil.copytree(self.src/'palettes',self.dst/'palettes',dirs_exist_ok=True)
        self.meta=words(self.src/'metatiles.bin');self.attrs=words(self.src/'metatile_attributes.bin')
        old=Image.open(self.src/'tiles.png');self.image=Image.new('P',(128,256));self.image.putpalette(old.getpalette());self.image.paste(old,(0,0))
        used={v&1023 for v in self.meta};self.pool=sorted(set(range(512,992))-used);self.cache={};self.allocated=[]
        self.art=art;self.palettes=palettes;self.floor=art['floor'][0]
        self.setpal(12,palettes[6]);self.setpal(13,palettes[12]);self.setpal(14,palettes[7]);self.setpal(15,palettes[9] if symbol=='AraunaSerraTecnica' else [(255,0,255),(57,81,65),(82,112,81),(112,142,98)]+[(41,65,57)]*12)
        if symbol=='AraunaSerraTecnica':
            self.setpal(12,[(255,0,255),(197,207,207),(157,174,181),(133,150,158),(106,123,139)]+[(73,90,106)]*11)
            self.setpal(13,[(255,0,255),(230,230,222),(207,215,215),(181,197,197),(148,164,172),(115,131,148),(90,106,123)]+[(90,106,123)]*9)
        # Warm housing vs. cool archive; preserve contrast and existing indices.
        for slot in (6,7):
            if symbol=='AraunaSerraEscola':continue
            lines=(self.dst/f'palettes/{slot:02}.pal').read_text().splitlines();colors=[]
            for index,line in enumerate(lines[3:19]):
                rgb=tuple(map(int,line.split()));lum=sum(a*b for a,b in zip(rgb,(.299,.587,.114)))
                if index==0:colors.append(rgb);continue
                if symbol=='AraunaSerraTecnica':colors.append(tuple(min(255,round(v)) for v in (lum*.76+20,lum*.80+24,lum*.85+25)))
                else:colors.append(tuple(min(255,round(v)) for v in (lum*.91+12,lum*.78+15,lum*.61+17)))
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
        if self.symbol=='AraunaSerraCasas':
            self.wall((824,832))
            self.module('table',((874,875),(882,883)),(32,32))
            self.module('table',((584,585),(592,593)),(32,32))
            self.module('table',((872,873),(880,881)),(32,32))
            self.piece(606,self.art['table'][0].resize((32,32),Image.Resampling.NEAREST).crop((16,0,32,16)),14)
            self.module('shelf',((878,879),(886,887)),(32,32))
            for mid in (574,891,892,893,899,901,907,908,909):
                image=Image.new('L',(16,16));image.putdata([3 if (x+y)%7==0 else 2 for y in range(16) for x in range(16)])
                self.piece(mid,image,15)
        elif self.symbol=='AraunaSerraTecnica':
            self.wall((904,905))
            self.module('pc',((931,932),(939,940)),(32,32),15)
            for mid in (952,953,954,960,961,962,955,956,957,963,964,965,958,966,959):
                image=Image.new('L',(16,16))
                left=mid in (952,960,955,963,958);right=mid in (954,962,957,965,959)
                top=mid in (952,953,954);bottom=mid in (963,964,965);legs=mid in (958,966,959)
                image.putdata([((9 if x in (2,3,12,13) and y<8 else 0) if legs else
                                (11 if left and x<2 or right and x>13 else
                                 (3 if top and y<2 or bottom and y>13 else
                                  (1 if mid==956 and 4<=x<=11 and 4<=y<=9 else 5))))
                               for y in range(16) for x in range(16)])
                self.piece(mid,image,14)
        elif self.symbol=='AraunaSerraEscola':
            self.wall((520,521))
            self.module('table',((540,541),(548,549)),(32,32))
            self.setpal(15,[(255,0,255),(73,49,32),(139,90,49),(180,131,73),(213,172,115),(230,221,189),(73,115,81)]+[(49,41,32)]*9)
            desk=Image.new('L',(16,32))
            desk.putdata([((5 if 3<=x<=9 and 3<=y<=8 else (3 if y<12 else (1 if x in (2,13) else 0))) if y<16 else
                           (3 if 3<=x<=12 and (16<=y<=19 or 22<=y<=24) else (1 if x in (4,11) and y>=25 else 0)))
                          for y in range(32) for x in range(16)])
            for top,bottom in ((524,532),(525,533),(526,534)):
                self.piece(top,desk.crop((0,0,16,16)),15)
                self.piece(bottom,desk.crop((0,16,16,32)),15)
        elif self.symbol=='AraunaSerraCentro':self.wall((523,531))
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
    original_symbols={'gTileset_GenericBuilding':'AraunaSerraCasas','gTileset_Facility':'AraunaSerraTecnica','gTileset_PokemonSchool':'AraunaSerraEscola','gTileset_PokemonCenter':'AraunaSerraCentro','gTileset_Shop':'AraunaSerraVenda'}
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
