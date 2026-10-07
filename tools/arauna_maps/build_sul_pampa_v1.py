#!/usr/bin/env python3
"""Reproducible original southern surface art and connection aliases."""
import argparse,collections,json,re,subprocess,tempfile,shutil
from pathlib import Path
from PIL import Image,ImageDraw
from native_visuals_v2 import ROOT,Pair,dump,binary,marked,declarations
from bancos_nativos import bank_words
from render_native_map import words
BASE='591aeb24973622bda8d12cce60b3560cef938c00'
TARGETS=('Route102','Route103','Route104','PetalburgCity')
ART_NAMES=('araucaria','tree','capim','rock','home','clinic','market','hall','fence','crop','roots','reeds','bridge','pier','fountain','cliff')
def lid(n):return 'LAYOUT_ARAUNA_'+re.sub(r'([a-z])([A-Z])',r'\1_\2',n).upper()+'_SUL_PAMPA_V1'
class Art:
 def __init__(self,pair):
  self.pair=pair;self.assets={};self.cache={};self.custom=[]
  src=Image.open(ROOT/'art/sul_pampa_v1/source_atlas.png').convert('RGBA')
  for n,box in zip(ART_NAMES,json.loads((ROOT/'art/sul_pampa_v1/asset_regions.json').read_text())):
   im=src.crop(box);im.putalpha(im.getchannel('A').point(lambda v:255 if v>=128 else 0));self.assets[n]=im.crop(im.getbbox())
  self.grass=Image.new('RGBA',(16,16),(112,144,72,255));d=ImageDraw.Draw(self.grass)
  for x,y in ((2,3),(11,10)):d.line((x,y+2,x+1,y),fill=(80,112,48,255));d.point((x+2,y+2),fill=(144,160,88,255))
  self.earth=Image.new('RGBA',(16,16),(176,120,64,255));d=ImageDraw.Draw(self.earth)
  for x,y in ((2,7),(9,3),(12,13)):d.line((x,y,x+2,y),fill=(200,144,88,255));d.point((x,y+1),fill=(144,96,56,255))
  self.stone=Image.new('RGBA',(16,16),(168,160,128,255));d=ImageDraw.Draw(self.stone);d.line((0,7,15,7),fill=(128,120,96,255));d.line((7,0,7,6),fill=(128,120,96,255));d.line((3,8,3,15),fill=(128,120,96,255))
 def quant(self,rgba):
  pixels=list(rgba.getdata());cs={c[:3] for c in pixels if c[3]};best=None
  for q,p in enumerate(self.pair.pals):
   mp={c:min(range(1,16),key=lambda j:sum((a-b)**2 for a,b in zip(c,p[j]))) for c in cs};loss=sum(sum((a-b)**2 for a,b in zip(c[:3],p[mp[c[:3]]])) for c in pixels if c[3])
   if best is None or loss<best[0]:best=loss,q,mp
  _,q,mp=best;im=Image.new('L',rgba.size);im.putdata([mp[c[:3]] if c[3] else 0 for c in pixels]);return im,q
 def entries(self,rgba):
  key=rgba.tobytes()
  if key not in self.cache:
   im,q=self.quant(rgba);self.cache[key]=self.pair.entries(im,q)
  return self.cache[key]
 def block(self,ground,attr,object=None):
  entries=self.entries(ground)+(self.entries(object) if object is not None else [0]*4);mid=self.pair.alias(0,entries,attr);self.custom.append(mid);return mid
 def asset(self,n,size):return self.assets[n].resize(size,Image.Resampling.NEAREST)
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--base',type=Path,required=True);ap.add_argument('--art-only',action='store_true');a=ap.parse_args();base=a.base.resolve();assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=base,text=True).strip()==BASE
 for f in ('src/arauna_border_visuals.c','src/fldeff_cut.c','src/data/tilesets/headers.h','src/data/tilesets/metatiles.h','src/data/tilesets/graphics.h'):(ROOT/f).write_bytes((base/f).read_bytes())
 node=json.loads((base/'data/layouts/layouts.json').read_text());ls={l['id']:l for l in node['layouts']};maps={m['name']:m for p in (base/'data/maps').glob('*/map.json') for m in [json.loads(p.read_text())]};byid={m['id']:m for m in maps.values()};report={'base_commit':BASE,'maps':{}};decl=collections.defaultdict(str)
 for n in TARGETS:
  print('Building art',n,flush=True)
  m=maps[n];l=ls[m['layout']];pair=Pair(base,l,repack=True);neighbor=[byid[c['map']]['name'] for c in m['connections'] or [] if c['direction'] in ('up','down','left','right')];pair.reserve(base,[n]+neighbor,ls,maps);old=words(base/l['blockdata_filepath']);g=list(old);w,h=l['width'],l['height']
  protected0={(int(e['x']),int(e['y'])) for k in ('warp_events','bg_events') for e in m[k]}
  keep={v&1023 for j,v in enumerate(old) if bank_words(pair.reader,v&1023,True)&255 not in (0,2) or (j%w,j//w) in protected0}
  labels={k:int(v,16) for hp in (base/'include/constants').glob('*metatile*.h') for k,v in re.findall(r'#define (METATILE_\w+)\s+(0x[\da-fA-F]+)',hp.read_text())}
  script=''.join(p.read_text() for p in (base/'data/maps'/n).glob('*.inc'));keep.update(labels[k] for k in re.findall(r'METATILE_\w+',script) if k in labels)
  engine=''.join(p.read_text() for p in (base/'src').glob('*.c'));engine_keep={labels[k] for k in re.findall(r'METATILE_General_\w+',engine) if k in labels and not any(word in k for word in ('Grass','Door'))};keep.update(engine_keep);keep.update((1,0xd,0x1c6,0x1c7,0x1d4,0x1d5,0x1dc,0x1dd))
  pair.tiles={i:raw for i,raw in pair.tiles.items() if i in pair.dynamic};pair.tiles[0]=bytes(64);pair.tile_cache={bytes(64):0};pair.free=[i for i in list(range(1,432))+list(range(512,992)) if i not in pair.dynamic];pair.touched=set();pair.meta=[[0]*len(b) for b in pair.meta]
  for mid in sorted(keep):
   try:entries=bank_words(pair.reader,mid)
   except ValueError:continue
   copied=[]
   for e in entries:
    tid=e&1023
    if tid not in pair.dynamic:
     im=pair.reader._tile(tid);tid=pair.tile(im if im is not None else Image.new('L',(8,8)))
    copied.append((e&~1023)|tid)
   pair.meta[mid>=512][mid%512*8:mid%512*8+8]=copied
  assert not any(e>>12==12 for b in pair.meta for e in b if e&1023),(n,'palette12 used by functional tiles')
  pair.pals[12]=[(0,0,0),(24,40,24),(40,64,32),(56,88,40),(72,112,48),(88,128,56),(112,144,72),(144,168,88),(184,192,112),(56,40,24),(88,56,32),(120,80,40),(168,120,64),(200,152,88),(224,208,160),(144,136,112)]
  art=Art(pair);objects=Image.new('RGBA',(w*16,h*16));land={};zones=[];assetcache={}
  def obj(kind,x,y,ww,hh):
   key=kind,ww,hh
   if key not in assetcache:
    image=art.asset(kind,(ww*16,hh*16));pix,q=art.quant(image);image.putdata([(*pair.pals[q][v],255 if v else 0) for v in pix.getdata()]);assetcache[key]=image
   objects.alpha_composite(assetcache[key],(x*16,y*16));zones.append({'kind':kind,'rectangle':[x,y,x+ww,y+hh]})
  for j,v in enumerate(old):
   x,y=j%w,j//w
   if n=='Route104' and v&1023==0x208 and x+1<w and y+3<h:obj('araucaria',x,y,2,4)
   if v&1023==0x1d4 and x+1<w and y+2<h:obj('araucaria' if n in ('Route104','Route103') else 'tree',x,y,2,3)
  if n=='PetalburgCity':
   for kind,x,y,ww,hh in [('hall',10,3,11,6),('home',23,3,6,5),('clinic',23,12,6,5),('market',7,17,6,5),('home',15,23,6,5),('home',25,23,6,5),('fountain',18,20,3,3)]:obj(kind,x,y,ww,hh)
   for y in range(17,23):
    for x in range(14,26):land[x,y]='stone'
   roads=[[(0,12),(8,12),(15,12),(18,17),(26,18),(37,22)],[(18,17),(18,27)],[(26,8),(26,12)]]
  elif n=='Route102':
   roads=[[(0,12),(8,12),(15,8),(24,10),(34,14),(49,12)]]
   for kind,x,y,ww,hh in [('fence',11,3,5,1),('crop',12,4,4,2),('fence',26,15,5,1),('crop',27,16,3,2)]:obj(kind,x,y,ww,hh)
  elif n=='Route103':
   roads=[[(8,21),(10,16),(9,10),(12,6)],[(59,13),(67,17),(79,17)]]
   for kind,x,y,ww,hh in [('reeds',22,8,2,2),('reeds',51,10,2,2),('rock',39,2,2,2),('fence',11,17,3,1)]:obj(kind,x,y,ww,hh)
  else:
   roads=[[(20,0),(19,5),(17,9),(18,22),(10,29)],[(11,39),(15,42),(21,47),(24,54),(28,62),(39,62)]]
   for kind,x,y,ww,hh in [('market',2,14,7,5),('home',14,46,7,5),('roots',3,31,4,2),('roots',17,33,4,2)]:obj(kind,x,y,ww,hh)
  for pts in roads:
   for (x1,y1),(x2,y2) in zip(pts,pts[1:]):
    dist=max(abs(x2-x1),abs(y2-y1),1)
    for k in range(dist+1):
     x=round(x1+(x2-x1)*k/dist);y=round(y1+(y2-y1)*k/dist)
     for yy in range(y-1,y+2):
      for xx in range(x-1,x+2):land[xx,yy]='earth'
  protected={(int(e['x']),int(e['y'])) for k in ('warp_events','bg_events') for e in m[k]};counts=collections.Counter();geometry=[]
  for j,v in enumerate(old):
   x,y=j%w,j//w;mid=v&1023;attr=bank_words(pair.reader,mid,True);behavior=attr&255;fg=objects.crop((x*16,y*16,x*16+16,y*16+16));has=fg.getbbox() is not None
   if behavior not in (0,2) or (x,y) in protected:continue
   if not has and v&0xc00:fg=art.asset('roots' if n=='Route104' else 'capim',(16,16));has=True
   if behavior==2:fg=art.asset('capim',(16,16));has=True
   alias=art.block(getattr(art,land.get((x,y),'grass')),attr,fg if has else None);g[j]=(v&0xfc00)|alias
   if n=='Route102' and behavior==0 and not v&0xc00 and any(z['kind']=='fence' and z['rectangle'][0]<=x<z['rectangle'][2] and z['rectangle'][1]<=y<z['rectangle'][3] for z in zones) and (x,y) not in {(int(e['x']),int(e['y'])) for e in m['object_events']}:g[j]|=0x400;geometry.append([x,y])
   counts['new_cells']+=1
  paths=[ROOT/'data/tilesets'/kind/('arauna_sul_'+n.lower()+'_v1') for kind in ('primary','secondary')];symbols=['AraunaSul'+n+('Base' if k==0 else 'Art')+'V1' for k in range(2)];pair.write(paths)
  for field,text in declarations(paths,symbols,pair.callbacks).items():decl[field]+=text
  p=ROOT/'data/layouts'/('AraunaSul'+n+'V1');binary(p/'map.bin',g);binary(p/'border.bin',words(base/l['border_filepath']));node['layouts'].append(dict(l,id=lid(n),name='AraunaSul'+n+'V1_Layout',blockdata_filepath=str((p/'map.bin').relative_to(ROOT)),border_filepath=str((p/'border.bin').relative_to(ROOT)),primary_tileset='gTileset_'+symbols[0],secondary_tileset='gTileset_'+symbols[1]));dump(ROOT/f'data/maps/{n}/map.json',dict(m,layout=lid(n)))
  report['maps'][n]={'old_layout':l['id'],'new_layout':lid(n),'dimensions':[w,h],'paths':[str(p.relative_to(ROOT)) for p in paths],'symbols':symbols,'new_cells':counts['new_cells'],'custom_metatile_ids':sorted(set(art.custom)),'new_static_slots':sorted(pair.touched),'engine_created_ids':sorted(engine_keep),'scene_events_and_warps_preserved':True,'geometry_changed_cells':geometry,'elevation_behavior_preserved':True,'landmarks':zones,'cut_outputs':{str(i):art.block(art.grass,bank_words(pair.reader,i,True)&~255) for i in set(art.custom) if (pair.attrs[i>=512][i%512]&255)==2}}
  pair.write(paths)
 for field,text in decl.items():marked(ROOT/'src/data/tilesets'/field,'SUL_PAMPA_V1',text)
 dump(ROOT/'data/layouts/layouts.json',node);dump(ROOT/'review/sul_pampa_v1/art_build.json',report)
 p=ROOT/'src/overworld.c';s=(base/'src/overworld.c').read_text();needle='(oldId == LAYOUT_OLDALE_TOWN && newId == LAYOUT_ARAUNA_OLDALE_TOWN_COMPOSICAO_V1)))';s=s.replace(needle,'(oldId == LAYOUT_OLDALE_TOWN && newId == LAYOUT_ARAUNA_OLDALE_TOWN_COMPOSICAO_V1)'+''.join('\n       || (oldId == '+report['maps'][n]['old_layout']+' && newId == '+lid(n)+')' for n in TARGETS)+'))');assert s!=(base/'src/overworld.c').read_text();p.write_text(s)
 if not a.art_only:
  with tempfile.TemporaryDirectory(prefix='arauna-art-source-') as t:
   src=Path(t)
   for folder in ('data','include/constants','src/data/tilesets'):shutil.copytree(ROOT/folder,src/folder)
   for p in (base/'src').glob('*.c'):shutil.copy(p,src/'src'/p.name)
   subprocess.run(['python3',str(ROOT/'tools/arauna_maps/build_sul_borders_v1.py'),'--source',str(src)],check=True)
if __name__=='__main__':main()
