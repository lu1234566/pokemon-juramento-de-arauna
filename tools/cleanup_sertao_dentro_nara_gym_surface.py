#!/usr/bin/env python3
from pathlib import Path
import argparse

ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / "data/maps/LavaridgeTown_Gym_1F/scripts.inc"

# Badge receive/explanation text is intentionally left to the parallel badge lot.
REPL = {
    'just like FLANNERY.$': 'como NARA.$',
    "of FLANNERY's power.\\p": 'da forca de NARA.\\p',
    'Registered GYM LEADER FLANNERY\\n': 'LIDER NARA registrada\\n',
    'in the POKéNAV.$': 'no POKéNAV.$',
    'LAVARIDGE TOWN POKéMON GYM$': 'SERTAO DE DENTRO - GINASIO$\n',
    'LAVARIDGE TOWN POKéMON GYM\\p': 'SERTAO DE DENTRO - GINASIO\\p',
    "FLANNERY'S CERTIFIED TRAINERS:\\n": 'TREINADORES DE NARA:\\n',
}

LEGACY = [
    'just like FLANNERY.$',
    "of FLANNERY's power.\\p",
    'Registered GYM LEADER FLANNERY\\n',
    'LAVARIDGE TOWN POKéMON GYM',
    "FLANNERY'S CERTIFIED TRAINERS:\\n",
]


def validate(text):
    return [x for x in LEGACY if x in text]


def apply():
    text = TARGET.read_text(encoding='utf-8')
    for old, new in REPL.items():
        text = text.replace(old, new)
    bad = validate(text)
    if bad:
        raise RuntimeError('legacy visible strings remain: ' + ', '.join(bad))
    TARGET.write_text(text, encoding='utf-8')
    print('Nara gym surface PASS')


def check():
    bad = validate(TARGET.read_text(encoding='utf-8'))
    if bad:
        print('FAIL:', ', '.join(bad)); return 1
    print('Nara gym surface PASS'); return 0

if __name__ == '__main__':
    p = argparse.ArgumentParser(); p.add_argument('--check', action='store_true'); a = p.parse_args()
    raise SystemExit(check() if a.check else (apply() or 0))
