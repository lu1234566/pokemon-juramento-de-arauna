#!/usr/bin/env python3
"""Deterministic atlas-to-native conversion for 13 cave maps; events untouched."""
import collections,json,re,struct,subprocess
from pathlib import Path
from PIL import Image,ImageDraw,ImageChops
from render_native_map import words,Renderer
from bancos_nativos import resolve_bank
ROOT=Path(__file__).resolve().parents[2];BASE='4439f996326bbe457d8a9eacbf2ae4341befa88b';MARK='CAMPANHA_GRUTAS_V1';OUT=ROOT/'review/campanha_grutas_v1';ART=ROOT/'art/campanha_grutas_v1'
PARTS=('floor','mass','left','right','top','bottom','ledge_south','ledge_west','ledge_east','upstairs','downstairs','entry','pillar','mineral','altar','water');WATER={16,17,18,20,21,25,26,80,81,82,83};FLOORS={0,8,11,12,33};WATER_TILE=424;FALL_TILE=428

def gitbytes(rel):return subprocess.check_output(['git','show',BASE+':'+rel],cwd=ROOT)
def dump(p,d):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
def binary(p,v):p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(struct.pack('<%dH'%len(v),*v))
def block(p,body):
 text=p.read_text();s='\n\n// '+MARK+'_BEGIN\n'+body+'// '+MARK+'_END\n';pattern=r'\n*// '+MARK+r'_BEGIN\n.*?// '+MARK+r'_END\n';p.write_text(re.sub(pattern,lambda _:s,text,flags=re.S) if '// '+MARK+'_BEGIN' in text else text.rstrip()+s)
def symbol(slug):return ''.join(p.capitalize() for p in slug.split('_'))
def extract(family):
 atlas=Image.open(ART/(family+'_atlas.png')).convert('RGBA');raw={}
 for i,name in enumerate(PARTS):
  y,x=divmod(i,4);im=atlas.crop((round(x*atlas.width/4)+8,round(y*atlas.height/4)+8,round((x+1)*atlas.width/4)-8,round((y+1)*atlas.height/4)-8));im.putdata([(r,g,b,0 if r>140 and b>140 and g<140 else 255) for r,g,b,a in im.getdata()]);assert im.getbbox();raw[name]=im.crop(im.getbbox()).resize((16,16),Image.Resampling.NEAREST)
 groups={0:['floor'],1:list(PARTS[1:9]),2:['water'],3:list(PARTS[9:12]),4:list(PARTS[12:15])};pals={};indexed={}
 for slot,names in groups.items():
  colors=[(r,g,b) for name in names for r,g,b,a in raw[name].getdata() if a];sample=Image.new('RGB',(len(colors),1));sample.putdata(colors);p=sample.quantize(colors=15,method=Image.Quantize.MEDIANCUT).getpalette()[:45];pals[slot]=[(0,0,0)]+[tuple((c>>3)<<3 for c in p[j:j+3]) for j in range(0,45,3)]
  for name in names:
   im=raw[name];opaque=name in ('floor','water');common=collections.Counter((r,g,b) for r,g,b,a in im.getdata() if a).most_common(1)[0][0];samples=[(r,g,b) if a else common for r,g,b,a in im.getdata()];lookup={c:min(range(1,16),key=lambda j:sum((u-v)**2 for u,v in zip(c,pals[slot][j]))) for c in set(samples)};idx=Image.new('L',(16,16));idx.putdata([lookup[c] if a or opaque else 0 for c,(_,_,_,a) in zip(samples,im.getdata())]);indexed[name]=(idx,slot)
 pals[5]=[(0,0,0),(8,16,24),(40,48,56),(80,96,96),(120,144,128),(176,184,144),(224,216,168),(248,240,200),(8,40,48),(24,72,80),(56,112,120),(96,152,160),(160,200,208),(200,224,224),(48,24,24),(112,64,48)];return indexed,pals
class Bank:
 def __init__(self,family,kind,source,uses,art,pals,scriptids):
  self.family,self.kind,self.source,self.uses,self.art,self.pals,self.scriptids=family,kind,source,uses,art,pals,scriptids;self.slug='arauna_grutas_'+family+('_correntes' if source.name=='pacifidlog' else '_base' if kind=='primary' else '_rocha')+'_v1';self.dst=ROOT/'data/tilesets'/kind/self.slug;self.symbol=symbol(self.slug);self.offset=0 if kind=='primary' else 512;self.attrs=words(source/'metatile_attributes.bin');self.entries=[0]*(len(self.attrs)*8);self.tiles=[bytes(64)];self.cache={bytes(64):self.offset};self.aliases={};self.roles={};self.required=set(uses)|scriptids
  prefix='General' if kind=='primary' else 'Pacifidlog' if source.name=='pacifidlog' else 'Cave';labels=re.findall(r'#define METATILE_'+prefix+r'_\w+\s+(0x[0-9a-fA-F]+)',(ROOT/'include/constants/metatile_labels.h').read_text());self.required.update(int(v,16) for v in labels if self.offset<=int(v,16)<self.offset+len(self.attrs));occupied=set(self.required)
  for mid,states in sorted(uses.items()):
   if len(states)>1 and self.attrs[mid-self.offset]&255 in FLOORS:
    attr=self.attrs[mid-self.offset];free=next((j+self.offset for j,a in enumerate(self.attrs) if a==attr and j+self.offset not in occupied),None)
    if free is None:assert len(self.attrs)<512;free=self.offset+len(self.attrs);self.attrs.append(attr);self.entries.extend([0]*8)
    self.aliases[mid]=free;occupied.add(free);self.required.add(free);self.roles[free]='solid'
  for mid in sorted(self.required):
   assert self.offset<=mid<self.offset+len(self.attrs);self.roles.setdefault(mid,self.role(self.attrs[mid-self.offset]&255,uses.get(mid,{False})))
 def role(self,b,states):
  if b in WATER:return 'water'
  if b==19:return 'waterfall'
  if b in (22,23):return 'shallow'
  if b in (96,108):return 'entry'
  if b==97:return 'upstairs'
  if b in (101,109,110):return 'exit'
  if b in (15,102):return 'hole'
  if b in range(48,64):return {56:'ledge_east',57:'ledge_west'}.get(b,'ledge_south')
  return 'solid' if states=={True} else 'floor'
 def tile(self,im):
  raw=im.tobytes()
  if raw not in self.cache:assert len(self.tiles)<(424 if self.kind=='primary' else 480);self.cache[raw]=self.offset+len(self.tiles);self.tiles.append(raw)
  return self.cache[raw]
 def pal(self,s):return s if self.kind=='primary' else 6+s
 def quadrant(self,im,pal):return [self.tile(im.crop((x,y,x+8,y+8)))|pal<<12 for x,y in ((0,0),(8,0),(0,8),(8,8))]
 def put(self,mid,bottom,pal,top=None):self.entries[(mid-self.offset)*8:(mid-self.offset+1)*8]=self.quadrant(bottom,pal)+(self.quadrant(*top) if top else [self.offset]*4)
 def solid_art(self,mid):
  edges={'left':{0x20d,0x218,0x21b,0x2eb,0x2f0,0x2f8,0x302,0x30a,0x312},'right':{0x212,0x21a,0x21c,0x2ed,0x2f3,0x2f9,0x303,0x30d,0x315},'top':{0x209,0x223,0x224,0x2e6,0x2e7,0x2e9,0x2f4,0x30e},'bottom':{0x210,0x220,0x222,0x2ee,0x2f1,0x2f2,0x304,0x305,0x31c,0x31d}}
  for name,ids in edges.items():
   if self.source.name=='cave' and mid in ids:return self.art[name]
  return self.art['mass']
 def draw(self):
  floor,p=self.art['floor'];p=self.pal(p)
  for i in range(len(self.attrs)):self.put(i+self.offset,floor,p)
  old=Renderer(resolve_bank(ROOT,'gTileset_General'),self.source) if self.kind=='secondary' else None
  for mid,role in sorted(self.roles.items()):
   b=self.attrs[mid-self.offset]&255
   if role in ('water','waterfall'):
    base=428 if role=='waterfall' else 424;self.entries[(mid-self.offset)*8:(mid-self.offset+1)*8]=[base+i|2<<12 for i in range(4)]+[self.offset]*4
    if b in (80,81,82,83):
     im=Image.new('L',(16,16),0);d=ImageDraw.Draw(im);d.polygon([(3,7),(8,7),(8,4),(12,8),(8,12),(8,9),(3,9)],fill=12,outline=1);im=im.rotate({80:0,81:180,82:90,83:270}[b]);self.entries[(mid-self.offset)*8+4:(mid-self.offset+1)*8]=self.quadrant(im,self.pal(5))
   elif role=='solid':im,slot=self.solid_art(mid);self.put(mid,floor,p,(im,self.pal(slot)))
   elif role in ('entry','upstairs','ledge_south','ledge_west','ledge_east'):im,slot=self.art[role];self.put(mid,floor,p,(im,self.pal(slot)))
   elif role in ('hole','exit'):
    im=Image.new('L',(16,16),0);d=ImageDraw.Draw(im)
    if role=='hole':d.ellipse((1,2,14,14),fill=1,outline=3)
    else:
     for x in range(0,16,4):d.line((x,12,x+2,12),fill=6)
    self.put(mid,floor,p,(im,self.pal(5)))
   else:self.put(mid,floor,p)
   if old and mid not in self.aliases.values() and mid in self.uses:
    im=old.metatile(mid).convert('RGB')
    if len(set(im.getdata()))==1 and max(im.getpixel((0,0)))<80:self.put(mid,Image.new('L',(16,16),1),self.pal(5));self.roles[mid]='void'
  self.dst.mkdir(parents=True,exist_ok=True);(self.dst/'palettes').mkdir(exist_ok=True)
  for i in range(13):
   colors=self.pals.get(i if self.kind=='primary' else i-6,[(0,0,0)]*16);text='JASC-PAL\n0100\n16\n'+''.join('%d %d %d\n'%c for c in colors);(self.dst/f'palettes/{i:02}.pal').write_bytes(text.replace('\n','\r\n').encode())
  if self.kind=='primary':
   while len(self.tiles)<432:self.tiles.append(bytes(64))
   for base,im in ((424,self.art['water'][0]),(428,self.art['water'][0].rotate(90))):
    for j,(x,y) in enumerate(((0,0),(8,0),(0,8),(8,8))):self.tiles[base+j]=im.crop((x,y,x+8,y+8)).tobytes()
   for f in range(8):
    for kind,im in [('water',ImageChops.offset(self.art['water'][0],-f*2,0)),('waterfall',ImageChops.offset(self.art['water'][0].rotate(90),0,f*2))]:
     img=Image.new('P',(16,16));img.putpalette([c for i in range(256) for c in (i,i,i)]);img.putdata(im.getdata());path=ROOT/f'graphics/tilesets/arauna_grutas_v1/{self.family}/{kind}/{f}.png';path.parent.mkdir(parents=True,exist_ok=True);img.save(path,bits=4)
  sheet=Image.new('P',(128,((len(self.tiles)+15)//16)*8));sheet.putpalette([c for i in range(256) for c in (i,i,i)])
  for i,t in enumerate(self.tiles):sheet.paste(Image.frombytes('L',(8,8),t),(i%16*8,i//16*8))
  sheet.save(self.dst/'tiles.png',bits=4);binary(self.dst/'metatiles.bin',self.entries);binary(self.dst/'metatile_attributes.bin',self.attrs)
  return {'path':str(self.dst.relative_to(ROOT)),'source':str(self.source.relative_to(ROOT)),'symbol':self.symbol,'kind':self.kind,'family':self.family,'required_ids':sorted(self.required),'aliases':{str(k):v for k,v in self.aliases.items()},'roles':{str(k):v for k,v in self.roles.items()},'script_ids':sorted(self.scriptids)}
def main():
 node=json.loads((ROOT/'data/layouts/layouts.json').read_text());old={l['id']:l for l in json.loads(gitbytes('data/layouts/layouts.json'))['layouts']};new={l['id']:l for l in node['layouts']};maps={};uses={};scripts={};labels=dict((n,int(v,16)) for n,v in re.findall(r'#define (METATILE_\w+)\s+(0x[0-9a-fA-F]+)',(ROOT/'include/constants/metatile_labels.h').read_text()))
 for p in sorted((ROOT/'data/maps').glob('*/map.json')):
  name=p.parent.name
  if not name.startswith(('VictoryRoad','SeafloorCavern')):continue
  m=json.loads(p.read_text());l=old[m['layout']];family='victory' if name.startswith('VictoryRoad') else 'seafloor';grid=list(struct.unpack('<%dH'%(l['width']*l['height']),gitbytes(l['blockdata_filepath'])));maps[name]={'layout':l,'family':family,'grid':grid};ids=set()
  for token in re.findall(r'^\s*setmetatile\s+[^,]+,\s*[^,]+,\s*([^,\s]+)',(p.parent/'scripts.inc').read_text(),re.M):ids.add(labels[token] if token in labels else int(token,0))
  for kind,sym in [('primary',l['primary_tileset']),('secondary',l['secondary_tileset'])]:
   key=(family,kind,resolve_bank(ROOT,sym));u=uses.setdefault(key,{});scripts.setdefault(key,set()).update(mid for mid in ids if (mid<512)==(kind=='primary'))
   for v in grid+words(ROOT/l['border_filepath']):
    mid=v&1023
    if (mid<512)==(kind=='primary'):u.setdefault(mid,set()).add(bool(v&0xc00))
 arts={f:extract(f) for f in ('victory','seafloor')};banks={key:Bank(*key,u,*arts[key[0]],scripts[key]) for key,u in uses.items()};report={'base_commit':BASE,'maps':{},'banks':{},'water_tiles':[424,428],'reserved_tiles_never_used':[[432,511],[992,1023]]}
 for b in banks.values():report['banks'][b.slug]=b.draw()
 for name,d in maps.items():
  l=d['layout'];pb=banks[(d['family'],'primary',resolve_bank(ROOT,l['primary_tileset']))];sb=banks[(d['family'],'secondary',resolve_bank(ROOT,l['secondary_tileset']))];grid=[];count=0
  for v in d['grid']:
   mid=v&1023;b=pb if mid<512 else sb
   if mid in b.aliases and v&0xc00:mid=b.aliases[mid];count+=1
   grid.append(v&~1023|mid)
  binary(ROOT/l['blockdata_filepath'],grid);new[l['id']]['primary_tileset']='gTileset_'+pb.symbol;new[l['id']]['secondary_tileset']='gTileset_'+sb.symbol;report['maps'][name]={'layout':l['id'],'primary':pb.slug,'secondary':sb.slug,'family':d['family'],'remapped_ids':count,'width':l['width'],'height':l['height']}
 dump(ROOT/'data/layouts/layouts.json',node);bodies={f:'' for f in ('graphics.h','metatiles.h','headers.h')}
 for b in banks.values():
  p=str(b.dst.relative_to(ROOT));s=b.symbol;bodies['graphics.h']+=f'const u32 gTilesetTiles_{s}[] = INCGFX_U32("{p}/tiles.png", ".4bpp.lz");\nconst u16 gTilesetPalettes_{s}[][16] =\n{{\n'+''.join(f'    INCGFX_U16("{p}/palettes/{i:02}.pal", ".gbapal"),\n' for i in range(13))+'};\n';bodies['metatiles.h']+=f'const u16 gMetatiles_{s}[] = INCBIN_U16("{p}/metatiles.bin");\nconst u16 gMetatileAttributes_{s}[] = INCBIN_U16("{p}/metatile_attributes.bin");\n';callback='InitTilesetAnim_AraunaGrutas'+b.family.title()+'V1' if b.kind=='primary' else 'NULL';bodies['headers.h']+=f'const struct Tileset gTileset_{s} =\n{{\n    .isCompressed = TRUE,\n    .isSecondary = {"FALSE" if b.kind=="primary" else "TRUE"},\n    .tiles = gTilesetTiles_{s},\n    .palettes = gTilesetPalettes_{s},\n    .metatiles = gMetatiles_{s},\n    .metatileAttributes = gMetatileAttributes_{s},\n    .callback = {callback},\n}};\n'
 for n,body in bodies.items():block(ROOT/'src/data/tilesets'/n,body)
 code=''
 for family in ('victory','seafloor'):
  prefix='AraunaGrutas'+family.title()+'V1'
  for kind in ('water','waterfall'):
   for i in range(8):code+=f'static const u16 s{prefix}{kind}{i}[] = INCGFX_U16("graphics/tilesets/arauna_grutas_v1/{family}/{kind}/{i}.png", ".4bpp");\n'
   code+=f'static const u16 *const s{prefix}{kind}Frames[] = {{'+', '.join(f's{prefix}{kind}{i}' for i in range(8))+'};\n'
  code+=f'''static void TilesetAnim_{prefix}(u16 timer)
{{
    if (timer % 16 == 0)
    {{
        u16 frame = (timer / 16) % 8;
        AppendTilesetAnimToBuffer(s{prefix}waterFrames[frame], (u16 *)(BG_VRAM + TILE_OFFSET_4BPP(424)), 4 * TILE_SIZE_4BPP);
        AppendTilesetAnimToBuffer(s{prefix}waterfallFrames[frame], (u16 *)(BG_VRAM + TILE_OFFSET_4BPP(428)), 4 * TILE_SIZE_4BPP);
    }}
}}
void InitTilesetAnim_{prefix}(void)
{{
    sPrimaryTilesetAnimCounter = 0;
    sPrimaryTilesetAnimCounterMax = 128;
    sPrimaryTilesetAnimCallback = TilesetAnim_{prefix};
}}
'''
 block(ROOT/'src/tileset_anims.c',code);p=ROOT/'include/tileset_anims.h';text=gitbytes('include/tileset_anims.h').decode();text=text.replace('#endif // GUARD_TILESET_ANIMS_H','// '+MARK+'_BEGIN\nvoid InitTilesetAnim_AraunaGrutasVictoryV1(void);\nvoid InitTilesetAnim_AraunaGrutasSeafloorV1(void);\n// '+MARK+'_END\n\n#endif // GUARD_TILESET_ANIMS_H');p.write_text(text)
 h='/* Generated by build_campanha_grutas_v1.py. */\n'+''.join(f'extern const struct Tileset gTileset_{b.symbol};\n' for b in banks.values())+'extern const struct Tileset gTileset_AraunaRotaTunelV1;\n'
 h+='''static u16 AraunaGrutas_NormalizeSavedBlock(u16 block)
{
    u16 mid = block & 0x03FF;
    const struct Tileset *bank = mid < 512 ? gMapHeader.mapLayout->primaryTileset : gMapHeader.mapLayout->secondaryTileset;
    if (bank == &gTileset_AraunaRotaTunelV1 && !(block & 0x0C00) && mid == 0x279)
        return (block & 0xFC00) | 0x303;
    if (!(block & 0x0C00))
        return block;
'''
 for b in banks.values():
  if b.aliases:h+=f'    if (bank == &gTileset_{b.symbol})\n    {{\n        switch (mid)\n        {{\n'+''.join(f'        case {omid}: return (block & 0xFC00) | {nmid};\n' for omid,nmid in sorted(b.aliases.items()))+'        default: break;\n        }\n    }\n'
 h+='    return block;\n}\n';(ROOT/'src/data/arauna_grutas_saved_view.h').write_text(h);fp=ROOT/'src/fieldmap.c';fs=fp.read_text();anchor='static const struct ConnectionFlags sDummyConnectionFlags = {0};'
 if '#include "data/arauna_grutas_saved_view.h"' not in fs:fs=fs.replace(anchor,anchor+'\n\n#include "data/arauna_grutas_saved_view.h"')
 fs=fs.replace('sBackupMapData[j + width * i] = *mapView;','sBackupMapData[j + width * i] = AraunaGrutas_NormalizeSavedBlock(*mapView);');fp.write_text(fs);dump(OUT/'build.json',report);print('Built',len(maps),'maps;',len(banks),'isolated banks')
if __name__=='__main__':main()
