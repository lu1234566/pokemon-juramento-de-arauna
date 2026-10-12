#!/usr/bin/env python3
"""Check native story sheets, palette wiring and the honest Libras status."""
import importlib.util
import json
import re
import struct
from pathlib import Path
from PIL import Image

ROOT=Path(__file__).resolve().parents[2]
def main():
    spec=importlib.util.spec_from_file_location('character_qc',ROOT/'tools/validate_arauna_character_assets.py')
    module=importlib.util.module_from_spec(spec)
    import sys
    sys.modules[spec.name]=module;spec.loader.exec_module(module)
    info=(ROOT/'src/data/object_events/object_event_graphics_info.h').read_text()
    movement=(ROOT/'src/event_object_movement.c').read_text()
    pics=(ROOT/'src/data/object_events/object_event_pic_tables.h').read_text()
    decl=(ROOT/'src/data/object_events/object_event_graphics.h').read_text()
    for png,pal,sym,width,tag,gfx_var,map_name in [
        ('people/arauna/hermit','hermit','Hermit',16,'HERMIT','E','Sala'),
        ('pokemon/arauna/guaracim_pup','guaracim_pup','UivoPup',32,'UIVO_PUP','F','Refugio')]:
        p=ROOT/'graphics/object_events/pics'/(png+'.png');raw=p.read_bytes()
        assert raw[24:26]==bytes([4,3]),(png,'must be indexed 4-bit PNG')
        with Image.open(p) as image:
            assert image.size==(width*9,32) and image.mode=='P'
            pixels=module.flattened_pixels(image)
            assert image.info.get('transparency')==0 and max(pixels)<=15
            palette=image.getpalette()[:48]
            lines=(ROOT/'graphics/object_events/palettes'/(pal+'.pal')).read_text().splitlines()
            assert lines[:3]==['JASC-PAL','0100','16']
            assert [int(v) for line in lines[3:] for v in line.split()]==palette
            assert all(v%8==0 for v in palette),'palette must be RGB555 reproducible'
            frames=[image.crop((i*width,0,(i+1)*width,32)) for i in range(9)]
            assert all(f.getbbox() and f.getbbox()[3]==31 for f in frames)
            for a,b,idle in [(3,4,0),(5,6,1),(7,8,2)]:
                assert len({frames[i].tobytes() for i in (a,b,idle)})==3,(png,'dead walking pose')
            if width==16:
                metadata=module.parse_png(p)
                module.validate_overworld(pixels,metadata,str(p.relative_to(ROOT)))
        assert f'.images = sPicTable_{sym},' in info
        assert f'OBJ_EVENT_PAL_TAG_{tag}' in movement
        assert f'gObjectEventPic_{sym}' in pics and png+'.png' in decl
        map_path=ROOT/'data/maps'/('Arauna_CasaUivo_'+map_name)
        obj=json.loads((map_path/'map.json').read_text())['object_events'][0]
        assert obj['graphics_id']=='OBJ_EVENT_GFX_VAR_'+gfx_var
        assert f'setvar VAR_OBJ_GFX_ID_{gfx_var}, ARAUNA_VIRTUAL_GFX_{tag}' in (map_path/'scripts.inc').read_text()
        own_info=info.split('gObjectEventGraphicsInfo_'+sym+' = {',1)[1].split('};',1)[0]
        assert '.paletteSlot = PALSLOT_NPC_SPECIAL,' in own_info
        pool=movement.split('static const u16 sAraunaExclusivePaletteTags[] = {',1)[1].split('};',1)[0]
        assert 'OBJ_EVENT_PAL_TAG_'+tag not in pool
        if sym=='Hermit':
            # The room's remaining occupants use generic NPC slots. Weather
            # may reuse pool banks, so this isolated private slot is deliberate.
            others=json.loads((map_path/'map.json').read_text())['object_events'][1:]
            assert {o['graphics_id'] for o in others} <= {
                'OBJ_EVENT_GFX_LITTLE_GIRL','OBJ_EVENT_GFX_HIKER',
                'OBJ_EVENT_GFX_WOMAN_3','OBJ_EVENT_GFX_MAN_2'}
        if sym=='UivoPup':
            # This map has one object; its private special slot never competes
            # with another character. Creature sheets remain outside the human
            # 16x32 manifest, with their native 32x32 checks above.
            assert len(json.loads((map_path/'map.json').read_text())['object_events'])==1
            pup_info=info.split('gObjectEventGraphicsInfo_UivoPup = {',1)[1].split('};',1)[0]
            assert '.paletteSlot = PALSLOT_NPC_SPECIAL,' in pup_info
    review=json.loads((ROOT/'data/arauna/story/libras_review.json').read_text())
    if review['signed_scene_enabled']:
        assert review['translation_status']=='approved'
        for k in ('qualified_translator','deaf_signing_reviewer','translation_reference','review_reference','storyboard_reference'):
            assert review.get(k),('missing qualified review',k)
        assert review['approved_signed_assets']
        for p in review['approved_signed_assets']:assert (ROOT/p).is_file()
    else:
        assert review['runtime_mode']=='written_notebook' and not review['approved_signed_assets']
    print('Arauna story sheets and Libras status: PASS (signed scene '+('approved' if review['signed_scene_enabled'] else 'pending qualified human review')+').')
if __name__=='__main__':main()
