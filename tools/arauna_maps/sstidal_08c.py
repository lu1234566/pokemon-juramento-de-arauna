#!/usr/bin/env python3
"""SS Tidal: coastal ferry interiors at unchanged native IDs and gameplay."""
import argparse
import json
import subprocess
from PIL import Image, ImageDraw, ImageFont
from native_visuals_v2 import Pair, ROOT, declarations, dump, marked
from render_native_map import words
from trainer_hill_06a_art import native_layers
from cavernas_03a_common import renderer, render as native_render
from desert_08b1 import sha

BASE = '54c82e4430fcc3673afc3686db07fcb26ce755c8'
PREVIOUS = '062b84e92f2a59ef1e6703560bfcbc6c47b3263e'
INTEGRATED = 'a594b3e1e64517421101d96f5b314df22d47e14f'
PARTY_HASH = 'e05f9efb61cfd652e56a361ba1e8b826f614abc0e684438a0b031b036679d08f'
NAMES = ('SSTidalCorridor','SSTidalLowerDeck','SSTidalRooms')
OUT = ROOT / 'review/sstidal_08c'
TAG = 'SS_TIDAL_08C'
MUTABLE = {'data/layouts/layouts.json', *('src/data/tilesets/'+n for n in ('graphics.h','metatiles.h','headers.h'))}
FIXES = {'src/party_menu.c': PARTY_HASH,
 'src/field_player_avatar.c': '81ebe4b5761f8992cb459cf37978262358231734a1c56f8b3447346f770db95f',
 'src/scrcmd.c': '98cd4b72474c3cc7dfd5dc6cf54a4a96f807733017761a2be58d62b0dcd063a9'}


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
       'scope':'All prior tracked files except four additive graphics registries; all historical contracts unchanged.'}
    path=OUT/'functional_contract.json'
    if path.exists():assert json.loads(path.read_text())==c,'Refusing different contract'
    else:dump(path,c)
    print('Frozen',len(c['protected_hashes']),'files; corrected party menu included')

MATERIAL = [(0,0,0),(16,24,32),(32,56,64),(48,88,96),
 (72,120,128),(112,160,152),(168,200,184),(120,120,104),
 (192,192,160),(232,224,192),(64,40,32),(104,64,40),
 (160,104,56),(208,160,88),(152,56,48),(216,104,72)]
BANKS = [ROOT/'data/tilesets'/kind/'arauna_sstidal08c' for kind in ('primary','secondary')]
SYMBOLS = ['AraunaSSTidal08CPrimary','AraunaSSTidal08C']
DOOR_IDS = (0x223,0x22b,0x263,0x297)
PRESERVED_IDS = {0x201,*DOOR_IDS}


def floor(kind):
    im=Image.new('L',(16,16),12 if kind=='wood' else 4 if kind=='deck' else 3)
    d=ImageDraw.Draw(im)
    if kind=='wood':
        d.line((0,0,15,0),fill=11);d.line((0,1,15,1),fill=13)
        d.line((0,8,15,8),fill=11);d.line((0,9,15,9),fill=13)
        d.line((5,2,5,7),fill=11);d.line((13,10,13,15),fill=11)
        d.line((8,4,11,4),fill=13);d.point((2,12),fill=11)
    elif kind=='deck':
        d.line((0,15,15,15),fill=3)
        for x,y in ((2,3),(10,11)):d.line((x,y,x+2,y),fill=5)
    else:
        d.line((0,0,15,0),fill=2);d.line((15,0,15,15),fill=2)
        for x,y in ((2,2),(12,12)):d.point((x,y),fill=6)
        d.line((5,7,6,8),fill=4);d.line((10,3,11,4),fill=4)
    return im


def material_index(rgb,mid):
    r,g,b=rgb;light=(r+g+b)//3
    if max(rgb)<32:return 1
    if r>g*1.45 and r>b*1.45:return 14 if light<140 else 15
    if g>r*1.1 and g>b*1.04:
        return 2 if light<80 else 3 if light<125 else 4 if light<165 else 5 if light<200 else 6
    if b>r+12 and b>g*1.02:
        return 2 if light<85 else 3 if light<130 else 4 if light<175 else 5 if light<210 else 6
    if r>b*1.25 and g>b*1.08:
        return 10 if light<95 else 11 if light<140 else 12 if light<190 else 13
    return 2 if light<70 else 7 if light<155 else 8 if light<215 else 9


def surface(native,mid,layer):
    im=Image.new('L',(16,16))
    for y in range(16):
        for x in range(16):
            r,g,b,a=native.getpixel((x,y))
            if not a:continue
            v=material_index((r,g,b),mid)
            if mid in (0x230,0x231,0x232) and min(r,g,b)>225:
                # Cabin ceiling is sheet metal, distinct from the walking deck.
                v=8 if y in (7,15) else 9
            if 0x2e0<=mid<=0x2f6 and layer==1 and v in (12,13,5,6):
                # Cargo panels retain their contour, with new grain and braces.
                v=(11 if v>=12 else 3) if x==y else (13 if v>=12 else 6) if x%8==2 else v
            if layer==1 and 0x250<=mid<=0x27a and v in (4,5,6):
                # Sparse cloth folds/stripes on bed covers and chair cushions.
                if y in (4,12):v=6
                elif y in (5,13):v=max(3,v-1)
            im.putpixel((x,y),v)
    return im


def build():
    c=json.loads((OUT/'functional_contract.json').read_text())
    for rel,h in c['protected_hashes'].items():assert sha((ROOT/rel).read_bytes())==h,rel
    node,ls,ms=inventory();p=Pair(ROOT,c['maps'][NAMES[0]]['layout'])
    assert p.callbacks==['InitTilesetAnim_General','NULL']
    p.tile_cache={raw:i for i,raw in p.tiles.items() if i not in p.dynamic and i not in p.free}
    p.pals[12]=MATERIAL
    ids=sorted({v&1023 for name in NAMES for k in ('blockdata_filepath','border_filepath') for v in words(ROOT/c['maps'][name]['layout'][k])})
    bindings={}
    for mids,kind in (((0x238,0x23b),'wood'),((0x2ba,0x2bb),'deck'),((0x21d,0x20d),'hold')):
        for mid in mids:
            for e in p.meta[1][(mid-512)*8:(mid-512)*8+4]:
                if e&1023:bindings[(e&1023,e>>12)]=floor(kind)
    redrawn=[]
    for mid in ids:
        if mid in PRESERVED_IDS:continue
        original=p.reader.secondary_metatiles[(mid-512)*8:(mid-512)*8+8];result=[]
        for layer,native in enumerate(native_layers(p.reader,mid)):
            art=surface(native,mid,layer)
            for q,(dx,dy) in enumerate(((0,0),(8,0),(0,8),(8,8))):
                e=original[layer*4+q];t=e&1023
                assert t not in p.dynamic,'Unexpected hardware animated quarter'
                sample=bindings.get((t,e>>12))
                if sample is not None:
                    for y in range(dy,dy+8):
                        for x in range(dx,dx+8):
                            if native.getpixel((x,y))[3]:art.putpixel((x,y),sample.getpixel((x,y)))
                result.append(p.tile(art.crop((dx,dy,dx+8,dy+8)))|12<<12)
        p.meta[1][(mid-512)*8:(mid-512)*8+8]=result;redrawn.append(mid)
    p.write(BANKS)
    for key,body in declarations(BANKS,SYMBOLS,p.callbacks).items():marked(ROOT/'src/data/tilesets'/key,TAG,body)
    report={'base_commit':BASE,'protected_fixes':FIXES,'active_ids':ids,'redrawn_ids':redrawn,
            'new_graphics_slots':sorted(p.touched),'callbacks':p.callbacks,'banks':[str(b.relative_to(ROOT)) for b in BANKS],
            'preserved_native_doors':list(DOOR_IDS),'maps':{}}
    for name in NAMES:
        l=ls[ms[name]['layout']];l['primary_tileset'],l['secondary_tileset']=['gTileset_'+s for s in SYMBOLS]
        report['maps'][name]={'width':l['width'],'height':l['height'],'cells':l['width']*l['height'],
            'active_ids':sorted({v&1023 for k in ('blockdata_filepath','border_filepath') for v in words(ROOT/l[k])})}
    dump(ROOT/'data/layouts/layouts.json',node);dump(OUT/'build.json',report)
    print('Built three maps,',len(redrawn),'redrawn IDs,',len(p.touched),'safe graphics slots; four door IDs unchanged')


def render():
    c=json.loads((OUT/'functional_contract.json').read_text());_,ls,ms=inventory()
    out=OUT/'renders';out.mkdir(parents=True,exist_ok=True)
    font=ImageFont.truetype('DejaVuSans.ttf',13);cameras=[]
    for name in NAMES:
        before=native_render(ROOT,c['maps'][name]['layout']);after=native_render(ROOT,ls[ms[name]['layout']])
        before.save(out/(name+'-before.png'));after.save(out/(name+'.png'))
        comparison=Image.new('RGB',(after.width,after.height*2+40),'#18222a');d=ImageDraw.Draw(comparison)
        d.text((6,2),'Original',fill='white',font=font);comparison.paste(before,(0,20))
        d.text((6,after.height+22),'Arauna 08C',fill='white',font=font);comparison.paste(after,(0,after.height+40))
        comparison.save(out/(name+'-comparison.png'))
        points={'SSTidalCorridor':[('Corredor / escotilhas',8,4),('Cabines / saída',7,9)],
                'SSTidalLowerDeck':[('Porão / cargas',8,6)],
                'SSTidalRooms':[('Cabine do jogador / cama',13,12),('Cabine / TM Snatch',31,5)]}
        for label,x,y in points[name]:
            left=max(0,min(x*16+8-120,max(0,after.width-240)));top=max(0,min(y*16+8-80,max(0,after.height-160)))
            cameras.append((label,after.crop((left,top,left+240,top+160))))
    board=Image.new('RGB',(768,420),'#18222a');d=ImageDraw.Draw(board)
    for i,(label,im) in enumerate(cameras):
        x,y=8+i%3*256,8+i//3*194;d.text((x,y),label,font=font,fill='#f0d8a0');board.paste(im,(x,y+24))
    d.text((526,234),'08C — três mapas',font=font,fill='#f0d8a0')
    d.text((526,263),'Madeira, tecidos e aço naval',font=font,fill='white')
    d.text((8,398),'Renders RGB555 nativos, sem atores; não são capturas do mGBA.',font=font,fill='white')
    board.save(out/'Arauna_08C_Preview.png')
    # Decode the original eight-tile door frames, at the offsets field_door.c
    # uses (0, 0x100, 0x200). Palette 7 and the closed door stacks are frozen.
    from render_native_map import indexed_tiles
    pal=Pair(ROOT,ls[ms[NAMES[0]]['layout']]).pals[7]
    pal=[tuple(v>>3<<3 for v in rgb) for rgb in pal]
    for filename,name,x,y in [('abandoned_ship','SSTidalCorridor',4,9),('abandoned_ship_room','SSTidalRooms',13,1)]:
        sheet,_,_=indexed_tiles(ROOT/f'graphics/door_anims/{filename}.png');frames=[]
        base=native_render(ROOT,ls[ms[name]['layout']])
        for index in (-1,0,1,2,1,0,-1):
            state=base.copy()
            if index>=0:
                pixels=sheet.crop((0,index*32,16,index*32+32));frame=Image.new('RGB',(16,32));frame.putdata([pal[v] for v in pixels.getdata()])
                state.paste(frame,(x*16,(y-1)*16))
            left=max(0,min(x*16-64,base.width-160));top=max(0,min((y-1)*16-32,base.height-112))
            frames.append(state.crop((left,top,left+160,top+112)).resize((320,224),Image.Resampling.NEAREST))
        frames[0].save(out/(filename+'-door.gif'),save_all=True,append_images=frames[1:],duration=[500,180,180,500,180,180,500],loop=0)
    print('Rendered three full maps, comparisons and five native cameras')


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
    assert len(rows)==528 and len(node['layouts'])==754 and len(remaining)==17 and private==487
    with (OUT/'inventario_528_mapas.csv').open('w') as f:
        writer=csv.DictWriter(f,fieldnames=list(rows[0]),lineterminator='\n');writer.writeheader();writer.writerows(rows)
    dump(OUT/'fila_restante.json',{'maps':len(rows),'layouts':len(node['layouts']),'arauna_bank_maps':private,
        'native_remaining':remaining,'native_remaining_count':len(remaining),'pyramid_runtime_modules':16,'inactive_maps':8})
    print('Six read-only gates PASS; 528 maps, 754 layouts, 487 Arauna banks, 17 native remaining')


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('action',choices=('freeze','build','render','gates'))
    globals()[parser.parse_args().action]()
