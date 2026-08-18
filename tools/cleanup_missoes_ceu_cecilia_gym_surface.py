#!/usr/bin/env python3
from pathlib import Path
import argparse

ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / "data/maps/MossdeepCity_Gym/scripts.inc"

REPL = {
    '{PLAYER} received the MIND BADGE\\n': '{PLAYER} recebeu a MIND BADGE\\n',
    'from TATE and LIZA.$': 'de CECILIA.$',
    'TATE: The MIND BADGE enhances the\\n': 'CECILIA: A MIND BADGE melhora\\n',
    'LIZA: It also lets you use the HM move\\n': 'Ela tambem permite usar a HM\\n',
    'TATE: You should also take this, too.$': 'CECILIA: Leve isto tambem.$',
    'Registered GYM LEADERS TATE & LIZA\\n': 'LIDER CECILIA registrada\\n',
    'in the POKéNAV.$': 'no POKéNAV.$',
    'MOSSDEEP CITY POKéMON GYM$': 'MISSOES DO CEU - GINASIO$\n',
    'MOSSDEEP CITY POKéMON GYM\\p': 'MISSOES DO CEU - GINASIO\\p',
    "LIZA AND TATE'S CERTIFIED TRAINERS:\\n": 'TREINADORES DE CECILIA:\\n',
}

LEGACY = ['TATE & LIZA', 'TATE and LIZA', 'MOSSDEEP CITY POKéMON GYM', "LIZA AND TATE'S CERTIFIED TRAINERS"]


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
    print('Cecilia gym surface PASS')


def check():
    bad = validate(TARGET.read_text(encoding='utf-8'))
    if bad:
        print('FAIL:', ', '.join(bad)); return 1
    print('Cecilia gym surface PASS'); return 0

if __name__ == '__main__':
    p = argparse.ArgumentParser(); p.add_argument('--check', action='store_true'); a = p.parse_args()
    raise SystemExit(check() if a.check else (apply() or 0))
