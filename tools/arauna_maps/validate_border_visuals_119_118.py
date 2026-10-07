#!/usr/bin/env python3
"""Compile the actual C selector on the host and audit native/cached cells.

Original banks are kept in the tree; they provide the before image without a
second checkout. Optional --base additionally verifies every map/grid/script
byte and the old layout registry against the installation base.
"""
import argparse
import collections
import ctypes
import json
import re
import subprocess
import tempfile
from pathlib import Path

from bancos_nativos import resolve_bank, bank_words
from build_border_visuals_119_118 import ROOT, CONFIG
from connection_cache import rectangle
from render_native_map import Renderer, words

def compile_selector(folder):
    if (ROOT/'src/data/arauna_border_priority_v2.h').exists():
        from host_visual_selector_v2 import compile_selector as modern
        return modern(folder)
    (folder/'global.h').write_text('''#include <stdint.h>
#include <stddef.h>
typedef uint16_t u16; typedef uint32_t u32; typedef int32_t s32; typedef uint8_t bool8;
struct Tileset {int dummy;};
struct MapLayout {const struct Tileset *primaryTileset; const struct Tileset *secondaryTileset; int width; int height;};
#define ARRAY_COUNT(a) (sizeof(a)/sizeof((a)[0]))
''')
    (folder/'fieldmap.h').write_text('#define MAP_OFFSET 7\n')
    (folder/'bridge.c').write_text('''#include "global.h"
#include "arauna_border_visuals.h"
const struct Tileset gTileset_AraunaRoute119BorderV1 = {119};
const struct Tileset gTileset_AraunaRoute118BorderV1 = {118};
const struct Tileset otherTileset = {0};
u16 test_selector(int map, int x, int y, u16 id) {
    struct MapLayout layout;
    layout.primaryTileset = &otherTileset;
    layout.secondaryTileset = map==119 ? &gTileset_AraunaRoute119BorderV1 : map==118 ? &gTileset_AraunaRoute118BorderV1 : &otherTileset;
    return AraunaBorderVisualMetatile(&layout,x,y,id);
}
''')
    target = folder/'selector.so'
    subprocess.run(['cc','-Wall','-Wextra','-Werror','-shared','-fPIC','-I'+str(folder),'-I'+str(ROOT/'include'),str(ROOT/'src/arauna_border_visuals.c'),str(folder/'bridge.c'),'-o',str(target)],check=True)
    dll = ctypes.CDLL(str(target))
    dll.test_selector.argtypes = [ctypes.c_int]*3+[ctypes.c_uint16]
    dll.test_selector.restype = ctypes.c_uint16
    return dll.test_selector

def compile_connections(folder):
    text=(ROOT/'src/fieldmap.c').read_text()
    functions=[]
    for name in ['FillNorthConnection','FillSouthConnection','FillWestConnection','FillEastConnection']:
        body=re.search(r'static void '+name+r'\([^;{}]*\)\n\{.*?^\}',text,re.S|re.M)
        assert body,name
        functions.append(body[0])
    (folder/'connections.c').write_text('''#include "global.h"
#define MAP_OFFSET 7
struct MapHeader {const struct MapLayout *mapLayout;};
struct {int width; int height;} gBackupMapLayout;
static int *result, count;
static void FillConnection(int x,int y,const struct MapHeader *other,int sx,int sy,int w,int h) {
    int xx,yy; (void)other;
    for(yy=0;yy<h;yy++) for(xx=0;xx<w;xx++) {
        result[count*4]=sx+xx;result[count*4+1]=sy+yy;
        result[count*4+2]=x+xx;result[count*4+3]=y+yy;count++;
    }
}
'''+ '\n'.join(functions)+'''
int test_connection(int dir,int cw,int ch,int pw,int ph,int offset,int *out) {
    struct MapLayout cur={NULL,NULL,cw,ch},src={NULL,NULL,pw,ph};
    struct MapHeader a={&cur},b={&src};
    gBackupMapLayout.width=cw+15;gBackupMapLayout.height=ch+14;
    result=out;count=0;
    if(dir==0)FillNorthConnection(&a,&b,offset);
    if(dir==1)FillSouthConnection(&a,&b,offset);
    if(dir==2)FillWestConnection(&a,&b,offset);
    if(dir==3)FillEastConnection(&a,&b,offset);
    return count;
}
''')
    so=folder/'connections.so'
    subprocess.run(['cc','-Wall','-Wextra','-Werror','-Wno-unused-parameter','-Wno-missing-field-initializers','-shared','-fPIC','-I'+str(folder),str(folder/'connections.c'),'-o',str(so)],check=True)
    dll=ctypes.CDLL(str(so));f=dll.test_connection
    f.argtypes=[ctypes.c_int]*6+[ctypes.POINTER(ctypes.c_int)];f.restype=ctypes.c_int
    return f

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--base',type=Path)
    args = parser.parse_args()
    layouts = {l['id']:l for l in json.loads((ROOT/'data/layouts/layouts.json').read_text())['layouts']}
    maps = {m['id']:m for p in (ROOT/'data/maps').glob('*/map.json') for m in [json.loads(p.read_text())]}
    priority_path=ROOT/'review/grutas_bordas_v2/borders_build.json'
    priority=json.loads(priority_path.read_text()) if priority_path.exists() else {'maps':{},'regions':[]}
    priority_pairs={(r['receiver'],r['source']) for r in priority['regions']}
    banks = {}
    def render(l,before=False):
        secondary = l['secondary_tileset']
        if before:
            for _,(_,original,symbol,_) in CONFIG.items():
                if secondary=='gTileset_'+symbol:secondary=original
        key = (l['primary_tileset'],secondary)
        if key not in banks:banks[key]=Renderer(resolve_bank(ROOT,key[0]),resolve_bank(ROOT,key[1]))
        return banks[key]
    images = {}
    def pixels(r,mid):
        key=(str(r.primary),str(r.secondary),mid)
        if key not in images:
            try:images[key]=r.metatile(mid).tobytes()
            except (IndexError,ValueError):images[key]=None
        return images[key]
    own = {};changed_connections=[];cache_checked=0;exact_target={};checks=0
    with tempfile.TemporaryDirectory(prefix='arauna-border-') as temp:
        selector = compile_selector(Path(temp))
        copier = compile_connections(Path(temp))
        for name in CONFIG:
            m = maps['MAP_'+name.upper()];l=layouts[m['layout']]
            old,new = render(l,True),render(l)
            grid=words(ROOT/l['blockdata_filepath']);w=l['width']
            for i,v in enumerate(grid):
                mid=v&1023;x=i%w+7;y=i//w+7
                assert selector(int(name[5:]),x,y,mid)==mid,(name,'own ID aliased',x,y)
                assert pixels(old,mid)==pixels(new,mid),(name,'own RGB changed',mid)
                assert bank_words(old,mid,True)==bank_words(new,mid,True),(name,'own behavior changed',mid)
            own[name]={'cells':len(grid),'rgb_identical':True,'native_ids_preserved':True,'behavior_identical':True}
        for mapid,m in maps.items():
            if not any(c['direction'] not in ('dive','emerge') for c in m.get('connections') or []):continue
            current=layouts[m['layout']];r=render(current);before=render(current,True)
            receiver=int(m['name'][5:]) if m['name'] in CONFIG else 0
            for c in m.get('connections') or []:
                if c['direction'] in ('dive','emerge'):continue
                if (m['name'],maps[c['map']]['name']) in priority_pairs:continue # audited with all animation frames by validate_grutas_bordas_v2.py
                other=layouts[maps[c['map']]['layout']];donor=render(other);grid=words(ROOT/other['blockdata_filepath'])
                target=(m['name']=='Route119' and maps[c['map']]['name']=='Route118') or (m['name']=='Route118' and maps[c['map']]['name']=='Route119')
                count=before_diff=after_diff=changed=0
                points=rectangle(current['width'],current['height'],other['width'],other['height'],c['offset'],c['direction'])
                buffer=(ctypes.c_int*40000)()
                native_count=copier(['up','down','left','right'].index(c['direction']),current['width'],current['height'],other['width'],other['height'],c['offset'],buffer)
                native_points=[tuple(buffer[i*4:i*4+4]) for i in range(native_count)]
                assert points==[(p[0],p[1]) for p in native_points],('cache rectangle differs from engine',m['name'],c)
                for x,y,gx,gy in native_points:
                    mid=grid[y*other['width']+x]&1023
                    alias=selector(receiver,gx,gy,mid)
                    old,actual,wanted=pixels(before,mid),pixels(r,alias),pixels(donor,mid)
                    if target:
                        assert actual==wanted,(m['name'],'cache RGB mismatch',x,y,mid,alias)
                        assert bank_words(r,alias,True)==bank_words(donor,mid,True)
                        assert bank_words(r,mid,True)==bank_words(donor,mid,True),'Camera must keep native layer type'
                    else:
                        assert alias==mid and actual==old,(m['name'],'unrelated cache changed',c,x,y,mid)
                    before_diff+=old!=wanted;after_diff+=actual!=wanted;changed+=old!=actual;count+=1
                cache_checked+=count
                if changed:changed_connections.append({'receiver':m['name'],'source':maps[c['map']]['name'],'changed_rgb_cells':changed,'different_rgb_before':before_diff,'different_rgb_after':after_diff})
                if target:exact_target[m['name']]={'cells':count,'before_rgb_different':before_diff,'after_rgb_different':after_diff}
        # Test every native ID throughout the owned map and adjacent wrong
        # directions, independently of which IDs today's grid happens to use.
        for receiver,width,height in [(119,40,140),(118,80,20),(0,40,140)]:
            points=[(7,7),(width+6,height+6),(7,0),(0,7),(width+7,7),(width+14,height+6),(-1,147),(47,147),(46,154),(87,0),(47,7)]
            for x,y in points:
                target=(receiver==119 and 0<=x<47 and 147<=y<154) or (receiver==118 and 47<=x<87 and 0<=y<7)
                if target:continue
                for mid in range(1024):
                    assert selector(receiver,x,y,mid)==mid,(receiver,'selector escapes scope',x,y,mid)
                    checks+=1
    base_files=0
    if args.base:
        # Ignore regenerated .inc aggregates; compare every tracked input.
        tracked=subprocess.check_output(['git','ls-files','data/maps','data/layouts'],cwd=ROOT,text=True).splitlines()
        for name in tracked:
            p=ROOT/name
            if p.name=='layouts.json':continue
            original=args.base/p.relative_to(ROOT)
            assert original.is_file() and original.read_bytes()==p.read_bytes(),('map/grid/script changed',p)
            base_files+=1
        assert (ROOT/'src/tileset_anims.c').read_bytes()==(args.base/'src/tileset_anims.c').read_bytes()
        old=json.loads((args.base/'data/layouts/layouts.json').read_text())['layouts']
        assert len(old)==len(layouts)
        for l in old:
            new=dict(layouts[l['id']]);expected=dict(l)
            for name,(_,_,symbol,_) in CONFIG.items():
                m=maps['MAP_'+name.upper()]
                if m['layout']==l['id']:expected['secondary_tileset']='gTileset_'+symbol
            for name,d in priority['maps'].items():
                m=next(m for m in maps.values() if m['name']==name)
                if m['layout']==l['id']:
                    expected['primary_tileset']='gTileset_'+d['symbols'][0]
                    expected['secondary_tileset']='gTileset_'+d['symbols'][1]
            assert new==expected,('unexpected layout edit',l['id'])
    report={'status':'PASS','priority_directions_checked_by_separate_V2_validator':len(priority_pairs),'native_C_selector_compiled_and_checked':True,'engine_Fill_functions_compiled_and_checked':True,'own_maps':own,'all_cache_cells_checked':cache_checked,'exact_target':exact_target,'connections_changed':changed_connections,'connections_worsened':0,'fallback_checks':checks,'unchanged_base_map_files':base_files}
    print(json.dumps(report,indent=2))

if __name__=='__main__':main()
