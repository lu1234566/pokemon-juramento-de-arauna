#!/usr/bin/env python3
"""Reproducible native previews, not emulator screenshots."""
import argparse,json,re,tempfile
from pathlib import Path
from PIL import Image,ImageDraw
from dive_04_common import ROOT,BASE,OUT,NAMES,inventory,render,renderer
from render_native_map import words
from dive_04_c_checks import selector

def crop(im,point):
 x,y=point;left=max(0,min(im.width-240,x*16-112));top=max(0,min(im.height-160,y*16-80))
 return im.crop((left,top,left+240,top+160))

def board(pairs,title,path):
 im=Image.new('RGB',(1008,72+len(pairs)*354),'#101e28');d=ImageDraw.Draw(im);d.text((16,12),title,fill='#e8ecdc');d.text((16,36),'ANTES / BASE INSTALADA',fill='#a8b8c8');d.text((520,36),'DEPOIS / CHECKPOINT 04',fill='#a8d8d0')
 for i,(name,before,after) in enumerate(pairs):
  y=60+i*354;d.text((16,y),name,fill='#e8ecdc');im.paste(before.resize((480,320),Image.Resampling.NEAREST),(16,y+22));im.paste(after.resize((480,320),Image.Resampling.NEAREST),(512,y+22))
 im.save(path)

def surface(repo,name,compiled=None,state=False):
 node,ls,maps=inventory(repo);l=ls[maps[name]['layout']];g=words(repo/l['blockdata_filepath']);idx=node['layouts'].index(l)
 if state=='absent':
  idx=711;l=node['layouts'][idx];g=words(repo/l['blockdata_filepath']);state=False
 if name=='Route103' and state:
  for y,mid in ((5,166),(6,167)):g[y*l['width']+45]=(g[y*l['width']+45]&~1023)|mid
 if name=='Route111' and state:
  labels={k:int(v,16) for k,v in re.findall(r'#define (METATILE_\w+)\s+(0x[\da-fA-F]+)',(repo/'include/constants/metatile_labels.h').read_text())}
  block=(repo/'data/maps/Route111/scripts.inc').read_text().split('Route111_EventScript_ShowTemporaryMirageTower::')[1].split('\treturn')[0]
  for x,y,label in re.findall(r'setmetatile (\d+), (\d+), (METATILE_\w+)',block):
   i=int(y)*l['width']+int(x);g[i]=(g[i]&~0xfff)|labels[label]
 visual=[compiled.probe(idx,i%l['width']+7,i//l['width']+7,v&1023) if compiled else v&1023 for i,v in enumerate(g)]
 return render(repo,l,visual)

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--base',type=Path,required=True);a=ap.parse_args();base=a.base.resolve();_,oldls,maps=inventory(base);_,ls,_=inventory(ROOT)
 build=json.loads((OUT/'build.json').read_text());pairs=[];overview=[];files=[]
 for n in NAMES:
  l=ls[maps[n]['layout']];old=oldls[l['id']];before=render(base,old);after=render(ROOT,l,words(ROOT/build['maps'][n]['visual_grid']))
  before.save(OUT/f'{n}_antes.png');after.save(OUT/f'{n}_depois.png');files.extend([n+'_antes.png',n+'_depois.png']);overview.append((n,after))
  points=[(e['x'],e['y']) for e in maps[n]['warp_events']]+[(e['x'],e['y']) for e in maps[n]['bg_events'][:2]]
  if not points:
   g=words(ROOT/l['blockdata_filepath']);i=next(i for i,v in enumerate(g) if not v&0xc00);points=[(i%l['width'],i//l['width'])]
  if n=='Underwater_SealedChamber':points=[(12,43),(12,44),(8,19)]
  for j,point in enumerate(points[:3]):
   b,c=crop(before,point),crop(after,point);b.save(OUT/f'{n}_camera{j+1}_antes.png');c.save(OUT/f'{n}_camera{j+1}_depois.png')
   if j==0:pairs.append((n,b,c))
  if n=='Underwater_SeafloorCavern':
   # Actual script substitutions; selector must pass changed native IDs through.
   g=words(ROOT/l['blockdata_filepath']);vis=words(ROOT/build['maps'][n]['visual_grid'])
   for y,mid in ((3,542),(4,552),(5,552)):
    for x in (5,6,7,8):vis[y*l['width']+x]=mid
   render(ROOT,l,vis).save(OUT/'Submarino_Ausente.png')
 board(pairs[:6],'DIVE 04 — costa, arquipelago e mare / dados nativos',OUT/'Dive_04A_Cameras.png')
 board(pairs[6:],'DIVE 04 — oceano, arquivo e acesso Horizonte / dados nativos',OUT/'Dive_04B_Cameras.png')
 sheet=Image.new('RGB',(1248,1280),'#101e28');d=ImageDraw.Draw(sheet)
 for i,(n,im) in enumerate(overview):
  x=(i%3)*416+12;y=(i//3)*320+12;d.text((x,y),n,fill='#e8ecdc')
  ratio=min(392/im.width,284/im.height,1);im=im.resize((int(im.width*ratio),int(im.height*ratio)),Image.Resampling.NEAREST);sheet.paste(im,(x,y+24))
 sheet.save(OUT/'Dive_04_12_Mapas.png')
 with tempfile.TemporaryDirectory() as tmp:
  compiled,_=selector(Path(tmp));surfaces=[]
  for n,p,state,title in [('Route103',(45,6),True,'Altering — entrada pos-jogo'),('Route111',(19,56),False,'Mirage — torre presente'),('Route111',(19,56),True,'Mirage — estado temporario antes da queda'),('Route111',(19,56),'absent','Mirage — layout sem torre preservado')]:
   surfaces.append((title,crop(surface(base,n,state=state),p),crop(surface(ROOT,n,compiled,state),p)))
  board(surfaces,'DIVE 04 — boca de Altering e base da Mirage Tower',OUT/'Altering_Mirage_Antes_Depois.png')
 # Blend study uses the actual fog sprite image and GBA coefficients. It is a
 # host illustration of transparency, not an emulator proof of weather.
 from render_native_map import indexed_tiles,palette
 fogfile=ROOT/'graphics/weather/fog_horizontal.png';pixels,cols,count=indexed_tiles(fogfile)
 fogpal=palette(ROOT/'graphics/weather/weather.pal') if (ROOT/'graphics/weather/weather.pal').exists() else None
 # Full sheet is a 64px fog sprite; use its opaque silhouette with pale fog.
 fogpairs=[]
 for n in ('TerraCave_End','MarineCave_End'):
  l=ls[maps[n]['layout']];h=(ROOT/'src/data/arauna_cave_visuals_v2.h').read_text();grid=words(ROOT/re.search(r'sVisual_'+n+r'\[\] = INCBIN_U16\("([^"]+)"\)',h)[1]);im=crop(render(ROOT,l,grid),(5,8) if n.startswith('Terra') else (20,8))
  fogrgba=Image.new('RGBA',(240,160));d=ImageDraw.Draw(fogrgba)
  for y in range(160):
   for x in range(240):
    ix=x%pixels.width;iy=y%pixels.height
    if pixels.getpixel((ix,iy)):d.point((x,y),fill=(224,240,224,255))
  old=im.copy();new=im.copy()
  # Coefficients A*fog+B*background, saturating at the RGB555 ceiling.
  for dst,a_,b_ in ((old,12,8),(new,4,16)):
   data=[]
   for bg,fg in zip(im.getdata(),fogrgba.getdata()):data.append(tuple(min(248,(f*a_+v*b_)//16)//8*8 for f,v in zip(fg[:3],bg)) if fg[3] else bg)
   dst.putdata(data)
  fogpairs.append((n+' — estudo de transparencia em host',old,new))
 board(fogpairs,'NEVOA — coeficientes 12/8 para 4/16 (estudo; nao emulador)',OUT/'Nevoa_Terra_Marine_Estudo.png')
 (OUT/'renders.json').write_text(json.dumps({'source':'native assets and production C selector; no emulator or sprite screenshot','maps':len(NAMES),'full_map_images':24,'camera_comparison_pairs':len(pairs),'surface_state_comparisons':len(surfaces),'submarine_gone_script_state':True,'fog':'Host coefficient study; runtime pending'},indent=2)+'\n')
 print('Rendered 12 maps, cameras, surface states and scoped fog study.')

if __name__=='__main__':main()
