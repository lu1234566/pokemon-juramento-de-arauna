#!/usr/bin/env python3
"""Special islands: private native art with unchanged legendary mechanics."""
import argparse
import json
import re
import subprocess
from PIL import Image, ImageDraw, ImageFont
from native_visuals_v2 import Pair, ROOT, declarations, dump, marked
from render_native_map import words, Renderer, indexed_tiles
from trainer_hill_06a_art import native_layers
from validate_grutas_bordas_v2 import animated
from desert_08b1 import sha

BASE = '72b72497acecfec8a14be009c9bebff3d2621877'
PREVIOUS = '5c8f309fd153b707e47a47d2f72780ac12ea0210'
INTEGRATED = 'a594b3e1e64517421101d96f5b314df22d47e14f'
MAIN = '979fb6c1b6731561f3c993efd6045a9bbf096c54'
NAMES = ('SouthernIsland_Exterior','SouthernIsland_Interior','BirthIsland_Exterior',
         'BirthIsland_Harbor','FarawayIsland_Entrance','FarawayIsland_Interior')
OUT = ROOT/'review/islands_08d'
TAG = 'SPECIAL_ISLANDS_08D'
MUTABLE = {'data/layouts/layouts.json', *('src/data/tilesets/'+n for n in ('graphics.h','metatiles.h','headers.h'))}
FIXES = {
 'src/party_menu.c':'e05f9efb61cfd652e56a361ba1e8b826f614abc0e684438a0b031b036679d08f',
 'src/field_player_avatar.c':'81ebe4b5761f8992cb459cf37978262358231734a1c56f8b3447346f770db95f',
 'src/scrcmd.c':'98cd4b72474c3cc7dfd5dc6cf54a4a96f807733017761a2be58d62b0dcd063a9',
 'data/maps/SlateportCity_Harbor/scripts.inc':'fc256e12cb37712c2a2b3e026d442e6baa55ed6560909e7cadecda83c19167ea',
 'data/maps/LilycoveCity_Harbor/scripts.inc':'46ab224e74a02b311a9a38b0eb8f940b169e9e5d83844283ccda00be39ebd18c',
 'data/maps/FallarborTown_CozmosHouse/scripts.inc':'798dc439a26a33d0845646eab56d599d7712e34414c712304d834ae4eb89f4a6',
 'data/maps/Route116/scripts.inc':'cd955b92f802f347645b82cc1bc54aa1715d35097009f7504ec98079c46a62c5'}
GROUPS = {
 'southern': {'names':NAMES[:2], 'suffix':'Southern', 'style':'granite'},
 'birth': {'names':NAMES[2:3], 'suffix':'Birth', 'style':'basalt'},
 'harbor': {'names':NAMES[3:4], 'suffix':'IslandHarbor', 'style':'harbor'},
 'faraway_entrance': {'names':NAMES[4:5], 'suffix':'FarawayCoast', 'style':'tropical'},
 'faraway_interior': {'names':NAMES[5:], 'suffix':'FarawayForest', 'style':'tropical'}}
# Three logical island checkpoints, five independent bank pairs. Separate
# Faraway banks retain Rustboro and Fortree's native secondary definitions.
CHECKPOINTS = {'08D1':NAMES[:2], '08D2':NAMES[2:4], '08D3':NAMES[4:]}
PALETTES = {
 'granite':[(0,0,0),(24,40,40),(32,72,48),(48,104,64),(80,136,80),(120,160,104),(176,200,144),
            (56,64,64),(88,96,96),(128,144,144),(48,40,32),(88,64,40),(144,112,64),(200,168,112),(216,216,184),(240,232,208)],
 'basalt': [(0,0,0),(24,32,40),(40,72,48),(64,112,56),(96,144,72),(144,176,88),(192,200,128),
            (48,48,56),(80,80,88),(128,128,136),(64,48,40),(112,88,64),(160,128,88),(200,168,112),(208,208,192),(240,232,208)],
 'harbor': [(0,0,0),(24,40,48),(40,72,72),(56,96,96),(88,128,128),(136,168,160),(184,208,192),
            (64,72,72),(112,120,112),(168,176,152),(56,40,32),(96,64,40),(152,112,64),(208,168,104),(200,216,200),(240,232,208)],
 'tropical':[(0,0,0),(16,40,40),(24,72,48),(40,104,64),(64,136,72),(104,168,88),(160,200,120),
             (48,56,64),(80,96,96),(128,152,144),(48,40,32),(96,64,40),(144,104,64),(192,144,96),(200,216,168),(232,232,200)]}
# Cut produces these native IDs even when they are absent from the initial
# map. Keep each new-state picture consistent with the base and vegetation.
CUT_IDS = {1,0xe,0xd,0x25,0x1c6,0x1c7,0x1ce,0x1cf,0x208,
           0x279,0x27a,0x27b,0x281,0x282,0x283}


def inventory():
    node=json.loads((ROOT/'data/layouts/layouts.json').read_text())
    ls={l['id']:l for l in node['layouts']}
    ms={n:json.loads((ROOT/f'data/maps/{n}/map.json').read_text()) for n in NAMES}
    return node,ls,ms


def reserve_dma(p):
    if p.callbacks[1]=='InitTilesetAnim_Rustboro':p.dynamic.update(range(640,672));p.dynamic.update(range(960,964))
    if p.callbacks[1]=='InitTilesetAnim_Dewford':p.dynamic.update(range(682,688))
    p.free=[i for i in p.free if i not in p.dynamic]
    p.tile_cache={raw:i for i,raw in p.tiles.items() if i not in p.dynamic and i not in p.free}
    return p


def freeze():
    assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()==BASE
    for n,h in FIXES.items():assert sha((ROOT/n).read_bytes())==h,n
    node,ls,ms=inventory()
    tracked=subprocess.check_output(['git','ls-files','-z'],cwd=ROOT).decode().rstrip('\0').split('\0')
    audit=json.loads((ROOT/'review/cavernas_fundo_mar_v1/recovery_audit.json').read_text())
    bible=ROOT/'docs/referencias/bible_concepts_recuperados/Arauna_Master_Map_Design_Bible.pdf'
    assert sha(bible.read_bytes())==audit['bible_sha256']
    provenance=json.loads((ROOT/'review/cavernas_fundo_mar_v1/concept_provenance.json').read_text())
    concepts={p['canonical_copy']:p['sha256'] for p in provenance}
    for n,h in concepts.items():assert sha((bible.parent/'concepts'/n).read_bytes())==h,n
    assert len(concepts)==82
    c={'base_commit':BASE,'previous_checkpoint':PREVIOUS,'protected_fixes':FIXES,
       'protected_hashes':{n:sha((ROOT/n).read_bytes()) for n in tracked if n not in MUTABLE},
       'registry_hashes':{n:sha((ROOT/n).read_bytes()) for n in sorted(MUTABLE)},
       'layout_ids':[l['id'] for l in node['layouts']],
       'maps':{n:{'map':ms[n],'layout':ls[ms[n]['layout']]} for n in NAMES},
       'references':{'bible_sha256':audit['bible_sha256'],'verified_unique_concepts':82,
                     'design':'coastal stone and forest: Bible routes 124–126 and tropical routes 118–123'},
       'scope':'All prior tracked files except four additive graphics registries; historical contracts stay unchanged.'}
    path=OUT/'functional_contract.json'
    if path.exists():assert json.loads(path.read_text())==c,'Refusing changed contract'
    else:dump(path,c)
    print('Frozen',len(c['protected_hashes']),'files, seven fixes and 82 verified concepts')


def ground(style):
    im=Image.new('L',(8,8),8 if style=='basalt' else 3)
    d=ImageDraw.Draw(im)
    for x,y in ((1,2),(5,6)):d.point((x,y),fill=9 if style=='basalt' else 4)
    if style=='basalt':d.line((3,4,4,4),fill=7)
    return im


def classify(rgb,style,mid):
    r,g,b=rgb;lum=(r+g+b)//3
    if max(rgb)<40:return 1
    if style in ('granite','tropical') and mid in (0x55,0x56,0x5d,0x5e,0x5f,0x70,0x71,0x73,0x74,0x75,0x285):
        return 10 if lum<80 else 11 if lum<130 else 12 if lum<190 else 13
    green=g>r*1.05 and g>b*1.02
    if green:
        if style=='basalt' and mid in (0x334,0x335):
            return 2 if lum<100 else 3 if lum<175 else 4
        if style=='basalt' and mid not in range(0x328,0x336):
            return 7 if lum<105 else 8 if lum<160 else 9 if lum<200 else 14
        return 2 if lum<75 else 3 if lum<110 else 4 if lum<150 else 5 if lum<190 else 6
    if r>b*1.15 and g>b*1.04:
        if style in ('granite','basalt') and (0x6b<=mid<=0x7d or mid in (0xaf,0xbe)):
            return 7 if lum<90 else 8 if lum<140 else 9 if lum<190 else 14
        return 10 if lum<85 else 11 if lum<130 else 12 if lum<180 else 13
    if style!='basalt' and mid in range(0x350,0x35e):
        return 10 if lum<80 else 11 if lum<140 else 12 if lum<195 else 13
    return 7 if lum<85 else 8 if lum<135 else 9 if lum<190 else 14 if lum<225 else 15


def draw_surface(native,style,mid,layer):
    im=Image.new('L',(16,16))
    for y in range(16):
        for x in range(16):
            r,g,b,a=native.getpixel((x,y))
            if not a:continue
            v=classify((r,g,b),style,mid)
            # New leaf clusters and veins replace the native bright stipple.
            # Contours and layer masks remain exact for actors and boundaries.
            if layer==1 and v in (4,5,6) and (x%8,y%8) in ((2,3),(3,3),(6,6)):
                v=max(2,v-1)
            # Wood grain on landing platforms and weathered harbor walls.
            if v in (12,13) and style!='basalt' and y%8==4 and x%8 in (2,3,4):v=11
            im.putpixel((x,y),v)
    return im


def build():
    c=json.loads((OUT/'functional_contract.json').read_text())
    for rel,h in c['protected_hashes'].items():assert sha((ROOT/rel).read_bytes())==h,rel
    node,ls,ms=inventory();report={'base_commit':BASE,'protected_fixes':FIXES,'groups':{},'maps':{}}
    bodies={k:'' for k in ('graphics.h','metatiles.h','headers.h')}
    for key,g in GROUPS.items():
        p=reserve_dma(Pair(ROOT,c['maps'][g['names'][0]]['layout']))
        assert not any(e>>12==12 and e&1023 for a in p.meta for e in a),'Palette 12 already used'
        p.pals[12]=PALETTES[g['style']]
        ids={v&1023 for n in g['names'] for k in ('blockdata_filepath','border_filepath') for v in words(ROOT/c['maps'][n]['layout'][k])}
        runtime=CUT_IDS if key=='faraway_interior' else {1,0xe,0xd,0x25,0x1c6,0x1c7,0x1ce,0x1cf} if key in ('southern','faraway_entrance') else set()
        ids=sorted(ids|runtime);redrawn=[];static_water=[]
        floor_bindings={}
        for e in p.meta[0][8:12]:
            if e&1023:floor_bindings[(e&1023,e>>12)]=ground(g['style'])
        for mid in ids:
            original=p.meta[mid>=512][mid%512*8:mid%512*8+8]
            assert len(original)==8,hex(mid)
            # Water and puddles retain native 8-frame shoreline quarters,
            # palette, reflection behavior and the transition to Surf.
            if p.attrs[mid>=512][mid%512]&255 in (0x15,0x16):continue
            result=[]
            for layer,native in enumerate(native_layers(p.reader,mid)):
                art=draw_surface(native,g['style'],mid,layer)
                for q,(dx,dy) in enumerate(((0,0),(8,0),(0,8),(8,8))):
                    e=original[layer*4+q];t=e&1023
                    if t in p.dynamic:result.append(e);continue
                    # Dock corners also contain static sea quarters with
                    # palette 3. Keep the entire native quarter, including
                    # its post silhouette, so it meets the animated sea.
                    if e>>12==3:
                        colors=[p.pals[3][v] for v in p.reader._tile(t).tobytes()]
                        if sum(b>r+24 and b>g+16 for r,g,b in colors)>8:
                            result.append(e);static_water.append({'mid':mid,'quarter':layer*4+q,'word':e});continue
                    patch=floor_bindings.get((t,e>>12))
                    if patch is not None:
                        for y in range(8):
                            for x in range(8):
                                if native.getpixel((dx+x,dy+y))[3]:art.putpixel((dx+x,dy+y),patch.getpixel((x,y)))
                    result.append(p.tile(art.crop((dx,dy,dx+8,dy+8)))|12<<12)
            p.meta[mid>=512][mid%512*8:mid%512*8+8]=result;redrawn.append(mid)
        paths=[ROOT/'data/tilesets'/kind/('arauna_islands08d_'+key) for kind in ('primary','secondary')]
        symbols=['AraunaIslands08D'+g['suffix']+'Primary','AraunaIslands08D'+g['suffix']]
        p.write(paths)
        for field,body in declarations(paths,symbols,p.callbacks).items():bodies[field]+=body
        report['groups'][key]={'names':list(g['names']),'style':g['style'],'active_and_runtime_ids':ids,'runtime_ids':sorted(runtime),
            'redrawn_ids':redrawn,'new_graphics_slots':sorted(p.touched),'reserved_dma_slots':sorted(p.dynamic),
            'preserved_static_sea_quarters':static_water,
            'callbacks':p.callbacks,'banks':[str(path.relative_to(ROOT)) for path in paths]}
        for n in g['names']:
            l=ls[ms[n]['layout']];l['primary_tileset'],l['secondary_tileset']=['gTileset_'+s for s in symbols]
            report['maps'][n]={'width':l['width'],'height':l['height'],'cells':l['width']*l['height'],'group':key}
        dump(OUT/('checkpoint_'+key+'.json'),{'status':'ART_BUILT','group':key,**report['groups'][key]})
        print(key,len(redrawn),'redrawn IDs;',len(p.touched),'safe new graphics slots')
    for key,body in bodies.items():marked(ROOT/'src/data/tilesets'/key,TAG,body)
    dump(ROOT/'data/layouts/layouts.json',node);dump(OUT/'build.json',report)


def renderer(layout,frame=0):
    from bancos_nativos import resolve_bank
    from native_visuals_v2 import callback
    r=animated(Renderer(*[resolve_bank(ROOT,layout[k]) for k in ('primary_tileset','secondary_tileset')]),ROOT,frame)
    secondary=callback(ROOT,layout['secondary_tileset']);raw=r._tile;regions=[]
    if secondary=='InitTilesetAnim_Rustboro':regions=[(640,32,'rustboro/anim/windy_water'),(960,4,'rustboro/anim/fountain')]
    if secondary=='InitTilesetAnim_Dewford':regions=[(682,6,'dewford/anim/flag')]
    def tile(t):
        for start,count,slug in regions:
            if start<=t<start+count:
                files=sorted((ROOT/'data/tilesets/secondary'/slug).glob('*.png'));im,row,_=indexed_tiles(files[frame%len(files)]);i=(t-start)%4 if start==640 else t-start
                return im.crop((i%row*8,i//row*8,i%row*8+8,i//row*8+8))
        return raw(t)
    r._tile=tile;r.palettes=[[tuple(v>>3<<3 for v in rgb) for rgb in pal] for pal in r.palettes]
    return r


def native_render(layout,frame=0):
    r=renderer(layout,frame);im=Image.new('RGBA',(layout['width']*16,layout['height']*16));cache={}
    for i,v in enumerate(words(ROOT/layout['blockdata_filepath'])):
        mid=v&1023
        if mid not in cache:cache[mid]=r.metatile(mid)
        im.alpha_composite(cache[mid],(i%layout['width']*16,i//layout['width']*16))
    return im.convert('RGB')


def render():
    c=json.loads((OUT/'functional_contract.json').read_text());_,ls,ms=inventory();out=OUT/'renders';out.mkdir(exist_ok=True)
    font=ImageFont.truetype('DejaVuSans.ttf',13);board=Image.new('RGB',(768,432),'#142b30');d=ImageDraw.Draw(board)
    centers=[(15,18),(13,10),(15,12),(8,5),(16,29),(14,12)]
    labels=['Ilha do Sul / desembarque','Ilha do Sul / santuário','Birth / basalto e triângulo',
            'Birth / porto de retorno','Faraway / costa e trilha','Faraway / mata de Mew']
    for i,n in enumerate(NAMES):
        l=ls[ms[n]['layout']];before=native_render(c['maps'][n]['layout']);after=native_render(l)
        before.save(out/(n+'-before.png'));after.save(out/(n+'.png'))
        comparison=Image.new('RGB',(after.width,after.height*2+40),'#142b30');dc=ImageDraw.Draw(comparison)
        dc.text((6,2),'Original',font=font,fill='white');comparison.paste(before,(0,20))
        dc.text((6,after.height+22),'Arauna 08D',font=font,fill='white');comparison.paste(after,(0,after.height+40));comparison.save(out/(n+'-comparison.png'))
        x,y=centers[i];left=max(0,min(x*16+8-120,max(0,after.width-240)));top=max(0,min(y*16+8-80,max(0,after.height-160)))
        bx,by=8+i%3*256,8+i//3*196;d.text((bx,by),labels[i],font=font,fill='#e0c690');board.paste(after.crop((left,top,left+240,top+160)),(bx,by+24))
        if n in ('SouthernIsland_Exterior','BirthIsland_Exterior','FarawayIsland_Entrance'):
            frames=[native_render(l,f).crop((left,top,left+240,top+160)) for f in range(8)]
            frames[0].save(out/(n+'-water.gif'),save_all=True,append_images=frames[1:],duration=120,loop=0)
    d.text((8,408),'Renders RGB555 sem atores; não são capturas do mGBA.',font=font,fill='white');board.save(out/'Arauna_08D_Preview.png')
    print('Six full maps, six comparisons, six cameras and three native animation previews')


def gates():
    import csv
    from concurrent.futures import ThreadPoolExecutor
    from safari_05_common import inventory as all_maps
    from audit_brazil_08 import UNUSED
    commands=['tools/arauna/audit_map_data.py','tools/arauna_maps/check_visual_protection_08.py',
        'tools/arauna/check_overworld_palette_capacity.py','tools/arauna/check_special_species.py',
        'tools/arauna/check_faction_visual_identity.py','tools/validate_arauna_character_assets.py']
    def run(script):
        r=subprocess.run(['python3',script],cwd=ROOT,capture_output=True,text=True);p=OUT/'logs'/(script.split('/')[-1]+'.log');p.parent.mkdir(exist_ok=True)
        p.write_text('\n'.join(line.rstrip() for line in (r.stdout+r.stderr).splitlines())+'\n')
        return {'script':script,'returncode':r.returncode,'status':'PASS' if r.returncode==0 else 'FAIL','log':str(p.relative_to(ROOT))}
    with ThreadPoolExecutor(max_workers=6) as pool:results=list(pool.map(run,commands))
    dump(OUT/'gates.json',{'status':'PASS' if all(r['returncode']==0 for r in results) else 'FAIL','gates':results});assert all(r['returncode']==0 for r in results),results
    node,ls,ms=all_maps(ROOT);rows=[];remaining=[];private=0
    for n,m in sorted(ms.items()):
        l=ls[m['layout']];arauna=any('Arauna' in l[k] for k in ('primary_tileset','secondary_tileset'));private+=arauna
        status='pyramid_runtime' if n.startswith('BattlePyramidSquare') else 'inactive' if n in UNUSED else 'Arauna bank' if arauna else 'native remaining'
        if status=='native remaining':remaining.append(n)
        rows.append({'map':n,'layout':m['layout'],'primary':l['primary_tileset'],'secondary':l['secondary_tileset'],'status':status})
    assert len(rows)==528 and len(node['layouts'])==754 and len(remaining)==11 and private==493
    with (OUT/'inventario_528_mapas.csv').open('w') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]),lineterminator='\n');w.writeheader();w.writerows(rows)
    dump(OUT/'fila_restante.json',{'maps':528,'layouts':754,'arauna_bank_maps':private,'native_remaining':remaining,
        'native_remaining_count':11,'pyramid_runtime_modules':16,'inactive_maps':8})
    print('Six read-only gates PASS; 493 Arauna bank maps; 11 native maps remain')


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('action',choices=('freeze','build','render','gates'));globals()[p.parse_args().action]()
