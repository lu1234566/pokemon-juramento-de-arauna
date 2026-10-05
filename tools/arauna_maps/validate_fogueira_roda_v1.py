#!/usr/bin/env python3
"""Assemble event DATA on the host and exercise its small bytecode subset.

This does not build or execute ARM engine code. Standard message boxes are
modeled as returning a supplied Yes/No response; rendering, timing, audio,
save/load and emulator interaction still need a ROM test.
"""
from __future__ import annotations
import argparse, collections, hashlib, itertools, json, re, struct, subprocess, tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
NAMES = ['Arauna_CasaFogueira_' + n for n in ('Entrada', 'Memorial', 'Salao')]
FLAGS = ['FLAG_ARAUNA_FOGUEIRA_' + n for n in ('LISTENED', 'MEMORIAL_READ', 'SHARED')]


def run(*args, **kwargs):
    return subprocess.run(args, cwd=ROOT, check=True, capture_output=True, text=True, **kwargs).stdout


def flatten(path):
    return re.sub(r'^\s*\.include "([^"]+)"\s*$',
                  lambda m: flatten(ROOT / m[1]), path.read_text(), flags=re.M)


def assemble(out):
    run('make', '-C', 'tools/preproc')
    source = ''.join('#include "constants/' + n + '.h"\n'
                     for n in ('global', 'flags', 'vars', 'comparison_operators'))
    source += flatten(ROOT / 'asm/macros/asm.inc') + '\n'
    source += flatten(ROOT / 'asm/macros/event.inc') + '\n'
    source += flatten(ROOT / 'constants/gba_constants.inc') + '\n'
    source += flatten(ROOT / 'constants/global.inc') + '\n'
    source += '\n'.join((ROOT / 'data/maps' / name / 'scripts.inc').read_text() for name in NAMES)
    source += '\n' + '\n'.join('.equ probe_' + n + ', ' + n for n in FLAGS + ['VAR_RESULT'])
    # ARM's @ comments and public :: labels are only syntax substitutions.
    # All scene commands, operands and text use the repository's real macros.
    source = '\n'.join(line.split('@', 1)[0] for line in source.splitlines())
    source = re.sub(r'^(\w+)::$', r'.global \1\n\1:', source, flags=re.M)
    with tempfile.TemporaryDirectory() as tmp:
        p = Path(tmp) / 'probe.s'; p.write_text(source)
        first = run(str(ROOT / 'tools/preproc/preproc'), str(p), str(ROOT / 'charmap.txt'))
        cpp = run('gcc', '-E', '-P', '-x', 'assembler-with-cpp', '-I', str(ROOT / 'include'), '-', input=first)
        encoded = run(str(ROOT / 'tools/preproc/preproc'), '-ie', str(p), str(ROOT / 'charmap.txt'), input=cpp)
        q = Path(tmp) / 'encoded.s'; q.write_text(encoded)
        obj = Path(tmp) / 'probe.o'; exe = Path(tmp) / 'probe.elf'; binary = Path(tmp) / 'probe.bin'
        run('as', '--32', '-o', str(obj), str(q))
        undefined = run('nm', '-u', str(obj)).strip()
        assert not undefined, ('unresolved constants or script labels', undefined)
        run('ld', '-m', 'elf_i386', '-Ttext=0', '--entry=' + NAMES[0] + '_MapScripts', '-o', str(exe), str(obj))
        run('objcopy', '-O', 'binary', '-j', '.text', str(exe), str(binary))
        symbols = {name: int(value, 16) for value, _, name in
                   (line.split() for line in run('nm', str(exe)).splitlines() if len(line.split()) == 3)}
        symbols.update({n: symbols['probe_' + n] for n in FLAGS + ['VAR_RESULT']})
        raw = binary.read_bytes()
    out.mkdir(parents=True, exist_ok=True)
    (out / 'event_data.bin').write_bytes(raw)
    (out / 'symbols.json').write_text(json.dumps(symbols, indent=2) + '\n')
    return raw, symbols


def execute(raw, symbols, label, initial, answer):
    pc = symbols[label]; state = set(initial); locked = False; result = 0; comparison = 0
    text = None; messages = []; questions = 0; visited = []
    op = {value: name[7:] for name, value in symbols.items() if name.startswith('SCR_OP_')}
    text_symbols = {value: name for name, value in symbols.items() if '_Text_' in name}
    for _ in range(200):
        visited.append(pc); command = op[raw[pc]]; pc += 1
        if command == 'END':
            assert not locked, (label, 'ended with player locked')
            return state, messages, questions, visited
        if command == 'LOCKALL': locked = True
        elif command == 'RELEASEALL': locked = False
        elif command == 'FACEPLAYER': pass
        elif command in ('SETFLAG', 'CHECKFLAG'):
            flag = struct.unpack_from('<H', raw, pc)[0]; pc += 2
            assert flag in [symbols[n] for n in FLAGS]
            if command == 'SETFLAG':
                assert locked
                state.add(flag)
            else: comparison = int(flag in state)
        elif command == 'GOTO_IF':
            condition = raw[pc]; dest = struct.unpack_from('<I', raw, pc + 1)[0]; pc += 5
            assert condition in (0, 1), condition
            if comparison == condition: pc = dest
        elif command == 'COMPARE_VAR_TO_VALUE':
            variable, value = struct.unpack_from('<HH', raw, pc); pc += 4
            assert variable == symbols['VAR_RESULT']
            comparison = 0 if result < value else 1 if result == value else 2
        elif command == 'LOAD_WORD':
            index = raw[pc]; text = struct.unpack_from('<I', raw, pc + 1)[0]; pc += 5
            assert index == 0 and text in text_symbols
        elif command == 'CALL_STD':
            kind = raw[pc]; pc += 1
            assert kind in [symbols[n] for n in ('MSGBOX_SIGN', 'MSGBOX_DEFAULT', 'MSGBOX_YESNO')]
            assert text is not None
            messages.append(text_symbols[text])
            if kind == symbols['MSGBOX_YESNO']:
                assert locked; questions += 1; result = answer
        else: raise AssertionError(('unexpected command', command, label))
    raise AssertionError(('unbounded script', label))


def geometry():
    layouts = {l['id']: l for l in json.loads((ROOT / 'data/layouts/layouts.json').read_text())['layouts']}
    maps = {n: json.loads((ROOT / 'data/maps' / n / 'map.json').read_text()) for n in NAMES}
    bank_users = {m['layout'] for m in maps.values()}
    assert {l['id'] for l in layouts.values() if l['secondary_tileset'] == 'gTileset_AraunaFogueira'} == bank_users
    lines = (ROOT / 'data/tilesets/secondary/arauna_fogueira/palettes/06.pal').read_text().splitlines()
    assert lines[:3] == ['JASC-PAL', '0100', '16'] and len(lines) == 19
    colors = [tuple(map(int, line.split())) for line in lines[3:]]
    assert all(len(rgb) == 3 and all(0 <= c <= 255 for c in rgb) for rgb in colors)
    encoded_palette = struct.pack('<16H', *(r >> 3 | (g >> 3) << 5 | (b >> 3) << 10 for r, g, b in colors))
    assert len(encoded_palette) == 32
    all_maps = {m['id']: m for m in (json.loads(p.read_text()) for p in (ROOT / 'data/maps').glob('*/map.json'))}
    reports = []
    for name, m in maps.items():
        assert m['coord_events'] == []
        assert len(m['object_events']) < 16
        assert (ROOT / 'data/maps' / name / 'scripts.inc').read_text().startswith(name + '_MapScripts::\n\t.byte 0\n')
        l = layouts[m['layout']]; w, h = l['width'], l['height']
        cells = struct.unpack('<' + 'H' * (w * h), (ROOT / l['blockdata_filepath']).read_bytes())
        blocked = {(i % w, i // w) for i, c in enumerate(cells) if c & 0xC00}
        objects = {(o['x'], o['y']) for o in m['object_events']}
        assert len(objects) == len(m['object_events']) and not objects & blocked
        assert all(o['flag'] == '0' for o in m['object_events'])
        start = (m['warp_events'][0]['x'], m['warp_events'][0]['y']); seen = {start}; queue = collections.deque(seen)
        def neighbors(x, y): return ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1))
        while queue:
            for x, y in neighbors(*queue.popleft()):
                p = (x, y)
                if 0 <= x < w and 0 <= y < h and p not in blocked | objects | seen:
                    seen.add(p); queue.append(p)
        for e in m['warp_events']:
            assert (e['x'], e['y']) in seen
            target = all_maps[e['dest_map']]['warp_events'][int(e['dest_warp_id'])]
            assert target['dest_map'] == m['id'], (name, 'missing return warp')
        for e in m['object_events'] + m['bg_events']:
            assert seen.intersection(neighbors(e['x'], e['y'])), (name, 'unreachable interaction', e['script'])
        if name.endswith('Salao'):
            baseline = json.loads((ROOT / 'review/fogueira_roda_v1/baseline/data/maps' / name / 'map.json').read_text())
            for key in baseline:
                if key != 'object_events': assert m[key] == baseline[key], key
            assert len(m['object_events']) == 6
            assert m['object_events'][1] == baseline['object_events'][1]
            old = dict(m['object_events'][0]); old.update(x=11, y=4)
            assert old == baseline['object_events'][0]
        reports.append({'map': name, 'objects': len(objects), 'warps': len(m['warp_events']), 'reachable_floor_cells': len(seen)})
    return maps, reports


def font_widths():
    widths = [int(x) for x in re.findall(r'\d+', re.search(r'gFontNormalLatinGlyphWidths\[\] = \{(.*?)\};', (ROOT / 'src/fonts.c').read_text(), re.S)[1])]
    charmap = {char: int(index, 16) for char, index in re.findall(r"^'(.)'\s*=\s*([0-9A-F]{2})\s*$", (ROOT / 'charmap.txt').read_text(), re.M)}
    charmap["'"] = charmap['’']
    maximum = 0; lines = 0
    for name in NAMES:
        for line in re.findall(r'\.string "(.*)"', (ROOT / 'data/maps' / name / 'scripts.inc').read_text()):
            for part in re.split(r'\\[nlp]|\$', line):
                width = sum(widths[charmap[c]] for c in part)
                assert width <= 208, (part, width)
                maximum = max(maximum, width); lines += bool(part)
    return {'font': 'gFontNormalLatinGlyphWidths', 'max_line_pixels': maximum, 'available_pixels': 208, 'lines': lines}


def integration():
    run('make', '-C', 'tools/mapjson')
    maps = [json.loads(p.read_text()) for p in (ROOT / 'data/maps').glob('*/map.json')]
    ids = {m['id'] for m in maps}
    layouts = {l['id'] for l in json.loads((ROOT / 'data/layouts/layouts.json').read_text())['layouts']}
    for m in maps:
        assert m['layout'] in layouts
        for w in m.get('warp_events', []): assert w['dest_map'] in ids or w['dest_map'] in ('MAP_DYNAMIC', 'MAP_NONE')
    labels = set()
    for name in NAMES:
        own = re.findall(r'^(\w+)::?', (ROOT / 'data/maps' / name / 'scripts.inc').read_text(), re.M)
        assert not labels.intersection(own) and len(own) == len(set(own))
        labels.update(own)
    for p in (ROOT / 'data/maps').glob('*/scripts.inc'):
        if p.parent.name not in NAMES:
            assert not labels.intersection(re.findall(r'^(\w+)::?', p.read_text(), re.M)), p
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        for name in NAMES:
            dest = tmp / name; dest.mkdir()
            run(str(ROOT / 'tools/mapjson/mapjson'), 'map', 'emerald', str(ROOT / 'data/maps' / name / 'map.json'), str(ROOT / 'data/layouts/layouts.json'), str(dest))
            assert set(p.name for p in dest.iterdir()) == {'header.inc', 'events.inc', 'connections.inc'}
        groups = tmp / 'groups'; const = tmp / 'constants'; groups.mkdir(); const.mkdir()
        run(str(ROOT / 'tools/mapjson/mapjson'), 'groups', 'emerald', str(ROOT / 'data/maps/map_groups.json'), str(groups), str(const))
    return {'map_references': len(maps), 'scene_labels_without_conflicts': len(labels), 'mapjson_scene_maps': len(NAMES), 'mapjson_groups': 'PASS'}


def main():
    parser = argparse.ArgumentParser(); parser.add_argument('--output', type=Path, default=ROOT / 'review/fogueira_roda_v1/validation.json'); args = parser.parse_args()
    raw, symbols = assemble(ROOT / 'review/fogueira_roda_v1/host_probe')
    assert [symbols[f] for f in FLAGS] == [0x40, 0x41, 0x42]
    maps, paths = geometry(); all_paths = []; offsets = set()
    L, M, S = (symbols[n] for n in FLAGS)
    for bits in itertools.product((0, 1), repeat=3):
        initial = {flag for flag, bit in zip((L, M, S), bits) if bit}
        for m in maps.values():
            for e in m['object_events'] + m['bg_events']:
                for answer in (0, 1):
                    label = e['script']; final, messages, questions, visited = execute(raw, symbols, label, initial, answer)
                    expected = set(initial)
                    if label.endswith('_EventScript_Letters') and M not in initial and answer: expected.add(M)
                    if label.endswith('_EventScript_Voices') and S not in initial and answer:
                        if L not in initial: expected.add(L)
                        elif M in initial: expected.add(S)
                    assert final == expected, (label, bits, answer, final, expected)
                    assert questions <= 1
                    if not answer: assert final == initial, 'declining must preserve all progress'
                    offsets.update(visited)
                    all_paths.append({'event': label, 'initial': list(bits), 'answer': answer, 'final': [int(f in final) for f in (L, M, S)], 'messages': messages})
    # Traverse both visit orders, leaving/re-entering between every interaction.
    V = NAMES[2] + '_EventScript_Voices'; R = NAMES[1] + '_EventScript_Letters'
    for order in ((V, R, V), (R, V, V)):
        state = set()
        for label in order: state = execute(raw, symbols, label, state, 1)[0]
        assert state == {L, M, S}
        for label in (V, R): assert execute(raw, symbols, label, state, 1)[0] == state
    event_include = (ROOT / 'data/event_scripts.s').read_text()
    assert all('data/maps/' + n + '/scripts.inc' in event_include for n in NAMES)
    report = {'status': 'PASS', 'scope': 'host-assembled event data; modeled message boxes; no ARM engine or ROM execution', 'flags': dict(zip(FLAGS, (0x40, 0x41, 0x42))), 'event_bytes': len(raw), 'event_sha256': hashlib.sha256(raw).hexdigest(), 'paths_tested': len(all_paths), 'opcode_positions_visited': len(offsets), 'maps': paths, 'integration': integration(), 'text': font_widths(), 'paths': all_paths, 'pending': ['ARM ROM build', 'in-game dialogue, sprites and timing', 'real save/load on GBA']}
    args.output.parent.mkdir(parents=True, exist_ok=True); args.output.write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps({k: v for k, v in report.items() if k != 'paths'}, indent=2))

if __name__ == '__main__': main()
