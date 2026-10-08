"""Deterministic native pixel motifs; no geometry or behavior is authored here."""
from functools import lru_cache
from PIL import Image,ImageDraw

GROUND=[(0,0,0),(16,32,24),(24,48,32),(32,72,40),(48,104,48),(96,144,88),(120,160,104),(144,176,104),(184,192,128),(72,56,32),(104,80,48),(144,112,64),(176,144,88),(208,184,120),(96,112,80),(184,192,144)]
WOOD=[(0,0,0),(24,24,16),(40,40,24),(64,48,32),(88,64,40),(112,80,48),(136,104,64),(160,128,80),(184,152,96),(208,184,136),(48,72,48),(72,96,56),(96,128,72),(128,152,96),(160,176,128),(224,216,168)]
SHALLOWS=[(0,0,0),(32,56,48),(64,72,48),(88,112,96),(104,144,144),(120,160,152),(152,184,168),(176,160,104),(200,184,128),(72,136,144),(56,120,136),(48,112,128),(40,96,120),(32,80,104),(184,200,168),(224,216,168)]

@lru_cache(None)
def floor(style='ground',variant=0):
 im=Image.new('L',(16,16),5 if style=='ground' else 11 if style=='path' else 7);d=ImageDraw.Draw(im)
 if style=='wood':
  for y in (0,8):
   d.line((0,y,15,y),fill=3);d.line((0,y+1,15,y+1),fill=9)
   seam=4 if y==0 else 12;d.line((seam,y+2,seam,y+7),fill=5)
   d.line((7,y+4,11,y+4),fill=6);d.point((seam+1,y+3),fill=4)
 else:
  for x,y in ((2,3),(10,6),(6,12),(14,14)):
   d.point(((x+variant*3)%16,(y+variant*2)%16),fill=6 if style=='ground' else 12)
  if style=='ground':d.line((10,10,11,9),fill=4)
  else:d.line((3,10,5,10),fill=10)
 return im

@lru_cache(None)
def grass():
 im=floor().copy();d=ImageDraw.Draw(im)
 for x,y in ((2,6),(8,4),(13,8),(5,12),(11,14)):
  d.line((x,y,x-2,y-4),fill=2);d.line((x,y,x+2,y-5),fill=3);d.line((x,y,x,y-6),fill=7)
  d.point((x,y-5),fill=8)
 return im

@lru_cache(None)
def wall(lower=False):
 im=Image.new('L',(16,16),6);d=ImageDraw.Draw(im)
 for x in (0,8):
  d.line((x,0,x,15),fill=4);d.line((x+1,0,x+1,15),fill=8)
 for x,y in ((4,3),(12,10)):d.line((x,y,x+2,y),fill=5)
 y=12 if lower else 0;d.rectangle((0,y,15,y+3),fill=3);d.line((0,y,15,y),fill=8)
 return im

@lru_cache(None)
def pond():
 im=Image.new('L',(16,16),9);d=ImageDraw.Draw(im)
 d.line((1,4,5,4),fill=10);d.line((2,5,4,5),fill=12)
 d.line((10,11,14,11),fill=10);d.point((11,12),fill=12)
 return im

@lru_cache(None)
def shallows():
 im=Image.new('L',(16,16),4);d=ImageDraw.Draw(im)
 d.line((1,3,5,3),fill=6);d.line((10,10,14,10),fill=5)
 d.point((4,12),fill=7);d.line((11,4,12,4),fill=3)
 return im

@lru_cache(None)
def tree_piece(column,row,bottom=False):
 # Broad overlapping crowns occupy exactly the inherited blocked footprint.
 im=Image.new('L',(32,32),0);d=ImageDraw.Draw(im)
 d.ellipse((1,4,30,31),fill=2)
 for x,y,rx,ry in ((10,8,8,7),(21,10,9,7),(7,18,7,8),(22,20,8,8),(15,17,9,9)):
  d.ellipse((x-rx,y-ry,x+rx,y+ry),fill=3)
  d.ellipse((x-rx+1,y-ry,x+rx-2,y+ry-4),fill=4)
  d.ellipse((x-rx+2,y-ry+1,x+rx-4,y+ry-6),fill=5)
  d.arc((x-rx+2,y-ry+1,x+rx-4,y+ry-6),185,300,fill=7)
 for x,y in ((6,6),(16,5),(23,10),(11,12),(5,18),(20,19),(14,22)):
  d.line((x,y,x+2,y),fill=6);d.point((x+1,y-1),fill=7)
 if bottom:
  d.rectangle((13,22,18,31),fill=9);d.line((14,23,14,30),fill=11);d.line((13,30,9,31),fill=9);d.line((17,30,22,31),fill=9)
 piece=im.crop((column*16,row*16,column*16+16,row*16+16));bg=floor().copy();bg.paste(piece,(0,0),piece.point(lambda i:255 if i else 0));return bg

def recolor_palettes(pals,theme):
 out=[list(p) for p in pals]
 for q,pal in enumerate(out):
  for i,(r,g,b) in enumerate(pal):
   if i==0:
    out[q][i]=tuple(c//8*8 for c in (r,g,b));continue
   if theme=='mata':
    if g>r*1.1 and g>b*1.08:r,g,b=int(r*.72),int(g*.78),int(b*.60)
    elif q in (3,9,10,11) and r>=b and g>=b:r,g,b=int(r*.88),int(g*.80),int(b*.65)
    elif q in (0,1,4) and b>r*1.15:r,g,b=int(r*.65),int(g*.85),int(b*.80)
   elif theme=='pouso':
    if q in (0,6,10) and r>=b:r,g,b=min(248,int(r*.94)),int(g*.83),int(b*.64)
   else:
    if g>r and g>b:r,g,b=int(r*.88),int(g*.88),int(b*.80)
   out[q][i]=tuple(max(0,min(248,c))//8*8 for c in (r,g,b))
 return out
