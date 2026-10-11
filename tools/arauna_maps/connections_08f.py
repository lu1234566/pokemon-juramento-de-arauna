#!/usr/bin/env python3
"""Five native connection rooms: public communications and League halls."""
import argparse
import json
import subprocess
from PIL import Image, ImageDraw, ImageFont
from native_visuals_v2 import Pair, ROOT, declarations, dump, marked
from render_native_map import words,Renderer,indexed_tiles
from trainer_hill_06a_art import native_layers
from islands_08d import FIXES, reserve_dma
from desert_08b1 import sha

BASE = 'f0f08e4ed2edea95963f979fb81a82dbb8b53400'
PREVIOUS = '76d76ddfe54649073810a8997d16bdb4e4c71371'
INTEGRATED = 'a594b3e1e64517421101d96f5b314df22d47e14f'
MAIN = '979fb6c1b6731561f3c993efd6045a9bbf096c54'
NAMES = ('BattleColosseum_2P','BattleColosseum_4P','RecordCorner','TradeCenter','UnionRoom')
OUT = ROOT/'review/connections_08f'
TAG = 'CONNECTIONS_08F'
MUTABLE = {'data/layouts/layouts.json', *('src/data/tilesets/'+n for n in ('graphics.h','metatiles.h','headers.h'))}
GROUPS = {
 'colosseum':{'names':NAMES[:2],'suffix':'League','style':'league'},
 'records':{'names':NAMES[2:3],'suffix':'Records','style':'records'},
 'trade':{'names':NAMES[3:4],'suffix':'Trade','style':'trade'},
 'union':{'names':NAMES[4:],'suffix':'Union','style':'union'}}
CHECKPOINTS = {'08F1':NAMES[:2], '08F2':NAMES[2:4], '08F3':NAMES[4:]}
MATERIAL = [(0,0,0),(32,32,32),(72,48,32),(144,104,64),(192,152,96),
            (32,64,56),(48,104,88),(104,160,136),(104,104,88),(176,168,144),
            (216,208,176),(144,104,40),(216,176,80),(184,80,56),(80,136,184),(240,232,208)]
PALETTES = {k:list(MATERIAL) for k in GROUPS}


def inventory():
    node=json.loads((ROOT/'data/layouts/layouts.json').read_text());ls={l['id']:l for l in node['layouts']}
    ms={n:json.loads((ROOT/f'data/maps/{n}/map.json').read_text()) for n in NAMES}
    return node,ls,ms


def freeze():
    assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()==BASE
    for n,h in FIXES.items():assert sha((ROOT/n).read_bytes())==h,n
    node,ls,ms=inventory();tracked=subprocess.check_output(['git','ls-files','-z'],cwd=ROOT).decode().rstrip('\0').split('\0')
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
                     'design':'Interpretation of Community Center, League Headquarters and Central Archive equipment; Bible p.44 public science/communications, distinct from Consortium ownership. No dedicated Link-room chapter is claimed.'},
       'scope':'All prior tracked files except four additive graphics registries; historical contracts stay unchanged.'}
    path=OUT/'functional_contract.json'
    if path.exists():assert json.loads(path.read_text())==c,'Refusing changed contract'
    else:dump(path,c)
    print('Frozen',len(c['protected_hashes']),'files, seven fixes and 82 verified concepts')


def wood(x,y):
    if y in (0,8):return 3
    if x==(3 if y<8 else 11):return 3
    if (x,y) in ((7,4),(8,4),(2,12),(3,12)):return 3
    return 4


def stone(x,y):
    if x==0 or y==0:return 8
    if (x,y) in ((1,1),(2,1),(1,2)):return 10
    if (x,y)==(12,13):return 8
    return 9


def plane(native,style,mid,layer):
    im=Image.new('L',(16,16))
    for y in range(16):
        for x in range(16):
            r,g,b,a=native.getpixel((x,y))
            if not a:continue
            rgb=(r,g,b);light=(r+g+b)//3
            if style=='league' and rgb==(180,172,148):v=wood(x,y)
            elif style=='trade' and rgb==(123,156,180):v=stone(x,y)
            elif style=='union' and rgb==(156,238,164):v=stone(x,y)
            elif style=='records' and rgb in ((230,238,255),(213,205,246),(156,197,156)):
                # Shared floor colors across all furniture/background pieces;
                # retain the gray bench strip and equipment silhouettes.
                v=stone(x,y)
            elif style=='union' and 0x210<=mid<=0x222 and g>r*1.08 and g>b*1.06:
                v=12 if light<215 else 15
            elif style=='union' and r>g*1.18 and r>b*1.18:
                # Public reception: wood paneling instead of a red fascia.
                v=2 if light<100 else 3 if light<175 else 4
                if y in (3,11):v=max(2,v-1)
            elif style=='league' and r>g*1.12 and g>b*1.1:
                # Bronze detailing over carved wooden wall panels.
                v=2 if light<90 else 3 if light<145 else 11 if light<190 else 12
                if layer==0 and x%8==0 and light<145:v=2
            elif r>g*1.3 and r>b*1.18:v=13
            elif b>r*1.22 and b>g*1.1:v=14
            elif g>r*1.12 and g>b*1.08:v=5 if light<80 else 6 if light<175 else 7
            elif r>b*1.2 and g>b*1.12:v=11 if light<140 else 12 if light<220 else 15
            elif max(rgb)<82:v=1
            elif max(rgb)-min(rgb)<32:v=8 if light<145 else 9 if light<190 else 10 if light<225 else 15
            else:
                # Teal glass, oxidized bronze and pale stone machine casings.
                v=5 if light<100 else 6 if light<160 else 7 if light<205 else 15
            im.putpixel((x,y),v)
    return im

def build():
    c=json.loads((OUT/'functional_contract.json').read_text())
    for rel,h in c['protected_hashes'].items():assert sha((ROOT/rel).read_bytes())==h,rel
    node,ls,ms=inventory();report={'base_commit':BASE,'protected_fixes':FIXES,'groups':{},'maps':{}}
    bodies={k:'' for k in ('graphics.h','metatiles.h','headers.h')}
    for key,g in GROUPS.items():
        p=reserve_dma(Pair(ROOT,c['maps'][g['names'][0]]['layout']))
        assert p.callbacks==['InitTilesetAnim_Building','NULL']
        assert not any(e>>12==12 and e&1023 for a in p.meta for e in a),'Palette 12 already used'
        p.pals[12]=PALETTES[key]
        ids=sorted({v&1023 for n in g['names'] for k in ('blockdata_filepath','border_filepath') for v in words(ROOT/c['maps'][n]['layout'][k])})
        # Shared cable scripts swap gate tiles in the existing Pokemon Centers,
        # not these rooms. Union Room changes occupancy flags, not tile IDs.
        redrawn=[]
        for mid in ids:
            original=p.meta[mid>=512][mid%512*8:mid%512*8+8];result=[]
            for layer,native in enumerate(native_layers(p.reader,mid)):
                art=plane(native,g['style'],mid,layer)
                for q,(dx,dy) in enumerate(((0,0),(8,0),(0,8),(8,8))):
                    e=original[layer*4+q]
                    if e&1023 in p.dynamic:result.append(e)
                    else:result.append(p.tile(art.crop((dx,dy,dx+8,dy+8)))|12<<12)
            p.meta[mid>=512][mid%512*8:mid%512*8+8]=result;redrawn.append(mid)
        paths=[ROOT/'data/tilesets'/kind/('arauna_connections08f_'+key) for kind in ('primary','secondary')]
        symbols=['AraunaConnections08F'+g['suffix']+'Primary','AraunaConnections08F'+g['suffix']]
        p.write(paths)
        declared=declarations(paths,symbols,p.callbacks)
        compressed=[True,key=='union']
        if not compressed[1]:
            declaration='const struct Tileset gTileset_'+symbols[1]+' ='
            prefix,secondary=declared['headers.h'].split(declaration,1)
            declared['headers.h']=prefix+declaration+secondary.replace('.isCompressed = TRUE','.isCompressed = FALSE')
            declared['graphics.h']=declared['graphics.h'].replace(str(paths[1].relative_to(ROOT))+'/tiles.png", ".4bpp.lz"',str(paths[1].relative_to(ROOT))+'/tiles.png", ".4bpp"')
        for field,body in declared.items():bodies[field]+=body
        report['groups'][key]={'names':list(g['names']),'style':key,'active_and_runtime_ids':ids,'runtime_ids':[],
            'redrawn_ids':redrawn,'new_graphics_slots':sorted(p.touched),'reserved_dma_slots':sorted(p.dynamic),
            'callbacks':p.callbacks,'is_compressed':compressed,'banks':[str(path.relative_to(ROOT)) for path in paths]}
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
    r=Renderer(*[resolve_bank(ROOT,layout[k]) for k in ('primary_tileset','secondary_tileset')])
    assert callback(ROOT,layout['primary_tileset'])=='InitTilesetAnim_Building'
    assert callback(ROOT,layout['secondary_tileset'])=='NULL'
    raw=r._tile
    im,row,_=indexed_tiles(ROOT/f'data/tilesets/primary/building/anim/tv_turned_on/{frame%2}.png')
    def tile(t):
        if 496<=t<500:
            i=t-496;return im.crop((i%row*8,i//row*8,i%row*8+8,i//row*8+8))
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
    font=ImageFont.truetype('DejaVuSans.ttf',13);board=Image.new('RGB',(984,492),'#202b30');d=ImageDraw.Draw(board)
    comparison=Image.new('RGB',(984,916),'#202b30');dc=ImageDraw.Draw(comparison)
    labels=['Liga / duelo 2P','Liga / confronto 4P','Arquivo / mesa de registros','Trocas / terminal comunitário','Union Room / encontro e conexão']
    for i,n in enumerate(NAMES):
        before=native_render(c['maps'][n]['layout']);after=native_render(ls[ms[n]['layout']])
        before.save(out/(n+'-before.png'));after.save(out/(n+'.png'))
        individual=Image.new('RGB',(after.width,after.height*2+40),'#202b30');di=ImageDraw.Draw(individual)
        di.text((4,1),'Original',font=font,fill='white');individual.paste(before,(0,20))
        di.text((4,after.height+22),'Arauna 08F',font=font,fill='white');individual.paste(after,(0,after.height+40));individual.save(out/(n+'-comparison.png'))
        bx,by=8+i%3*328,8+i//3*232;d.text((bx,by),labels[i],font=font,fill='#e0c690');board.paste(after,(bx,by+24))
        cy=8+i//3*448;dc.text((bx,cy),labels[i]+' / original',font=font,fill='white');comparison.paste(before,(bx,cy+24))
        dc.text((bx,cy+222),'Arauna 08F',font=font,fill='#e0c690');comparison.paste(after,(bx,cy+244))
    d.text((668,264),'08F1: duas arenas da Liga',font=font,fill='#e0c690')
    d.text((668,290),'08F2: registros e trocas',font=font,fill='#e0c690')
    d.text((668,316),'08F3: Union Room',font=font,fill='#e0c690')
    d.text((668,354),'Scripts e posições preservados.',font=font,fill='white')
    d.text((8,470),'Renders RGB555 nativos sem atores; não são capturas do mGBA.',font=font,fill='white')
    board.save(out/'Arauna_08F_Preview.png');comparison.save(out/'Arauna_08F_Comparacao.png')
    print('Five full maps, five comparisons and combined before/after board')

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
    assert len(rows)==528 and len(node['layouts'])==754 and len(remaining)==0 and private==504
    with (OUT/'inventario_528_mapas.csv').open('w') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]),lineterminator='\n');w.writeheader();w.writerows(rows)
    dump(OUT/'fila_restante.json',{'maps':528,'layouts':754,'arauna_bank_maps':private,'native_remaining':remaining,
        'native_remaining_count':0,'pyramid_runtime_modules':16,'inactive_maps':8})
    print('Six read-only gates PASS; 504 Arauna bank maps; no active native map remains')


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('action',choices=('freeze','build','render','gates'));globals()[p.parse_args().action]()
