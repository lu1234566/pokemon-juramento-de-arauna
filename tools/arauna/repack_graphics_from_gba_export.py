#!/usr/bin/env python3
"""Rebuild the fakemon graphics header from the GBA sprite export.

Supersedes repack_graphics_from_art_pack.py as the source of the front and back
sprites. The export (graphics/arauna/arauna_sprites_gba_export.zip) carries, per
species, an indexed front (64x128, two stacked 64x64 frames), a rear-view back
(64x64) and a shiny front (64x128) -- each authored with its OWN optimal <=15
colour palette.

The engine, though, loads ONE palette per species for front AND back
(SpeciesInfo.palette), so the two cannot keep their separate palettes. For each
species this builds a single 15-colour palette (index 0 transparent) from the
front+back pixels together via k-means, then re-indexes front and back onto it.
The shiny palette is recovered from the export's shiny art, which shares the
front's index matrix, by averaging each new index's shiny colour.

Icons are NOT touched: they use a separate icon palette (SpeciesInfo.iconPalIndex
into gMonIconPalettes), so the committed gAraunaIcon_NNN arrays are preserved
verbatim.

Requires numpy and Pillow. graphics/arauna/ is gitignored, so the export is a
local authoring asset; --check skips cleanly when it is absent, exactly like the
art-pack tool, and never gates a CI checkout that does not carry it.
"""
from __future__ import annotations

import argparse
import io
import re
import struct
import sys
import zipfile
from pathlib import Path

# numpy and Pillow are imported lazily in main() only on the build path. The
# repository-safety CI job does not install them, and there the export is absent
# so --check must skip without needing them; importing at module top would crash
# that job on ModuleNotFoundError before the skip can happen.
np = None
Image = None

ROOT = Path(__file__).resolve().parents[2]
EXPORT = ROOT / "graphics/arauna/arauna_sprites_gba_export.zip"
HEADER = ROOT / "src/data/graphics/arauna_fakemon_graphics.h"

TRANSPARENT = 0x7C1F        # magenta in RGB555, the project's transparent slot
SPECIES = 386
ALPHA_THRESHOLD = 128
PALETTE_COLOURS = 15        # plus the transparent index 0

# The shared 15-colour palette is built from the front+back pixels together. For
# most species a plain union balances both, but a handful of colour-rich backs
# came out with a mean colour error just over the ~20 curation threshold because
# the front dominated the palette. Replicating the back pixels this many times in
# the k-means input buys the back more palette slots while keeping the front's
# error <= ~15. Chosen per species by a front<=15 / minimise-back sweep; species
# not listed use weight 1. The remaining over-threshold backs (19, 33, 45, 135,
# 277, 362) are genuinely palette-limited: their front already needs ~16+ of the
# 15 slots, so lowering the back would push the front error higher than the gain.
BACK_WEIGHT = {32: 2, 42: 3, 47: 4, 54: 3, 105: 2, 158: 4, 174: 4, 195: 4}


# --- image helpers ---------------------------------------------------------
def sprite_rgba(archive: zipfile.ZipFile, member: str) -> np.ndarray:
    return np.asarray(Image.open(io.BytesIO(archive.read(member))).convert("RGBA")).astype(np.uint8)


def opaque_pixels(rgba: np.ndarray) -> np.ndarray:
    mask = rgba[:, :, 3] >= ALPHA_THRESHOLD
    return rgba[:, :, :3][mask].reshape(-1, 3).astype(np.float64)


def _kpp_init(px: np.ndarray, k: int, rng: np.random.Generator) -> np.ndarray:
    centres = [px[rng.integers(len(px))]]
    d2 = ((px - centres[0]) ** 2).sum(1)
    for _ in range(1, k):
        total = d2.sum()
        idx = rng.choice(len(px), p=d2 / total) if total > 0 else rng.integers(len(px))
        centres.append(px[idx])
        d2 = np.minimum(d2, ((px - centres[-1]) ** 2).sum(1))
    return np.array(centres, dtype=np.float64)


def build_palette(px: np.ndarray, seed: int, iters: int = 20) -> np.ndarray:
    """A 16x3 uint8 palette: index 0 unused here, 1..15 are k-means centres
    snapped to the GBA's 5-bit-per-channel precision."""
    uniq = np.unique(px, axis=0)
    rng = np.random.default_rng(seed)
    if len(uniq) <= PALETTE_COLOURS:
        centres = uniq.astype(np.float64)
    else:
        centres = _kpp_init(uniq, PALETTE_COLOURS, rng)
        for _ in range(iters):
            labels = ((px[:, None, :] - centres[None, :, :]) ** 2).sum(2).argmin(1)
            for j in range(len(centres)):
                if (labels == j).any():
                    centres[j] = px[labels == j].mean(0)
    pal = np.zeros((16, 3), np.uint8)
    for i, colour in enumerate(centres[:PALETTE_COLOURS]):
        pal[i + 1] = np.clip(np.round(colour / 8) * 8, 0, 248)
    return pal


def remap(rgba: np.ndarray, pal: np.ndarray) -> np.ndarray:
    """64xN indices; opaque pixels map to the nearest of palette 1..15, index 0
    is transparent."""
    h, w, _ = rgba.shape
    rgb = rgba[:, :, :3].astype(np.int32).reshape(-1, 3)
    choices = pal[1:16].astype(np.int32)
    nearest = ((rgb[:, None, :] - choices[None, :, :]) ** 2).sum(2).argmin(1)
    idx = (nearest + 1).astype(np.uint8).reshape(h, w)
    idx[rgba[:, :, 3] < ALPHA_THRESHOLD] = 0
    return idx


def derive_shiny_palette(normal: np.ndarray, front_rgba: np.ndarray, shiny_rgba: np.ndarray) -> np.ndarray:
    """The export's normal front and shiny front share one index matrix, so each
    opaque pixel gives a normal-colour -> shiny-colour pair. Build that lookup and
    recolour every entry of our shared palette through the nearest normal colour.

    Doing it by colour (not by front-pixel position) means back-only palette
    entries -- colours the back uses but the front does not -- also get a proper
    shiny instead of staying on their normal value."""
    opaque = front_rgba[:, :, 3] >= ALPHA_THRESHOLD
    fn = front_rgba[:, :, :3][opaque].reshape(-1, 3).astype(np.int64)
    sh = shiny_rgba[:, :, :3][opaque].reshape(-1, 3).astype(np.int64)
    if len(fn) == 0:
        return normal.copy()
    keys, inv = np.unique(fn, axis=0, return_inverse=True)
    shiny_for_key = np.zeros_like(keys)
    for k in range(len(keys)):
        shiny_for_key[k] = np.rint(sh[inv == k].mean(0))
    pal = normal.copy()
    for i in range(1, 16):
        nearest = ((keys - normal[i].astype(np.int64)) ** 2).sum(1).argmin()
        pal[i] = np.clip(np.round(shiny_for_key[nearest] / 8) * 8, 0, 248)
    return pal


# --- 4bpp / LZ77 / emit (shared conventions with the art-pack tool) ---------
def to_4bpp(idx: np.ndarray) -> bytes:
    h, w = idx.shape
    out = bytearray()
    for ty in range(0, h, 8):
        for tx in range(0, w, 8):
            for y in range(8):
                row = idx[ty + y]
                for x in range(0, 8, 2):
                    out.append(int(row[tx + x]) | (int(row[tx + x + 1]) << 4))
    return bytes(out)


def lz77_compress(data: bytes) -> bytes:
    out = bytearray((0x10, len(data) & 0xFF, (len(data) >> 8) & 0xFF, (len(data) >> 16) & 0xFF))
    starts: dict[bytes, list[int]] = {}
    pos = 0
    while pos < len(data):
        flags_at = len(out); out.append(0); flags = 0
        for bit in range(8):
            if pos >= len(data):
                break
            best_len, best_disp = 0, 0
            if pos + 3 <= len(data):
                for cand in reversed(starts.get(data[pos:pos + 3], ())):
                    disp = pos - cand
                    if disp > 4096:
                        break
                    length = 0; limit = min(18, len(data) - pos)
                    while length < limit and data[cand + length] == data[pos + length]:
                        length += 1
                    if length > best_len:
                        best_len, best_disp = length, disp
                        if length == 18:
                            break
            if best_len >= 3:
                flags |= 0x80 >> bit
                out.append(((best_len - 3) << 4) | ((best_disp - 1) >> 8))
                out.append((best_disp - 1) & 0xFF)
                consumed = best_len
            else:
                out.append(data[pos]); consumed = 1
            for i in range(pos, min(len(data), pos + consumed)):
                if i + 3 <= len(data):
                    starts.setdefault(data[i:i + 3], []).append(i)
            pos += consumed
        out[flags_at] = flags
    out += b"\x00" * (-len(out) % 4)
    return bytes(out)


def pack555(pal: np.ndarray) -> list[int]:
    values = []
    for i, (r, g, b) in enumerate(pal):
        r, g, b = int(r), int(g), int(b)   # plain ints: numpy uint8 shifts overflow
        values.append(TRANSPARENT if i == 0 else ((r >> 3) | ((g >> 3) << 5) | ((b >> 3) << 10)))
    return values


def emit(name: str, ctype: str, values, align: int) -> str:
    digits = {"u8": 2, "u16": 4, "u32": 8}[ctype]
    per_line = {"u8": 16, "u16": 8, "u32": 8}[ctype]
    body = ",\n".join(
        "    " + ", ".join(f"0x{v:0{digits}X}" for v in values[i:i + per_line])
        for i in range(0, len(values), per_line)
    )
    return f"const {ctype} {name}[] __attribute__((aligned({align}))) =\n{{\n{body},\n}};\n"


def as_words(data: bytes) -> list[int]:
    return [struct.unpack_from("<I", data, i)[0] for i in range(0, len(data), 4)]


def extract_icons(header_text: str) -> dict[int, str]:
    icons = {}
    for m in re.finditer(r'(const u8 gAraunaIcon_(\d{3})\[\][^;]*;)', header_text, re.S):
        icons[int(m.group(2))] = m.group(1) + "\n"
    return icons


def build_header() -> str:
    archive = zipfile.ZipFile(EXPORT)
    members = {}
    for name in archive.namelist():
        m = re.match(r'(front|back|shiny)/(\d{3})_', name)
        if m:
            members[(m.group(1), int(m.group(2)))] = name

    icons = extract_icons(HEADER.read_text(encoding="ascii"))
    if len(icons) != SPECIES:
        raise SystemExit(f"expected {SPECIES} committed icons, found {len(icons)}")

    parts = ["// Auto-generated packed Arauna GBA graphics (new GBA export, shared front+back palette).\n"]
    for num in range(1, SPECIES + 1):
        front = sprite_rgba(archive, members[("front", num)])
        back = sprite_rgba(archive, members[("back", num)])
        if front.shape[:2] != (128, 64) or back.shape[:2] != (64, 64):
            raise SystemExit(f"#{num}: unexpected sizes front={front.shape} back={back.shape}")

        back_px = opaque_pixels(back)
        weight = BACK_WEIGHT.get(num, 1)
        pal = build_palette(
            np.concatenate([opaque_pixels(front), np.repeat(back_px, weight, 0)], 0), seed=num)
        idx_front = remap(front, pal)
        idx_back = remap(back, pal)
        shiny = derive_shiny_palette(pal, front, sprite_rgba(archive, members[("shiny", num)]))

        front_4bpp, back_4bpp = to_4bpp(idx_front), to_4bpp(idx_back)
        if len(front_4bpp) != 4096 or len(back_4bpp) != 2048:
            raise SystemExit(f"#{num}: bad 4bpp sizes {len(front_4bpp)}/{len(back_4bpp)}")

        parts.append(emit(f"gAraunaFrontPic_{num:03d}", "u32", as_words(lz77_compress(front_4bpp)), 4))
        parts.append(emit(f"gAraunaBackPic_{num:03d}", "u32", as_words(lz77_compress(back_4bpp)), 4))
        parts.append(emit(f"gAraunaPalette_{num:03d}", "u16", pack555(pal), 2))
        parts.append(emit(f"gAraunaShinyPalette_{num:03d}", "u16", pack555(shiny), 2))
        parts.append(icons[num])
    return "\n".join(parts)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true",
                        help="report whether the committed header matches the export without writing")
    args = parser.parse_args()

    if not EXPORT.exists():
        if args.check:
            print(f"GBA export not present at {EXPORT.relative_to(ROOT)}; skipping")
            return 0
        print(f"missing GBA export: {EXPORT}", file=sys.stderr)
        return 1

    global np, Image
    import numpy as np
    from PIL import Image

    text = build_header()
    previous = HEADER.read_text(encoding="ascii") if HEADER.exists() else ""
    if args.check:
        if text == previous:
            print(f"Graphics header matches the GBA export ({SPECIES} species)")
            return 0
        print("Graphics header does not match the GBA export.", file=sys.stderr)
        print("Run tools/arauna/repack_graphics_from_gba_export.py to rebuild it.", file=sys.stderr)
        return 1

    HEADER.write_text(text, encoding="ascii")
    print(f"repacked {SPECIES} species from the GBA export (front+back+palettes; icons preserved)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
