#!/usr/bin/env python3
"""Sul/Pampa 1.1 vegetation and original Serra do Uivo/coastal/mining scenery."""
import argparse,collections,json,re,subprocess,tempfile,shutil
from pathlib import Path
from PIL import Image,ImageDraw
from native_visuals_v2 import ROOT,Pair,dump,binary,marked,declarations
from bancos_nativos import bank_words
from render_native_map import words
from build_sul_pampa_v1 import Art as PreviousArt
from build_uivo_borders_v1 import private_alias
from script_metatile_dependencies import collect
BASE='59f4c6eea2a7aa033bb10ca4e6074a0a2ec3883c'
FIXES=('Route102','Route103','Route104');REDRAW=('RustboroCity','Route115','Route116');TARGETS=FIXES+REDRAW
NAMES=('bush','forest','araucaria','boulder','home','clinic','market','sobrado','gym','guild','school','fence','cliff','coastal_bush','mining','tunnel')

def lid(n):return 'LAYOUT_ARAUNA_UIVO_'+re.sub(r'([a-z])([A-Z])',r'\1_\2',n).upper()+'_V1'
class Art(PreviousArt):
 def __init__(self,pair):
  self.pair=pair;self.assets={};self.cache={};self.custom=[]
  src=Image.open(ROOT/'art/uivo_norte_v1/source_atlas.png').convert('RGBA')
  for n,box in zip(NAMES,json.loads((ROOT/'art/uivo_norte_v1/asset_regions.json').read_text())):
   im=src.crop(box);im.putalpha(im.getchannel('A').point(lambda v:255 if v>=128 else 0));self.assets[n]=im.crop(im.getbbox())
  self.grass=Image.new('RGBA',(16,16),(104,144,64,255));d=ImageDraw.Draw(self.grass)
  for x,y in ((2,3),(11,10)):d.line((x,y+2,x+1,y),fill=(64,104,40,255));d.point((x+2,y+2),fill=(136,168,80,255))
  self.earth=Image.new('RGBA',(16,16),(168,120,72,255));d=ImageDraw.Draw(self.earth)
  for x,y in ((2,7),(9,3),(12,13)):d.line((x,y,x+2,y),fill=(192,152,96,255));d.point((x,y+1),fill=(136,96,56,255))
  self.stone=Image.new('RGBA',(16,16),(136,136,120,255));d=ImageDraw.Draw(self.stone);d.line((0,7,15,7),fill=(88,96,80,255));d.line((7,0,7,6),fill=(88,96,80,255));d.line((3,8,3,15),fill=(88,96,80,255));d.point((11,11),fill=(168,168,144,255))
  self.stairs=self.stone.copy();d=ImageDraw.Draw(self.stairs)
  for y in (0,4,8,12):d.line((0,y,15,y),fill=(184,184,160,255));d.line((0,y+3,15,y+3),fill=(56,64,56,255))
  self.sand=Image.new('RGBA',(16,16),(192,168,112,255));d=ImageDraw.Draw(self.sand)
  for x,y in ((1,2),(8,7),(12,13)):d.point((x,y),fill=(160,136,88,255));d.point((x+1,y),fill=(216,192,136,255))
 def asset(self,n,size):
  im=self.assets[n]
  if n in ('home','clinic','market','sobrado','gym','guild','school'):
   # Canonical 64x64 facades, expanded by whole 8px tile repetition.
   # This preserves crisp native pixels and keeps the bank below hardware capacity.
   src=im.resize((64,64),Image.Resampling.NEAREST);out=Image.new('RGBA',size)
   for y in range(0,size[1],8):
    for x in range(0,size[0],8):
     sx=round(x/(size[0]-8)*7)*8;sy=round(y/(size[1]-8)*7)*8;out.paste(src.crop((sx,sy,sx+8,sy+8)),(x,y))
   return out
  if max(size)>32:return im.resize((size[0]//2,size[1]//2),Image.Resampling.NEAREST).resize(size,Image.Resampling.NEAREST)
  return im.resize(size,Image.Resampling.NEAREST)
 def entries(self,rgba):
  key=rgba.tobytes()
  if key not in self.cache:
   im,q=self.quant(rgba);entries=[]
   for x,y in ((0,0),(8,0),(0,8),(8,8)):
    tile=im.crop((x,y,x+8,y+8));raw=tile.tobytes();found=None
    for op,flags in ((None,0),(Image.Transpose.FLIP_LEFT_RIGHT,0x400),(Image.Transpose.FLIP_TOP_BOTTOM,0x800),(Image.Transpose.ROTATE_180,0xc00)):
     candidate=(tile.transpose(op) if op is not None else tile).tobytes()
     if candidate in self.pair.tile_cache:found=self.pair.tile_cache[candidate]|flags;break
    if found is None:found=self.pair.tile(tile)
    entries.append(found|q<<12)
   self.cache[key]=entries
  return self.cache[key]
 def block(self,ground,attr,object=None):
  entries=self.entries(ground)+(self.entries(object) if object is not None else [0]*4);mid=private_alias(self.pair,0,entries,attr);self.custom.append(mid);return mid

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--base',type=Path,required=True);ap.add_argument('--art-only',action='store_true');a=ap.parse_args();base=a.base.resolve();assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=base,text=True).strip()==BASE
 for f in ('src/arauna_border_visuals.c','src/fldeff_cut.c','src/overworld.c','src/data/tilesets/headers.h','src/data/tilesets/metatiles.h','src/data/tilesets/graphics.h'):(ROOT/f).write_bytes((base/f).read_bytes())
 node=json.loads((base/'data/layouts/layouts.json').read_text());ls={l['id']:l for l in node['layouts']};maps={m['name']:m for p in (base/'data/maps').glob('*/map.json') for m in [json.loads(p.read_text())]};byid={m['id']:m for m in maps.values()};report={'base_commit':BASE,'maps':{}};decl=collections.defaultdict(str)
 previous=json.loads((base/'review/sul_pampa_v1/art_build.json').read_text())['maps'];labels={k:int(v,16) for hp in (base/'include/constants').glob('*metatile*.h') for k,v in re.findall(r'#define (METATILE_\w+)\s+(0x[\da-fA-F]+)',hp.read_text())};engine=''.join(p.read_text() for p in (base/'src').glob('*.c'));engine_keep={labels[k] for k in re.findall(r'METATILE_General_\w+',engine) if k in labels}
 for n in TARGETS:
  print('Building scenery',n,flush=True);m=maps[n];l=ls[m['layout']];pair=Pair(base,l,repack=True);old=words(base/l['blockdata_filepath']);g=list(old);w,h=l['width'],l['height'];neighbors=[byid[c['map']]['name'] for c in m['connections'] or [] if c['direction'] in ('up','down','left','right')];pair.reserve(base,[n]+neighbors,ls,maps);art=Art(pair);zones=[];changes=[];cut={};newslots0=set(pair.touched)
  if n in FIXES:
   ids={'Route102':{778,779},'Route103':{565,566,586,737},'Route104':{753,873}}[n];expected={'Route102':104,'Route103':588,'Route104':688}[n]
   assert sum((v&1023) in ids and bool(v&0xc00) for v in old)==expected
   foreground=art.asset('forest',(32,32)).crop((8,6,24,22)) if n=='Route104' else art.asset('bush',(16,16));entries=art.entries(foreground)
   for mid in sorted(ids):
    assert bank_words(pair.reader,mid,True)&255==0
    # All uses must be blocked: never change an encounter/passable tile.
    assert all(v&0xc00 for v in old if v&1023==mid)
    pair.meta[mid>=512][mid%512*8+4:mid%512*8+8]=entries;art.custom.append(mid)
   changes=[[j%w,j//w] for j,v in enumerate(old) if v&1023 in ids];cut=previous[n]['cut_outputs'];created=previous[n]['engine_created_ids'];outlayout=l;geometry=[]
  else:
   keep={v&1023 for j,v in enumerate(old) if bank_words(pair.reader,v&1023,True)&255 not in (0,2,12,33) or (j%w,j//w) in {(int(e['x']),int(e['y'])) for k in ('warp_events','bg_events') for e in m[k]}}
   script_ids,script_labels=collect(base,n,labels);keep.update(script_ids);keep.update(engine_keep);pair.reserved.update(keep)
   pair.tiles={i:raw for i,raw in pair.tiles.items() if i in pair.dynamic};pair.tiles[0]=bytes(64);pair.tile_cache={bytes(64):0};pair.free=[i for i in list(range(1,432))+list(range(512,992)) if i not in pair.dynamic];pair.touched=set();pair.meta=[[0]*len(b) for b in pair.meta]
   for mid in sorted(keep):
    try:entries=bank_words(pair.reader,mid)
    except ValueError:continue
    copied=[]
    for e in entries:
     t=e&1023
     if t not in pair.dynamic:
      im=pair.reader._tile(t);t=pair.tile(im if im is not None else Image.new('L',(8,8)))
     copied.append((e&~1023)|t)
    pair.meta[mid>=512][mid%512*8:mid%512*8+8]=copied
   print("Functional graphics",n,len(pair.tile_cache),"keep",len(keep),flush=True)
   # Free art palette rows get dedicated green and stone/roof ramp groups.
   usedrows={e>>12 for b in pair.meta for e in b if e&1023}
   ramps=[[(0,0,0),(24,40,24),(40,64,32),(56,88,40),(72,112,48),(88,128,56),(112,144,72),(144,168,88),(184,192,112),(56,40,24),(88,56,32),(120,80,40),(168,120,64),(200,152,88),(224,208,160),(144,136,112)],[(0,0,0),(32,32,40),(48,56,64),(64,72,80),(88,96,104),(120,128,128),(152,160,152),(192,192,168),(224,216,184),(64,32,24),(96,48,32),(136,64,40),(176,88,48),(208,120,64),(232,152,80),(120,88,56)]]
   for q,colors in zip([q for q in range(12,-1,-1) if q not in usedrows],ramps):pair.pals[q]=colors
   art=Art(pair);objects=Image.new('RGBA',(w*16,h*16));assets={}
   def obj(kind,x,y,ww,hh):
    key=kind,ww,hh
    if key not in assets:
     image=art.asset(kind,(ww*16,hh*16));pix,q=art.quant(image);image.putdata([(*pair.pals[q][v],255 if v else 0) for v in pix.getdata()]);assets[key]=image
    objects.alpha_composite(assets[key],(x*16,y*16));zones.append({'kind':kind,'rectangle':[x,y,x+ww,y+hh]})
   # Trees stay on their established blocking footprints.
   for j,v in enumerate(old):
    x,y=j%w,j//w
    if v&1023==0x1d4 and x+1<w and y+1<h:obj('forest' if n=='RustboroCity' else 'araucaria',x,y,2,2)
   if n=='RustboroCity':
    for z in [('guild',6,12,7,6),('home',25,14,7,5),('gym',6,28,7,6),('clinic',25,28,7,5),('home',6,36,7,5),('home',14,34,7,5),('school',26,36,7,5),('sobrado',12,44,7,5),('home',5,46,7,5),('market',23,45,7,5),('home',30,47,7,5)]:obj(*z)
   elif n=='Route116':
    obj('home',35,4,7,5);obj('tunnel',45,5,5,4);obj('tunnel',63,7,5,4)
    # Mining supplies are placed on existing blocked mountain cells only.
    for xx,yy in ((12,2),(71,2)):
     if old[yy*w+xx]&0xc00:obj('mining',xx,yy,3,2)
   grass=art.asset('coastal_bush' if n=='Route115' else 'bush',(16,16));cliff=art.asset('cliff',(48,48));protect={(int(e['x']),int(e['y'])) for k in ('warp_events','bg_events') for e in m[k]}
   for j,v in enumerate(old):
    x,y=j%w,j//w;mid=v&1023;attr=bank_words(pair.reader,mid,True);behavior=attr&255
    if behavior not in (0,2,12,33) or (x,y) in protect:continue
    fg=objects.crop((x*16,y*16,x*16+16,y*16+16));has=fg.getbbox() is not None
    if has and not v&0xc00 and behavior!=2:
     # Visual obstacles never occupy a passable cell; keep just opaque floor.
     fg=Image.new('RGBA',(16,16));has=False
    if behavior==2:
     # Encounter grass is the familiar walkable tuft, distinct from bushes.
     from build_sul_pampa_v1 import Art as OldArt
     if not hasattr(art,'encounter'):art.encounter=OldArt(pair).asset('capim',(16,16))
     fg=art.encounter;has=True
    elif not has and v&0xc00:
     if mid in (0x1d4,0x1d5,0x1dc,0x1dd,0x1e4,0x1e5) or (n=='Route115' and behavior==0):fg=grass
     else:
      above=y>0 and not old[(y-1)*w+x]&0xc00;below=y+1<h and not old[(y+1)*w+x]&0xc00;row=0 if above else 2 if below else 1;fg=cliff.crop((x%3*16,row*16,x%3*16+16,row*16+16))
     has=True
    if n=='RustboroCity':
     street=(18<=x<=22 or 6<=x<=32 and 17<=y<=21 or 8<=x<=32 and 32<=y<=41 or 12<=x<=30 and 48<=y<=53)
     stairs=(18<=x<=22 and (24<=y<=26 or 43<=y<=44)) or 19<=x<=24 and y==6
     ground=art.stairs if stairs and not v&0xc00 else art.stone if street else art.grass
    else:ground=art.sand if behavior==33 else art.stone if behavior==12 else art.earth if n=='Route116' and 8<=y<=14 else art.grass
    g[j]=(v&0xfc00)|art.block(ground,attr,fg if has else None);changes.append([x,y])
   for mid in sorted(set(art.custom)):
    if pair.attrs[mid>=512][mid%512]&255==2:cut[str(mid)]=art.block(art.grass,pair.attrs[mid>=512][mid%512]&~255)
   p=ROOT/'data/layouts'/('AraunaUivo'+n+'V1');binary(p/'map.bin',g);binary(p/'border.bin',words(base/l['border_filepath']));outlayout=dict(l,id=lid(n),name='AraunaUivo'+n+'V1_Layout',blockdata_filepath=str((p/'map.bin').relative_to(ROOT)),border_filepath=str((p/'border.bin').relative_to(ROOT)));node['layouts'].append(outlayout);dump(ROOT/f'data/maps/{n}/map.json',dict(m,layout=lid(n)));geometry=[];created=sorted(engine_keep|script_ids)
  paths=[ROOT/'data/tilesets'/kind/('arauna_uivo_art_'+n.lower()+'_v1') for kind in ('primary','secondary')];symbols=['AraunaUivoArt'+n+('Base' if k==0 else 'Art')+'V1' for k in range(2)];pair.write(paths)
  for field,text in declarations(paths,symbols,pair.callbacks).items():decl[field]+=text
  for field,sym in zip(('primary_tileset','secondary_tileset'),symbols):outlayout[field]='gTileset_'+sym
  report['maps'][n]={'old_layout':l['id'],'new_layout':outlayout['id'],'dimensions':[w,h],'paths':[str(p.relative_to(ROOT)) for p in paths],'symbols':symbols,'new_cells':len(changes),'changed_cells':changes,'custom_metatile_ids':sorted(set(art.custom)),'new_static_slots':sorted(pair.touched),'engine_created_ids':created,'scene_events_and_warps_preserved':True,'geometry_changed_cells':geometry,'elevation_behavior_preserved':True,'landmarks':zones,'cut_outputs':cut,'fix_only':n in FIXES,'script_created_ids':sorted(collect(base,n,labels)[0])}
 for field,text in decl.items():marked(ROOT/'src/data/tilesets'/field,'UIVO_ART_V1',text)
 dump(ROOT/'data/layouts/layouts.json',node);dump(ROOT/'review/uivo_norte_v1/art_build.json',report)
 p=ROOT/'src/overworld.c';s=(base/'src/overworld.c').read_text();needle='(oldId == LAYOUT_PETALBURG_CITY && newId == LAYOUT_ARAUNA_PETALBURG_CITY_SUL_PAMPA_V1)))';assert needle in s;s=s.replace(needle,needle[:-2]+''.join('\n       || (oldId == '+report['maps'][n]['old_layout']+' && newId == '+lid(n)+')' for n in REDRAW)+'))');p.write_text(s)
 if not a.art_only:
  with tempfile.TemporaryDirectory(prefix='arauna-uivo-art-') as t:
   src=Path(t)
   for folder in ('data','include/constants','src/data/tilesets'):shutil.copytree(ROOT/folder,src/folder)
   for p in (base/'src').glob('*.c'):shutil.copy(p,src/'src'/p.name)
   subprocess.run(['python3',str(ROOT/'tools/arauna_maps/build_uivo_borders_v1.py'),'--source',str(src)],check=True)
if __name__=='__main__':main()
