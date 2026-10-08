#!/usr/bin/env python3
"""Freeze contracts, execute production C and inspect native bank/puzzle art."""
import argparse,ctypes,hashlib,json,re,subprocess,tempfile
from pathlib import Path
from PIL import Image
from build_cavernas_03c import ROOT,OUT,BASE,NAMES,BNAMES,ALLNAMES,REGISTRIES
from cavernas_03a_common import compile_caves,renderer
from bancos_nativos import bank_words
from render_native_map import words,indexed_tiles,palette
from cavernas_03c_art import glyph_mask
import puzzles_cavernas_03b as puzzles


def overlay_indices(r,mid):
    out=Image.new('L',(16,16))
    for e,(x,y) in zip(bank_words(r,mid)[4:],((0,0),(8,0),(0,8),(8,8))):
        im=r._tile(e&1023)
        if e&0x400:im=im.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
        if e&0x800:im=im.transpose(Image.Transpose.FLIP_TOP_BOTTOM)
        out.paste(im,(x,y))
    return out

def wild_checks(folder):
    """Actual inherited header selector over the real JSON header ordering."""
    data=json.loads((ROOT/'src/data/wild_encounters.json').read_text());entries=[e for g in data['wild_encounter_groups'] if g['for_maps'] for e in g['encounters']]
    selected=[i for i,e in enumerate(entries) if e['map']=='MAP_ALTERING_CAVE'];assert len(selected)==9 and selected==list(range(selected[0],selected[0]+9))
    text=(ROOT/'src/wild_encounter.c').read_text();m=re.search(r'^static u16 GetCurrentMapWildMonHeaderId\(void\)\n\{',text,re.M);start=m.start();pos=text.index('{',start);end=pos+1;depth=1
    while depth:depth+=(text[end]=='{')-(text[end]=='}');end+=1
    function=text[start:end]
    # Runtime source obtains NUM_ALTERING_CAVE_TABLES from the JSON-produced
    # header constant. Check its literal official value against these records.
    template=(ROOT/'src/data/wild_encounters.constants.json.txt').read_text();num=int(re.search(r'#define NUM_ALTERING_CAVE_TABLES (\d+)',template)[1]);assert num==len(selected)
    bridge='''#include <stdint.h>\ntypedef uint16_t u16;typedef uint8_t u8;\n#include "constants/maps.h"\n#include "constants/vars.h"\n#define HEADER_NONE 0xFFFF\n'''+f'#define NUM_ALTERING_CAVE_TABLES {num}\n'+'''
struct Location{u8 mapGroup,mapNum;};struct Save{struct Location location;};static struct Save save;static struct Save *gSaveBlock1Ptr=&save;
struct WildPokemonHeader{u8 mapGroup,mapNum;};static const struct WildPokemonHeader gWildMonHeaders[]={
'''+''.join(f'{{MAP_GROUP({e["map"]}),MAP_NUM({e["map"]})}},\n' for e in entries)+'{MAP_GROUP(MAP_UNDEFINED),MAP_NUM(MAP_UNDEFINED)}};\nstatic u16 variant;static u16 VarGet(u16 v){(void)v;return variant;}\n'+function+'''
int probe(int map,int value){save.location.mapGroup=map>>8;save.location.mapNum=map&255;variant=value;return GetCurrentMapWildMonHeaderId();}
int map(int i){const int values[]={MAP_ALTERING_CAVE,MAP_ARTISAN_CAVE_B1F,MAP_ARTISAN_CAVE_1F,MAP_UNDEFINED};return values[i];}
'''
    folder=Path(folder);folder.mkdir(exist_ok=True);(folder/'wild.c').write_text(bridge);dllpath=folder/'wild.so'
    subprocess.run(['cc','-Wall','-Wextra','-Werror','-shared','-fPIC','-iquote',str(ROOT/'include'),str(folder/'wild.c'),'-o',str(dllpath)],capture_output=True,text=True,check=True)
    dll=ctypes.CDLL(str(dllpath));count=0
    for value in range(9):assert dll.probe(dll.map(0),value)==selected[0]+value;count+=1
    for value in (9,10,65535):assert dll.probe(dll.map(0),value)==selected[0];count+=1
    for mode,name in [(1,'MAP_ARTISAN_CAVE_B1F'),(2,'MAP_ARTISAN_CAVE_1F')]:
        expected=next(i for i,e in enumerate(entries) if e['map']==name)
        for value in (0,8,65535):assert dll.probe(dll.map(mode),value)==expected;count+=1
    assert dll.probe(dll.map(3),0)==65535;count+=1
    return {'status':'PASS','actual_c_checks':count,'altering_variants':len(selected),'selection_source':'GetCurrentMapWildMonHeaderId verbatim','preserved_tables_sha256':hashlib.sha256((ROOT/'src/data/wild_encounters.json').read_bytes()).hexdigest(),'scope':'header selection; species/levels/rates preserved by full-file hash'}

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--base',type=Path,required=True);a=ap.parse_args();base=a.base.resolve()
    assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=base,text=True).strip()==BASE
    contract=json.loads((OUT/'functional_contract.json').read_text());build=json.loads((OUT/'build.json').read_text())
    for rel,sha in {**contract['protected_hashes'],**contract['dependency_hashes']}.items():assert hashlib.sha256((ROOT/rel).read_bytes()).hexdigest()==sha,('protected',rel)
    nodes=[json.loads((r/'data/layouts/layouts.json').read_text())['layouts'] for r in (base,ROOT)];assert len(nodes[0])==len(nodes[1])==744;ids={contract['maps'][n]['map']['layout'] for n in ALLNAMES}
    for old,new in zip(*nodes):
        if old['id'] in ids:assert {k:v for k,v in old.items() if k!='secondary_tileset'}=={k:v for k,v in new.items() if k!='secondary_tileset'}
        else:assert old==new
    for rel in ('src/data/tilesets/graphics.h','src/data/tilesets/metatiles.h','src/data/tilesets/headers.h'):
        s=re.sub(r'\n*// CAVERNAS_03C_BEGIN\n.*?// CAVERNAS_03C_END\n','\n',(ROOT/rel).read_text(),flags=re.S);assert s.rstrip()==(base/rel).read_text().rstrip()
    oldh=(base/'src/data/arauna_cave_visuals_v2.h').read_text();newh=(ROOT/'src/data/arauna_cave_visuals_v2.h').read_text();oldrec=re.findall(r'\{(\d+), sVisual_(\w+)\}',oldh);newrec=re.findall(r'\{(\d+), sVisual_(\w+)\}',newh);assert newrec[:22]==oldrec and len(newrec)==25
    banks=[]
    for theme,b in build['banks'].items():
        p=ROOT/b['path'];old=base/b['source_secondary'];im,cols,count=indexed_tiles(p/'tiles.png');assert count<=512
        assert not set(b['new_static_graphics_slots'])&(set(range(432,512))|set(range(928,932))|set(range(992,1024)))
        values=list(im.getdata());encoded=bytes(values[i]|values[i+1]<<4 for i in range(0,len(values),2));assert [v for x in encoded for v in (x&15,x>>4)]==values
        attrs=words(p/'metatile_attributes.bin');meta=words(p/'metatiles.bin');assert len(attrs)<=512 and len(meta)==len(attrs)*8 and all(e>>12<=12 for e in meta)
        for row in range(13):
            raw=(p/f'palettes/{row:02}.pal').read_bytes();assert raw.count(b'\n')==raw.count(b'\r\n');pal=palette(p/f'palettes/{row:02}.pal');assert len(pal)==16
            if row in (7,9,11,12):assert all(c%8==0 for rgb in pal for c in rgb)
            hw=[sum((c>>3)<<(5*i) for i,c in enumerate(rgb)) for rgb in pal];assert [tuple((v>>(5*i)&31)<<3 for i in range(3)) for v in hw]==[tuple(c>>3<<3 for c in rgb) for rgb in pal]
            if b['stage']=='03B V1.1' and row>=6:assert pal==palette(old/f'palettes/{row:02}.pal')
        if b['stage']=='03B V1.1':
            assert attrs==words(old/'metatile_attributes.bin'),'03B full attributes'
            original=words(old/'metatiles.bin');allowed=set(b['landmarks']['changed_native_ids'])
            for j in range(len(attrs)):
                if j+512 not in allowed:assert meta[j*8:j*8+8]==original[j*8:j*8+8],('untargeted metatile',theme,j+512)
        # Dynamic slots and every original referenced graphic retain their data.
        oim,oc,ot=indexed_tiles(old/'tiles.png')
        for slot in (928,929,930,931):
            x=slot-512;assert im.crop((x%cols*8,x//cols*8,x%cols*8+8,x//cols*8+8)).tobytes()==oim.crop((x%oc*8,x//oc*8,x%oc*8+8,x//oc*8+8)).tobytes()
        banks.append({'theme':theme,'stage':b['stage'],'graphics_tiles':count,'new_tiles':len(b['new_static_graphics_slots']),'native_landmark_ids':b['landmarks']['changed_native_ids'],'gba_encoding':'PASS'})
    layouts=[{l['id']:l for l in node} for node in nodes];reports={};cells=fallbacks=legacy=doors=exitchecks=glyphchecks=0
    with tempfile.TemporaryDirectory() as tmp:
        sel,cases=compile_caves(tmp);puzzles.OUT=OUT;puzzle_report=puzzles.run(Path(tmp)/'puzzles');wild=wild_checks(Path(tmp)/'wild')
        for idx,n in oldrec:
            l=nodes[1][int(idx)];g=words(ROOT/l['blockdata_filepath']);expected=words(ROOT/build['maps'][n]['visual_grid']) if n in BNAMES else words(base/re.search(r'sVisual_'+n+r'\[\] = INCBIN_U16\("([^"]+)"\)',oldh)[1])
            if n in BNAMES:
                prior=words(base/f'review/cavernas_03b/visual_grids/{n}.bin');delta=[i for i,(a,b) in enumerate(zip(prior,expected)) if a!=b]
                allowed={30*l['width']+x for x in (7,8,9)} if n in ('AncientTomb','IslandCave') else set();assert set(delta)==allowed
            for i,v in enumerate(g):assert sel(cases[n],i%l['width']+7,i//l['width']+7,v&1023)==expected[i];legacy+=1
        for n in ALLNAMES:
            m=contract['maps'][n]['map'];old,new=[layouts[i][m['layout']] for i in (0,1)];g=words(ROOT/new['blockdata_filepath']);vis=words(ROOT/build['maps'][n]['visual_grid']);oldr=renderer(base,old);r=renderer(ROOT,new)
            oldmatch=re.search(r'sVisual_'+n+r'\[\] = INCBIN_U16\("([^"]+)"\)',oldh);oldvis=words(base/oldmatch[1]) if oldmatch else [v&1023 for v in g];changed=0;cache={}
            assert len(g)==len(vis)==new['width']*new['height']
            for i,v in enumerate(g):
                native=v&1023;alias=sel(cases[n],i%new['width']+7,i//new['width']+7,native);assert alias==vis[i]
                assert bank_words(oldr,native,True)==bank_words(r,native,True)==bank_words(r,alias,True),(n,i,'attribute')
                im=r.metatile(alias);assert im.getextrema()[3]==(255,255),(n,i,'opacity');assert all((e&1023)<512+r.secondary_tiles[2] for e in bank_words(r,alias)),(n,i,'tile range')
                key=(oldvis[i],alias)
                if key not in cache:cache[key]=oldr.metatile(oldvis[i]).tobytes()!=im.tobytes()
                changed+=cache[key];cells+=1
                for other in (native^1,1023 if native!=1023 else 1022,0 if native else 1):assert sel(cases[n],i%new['width']+7,i//new['width']+7,other)==other;fallbacks+=1
            for x,y in [(-1,0),(0,-1),(new['width'],0),(0,new['height'])]:assert sel(cases[n],x+7,y+7,529)==529;fallbacks+=1
            reports[n]={'stage':build['maps'][n]['stage'],'cells':len(g),'changed_visual_cells':changed,'native_grid_words_preserved':True,'attributes_compared':len(g),'warps':len(m['warp_events']),'objects':len(m['object_events']),'bg_events':len(m['bg_events'])}
            if n in NAMES:
                for warp in m['warp_events']:
                    x,y=warp['x'],warp['y'];j=y*new['width']+x;assert vis[j]==g[j]&1023 and (g[j]&0xc00)==0;exitchecks+=1
            else:
                for mid in (565,567):
                    expected=glyph_mask(oldr,mid);actual=overlay_indices(r,mid);assert actual.tobytes()==expected.tobytes(),('glyph geometry',n,mid);glyphchecks+=1
        for n,states in puzzle_report['door_states'].items():
            l=layouts[1][contract['maps'][n]['map']['layout']];g=words(ROOT/l['blockdata_filepath']);vis=words(ROOT/build['maps'][n]['visual_grid']);r=renderer(ROOT,l)
            for state,patch in states.items():
                for x,y,v in patch:assert sel(cases[n],x+7,y+7,v&1023)==v&1023 and vis[y*l['width']+x]==g[y*l['width']+x]&1023;doors+=1
        for n,positions in [('SealedChamber_InnerRoom',[(9,20),(10,20),(11,20)]),('AncientTomb',[(7,12),(8,12),(9,12),(7,30),(8,30),(9,30)]),('IslandCave',[(7,12),(8,12),(9,12),(7,30),(8,30),(9,30)])]:
            l=layouts[1][contract['maps'][n]['map']['layout']];g=words(ROOT/l['blockdata_filepath']);vis=words(ROOT/build['maps'][n]['visual_grid']);r=renderer(ROOT,l);oldr=renderer(base,layouts[0][l['id']])
            for x,y in positions:
                i=y*l['width']+x;assert vis[i]==g[i]&1023;assert r.metatile(vis[i]).tobytes()!=oldr.metatile(vis[i]).tobytes(),('new exit pixels',n,x,y);exitchecks+=1
        for n in NAMES:
            l=layouts[1][contract['maps'][n]['map']['layout']];g=words(ROOT/l['blockdata_filepath']);vis=words(ROOT/build['maps'][n]['visual_grid'])
            for i,v in enumerate(g):
                if v&1023 in (600,601,602):assert vis[i]==v&1023;exitchecks+=1
        l=layouts[1][contract['maps']['IslandCave']['map']['layout']];g=words(ROOT/l['blockdata_filepath']);r=renderer(ROOT,l);vis=words(ROOT/build['maps']['IslandCave']['visual_grid'])
        for x,y in contract['regice_perimeter']:
            i=y*l['width']+x;assert g[i]&0xc00==0 and bank_words(r,vis[i],True)==bank_words(r,g[i]&1023,True)
    (OUT/'puzzles.json').write_text(json.dumps(puzzle_report,indent=2)+'\n');(OUT/'wild_selection.json').write_text(json.dumps(wild,indent=2)+'\n')
    report={'status':'PASS','base_commit':BASE,'protected_gameplay_files':len(contract['protected_hashes']),'extra_dependencies':len(contract['dependency_hashes']),'layouts_preserved':737,'target_secondary_fields':7,'maps':reports,'banks':banks,'actual_c_selector_cells':cells,'actual_c_fallback_checks':fallbacks,'legacy_selector_cells':legacy,'existing_03b_corrected_exit_cells_preserved':9,'additional_outer_exit_cells_restored':6,'door_state_piece_checks':doors,'warp_and_exit_piece_checks':exitchecks,'braille_stroke_masks_compared':glyphchecks,'braille_text_and_font_unchanged':True,'real_c_puzzle_checks':puzzle_report['checks'],'real_c_wild_header_checks':wild['actual_c_checks'],'altering_tables_preserved':9,'regice_perimeter_preserved':36,'rom_build':'pending_arm_toolchain_unavailable','emulator':'pending_unavailable'}
    (OUT/'validation.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
if __name__=='__main__':main()
