#!/usr/bin/env python3
"""Rebuild the title-screen background layer around the M'Boi serpent.

The layer is a 32x32 tilemap over a deduplicated tile bank, both authored
against the original art, so a freshly drawn image cannot simply replace
rayquaza.png -- the tilemap would reassemble the new tiles into noise, which
is exactly what happened the first time this was tried. This regenerates the
whole set together: tile bank, tilemap and shared palette.

The sky gradient is rebuilt from the band table below (measured off the
original background) rather than read back from rayquaza.png, so the tool is
idempotent and can be re-run to reposition the serpent.

The clouds share palette 14, so the serpent is drawn as a silhouette using
only roles the Rayquaza art already used plus two indices neither layer
touched, and the cloud indices (0, 2, 12) are left alone:

    index 11   darkest body      unchanged
    index  1   mid-dark body     unused by both layers, repainted here
    index  3   mid body          unused by both layers, repainted here
    index 15   markings          animated every 4th frame by
                                 UpdateLegendaryMarkingColor, so the belly
                                 line pulses gold on its own
    index  2   eye highlight     white, also a cloud colour

Usage:
    python3 tools/art/build_title_background.py [scale] [x] [y]
"""
import struct, sys
from PIL import Image

R = 'graphics/title_screen/'
MAX_TILES = 512      # char block 2 holds 512 4bpp tiles before the clouds bank

# (palette index, row count) down the screen, measured off the original art
SKY_BANDS = [(10, 14), (9, 16), (8, 16), (7, 22), (6, 25), (5, 31), (4, 36)]

RAMP = {1: 11, 2: 11, 3: 11, 4: 1, 5: 1, 6: 3, 7: 15, 8: 15, 9: 2}
NEW_PAL = {1: (0, 86, 108), 3: (0, 98, 118)}


def sky_rows():
    rows = []
    for idx, n in SKY_BANDS:
        rows += [idx] * n
    return rows + [0] * (256 - len(rows))


def build_index_map(scale, origin):
    sky = sky_rows()
    idx = [[0] * 256 for _ in range(256)]
    for y in range(256):
        for x in range(240):
            idx[y][x] = sky[y]
    mb = Image.open('art/title_screen/mboi_source.png')
    mb = mb.resize((int(mb.width * scale), int(mb.height * scale)), Image.NEAREST)
    mp = mb.load()
    ox, oy = origin
    for y in range(mb.height):
        ty = oy + y
        if not 0 <= ty < 256:
            continue
        for x in range(mb.width):
            tx = ox + x
            if not 0 <= tx < 240:
                continue
            s = mp[x, y]
            if s in RAMP:
                idx[ty][tx] = RAMP[s]
    return idx


def pack(idx):
    """Split into 8x8 tiles and dedup across h/v flips, as the original did."""
    bank, seen, tmap = [], {}, []
    for ty in range(32):
        for tx in range(32):
            t = tuple(tuple(idx[ty * 8 + y][tx * 8 + x] for x in range(8))
                      for y in range(8))
            hit = None
            for hf in (0, 1):
                for vf in (0, 1):
                    v = t
                    if hf:
                        v = tuple(r[::-1] for r in v)
                    if vf:
                        v = v[::-1]
                    if v in seen:
                        hit = (seen[v], hf, vf)
                        break
                if hit:
                    break
            if hit is None:
                seen[t] = len(bank)
                bank.append(t)
                hit = (len(bank) - 1, 0, 0)
            tid, hf, vf = hit
            tmap.append(tid | (hf << 10) | (vf << 11) | (14 << 12))
    return bank, tmap


def main(argv):
    scale = float(argv[0]) if argv else 1.15
    origin = (int(argv[1]), int(argv[2])) if len(argv) > 2 else (46, 49)

    bank, tmap = pack(build_index_map(scale, origin))
    if len(bank) > MAX_TILES:
        raise SystemExit('%d tiles exceeds the %d that fit in char block 2'
                         % (len(bank), MAX_TILES))

    pal = [tuple(int(c) for c in l.split())
           for l in open(R + 'rayquaza_and_clouds.pal').read().split('\n')[3:]
           if len(l.split()) == 3]
    for i, c in NEW_PAL.items():
        pal[i] = c

    cols = 16
    out = Image.new('P', (cols * 8, ((len(bank) + cols - 1) // cols) * 8), 0)
    flat = []
    for c in pal:
        flat += list(c)
    out.putpalette(flat + [0] * (768 - len(flat)))
    op = out.load()
    for i, t in enumerate(bank):
        bx, by = (i % cols) * 8, (i // cols) * 8
        for y in range(8):
            for x in range(8):
                op[bx + x, by + y] = t[y][x]
    out.save(R + 'rayquaza.png')
    open(R + 'rayquaza.bin', 'wb').write(struct.pack('<1024H', *tmap))
    # .gitattributes marks *.pal as eol=crlf, so write the file that way
    open(R + 'rayquaza_and_clouds.pal', 'w', newline='\r\n').write(
        '\n'.join(['JASC-PAL', '0100', '16'] + ['%d %d %d' % c for c in pal]) + '\n')
    print('scale %.2f at %s -> %d distinct tiles (cap %d), bank %dx%d'
          % (scale, origin, len(bank), MAX_TILES, out.width, out.height))


if __name__ == '__main__':
    main(sys.argv[1:])
