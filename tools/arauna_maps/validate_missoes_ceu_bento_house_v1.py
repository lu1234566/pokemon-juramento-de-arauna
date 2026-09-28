#!/usr/bin/env python3
"""Static geometry, movement and story guards for Casa de Bento."""
import collections, json, struct, subprocess
from pathlib import Path
from PIL import Image

ROOT=Path(__file__).resolve().parents[2]
NAME='MossdeepCity_StevensHouse'
SYMBOL='AraunaMissoesCeuBentoHouseV1'
ID='LAYOUT_ARAUNA_MISSOES_CEU_BENTO_HOUSE'
def words(p):
    b=p.read_bytes();return struct.unpack('<%dH'%(len(b)//2),b)
def main():
    original=json.loads(subprocess.check_output(['git','show','HEAD:data/maps/'+NAME+'/map.json'],cwd=ROOT))
    event=json.loads((ROOT/'data/maps'/NAME/'map.json').read_text())
    assert {**event,'layout':original['layout']}==original
    records=json.loads((ROOT/'data/layouts/layouts.json').read_text())['layouts']
    record=next(r for r in records if r['id']==ID)
    assert event['layout']==ID and record['secondary_tileset']=='gTileset_'+SYMBOL
    assert (record['width'],record['height'])==(11,8)
    old=words(ROOT/'data/layouts'/NAME/'map.bin')
    new=words(ROOT/record['blockdata_filepath'])
    assert len(old)==len(new)==88
    assert all((a&~0x3ff)==(b&~0x3ff) for a,b in zip(old,new))
    bank=ROOT/'data/tilesets/secondary/arauna_missoes_ceu_bento_house_v1'
    attr=words(bank/'metatile_attributes.bin')
    tiles=words(bank/'metatiles.bin')
    assert len(attr)>=242 and len(tiles)==len(attr)*8
    assert attr[0x2f1-0x200]==0x1000
    assert all(0x200<=v&0x3ff<0x200+len(attr) for v in new)
    assert Image.open(bank/'tiles.png').size==(128,256)
    script=(ROOT/'data/maps'/NAME/'scripts.inc').read_bytes()
    baseline=subprocess.check_output(['git','show','HEAD:data/maps/'+NAME+'/scripts.inc'],cwd=ROOT)
    assert script.split(b'MossdeepCity_StevensHouse_Text_YouveEarnedHMDive:',1)[0]==baseline.split(b'MossdeepCity_StevensHouse_Text_YouveEarnedHMDive:',1)[0], 'Os comandos do roteiro foram alterados'
    assert b'setmetatile 6, 4, METATILE_GenericBuilding_TableEdge, TRUE' in script
    for token in (b'MossdeepCity_StevensHouse_EventScript_StevenGivesDive',
                  b'MossdeepCity_StevensHouse_EventScript_BeldumPokeball',
                  b'MossdeepCity_StevensHouse_EventScript_Letter'):
        assert token in script
    assert [(w['x'],w['y'],w['dest_warp_id']) for w in event['warp_events']]==[(3,7,'6'),(4,7,'6')]
    assert [(o['x'],o['y']) for o in event['object_events']]==[(9,6),(4,3),(6,4)]
    # Bento walks horizontally from (9,6) to (3,6); his fixed return has
    # access through (3,5) and the original west-to-east corridor.
    assert all(not new[6*11+x]&0x400 for x in range(3,10))
    assert not new[5*11+3]&0x400
    blocked={(i%11,i//11) for i,v in enumerate(new) if v&0x400}
    blocked.update((o['x'],o['y']) for o in event['object_events'])
    seen={(3,6)};q=collections.deque(seen)
    while q:
        x,y=q.popleft()
        for p in ((x+1,y),(x-1,y),(x,y+1),(x,y-1)):
            if 0<=p[0]<11 and 0<=p[1]<8 and p not in blocked and p not in seen:
                seen.add(p);q.append(p)
    assert (4,7) in seen and (3,7) in seen
    for o in event['object_events']:
        x,y=o['x'],o['y']
        assert seen.intersection({(x+1,y),(x-1,y),(x,y+1),(x,y-1)})
    for header in ('graphics','metatiles','headers'):
        t=(ROOT/f'src/data/tilesets/{header}.h').read_text()
        assert t.count('// MISSOES_CEU_BENTO_HOUSE_V1_BEGIN')==t.count('// MISSOES_CEU_BENTO_HOUSE_V1_END')==1
        assert SYMBOL in t
    print(json.dumps({'status':'PASS','map':NAME,'cells':88,'reachable_cells':len(seen),
                      'script_commands_unchanged':True,'collision_elevation_unchanged':True,
                      'warps':2,'object_events':3,'script_table_metatile':hex(0x2f1)},indent=2))
if __name__=='__main__':main()
