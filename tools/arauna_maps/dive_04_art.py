"""Mineral shelves, silt and ruined masonry in indexed 16px metatiles."""
from PIL import Image,ImageDraw
from functools import lru_cache
from build_cavernas_03a import pieces,quantize

COLORS={
 'costa':((24,56,64),(80,112,104),(152,160,120),(80,136,112)),
 'arquipelago':((16,48,64),(72,112,112),(144,176,160),(64,136,120)),
 'mare':((16,40,64),(64,96,120),(136,168,184),(64,112,128)),
 'oceano':((8,24,48),(40,72,104),(104,144,168),(40,96,112)),
 'arquivo':((16,32,48),(56,88,96),(128,152,152),(72,112,104)),
 'horizonte':((8,24,40),(48,72,88),(112,144,160),(48,104,112)),
}

def interpolate(a,b,t):return tuple(int((x+(y-x)*t)//8)*8 for x,y in zip(a,b))

def palettes(theme):
 dark,stone,sand,weed=COLORS[theme]
 rock=[(0,0,0)]+[interpolate(dark,tuple(min(248,c+64) for c in stone),(i-1)/14) for i in range(1,16)]
 floor=[(0,0,0)]+[interpolate(dark,tuple(min(248,c+32) for c in sand),(i-1)/14) for i in range(1,16)]
 flora=[(0,0,0)]+[interpolate(dark,tuple(min(248,c+56) for c in weed),(i-1)/14) for i in range(1,16)]
 # 6/8 are used by the inherited animated kelp. Their index topology stays.
 accent=list(rock)
 accent[10:16]=[(120,80,56),(144,96,64),(168,120,80),(192,144,104),(208,176,128),(224,208,160)]
 return {6:rock,7:floor,8:flora,9:floor,10:rock,11:rock,12:accent}

@lru_cache(maxsize=None)
def floor(variant=0,bright=False):
 im=Image.new('L',(16,16),9 if bright else 7);d=ImageDraw.Draw(im)
 for x,y in ((2,3),(11,6),(5,12)):
  xx=(x+variant*3)%13;yy=(y+variant*4)%14
  d.line((xx,yy,xx+2,yy),fill=8 if bright else 6)
 if variant==3:
  d.line((0,4,4,5,8,5),fill=10);d.line((8,11,12,12,15,12),fill=8)
 return im

@lru_cache(maxsize=None)
def stone(role):
 art=pieces('marine');im=art.get(role,art['cap']).copy()
 im.putdata([v or 3 for v in im.getdata()])
 return im

@lru_cache(maxsize=None)
def decoration(role):
 im=Image.new('L',(16,16));d=ImageDraw.Draw(im)
 if role=='coral':
  for x,y in ((4,13),(10,14)):
   d.line((x,y,x,y-6),fill=10,width=2);d.line((x,y-3,x-3,y-6),fill=12);d.line((x,y-5,x+3,y-8),fill=13)
 elif role=='ruin':
  d.polygon(((2,12),(3,5),(12,4),(14,11)),fill=5);d.line((3,5,12,4,14,5),fill=12)
  d.line((3,8,12,8),fill=3);d.line((7,5,7,7),fill=4);d.line((10,9,10,11),fill=4)
  d.line((2,13,14,13),fill=2)
 elif role=='post':
  d.polygon(((5,12),(5,3),(8,1),(10,3),(10,12)),fill=5);d.line((5,3,8,1,10,3),fill=12);d.line((6,4,6,11),fill=9)
  d.line((3,13,12,13),fill=2);d.line((7,6,10,5),fill=3)
 elif role=='masonry':
  d.line((0,3,15,3),fill=5);d.line((0,12,15,12),fill=5);d.line((6,3,6,11),fill=6);d.line((13,13,13,15),fill=6)
 elif role=='light':
  d.line((3,2,9,2,12,4),fill=13);d.line((1,8,5,8),fill=11);d.line((10,12,15,12),fill=12)
 elif role=='ripples':
  d.line((0,4,5,5,10,5),fill=8);d.line((7,11,12,12,15,12),fill=6)
 return im

def cave_mouth():
 im=Image.new('L',(16,32),5);d=ImageDraw.Draw(im)
 d.polygon(((1,9),(4,3),(9,1),(14,6),(15,17),(14,31),(1,31),(0,18)),fill=9)
 d.line((1,10,4,3,9,1,14,6),fill=7);d.line((1,11,3,12,3,23),fill=6)
 d.polygon(((4,14),(6,10),(10,10),(12,14),(12,30),(4,30)),fill=1)
 d.line((4,14,6,10,10,10,12,14),fill=5);d.line((4,15,4,29),fill=6)
 d.line((5,27,11,27),fill=9);d.line((4,30,12,30),fill=7)
 d.line((9,4,7,7,8,10),fill=6)
 for x,y in ((2,16),(12,8),(2,25),(13,22)):d.line((x,y,x+1,y),fill=7)
 return im
