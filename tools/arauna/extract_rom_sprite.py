#!/usr/bin/env python3
"""Decode a sprite out of the built ROM, the way the hardware would read it.

Checking the source PNGs proves the art is right. It does not prove the art
reached the cartridge: a graphic can be correct on disk and still be linked
against the wrong palette, incgfx'd at the wrong tile width, or shadowed by
another symbol. This reads the linked ROM instead -- looks the symbol up in
pokeemerald_modern.map, pulls the bytes at that address, and unpacks them as
the GBA would: 4bpp, 8x8 tiles, low nibble first, palette entry 0 transparent.

What comes out is what the console would put on screen, so a preview from
here can be compared against the source art and a mismatch means the wiring
is wrong rather than the drawing.

Usage:
    extract_rom_sprite.py --gfx gObjectEventPic_Roxanne \\
                          --pal gObjectEventPal_Dalva \\
                          --frames 9 --tiles-wide 2 --tiles-high 4 \\
                          --out preview.png
"""
from __future__ import annotations

import argparse
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DEFAULT_ROM = ROOT / "pokeemerald_modern.gba"
DEFAULT_MAP = ROOT / "pokeemerald_modern.map"

ROM_BASE = 0x08000000
SYMBOL = re.compile(r"^\s+0x0*([0-9a-f]{8})\s+(\w+)\s*$", re.M)


def symbols(map_path: Path) -> dict[str, int]:
    found: dict[str, int] = {}
    for address, name in SYMBOL.findall(map_path.read_text(encoding="utf-8",
                                                           errors="ignore")):
        found.setdefault(name, int(address, 16))
    return found


def rom_slice(rom: bytes, address: int, length: int) -> bytes:
    offset = address - ROM_BASE
    if offset < 0 or offset + length > len(rom):
        raise SystemExit(f"address {address:#010x} is outside the ROM")
    return rom[offset:offset + length]


def read_palette(rom: bytes, address: int) -> list[tuple[int, int, int]]:
    """Sixteen BGR555 entries, expanded to 8-bit RGB the way the GBA shows them."""
    raw = rom_slice(rom, address, 32)
    colors = []
    for i in range(16):
        value = raw[i * 2] | (raw[i * 2 + 1] << 8)
        r, g, b = value & 31, (value >> 5) & 31, (value >> 10) & 31
        colors.append((r * 255 // 31, g * 255 // 31, b * 255 // 31))
    return colors


def lz77_decompress(rom: bytes, address: int) -> bytes:
    """The BIOS LZ77 variant the GBA uses for compressed sprite sheets.

    Header byte 0x10, then a 24-bit decompressed length, then blocks of one
    flag byte followed by eight items: a literal byte, or a back-reference of
    3..18 bytes from up to 4096 back.
    """
    offset = address - ROM_BASE
    header = int.from_bytes(rom[offset:offset + 4], "little")
    if header & 0xFF != 0x10:
        raise SystemExit(f"{address:#010x} is not LZ77-compressed")
    size = header >> 8
    out = bytearray()
    pos = offset + 4
    while len(out) < size:
        flags = rom[pos]
        pos += 1
        for bit in range(8):
            if len(out) >= size:
                break
            if flags & (0x80 >> bit):
                pair = (rom[pos] << 8) | rom[pos + 1]
                pos += 2
                length = (pair >> 12) + 3
                back = (pair & 0x0FFF) + 1
                for _ in range(length):
                    out.append(out[-back])
            else:
                out.append(rom[pos])
                pos += 1
    return bytes(out[:size])


def read_pointer(rom: bytes, address: int) -> int:
    return int.from_bytes(rom_slice(rom, address, 4), "little")


def decode_tiles(data: bytes) -> list[list[list[int]]]:
    """4bpp 8x8 tiles into per-tile rows of palette indices, low nibble first."""
    tiles = []
    for base in range(0, len(data), 32):
        chunk = data[base:base + 32]
        if len(chunk) < 32:
            break
        rows = []
        for y in range(8):
            row = []
            for x in range(4):
                byte = chunk[y * 4 + x]
                row.append(byte & 0x0F)
                row.append(byte >> 4)
            rows.append(row)
        tiles.append(rows)
    return tiles


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--gfx", help="graphics symbol name")
    parser.add_argument("--pal", help="palette symbol name")
    parser.add_argument(
        "--trainer-pic", type=int,
        help="TRAINER_PIC_* index; reads gTrainerFrontPicTable and its "
             "palette table instead of a pair of symbols, and decompresses "
             "the LZ77 the front pics are stored in")
    parser.add_argument("--frames", type=int, default=1)
    parser.add_argument("--tiles-wide", type=int, default=2)
    parser.add_argument("--tiles-high", type=int, default=4)
    parser.add_argument("--out", required=True)
    parser.add_argument("--rom", default=str(DEFAULT_ROM))
    parser.add_argument("--map", dest="map_path", default=str(DEFAULT_MAP))
    parser.add_argument("--scale", type=int, default=1)
    args = parser.parse_args()

    from PIL import Image  # noqa: PLC0415  -- optional dependency, only here

    rom = Path(args.rom).read_bytes()
    table = symbols(Path(args.map_path))

    if args.trainer_pic is not None:
        # struct CompressedSpriteSheet { const u32 *data; u16 size; u16 tag; }
        # and CompressedSpritePalette { const u32 *data; u16 tag; }, both
        # eight bytes wide, so the index scales straight into each table.
        for name in ("gTrainerFrontPicTable", "gTrainerFrontPicPaletteTable"):
            if name not in table:
                raise SystemExit(f"{name} is not in {args.map_path}")
        gfx_ptr = read_pointer(rom, table["gTrainerFrontPicTable"]
                               + args.trainer_pic * 8)
        pal_ptr = read_pointer(rom, table["gTrainerFrontPicPaletteTable"]
                               + args.trainer_pic * 8)
        data = lz77_decompress(rom, gfx_ptr)
        palette_bytes = lz77_decompress(rom, pal_ptr)
        palette = []
        for i in range(16):
            value = palette_bytes[i * 2] | (palette_bytes[i * 2 + 1] << 8)
            r, g, b = value & 31, (value >> 5) & 31, (value >> 10) & 31
            palette.append((r * 255 // 31, g * 255 // 31, b * 255 // 31))
        source = (f"TRAINER_PIC {args.trainer_pic} -> gfx {gfx_ptr:#010x} "
                  f"pal {pal_ptr:#010x}")
    else:
        if not args.gfx or not args.pal:
            parser.error("pass --gfx and --pal, or --trainer-pic")
        for name in (args.gfx, args.pal):
            if name not in table:
                raise SystemExit(f"{name} is not in {args.map_path}")
        palette = read_palette(rom, table[args.pal])
        per_frame = args.tiles_wide * args.tiles_high
        data = rom_slice(rom, table[args.gfx], per_frame * args.frames * 32)
        source = (f"{args.gfx} @ {table[args.gfx]:#010x} with {args.pal} "
                  f"@ {table[args.pal]:#010x}")

    per_frame = args.tiles_wide * args.tiles_high
    tiles = decode_tiles(data)

    tile_w, tile_h = args.tiles_wide, args.tiles_high
    frame_w, frame_h = tile_w * 8, tile_h * 8
    sheet = Image.new("RGBA", (frame_w * args.frames, frame_h), (0, 0, 0, 0))

    for frame in range(args.frames):
        for index in range(per_frame):
            tile = tiles[frame * per_frame + index]
            # A frame is one -mwidth x -mheight metatile, and gbagfx walks a
            # metatile row by row: the top row of tiles left to right, then
            # the row under it.
            ty, tx = divmod(index, tile_w)
            for y, row in enumerate(tile):
                for x, entry in enumerate(row):
                    if entry == 0:
                        continue  # index 0 is the transparent one
                    r, g, b = palette[entry]
                    sheet.putpixel((frame * frame_w + tx * 8 + x,
                                    ty * 8 + y), (r, g, b, 255))

    if args.scale > 1:
        sheet = sheet.resize((sheet.width * args.scale,
                              sheet.height * args.scale), Image.NEAREST)
    sheet.save(args.out)
    print(f"{source} -> {args.out} "
          f"({args.frames} frames of {frame_w}x{frame_h})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
