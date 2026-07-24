#!/usr/bin/env python3
"""Render an Arauna map layout (map.bin) to a PNG preview.

No emulator needed: composites the tileset tiles + palettes + metatile
definitions exactly like the GBA does, so map edits can be verified visually.

Usage:
    python3 tools/arauna/render_map.py LAYOUT_ARAUNA_MAP_LAB -o /tmp/village.png
    python3 tools/arauna/render_map.py --bin data/layouts/X/map.bin \
        --primary primary/general --secondary secondary/petalburg -W 20 -H 20 -o out.png
"""
import argparse, json, struct
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parents[2]
NUM_PALS_IN_PRIMARY = 6
TILES_PER_ROW = 16  # tiles.png is 128px wide

def load_palettes(primary, secondary):
    pals = []
    for p in range(16):
        base = primary if p < NUM_PALS_IN_PRIMARY else secondary
        f = ROOT / "data/tilesets" / base / "palettes" / f"{p:02d}.pal"
        lines = f.read_text().splitlines()
        cols = [tuple(map(int, l.split())) for l in lines[3:19]]
        while len(cols) < 16:
            cols.append((0, 0, 0))
        pals.append(cols)
    return pals

def load_tiles(name):
    """Return list of 8x8 index grids for a tileset's tiles.png."""
    im = Image.open(ROOT / "data/tilesets" / name / "tiles.png")
    im = im.convert("P") if im.mode != "P" else im
    px = im.load()
    cols = im.width // 8
    rows = im.height // 8
    tiles = []
    for ty in range(rows):
        for tx in range(cols):
            t = [[px[tx * 8 + x, ty * 8 + y] for x in range(8)] for y in range(8)]
            tiles.append(t)
    return tiles

def load_metatiles(name):
    data = (ROOT / "data/tilesets" / name / "metatiles.bin").read_bytes()
    return [struct.unpack_from("<8H", data, i * 16) for i in range(len(data) // 16)]

def draw_tile(out, ox, oy, tile, entry, pals, opaque):
    tid = entry & 0x3FF
    xflip = (entry >> 10) & 1
    yflip = (entry >> 11) & 1
    pal = pals[(entry >> 12) & 0xF]
    for y in range(8):
        sy = 7 - y if yflip else y
        for x in range(8):
            sx = 7 - x if xflip else x
            idx = tile[sy][sx]
            if idx == 0 and not opaque:
                continue
            out[oy + y][ox + x] = pal[idx]

def render(map_bin, primary, secondary, W, H, scale=2):
    pals = load_palettes(primary, secondary)
    prim_tiles = load_tiles(primary)
    sec_tiles = load_tiles(secondary)
    blank = [[0] * 8 for _ in range(8)]
    def tile(tid):
        if tid < 512:
            return prim_tiles[tid] if tid < len(prim_tiles) else blank
        j = tid - 512
        return sec_tiles[j] if j < len(sec_tiles) else blank
    prim_mt = load_metatiles(primary)
    sec_mt = load_metatiles(secondary)
    def metatile(mid):
        return prim_mt[mid] if mid < 512 else sec_mt[mid - 512]
    grid = struct.unpack(f"<{W*H}H", Path(map_bin).read_bytes())
    px = [[(0, 0, 0) for _ in range(W * 16)] for _ in range(H * 16)]
    for y in range(H):
        for x in range(W):
            block = grid[y * W + x]
            mid = block & 0x3FF
            mt = metatile(mid)
            bx, by = x * 16, y * 16
            # positions: 0 TL,1 TR,2 BL,3 BR (per layer)
            offs = [(0, 0), (8, 0), (0, 8), (8, 8)]
            for layer in range(2):
                for i in range(4):
                    entry = mt[layer * 4 + i]
                    tid = entry & 0x3FF
                    if layer == 1 and tid == 0:
                        continue
                    dx, dy = offs[i]
                    draw_tile(px, bx + dx, by + dy, tile(tid), entry, pals, opaque=(layer == 0))
    img = Image.new("RGB", (W * 16, H * 16))
    img.putdata([c for row in px for c in row])
    if scale != 1:
        img = img.resize((img.width * scale, img.height * scale), Image.NEAREST)
    return img

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("layout", nargs="?", help="LAYOUT_ id from layouts.json")
    ap.add_argument("--bin"); ap.add_argument("--primary"); ap.add_argument("--secondary")
    ap.add_argument("-W", type=int); ap.add_argument("-H", type=int)
    ap.add_argument("-o", "--out", default="/tmp/map.png")
    ap.add_argument("-s", "--scale", type=int, default=2)
    a = ap.parse_args()
    if a.layout:
        layouts = json.loads((ROOT / "data/layouts/layouts.json").read_text())["layouts"]
        L = next(x for x in layouts if x["id"] == a.layout)
        a.bin = a.bin or L["blockdata_filepath"]
        a.primary = a.primary or L["primary_tileset"].replace("gTileset_", "")
        a.secondary = a.secondary or L["secondary_tileset"].replace("gTileset_", "")
        a.W, a.H = a.W or L["width"], a.H or L["height"]
    # tileset dir names: gTileset_General -> primary/general ; map by scanning
    def resolve(ts):
        import re
        snake = re.sub(r"(?<!^)(?=[A-Z])", "_", ts).lower()
        for cat in ("primary", "secondary"):
            if (ROOT / "data/tilesets" / cat / snake).is_dir():
                return f"{cat}/{snake}"
        raise SystemExit(f"tileset dir not found for {ts}")
    render(a.bin, resolve(a.primary), resolve(a.secondary), a.W, a.H, a.scale).save(a.out)
    print("wrote", a.out)

if __name__ == "__main__":
    main()
