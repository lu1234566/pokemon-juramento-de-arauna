#!/usr/bin/env python3
"""Pack all 386 Arauna sprites into one build-ready C graphics header.

This compact representation keeps the GitHub change reviewable and avoids adding
thousands of generated PNG paths.  Battle images use standard GBA LZ77 data;
icons and palettes remain uncompressed, matching pokeemerald-expansion's loaders.
The editable indexed PNG packages are kept separately in a ZIP archive.
"""

from __future__ import annotations

import argparse
import csv
import shutil
import struct
from pathlib import Path

from PIL import Image


def gba_4bpp(image: Image.Image) -> bytes:
    if image.mode != "P" or image.width % 8 or image.height % 8:
        raise ValueError(f"expected indexed tile-aligned image, got {image.mode} {image.size}")
    pixels = image.load()
    out = bytearray()
    for tile_y in range(0, image.height, 8):
        for tile_x in range(0, image.width, 8):
            for y in range(8):
                for x in range(0, 8, 2):
                    lo = int(pixels[tile_x + x, tile_y + y])
                    hi = int(pixels[tile_x + x + 1, tile_y + y])
                    if lo > 15 or hi > 15:
                        raise ValueError("4bpp image uses a palette index above 15")
                    out.append(lo | (hi << 4))
    return bytes(out)


def lz77_compress(data: bytes) -> bytes:
    """Encode BIOS-compatible type-0x10 LZ77 with a 4 KiB window."""
    out = bytearray((0x10, len(data) & 0xFF, (len(data) >> 8) & 0xFF, (len(data) >> 16) & 0xFF))
    positions: dict[bytes, list[int]] = {}
    pos = 0
    while pos < len(data):
        flag_pos = len(out)
        out.append(0)
        flags = 0
        for bit in range(8):
            if pos >= len(data):
                break
            best_len = 0
            best_disp = 0
            key = data[pos:pos + 3]
            if len(key) == 3:
                candidates = positions.get(key, [])
                for previous in reversed(candidates[-96:]):
                    disp = pos - previous
                    if disp > 4096:
                        continue
                    length = 3
                    while length < 18 and pos + length < len(data) and data[previous + length] == data[pos + length]:
                        length += 1
                    if length > best_len:
                        best_len, best_disp = length, disp
                        if length == 18:
                            break
            if best_len >= 3:
                flags |= 1 << (7 - bit)
                encoded = best_disp - 1
                out.append(((best_len - 3) << 4) | ((encoded >> 8) & 0xF))
                out.append(encoded & 0xFF)
                consumed = best_len
            else:
                out.append(data[pos])
                consumed = 1
            for index in range(pos, min(len(data), pos + consumed)):
                if index + 3 <= len(data):
                    item = data[index:index + 3]
                    bucket = positions.setdefault(item, [])
                    bucket.append(index)
                    while bucket and index - bucket[0] > 4096:
                        bucket.pop(0)
            pos += consumed
        out[flag_pos] = flags
    while len(out) % 4:
        out.append(0)
    return bytes(out)


def lz77_decompress(data: bytes) -> bytes:
    if data[0] != 0x10:
        raise ValueError("invalid LZ77 header")
    size = data[1] | data[2] << 8 | data[3] << 16
    out = bytearray()
    pos = 4
    while len(out) < size:
        flags = data[pos]; pos += 1
        for bit in range(8):
            if len(out) >= size:
                break
            if flags & (1 << (7 - bit)):
                first, second = data[pos], data[pos + 1]; pos += 2
                length = (first >> 4) + 3
                disp = ((first & 0xF) << 8 | second) + 1
                for _ in range(length):
                    out.append(out[-disp])
            else:
                out.append(data[pos]); pos += 1
    return bytes(out[:size])


def read_palette(path: Path) -> list[int]:
    lines = path.read_text(encoding="ascii").replace("\r", "").splitlines()
    colors = [tuple(map(int, line.split())) for line in lines[3:19]]
    if len(colors) != 16:
        raise ValueError(f"expected 16 palette colors in {path}")
    return [((r >> 3) | ((g >> 3) << 5) | ((b >> 3) << 10)) for r, g, b in colors]


def c_array(name: str, c_type: str, data: bytes | list[int], width: int) -> str:
    if isinstance(data, bytes):
        if c_type == "u32":
            values = [struct.unpack_from("<I", data, offset)[0] for offset in range(0, len(data), 4)]
        else:
            values = list(data)
    else:
        values = data
    digits = {"u8": 2, "u16": 4, "u32": 8}[c_type]
    per_line = {"u8": 16, "u16": 8, "u32": 8}[c_type]
    lines = []
    for start in range(0, len(values), per_line):
        group = ", ".join(f"0x{value:0{digits}X}" for value in values[start:start + per_line])
        lines.append(f"    {group},")
    return f"const {c_type} {name}[] __attribute__((aligned({width}))) =\n{{\n" + "\n".join(lines) + "\n};\n"


def replace_graphics_symbols(block: str, number: int) -> str:
    replacements = {
        ".frontPic": f"gAraunaFrontPic_{number:03d}",
        ".backPic": f"gAraunaBackPic_{number:03d}",
        ".palette": f"gAraunaPalette_{number:03d}",
        ".shinyPalette": f"gAraunaShinyPalette_{number:03d}",
        ".iconSprite": f"gAraunaIcon_{number:03d}",
    }
    lines = block.splitlines()
    for index, line in enumerate(lines):
        for field_name, symbol in replacements.items():
            if line.lstrip().startswith(field_name + " ="):
                indent = line[:len(line) - len(line.lstrip())]
                lines[index] = f"{indent}{field_name} = {symbol},"
                break
    return "\n".join(lines)


def species_blocks(path: Path) -> list[str]:
    text = path.read_text(encoding="utf-8")
    starts = [match.start() for match in __import__("re").finditer(r"^\s*\[SPECIES_[A-Z0-9_]+\]\s*=", text, __import__("re").MULTILINE)]
    starts.append(len(text))
    prefix = text[:starts[0]]
    blocks = [text[starts[i]:starts[i + 1]].rstrip() for i in range(len(starts) - 1)]
    if len(blocks) != 386:
        raise ValueError(f"expected 386 species blocks, got {len(blocks)}")
    blocks[0] = prefix + replace_graphics_symbols(blocks[0], 1)
    for index in range(1, 386):
        blocks[index] = replace_graphics_symbols(blocks[index], index + 1)
    return blocks


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--packages", type=Path, default=Path("art_candidates/full_dex/gba"))
    parser.add_argument("--mapping", type=Path, default=Path("full_dex_build/repo_overlay/docs/arauna/ARAUNA_DEX_ENGINE_MAPPING.csv"))
    parser.add_argument("--editable-species", type=Path, default=Path("full_dex_build/repo_overlay/src/data/pokemon/species_info/arauna_dex.h"))
    parser.add_argument("--species-info", type=Path, default=Path("full_dex_build/repo_overlay/src/data/pokemon/species_info.h"))
    parser.add_argument("--pokemon-graphics", type=Path, default=Path("engine-reference/src/data/graphics/pokemon.h"))
    parser.add_argument("--docs", type=Path, default=Path("full_dex_build/repo_overlay/docs/arauna"))
    parser.add_argument("--out", type=Path, default=Path("full_dex_build/publish_overlay"))
    args = parser.parse_args()

    mapping = list(csv.DictReader(args.mapping.open(encoding="utf-8")))
    folders = sorted(path for path in args.packages.iterdir() if path.is_dir())
    if len(mapping) != 386 or len(folders) != 386:
        raise ValueError("mapping and package directory must both contain 386 entries")

    graphics_parts = ["// Auto-generated packed Arauna GBA graphics.\n"]
    raw_total = compressed_total = 0
    for number, folder in enumerate(folders, start=1):
        front_raw = gba_4bpp(Image.open(folder / "anim_front.png"))
        back_raw = gba_4bpp(Image.open(folder / "back.png"))
        icon_raw = gba_4bpp(Image.open(folder / "icon.png"))
        front = lz77_compress(front_raw)
        back = lz77_compress(back_raw)
        assert lz77_decompress(front) == front_raw and lz77_decompress(back) == back_raw
        raw_total += len(front_raw) + len(back_raw)
        compressed_total += len(front) + len(back)
        graphics_parts.extend((
            c_array(f"gAraunaFrontPic_{number:03d}", "u32", front, 4),
            c_array(f"gAraunaBackPic_{number:03d}", "u32", back, 4),
            c_array(f"gAraunaPalette_{number:03d}", "u16", read_palette(folder / "normal.pal"), 2),
            c_array(f"gAraunaShinyPalette_{number:03d}", "u16", read_palette(folder / "shiny.pal"), 2),
            c_array(f"gAraunaIcon_{number:03d}", "u8", icon_raw, 4),
        ))
    graphics_path = args.out / "src/data/graphics/arauna_fakemon_graphics.h"
    graphics_path.parent.mkdir(parents=True, exist_ok=True)
    graphics_path.write_text("\n".join(graphics_parts), encoding="ascii")

    dex_path = args.out / "src/data/pokemon/species_info/arauna_dex.h"
    dex_path.parent.mkdir(parents=True, exist_ok=True)
    dex_path.write_text("\n\n".join(species_blocks(args.editable_species)) + "\n", encoding="utf-8")
    species_info_path = args.out / "src/data/pokemon/species_info.h"
    species_info_path.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(args.species_info, species_info_path)

    pokemon_graphics = args.pokemon_graphics.read_text(encoding="utf-8")
    anchor = '// Normally, INCGFX_COMP acts like INCGFX_U32'
    if anchor not in pokemon_graphics:
        raise ValueError("could not locate graphics header insertion point")
    pokemon_graphics = pokemon_graphics.replace(anchor, '#include "arauna_fakemon_graphics.h"\n\n' + anchor, 1)
    pokemon_path = args.out / "src/data/graphics/pokemon.h"
    pokemon_path.parent.mkdir(parents=True, exist_ok=True)
    pokemon_path.write_text(pokemon_graphics, encoding="utf-8")

    docs_out = args.out / "docs/arauna"
    docs_out.mkdir(parents=True, exist_ok=True)
    for source in args.docs.iterdir():
        if source.is_file():
            shutil.copy2(source, docs_out / source.name)
    print(f"packed 386 species: raw_battle={raw_total} compressed_battle={compressed_total} graphics_header={graphics_path.stat().st_size}")


if __name__ == "__main__":
    main()
