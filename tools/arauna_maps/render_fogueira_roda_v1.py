#!/usr/bin/env python3
"""Native map/sprite composition for review; not an emulator capture."""
import argparse, json, re
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
from render_quatro_interiors_native import ROOT, Renderer, palette, render_map, resolve_tileset


def sprite(event):
    slug = event['graphics_id'][len('OBJ_EVENT_GFX_'):].lower()
    cname = ''.join(w.title() for w in slug.split('_'))
    info = (ROOT / 'src/data/object_events/object_event_graphics_info.h').read_text()
    block = re.search(r'gObjectEventGraphicsInfo_' + cname + r' = \{(.*?)\};', info, re.S)[1]
    pal_number = re.search(r'paletteTag = OBJ_EVENT_PAL_TAG_NPC_(\d)', block)[1]
    pal = palette(ROOT / ('graphics/object_events/palettes/npc_' + pal_number + '.pal'))
    source = Image.open(ROOT / ('graphics/object_events/pics/people/' + slug + '.png'))
    assert source.mode == 'P'
    facing = event['movement_type'].removeprefix('MOVEMENT_TYPE_FACE_')
    frame = {'DOWN': 0, 'UP': 1, 'LEFT': 2, 'RIGHT': 2}[facing]
    source = source.crop((frame * 16, 0, frame * 16 + 16, 32))
    image = Image.new('RGBA', (16, 32)); image.putdata([(*pal[i], 0 if i == 0 else 255) for i in source.tobytes()])
    if facing == 'RIGHT': image = image.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
    return image


def room(name, before=False):
    current = ROOT / 'data/maps' / name / 'map.json'
    baseline = ROOT / 'review/fogueira_roda_v1/baseline/data/maps' / name / 'map.json'
    m = json.loads((baseline if before and baseline.exists() else current).read_text())
    layout = next(l for l in json.loads((ROOT / 'data/layouts/layouts.json').read_text())['layouts'] if l['id'] == m['layout'])
    renderer = Renderer(resolve_tileset(layout['primary_tileset']), resolve_tileset(layout['secondary_tileset']))
    if before: renderer.palettes[6] = palette(ROOT / 'review/fogueira_roda_v1/baseline/data/tilesets/secondary/arauna_fogueira/palettes/06.pal')
    image = render_map(renderer, ROOT / layout['blockdata_filepath'], layout['width'], layout['height']).convert('RGBA')
    for event in sorted(m['object_events'], key=lambda e: e['y']):
        image.alpha_composite(sprite(event), (event['x'] * 16, event['y'] * 16 - 16))
    return image.convert('RGB')


def main():
    parser = argparse.ArgumentParser(); parser.add_argument('--output', type=Path, required=True); parser.add_argument('--concept', type=Path, required=True); args = parser.parse_args()
    board = Image.new('RGB', (1460, 1000), '#192327'); draw = ImageDraw.Draw(board)
    font = lambda size, bold=False: ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans' + ('-Bold' if bold else '') + '.ttf', size)
    def text(x, y, s, size=17, color='#cfcec4', bold=False): draw.text((x, y), s, font=font(size, bold), fill=color)
    text(28, 25, 'CASA DA FOGUEIRA  /  RODA DE ESCUTA V1', 29, '#f0ddbb', True)
    text(28, 72, 'Comparação com o concept fornecido • paleta nativa revisada • escolhas com memória persistente', 18)
    text(28, 112, 'Concept fornecido', 19, bold=True)
    concept = Image.open(args.concept).convert('RGB'); concept.thumbnail((380, 340)); board.paste(concept, (28, 147))
    text(440, 112, 'Antes — salão com dois moradores', 19, bold=True)
    text(950, 112, 'Agora — roda com seis moradores', 19, bold=True)
    before = room('Arauna_CasaFogueira_Salao', True); after = room('Arauna_CasaFogueira_Salao')
    board.paste(before.resize((480, 448), Image.Resampling.NEAREST), (440, 147)); board.paste(after.resize((480, 448), Image.Resampling.NEAREST), (950, 147))
    for i, line in enumerate(['Madeira escura e reflexos de âmbar.', 'A fogueira concentra o contraste.', 'Entrada → memorial → roda.', '', 'Ouvir e ler em qualquer ordem.', 'Compartilhar é uma escolha.', 'Recusar permite retomar depois.', '', '224 percursos de escolhas passaram.', '80 linhas: máximo de 182 px.', 'Cinco warps preservados.']): text(28, 516 + i * 27, line)
    text(440, 634, 'Entrada — acolhimento e retorno', 19, bold=True)
    text(950, 634, 'Memorial — carta aberta aos visitantes', 19, bold=True)
    for x, suffix in [(440, 'Entrada'), (950, 'Memorial')]:
        image = room('Arauna_CasaFogueira_' + suffix)
        board.paste(image.resize((480, 320), Image.Resampling.NEAREST), (x, 675))
    text(28, 902, 'Composição dos mapas e sprites reais.', 16)
    text(28, 929, 'Não é captura de emulador.', 16)
    text(28, 956, 'ROM e save/load ainda pendentes.', 16)
    args.output.parent.mkdir(parents=True, exist_ok=True); board.save(args.output)
    print(args.output)

if __name__ == '__main__': main()
