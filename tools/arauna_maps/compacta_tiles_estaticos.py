#!/usr/bin/env python3
"""Free duplicate static tiles by reusing Emerald's hardware flip flags.

Keeps the PNG and attributes unchanged. Primary-bank references are pinned.
Refuses secondary callbacks with animation, whose VRAM slots can change.
"""
import argparse
import json
import re
import struct
from pathlib import Path
from PIL import Image
from bancos_nativos import resolve_bank, normalized, Renderer

ROOT = Path(__file__).resolve().parents[2]

def flip(tile, flags):
    return tuple(tile[(7-y if flags & 2 else y)*8 + (7-x if flags & 1 else x)]
                 for y in range(8) for x in range(8))

def compact(symbol, apply=False):
    header = (ROOT/'src/data/tilesets/headers.h').read_text()
    body = re.search(r'const struct Tileset '+re.escape(symbol)+r'\s*=\s*\{(.*?)\};', header, re.S)[1]
    if not re.search(r'\.isSecondary\s*=\s*TRUE', body):
        raise ValueError('Only secondary banks can be compacted')
    callback = re.search(r'\.callback\s*=\s*(\w+)', body)[1]
    if callback != 'NULL':
        anim = (ROOT/'src/tileset_anims.c').read_text()
        function = re.search(r'void '+callback+r'\(void\)\s*\{([^{}]*)\}', anim)
        if not function or not re.search(r'sSecondaryTilesetAnimCallback\s*=\s*NULL', function[1]):
            raise ValueError('Bank callback writes animated VRAM')
    layouts = json.loads((ROOT/'data/layouts/layouts.json').read_text())['layouts']
    primaries = {l['primary_tileset'] for l in layouts if l['secondary_tileset'] == symbol}
    path = resolve_bank(ROOT, symbol)
    image = Image.open(path/'tiles.png')
    assert image.mode == 'P' and max(image.getdata()) <= 15
    tiles = [tuple(image.crop((x,y,x+8,y+8)).getdata())
             for y in range(0,image.height,8) for x in range(0,image.width,8)]
    pinned = set()
    for primary in primaries:
        raw = (resolve_bank(ROOT, primary)/'metatiles.bin').read_bytes()
        pinned.update((word & 1023)-512 for (word,) in struct.iter_unpack('<H',raw) if (word & 1023)>=512)
    lookup = {}
    # Pinned tiles cannot be moved or overwritten.
    for i in sorted(pinned):
        if i < len(tiles):
            for flags in range(4): lookup.setdefault(flip(tiles[i], flags), (i, flags))
    replacements = {}
    for i, tile in enumerate(tiles):
        if i in pinned: continue
        if tile in lookup:
            replacements[i] = lookup[tile]
        else:
            for flags in range(4): lookup.setdefault(flip(tile, flags), (i, flags))
    before = (path/'metatiles.bin').read_bytes()
    after = bytearray(before)
    changed = 0
    for offset, (entry,) in enumerate(struct.iter_unpack('<H', before)):
        local = (entry & 1023)-512
        if local in replacements:
            tile, flags = replacements[local]
            replacement = ((entry & ~1023) ^ (flags << 10)) | (tile+512)
            struct.pack_into('<H', after, offset*2, replacement)
            changed += entry != replacement
    # Compare all definitions, including those visible only through caches.
    for primary in primaries:
        renderer = Renderer(resolve_bank(ROOT,primary),path)
        old = [normalized(renderer, 512+i) for i in range(len(before)//16)]
        renderer.secondary_metatiles = list(struct.unpack('<%dH'%(len(after)//2),after))
        # bank_words reads source files; check transformed tile layers directly.
        for i, layers in enumerate(old):
            actual=[]
            for entry in struct.unpack_from('<8H',after,i*16):
                tile=renderer._tile(entry & 1023)
                if tile is None: actual.append(('VRAM',entry & 1023,entry & 0xC00))
                else:
                    if entry & 0x400: tile=tile.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
                    if entry & 0x800: tile=tile.transpose(Image.Transpose.FLIP_TOP_BOTTOM)
                    actual.append(tile.tobytes())
            assert tuple(actual)==layers, (primary,i)
    used_before = {(e & 1023)-512 for (e,) in struct.iter_unpack('<H', before) if (e & 1023)>=512}
    used_after = {(e & 1023)-512 for (e,) in struct.iter_unpack('<H', after) if (e & 1023)>=512}
    report={'tileset':symbol, 'rewritten_entries':changed, 'freed_slots':sorted(used_before-used_after),
            'all_metatile_layers_identical':True, 'pinned_primary_slots':sorted(pinned), 'applied':apply}
    if apply: (path/'metatiles.bin').write_bytes(after)
    return report

if __name__ == '__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('tileset');parser.add_argument('--aplicar',action='store_true')
    args=parser.parse_args()
    print(json.dumps(compact(args.tileset,args.aplicar),indent=2))
