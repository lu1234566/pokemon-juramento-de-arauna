"""Resolve the C registrations and compare native metatile geometry."""
import re
from PIL import Image
from render_native_map import Renderer, words

def resolve_bank(repo, symbol):
    headers = (repo / 'src/data/tilesets/headers.h').read_text()
    definition = re.search(r'const struct Tileset\s+' + re.escape(symbol) + r'\s*=\s*\{(.*?)\};', headers, re.S)
    if not definition:
        raise ValueError('Unregistered tileset: ' + symbol)
    symbol = re.search(r'\.metatiles\s*=\s*(\w+)', definition[1])[1]
    text = (repo / 'src/data/tilesets/metatiles.h').read_text()
    path = re.search(re.escape(symbol) + r'\[\]\s*=\s*INCBIN_U16\("([^"]+)"', text)
    if not path:
        raise ValueError('Unregistered metatiles: ' + symbol)
    return repo / path[1].rsplit('/', 1)[0]

def bank_words(renderer, mid, attribute=False):
    path = renderer.primary if mid < 512 else renderer.secondary
    data = words(path / ('metatile_attributes.bin' if attribute else 'metatiles.bin'))
    start, length = (mid % 512, 1) if attribute else ((mid % 512) * 8, 8)
    result = data[start:start + length]
    if len(result) != length:
        raise ValueError(f'Undefined metatile {mid} in {path}')
    return result[0] if attribute else result

def normalized(renderer, mid):
    layers = []
    for raw in bank_words(renderer, mid):
        tile = renderer._tile(raw & 1023)
        if tile is None:
            layers.append(('VRAM', raw & 1023, raw & 0xC00))
        else:
            if raw & 0x400:
                tile = tile.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
            if raw & 0x800:
                tile = tile.transpose(Image.Transpose.FLIP_TOP_BOTTOM)
            layers.append(tile.tobytes())
    return tuple(layers)

def geometry(renderer, mid):
    """Compare pixel structure after palette-index relocation.

    Zero remains transparent. Renumbering the other colors by first occurrence
    avoids diagnosing a transplant's changed color indices as changed art.
    """
    out=[]
    for layer in normalized(renderer,mid):
        if not isinstance(layer,bytes):
            out.append(layer)
            continue
        colors={0:0};pixels=[]
        for color in layer:
            if color not in colors:colors[color]=len(colors)
            pixels.append(colors[color])
        out.append(bytes(pixels))
    return tuple(out)
