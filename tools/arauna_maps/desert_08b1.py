#!/usr/bin/env python3
"""DesertRuins: native pixel art at unchanged functional metatile IDs."""
import argparse
import hashlib
import json
import re
import subprocess
from pathlib import Path

from PIL import Image, ImageDraw
from native_visuals_v2 import Pair, ROOT, declarations, dump, marked
from render_native_map import words, render_map
from trainer_hill_06a_art import native_layers

BASE = '393cdf63e4cef254d5890882df572f4011c69bf4'
INTEGRATED = 'a594b3e1e64517421101d96f5b314df22d47e14f'
OUT = ROOT / 'review/desert_08b1'
MUTABLE = {'data/layouts/layouts.json', *('src/data/tilesets/' + n for n in ('graphics.h', 'metatiles.h', 'headers.h'))}
TAG = 'DESERT_08B1'
BANKS = [ROOT / 'data/tilesets' / kind / 'arauna_desert08b1' for kind in ('primary', 'secondary')]
SYMBOLS = ['AraunaDesert08B1Primary', 'AraunaDesert08B1']
MATERIAL = [(0,0,0), (0,0,0), (48,40,32), (80,56,40), (120,80,48),
            (152,112,72), (184,144,96), (208,176,120), (232,208,152),
            (248,232,184), (56,64,64), (88,96,88), (136,144,120),
            (120,72,72), (200,168,120), (184,184,152)]
BRAILLE = {0x232, 0x235, 0x236, 0x237}
GLYPH = (205,172,123)


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def layout():
    node = json.loads((ROOT / 'data/layouts/layouts.json').read_text())
    return node, next(l for l in node['layouts'] if l['id'] == 'LAYOUT_DESERT_RUINS')


def freeze():
    assert subprocess.check_output(['git','rev-parse','HEAD'], cwd=ROOT, text=True).strip() == BASE
    tracked = subprocess.check_output(['git','ls-files','-z'], cwd=ROOT).decode().rstrip('\0').split('\0')
    node, l = layout()
    contract = {'base_commit': BASE, 'integrated_gameplay_base': INTEGRATED,
                'protected_hashes': {n: sha((ROOT/n).read_bytes()) for n in tracked if n not in MUTABLE},
                'registry_hashes': {n: sha((ROOT/n).read_bytes()) for n in sorted(MUTABLE)},
                'layout': l, 'layout_ids': [x['id'] for x in node['layouts']],
                'map': json.loads((ROOT/'data/maps/DesertRuins/map.json').read_text()),
                'scope': 'All existing tracked files except four additive graphics registries; no grid or gameplay changes.'}
    path = OUT / 'functional_contract.json'
    if path.exists():
        assert json.loads(path.read_text()) == contract, 'Frozen contract differs'
    else:
        dump(path, contract)
    print('Frozen', len(contract['protected_hashes']), 'existing files')


def floor():
    # A single seamless native module: broad offset lajedo plates, sparse wear.
    im = Image.new('L', (16,16), 7)
    d = ImageDraw.Draw(im)
    d.line((0,0,15,0), fill=6)
    d.line((0,1,15,1), fill=8)
    d.line((11,2,11,7), fill=6)
    d.line((0,8,15,8), fill=6)
    d.line((0,9,15,9), fill=8)
    d.line((3,10,3,15), fill=6)
    d.line((5,5,7,5), fill=8)
    d.point((13,12), fill=6)
    return im


def mineral(native, mid):
    """Retain per-layer silhouettes, replace surfaces with stratified sandstone."""
    im = Image.new('L', (16,16))
    for y in range(16):
        for x in range(16):
            r,g,b,a = native.getpixel((x,y))
            if not a:
                continue
            if (r,g,b) == (0,0,0):
                v = 1
            else:
                light = (r+g+b)//3
                v = 2 if light<65 else 3 if light<100 else 4 if light<135 else 5 if light<170 else 6 if light<200 else 8
                # Horizontal mineral strata replace the original diagonal hatching.
                if light >= 105 and y in (3,11):
                    v = max(3, v-1)
                if light >= 130 and y in (4,12):
                    v = min(8, v+1)
                if light >= 130 and x == (5 if y<8 else 13) and y not in (0,8):
                    v = max(3, v-1)
            if mid in BRAILLE and (r,g,b) == GLYPH:
                v = 14  # Exact original dots, at their original pixel coordinates.
            im.putpixel((x,y), v)
    return im


def build():
    contract = json.loads((OUT/'functional_contract.json').read_text())
    for n,h in contract['protected_hashes'].items():
        assert sha((ROOT/n).read_bytes()) == h, n
    node, l = layout()
    old = contract['layout']
    p = Pair(ROOT, old)
    p.dynamic.update(range(928,932))  # Cave's actual lava DMA destination.
    p.free = [i for i in p.free if i not in p.dynamic]
    p.tile_cache = {raw:i for i,raw in p.tiles.items() if i not in p.dynamic}
    p.pals[12] = MATERIAL
    ids = sorted({v&1023 for k in ('blockdata_filepath','border_filepath') for v in words(ROOT/old[k])}
                 | set(range(0x229,0x22d)) | set(range(0x232,0x238)))
    # Floor planes common to the native cave pieces are kept at their original
    # alpha masks. The six low boulders remain obstacles where collision says so.
    floor_entries = p.reader.secondary_metatiles[(0x201-512)*8:(0x201-512)*8+8]
    floor_tiles = {e&1023 for e in floor_entries if e&1023}
    ground = floor()
    for mid in ids:
        planes = []
        original_entries = p.meta[mid>=512][mid%512*8:mid%512*8+8]
        for layer, native in enumerate(native_layers(p.reader, mid)):
            art = mineral(native, mid)
            # Replace only pixels belonging to the old ground plane. This keeps
            # wall cutouts, openings and foreground overlap in the same layer.
            if mid not in BRAILLE and mid != 0x233:
                for y in range(16):
                    for x in range(16):
                        a = native.getpixel((x,y))[3]
                        quadrant = (y//8)*2+x//8
                        if a and original_entries[layer*4+quadrant]&1023 in floor_tiles:
                            art.putpixel((x,y), ground.getpixel((x,y)))
            planes.append(art)
        if mid == 0x201:
            planes[0] = ground.copy()
            # Preserve foreground transparency, including its native layer type.
            planes[1] = Image.new('L', (16,16))
        p.put(mid, planes[0], 12, (planes[1], 12))
    p.write(BANKS)
    for key, body in declarations(BANKS, SYMBOLS, p.callbacks).items():
        marked(ROOT/'src/data/tilesets'/key, TAG, body)
    l['primary_tileset'], l['secondary_tileset'] = ['gTileset_'+s for s in SYMBOLS]
    dump(ROOT/'data/layouts/layouts.json', node)
    dump(OUT/'build.json', {'base_commit':BASE, 'redrawn_ids':ids,
         'new_graphics_slots':sorted(p.touched), 'callbacks':p.callbacks,
         'banks':[str(b.relative_to(ROOT)) for b in BANKS],
         'palette':12, 'geometry':'unchanged 17x33, original map.bin and border.bin',
         'materials':['layered sandstone', 'weathered lajedo', 'original Braille dot geometry'],
         'script_runtime_ids':'closed and all six open IDs retained at native positions'})
    print('Built', len(ids), 'IDs;', len(p.touched), 'safe static graphics tiles')


def states(contract):
    grid = words(ROOT/contract['layout']['blockdata_filepath'])
    closed, opened = list(grid), list(grid)
    for x in range(7,10):
        closed[19*17+x] = (grid[19*17+x]&0xf000) | 0xc00 | 0x229
        closed[20*17+x] = (grid[20*17+x]&0xf000) | 0xc00 | 0x235
    for y, mids in ((19,(0x22a,0x22b,0x22c)), (20,(0x232,0x233,0x234))):
        for x, mid in zip(range(7,10), mids):
            opened[y*17+x] = (grid[y*17+x]&0xf000) | mid | (0xc00 if y==20 and x!=8 else 0)
    return {'closed':closed, 'open':opened}


def render():
    import struct
    contract = json.loads((OUT/'functional_contract.json').read_text())
    _, l = layout()
    before = Pair(ROOT, contract['layout']).reader
    after = Pair(ROOT, l).reader
    renders = OUT/'renders'
    renders.mkdir(parents=True, exist_ok=True)
    images = {}
    for state, grid in states(contract).items():
        path = renders / 'temporary-grid.bin'
        path.write_bytes(struct.pack('<%dH'%len(grid), *grid))
        old = render_map(before, path, 17,33)
        new = render_map(after, path, 17,33)
        old.save(renders/f'DesertRuins-{state}-before.png')
        new.save(renders/f'DesertRuins-{state}.png')
        comparison = Image.new('RGB', (552,528), '#18222a')
        comparison.paste(old,(0,0)); comparison.paste(new,(280,0))
        comparison.save(renders/f'comparacao-{state}.png')
        images[state] = new
    path.unlink()
    sheet = Image.new('RGB', (752,394), '#18222a')
    d = ImageDraw.Draw(sheet)
    for i,(label,state,x,y) in enumerate((('Inscrição / passagem selada','closed',8,22),
                                         ('Passagem aberta','open',8,22),
                                         ('Câmara de Regirock','open',8,7))):
        d.text((i*256+8,8), label, fill='white')
        crop = images[state].crop((x*16+8-120, y*16+8-80, x*16+8+120, y*16+8+80))
        sheet.paste(crop,(i*256,28))
    # Passage detail at integer zoom: the original inscription stays recognizable.
    detail = images['closed'].crop((6*16,18*16,11*16,21*16)).resize((320,192),Image.Resampling.NEAREST)
    sheet.paste(detail,(216,200))
    sheet.save(renders/'Arauna_08B1_Preview.png')
    atlas = Image.new('RGB',(8*80,((len(json.loads((OUT/'build.json').read_text())['redrawn_ids'])+7)//8)*100),'#18222a')
    d = ImageDraw.Draw(atlas)
    for i,mid in enumerate(json.loads((OUT/'build.json').read_text())['redrawn_ids']):
        x,y=(i%8)*80,(i//8)*100
        d.text((x+8,y+3),f'{mid:03X}',fill='white')
        atlas.paste(after.metatile(mid).resize((64,64),Image.Resampling.NEAREST).convert('RGB'),(x+8,y+20))
    atlas.save(renders/'metatiles.png')
    print('Rendered both functional states and three 240x160 native cameras')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=('freeze','build','render'))
    globals()[parser.parse_args().action]()
