#!/usr/bin/env python3
"""Quantise high-art back sprites into 4bpp indexed PNGs against each species' palette.

The back sprites come out of the art pipeline as 64x64 with the creature drawn
over a flat background that stands in for transparency. That background reaches
this converter one of two ways -- a soft alpha edge, or a solid key colour (the
observed batches bake a GB-green, 224,248,208, over ~79% of the frame) -- and
the GBA supports neither: a pixel is either one of 16 palette entries or it is
the transparent slot. So the background has to be cut cleanly before packing,
with a hard threshold rather than a blend, or it smears into a halo (soft alpha)
or, worse, snaps to some palette colour and fills the frame with a solid box --
exactly the "canvas" defect check_sprite_health.py rejects.

A pixel becomes the transparent index when it matches the background key colour
(within --bg-tolerance) OR its alpha is below --threshold. Everything else is
opaque and snaps to the nearest of the 15 opaque palette colours. The key colour
is auto-detected per file from its corners (override with --bg-color, disable
with --no-bg-key to key on alpha alone).

The palette is not invented here. Each species already ships a locked 16-colour
palette in src/data/graphics/arauna_fakemon_graphics.h (gAraunaPalette_NNN, or
gAraunaShinyPalette_NNN with --shiny), stored as RGB555. This reads that palette
straight from the header so the back sprite lands in the exact colours the front
sprite and icon already use, and writes a 4-bit indexed PNG carrying that same
palette in its PLTE, with index 0 flagged transparent in tRNS.

Index 0 is the transparent slot everywhere in this project, so opaque pixels
only ever match indices 1..15; a solid pixel can never collapse into the
transparent colour no matter how close it sits to it.

Colour fidelity is gated, not assumed. Because the output is indexed against
gAraunaPalette_NNN, every opaque pixel is by construction one of that species'
own colours. But a sprite drawn in colours the palette cannot represent would be
silently recoloured, so each sprite's mean opaque-pixel error (Euclidean RGB
distance from source colour to the palette entry chosen, 0..441) is measured and
any sprite above --max-error (default 25) is rejected and reported by number
instead of delivered in the wrong palette.

Input is a directory or .zip of files named "<num>_<name>_back_64x64.png"
(the "converted_images/..." layout the art pipeline emits). Output mirrors the
input names into a directory, or into a .zip when --out ends in .zip.

    python3 tools/arauna/convert_back_sprites_to_4bit.py converted_64x64.zip
    python3 tools/arauna/convert_back_sprites_to_4bit.py in_dir --out out_dir --threshold 128
"""

from __future__ import annotations

import argparse
import io
import re
import struct
import sys
import zipfile
import zlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
HEADER = ROOT / "src/data/graphics/arauna_fakemon_graphics.h"

# Index 0 is the transparent slot across the whole project; opaque pixels never
# match it, and it is written as magenta (the decomp convention) but flagged
# transparent in the PNG's tRNS so previews show through.
TRANSPARENT_INDEX = 0
# Accept both the "<num>_<name>_back_64x64.png" batch layout and the plainer
# "<num>_<name>_back.png" the high-art exports use.
NAME_RE = re.compile(r"(?P<num>\d+)_.*_back(?:_64x64)?\.png$", re.I)


# --------------------------------------------------------------------------- #
# Palette (read from the committed header)
# --------------------------------------------------------------------------- #

PALETTE_RE = re.compile(
    r"const u16 (gArauna(?:Shiny)?Palette_(\d+))\[\][^=]*=\s*\{([^}]*)\}", re.S
)


def rgb555_to_rgb888(value: int) -> tuple[int, int, int]:
    """Expand a GBA RGB555 word into 8-bit RGB.

    Uses the project's own formula -- (c & 31) * 8 per channel, the same one
    check_sprite_health.py renders with -- so a colour compared here is the exact
    colour the rest of the toolchain treats it as. Max channel is 248, not 255.
    """
    return (value & 31) * 8, ((value >> 5) & 31) * 8, ((value >> 10) & 31) * 8


def load_palettes(shiny: bool) -> dict[int, list[int]]:
    """Map species number -> its 16 RGB555 palette entries from the header."""
    text = HEADER.read_text(encoding="ascii")
    want_shiny = shiny
    palettes: dict[int, list[int]] = {}
    for name, number, body in PALETTE_RE.findall(text):
        if name.startswith("gAraunaShinyPalette") != want_shiny:
            continue
        entries = [int(v.strip(), 16) for v in body.replace("\n", "").split(",") if v.strip()]
        if len(entries) != 16:
            raise ValueError(f"{name} has {len(entries)} entries, expected 16")
        palettes[int(number)] = entries
    return palettes


# --------------------------------------------------------------------------- #
# PNG decode (RGBA) / encode (4bpp indexed)
# --------------------------------------------------------------------------- #


def _unfilter(filter_type: int, line: bytearray, previous: bytes, bpp: int) -> None:
    if filter_type == 0:
        return
    if filter_type == 1:
        for i in range(bpp, len(line)):
            line[i] = (line[i] + line[i - bpp]) & 0xFF
    elif filter_type == 2:
        for i in range(len(line)):
            line[i] = (line[i] + previous[i]) & 0xFF
    elif filter_type == 3:
        for i in range(len(line)):
            left = line[i - bpp] if i >= bpp else 0
            line[i] = (line[i] + (left + previous[i]) // 2) & 0xFF
    elif filter_type == 4:
        def paeth(a: int, b: int, c: int) -> int:
            guess = a + b - c
            da, db, dc = abs(guess - a), abs(guess - b), abs(guess - c)
            return a if da <= db and da <= dc else (b if db <= dc else c)

        for i in range(len(line)):
            left = line[i - bpp] if i >= bpp else 0
            up_left = previous[i - bpp] if i >= bpp else 0
            line[i] = (line[i] + paeth(left, previous[i], up_left)) & 0xFF
    else:
        raise ValueError(f"unknown PNG filter {filter_type}")


def read_png_rgba(blob: bytes) -> tuple[int, int, list[bytes]]:
    """Decode an 8-bit RGBA (colour type 6) PNG into rows of RGBA bytes."""
    if blob[:8] != b"\x89PNG\r\n\x1a\n":
        raise ValueError("not a PNG")
    width, height = struct.unpack(">II", blob[16:24])
    depth, colour = blob[24], blob[25]
    if depth != 8 or colour != 6:
        raise ValueError(f"expected 8-bit RGBA PNG, got depth={depth} colour={colour}")

    data = b""
    offset = 8
    while offset < len(blob):
        length = struct.unpack(">I", blob[offset : offset + 4])[0]
        kind = blob[offset + 4 : offset + 8]
        if kind == b"IDAT":
            data += blob[offset + 8 : offset + 8 + length]
        offset += 12 + length

    raw = zlib.decompress(data)
    stride = width * 4
    rows: list[bytes] = []
    pos = 0
    previous = bytes(stride)
    for _ in range(height):
        filter_type = raw[pos]
        pos += 1
        line = bytearray(raw[pos : pos + stride])
        pos += stride
        _unfilter(filter_type, line, previous, bpp=4)
        rows.append(bytes(line))
        previous = line
    return width, height, rows


def _chunk(kind: bytes, payload: bytes) -> bytes:
    body = kind + payload
    return struct.pack(">I", len(payload)) + body + struct.pack(">I", zlib.crc32(body) & 0xFFFFFFFF)


def write_png_4bit(width: int, height: int, index_rows: list[list[int]],
                   palette: list[int]) -> bytes:
    """Encode index rows (values 0..15) as a 4bpp indexed PNG with the palette."""
    raw = bytearray()
    for row in index_rows:
        raw.append(0)  # filter: none
        for x in range(0, width, 2):
            high = row[x] & 0xF
            low = (row[x + 1] & 0xF) if x + 1 < width else 0
            raw.append((high << 4) | low)

    plte = bytearray()
    for entry in palette:
        plte += bytes(rgb555_to_rgb888(entry))
    # tRNS: only index 0 is transparent; trailing entries default to opaque.
    trns = bytes([0])

    return (
        b"\x89PNG\r\n\x1a\n"
        + _chunk(b"IHDR", struct.pack(">IIBBBBB", width, height, 4, 3, 0, 0, 0))
        + _chunk(b"PLTE", bytes(plte))
        + _chunk(b"tRNS", trns)
        + _chunk(b"IDAT", zlib.compress(bytes(raw), 9))
        + _chunk(b"IEND", b"")
    )


# --------------------------------------------------------------------------- #
# Quantisation
# --------------------------------------------------------------------------- #


def detect_bg_key(rows: list[bytes], width: int, height: int,
                  threshold: int) -> tuple[int, int, int] | None:
    """Pick the flat-colour background key from the four corner pixels, if any.

    Only *opaque* corners define a colour key: a sprite with real transparency
    has transparent corners, and there the alpha threshold already does the
    cutting, so return None and let it. A colour key is meant only for art that
    fakes transparency with a solid opaque fill (the GB-green batches). The
    majority opaque corner wins; without a majority there is no reliable key.
    """
    corners = []
    for cy in (0, height - 1):
        line = rows[cy]
        for cx in (0, width - 1):
            base = cx * 4
            if line[base + 3] >= threshold:  # opaque corner only
                corners.append((line[base], line[base + 1], line[base + 2]))
    if not corners:
        return None
    counts: dict[tuple[int, int, int], int] = {}
    for colour in corners:
        counts[colour] = counts.get(colour, 0) + 1
    best_colour, best_count = max(counts.items(), key=lambda kv: kv[1])
    return best_colour if best_count > 1 else None


def quantise(rows: list[bytes], width: int, height: int, palette: list[int],
             threshold: int, bg_key: tuple[int, int, int] | None,
             bg_tolerance: int) -> tuple[list[list[int]], dict[str, float]]:
    """Map each RGBA pixel to a palette index with a hard transparency cut.

    A pixel becomes the transparent index when its colour is within
    ``bg_tolerance`` (squared RGB distance) of ``bg_key``, or when its alpha is
    below ``threshold``. Otherwise it snaps to the nearest of the 15 opaque
    palette colours by squared RGB distance.
    """
    opaque = [(i, rgb555_to_rgb888(palette[i])) for i in range(16) if i != TRANSPARENT_INDEX]
    # Cache maps a source colour to (index, distance-to-that-index) so the error
    # is measured against the palette entry actually written, not recomputed.
    cache: dict[tuple[int, int, int], tuple[int, float]] = {}
    index_rows: list[list[int]] = []
    stats = {"transparent": 0, "opaque": 0, "fringe_cut": 0, "bg_keyed": 0}
    error_sum = 0.0

    for y in range(height):
        line = rows[y]
        out_row = [TRANSPARENT_INDEX] * width
        for x in range(width):
            base = x * 4
            rgb = (line[base], line[base + 1], line[base + 2])
            alpha = line[base + 3]
            if bg_key is not None:
                kr, kg, kb = bg_key
                if (rgb[0] - kr) ** 2 + (rgb[1] - kg) ** 2 + (rgb[2] - kb) ** 2 <= bg_tolerance:
                    stats["transparent"] += 1
                    stats["bg_keyed"] += 1
                    continue
            if alpha < threshold:
                stats["transparent"] += 1
                if alpha != 0:
                    stats["fringe_cut"] += 1
                continue
            hit = cache.get(rgb)
            if hit is None:
                r, g, b = rgb
                best_dist = None
                best = TRANSPARENT_INDEX
                for index, (pr, pg, pb) in opaque:
                    dist = (r - pr) ** 2 + (g - pg) ** 2 + (b - pb) ** 2
                    if best_dist is None or dist < best_dist:
                        best_dist, best = dist, index
                hit = (best, best_dist ** 0.5)
                cache[rgb] = hit
            out_row[x] = hit[0]
            error_sum += hit[1]
            stats["opaque"] += 1
        index_rows.append(out_row)
    stats["mean_error"] = error_sum / stats["opaque"] if stats["opaque"] else 0.0
    return index_rows, stats


# --------------------------------------------------------------------------- #
# Input / output plumbing
# --------------------------------------------------------------------------- #


def iter_inputs(source: Path):
    """Yield (output_name, png_bytes) for every back sprite in a dir or zip."""
    if source.is_dir():
        for path in sorted(source.rglob("*.png")):
            if NAME_RE.search(path.name):
                yield path.name, path.read_bytes()
    elif source.suffix.lower() == ".zip":
        with zipfile.ZipFile(source) as archive:
            for info in sorted(archive.infolist(), key=lambda i: i.filename):
                name = info.filename.rsplit("/", 1)[-1]
                if NAME_RE.search(name):
                    yield name, archive.read(info)
    else:
        raise SystemExit(f"input must be a directory or .zip: {source}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("input", type=Path, help="directory or .zip of RGBA back sprites")
    parser.add_argument("--out", type=Path,
                        help="output directory, or a path ending in .zip "
                             "(default: <input>_4bit)")
    parser.add_argument("--threshold", type=int, default=128,
                        help="alpha cutoff 1..255; >= keeps a pixel, < drops it (default 128)")
    parser.add_argument("--bg-color", metavar="R,G,B",
                        help="force the transparent background key colour "
                             "(default: auto-detect from each sprite's corners)")
    parser.add_argument("--bg-tolerance", type=int, default=0,
                        help="max per-channel distance from the key that still counts as "
                             "background, cutting an anti-aliased edge (default 0 = exact match)")
    parser.add_argument("--no-bg-key", action="store_true",
                        help="ignore the background colour and key transparency on alpha alone")
    parser.add_argument("--max-error", type=float, default=25.0,
                        help="reject a sprite whose mean opaque-pixel colour error against its "
                             "species palette exceeds this (RGB distance 0..441, default 25)")
    parser.add_argument("--shiny", action="store_true",
                        help="quantise against gAraunaShinyPalette_NNN instead of the normal one")
    args = parser.parse_args()

    if not (1 <= args.threshold <= 255):
        parser.error("--threshold must be between 1 and 255")
    if args.bg_tolerance < 0:
        parser.error("--bg-tolerance must be >= 0")
    if not args.input.exists():
        parser.error(f"input not found: {args.input}")
    if not HEADER.exists():
        parser.error(f"graphics header not found: {HEADER}")

    forced_bg = None
    if args.bg_color is not None:
        if args.no_bg_key:
            parser.error("--bg-color and --no-bg-key cannot be combined")
        try:
            forced_bg = tuple(int(c) for c in args.bg_color.split(","))
        except ValueError:
            forced_bg = None
        if forced_bg is None or len(forced_bg) != 3 or not all(0 <= c <= 255 for c in forced_bg):
            parser.error("--bg-color must be R,G,B with each channel 0..255")
    # A per-channel tolerance is easiest for a human to reason about; the
    # quantiser compares squared RGB distance, so square it here once.
    bg_tolerance_sq = (args.bg_tolerance ** 2) * 3

    palettes = load_palettes(args.shiny)

    out = args.out
    if out is None:
        stem = args.input.stem if args.input.suffix else args.input.name
        out = args.input.with_name(f"{stem}_4bit")
    to_zip = out.suffix.lower() == ".zip"
    zip_out = None
    if to_zip:
        out.parent.mkdir(parents=True, exist_ok=True)
        zip_out = zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED)
    else:
        out.mkdir(parents=True, exist_ok=True)

    converted = 0
    fringe_total = 0
    bg_keyed_total = 0
    detected_keys: dict[tuple[int, int, int], int] = {}
    missing: list[str] = []
    errors: list[str] = []
    empty: list[str] = []
    rejected: list[tuple[float, str]] = []

    for name, blob in iter_inputs(args.input):
        number = int(NAME_RE.search(name).group("num"))
        palette = palettes.get(number)
        if palette is None:
            missing.append(name)
            continue
        try:
            width, height, rows = read_png_rgba(blob)
        except ValueError as exc:
            errors.append(f"{name}: {exc}")
            continue
        if (width, height) != (64, 64):
            errors.append(f"{name}: expected 64x64, got {width}x{height}")
            continue

        if args.no_bg_key:
            bg_key = None
        elif forced_bg is not None:
            bg_key = forced_bg
        else:
            bg_key = detect_bg_key(rows, width, height, args.threshold)
        if bg_key is not None:
            detected_keys[bg_key] = detected_keys.get(bg_key, 0) + 1

        index_rows, stats = quantise(
            rows, width, height, palette, args.threshold, bg_key, bg_tolerance_sq
        )
        if stats["opaque"] == 0:
            # Every pixel keyed out to transparent -- the background key almost
            # certainly swallowed the creature. Refuse to emit a blank sprite.
            empty.append(name)
            continue

        # Gate on colour fidelity. A sprite drawn in colours its species palette
        # cannot represent would come out recoloured; reject it and report the
        # number rather than ship a sprite in the wrong palette.
        if stats["mean_error"] > args.max_error:
            rejected.append((stats["mean_error"], name))
            continue

        png = write_png_4bit(width, height, index_rows, palette)
        if zip_out is not None:
            zip_out.writestr(name, png)
        else:
            (out / name).write_bytes(png)
        converted += 1
        fringe_total += int(stats["fringe_cut"])
        bg_keyed_total += int(stats["bg_keyed"])

    if zip_out is not None:
        zip_out.close()

    print(f"converted {converted} back sprite(s) -> {out}")
    print(f"  palette: {'shiny' if args.shiny else 'normal'} (from {HEADER.relative_to(ROOT)})")
    if args.no_bg_key:
        print("  background key: off (alpha only)")
    elif forced_bg is not None:
        print(f"  background key: forced {forced_bg}, tolerance {args.bg_tolerance}/chan")
    else:
        summary = ", ".join(
            f"{colour}x{count}" for colour, count in
            sorted(detected_keys.items(), key=lambda kv: -kv[1])[:3]
        )
        print(f"  background key: auto per-file [{summary}], tolerance {args.bg_tolerance}/chan")
    print(f"  hard alpha threshold: {args.threshold}")
    print(f"  cut to transparent: {bg_keyed_total}px background, {fringe_total}px alpha fringe")

    if rejected:
        rejected.sort(reverse=True)
        print(f"  REJECTED {len(rejected)} sprite(s): mean colour error > {args.max_error:g} "
              f"against their own species palette (not delivered):", file=sys.stderr)
        for mean_error, name in rejected[:25]:
            print(f"    - {name}: mean error {mean_error:.1f}/441", file=sys.stderr)
        if len(rejected) > 25:
            print(f"    ... and {len(rejected) - 25} more", file=sys.stderr)
    if missing:
        print(f"  skipped {len(missing)} file(s) with no palette in the header:", file=sys.stderr)
        for name in missing[:10]:
            print(f"    - {name}", file=sys.stderr)
        if len(missing) > 10:
            print(f"    ... and {len(missing) - 10} more", file=sys.stderr)
    if empty:
        print(f"  {len(empty)} file(s) came out fully transparent (key ate the sprite?):",
              file=sys.stderr)
        for name in empty[:10]:
            print(f"    - {name}", file=sys.stderr)
        if len(empty) > 10:
            print(f"    ... and {len(empty) - 10} more", file=sys.stderr)
    if errors:
        print(f"  {len(errors)} file(s) failed to convert:", file=sys.stderr)
        for message in errors[:10]:
            print(f"    - {message}", file=sys.stderr)
        if len(errors) > 10:
            print(f"    ... and {len(errors) - 10} more", file=sys.stderr)

    if errors or empty or rejected or converted == 0:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
