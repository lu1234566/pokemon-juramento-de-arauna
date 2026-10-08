#!/usr/bin/env python3
"""Draw-only Dive atlas and scoped exterior landmarks over installed base 802d."""
import argparse,collections,json,re,subprocess
from pathlib import Path
from PIL import Image
from native_visuals_v2 import Pair,binary,dump,declarations,marked
from dive_04_common import ROOT,BASE,OUT,GROUPS,NAMES,inventory,safe,renderer
from dive_04_art import palettes,floor,stone,decoration,cave_mouth
from build_cavernas_03a import quantize
from render_native_map import words,Renderer
from bancos_nativos import resolve_bank
from script_metatile_dependencies import collect

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--base',type=Path,required=True);a=ap.parse_args();base=a.base.resolve()
 assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=base,text=True).strip()==BASE
 OUT.mkdir(parents=True,exist_ok=True);node,ls,maps=inventory(base);report={'base_commit':BASE,'maps':{},'banks':{},'landmarks':{}}
 labels={k:int(v,16) for k,v in re.findall(r'#define (METATILE_\w+)\s+(0x[\da-fA-F]+)',(base/'include/constants/metatile_labels.h').read_text())}
 tables=[];decl={k:'' for k in ('graphics.h','metatiles.h','headers.h')}
 for theme,group in GROUPS.items():
  first=ls[maps[group[0]]['layout']];p=Pair(base,first);safe(p);p.reserve(base,group,ls,maps)
  p.reserved.update(range(512,512+len(p.attrs[1])))
  for n in group:p.reserved.update(collect(base,n,labels)[0])
  for q,pal in palettes(theme).items():p.pals[q]=pal
  # Recolor inherited detail silhouettes, keeping live kelp entries native.
  used={v&1023 for n in group for field in ('blockdata_filepath','border_filepath') for v in words(base/ls[maps[n]['layout']][field])}
  used.update((542,552));special={513,514,515,548,555,556,557,613,614,615,621,622,623,624}|set(range(736,748))
  native_dynamic=set();source_renderer=renderer(base,first)
  for mid in used:
   if mid==624:continue  # Braille strokes retain their original tile entries.
   entries=p.meta[mid>=512][mid%512*8:mid%512*8+8]
   if any(1008<=e&1023<1012 for e in entries):native_dynamic.add(mid);continue
   im=source_renderer.metatile(mid)
   # Native script substitutions (submarine gone, doors/return) have new art too.
   indexed=quantize(im,p.pals[6],opaque=True)
   if mid==542:indexed=stone('single')
   elif mid==552:indexed=floor(0,True)
   pal=7 if mid==552 else 6
   p.put(mid,indexed,pal)
  for n in group:
   l=ls[maps[n]['layout']];g=words(base/l['blockdata_filepath']);w,h=l['width'],l['height'];vis=[];roles=[]
   at=lambda x,y:g[y*w+x] if 0<=x<w and 0<=y<h else None
   solid=lambda x,y:at(x,y) is not None and bool(at(x,y)&0xc00)
   for i,v in enumerate(g):
    x,y=i%w,i//w;mid=v&1023;role='native_detail'
    if mid in special or mid in native_dynamic:alias=mid;role='native_landmark' if mid in special else 'animated_kelp'
    elif solid(x,y):
     if mid in (680,688,689) and theme=='arquipelago':
      entries=p.entries(floor(0),7)+p.entries(decoration('post'),6)
      alias=p.alias(mid,entries);vis.append(alias);roles.append('ancestral_post');continue
     if not solid(x,y+1):part='lower' if solid(x,y-1) else 'single'
     elif not solid(x,y+2):part='upper'
     elif not solid(x-1,y):part='left'
     elif not solid(x+1,y):part='right'
     else:part='cap'
     im=stone(part);role='mineral_'+part
     if part=='cap' and all(solid(x+dx,y+dy) for dx,dy in ((-2,0),(2,0),(0,-2),(0,2))):
      im=Image.new('L',(16,16),2);role='bedrock'
     entries=p.entries(im,6)+[0]*4;alias=p.alias(mid,entries)
    else:
     attr=p.attrs[mid>=512][mid%512]&255;bright=attr in (0x10,0x11,0x12,0x14,0x15,0x18)
     top=Image.new('L',(16,16));role='silt' if not bright else 'surface_light'
     if bright:top=decoration('light')
     elif n=='Underwater_SealedChamber':top=decoration('masonry');role='buried_archive'
     elif n in ('Underwater_Route126','Underwater_SootopolisCity') and x%11 in (4,5) and y%8 in (3,4):top=decoration('masonry');role='ancestral_paving'
     elif mid in (513,514,515):top=decoration('ruin');role='ruin'
     elif mid in (525,526,527,528,529,536,537):top=decoration('ripples');role='current_silt'
     elif x%7==4 and y%6==3:top=decoration('coral');role='low_coral'
     if solid(x,y-1):
      top=top.copy()
      from PIL import ImageDraw
      ImageDraw.Draw(top).line((0,0,15,1),fill=2)
     entries=p.entries(floor((x//4+y//3)%4,bright),7)+p.entries(top,12 if role=='low_coral' else 6)
     alias=p.alias(mid,entries)
    vis.append(alias);roles.append(role)
   path=OUT/'visual_grids'/f'{n}.bin';binary(path,vis);idx=node['layouts'].index(l);tables.append((n,idx,vis))
   l['secondary_tileset']='gTileset_AraunaDive04'+theme.title()
   report['maps'][n]={'layout_index':idx,'cells':len(g),'theme':theme,'visual_grid':path.relative_to(ROOT).as_posix(),'roles':dict(collections.Counter(roles))}
  path=ROOT/f'data/tilesets/secondary/arauna_dive04_{theme}';p.write([p.paths[0],path],kinds=(1,));symbol='AraunaDive04'+theme.title()
  d=declarations([ROOT/p.paths[0].relative_to(base),path],['General',symbol],p.callbacks)
  for k,body in d.items():decl[k]+=body[body.index('const '+('u32 gTilesetTiles_' if k=='graphics.h' else 'u16 gMetatiles_' if k=='metatiles.h' else 'struct Tileset gTileset_')+symbol):]
  report['banks'][theme]={'path':path.relative_to(ROOT).as_posix(),'source_secondary':p.paths[1].relative_to(base).as_posix(),'new_tiles':sorted(p.touched),'aliases':len(p.alias_cache),'native_dynamic_ids':sorted(native_dynamic),'callbacks':p.callbacks}
 # Altering uses native script IDs 0xA6/0xA7; preserve their complete attributes.
 l=ls[maps['Route103']['layout']];p=Pair(base,l);safe(p);mouth=cave_mouth()
 for row,mid in enumerate((166,167)):p.put(mid,mouth.crop((0,row*16,16,row*16+16)),10)
 p.write([ROOT/p.paths[0].relative_to(base),ROOT/p.paths[1].relative_to(base)])
 # Preserve palette/attribute files byte-for-byte; only native art and new graphics.
 allowed103={p.paths[0].relative_to(base).as_posix()+'/metatiles.bin',p.paths[1].relative_to(base).as_posix()+'/tiles.png'}
 for path in [ROOT/p.paths[0].relative_to(base),ROOT/p.paths[1].relative_to(base)]:
  for f in path.rglob('*'):
   if f.is_file() and f.relative_to(ROOT).as_posix() not in allowed103:f.write_bytes((base/f.relative_to(ROOT)).read_bytes())
 report['landmarks']['altering']={'map':'Route103','native_ids':[166,167],'positions':[[45,5],[45,6]],'new_tiles':sorted(p.touched)}
 # The three base IDs are reused by 363 terrain cells. Allocate camera aliases;
 # do not change the original entries, attributes, stored map or scripts.
 l=ls[maps['Route111']['layout']];p=Pair(base,l);safe(p)
 related=[q for q in node['layouts'] if q['secondary_tileset']==l['secondary_tileset']]
 for q in related:
  for f in ('blockdata_filepath','border_filepath'):p.reserved.update(v&1023 for v in words(base/q[f]))
 p.reserve(base,('Route111',),ls,maps)
 p.reserved.update(json.loads((base/'review/uivo_norte_v1/borders_build.json').read_text())['maps']['Route111']['runtime_visual_ids'])
 # Reserve incoming cache aliases for this receiver bank too.
 hdr=(base/'src/data/arauna_border_uivo_v1.h').read_text()
 for arr in re.findall(r'\{&gTileset_AraunaBorderRoute111ArtUivoV1,.*?,\s*(s\w+),',hdr):
  match=re.search(r'\b'+arr+r'\[\]\s*=\s*\{(.*?)\};',hdr,re.S)
  if match:p.reserved.update(int(v) for v in re.findall(r'\{\d+,\s*(\d+)\}',match[1]))
 original=Renderer(base/'data/tilesets/primary/general',base/'data/tilesets/secondary/mauville');aliases=[]
 for col,mid in enumerate((1008,1009,1010)):
  im=original.metatile(mid);indexed=quantize(im,p.pals[6],opaque=True);entries=p.entries(indexed,6)+[0]*4
  alias=p.alias(mid,entries);aliases.append(alias)
 p.write([ROOT/p.paths[0].relative_to(base),ROOT/p.paths[1].relative_to(base)],kinds=(1,))
 for f in (ROOT/p.paths[1].relative_to(base)/'palettes').glob('*.pal'):f.write_bytes((base/f.relative_to(ROOT)).read_bytes())
 report['landmarks']['mirage']={'native_ids':[1008,1009,1010],'visual_ids':aliases,'layout_indices':[node['layouts'].index(q) for q in related],'positions':[[18,56],[19,56],[20,56]],'new_tiles':sorted(p.touched),'terrain_cells_using_native_ids':sum(v&1023 in (1008,1009,1010) for v in words(base/l['blockdata_filepath']))}
 for k,body in decl.items():marked(ROOT/'src/data/tilesets'/k,'DIVE_04',body)
 dump(ROOT/'data/layouts/layouts.json',node)
 header=(base/'src/data/arauna_cave_visuals_v2.h').read_text();defs=''.join(f'static const u16 sVisual_{n}[] = INCBIN_U16("review/dive_04/visual_grids/{n}.bin");\n' for n,idx,g in tables)
 header=header.replace('static const struct CaveVisualGrid sCaveVisualGrids[] =',defs+'static const struct CaveVisualGrid sCaveVisualGrids[] =');pos=header.rfind('};');header=header[:pos]+''.join(f'    {{{idx}, sVisual_{n}}}, // Dive checkpoint 04\n' for n,idx,g in tables)+header[pos:]
 (ROOT/'src/data/arauna_cave_visuals_v2.h').write_text(header)
 source=(base/'src/arauna_cave_visuals.c').read_text();indices=report['landmarks']['mirage']['layout_indices']
 hook='''    // DIVE_04_LANDMARKS_BEGIN
    // These native IDs also draw ordinary terrain. Only the tower's three
    // base coordinates receive aliases, including its temporary script state.
    if (('''+' || '.join(f'layout == gMapLayouts[{i}]' for i in indices)+''')
     && y == 56 && x >= 18 && x <= 20 && nativeId == 1008 + x - 18)
    {
        static const u16 baseVisuals[] = {'''+','.join(map(str,aliases))+'''};
        return baseVisuals[x - 18];
    }
    // DIVE_04_LANDMARKS_END
'''
 source=source.replace('    index = y * layout->width + x;\n','    index = y * layout->width + x;\n'+hook);(ROOT/'src/arauna_cave_visuals.c').write_text(source)
 fog=(base/'src/field_weather_effect.c').read_text();fog=fog.replace('#include "constants/weather.h"','#include "constants/weather.h"\n#include "constants/maps.h"')
 old='''        if (gWeatherPtr->currWeather == WEATHER_FOG_HORIZONTAL)
            Weather_SetTargetBlendCoeffs(12, 8, 3);'''
 new='''        if (gWeatherPtr->currWeather == WEATHER_FOG_HORIZONTAL)
        {
            // Arauna: thin haze in the two legendary chambers; keep the
            // weather ID, lifecycle and encounter scripts unchanged.
            if ((gSaveBlock1Ptr->location.mapGroup == MAP_GROUP(MAP_TERRA_CAVE_END)
              && gSaveBlock1Ptr->location.mapNum == MAP_NUM(MAP_TERRA_CAVE_END))
             || (gSaveBlock1Ptr->location.mapGroup == MAP_GROUP(MAP_MARINE_CAVE_END)
              && gSaveBlock1Ptr->location.mapNum == MAP_NUM(MAP_MARINE_CAVE_END)))
                Weather_SetTargetBlendCoeffs(4, 16, 3);
            else
                Weather_SetTargetBlendCoeffs(12, 8, 3);
        }'''
 assert fog.count(old)==1;fog=fog.replace(old,new);(ROOT/'src/field_weather_effect.c').write_text(fog)
 dump(OUT/'build.json',report);print(json.dumps({'maps':len(report['maps']),'banks':{k:{'new_tiles':len(b['new_tiles']),'aliases':b['aliases']} for k,b in report['banks'].items()},'landmarks':report['landmarks']},indent=2))

if __name__=='__main__':main()
