#!/usr/bin/env python3
"""Private native geology for Underpass and Slab; no functional grid changes."""
import argparse
import json
import subprocess
from PIL import Image, ImageDraw, ImageFont
from native_visuals_v2 import Pair, ROOT, declarations, dump, marked
from render_native_map import words
from trainer_hill_06a_art import native_layers
from cavernas_03a_common import renderer, render as native_render
from desert_08b1 import sha

BASE = '0434665c07f2598f43bc399da4e8a7ce44e02979'
PREVIOUS = '5e51e3b2bac404da5753af6cf3d24cdd8195bfd1'
INTEGRATED = 'a594b3e1e64517421101d96f5b314df22d47e14f'
PARTY_HASH = 'e05f9efb61cfd652e56a361ba1e8b826f614abc0e684438a0b031b036679d08f'
NAMES = ('DesertUnderpass', 'ScorchedSlab')
OUT = ROOT / 'review/desert_08b2'
TAG = 'DESERT_08B2'
MUTABLE = {'data/layouts/layouts.json', *('src/data/tilesets/'+n for n in ('graphics.h','metatiles.h','headers.h'))}
PALETTES = {
 'DesertUnderpass': [(0,0,0),(0,0,0),(48,40,40),(72,56,48),(104,72,56),
                    (144,104,72),(176,136,88),(208,168,112),(232,200,144),
                    (248,224,184),(120,112,80),(128,112,88),(168,152,112),
                    (200,184,144),(224,208,168),(248,232,192)],
 'ScorchedSlab': [(0,0,0),(0,0,0),(24,32,40),(40,48,56),(64,72,80),
                  (88,96,104),(120,128,136),(152,160,160),(184,184,160),
                  (224,216,176),(48,72,56),(80,104,64),(120,136,88),
                  (136,112,72),(184,152,88),(232,200,136)]}


def inventory():
    node=json.loads((ROOT/'data/layouts/layouts.json').read_text())
    layouts={l['id']:l for l in node['layouts']}
    maps={n:json.loads((ROOT/f'data/maps/{n}/map.json').read_text()) for n in NAMES}
    return node,layouts,maps


def freeze():
    assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()==BASE
    assert sha((ROOT/'src/party_menu.c').read_bytes())==PARTY_HASH
    node,ls,ms=inventory()
    tracked=subprocess.check_output(['git','ls-files','-z'],cwd=ROOT).decode().rstrip('\0').split('\0')
    c={'base_commit':BASE,'previous_checkpoint':PREVIOUS,'corrected_party_menu_sha256':PARTY_HASH,
       'protected_hashes':{n:sha((ROOT/n).read_bytes()) for n in tracked if n not in MUTABLE},
       'registry_hashes':{n:sha((ROOT/n).read_bytes()) for n in sorted(MUTABLE)},
       'layout_ids':[l['id'] for l in node['layouts']],
       'maps':{n:{'map':ms[n],'layout':ls[ms[n]['layout']]} for n in NAMES},
       'scope':'All prior tracked files except four additive graphics registries; historical 08B1 contract unchanged.'}
    path=OUT/'functional_contract.json'
    if path.exists():assert json.loads(path.read_text())==c,'Refusing different contract'
    else:dump(path,c)
    print('Frozen',len(c['protected_hashes']),'files; corrected party menu included')


def ground(name, sand=False):
    im=Image.new('L',(16,16),14 if sand else 12 if name=='DesertUnderpass' else 6)
    d=ImageDraw.Draw(im)
    if name=='DesertUnderpass':
        for x,y in ((2,3),(12,6),(5,12),(14,14)):
            d.line((x,y,min(x+1,15),y),fill=13 if sand else 11)
            d.point((x,y-1),fill=15 if sand else 13)
        if sand:d.line((7,8,10,8),fill=15)
    else:
        # Large fractured stone slabs; darker edges make the raised platform read.
        d.line((0,0,15,0),fill=5);d.line((0,1,15,1),fill=7)
        d.line((15,0,15,15),fill=4)
        d.line((4,7,6,9),fill=4);d.line((6,9,6,11),fill=4)
        d.point((2,13),fill=11);d.point((3,13),fill=10)
        d.point((11,4),fill=7)
    return im


def geology(native, name, mid):
    im=Image.new('L',(16,16))
    for y in range(16):
        for x in range(16):
            r,g,b,a=native.getpixel((x,y))
            if not a:continue
            if (r,g,b)==(0,0,0):v=1
            else:
                light=(r+g+b)//3
                v=2 if light<65 else 3 if light<95 else 4 if light<125 else 5 if light<155 else 6 if light<185 else 7 if light<215 else 8
                if name=='DesertUnderpass':
                    # Continuous horizontal sediment bands replace diagonal marks.
                    if light>=120 and y in (4,12):v=max(3,v-1)
                    if light>=120 and y in (5,13):v=min(9,v+1)
                    if r>215 and g>190 and b<r*.9:v=14 if (x+y)%7 else 15
                else:
                    # Basalt fractures and sparse lichen belong on rock, not water.
                    if light>=120 and x in (3,11) and y in range(2,12):v=max(3,v-1)
                    if light>=140 and (x,y) in ((1,3),(2,3),(12,10),(13,10)):v=11
                    if light>=140 and (x,y) in ((1,4),(12,11)):v=10
            im.putpixel((x,y),v)
    return im


def build():
    c=json.loads((OUT/'functional_contract.json').read_text())
    for rel,h in c['protected_hashes'].items():assert sha((ROOT/rel).read_bytes())==h,rel
    node,ls,ms=inventory();decl={k:'' for k in ('graphics.h','metatiles.h','headers.h')};report={'base_commit':BASE,'maps':{}}
    for name in NAMES:
        old=c['maps'][name]['layout'];p=Pair(ROOT,old)
        p.dynamic.update(range(928,932));p.free=[i for i in p.free if i not in p.dynamic]
        p.tile_cache={raw:i for i,raw in p.tiles.items() if i not in p.dynamic}
        p.pals[12]=PALETTES[name]
        ids=sorted({v&1023 for k in ('blockdata_filepath','border_filepath') for v in words(ROOT/old[k])})
        # Only these native ground graphics receive the new ground texture.
        # Native cliff surfaces retain their silhouettes and shading hierarchy.
        floor_ids=(0x211,) if name=='DesertUnderpass' else (0x201,)
        floor_graphics={}
        for mid in floor_ids:
            for e in p.meta[mid>=512][mid%512*8:mid%512*8+8]:
                if e&1023:floor_graphics[(e&1023,e>>12)]=ground(name)
        if name=='DesertUnderpass':
            # Sand overlays the same floor as 0x211; only its upper plane is sand.
            for e in p.meta[1][(0x2a1-512)*8+4:(0x2a1-512)*8+8]:
                if e&1023:floor_graphics[(e&1023,e>>12)]=ground(name,True)
        redrawn=[];dynamic_words=0
        for mid in ids:
            entries=p.reader.primary_metatiles if mid<512 else p.reader.secondary_metatiles
            original=entries[mid%512*8:mid%512*8+8]
            # Pure water remains literally unchanged, including the warp 0x283.
            if any(e&1023 in p.dynamic for e in original) and all(not e&1023 or e&1023 in p.dynamic for e in original):
                dynamic_words+=sum(e&1023 in p.dynamic for e in original)
                continue
            result=[]
            for layer,native in enumerate(native_layers(p.reader,mid)):
                art=geology(native,name,mid)
                for q,(dx,dy) in enumerate(((0,0),(8,0),(0,8),(8,8))):
                    e=original[layer*4+q];t=e&1023
                    if t in p.dynamic:
                        result.append(e);dynamic_words+=1;continue
                    if (t,e>>12) in floor_graphics:
                        sample=floor_graphics[(t,e>>12)]
                        for y in range(dy,dy+8):
                            for x in range(dx,dx+8):
                                if native.getpixel((x,y))[3]:art.putpixel((x,y),sample.getpixel((x,y)))
                    if name=='ScorchedSlab' and mid==0x211:
                        # This ID is exclusively blocked bedrock in this map.
                        for y in range(dy,dy+8):
                            for x in range(dx,dx+8):
                                if native.getpixel((x,y))[3]:art.putpixel((x,y),3 if (x,y) in ((3,6),(4,6),(5,7),(12,13)) else 2)
                    tile=art.crop((dx,dy,dx+8,dy+8))
                    result.append(p.tile(tile)|12<<12)
            p.meta[mid>=512][mid%512*8:mid%512*8+8]=result;redrawn.append(mid)
        slug='arauna_underpass08b2' if name=='DesertUnderpass' else 'arauna_scorched08b2'
        paths=[ROOT/'data/tilesets'/kind/slug for kind in ('primary','secondary')]
        stem='AraunaUnderpass08B2' if name=='DesertUnderpass' else 'AraunaScorched08B2'
        symbols=[stem+'Primary',stem];p.write(paths)
        for key,body in declarations(paths,symbols,p.callbacks).items():decl[key]+=body
        l=ls[ms[name]['layout']];l['primary_tileset'],l['secondary_tileset']=['gTileset_'+s for s in symbols]
        report['maps'][name]={'redrawn_ids':redrawn,'active_ids':ids,'new_graphics_slots':sorted(p.touched),
             'banks':[str(path.relative_to(ROOT)) for path in paths],'callbacks':p.callbacks,
             'preserved_dynamic_tile_words':dynamic_words,'cells':old['width']*old['height'],
             'width':old['width'],'height':old['height'],'palette':12}
    for key,body in decl.items():marked(ROOT/'src/data/tilesets'/key,TAG,body)
    dump(ROOT/'data/layouts/layouts.json',node);dump(OUT/'build.json',report)
    print(json.dumps({n:{'redrawn_ids':len(d['redrawn_ids']),'new_tiles':len(d['new_graphics_slots'])} for n,d in report['maps'].items()}))


def render():
    c=json.loads((OUT/'functional_contract.json').read_text());_,ls,ms=inventory()
    out=OUT/'renders';out.mkdir(parents=True,exist_ok=True)
    font=ImageFont.truetype('DejaVuSans.ttf',13)
    cameras=[]
    for name in NAMES:
        before=native_render(ROOT,c['maps'][name]['layout'],frame=0)
        after=native_render(ROOT,ls[ms[name]['layout']],frame=0)
        before.save(out/(name+'-before.png'));after.save(out/(name+'.png'))
        comparison=Image.new('RGB',(after.width,after.height*2+32),'#18222a');d=ImageDraw.Draw(comparison)
        d.text((6,0),'Original',fill='white',font=font);comparison.paste(before,(0,16))
        d.text((6,after.height+16),'Arauna 08B2',fill='white',font=font);comparison.paste(after,(0,after.height+32))
        comparison.save(out/(name+'-comparison.png'))
        for label,x,y in ([('Entrada do Underpass',10,12),('Galeria sedimentar',67,11),('Depósito / fóssil',132,10)] if name=='DesertUnderpass' else [('Patamar do TM',7,5),('Margem e retorno',7,14)]):
            left,top=x*16+8-120,y*16+8-80
            left=max(0,min(left,after.width-240));top=max(0,min(top,after.height-160))
            cameras.append((label,after.crop((left,top,left+240,top+160))))
    board=Image.new('RGB',(752,394),'#18222a');d=ImageDraw.Draw(board)
    for i,(label,im) in enumerate(cameras):
        x,y=i%3*256,i//3*192;d.text((x+4,y+4),label,font=font,fill='white');board.paste(im,(x,y+26))
    d.text((516,226),'08B2 — dois mapas',font=font,fill='#e8d1a0')
    d.text((516,252),'Renders RGB555 nativos',font=font,fill='white')
    d.text((516,276),'Sem atores / não são mGBA',font=font,fill='white')
    board.save(out/'Arauna_08B2_Preview.png')
    l=ls[ms['ScorchedSlab']['layout']]
    frames=[native_render(ROOT,l,frame=i) for i in range(8)]
    frames[0].save(out/'ScorchedSlab-water.gif',save_all=True,append_images=frames[1:],duration=160,loop=0)
    print('Rendered full maps, five 240x160 cameras and native water frames')


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('action',choices=('freeze','build','render'))
    globals()[parser.parse_args().action]()
