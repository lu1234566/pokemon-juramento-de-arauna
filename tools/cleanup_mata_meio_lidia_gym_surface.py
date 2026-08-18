#!/usr/bin/env python3
from pathlib import Path
import argparse

ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / "data/maps/FortreeCity_Gym/scripts.inc"

# Badge receive/explanation text is intentionally left to the parallel badge lot.
REPL = {
    "WINONA's POKéMON are all business.$": "os POKéMON de LIDIA sao serios.$",
    'Registered GYM LEADER WINONA\\n': 'LIDER LIDIA registrada\\n',
    'in the POKéNAV.$': 'no POKéNAV.$',
    'FORTREE CITY POKéMON GYM$': 'MATA DO MEIO - GINASIO$\n',
    'FORTREE CITY POKéMON GYM\\p': 'MATA DO MEIO - GINASIO\\p',
    "WINONA'S CERTIFIED TRAINERS:\\n": 'TREINADORES DE LIDIA:\\n',
}

LEGACY = [
    "WINONA's POKéMON are all business.$",
    'Registered GYM LEADER WINONA\\n',
    'FORTREE CITY POKéMON GYM',
    "WINONA'S CERTIFIED TRAINERS:\\n",
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
    print('Lidia gym surface PASS')


def check():
    bad = validate(TARGET.read_text(encoding='utf-8'))
    if bad:
        print('FAIL:', ', '.join(bad)); return 1
    print('Lidia gym surface PASS'); return 0

if __name__ == '__main__':
    p = argparse.ArgumentParser(); p.add_argument('--check', action='store_true'); a = p.parse_args()
    raise SystemExit(check() if a.check else (apply() or 0))
