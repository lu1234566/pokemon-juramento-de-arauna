#!/usr/bin/env python3
"""Read-only source coverage audit; native-bank coverage is not art acceptance."""
import csv
import json
import re
from PIL import Image, ImageDraw, ImageFont
from safari_05_common import inventory
from frontier_07i_common import ROOT, render

OUT = ROOT / 'review/aceitacao_08_auditoria'
GROUPS = {
    '08B Ruínas e cavernas': ('DesertRuins', 'DesertUnderpass', 'ScorchedSlab', *(f'MirageTower_{i}F' for i in range(1, 5))),
    '08C Navio': ('SSTidalCorridor', 'SSTidalLowerDeck', 'SSTidalRooms'),
    '08D Ilhas especiais': ('SouthernIsland_Exterior', 'SouthernIsland_Interior', 'BirthIsland_Exterior', 'BirthIsland_Harbor', 'FarawayIsland_Entrance', 'FarawayIsland_Interior'),
    '08E Concursos': ('ContestHall', 'ContestHallBeauty', 'ContestHallCool', 'ContestHallCute', 'ContestHallSmart', 'ContestHallTough'),
    '08F Conexão': ('BattleColosseum_2P', 'BattleColosseum_4P', 'RecordCorner', 'TradeCenter', 'UnionRoom'),
}
UNUSED = {'Route104_Prototype', 'Route104_PrototypePrettyPetalFlowerShop', *(f'UnusedContestHall{i}' for i in range(1, 7))}
CITIES = ('LittlerootTown', 'OldaleTown', 'PetalburgCity', 'RustboroCity', 'DewfordTown', 'SlateportCity', 'MauvilleCity', 'VerdanturfTown', 'FallarborTown', 'LavaridgeTown', 'FortreeCity', 'LilycoveCity', 'MossdeepCity', 'SootopolisCity', 'PacifidlogTown', 'EverGrandeCity')
SAMPLES = ('MirageTower_1F', 'DesertRuins', 'DesertUnderpass', 'ScorchedSlab', 'SSTidalCorridor', 'SSTidalLowerDeck', 'FarawayIsland_Interior', 'BirthIsland_Exterior', 'SouthernIsland_Interior', 'ContestHall', 'ContestHallBeauty', 'UnionRoom')


def montage(names, filename, columns, height, layouts, maps, captions=None):
    font = ImageFont.truetype('DejaVuSans.ttf', 18)
    small = ImageFont.truetype('DejaVuSans.ttf', 14)
    board = Image.new('RGB', (columns * 400, ((len(names) + columns - 1) // columns) * height + 85), '#151c24')
    draw = ImageDraw.Draw(board)
    draw.text((16, 12), 'ARAUNA — revisão da base a594b3e1e6 — ' + ('mapas nativos' if captions else 'assentamentos atuais'), font=font, fill='#f2dec4')
    for i, name in enumerate(names):
        image = render(ROOT, layouts[maps[name]['layout']])
        image.save(OUT / 'renders' / f'{name}.png', optimize=True)
        thumb = image.copy()
        thumb.thumbnail((374, height - 64), Image.Resampling.NEAREST)
        x, y = 15 + i % columns * 400, 55 + i // columns * height
        draw.text((x, y), name, font=small, fill='white')
        board.paste(thumb, (x + (374 - thumb.width) // 2, y + 28))
        if captions:
            draw.text((x, y + height - 27), captions[name], font=small, fill='#f2dec4')
    draw.text((16, board.height - 25), 'Renders dos bancos e map.bin atuais, sem atores. Não são capturas de emulador.', font=small, fill='white')
    board.save(OUT / filename, optimize=True)


def regional_map():
    source = Image.open(ROOT / 'graphics/pokenav/region_map/map.png').convert('RGB')
    tilemap = (ROOT / 'graphics/pokenav/region_map/map.bin').read_bytes()
    assert len(tilemap) == 64 * 64
    image = Image.new('RGB', (512, 512))
    for i, tile in enumerate(tilemap):
        x, y = tile % 16 * 8, tile // 16 * 8
        image.paste(source.crop((x, y, x + 8, y + 8)), (i % 64 * 8, i // 64 * 8))
    image.save(OUT / 'renders/PokeNav_MapaRegional.png', optimize=True)
    crop = image.crop((0, 0, 256, 160)).resize((512, 320), Image.Resampling.NEAREST)
    board = Image.new('RGB', (550, 390), '#151c24')
    draw = ImageDraw.Draw(board)
    font = ImageFont.truetype('DejaVuSans.ttf', 16)
    draw.text((16, 12), 'PokéNav — desenho regional ainda de Hoenn', font=font, fill='white')
    board.paste(crop, (19, 45))
    draw.text((16, 371), 'Recorte do tilemap real, sem cursor ou interface.', font=font, fill='white')
    board.save(OUT / 'Arauna_08_MapaRegional.png', optimize=True)


def acceptance_checklist():
    plan = json.loads((ROOT / 'review/frontier_07i/checkpoint_plan.json').read_text())
    rows = []
    for checkpoint in plan['checkpoints']:
        for name in checkpoint['maps']:
            rows.append({'checkpoint': checkpoint['id'], 'mapa': name, 'entrada_por_fluxo_real': 'pendente', 'retorno_por_fluxo_real': 'pendente', 'scripts_ativos': 'obrigatório', 'save_carregado': 'pendente', 'batalhas_reais_do_grupo': 'pendente' if checkpoint['id'] in ('07A', '07B', '07C', '07D', '07E', '07F') else 'não se aplica', 'anomalias': '', 'evidencia_rom_save_emulador': ''})
    assert len(rows) == 47 and len({row['mapa'] for row in rows}) == 47
    with (OUT / 'aceitacao_frontier_47_mapas.csv').open('w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=rows[0].keys(), lineterminator='\n')
        writer.writeheader()
        writer.writerows(rows)


def main():
    OUT.mkdir(exist_ok=True)
    (OUT / 'renders').mkdir(exist_ok=True)
    node, layouts, maps = inventory(ROOT)
    indices = {layout['id']: i for i, layout in enumerate(node['layouts'])}
    header = (ROOT / 'src/data/arauna_cave_visuals_v2.h').read_text()
    aliases = {int(i) for i in re.findall(r'\{(\d+), sVisual_', header)}
    groups = {name: group for group, names in GROUPS.items() for name in names}
    rows, native = [], []
    for name, m in sorted(maps.items()):
        layout = layouts[m['layout']]
        private = any('Arauna' in layout[k] for k in ('primary_tileset', 'secondary_tileset'))
        alias = indices[layout['id']] in aliases
        if name.startswith('BattlePyramidSquare'):
            status, scope = 'Módulo gerador; arte Arauna no banco do andar', '07F concluído'
        elif name in UNUSED:
            status, scope = 'Protótipo/inativo; fora da fila de arte', 'Sem prioridade'
        elif private or alias:
            status, scope = 'Arte Arauna presente; aprovação visual exige revisão', 'V1 instalada'
        else:
            status, scope = 'Bancos nativos; sem alias de câmera', groups[name]
            native.append(name)
        rows.append({'mapa': name, 'layout': layout['id'], 'largura': layout['width'], 'altura': layout['height'], 'tipo': m['map_type'], 'banco_primario': layout['primary_tileset'], 'banco_secundario': layout['secondary_tileset'], 'alias_camera': alias, 'status': status, 'checkpoint': scope, 'warps': len(m.get('warp_events', [])), 'objetos': len(m.get('object_events', []))})
    assert len(rows) == 528 and len(node['layouts']) == 754
    assert len(native) == 27 and set(native) == set(groups)
    with (OUT / 'inventario_528_mapas.csv').open('w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=rows[0].keys(), lineterminator='\n')
        writer.writeheader()
        writer.writerows(rows)
    summary = {'base_commit': 'a594b3e1e64517421101d96f5b314df22d47e14f', 'maps': 528, 'layouts': 754, 'arauna_bank_maps': sum(any('Arauna' in layouts[m['layout']][k] for k in ('primary_tileset', 'secondary_tileset')) for m in maps.values()), 'pyramid_runtime_modules': 16, 'native_remaining': GROUPS, 'inactive_maps': sorted(UNUSED), 'classification': 'Coverage of source banks and runtime override, not artistic acceptance; 27 native + 8 inactive + 16 runtime modules + 477 Arauna banks = 528.'}
    (OUT / 'inventory_summary.json').write_text(json.dumps(summary, ensure_ascii=False, indent=2) + '\n')
    montage(SAMPLES, 'Arauna_08_Pendencias_Visuais.png', 3, 355, layouts, maps, groups)
    montage(CITIES, 'Arauna_08_Cidades_Atuais.png', 4, 440, layouts, maps)
    regional_map()
    acceptance_checklist()
    print('528 maps audited; 27 native maps, 16 runtime modules, 8 inactive maps, 477 Arauna banks.')


if __name__ == '__main__':
    main()
