#!/usr/bin/env python3
"""Independent GBA format roundtrip for the 37 banks of the 86-room delivery.

Does not replace gbagfx, compile a ROM, or alter source assets. PNG indices are
packed into 8x8 4bpp tiles; JASC palettes into RGB555; a literal-only LZ10 stream
is decoded and compared. Derived bytes are only validation intermediates.
"""
import argparse, hashlib, json, struct
from pathlib import Path
from PIL import Image
from render_quatro_interiors_native import ROOT, resolve_tileset, palette


def pack_tiles(image):
    assert image.mode == 'P' and image.width % 8 == image.height % 8 == 0
    pixels = image.load(); result = bytearray()
    for ty in range(0, image.height, 8):
        for tx in range(0, image.width, 8):
            for y in range(8):
                for x in range(0, 8, 2):
                    low, high = pixels[tx + x, ty + y], pixels[tx + x + 1, ty + y]
                    assert 0 <= low < 16 and 0 <= high < 16
                    result.append(low | high << 4)
    return bytes(result)


def unpack_tiles(raw, size):
    width, height = size; out = bytearray(width * height); i = 0
    for ty in range(0, height, 8):
        for tx in range(0, width, 8):
            for y in range(8):
                for x in range(0, 8, 2):
                    value = raw[i]; i += 1
                    out[(ty + y) * width + tx + x] = value & 15
                    out[(ty + y) * width + tx + x + 1] = value >> 4
    assert i == len(raw)
    return bytes(out)


def lz10_literals(raw):
    out = bytearray(b'\x10' + len(raw).to_bytes(3, 'little'))
    for i in range(0, len(raw), 8): out.extend(b'\0' + raw[i:i + 8])
    out.extend(b'\0' * (-len(out) % 4)); return bytes(out)


def unlz10(raw):
    assert raw[0] == 0x10
    size = int.from_bytes(raw[1:4], 'little'); out = bytearray(); i = 4
    while len(out) < size:
        flags = raw[i]; i += 1
        for bit in range(7, -1, -1):
            if len(out) == size: break
            if flags & (1 << bit):
                a, b = raw[i:i + 2]; i += 2
                length, distance = (a >> 4) + 3, ((a & 15) << 8 | b) + 1
                assert distance <= len(out)
                for _ in range(length): out.append(out[-distance])
            else: out.append(raw[i]); i += 1
    assert len(out) == size
    return bytes(out)


def main():
    parser = argparse.ArgumentParser(); parser.add_argument('--output', type=Path, default=ROOT / 'review/fogueira_roda_v1/native_encoding_37_banks.json'); args = parser.parse_args()
    banks = []
    for slug in ('serra', 'porto', 'encruz', 'quatro'):
        geo = json.loads((ROOT / 'review' / (slug + '_interiors_v1') / 'geometry.json').read_text())
        for name in geo['banks']:
            folder = resolve_tileset('gTileset_' + name); image = Image.open(folder / 'tiles.png')
            packed = pack_tiles(image); assert unpack_tiles(packed, image.size) == image.tobytes()
            assert unlz10(lz10_literals(packed)) == packed
            assert len(packed) <= 512 * 32
            palette_bytes = b''
            for p in sorted((folder / 'palettes').glob('*.pal')):
                colors = palette(p)
                words = [r >> 3 | (g >> 3) << 5 | (b >> 3) << 10 for r, g, b in colors]
                binary = struct.pack('<16H', *words); assert len(binary) == 32
                decoded = [((v & 31) << 3, (v >> 5 & 31) << 3, (v >> 10 & 31) << 3) for v in struct.unpack('<16H', binary)]
                assert decoded == [tuple((c >> 3) << 3 for c in rgb) for rgb in colors]
                palette_bytes += binary
            assert len(palette_bytes) == 16 * 32
            banks.append({'bank': name, 'tiles': len(packed) // 32, '4bpp_bytes': len(packed), '4bpp_sha256': hashlib.sha256(packed).hexdigest(), 'rgb555_palette_bytes': len(palette_bytes), 'lz10_literal_bytes': len(lz10_literals(packed))})
    assert len(banks) == 37
    # Fixed byte-vector and compressed back-reference exercise the decoders
    # separately from our encoder, whose validation stream uses only literals.
    fixed = Image.new('P', (8, 8)); fixed.putdata([i % 16 for i in range(64)])
    assert pack_tiles(fixed) == bytes([0x10, 0x32, 0x54, 0x76, 0x98, 0xba, 0xdc, 0xfe] * 4)
    assert unlz10(bytes.fromhex('10060000106162630002')) == b'abcabc'
    report = {'status': 'PASS', 'bank_count': len(banks), 'scope': 'independent 4bpp/RGB555/LZ10 format roundtrip; not gbagfx or ROM build', 'banks': banks}
    args.output.parent.mkdir(parents=True, exist_ok=True); args.output.write_text(json.dumps(report, indent=2) + '\n')
    print(f"PASS: {len(banks)} banks, {sum(b['tiles'] for b in banks)} tiles, {len(banks) * 16} palettes; indexed pixels roundtrip exactly; RGB555 quantization verified")

if __name__ == '__main__': main()
