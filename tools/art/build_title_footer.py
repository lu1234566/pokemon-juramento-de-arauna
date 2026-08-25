#!/usr/bin/env python3
"""Rewrite the footer line on the title screen.

press_start.png is a 160x24 sprite sheet: rows 0-7 are "PRESS START" and rows
8-15 are the line under it, which shipped as Emerald's "(C)2005 GAMEFREAK
inc." That notice is false on a fan work, so it is replaced with a fan-game
disclaimer here.

The original glyphs are kerned with shared outlines, so individual letters
cannot be lifted out of the sheet -- and the letters needed (N, O, L, T ...)
are not all present in the two lines anyway. The text is drawn instead from
the 5x5 font below and then given the same treatment as the original: a 1px
black outline and a three-step vertical gradient, which comes out 7 rows
tall and pixel-compatible with the row it replaces.

    python3 tools/art/build_title_footer.py ["YOUR TEXT"]
"""
import sys
from PIL import Image

SHEET = 'graphics/title_screen/press_start.png'
ROW, HEIGHT, WIDTH = 8, 8, 160
OUTLINE, LIGHT, MID, DARK = 1, 5, 4, 3      # palette indices in the sheet
GRADIENT = [LIGHT, LIGHT, MID, DARK, DARK]  # one entry per core row

FONT = {
    'A': ('.###.', '#...#', '#####', '#...#', '#...#'),
    'B': ('####.', '#...#', '####.', '#...#', '####.'),
    'C': ('.####', '#....', '#....', '#....', '.####'),
    'D': ('####.', '#...#', '#...#', '#...#', '####.'),
    'E': ('#####', '#....', '####.', '#....', '#####'),
    'F': ('#####', '#....', '####.', '#....', '#....'),
    'G': ('.####', '#....', '#..##', '#...#', '.####'),
    'H': ('#...#', '#...#', '#####', '#...#', '#...#'),
    'I': ('#####', '..#..', '..#..', '..#..', '#####'),
    'J': ('....#', '....#', '....#', '#...#', '.###.'),
    'K': ('#...#', '#..#.', '###..', '#..#.', '#...#'),
    'L': ('#....', '#....', '#....', '#....', '#####'),
    'M': ('#...#', '##.##', '#.#.#', '#...#', '#...#'),
    'N': ('#...#', '##..#', '#.#.#', '#..##', '#...#'),
    'O': ('.###.', '#...#', '#...#', '#...#', '.###.'),
    'P': ('####.', '#...#', '####.', '#....', '#....'),
    'Q': ('.###.', '#...#', '#...#', '#..#.', '.##.#'),
    'R': ('####.', '#...#', '####.', '#..#.', '#...#'),
    'S': ('.####', '#....', '.###.', '....#', '####.'),
    'T': ('#####', '..#..', '..#..', '..#..', '..#..'),
    'U': ('#...#', '#...#', '#...#', '#...#', '.###.'),
    'V': ('#...#', '#...#', '#...#', '.#.#.', '..#..'),
    'W': ('#...#', '#...#', '#.#.#', '##.##', '#...#'),
    'X': ('#...#', '.#.#.', '..#..', '.#.#.', '#...#'),
    'Y': ('#...#', '.#.#.', '..#..', '..#..', '..#..'),
    'Z': ('#####', '...#.', '..#..', '.#...', '#####'),
    '0': ('.###.', '#..##', '#.#.#', '##..#', '.###.'),
    '1': ('..#..', '.##..', '..#..', '..#..', '.###.'),
    '2': ('####.', '....#', '.###.', '#....', '#####'),
    '3': ('####.', '....#', '.###.', '....#', '####.'),
    '4': ('#..#.', '#..#.', '#####', '...#.', '...#.'),
    '5': ('#####', '#....', '####.', '....#', '####.'),
    '6': ('.###.', '#....', '####.', '#...#', '.###.'),
    '7': ('#####', '....#', '...#.', '..#..', '..#..'),
    '8': ('.###.', '#...#', '.###.', '#...#', '.###.'),
    '9': ('.###.', '#...#', '.####', '....#', '.###.'),
    '-': ('.....', '.....', '.###.', '.....', '.....'),
    '.': ('.....', '.....', '.....', '.....', '..#..'),
    ',': ('.....', '.....', '.....', '..#..', '.#...'),
    "'": ('..#..', '..#..', '.....', '.....', '.....'),
    ' ': ('.....', '.....', '.....', '.....', '.....'),
}
PITCH = 6   # 5 core columns plus one, so adjacent outlines merge as they did


def core_mask(text):
    """{(x, y): True} for the lit core pixels of the whole line."""
    out = {}
    for i, ch in enumerate(text):
        g = FONT.get(ch.upper())
        if g is None:
            raise SystemExit('no glyph for %r' % ch)
        for y, row in enumerate(g):
            for x, c in enumerate(row):
                if c == '#':
                    out[(i * PITCH + x, y)] = True
    return out


def main(argv):
    text = argv[0] if argv else 'FAN GAME - NOT FOR SALE'
    core = core_mask(text)
    span = (len(text) - 1) * PITCH + 5
    if span + 2 > WIDTH:
        raise SystemExit('%r needs %dpx, the strip is %d' % (text, span + 2, WIDTH))
    ox = (WIDTH - span) // 2
    oy = ROW + 1                       # leave a row for the outline above

    im = Image.open(SHEET)
    px = im.load()
    for y in range(ROW, ROW + HEIGHT):
        for x in range(WIDTH):
            px[x, y] = 0

    for (cx, cy) in core:              # outline first, fill paints over it
        for dy in (-1, 0, 1):
            for dx in (-1, 0, 1):
                if (cx + dx, cy + dy) not in core:
                    px[ox + cx + dx, oy + cy + dy] = OUTLINE
    for (cx, cy) in core:
        px[ox + cx, oy + cy] = GRADIENT[cy]

    im.save(SHEET)
    print('%r -> %dpx, drawn at x=%d in the %dpx strip' % (text, span, ox, WIDTH))


if __name__ == '__main__':
    main(sys.argv[1:])
