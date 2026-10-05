#!/usr/bin/env python3
"""Render all 48 native before/after comparisons and stage owned files."""
import hashlib,json,subprocess,math
from PIL import Image,ImageDraw,ImageFont
import build_quatro_interiors_v1 as b
import render_quatro_interiors_native as r
ROOT=b.ROOT;OUT=ROOT.parent/'output';FONT='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
MATERIALS={
 'Campo':'Cinza e pedra clara, carpintaria envelhecida e tecidos verdes; Bíblia p. 8.',
 'Cinza':'Pedra escura, reboco quente, madeira e tecidos terracota; Bíblia p. 8 e concept 05.',
 'Mata':'Tábuas, estrutura de madeira, tecidos e folhagem verdes; Bíblia p. 9.',
 'Baia':'Calçamento claro, cores costeiras, tecidos azuis e molduras; Bíblia p. 9.',
}
LABELS={'BattleTentBattleRoom':'Pavilhão — arena','BattleTentCorridor':'Pavilhão — corredor','BattleTentLobby':'Pavilhão — recepção',
 'CozmosHouse':'Casa do pesquisador','MoveRelearnersHouse':'Casa dos movimentos','House':'Casa residencial','HerbShop':'Ervanaria',
 'Gym_1F':'Casa termal — térreo','Gym_B1F':'Casa termal — inferior','Gym':'Casa do Ar','Mart':'Venda local',
 'PokemonCenter_1F':'Centro — térreo','PokemonCenter_2F':'Centro — conexão','DecorationShop':'Venda de artesanato',
 'ContestHall':'Pavilhão — salões','ContestLobby':'Pavilhão — recepção','CoveLilyMotel_1F':'Pousada — térreo','CoveLilyMotel_2F':'Pousada — superior',
 'DepartmentStoreElevator':'Loja — elevador','DepartmentStoreRooftop':'Loja — terraço','Harbor':'Cais e embarque',
 'LilycoveMuseum_1F':'Museu — térreo','LilycoveMuseum_2F':'Museu — exposição','MoveDeletersHouse':'Casa dos movimentos',
 'PokemonTrainerFanClub':'Clube comunitário','UnusedMart':'Venda legada (UnusedMart)'}
def label(name):
 tail=name.split('_',1)[1]
 if tail.startswith('House'):return 'Casa residencial '+tail.removeprefix('House')
 if tail.startswith('DepartmentStore_'):return 'Loja — piso '+tail.split('_')[1]
 return LABELS.get(tail,tail)
def main():
 OUT.mkdir(exist_ok=True);layouts={l['id']:l for l in json.loads((ROOT/'data/layouts/layouts.json').read_text())['layouts']}
 geometry=json.loads((b.OUT/'geometry.json').read_text())['maps']
 for prefix,(city,title,count) in b.CITIES.items():
  names=[name for name in b.NAMES if name.startswith(prefix+'_')];rows=math.ceil(count/4)
  height=330+rows*370+110;canvas=Image.new('RGB',(2400,height),'#202b30');draw=ImageDraw.Draw(canvas)
  def text(x,y,s,size=21):draw.multiline_text((x,y),s,font=ImageFont.truetype(FONT,size),fill='#e8e2d2',spacing=10)
  text(30,22,title.upper()+' • '+str(count)+' INTERIORES V1',36)
  text(30,100,MATERIALS[city],25)
  text(30,160,'Geometria, eventos, scripts, atributos e IDs de serviço preservados.\nReferências de materiais; não há concept individual destes interiores no conjunto recuperado.',22)
  for i,name in enumerate(names):
   event=json.loads((ROOT/'data/maps'/name/'map.json').read_text());before=json.loads(subprocess.check_output(['git','show','HEAD:data/maps/'+name+'/map.json'],cwd=ROOT))
   x=20+i%4*595;y=300+i//4*370;draw.rounded_rectangle((x,y,x+578,y+354),radius=10,fill='#2b373a')
   text(x+12,y+8,label(name),22);text(x+12,y+45,'Antes',17);text(x+300,y+45,'Depois',17)
   for shift,mapdata,isbefore in ((12,before,True),(300,event,False)):
    l=layouts[mapdata['layout']];im=r.render_map(r.Renderer(r.resolve_tileset(l['primary_tileset']),r.resolve_tileset(l['secondary_tileset'])),ROOT/l['blockdata_filepath'],l['width'],l['height'])
    if not isbefore:im.save(b.OUT/(name+'_native.png'));r.add_event_overlay(im,event).save(b.OUT/(name+'_events.png'))
    factor=min(265/im.width,260/im.height);im=im.resize((round(im.width*factor),round(im.height*factor)),Image.Resampling.NEAREST);canvas.paste(im,(x+shift,y+80))
  text(30,height-92,f"{sum(geometry[n]['warps'] for n in names)} warps • {sum(geometry[n]['objects'] for n in names)} objetos • gráficos nativos de 16 cores.",24)
  text(30,height-48,'Compilação de ROM e execução em emulador pendentes.',20)
  canvas.save(OUT/(city.lower()+'_interiors_v1_comparacao.png'))
 new=[]
 for symbol in b.SPECS:new.extend(str(p.relative_to(ROOT)) for p in b.target(symbol).rglob('*') if p.is_file())
 for name in b.NAMES:new.extend(str(p.relative_to(ROOT)) for p in (ROOT/'data/layouts'/(name+'_Arauna')).rglob('*') if p.is_file())
 new+=['docs/QUATRO_INTERIORS_V1.md','docs/ADAPTACAO_INTERIORES_STATUS_86_2026_10_04.md',
        'review/quatro_interiors_v1/manifest.json','review/quatro_interiors_v1/geometry.json',
        'review/quatro_interiors_v1/Casa_da_Cinza_concept.png',
        'tools/arauna_maps/build_quatro_interiors_review_v1.py','tools/arauna_maps/render_quatro_interiors_native.py']
 new+=[f'tools/arauna_maps/{kind}_quatro_interiors_v1.py' for kind in ('apply','build','validate','package')]
 b.dump(b.OUT/'manifest.json',{'new_files':sorted(new),'new_layout_ids':[b.layout_id(n) for n in b.NAMES],
      'map_baselines':{'data/maps/'+n+'/map.json':hashlib.sha256(subprocess.check_output(['git','show','HEAD:data/maps/'+n+'/map.json'],cwd=ROOT)).hexdigest() for n in b.NAMES}})
if __name__=='__main__':main()
