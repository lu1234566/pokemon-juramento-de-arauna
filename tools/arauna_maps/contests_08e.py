#!/usr/bin/env python3
"""Six native contest stages: Arauna's community festival, unchanged mechanics."""
import argparse
import json
import subprocess
from PIL import Image, ImageDraw, ImageFont
from native_visuals_v2 import Pair, ROOT, declarations, dump, marked
from render_native_map import words
from trainer_hill_06a_art import native_layers
from islands_08d import FIXES, reserve_dma, renderer, native_render
from desert_08b1 import sha

BASE = 'e740b80190d1e0a5c18e2536b1705a2795f943a7'
PREVIOUS = 'c6143a51737f4716ac347e14ab4eb0b0dbccba01'
INTEGRATED = 'a594b3e1e64517421101d96f5b314df22d47e14f'
MAIN = '979fb6c1b6731561f3c993efd6045a9bbf096c54'
NAMES = ('ContestHall','ContestHallCool','ContestHallBeauty','ContestHallCute','ContestHallSmart','ContestHallTough')
OUT = ROOT/'review/contests_08e'
TAG = 'CONTESTS_08E'
MUTABLE = {'data/layouts/layouts.json', *('src/data/tilesets/'+n for n in ('graphics.h','metatiles.h','headers.h'))}
GROUPS = {key:{'names':(name,), 'suffix':suffix,'style':key} for key,name,suffix in zip(
    ('festival','cool','beauty','cute','smart','tough'),NAMES,('Festival','Cool','Beauty','Cute','Smart','Tough'))}
CHECKPOINTS = {'08E1':NAMES[:2], '08E2':NAMES[2:4], '08E3':NAMES[4:]}
ACCENTS = {
    'festival':[(64,72,72),(104,120,112),(168,184,160)],
    'cool':[(120,48,40),(184,80,56),(224,136,88)],
    'beauty':[(40,72,120),(64,112,168),(120,168,200)],
    'cute':[(120,56,88),(184,104,136),(224,152,160)],
    'smart':[(40,88,64),(72,136,88),(144,176,112)],
    'tough':[(128,88,32),(184,136,48),(224,184,96)]}
# 1-5 hardwood and bronze, 6-9 limestone, 10-12 dyed cloth, 13-15 gold.
PALETTES = {k:[(0,0,0),(40,32,32),(72,48,32),(112,72,40),(160,112,64),(200,152,96),
                 (88,80,64),(144,136,112),(192,184,152),(224,216,184),*a,
                 (144,104,40),(208,168,72),(240,216,144)] for k,a in ACCENTS.items()}
STAGE_RGB = (189,222,197)
AUDIENCE_RGB = {(148,172,180),(115,131,131)}


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
                     'design':'Interpretation of the community-center concept and Bible p.42 community stage; Bravamar material continuity. No dedicated Contest chapter is claimed.'},
       'scope':'All prior tracked files except four additive graphics registries; historical contracts stay unchanged.'}
    path=OUT/'functional_contract.json'
    if path.exists():assert json.loads(path.read_text())==c,'Refusing changed contract'
    else:dump(path,c)
    print('Frozen',len(c['protected_hashes']),'files, seven fixes and 82 verified concepts')


def wood(x,y):
    # Short, staggered planks with quiet grain and small iron nail heads.
    if y%8==0:return 3
    seam=2 if y<8 else 10
    if x==seam:return 3
    if (x,y) in ((4,3),(5,3),(13,12),(14,12)):return 4
    if (x,y) in ((3,2),(11,10)):return 2
    return 5


def stone(x,y):
    if x==0 or y==0:return 7
    if (x,y) in ((1,1),(2,1),(1,2)):return 9
    if (x,y)==(11,13):return 7
    return 8


def plane(native,style,mid,layer):
    im=Image.new('L',(16,16));pal=PALETTES[style]
    for y in range(16):
        for x in range(16):
            r,g,b,a=native.getpixel((x,y))
            if not a:continue
            rgb=(r,g,b);light=(r+g+b)//3
            if rgb==STAGE_RGB:v=wood(x,y)
            elif rgb in AUDIENCE_RGB:v=stone(x,y)
            elif mid==0x260:
                # Carved beam, a cord and a repeated woven festival pennant.
                v=2 if y in (0,15) else 3 if y%8 in (2,6) else 4
                if y==3:v=14
                if 4<=y<=11 and abs(x-7)<=(11-y)//2:v=10 if x==7 else 11
                if (x,y) in ((6,5),(7,6),(8,5)):v=12
            elif mid==0x201:v=1
            elif 0x20c<=mid<=0x226:
                # Stone wall faces, inset wooden frieze and dark wall shadows.
                if light<100:v=1 if light<65 else 2
                elif light<155:v=6
                elif light<200:v=7
                else:v=9
            elif mid in (0x26f,0x277):
                # Gold-framed textile emblem, keeping its tiny native silhouette.
                v=14 if r>g*1.12 and r>b*1.1 else 15 if light>210 else 10 if light<100 else 11
            elif 0x268<=mid<=0x27a:
                # Existing stage borders become wooden/bronze rails.
                if light<100:v=1
                elif r>g*1.12:v=3 if light<155 else 4 if light<195 else 14
                else:v=6 if light<155 else 7
                if layer==1 and v==4 and (x+y)%8==2:v=5
            elif layer==1:
                # The native category award and the two ribbon ornaments stay
                # readable as gold objects; category dyes live on their base.
                v=13 if light<120 else 14 if light<180 else 15
            else:
                # Native category stairs: darker vertical risers, woven tread.
                v=1 if light<90 else 10 if light<140 else 11 if light<195 else 12
                if v==11 and x%4==0 and y%2==0:v=12
            im.putpixel((x,y),v)
    return im


def build():
    c=json.loads((OUT/'functional_contract.json').read_text())
    for rel,h in c['protected_hashes'].items():assert sha((ROOT/rel).read_bytes())==h,rel
    node,ls,ms=inventory();report={'base_commit':BASE,'protected_fixes':FIXES,'groups':{},'maps':{}}
    bodies={k:'' for k in ('graphics.h','metatiles.h','headers.h')}
    for key,g in GROUPS.items():
        p=reserve_dma(Pair(ROOT,c['maps'][g['names'][0]]['layout']))
        assert p.callbacks==['InitTilesetAnim_General','NULL']
        assert not any(e>>12==12 and e&1023 for a in p.meta for e in a),'Palette 12 already used'
        p.pals[12]=PALETTES[key]
        ids=sorted({v&1023 for n in g['names'] for k in ('blockdata_filepath','border_filepath') for v in words(ROOT/c['maps'][n]['layout'][k])})
        # Stage scripts never swap metatiles. Lobby flap swaps belong to its
        # already-adapted bank, protected here, not to these six stages.
        redrawn=[]
        for mid in ids:
            original=p.meta[mid>=512][mid%512*8:mid%512*8+8];result=[]
            for layer,native in enumerate(native_layers(p.reader,mid)):
                art=plane(native,key,mid,layer)
                for q,(dx,dy) in enumerate(((0,0),(8,0),(0,8),(8,8))):
                    e=original[layer*4+q]
                    if e&1023 in p.dynamic:result.append(e)
                    else:result.append(p.tile(art.crop((dx,dy,dx+8,dy+8)))|12<<12)
            p.meta[mid>=512][mid%512*8:mid%512*8+8]=result;redrawn.append(mid)
        paths=[ROOT/'data/tilesets'/kind/('arauna_contests08e_'+key) for kind in ('primary','secondary')]
        symbols=['AraunaContests08E'+g['suffix']+'Primary','AraunaContests08E'+g['suffix']]
        p.write(paths)
        for field,body in declarations(paths,symbols,p.callbacks).items():bodies[field]+=body
        report['groups'][key]={'names':list(g['names']),'style':key,'active_and_runtime_ids':ids,'runtime_ids':[],
            'redrawn_ids':redrawn,'new_graphics_slots':sorted(p.touched),'reserved_dma_slots':sorted(p.dynamic),
            'callbacks':p.callbacks,'banks':[str(path.relative_to(ROOT)) for path in paths]}
        for n in g['names']:
            l=ls[ms[n]['layout']];l['primary_tileset'],l['secondary_tileset']=['gTileset_'+s for s in symbols]
            report['maps'][n]={'width':l['width'],'height':l['height'],'cells':l['width']*l['height'],'group':key}
        dump(OUT/('checkpoint_'+key+'.json'),{'status':'ART_BUILT','group':key,**report['groups'][key]})
        print(key,len(redrawn),'redrawn IDs;',len(p.touched),'safe new graphics slots')
    for key,body in bodies.items():marked(ROOT/'src/data/tilesets'/key,TAG,body)
    dump(ROOT/'data/layouts/layouts.json',node);dump(OUT/'build.json',report)


def render():
    c=json.loads((OUT/'functional_contract.json').read_text());_,ls,ms=inventory();out=OUT/'renders';out.mkdir(exist_ok=True)
    font=ImageFont.truetype('DejaVuSans.ttf',13);board=Image.new('RGB',(768,448),'#202b30');d=ImageDraw.Draw(board)
    comparison=Image.new('RGB',(768,840),'#202b30');dc=ImageDraw.Draw(comparison)
    labels=['Palco comunitário / salão','Cool / urucum','Beauty / azul do litoral','Cute / tecido rosado','Smart / verde da mata','Tough / ocre e bronze']
    for i,n in enumerate(NAMES):
        before=native_render(c['maps'][n]['layout']);after=native_render(ls[ms[n]['layout']])
        before.save(out/(n+'-before.png'));after.save(out/(n+'.png'))
        individual=Image.new('RGB',(240,392),'#202b30');di=ImageDraw.Draw(individual)
        di.text((4,1),'Original',font=font,fill='white');individual.paste(before,(0,20))
        di.text((4,198),'Arauna 08E',font=font,fill='white');individual.paste(after,(0,216));individual.save(out/(n+'-comparison.png'))
        bx,by=8+i%3*256,8+i//3*212;d.text((bx,by),labels[i],font=font,fill='#e0c690');board.paste(after,(bx,by+24))
        cy=8+i//3*416;dc.text((bx,cy),labels[i]+' / original',font=font,fill='white');comparison.paste(before,(bx,cy+24))
        dc.text((bx,cy+206),'Arauna 08E',font=font,fill='#e0c690');comparison.paste(after,(bx,cy+228))
    d.text((8,430),'Renders RGB555 nativos sem atores; não são capturas do mGBA.',font=font,fill='white')
    board.save(out/'Arauna_08E_Preview.png');comparison.save(out/'Arauna_08E_Comparacao.png')
    print('Six full maps, six comparisons and combined before/after board')


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
    assert len(rows)==528 and len(node['layouts'])==754 and len(remaining)==5 and private==499
    with (OUT/'inventario_528_mapas.csv').open('w') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]),lineterminator='\n');w.writeheader();w.writerows(rows)
    dump(OUT/'fila_restante.json',{'maps':528,'layouts':754,'arauna_bank_maps':private,'native_remaining':remaining,
        'native_remaining_count':5,'pyramid_runtime_modules':16,'inactive_maps':8})
    print('Six read-only gates PASS; 499 Arauna bank maps; five native connection rooms remain')


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('action',choices=('freeze','build','render','gates'));globals()[p.parse_args().action]()
