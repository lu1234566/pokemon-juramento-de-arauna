#!/usr/bin/env python3
"""Independent map, script, encoding and actual-C saved-view validation."""
import argparse,ctypes,json,re,subprocess,tempfile
from pathlib import Path
from PIL import Image
from render_native_map import words,Renderer
from bancos_nativos import resolve_bank
from check_interiors_native_encoding_v1 import pack_tiles,unpack_tiles
ROOT=Path(__file__).resolve().parents[2];BASE='4439f996326bbe457d8a9eacbf2ae4341befa88b'
def check_saved(build,base,old,new):
 banks=list(build['banks'].values());symbols=[b['symbol'] for b in banks]+['AraunaRotaTunelV1','Outside'];outside=len(symbols)-1;code='#include <stdint.h>\ntypedef uint16_t u16;\nstruct Tileset { int identity; };\nstruct MapLayout { const struct Tileset *primaryTileset,*secondaryTileset; };\nstatic struct MapLayout layout;\nstatic struct { const struct MapLayout *mapLayout; } gMapHeader={&layout};\n'+''.join(f'const struct Tileset gTileset_{s}={{{i}}};\n' for i,s in enumerate(symbols))+'#include "src/data/arauna_grutas_saved_view.h"\nstatic const struct Tileset *banks[]={'+','.join('&gTileset_'+s for s in symbols)+'};\nu16 check(int p,int s,u16 v){layout.primaryTileset=banks[p];layout.secondaryTileset=banks[s];return AraunaGrutas_NormalizeSavedBlock(v);}\n';report={'status':'PASS','actual_generated_C_executed':True,'historical_save_imported':False,'banks':{},'maps':{}}
 with tempfile.TemporaryDirectory() as td:
  p=Path(td);(p/'check.c').write_text(code);subprocess.run(['gcc','-shared','-fPIC','-O2','-I',str(ROOT),str(p/'check.c'),'-o',str(p/'check.so')],check=True);fn=ctypes.CDLL(str(p/'check.so')).check;fn.argtypes=[ctypes.c_int,ctypes.c_int,ctypes.c_uint16];fn.restype=ctypes.c_uint16
  cases=[(b['symbol'],(i,outside) if b['kind']=='primary' else (outside,i),b) for i,b in enumerate(banks)]+[('AraunaRotaTunelV1',(outside,len(banks)),None),('Outside',(outside,outside),None)]
  for sym,pair,b in cases:
   for v in range(65536):
    mid=v&1023;expected=v
    if b and (mid<512)==(b['kind']=='primary') and v&0xc00:expected=(v&0xfc00)|b['aliases'].get(str(mid),mid)
    elif sym=='AraunaRotaTunelV1' and mid==0x279 and not v&0xc00:expected=(v&0xfc00)|0x303
    got=fn(*pair,v);assert got==expected,(sym,v);assert got&0xfc00==v&0xfc00;assert fn(*pair,got)==got
   report['banks'][sym]={'words_checked':65536,'flags_preserved':True,'idempotent':True}
  for name in list(build['maps'])+['Route114_FossilManiacsTunnel']:
   m=json.loads((ROOT/'data/maps'/name/'map.json').read_text());l,o=new[m['layout']],old[m['layout']];pair=[symbols.index(l[k][9:]) if l[k][9:] in symbols else outside for k in ('primary_tileset','secondary_tileset')];g,og=words(ROOT/l['blockdata_filepath']),words(base/o['blockdata_filepath']);assert [fn(*pair,v) for v in og]==g,name;report['maps'][name]={'legacy_cache_matches_current_grid':True,'cells':len(g)}
 report['words_checked']=len(cases)*65536;return report

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--base',type=Path,required=True);ap.add_argument('--output',type=Path,default=ROOT/'review/campanha_grutas_v1/validation.json');a=ap.parse_args();base=a.base.resolve();assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=base,text=True).strip()==BASE
 build=json.loads((ROOT/'review/campanha_grutas_v1/build.json').read_text());ol=json.loads((base/'data/layouts/layouts.json').read_text())['layouts'];nl=json.loads((ROOT/'data/layouts/layouts.json').read_text())['layouts'];old={l['id']:l for l in ol};new={l['id']:l for l in nl};assert [l['id'] for l in ol]==[l['id'] for l in nl];owned={d['layout'] for d in build['maps'].values()}
 for l,o in zip(nl,ol):
  if l['id'] in owned:assert {k:v for k,v in l.items() if k not in ('primary_tileset','secondary_tileset')}=={k:v for k,v in o.items() if k not in ('primary_tileset','secondary_tileset')}
  else:assert l==o,l['id']
 names=list(build['maps'])+list(json.loads((ROOT/'review/interiores_rota_v1/build.json').read_text())['maps']);grids={new[json.loads((ROOT/'data/maps'/n/'map.json').read_text())['layout']]['blockdata_filepath'] for n in names};accepted={'data/layouts/layouts.json','src/tileset_anims.c','include/tileset_anims.h','src/fieldmap.c'}|grids|{f'src/data/tilesets/{n}.h' for n in ('graphics','metatiles','headers')}
 for k in ('enigmas','tecnica','tunel'):accepted|={f'data/tilesets/secondary/arauna_rota_{k}_v1/{n}' for n in ('tiles.png','metatiles.bin')}
 protected=0
 for rel in subprocess.check_output(['git','ls-files','data','src','include','graphics'],cwd=base,text=True).splitlines():
  if rel in accepted:continue
  assert (ROOT/rel).read_bytes()==(base/rel).read_bytes(),rel;protected+=1
 for rel in ['src/tileset_anims.c']+[f'src/data/tilesets/{n}.h' for n in ('graphics','metatiles','headers')]:
  text=re.sub(r'\n*// CAMPANHA_GRUTAS_V1_BEGIN\n.*?// CAMPANHA_GRUTAS_V1_END\n','',(ROOT/rel).read_text(),flags=re.S);assert text.rstrip()==(base/rel).read_text().rstrip(),rel
 text=(ROOT/'src/fieldmap.c').read_text().replace('\n\n#include "data/arauna_grutas_saved_view.h"','').replace('AraunaGrutas_NormalizeSavedBlock(*mapView)','*mapView');assert text==(base/'src/fieldmap.c').read_text()
 report={'status':'PASS','base_commit':BASE,'new_maps':13,'V1_regression_maps_checked':25,'layout_indices_preserved':len(ol),'protected_files_identical':protected,'maps':{},'banks':{}};total=remapped=0;labels=dict((n,int(v,16)) for n,v in re.findall(r'#define (METATILE_\w+)\s+(0x[0-9a-fA-F]+)',(ROOT/'include/constants/metatile_labels.h').read_text()))
 for name in names:
  m=json.loads((ROOT/'data/maps'/name/'map.json').read_text());l,o=new[m['layout']],old[m['layout']];g,og=words(ROOT/l['blockdata_filepath']),words(base/o['blockdata_filepath']);assert len(g)==len(og);assert words(ROOT/l['border_filepath'])==words(base/o['border_filepath']);r=Renderer(resolve_bank(ROOT,l['primary_tileset']),resolve_bank(ROOT,l['secondary_tileset']));br=Renderer(resolve_bank(base,o['primary_tileset']),resolve_bank(base,o['secondary_tileset']));attrs=[words(r.primary/'metatile_attributes.bin'),words(r.secondary/'metatile_attributes.bin')];oa=[words(br.primary/'metatile_attributes.bin'),words(br.secondary/'metatile_attributes.bin')];count=0;cache={}
  for v,ov in zip(g,og):
   mid,omid=v&1023,ov&1023;assert v&~1023==ov&~1023;attr=attrs[mid>=512][mid%512];assert attr==oa[omid>=512][omid%512],(name,mid,'behavior/layer');count+=mid!=omid
   if mid not in cache:
    e=(r.primary_metatiles if mid<512 else r.secondary_metatiles)[mid%512*8:][:8];assert len(e)==8
    for entry in e[:4]:t=r._tile(entry&1023);assert t is not None and min(t.getdata())>0,(name,mid,'transparent lower layer')
    assert r.metatile(mid).getextrema()[3]==(255,255);cache[mid]=True
   if name in build['maps'] and not v&0xc00 and attr&255 in (0,8,11,12,33):bank=build['banks'][build['maps'][name]['primary' if mid<512 else 'secondary']];assert bank['roles'][str(mid)]!='solid',(name,mid,'walking ground drawn as wall')
  scriptids=set()
  for token in re.findall(r'^\s*setmetatile\s+[^,]+,\s*[^,]+,\s*([^,\s]+)',(ROOT/'data/maps'/name/'scripts.inc').read_text(),re.M):scriptids.add(labels[token] if token in labels else int(token,0))
  if name in build['maps']:
   for mid in scriptids:bank=build['banks'][build['maps'][name]['primary' if mid<512 else 'secondary']];assert mid in bank['required_ids'];assert r.metatile(mid).getextrema()[3]==(255,255)
  report['maps'][name]={'cells':len(g),'remapped_ids':count,'collision_elevation_behavior_layer_identical':True,'opaque_bottom_layer':True,'script_metatile_ids':sorted(scriptids)};total+=len(g);remapped+=count
 for slug,b in build['banks'].items():
  p=ROOT/b['path'];im=Image.open(p/'tiles.png');raw=pack_tiles(im);assert im.mode=='P' and max(im.getdata())<=15;assert unpack_tiles(raw,im.size)==im.tobytes();assert words(p/'metatile_attributes.bin')[:len(words(ROOT/b['source']/'metatile_attributes.bin'))]==words(ROOT/b['source']/'metatile_attributes.bin')
  for v in words(p/'metatiles.bin'):assert v>>12<=12 and not 432<=v&1023<=511 and not 992<=v&1023<=1023
  assert sorted(x.name for x in (p/'palettes').glob('*.pal'))==[f'{i:02}.pal' for i in range(13)]
  for q in (p/'palettes').glob('*.pal'):assert b'\n' not in q.read_bytes().replace(b'\r\n',b'')
  report['banks'][slug]={'native_4bpp_roundtrip':True,'source_attributes_retained':True,'palettes_0_to_12_CRLF':True,'reserved_VRAM_tiles_unused':True}
 for f in ('victory','seafloor'):
   for k in ('water','waterfall'):frames=[pack_tiles(Image.open(ROOT/f'graphics/tilesets/arauna_grutas_v1/{f}/{k}/{i}.png')) for i in range(8)];assert all(len(x)==128 for x in frames) and len(set(frames))>=4
 for slug in ('enigmas','tecnica','tunel'):
  for v in words(ROOT/f'data/tilesets/secondary/arauna_rota_{slug}_v1/metatiles.bin'):assert v>>12<=12 and not 432<=v&1023<=511 and not 992<=v&1023<=1023
 report.update(cells_checked=total,remapped_ids_checked=remapped,all_map_json_scripts_objects_warps_weather_encounters_identical=True,engine_changed_only_for_scoped_animations_and_legacy_view_normalization=True);sv=check_saved(build,base,old,new);(ROOT/'review/campanha_grutas_v1/saved_view.json').write_text(json.dumps(sv,indent=2)+'\n');report['saved_view_words_checked']=sv['words_checked'];a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({k:v for k,v in report.items() if k not in ('maps','banks')},indent=2))
if __name__=='__main__':main()
