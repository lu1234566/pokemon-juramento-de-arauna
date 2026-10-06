#!/usr/bin/env python3
"""Build seven scoped campaign rooms from original banks, without changing grids.

Pixel modules are native indexed craft art, following the project's existing
interior builders. All lower floor pixels are opaque. Palette 12 was unused in
every source bank; OBJ/primary/animated/door graphics are never overwritten.
"""
import json
import re
import shutil
import struct
from pathlib import Path

from PIL import Image, ImageDraw
from render_native_map import indexed_tiles, palette, words

ROOT = Path(__file__).resolve().parents[2]
BASE = '258195026b8e5d1a43bfb81fdf1480c02000c4b2'
MARK = 'CAMPANHA_INTERIORES_V1'
SPECS = {
    'carga': ('inside_of_truck', 'AraunaCargaV1', 'metal'),
    'briney': ('generic_building', 'AraunaBrineyV1', 'coast'),
    'flores': ('pretty_petal_flower_shop', 'AraunaFloresV1', 'garden'),
    'daycare': ('pokemon_day_care', 'AraunaDayCareV1', 'field'),
    'abrigo': ('generic_building', 'AraunaAbrigoChuvaV1', 'forest'),
    'clima': ('lab', 'AraunaInstitutoClimaV1', 'science'),
}
MAPS = {
    'InsideOfTruck': ('LAYOUT_INSIDE_OF_TRUCK', 'carga'),
    'Route104_MrBrineysHouse': ('LAYOUT_ROUTE104_MR_BRINEYS_HOUSE', 'briney'),
    'Route104_PrettyPetalFlowerShop': ('LAYOUT_ROUTE104_PRETTY_PETAL_FLOWER_SHOP', 'flores'),
    'Route117_PokemonDayCare': ('LAYOUT_ROUTE117_POKEMON_DAY_CARE', 'daycare'),
    'Route119_House': ('LAYOUT_HOUSE1', 'abrigo'),
    'Route119_WeatherInstitute_1F': ('LAYOUT_ROUTE119_WEATHER_INSTITUTE_1F', 'clima'),
    'Route119_WeatherInstitute_2F': ('LAYOUT_ROUTE119_WEATHER_INSTITUTE_2F', 'clima'),
}


def dump(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + '\n')


def art_palette(style):
    # 0 transparent; 1..5 materials; 6..8 paper/metal; 9..11 leaves;
    # 12..14 blue water/instruments; 15 brass. GBA-native multiples of eight.
    woods = {
        'coast': [(48, 40, 32), (128, 88, 56), (160, 120, 80), (104, 72, 48), (184, 144, 96)],
        'garden': [(48, 48, 32), (168, 128, 88), (192, 152, 112), (144, 104, 72), (216, 184, 144)],
        'field': [(56, 40, 32), (160, 112, 72), (184, 144, 96), (128, 88, 56), (208, 168, 112)],
        'forest': [(40, 48, 40), (112, 96, 64), (144, 128, 88), (80, 72, 48), (168, 152, 112)],
        'science': [(40, 56, 56), (96, 120, 112), (128, 152, 136), (72, 96, 96), (160, 176, 160)],
        'metal': [(40, 40, 48), (88, 96, 104), (112, 120, 120), (64, 72, 80), (144, 144, 136)],
    }
    return [(0, 0, 0)] + woods[style] + [(224, 216, 176), (184, 184, 152), (120, 136, 128),
            (48, 72, 48), (80, 112, 64), (136, 152, 80), (40, 80, 96),
            (64, 120, 136), (128, 168, 168), (192, 152, 72)]


def floor_art(style):
    im = Image.new('L', (16, 16), 2)
    p = im.load()
    for y in range(16):
        for x in range(16):
            if style == 'science':
                p[x, y] = 4 if x == 0 or y == 0 else 2
                if (x, y) in [(1, 1), (14, 14)]: p[x, y] = 5
            elif style == 'metal':
                p[x, y] = 3 if y in (0, 8) else 2
                if y in (3, 11) and x in (2, 3, 10, 11): p[x, y] = 4
            else:
                p[x, y] = 4 if y in (7, 15) else 2
                if x == (8 if y < 8 else 0): p[x, y] = 4
                if y % 8 == 0: p[x, y] = 3
                if (x, y) in [(3, 2), (12, 10), (6, 11)]: p[x, y] = 3
    return im


def chart_art(kind):
    im = Image.new('L', (32, 32), 0); d = ImageDraw.Draw(im)
    d.rectangle((1, 0, 30, 27), fill=4, outline=1)
    d.rectangle((3, 2, 28, 23), fill=6, outline=5)
    if kind == 'coast':
        d.polygon([(5, 4), (15, 4), (13, 10), (18, 13), (14, 19), (7, 21), (5, 21)], fill=10)
        d.line([(18, 4), (22, 8), (19, 13), (23, 19), (26, 21)], fill=13)
        d.line((7, 7, 14, 7), fill=9); d.line((7, 12, 11, 12), fill=9)
        d.ellipse((20, 6, 24, 10), outline=12); d.line((22, 5, 22, 11), fill=12)
    elif kind == 'science':
        d.line((5, 5, 5, 19), fill=8); d.line((5, 19, 25, 19), fill=8)
        for x, h in [(8, 8), (12, 11), (16, 6), (20, 13)]:
            d.rectangle((x, 18-h, x+2, 18), fill=13)
        d.line([(5, 10), (9, 7), (13, 11), (17, 6), (23, 9)], fill=9)
    else:
        d.rectangle((5, 5, 25, 19), fill=10)
        d.line([(5, 17), (9, 12), (16, 14), (21, 6), (25, 7)], fill=14, width=2)
    d.rectangle((2, 28, 29, 30), fill=4, outline=1)
    return im


class Bank:
    def __init__(self, key):
        self.key = key; source, self.symbol, self.style = SPECS[key]
        self.src = ROOT / 'data/tilesets/secondary' / source
        self.dst = ROOT / 'data/tilesets/secondary' / ('arauna_campanha_' + key + '_v1')
        self.dst.mkdir(parents=True, exist_ok=True)
        for p in (self.src/'palettes').glob('*.pal'):
            q = self.dst/'palettes'/p.name; q.parent.mkdir(exist_ok=True); shutil.copyfile(p, q)
        self.meta = words(self.src/'metatiles.bin'); self.original = list(self.meta)
        self.attrs = words(self.src/'metatile_attributes.bin')
        assert 12 not in {x >> 12 for x in self.meta}
        native, _, _ = indexed_tiles(self.src/'tiles.png')
        self.image = Image.new('P', (128, 256)); self.image.putpalette([v for i in range(256) for v in (i, i, i)])
        self.image.paste(native, (0, 0))
        used = {x & 1023 for x in self.meta}
        # Reserve the final door tile slots; these banks have no callback.
        self.pool = sorted(set(range(512, 992)) - used)
        self.cache = {}; self.allocated = []
        self.floor = floor_art(self.style)
        self.setpal(12, art_palette(self.style))
        # Retain index identities while giving existing architecture local
        # materials. Primary/device palettes are not recolored.
        for slot in (6, 7):
            old = palette(self.src/f'palettes/{slot:02}.pal'); new = []
            for i, (r, g, b) in enumerate(old):
                if i == 0 or self.key == 'carga': new.append((r, g, b)); continue
                lum = .299*r + .587*g + .114*b
                scales = (.94, .80, .62) if self.style in ('coast', 'field') else (.82, .92, .74)
                if self.style == 'science': scales = (.78, .91, .88)
                # Keep strongly chromatic device/flower colors recognizable.
                blend = .38 if max(r, g, b) - min(r, g, b) > 65 else .78
                target = [min(248, int((lum*s+12)//8)*8) for s in scales]
                new.append(tuple(int((a*(1-blend)+b*blend)//8)*8 for a, b in zip((r,g,b), target)))
            self.setpal(slot, new)

    def setpal(self, slot, colors):
        assert 6 <= slot <= 12 and len(colors) == 16
        text = 'JASC-PAL\r\n0100\r\n16\r\n' + ''.join('%d %d %d\r\n' % c for c in colors)
        (self.dst/f'palettes/{slot:02}.pal').write_bytes(text.encode())

    def tile(self, im):
        key = im.tobytes()
        if key not in self.cache:
            assert self.pool, (self.key, 'tile budget exceeded')
            number = self.pool.pop(0); self.cache[key] = number; self.allocated.append(number)
            self.image.paste(im, ((number-512)%16*8, (number-512)//16*8))
        return self.cache[key]

    def quadrants(self, im):
        return [self.tile(im.crop((x, y, x+8, y+8))) | 12 << 12 for x, y in [(0,0),(8,0),(0,8),(8,8)]]

    def replace_floor(self, mids):
        replacements = {}
        for mid in mids:
            old = self.original[(mid-512)*8:(mid-512)*8+4]
            new = self.quadrants(self.floor)
            for i, e in enumerate(old):
                assert (e & 1023) != 0, 'Do not alias the universal transparent tile'
                replacements[e & ~0xc00] = new[i]
        for i, e in enumerate(self.meta):
            # Floor beneath furniture changes with the architecture; upper
            # silhouettes and all attributes retain their original meaning.
            if (e & ~0xc00) in replacements:
                self.meta[i] = replacements[e & ~0xc00] | (e & 0xc00)
        for mid in mids:
            self.meta[(mid-512)*8:(mid-511)*8] = self.quadrants(self.floor) + [0]*4

    def module(self, mids, image):
        for y, row in enumerate(mids):
            for x, mid in enumerate(row):
                self.meta[(mid-512)*8:(mid-511)*8] = self.quadrants(self.floor) + self.quadrants(image.crop((16*x,16*y,16*x+16,16*y+16)))

    def redraw(self):
        if self.key == 'carga':
            # The truck is a 5x5 staged scene. Keep crate/door silhouettes and
            # every runtime door ID, replace only the two unobstructed floors.
            self.replace_floor([0x214, 0x21c])
            old = palette(self.src/'palettes/06.pal')
            colors = [(r, g, b) if i in (0,4,5,9,10,11,15) else
                      (min(248,int(r*.90)//8*8),min(248,int(g*.97)//8*8),min(248,int(b*.90)//8*8))
                      for i, (r,g,b) in enumerate(old)]
            self.setpal(6, colors)
            # A reinforced wooden cargo panel retains the upper crate mass.
            panel = Image.new('L',(32,16),2); d=ImageDraw.Draw(panel)
            d.rectangle((0,0,31,15),outline=1); d.line((0,7,31,7),fill=4)
            d.line((2,1,13,14),fill=5);d.line((18,1,29,14),fill=5)
            for x in (1,14,17,30): d.point((x,2),fill=6);d.point((x,13),fill=6)
            self.module(((0x203,0x204),),panel)
        elif self.key == 'briney':
            self.replace_floor([0x221, 0x229])
            self.module(((0x2c6,0x2c7),(0x2ce,0x2cf)),chart_art('coast'))
        elif self.key == 'flores':
            self.replace_floor([0x201,0x202,0x203,0x208,0x209,0x20a,0x20b,0x20c,0x22a])
            # The native live plants and flower containers stay recognizable;
            # wood flooring and sage shelving communicate a working nursery.
        elif self.key == 'daycare':
            self.replace_floor([0x201,0x206,0x207,0x219,0x226,0x233])
        elif self.key == 'abrigo':
            self.replace_floor([0x223,0x224,0x239])
            # Weather records on the old bookshelf footprint, away from NPCs.
            self.module(((0x281,), (0x282,)),chart_art('forest').resize((16,32),Image.Resampling.NEAREST))
        else:
            # Palette 10 belongs to the floor and its shadow quadrants. Keep
            # those native variants continuous with the new central panels;
            # the white columns/stairs use other palettes and retain their art.
            self.setpal(10, [(r,g,b) if i == 0 else
                            (int((r*.45+8)//8)*8, int((g*.56+8)//8)*8, int((b*.52+8)//8)*8)
                            for i,(r,g,b) in enumerate(palette(self.src/'palettes/10.pal'))])
            self.replace_floor([0x252,0x269])
            self.module(((0x22c,0x22d),(0x234,0x235)),chart_art('science'))

    def save(self):
        assert len(self.meta) == len(self.original) and all(e >> 12 <= 12 for e in self.meta)
        self.image.save(self.dst/'tiles.png', bits=4)
        (self.dst/'metatiles.bin').write_bytes(struct.pack('<%dH' % len(self.meta), *self.meta))
        shutil.copyfile(self.src/'metatile_attributes.bin', self.dst/'metatile_attributes.bin')
        return {'source':str(self.src.relative_to(ROOT)), 'target':str(self.dst.relative_to(ROOT)),
                'allocated_static_tiles':self.allocated, 'palette_12_previously_unused':True,
                'attributes_byte_identical':True, 'metatile_count':len(self.attrs),
                'changed_metatiles':[512+i for i in range(len(self.attrs)) if self.original[i*8:(i+1)*8] != self.meta[i*8:(i+1)*8]]}


def main():
    node = json.loads((ROOT/'data/layouts/layouts.json').read_text())
    originals = {l['id']:l for l in node['layouts']}
    banks = {key:Bank(key) for key in SPECS}
    for b in banks.values(): b.redraw()
    report = {'base_commit':BASE, 'maps':{}, 'banks':{k:b.save() for k,b in banks.items()}}
    for name, (layout, key) in MAPS.items():
        original = originals[layout]
        dest = ROOT/'data/layouts'/('AraunaCampanhaV1_'+name); dest.mkdir(exist_ok=True)
        for file, field in [('map.bin','blockdata_filepath'),('border.bin','border_filepath')]:
            shutil.copyfile(ROOT/original[field],dest/file)
        id = 'LAYOUT_ARAUNA_CAMPANHA_V1_'+re.sub(r'(?<=[a-z0-9])(?=[A-Z])','_',name).upper()
        record = dict(original, id=id, name='AraunaCampanhaV1_'+name+'_Layout',
                      secondary_tileset='gTileset_'+banks[key].symbol,
                      blockdata_filepath=str((dest/'map.bin').relative_to(ROOT)),
                      border_filepath=str((dest/'border.bin').relative_to(ROOT)))
        found=next((l for l in node['layouts'] if l['id']==id),None)
        if found: found.update(record)
        else: node['layouts'].append(record)
        path=ROOT/'data/maps'/name/'map.json'; m=json.loads(path.read_text());m['layout']=id;dump(path,m)
        report['maps'][name]={'original_layout':layout,'layout':id,'bank':key,'width':record['width'],'height':record['height']}
    dump(ROOT/'data/layouts/layouts.json',node)
    registrations = {'graphics.h':'', 'metatiles.h':'', 'headers.h':''}
    for b in banks.values():
        prefix=str(b.dst.relative_to(ROOT)); symbol=b.symbol
        registrations['graphics.h'] += f'const u32 gTilesetTiles_{symbol}[] = INCGFX_U32("{prefix}/tiles.png", ".4bpp.lz");\nconst u16 gTilesetPalettes_{symbol}[][16] =\n{{\n' + ''.join(f'    INCGFX_U16("{prefix}/palettes/{i:02}.pal", ".gbapal"),\n' for i in range(16))+'};\n'
        registrations['metatiles.h'] += f'const u16 gMetatiles_{symbol}[] = INCBIN_U16("{prefix}/metatiles.bin");\nconst u16 gMetatileAttributes_{symbol}[] = INCBIN_U16("{prefix}/metatile_attributes.bin");\n'
        registrations['headers.h'] += f'const struct Tileset gTileset_{symbol} =\n{{\n    .isCompressed = TRUE,\n    .isSecondary = TRUE,\n    .tiles = gTilesetTiles_{symbol},\n    .palettes = gTilesetPalettes_{symbol},\n    .metatiles = gMetatiles_{symbol},\n    .metatileAttributes = gMetatileAttributes_{symbol},\n    .callback = NULL,\n}};\n'
    for filename, body in registrations.items():
        path=ROOT/'src/data/tilesets'/filename
        clean=re.sub(r'\n*// '+MARK+r'_BEGIN\n.*?// '+MARK+r'_END\n','',path.read_text(),flags=re.S)
        path.write_text(clean.rstrip()+'\n\n// '+MARK+'_BEGIN\n'+body+'// '+MARK+'_END\n')
    dump(ROOT/'review/campanha_interiores_v1/build.json',report)
    print(json.dumps({'maps':len(MAPS),'banks':len(banks),'allocated_tiles':{k:len(b.allocated) for k,b in banks.items()}},indent=2))


if __name__ == '__main__': main()
