#!/usr/bin/env python3
"""Strict structural validation for Arauana Fairy battle-animation PNGs.

This catches the failure mode that SHA-256 cannot: a file can hash correctly
while already being truncated/corrupt. We validate the PNG container, CRCs,
indexed 4-bit format, expected sheet dimensions, palette size, zlib payload,
scanline length, and exact IEND/EOF.
"""
from __future__ import annotations
import argparse, hashlib, json, struct, zlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SPRITES = ROOT / "graphics/battle_anims/sprites"
EXPECTED = {
    "fairy_spark.png": (16, 64),
    "fairy_wave.png": (32, 96),
    "fairy_crescent.png": (32, 64),
    "fairy_oath.png": (32, 64),
    "fairy_eclipse.png": (32, 64),
}
SIG = b"\x89PNG\r\n\x1a\n"

def validate(path: Path, expected: tuple[int, int]) -> dict:
    raw = path.read_bytes()
    if raw[:8] != SIG:
        raise ValueError(f"{path.name}: invalid PNG signature")

    pos = 8
    chunks = []
    idat = bytearray()
    ihdr = None
    palette_entries = None
    saw_iend = False

    while pos < len(raw):
        if pos + 12 > len(raw):
            raise ValueError(f"{path.name}: truncated chunk header at {pos}")
        size = struct.unpack(">I", raw[pos:pos+4])[0]
        kind = raw[pos+4:pos+8]
        end = pos + 12 + size
        if end > len(raw):
            raise ValueError(f"{path.name}: truncated {kind.decode(errors='replace')} chunk")
        data = raw[pos+8:pos+8+size]
        stored = struct.unpack(">I", raw[pos+8+size:pos+12+size])[0]
        calc = zlib.crc32(kind)
        calc = zlib.crc32(data, calc) & 0xffffffff
        if stored != calc:
            raise ValueError(f"{path.name}: CRC mismatch in {kind!r}")
        name = kind.decode("ascii")
        chunks.append([name, size])

        if kind == b"IHDR":
            if size != 13:
                raise ValueError(f"{path.name}: bad IHDR size")
            ihdr = struct.unpack(">IIBBBBB", data)
        elif kind == b"PLTE":
            if size % 3 or size > 48:
                raise ValueError(f"{path.name}: palette is not <=16 RGB entries")
            palette_entries = size // 3
        elif kind == b"IDAT":
            idat.extend(data)
        elif kind == b"IEND":
            if size != 0:
                raise ValueError(f"{path.name}: non-empty IEND")
            saw_iend = True
            pos = end
            break
        pos = end

    if not saw_iend or pos != len(raw):
        raise ValueError(f"{path.name}: IEND missing, trailing bytes, or truncation")
    if ihdr is None:
        raise ValueError(f"{path.name}: missing IHDR")
    width, height, bit_depth, color_type, compression, filter_method, interlace = ihdr
    if (width, height) != expected:
        raise ValueError(f"{path.name}: expected {expected}, got {(width, height)}")
    if bit_depth != 4 or color_type != 3:
        raise ValueError(f"{path.name}: expected 4-bit indexed PNG, got depth={bit_depth} type={color_type}")
    if compression != 0 or filter_method != 0 or interlace != 0:
        raise ValueError(f"{path.name}: unsupported PNG encoding flags")
    if palette_entries is None or not 1 <= palette_entries <= 16:
        raise ValueError(f"{path.name}: missing/invalid <=16-entry PLTE")
    if not idat:
        raise ValueError(f"{path.name}: no IDAT payload")

    try:
        decoded = zlib.decompress(bytes(idat))
    except zlib.error as exc:
        raise ValueError(f"{path.name}: IDAT zlib stream invalid: {exc}") from exc

    row_bytes = (width * bit_depth + 7) // 8
    expected_decoded = height * (1 + row_bytes)
    if len(decoded) != expected_decoded:
        raise ValueError(
            f"{path.name}: decoded scanlines {len(decoded)} bytes, expected {expected_decoded}"
        )
    filters = [decoded[y * (row_bytes + 1)] for y in range(height)]
    if any(f > 4 for f in filters):
        raise ValueError(f"{path.name}: invalid PNG filter byte")

    return {
        "file": path.name,
        "bytes": len(raw),
        "dimensions": [width, height],
        "bit_depth": bit_depth,
        "color_type": "indexed",
        "palette_entries": palette_entries,
        "decoded_scanline_bytes": len(decoded),
        "chunks": chunks,
        "sha256": hashlib.sha256(raw).hexdigest(),
    }

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--json", type=Path)
    args = ap.parse_args()
    assets = [validate(SPRITES / name, dims) for name, dims in EXPECTED.items()]
    report = {
        "status": "PASS",
        "assets": assets,
        "checks": [
            "signature", "chunk boundaries", "chunk CRCs", "IHDR",
            "4-bit indexed format", "<=16-entry palette", "IDAT zlib decode",
            "decoded scanline size", "valid filter bytes", "IEND at exact EOF"
        ],
    }
    if args.json:
        args.json.parent.mkdir(parents=True, exist_ok=True)
        args.json.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
