import sys,json,subprocess
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
root=Path(__file__).resolve().parents[2];sys.path.insert(0,str(root/'tools/arauna_maps'))
import build_vale_interiors_v1 as b,render_vale_interiors_native as r
out=root.parent/'output';layouts={x['id']:x for x in json.loads(b.LAYOUTS.read_text())['layouts']}
font='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
canvas=Image.new('RGB',(1890,1320),'#202b30');draw=ImageDraw.Draw(canvas)
def text(x,y,s,size=18,color='#e8e2d2'):draw.text((x,y),s,font=ImageFont.truetype(font,size),fill=color)
text(30,20,'VALE DO SILÊNCIO • NOVE INTERIORES V1',32)
text(30,70,'Direção: Bíblia p. 7 — assentamento entre serras, jardins e pausa contemplativa.',22)
text(30,106,'Materiais domésticos nativos de Arauna. Sem concept interno dedicado no pacote recuperado.',18)
labels=('Casa residencial','Casa dos vínculos','Casa de Wanda e Val','Venda local','Centro — térreo','Centro — conexão','Pavilhão — recepção','Pavilhão — corredor','Pavilhão — arena')
for i,(name,label) in enumerate(zip(b.NAMES,labels)):
 m=json.loads((root/'data/maps'/name/'map.json').read_text());baseline=json.loads(subprocess.check_output(['git','show','HEAD:data/maps/'+name+'/map.json'],cwd=root))
 x=25+(i%3)*625;y=165+(i//3)*345
 draw.rounded_rectangle((x-5,y-5,x+605,y+323),radius=10,fill='#2b373a')
 text(x+12,y+4,label,22);text(x+12,y+39,'Antes',16);text(x+305,y+39,'Depois',16)
 for shift,event,before in ((12,baseline,True),(305,m,False)):
  l=layouts[event['layout']];im=r.render_map(r.Renderer(r.resolve_tileset(l['primary_tileset']),r.resolve_tileset(l['secondary_tileset'])),root/l['blockdata_filepath'],l['width'],l['height'])
  if not before:
   im.save(b.OUT/(name+'_native.png'));r.add_event_overlay(im,m).save(b.OUT/(name+'_events.png'))
  scale=min(275/im.width,220/im.height);im=im.resize((round(im.width*scale),round(im.height*scale)),Image.Resampling.NEAREST)
  canvas.paste(im,(x+shift,y+70))
text(30,1220,'16 warps • 31 objetos • PC, balcão, escadas e percursos de cena verificados.',21)
text(30,1265,'Prévia dos dados nativos. Compilação de ROM e testes em emulador pendentes.',18)
canvas.save(out/'vale_interiors_v1_9_ambientes.png')
new=[]
for rel in ('data/tilesets/secondary/arauna_vale_interiors_v1','data/tilesets/secondary/arauna_vale_pavilhao'):
 new.extend(str(p.relative_to(root)) for p in (root/rel).rglob('*') if p.is_file())
for name in b.NAMES:
 new.extend(str(p.relative_to(root)) for p in (root/'data/layouts'/(name+'_Arauna')).rglob('*') if p.is_file())
new+=['docs/ADAPTACAO_INTERIORES_STATUS_2026_10_04.md','tools/arauna_maps/build_vale_interiors_review_v1.py','art/arauna_vale_interiors_v1/source_atlas.png','docs/VALE_INTERIORS_V1.md','review/vale_interiors_v1/manifest.json','review/vale_interiors_v1/geometry.json']+[f'tools/arauna_maps/{action}_vale_interiors_v1.py' for action in ('build','apply','validate','package')]
for rel in ('tools/arauna_maps/render_vale_interiors_native.py',):
 if subprocess.run(['git','cat-file','-e','HEAD:'+rel],cwd=root,capture_output=True).returncode:new.append(rel)
import hashlib
meta={'new_files':sorted(new),'map_baselines':{'data/maps/'+name+'/map.json':hashlib.sha256(subprocess.check_output(['git','show','HEAD:data/maps/'+name+'/map.json'],cwd=root)).hexdigest() for name in b.NAMES},'new_layout_ids':[b.layout_id(name) for name in b.NAMES]}
(b.OUT/'manifest.json').write_text(json.dumps(meta,indent=2)+'\n')
