#!/usr/bin/env python3
"""Mirage Tower: stratified sandstone, native crack/hole IDs and intact gameplay."""
import argparse
import json
import subprocess
from PIL import Image, ImageDraw, ImageFont
from native_visuals_v2 import Pair, ROOT, declarations, dump, marked
from render_native_map import words
from trainer_hill_06a_art import native_layers
from cavernas_03a_common import renderer, render as native_render
from desert_08b1 import sha

BASE = 'a862cdee1d7e2c910abae6122b45951ea1690198'
PREVIOUS = '646a270fdf3a897b50bf12c7b4e50d5a06f3f24e'
INTEGRATED = 'a594b3e1e64517421101d96f5b314df22d47e14f'
PARTY_HASH = 'e05f9efb61cfd652e56a361ba1e8b826f614abc0e684438a0b031b036679d08f'
NAMES = tuple(f'MirageTower_{i}F' for i in range(1,5))
OUT = ROOT / 'review/mirage_08b3'
TAG = 'MIRAGE_08B3'
MUTABLE = {'data/layouts/layouts.json', *('src/data/tilesets/'+n for n in ('graphics.h','metatiles.h','headers.h'))}
FIXES = {'src/party_menu.c': PARTY_HASH,
 'src/field_player_avatar.c': '81ebe4b5761f8992cb459cf37978262358231734a1c56f8b3447346f770db95f',
 'src/scrcmd.c': '98cd4b72474c3cc7dfd5dc6cf54a4a96f807733017761a2be58d62b0dcd063a9'}
MATERIAL = [(0,0,0),(16,16,24),(48,32,32),(72,40,32),
 (104,56,40),(136,80,48),(168,104,64),(192,136,80),
 (216,168,104),(240,200,136),(112,88,56),(144,112,72),
 (176,144,96),(208,176,120),(232,208,160),(248,232,192)]
BANKS = [ROOT/'data/tilesets'/kind/'arauna_mirage08b3' for kind in ('primary','secondary')]
SYMBOLS = ['AraunaMirage08B3Primary','AraunaMirage08B3']
RUNTIME_IDS = (0x22f,0x206)


def inventory():
    node=json.loads((ROOT/'data/layouts/layouts.json').read_text())
    layouts={l['id']:l for l in node['layouts']}
    maps={n:json.loads((ROOT/f'data/maps/{n}/map.json').read_text()) for n in NAMES}
    return node,layouts,maps


def freeze():
    assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()==BASE
    for rel,h in FIXES.items():assert sha((ROOT/rel).read_bytes())==h,rel
    node,ls,ms=inventory()
    tracked=subprocess.check_output(['git','ls-files','-z'],cwd=ROOT).decode().rstrip('\0').split('\0')
    c={'base_commit':BASE,'previous_checkpoint':PREVIOUS,'corrected_party_menu_sha256':PARTY_HASH,'protected_fixes':FIXES,
       'protected_hashes':{n:sha((ROOT/n).read_bytes()) for n in tracked if n not in MUTABLE},
       'registry_hashes':{n:sha((ROOT/n).read_bytes()) for n in sorted(MUTABLE)},
       'layout_ids':[l['id'] for l in node['layouts']],
       'maps':{n:{'map':ms[n],'layout':ls[ms[n]['layout']]} for n in NAMES},
       'scope':'All prior tracked files except four additive graphics registries; historical 08B1 and 08B2 contracts unchanged.'}
    path=OUT/'functional_contract.json'
    if path.exists():assert json.loads(path.read_text())==c,'Refusing different contract'
    else:dump(path,c)
    print('Frozen',len(c['protected_hashes']),'files; corrected party menu included')


def floor(sand=False, bedrock=False):
    im=Image.new('L',(16,16),14 if sand else 7 if bedrock else 12)
    d=ImageDraw.Draw(im)
    if sand:
        for x,y in ((1,4),(10,11)):
            d.line((x,y,x+3,y),fill=13);d.line((x+1,y-1,x+4,y-1),fill=15)
    elif bedrock:
        d.line((0,5,15,5),fill=6);d.line((0,6,15,6),fill=8)
        d.line((0,13,15,13),fill=6);d.point((4,2),fill=8)
    else:
        for x,y in ((2,3),(11,7),(5,13)):
            d.line((x,y,x+1,y),fill=11);d.point((x,y-1),fill=13)
    return im


def sandstone(native,mid):
    im=Image.new('L',(16,16))
    for y in range(16):
        for x in range(16):
            r,g,b,a=native.getpixel((x,y))
            if not a:continue
            light=(r+g+b)//3
            v=1 if max(r,g,b)<24 else 2 if light<65 else 3 if light<95 else 4 if light<125 else 5 if light<155 else 6 if light<185 else 7 if light<215 else 8
            if v>=4 and y in (3,11):v=max(3,v-1)
            if v>=4 and y in (4,12):v=min(9,v+1)
            if mid in (0x20e,0x20f,0x216,0x217,0x23f,0x259) and light>=180:v=14
            im.putpixel((x,y),v)
    return im


def floor_state(hole=False):
    im=floor();d=ImageDraw.Draw(im)
    if hole:
        d.polygon([(2,2),(7,0),(12,2),(15,6),(14,12),(10,15),(3,14),(0,8)],fill=3)
        d.polygon([(3,3),(7,2),(11,3),(13,6),(12,11),(9,13),(4,12),(2,8)],fill=1)
        d.line((1,8,3,3,7,1,12,3,14,6),fill=8)
        d.point((3,13),fill=5)
    else:
        # Wide, continuous dark fractures remain legible in a 240x160 camera.
        for points in ([(0,3),(4,5),(7,4),(10,8),(15,6)],
                       [(7,4),(6,0)],[(10,8),(8,12),(9,15)],
                       [(8,12),(3,11),(0,14)]):
            d.line(points,fill=3,width=1)
        d.line((1,2,4,4,7,3),fill=14)
        d.line((11,9,9,12),fill=14)
    return im


def build():
    c=json.loads((OUT/'functional_contract.json').read_text())
    for rel,h in c['protected_hashes'].items():assert sha((ROOT/rel).read_bytes())==h,rel
    node,ls,ms=inventory();old=c['maps'][NAMES[0]]['layout'];p=Pair(ROOT,old)
    assert p.callbacks==['InitTilesetAnim_General','NULL']
    # A free source slot may still contain unreferenced graphics. Exclude its
    # old bytes from reuse: allocation will overwrite them during this build.
    p.tile_cache={raw:i for i,raw in p.tiles.items() if i not in p.dynamic and i not in p.free}
    p.pals[12]=MATERIAL
    ids=sorted({v&1023 for name in NAMES for k in ('blockdata_filepath','border_filepath') for v in words(ROOT/c['maps'][name]['layout'][k])}|set(RUNTIME_IDS))
    ground_graphics={}
    for mid,art in ((0x201,floor()),(0x211,floor(bedrock=True))):
        for e in p.meta[1][(mid-512)*8:(mid-512)*8+4]:
            ground_graphics[(e&1023,e>>12)]=art
    sand_graphics={e&1023 for mid in range(0x298,0x2ab) for e in p.meta[1][(mid-512)*8+4:(mid-512)*8+8] if e>>12==5 and e&1023}
    for mid in ids:
        original=p.reader.secondary_metatiles[(mid-512)*8:(mid-512)*8+8]
        result=[]
        for layer,native in enumerate(native_layers(p.reader,mid)):
            art=sandstone(native,mid)
            if mid in RUNTIME_IDS and layer==0:art=floor_state(mid==0x206)
            for q,(dx,dy) in enumerate(((0,0),(8,0),(0,8),(8,8))):
                e=original[layer*4+q];t=e&1023
                assert t not in p.dynamic,'Tower art unexpectedly uses hardware animation'
                sample=ground_graphics.get((t,e>>12))
                if layer==1 and e>>12==5 and t in sand_graphics:sample=floor(sand=True)
                if sample is not None:
                    for y in range(dy,dy+8):
                        for x in range(dx,dx+8):
                            if native.getpixel((x,y))[3]:art.putpixel((x,y),sample.getpixel((x,y)))
                result.append(p.tile(art.crop((dx,dy,dx+8,dy+8)))|12<<12)
        p.meta[1][(mid-512)*8:(mid-512)*8+8]=result
    p.write(BANKS)
    for key,body in declarations(BANKS,SYMBOLS,p.callbacks).items():marked(ROOT/'src/data/tilesets'/key,TAG,body)
    report={'base_commit':BASE,'protected_fixes':FIXES,'redrawn_ids':ids,
            'new_graphics_slots':sorted(p.touched),'callbacks':p.callbacks,
            'banks':[str(p.relative_to(ROOT)) for p in BANKS],
            'runtime_crack_to_hole':['0x22F','0x206'],'maps':{}}
    for name in NAMES:
        l=ls[ms[name]['layout']];l['primary_tileset'],l['secondary_tileset']=['gTileset_'+s for s in SYMBOLS]
        report['maps'][name]={'width':l['width'],'height':l['height'],'cells':l['width']*l['height'],
            'active_ids':sorted({v&1023 for k in ('blockdata_filepath','border_filepath') for v in words(ROOT/l[k])})}
    dump(ROOT/'data/layouts/layouts.json',node);dump(OUT/'build.json',report)
    print('Built four maps,',len(ids),'IDs including runtime hole,',len(p.touched),'safe graphics slots')


def render():
    c=json.loads((OUT/'functional_contract.json').read_text());_,ls,ms=inventory()
    out=OUT/'renders';out.mkdir(parents=True,exist_ok=True)
    font=ImageFont.truetype('DejaVuSans.ttf',13);cameras=[]
    for i,name in enumerate(NAMES):
        before=native_render(ROOT,c['maps'][name]['layout']);after=native_render(ROOT,ls[ms[name]['layout']])
        before.save(out/(name+'-before.png'));after.save(out/(name+'.png'))
        comparison=Image.new('RGB',(max(240,after.width),after.height*2+40),'#18222a');d=ImageDraw.Draw(comparison)
        d.text((6,2),'Original',fill='white',font=font);comparison.paste(before,(0,20))
        d.text((6,after.height+22),'Arauna 08B3',fill='white',font=font);comparison.paste(after,(0,after.height+40))
        comparison.save(out/(name+'-comparison.png'))
        x,y=[(10,11),(3,5),(3,6),(6,5)][i]
        left=max(0,min(x*16+8-120,max(0,after.width-240)));top=max(0,min(y*16+8-80,max(0,after.height-160)))
        camera=Image.new('RGB',(240,160),'#101018');camera.paste(after.crop((left,top,min(left+240,after.width),min(top+160,after.height))),(0,0))
        cameras.append((f'{i+1}F — '+['Entrada e arenito','Piso frágil','Ascensão / Rock Smash','Sala dos fósseis'][i],camera))
        if i in (1,2):
            visual=[0x206 if v&1023==0x22f else v&1023 for v in words(ROOT/ls[ms[name]['layout']]['blockdata_filepath'])]
            native_render(ROOT,ls[ms[name]['layout']],visual).save(out/(name+'-holes.png'))
    board=Image.new('RGB',(512,428),'#18222a');d=ImageDraw.Draw(board)
    for i,(label,im) in enumerate(cameras):
        x,y=8+i%2*256,8+i//2*194;d.text((x,y),label,font=font,fill='#f0d8a0');board.paste(im,(x,y+24))
    d.text((8,404),'Renders RGB555 nativos, sem atores; não são capturas do mGBA.',font=font,fill='white')
    board.save(out/'Arauna_08B3_Preview.png')
    p=Pair(ROOT,ls[ms[NAMES[1]]['layout']]);a=p.reader.metatile(0x22f).convert('RGB');b=p.reader.metatile(0x206).convert('RGB')
    a.save(out/'Crack-to-hole.gif',save_all=True,append_images=[b],duration=[900,900],loop=0)
    print('Rendered all floors, camera views and crack/hole states')


def gates():
    import csv
    from concurrent.futures import ThreadPoolExecutor
    from safari_05_common import inventory as all_maps
    from audit_brazil_08 import UNUSED
    commands=['tools/arauna/audit_map_data.py','tools/arauna_maps/check_visual_protection_08.py',
        'tools/arauna/check_overworld_palette_capacity.py','tools/arauna/check_special_species.py',
        'tools/arauna/check_faction_visual_identity.py','tools/validate_arauna_character_assets.py']
    def run(script):
        result=subprocess.run(['python3',script],cwd=ROOT,capture_output=True,text=True)
        path=OUT/'logs'/(script.split('/')[-1]+'.log');path.parent.mkdir(exist_ok=True)
        path.write_text('\n'.join(line.rstrip() for line in (result.stdout+result.stderr).splitlines())+'\n')
        return {'script':script,'returncode':result.returncode,'status':'PASS' if result.returncode==0 else 'FAIL','log':str(path.relative_to(ROOT))}
    with ThreadPoolExecutor(max_workers=6) as pool:results=list(pool.map(run,commands))
    dump(OUT/'gates.json',{'status':'PASS' if all(r['returncode']==0 for r in results) else 'FAIL','gates':results})
    assert all(r['returncode']==0 for r in results),results
    node,layouts,maps=all_maps(ROOT);rows=[];remaining=[];private=0
    for name,m in sorted(maps.items()):
        l=layouts[m['layout']];arauna=any('Arauna' in l[k] for k in ('primary_tileset','secondary_tileset'));private+=arauna
        status='pyramid_runtime' if name.startswith('BattlePyramidSquare') else 'inactive' if name in UNUSED else 'Arauna bank' if arauna else 'native remaining'
        if status=='native remaining':remaining.append(name)
        rows.append({'map':name,'layout':m['layout'],'primary':l['primary_tileset'],'secondary':l['secondary_tileset'],'status':status})
    assert len(rows)==528 and len(node['layouts'])==754 and len(remaining)==20 and private==484
    with (OUT/'inventario_528_mapas.csv').open('w') as f:
        writer=csv.DictWriter(f,fieldnames=list(rows[0]),lineterminator='\n');writer.writeheader();writer.writerows(rows)
    dump(OUT/'fila_restante.json',{'maps':len(rows),'layouts':len(node['layouts']),'arauna_bank_maps':private,
        'native_remaining':remaining,'native_remaining_count':len(remaining),'pyramid_runtime_modules':16,'inactive_maps':8})
    print('Six read-only gates PASS; 528 maps, 754 layouts, 484 Arauna banks, 20 native remaining')


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('action',choices=('freeze','build','render','gates'))
    globals()[parser.parse_args().action]()
