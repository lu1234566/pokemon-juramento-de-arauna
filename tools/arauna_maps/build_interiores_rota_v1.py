#!/usr/bin/env python3
"""New roadside interior artwork; preserve original layout/functional IDs.

Atlas extraction is a production conversion, not a recolour of Emerald.
Objects have a transparent upper layer and an opaque independent floor.
An exclusive primary supplies native PC/TV states without touching other maps.
"""
import json, re, shutil, struct
from pathlib import Path
from PIL import Image, ImageDraw
from bancos_nativos import resolve_bank
from render_native_map import Renderer, words

ROOT=Path(__file__).resolve().parents[2]
BASE='14e56ecd6e9653c67f2ca8a111c8fabdeddd3e2f'
MARK='INTERIORES_ROTA_V1'
ARTDIR=ROOT/'art/interiores_rota_v1'
OUT=ROOT/'review/interiores_rota_v1'
MAPS={
 'Route109_SeashoreHouse':'praia',
 'Route110_SeasideCyclingRoadNorthEntrance':'ciclovia',
 'Route110_SeasideCyclingRoadSouthEntrance':'ciclovia',
 'Route110_TrickHouseEntrance':'oficina',
 'Route110_TrickHouseCorridor':'oficina',
 'Route110_TrickHouseEnd':'oficina',
 **{'Route110_TrickHousePuzzle'+str(i):'enigmas' for i in range(1,9)},
 'Route111_OldLadysRestStop':'pouso',
 'Route111_WinstrateFamilysHouse':'fazenda',
 'Route112_CableCarStation':'estacao',
 'Route113_GlassWorkshop':'vidro',
 'Route114_FossilManiacsHouse':'fosseis',
 'Route114_FossilManiacsTunnel':'tunel',
 'Route114_LanettesHouse':'tecnica',
 'Route116_TunnelersRestHouse':'mineiros',
 'Route121_SafariZoneEntrance':'safari',
 'Route123_BerryMastersHouse':'fazenda',
 'Route124_DivingTreasureHuntersHouse':'mergulho',
}
SOURCES={'praia':'seashore_house','ciclovia':'shop','oficina':'generic_building',
 'enigmas':'trick_house_puzzle','pouso':'generic_building','fazenda':'generic_building',
 'estacao':'facility','vidro':'generic_building','fosseis':'generic_building',
 'tunel':'fallarbor','tecnica':'lab','mineiros':'generic_building',
 'safari':'shop','mergulho':'generic_building'}
NAMES={
 'casas':('wall','window','door','shelf','table','chair','hammock','bed',
          'glassbench','kiln','glasscase','fossilcase','tools','diving','seeds','counter'),
 'oficina':('publicwall','shutter','redgate','bluegate','lever','button','compass','stairs',
            'desk','bikes','notice','turnstile','console','pulley','workstation','fern'),
 'rocha':('rockwall','rockleft','rockright','rockbase','mineentry','support','pillar','boulder',
          'cart','specimens','sandstonefloor','stonefloor','rail','geologybench','supplies','landing'),
}
GROUPS={6:('wall','window','door','shelf','table','chair','hammock','bed','counter','seeds'),
 7:('glassbench','kiln','glasscase','fossilcase','tools','diving','fern'),
 8:tuple(NAMES['oficina'][:-1]),9:tuple(NAMES['rocha'])}
FLOORPAL=[(0,0,0),(0,0,0),(56,32,24),(80,48,32),(112,72,40),(144,96,56),
 (176,128,80),(208,160,104),(232,200,144),(96,112,104),(128,144,128),
 (160,168,144),(184,192,176),(208,216,200),(232,232,208),(248,248,232)]
SIGNALPAL=[(0,0,0),(24,24,24),(56,40,32),(104,72,40),(160,120,64),(216,184,120),
 (240,216,168),(248,240,208),(72,104,112),(112,152,160),(160,192,200),
 (208,224,224),(144,40,40),(208,72,56),(40,88,144),(72,136,192)]

def dump(path,obj):
 path.parent.mkdir(parents=True,exist_ok=True)
 path.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')

def artwork():
 raw={}
 for filename,names in NAMES.items():
  src=Image.open(ARTDIR/(filename+'_atlas.png')).convert('RGBA')
  for i,name in enumerate(names):
   y,x=divmod(i,4);box=(round(x*src.width/4)+10,round(y*src.height/4)+10,
      round((x+1)*src.width/4)-10,round((y+1)*src.height/4)-10)
   im=src.crop(box)
   im.putdata([(r,g,b,0 if r>140 and b>140 and g<130 else 255) for r,g,b,a in im.getdata()])
   assert im.getbbox(),name
   raw[name]=im.crop(im.getbbox())
 pals={11:FLOORPAL,12:SIGNALPAL};art={}
 for slot,names in GROUPS.items():
  samples=[]
  for name in names:
   samples.extend((r,g,b) for r,g,b,a in raw[name].resize((48,48),Image.Resampling.NEAREST).getdata() if a)
  sample=Image.new('RGB',(len(samples),1));sample.putdata(samples)
  colors=sample.quantize(colors=15,method=Image.Quantize.MEDIANCUT).getpalette()[:45]
  colors=[(0,0,0)]+[tuple((v>>3)<<3 for v in colors[j:j+3]) for j in range(0,45,3)]
  pals[slot]=colors
  for name in names:
   im=raw[name];idx=Image.new('L',im.size);pixels=list(im.getdata())
   nearest={rgb:min(range(1,16),key=lambda j:sum((u-v)**2 for u,v in zip(rgb,colors[j]))) for rgb in {(r,g,b) for r,g,b,a in pixels if a}}
   idx.putdata([0 if not a else nearest[(r,g,b)] for r,g,b,a in pixels])
   art[name]=(idx,slot)
 return art,pals

ART,PALS=artwork()

def asset(name,size):
 im,pal=ART[name];return im.resize(size,Image.Resampling.NEAREST),pal

def floor_art(style):
 im=Image.new('L',(16,16),6);d=ImageDraw.Draw(im)
 if style=='tunel':
  im=Image.new('L',(16,16),8);d=ImageDraw.Draw(im)
  d.line((1,5,3,4),fill=7);d.line((10,11,12,11),fill=6)
  d.point((6,13),fill=7);d.point((14,3),fill=6)
 elif style in ('ciclovia','safari','tecnica','estacao'):
  im=Image.new('L',(16,16),11);d=ImageDraw.Draw(im)
  d.rectangle((0,0,15,15),outline=9)
  d.line((1,1,14,1),fill=13);d.line((1,2,1,14),fill=12)
  d.point((4,6),fill=10);d.point((11,12),fill=12)
 elif style=='vidro':
  im=Image.new('L',(16,16),6);d=ImageDraw.Draw(im)
  for x,y,w,h in [(0,0,8,8),(8,0,8,8),(4,8,8,8),(-4,8,8,8),(12,8,8,8)]:
   d.rectangle((x,y,x+w-1,y+h-1),fill=5,outline=3)
   d.line((x+1,y+1,x+w-2,y+1),fill=7)
   d.point((x+3,y+4),fill=6)
 else:
  for y in (0,8):
   d.line((0,y,15,y),fill=3);d.line((0,y+1,15,y+1),fill=7)
   seam=4 if y==0 else 12;d.line((seam,y+1,seam,y+7),fill=4)
   d.line((1,y+4,3,y+4),fill=5);d.line((9,y+6,13,y+6),fill=5)
 assert min(im.getdata())>0
 return im,11

def native(kind,size=(16,16),state=0,direction=0):
 """Small editable indicators, rails and floor variants in native pixels."""
 im=Image.new('L',size,0);d=ImageDraw.Draw(im);w,h=size
 if kind=='mat':
  d.rectangle((0,0,w-1,h-1),fill=3,outline=2)
  for y in range(2,h-2):
   for x in range(2,w-2):
    if (x+y)%6 in (0,1):d.point((x,y),fill=6)
  d.rectangle((1,1,w-2,h-2),outline=5)
 elif kind=='black':im.paste(1,(0,0,w,h))
 elif kind=='arrow':
  d.rectangle((0,0,15,15),fill=3,outline=2);d.rectangle((1,1,14,14),outline=5)
  color=12 if state==0 else 14 if state==1 else 6 if state==2 else 10
  d.polygon([(3,5),(8,5),(8,2),(13,7),(8,12),(8,9),(3,9)],fill=color)
  im=im.rotate([0,270,180,90][direction])
 elif kind=='button':
  d.rectangle((1,1,14,14),fill=3,outline=2);d.ellipse((3,3,12,12),fill=5 if not state else 4,outline=1)
  d.arc((4,4,11,11),180,310,fill=7)
  if state:d.rectangle((6,6,9,9),fill=13)
 elif kind=='lever':
  d.rectangle((2,8,13,14),fill=3,outline=1);d.line((7,11,11 if state else 3,3),fill=5,width=2)
  d.ellipse((9 if state else 1,1,13 if state else 5,5),fill=13 if state else 15,outline=1)
 elif kind=='hole':
  d.ellipse((1,2,w-2,h-2),fill=2,outline=4);d.ellipse((3,4,w-4,h-4),fill=1)
 elif kind=='ice':
  im.paste(10,(0,0,w,h));d=ImageDraw.Draw(im)
  d.line((0,4,4,0),fill=11);d.line((3,h-1,w-1,3),fill=11,width=2)
  d.line((0,h-2,w-3,0),fill=9);d.line((w-6,h-1,w-1,h-6),fill=8)
 elif kind=='rail':
  d.line((3,0,3,15),fill=2,width=2);d.line((12,0,12,15),fill=2,width=2)
  for y in (3,11):d.line((1,y,14,y),fill=4,width=2)
  d.line((3,0,3,15),fill=10);d.line((12,0,12,15),fill=10)
  im=im.rotate(90 if direction else 0)
 elif kind=='rim':
  d.rectangle((0,0,w-1,h-1),fill=3);d.line((0,0,w-1,0),fill=6,width=2)
  for x in range(3,w,8):d.rectangle((x,3,x+1,h-1),fill=2)
 elif kind=='barrier':
  d.rectangle((0,0,w-1,h-1),fill=3)
  for y in (2,12,h-5):d.rectangle((0,y,w-1,y+2),fill=5);d.line((0,y,w-1,y),fill=6)
  for x in (2,w-4):d.rectangle((x,0,x+2,h-1),fill=4);d.line((x,0,x,h-1),fill=6)
  for y in range(18,h-8,6):d.line((5,y,w-6,y),fill=2)
 else:raise ValueError(kind)
 return im,12

class Bank:
 def __init__(self,key,layouts):
  self.key=key;self.src=ROOT/'data/tilesets/secondary'/SOURCES[key]
  self.dst=ROOT/'data/tilesets/secondary'/('arauna_rota_'+key+'_v1')
  self.symbol='AraunaRota'+key.title()+'V1'
  self.attrs=words(self.src/'metatile_attributes.bin');self.meta=[512]*(8*len(self.attrs))
  self.tiles=[bytes(64)];self.cache={bytes(64):512};self.used=set();self.blocked=set();self.drawn=set();self.props=set()
  for l in layouts:
   for field in ('blockdata_filepath','border_filepath'):
    for raw in words(ROOT/l[field]):
     mid=raw&1023
     if mid>=512:
      self.used.add(mid)
      if raw&0xc00:self.blocked.add(mid)
  labels=dict((n,int(v,16)) for n,v in re.findall(r'#define (METATILE_\w+)\s+(0x[0-9a-fA-F]+)',(ROOT/'include/constants/metatile_labels.h').read_text()))
  if key=='enigmas':self.used.update(v for n,v in labels.items() if n.startswith('METATILE_TrickHousePuzzle_'))
  if key=='oficina':self.used.update((0x21b,0x219))
  for name,k in MAPS.items():
   if k!=key:continue
   text=(ROOT/'data/maps'/name/'scripts.inc').read_text()
   for n in re.findall(r'^\s*setmetatile\s+[^,]+,\s*[^,]+,\s*(METATILE_\w+)',text,re.M):
    mid=labels[n]
    if mid>=512:self.used.add(mid)
  self.floor,self.floorpal=floor_art(key)
  for mid in self.used:self.put(mid,self.floor,self.floorpal)

 def tile(self,im):
  p=im.tobytes()
  if p not in self.cache:
   assert len(self.tiles)<480,(self.key,'static tile budget')
   self.cache[p]=512+len(self.tiles);self.tiles.append(p)
  return self.cache[p]

 def entries(self,im,pal):
  return [self.tile(im.crop((x,y,x+8,y+8)))|(pal<<12) for x,y in ((0,0),(8,0),(0,8),(8,8))]

 def put(self,mid,bottom,pal,top=None):
  assert 512<=mid<512+len(self.attrs),(self.key,hex(mid))
  self.meta[(mid-512)*8:(mid-511)*8]=self.entries(bottom,pal)+(self.entries(*top) if top else [512]*4)
  self.drawn.add(mid)

 def module(self,mids,art):
  im,pal=art;assert im.size==(len(mids[0])*16,len(mids)*16)
  for y,row in enumerate(mids):
   for x,mid in enumerate(row):
    if mid is not None:
     self.put(mid,self.floor,self.floorpal,(im.crop((x*16,y*16,x*16+16,y*16+16)),pal));self.props.add(mid)

 def single(self,mid,name):self.module(((mid,),),asset(name,(16,16)))
 def module_asset(self,mids,name):self.module(mids,asset(name,(len(mids[0])*16,len(mids)*16)))

 def generic(self):
  self.module_asset(((0x215,),(0x21d,)),'wall');self.module_asset(((0x217,),(0x21f,)),'window')
  self.module_asset(((0x205,),(0x20d,)),'wall');self.module_asset(((0x206,),(0x20e,)),'window')
  self.module_asset(((0x207,),(0x20f,)),'window')
  self.module_asset(((0x2e3,0x2e4),(0x2eb,0x2ec)),'wall')
  self.module_asset(((0x2ee,),(0x2f6,)),'door')
  self.module_asset(((0x24a,0x24b),(0x252,0x253)),'table')
  self.module_asset(((0x24e,0x24f),(0x256,0x257)),'table')
  self.module_asset(((0x2b9,0x2ba),(0x2c1,0x2c2)),'shelf')
  self.module_asset(((0x2ae,0x2af),(0x2b6,0x2b7)),'shelf')
  self.module_asset(((0x296,0x297),),'counter')
  self.module_asset(((0x2ce,0x2cf),),'counter')
  for mid in (0x244,0x259,0x22a,0x298,0x299,0x264,0x274):self.single(mid,'fern')
  for mid in (0x268,0x2a0):self.single(mid,'counter')
  for mid in (0x2a8,0x270):self.single(mid,'chair')
  self.module(((0x208,0x209),),native('mat',(32,16)))
  self.module(((0x210,0x211),),native('mat',(32,16)))
  self.module_asset(((0x2c6,0x2c7),),'notice')
  self.module_asset(((0x28e,0x28f),),'notice')
  self.module_asset(((0x2d6,),(0x2de,)),'chair')
  k=self.key
  if k=='pouso':
   self.module_asset(((0x240,0x21e),(0x2a1,0x2a9)),'bed')
   self.module_asset(((0x2ae,0x2af),(0x2b6,0x2b7)),'hammock')
  elif k=='fazenda':
   self.module_asset(((0x26c,0x26d),(0x274,0x275)),'seeds')
   self.module_asset(((0x28e,0x28f),),'notice')
   self.single(0x222,'seeds');self.single(0x291,'fern')
  elif k=='vidro':
   self.module_asset(((0x2c6,0x2c7),(0x2ce,0x2cf)),'glasscase')
   self.module_asset(((0x2a0,),(0x2a8,),(0x2b0,)),'kiln')
   self.module_asset(((0x24e,0x24f),(0x256,0x257)),'glassbench');self.single(0x2b3,'glassbench')
  elif k=='fosseis':
   self.module_asset(((0x2ae,0x2af),(0x2b6,0x2b7)),'fossilcase')
   self.module_asset(((0x2b9,0x2ba),(0x2c1,0x2c2)),'specimens')
   self.module_asset(((0x2ee,),(0x2f6,)),'mineentry')
  elif k=='mineiros':
   self.module_asset(((0x2b9,0x2ba),(0x2c1,0x2c2)),'tools')
   self.module_asset(((0x2c6,0x2c7),(0x2ce,0x2cf)),'geologybench')
   self.module_asset(((0x24e,0x24f),(0x256,0x257)),'table')
  elif k=='mergulho':
   self.module_asset(((0x235,0x236,0x237),(0x23d,0x23e,0x23f),(0x245,0x246,0x247)),'diving')
   self.module_asset(((0x279,0x27a),(0x281,0x282)),'shelf')
  elif k=='oficina':
   self.module_asset(((0x21a,),(0x21b,)),'door')
   self.single(0x219,'stairs');self.single(0x20b,'stairs')
   self.module_asset(((0x212,0x213,0x214),),'desk')
   self.module_asset(((0x2c6,0x2c7),(0x2ce,0x2cf)),'workstation')
   self.single(0x2f1,'table')
  for mid in (0x318,0x320,0x31b,0x323):
   self.module(((mid,),),native('rim'))

 def public(self):
  for a,b in ((0x288,0x290),(0x293,0x295)):
   self.module_asset(((a,),(b,)),'publicwall')
  for pair in ((0x259,0x25a),(0x261,0x262),(0x298,0x299)):
   self.module_asset((pair,),'fern' if pair!=(0x298,0x299) else 'desk')
  self.module_asset(((0x28b,),(0x28d,)),'notice')
  self.module_asset(((0x29c,),(0x2a0,),(0x2a8,),(0x2b0,)),'shutter')
  self.module_asset(((0x2a1,),(0x2a9,),(0x2b1,)),'publicwall')
  self.module(((0x216,0x217),),native('mat',(32,16)))
  for mid in (0x264,0x274):self.single(mid,'fern')
  if self.key=='ciclovia':
   self.module_asset(((0x259,0x25a),(0x261,0x262)),'bikes')
   self.single(0x25c,'turnstile')
  else:
   self.module_asset(((0x2c3,0x2c8),(0x2d0,0x2d1)),'desk')
   self.module_asset(((0x265,),(0x2ba,)),'notice')

 def puzzle(self):
  self.module_asset(((0x202,0x203,0x204),(0x20a,0x20b,0x20c)),'publicwall')
  for mid in (0x201,0x209):self.single(mid,'publicwall')
  self.module_asset(((0x211,0x212),),'desk');self.single(0x213,'notice')
  self.single(0x205,'stairs');self.single(0x206,'support')
  self.single(0x20d,'stairs');self.single(0x20e,'support')
  self.module_asset(((0x21e,0x21f),(0x22e,0x22f)),'table')
  self.module_asset(((0x223,0x224,0x225),),'counter')
  self.module_asset(((0x235,0x236),),'counter')
  self.module_asset(((0x26f,),(0x277,)),'door')
  self.single(0x20b,'stairs');self.single(0x26a,'door')
  for group,name in (((0x238,0x239,0x240,0x241),'redgate'),((0x23b,0x23c,0x243,0x244),'bluegate')):
   self.module_asset((group[:2],group[2:]),name)
  for group in ((0x248,0x249,0x250,0x251),(0x24b,0x24c,0x253,0x254)):
   for mid in group:self.put(mid,self.floor,self.floorpal)
  for group,name in (((0x23a,0x242),'redgate'),((0x23d,0x245),'bluegate')):
   # Retracted panel stays in the wall cell, keeping the path clear.
   im,pal=asset(name,(16,32));narrow=Image.new('L',(16,32),0)
   narrow.paste(im.resize((4,32),Image.Resampling.NEAREST),(0,0));self.module(tuple((mid,) for mid in group),(narrow,pal))
  for mid,name in ((0x24a,'redgate'),(0x24d,'bluegate')):self.single(mid,name)
  for mid,state in ((0x258,0),(0x259,1)):self.module(((mid,),),native('button',state=state))
  for mid,state in ((0x23e,0),(0x23f,1)):self.module(((mid,),),native('lever',state=state))
  for mid,direction in ((0x260,0),(0x261,2),(0x262,3),(0x263,1),(0x27b,2),(0x27c,0)):
   self.module(((mid,),),native('arrow',direction=direction))
  for start,state in ((0x298,2),(0x2a0,1),(0x2a8,3),(0x2b0,0)):
   for i in range(4):self.module(((start+i,),),native('arrow',state=state,direction=i))
   self.module(((start+4,),),native('button',state=1))
  for mid in range(0x280,0x295):self.module(((mid,),),native('rail',direction=mid in (0x281,0x282,0x283,0x28a,0x28b,0x28c,0x293,0x294)))
  self.module(((0x287,),),native('button'))
  self.module(((0x268,),),native('hole'))
  for mid in (0x26b,0x26c):self.put(mid,native('ice')[0],12)
  for mid in (0x255,0x252):self.put(mid,self.floor,self.floorpal)

 def redraw(self):
  if self.key in ('oficina','pouso','fazenda','vidro','fosseis','mineiros','mergulho'):self.generic()
  elif self.key in ('ciclovia','safari'):self.public()
  elif self.key=='enigmas':self.puzzle()
  elif self.key=='praia':
   self.module_asset(((0x201,0x202,0x203,0x204,0x205),(0x209,0x20a,0x20b,0x20c,0x20d)),'wall')
   self.module_asset(((0x206,0x207),(0x20e,0x20f)),'window')
   self.module_asset(((0x211,),(0x214,)),'table');self.module_asset(((0x210,),(0x218,)),'counter')
   self.module_asset(((0x216,0x217),(0x222,0x224),(0x22a,0x22c)),'glasscase')
   for mid in (0x212,0x21f,0x227):self.single(mid,'chair')
   self.module_asset(((0x236,0x237),),'glassbench')
  elif self.key=='tecnica':
   self.module_asset(((0x205,0x206,0x207),(0x20a,0x20c,0x210)),'publicwall')
   self.module_asset(((0x218,0x219),(0x22c,0x22d)),'shelf')
   self.module_asset(((0x234,0x235),(0x258,0x259)),'shelf')
   self.module_asset(((0x21a,0x21b),(0x230,0x231),(0x250,0x251)),'workstation')
   self.module_asset(((0x232,),(0x24c,)),'workstation');self.module_asset(((0x212,0x213),),'console')
   self.module_asset(((0x220,0x221),(0x228,0x229)),'table')
   self.module_asset(((0x223,),(0x23a,)),'fern')
   self.module(((0x208,0x209),),native('mat',(32,16)))
  elif self.key=='estacao':
   self.module_asset(((0x218,0x219),(0x220,0x221),(0x2f2,0x2f3)),'publicwall')
   self.module_asset(((0x2f8,),(0x300,)),'window')
   self.module_asset(((0x2f4,0x2f5),),'notice')
   self.module(((0x2f9,),),native('rim'))
   self.module_asset(((0x2fa,),(0x302,),(0x2fb,)),'console')
   self.module_asset(((0x303,),(0x30b,),(0x313,),(0x31b,)),'pulley')
   for col in ((0x308,0x310,0x318,0x320),(0x309,0x311,0x319,0x321),(0x30a,0x312,0x31a,0x322)):
    self.module(tuple((mid,) for mid in col),native('barrier',(16,64)))
   self.module(((0x206,0x207),),native('mat',(32,16)))
  elif self.key=='tunel':
   for mid in (0x268,0x278):self.single(mid,'rockleft')
   for mid in (0x26a,0x27a):self.single(mid,'rockright')
   for mid in (0x269,0x270,0x272,0x22c,0x22d):self.single(mid,'rockwall')
   for mid in (0x2b8,0x2c5,0x2c6):self.single(mid,'rockbase')
   for mid in (0x2af,0x2b7,0x2bf,0x2c7):self.single(mid,'boulder')
   self.module_asset(((0x347,),(0x34f,)),'mineentry')
   self.module_asset(((0x2b1,0x2b2),),'stairs')
   for mid in (0x303,0x304,0x305,0x30b,0x30c,0x314,0x315,0x31c,0x31d,0x31f):
    self.put(mid,self.floor,self.floorpal)

 def save(self,layouts):
  old=Renderer(resolve_bank(ROOT,layouts[0]['primary_tileset']),self.src)
  for mid in self.blocked-self.props:
   self.single(mid,'rockwall' if self.key=='tunel' else 'publicwall' if self.key in ('enigmas','ciclovia','safari','estacao') else 'wall')
  # Preserve outside voids as opaque black, never transparent floor.
  blacks=set();voidcolors=[(0,0,0)];voids=set()
  for mid in self.used:
   im=old.metatile(mid).convert('RGB')
   if not any(im.tobytes()):self.put(mid,native('black')[0],12);blacks.add(mid)
   elif len(set(im.getdata()))==1 and max(im.getpixel((0,0)))<80:
    color=im.getpixel((0,0))
    if color not in voidcolors:voidcolors.append(color)
    self.put(mid,Image.new('L',(16,16),voidcolors.index(color)),10);voids.add(mid)
  self.dst.mkdir(parents=True,exist_ok=True);shutil.copytree(self.src/'palettes',self.dst/'palettes',dirs_exist_ok=True)
  for slot,colors in PALS.items():
   (self.dst/f'palettes/{slot:02}.pal').write_bytes(('JASC-PAL\r\n0100\r\n16\r\n'+''.join('%d %d %d\r\n'%c for c in colors)).encode())
  if voids:
   colors=voidcolors+[(0,0,0)]*(16-len(voidcolors))
   (self.dst/'palettes/10.pal').write_bytes(('JASC-PAL\r\n0100\r\n16\r\n'+''.join('%d %d %d\r\n'%c for c in colors)).encode())
  sheet=Image.new('P',(128,((len(self.tiles)+15)//16)*8));sheet.putpalette([c for i in range(256) for c in (i,i,i)])
  for i,raw in enumerate(self.tiles):sheet.paste(Image.frombytes('L',(8,8),raw),(i%16*8,i//16*8))
  sheet.save(self.dst/'tiles.png',bits=4)
  (self.dst/'metatiles.bin').write_bytes(struct.pack('<%dH'%len(self.meta),*self.meta))
  (self.dst/'metatile_attributes.bin').write_bytes(struct.pack('<%dH'%len(self.attrs),*self.attrs))
  return {'source':str(self.src.relative_to(ROOT)),'symbol':'gTileset_'+self.symbol,'tiles_including_transparent':len(self.tiles),'required_ids':sorted(self.used),'drawn_ids':sorted(self.drawn),'opaque_black_ids':sorted(blacks),'opaque_dark_void_ids':sorted(voids),'opaque_floor_with_transparent_objects':True,'original_tiles_copied':0}

def primary():
 """Scoped PC/TV states with an opaque lower layer, including Safari PC."""
 src=ROOT/'data/tilesets/primary/building';dst=ROOT/'data/tilesets/primary/arauna_rota_base_v1'
 dst.mkdir(parents=True,exist_ok=True);shutil.copytree(src/'palettes',dst/'palettes',dirs_exist_ok=True)
 pals={0:[(0,0,0)]*16,1:PALS[8],2:FLOORPAL,3:SIGNALPAL}
 for slot,colors in pals.items():
  (dst/f'palettes/{slot:02}.pal').write_bytes(('JASC-PAL\r\n0100\r\n16\r\n'+''.join('%d %d %d\r\n'%c for c in colors)).encode())
 attrs=words(src/'metatile_attributes.bin');meta=[0]*(8*len(attrs));tiles=[bytes(64)];cache={bytes(64):0}
 def entries(im,slot):
  out=[]
  for x,y in ((0,0),(8,0),(0,8),(8,8)):
   raw=im.crop((x,y,x+8,y+8)).tobytes()
   if raw not in cache:cache[raw]=len(tiles);tiles.append(raw)
   out.append(cache[raw]|slot<<12)
  return out
 floor,slot=floor_art('safari')
 for mid in range(len(attrs)):meta[mid*8:(mid+1)*8]=entries(floor,2)+[0]*4
 meta[8:16]=entries(Image.new('L',(16,16),1),0)+[0]*4
 for mid in (2,3,4,5):
  device,pal=asset('workstation',(16,16));device=device.copy()
  if mid in (3,5):
   lit=min(range(1,16),key=lambda i:sum((u-v)**2 for u,v in zip(PALS[8][i],(88,144,120))))
   ImageDraw.Draw(device).rectangle((2,3,6,5),fill=lit)
  meta[mid*8:(mid+1)*8]=entries(floor,2)+entries(device,1)
 # IDs 6/7 are not referenced by these maps or runtime states. Keep their
 # attributes and opaque fallback, without carrying unused rug artwork.
 sheet=Image.new('P',(128,((len(tiles)+15)//16)*8));sheet.putpalette([c for i in range(256) for c in (i,i,i)])
 for i,raw in enumerate(tiles):sheet.paste(Image.frombytes('L',(8,8),raw),(i%16*8,i//16*8))
 sheet.save(dst/'tiles.png',bits=4);(dst/'metatiles.bin').write_bytes(struct.pack('<%dH'%len(meta),*meta));(dst/'metatile_attributes.bin').write_bytes(struct.pack('<%dH'%len(attrs),*attrs))
 return dst,'AraunaRotaBaseV1',len(tiles)

def register(banks,pd,ps):
 bodies={f:'' for f in ('graphics.h','metatiles.h','headers.h')}
 registrations=[(pd,ps,False)]+[(b.dst,b.symbol,True) for b in banks.values()]
 for path,s,secondary in registrations:
  p=str(path.relative_to(ROOT))
  bodies['graphics.h']+=f'const u32 gTilesetTiles_{s}[] = INCGFX_U32("{p}/tiles.png", ".4bpp.lz");\nconst u16 gTilesetPalettes_{s}[][16] =\n{{\n'+''.join(f'    INCGFX_U16("{p}/palettes/{i:02}.pal", ".gbapal"),\n' for i in range(16))+'};\n'
  bodies['metatiles.h']+=f'const u16 gMetatiles_{s}[] = INCBIN_U16("{p}/metatiles.bin");\nconst u16 gMetatileAttributes_{s}[] = INCBIN_U16("{p}/metatile_attributes.bin");\n'
  bodies['headers.h']+=f'const struct Tileset gTileset_{s} =\n{{\n    .isCompressed = TRUE,\n    .isSecondary = {"TRUE" if secondary else "FALSE"},\n    .tiles = gTilesetTiles_{s},\n    .palettes = gTilesetPalettes_{s},\n    .metatiles = gMetatiles_{s},\n    .metatileAttributes = gMetatileAttributes_{s},\n    .callback = NULL,\n}};\n'
 for filename,body in bodies.items():
  p=ROOT/'src/data/tilesets'/filename;text=re.sub(r'\n*// '+MARK+r'_BEGIN\n.*?// '+MARK+r'_END\n','',p.read_text(),flags=re.S)
  p.write_text(text.rstrip()+'\n\n// '+MARK+'_BEGIN\n'+body+'// '+MARK+'_END\n')

def main():
 node=json.loads((ROOT/'data/layouts/layouts.json').read_text());ls={l['id']:l for l in node['layouts']};configs={};source={}
 for name,key in MAPS.items():
  m=json.loads((ROOT/'data/maps'/name/'map.json').read_text());l=ls[m['layout']]
  old=dict(l)
  if l['secondary_tileset'].startswith('gTileset_AraunaRota'):
   old['secondary_tileset']='gTileset_'+''.join(part.title() for part in SOURCES[key].split('_'))
   old['primary_tileset']='gTileset_General' if key in ('tunel','estacao') else 'gTileset_Building'
  source[name]=old;configs.setdefault(key,{})[l['id']]=old
 banks={k:Bank(k,list(c.values())) for k,c in configs.items()}
 report={'base_commit':BASE,'maps':{},'banks':{}}
 for key,b in banks.items():b.redraw();report['banks'][key]=b.save(list(configs[key].values()))
 for name,key in MAPS.items():
  l=ls[source[name]['id']]
  l['secondary_tileset']='gTileset_'+banks[key].symbol
  if key not in ('tunel','estacao'):l['primary_tileset']='gTileset_AraunaRotaBaseV1'
  report['maps'][name]={'layout':l['id'],'bank':key,'width':l['width'],'height':l['height'],'source_primary':source[name]['primary_tileset'],'source_secondary':source[name]['secondary_tileset']}
 pd,ps,nt=primary();report['primary']={'symbol':'gTileset_'+ps,'tiles_including_transparent':nt,'opaque_floor_under_PC_states':True}
 dump(ROOT/'data/layouts/layouts.json',node);register(banks,pd,ps);dump(OUT/'build.json',report)
 print(json.dumps({k:v['tiles_including_transparent'] for k,v in report['banks'].items()}))

if __name__=='__main__':main()
