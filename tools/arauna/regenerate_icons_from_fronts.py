#!/usr/bin/env python3
"""Regenerate party/box icons for the species whose design changed in the GBA
export.

When the graphics header was rebuilt from the GBA export, many front sprites
became the finished art while their icons (SpeciesInfo.iconSprite, a separate
asset on a shared icon palette) stayed on the OLD design -- e.g. #383 Oxumara's
icon was still a purple cat, #350 a beige cat, #386 a grey cat. This rebuilds
those icons from the new front: it area-downscales the front's top frame to
32x32, picks the shared icon palette (gMonIconPalettes 0..5) that fits it best,
re-indexes, and writes both 32x32 icon frames plus the chosen iconPalIndex.

Only the listed, design-changed species are touched; icons that already match
their creature are left exactly as they were. Requires numpy + Pillow, and reads
the front art straight from the committed header, so it needs nothing external.
"""
from __future__ import annotations

import re
import struct
import sys
from pathlib import Path

import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parents[2]
HEADER = ROOT / "src/data/graphics/arauna_fakemon_graphics.h"
DEX = ROOT / "src/data/pokemon/species_info/arauna_dex.h"
ICON_PAL_DIR = ROOT / "graphics/pokemon/icon_palettes"

# Species whose front design changed in the export, so the old icon no longer
# depicts the creature. Verified against an old-vs-new front comparison.
DESIGN_CHANGED = [
    25, 79, 85, 94, 101, 111, 121, 140, 224, 326, 327, 329, 332, 347, 350,
    359, 361, 365, 372, 373, 376, 380, 383, 386,
]
ALPHA_THRESHOLD = 128


def load_icon_palettes():
    pals = []
    for i in range(6):
        lines = (ICON_PAL_DIR / f"pal{i}.pal").read_text().splitlines()
        pals.append(np.array([tuple(map(int, l.split())) for l in lines[3:19]], np.uint8))
    return pals


def words(text: str, name: str) -> list[int]:
    m = re.search(rf'{name}\[\][^=]*=\s*\{{([^}}]*)\}}', text)
    return [int(x, 16) for x in re.findall(r'0x[0-9A-Fa-f]+', m.group(1))]


def lz_decompress(b: bytes) -> bytes:
    size = b[1] | (b[2] << 8) | (b[3] << 16)
    out = bytearray(); pos = 4
    while len(out) < size:
        flags = b[pos]; pos += 1
        for bit in range(8):
            if len(out) >= size:
                break
            if flags & (0x80 >> bit):
                hi, lo = b[pos], b[pos + 1]; pos += 2
                length = (hi >> 4) + 3; disp = ((hi & 0xF) << 8 | lo) + 1
                for _ in range(length):
                    out.append(out[-disp])
            else:
                out.append(b[pos]); pos += 1
    return bytes(out)


def decode_4bpp(raw: bytes, w: int, h: int) -> np.ndarray:
    a = np.zeros((h, w), np.uint8); p = 0
    for ty in range(0, h, 8):
        for tx in range(0, w, 8):
            for y in range(8):
                for x in range(0, 8, 2):
                    byte = raw[p]; p += 1
                    a[ty + y, tx + x] = byte & 0xF
                    a[ty + y, tx + x + 1] = byte >> 4
    return a


def front_rgba(header: str, num: int) -> np.ndarray:
    raw = lz_decompress(bytes().join(struct.pack("<I", x) for x in words(header, f"gAraunaFrontPic_{num:03d}")))
    idx = decode_4bpp(raw, 64, 128)[:64]
    pw = words(header, f"gAraunaPalette_{num:03d}")
    pal = np.array([[(c & 31) * 8, (c >> 5 & 31) * 8, (c >> 10 & 31) * 8] for c in pw], np.uint8)
    rgb = pal[idx]
    alpha = np.where(idx == 0, 0, 255).astype(np.uint8)
    return np.dstack([rgb, alpha])


def downscale(rgba: np.ndarray, size: int = 32) -> np.ndarray:
    arr = rgba.astype(np.float64)
    a = arr[:, :, 3:4] / 255.0
    prem = np.concatenate([arr[:, :, :3] * a, arr[:, :, 3:4]], 2)
    small = Image.fromarray(np.clip(prem, 0, 255).astype(np.uint8), "RGBA").resize((size, size), Image.BOX)
    pa = np.asarray(small).astype(np.float64)
    a2 = pa[:, :, 3:4] / 255.0
    with np.errstate(all="ignore"):
        rgb = np.where(a2 > 0, pa[:, :, :3] / a2, 0.0)
    return np.concatenate([np.clip(rgb, 0, 255), pa[:, :, 3:4]], 2).astype(np.uint8)


def remap(rgba: np.ndarray, pal: np.ndarray):
    rgb = rgba[:, :, :3].astype(np.int32).reshape(-1, 3)
    choices = pal[1:16].astype(np.int32)
    d = ((rgb[:, None, :] - choices[None, :, :]) ** 2).sum(2)
    nn = d.argmin(1)
    idx = (nn + 1).astype(np.uint8).reshape(32, 32)
    idx[rgba[:, :, 3] < ALPHA_THRESHOLD] = 0
    opaque = (rgba[:, :, 3] >= ALPHA_THRESHOLD).reshape(-1)
    err = float(np.sqrt(d[np.arange(len(rgb)), nn])[opaque].mean()) if opaque.any() else 0.0
    return idx, err


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


def emit_icon(name: str, data: bytes) -> str:
    per_line = 16
    body = ",\n".join("    " + ", ".join(f"0x{b:02X}" for b in data[i:i + per_line])
                      for i in range(0, len(data), per_line))
    return f"const u8 {name}[] __attribute__((aligned(4))) =\n{{\n{body},\n}};\n"


def main() -> int:
    palettes = load_icon_palettes()
    header = HEADER.read_text(encoding="ascii")
    dex = DEX.read_text(encoding="utf-8")

    for num in DESIGN_CHANGED:
        small = downscale(front_rgba(header, num))
        best_pi, best_idx, best_err = 0, None, None
        for pi, pal in enumerate(palettes):
            idx, err = remap(small, pal)
            if best_err is None or err < best_err:
                best_pi, best_idx, best_err = pi, idx, err
        frame = to_4bpp(best_idx)                 # 512 bytes (32x32)
        icon_data = frame + frame                 # two identical 32x64 frames

        block = emit_icon(f"gAraunaIcon_{num:03d}", icon_data)
        header, n = re.subn(rf'const u8 gAraunaIcon_{num:03d}\[\][^;]*;\n', block, header, count=1)
        if n != 1:
            print(f"failed to replace icon {num}", file=sys.stderr); return 1
        dex, n = re.subn(rf'(\.iconSprite = gAraunaIcon_{num:03d},\s*\n\s*\.iconPalIndex = )\d+',
                         rf'\g<1>{best_pi}', dex, count=1)
        if n != 1:
            print(f"failed to set iconPalIndex for {num}", file=sys.stderr); return 1
        print(f"  #{num:03d} -> icon palette {best_pi} (err {best_err:.0f})")

    HEADER.write_text(header, encoding="ascii")
    DEX.write_text(dex, encoding="utf-8")
    print(f"regenerated {len(DESIGN_CHANGED)} icons from the new fronts")
    return 0


if __name__ == "__main__":
    sys.exit(main())
