#!/usr/bin/env python3
"""Check Shoal Cave's paired tide states, ice exception and event positions."""
import json,struct,subprocess
from PIL import Image
from build_gruta_da_mare_v1 import ROOT,MAPS,PRIMARY_HIGH,PRIMARY_LOW,SECONDARY,BASE,state,layout_id

def words(path):
    b=path.read_bytes();return struct.unpack('<%dH'%(len(b)//2),b)

def main():
    layout={r['id']:r for r in json.loads((ROOT/'data/layouts/layouts.json').read_text())['layouts']}
    source=ROOT/'data/tilesets/secondary/cave'
    original_meta=words(source/'metatiles.bin');original_attrs=words(source/'metatile_attributes.bin')
    for k,target in SECONDARY.items():
        meta=words(target/'metatiles.bin');attrs=words(target/'metatile_attributes.bin')
        assert meta[:len(original_meta)]==original_meta and attrs[:len(original_attrs)]==original_attrs
        assert len(attrs)==(414 if k=='gelo' else 415)
        assert Image.open(target/'tiles.png').size==((128,216) if k=='gelo' else (128,256))
        if k!='gelo':
            assert attrs[-1]==original_attrs[529-512]
            entries=meta[414*8:415*8]
            assert entries[:4]==original_meta[(529-512)*8:(529-512)*8+4]
            assert [v&1023 for v in entries[4:]]==list(range(0x3f8,0x3fc))
            assert all(v>>12==11 for v in entries[4:])
    for target in (PRIMARY_HIGH,PRIMARY_LOW):
        assert words(target/'metatiles.bin')==words(ROOT/'data/tilesets/primary/general/metatiles.bin')
    report={};warps=objects=0
    for name in MAPS:
        rel=f'data/maps/{name}/map.json'
        before=json.loads(subprocess.check_output(['git','show','HEAD:'+rel],cwd=ROOT))
        after=json.loads((ROOT/rel).read_text());new_id=layout_id(name)
        assert after=={**before,'layout':new_id}
        old=layout[before['layout']];new=layout[new_id]
        k=state(name);w,h=old['width'],old['height']
        assert (new['width'],new['height'])==(w,h)
        assert new['primary_tileset']==('gTileset_AraunaMareBaixa' if k=='baixa' else 'gTileset_AraunaMareAlta')
        assert new['secondary_tileset']=={'alta':'gTileset_AraunaMareRochaAlta',
                                          'baixa':'gTileset_AraunaMareRochaBaixa',
                                          'gelo':'gTileset_AraunaMareGelo'}[k]
        a=words(ROOT/old['blockdata_filepath']);b=words(ROOT/new['blockdata_filepath'])
        assert len(a)==len(b)==w*h
        changed=[]
        for i,(v,t) in enumerate(zip(a,b)):
            if v==t:continue
            x,y=i%w,i//w
            assert k!='gelo' and (v&1023,t&1023)==(529,BASE)
            assert (v^t)&~1023==0,(name,x,y,'collision/elevation changed')
            changed.append((x,y))
        occupied={(int(e['x']),int(e['y'])) for group in ('warp_events','object_events','coord_events','bg_events') for e in after[group]}
        assert not occupied.intersection(changed)
        assert (ROOT/old['border_filepath']).read_bytes()==(ROOT/new['border_filepath']).read_bytes()
        warps+=len(after['warp_events']);objects+=len(after['object_events'])
        report[name]={'state':k,'marks':len(changed)}
    assert warps==19 and objects==8,(warps,objects)
    assert sum(x['marks'] for x in report.values())==16
    print(json.dumps({'status':'PASS','maps':report,'warps':warps,'objects':objects,
                      'collision_and_events_preserved':True},indent=2))

if __name__=='__main__':main()
