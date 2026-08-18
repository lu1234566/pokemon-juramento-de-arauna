#!/usr/bin/env python3
from pathlib import Path
import argparse

ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / "data/maps/SootopolisCity_Gym_1F/scripts.inc"

REPL = {
    "SOOTOPOLIS's GYM LEADER JUAN is\\n": "DONA CELINA, de AGUAS DE M'BOI,\\n",
    'And, to get to JUAN, an icy floor\\n': 'Para chegar a CELINA, o piso de gelo\\n',
    "You've beaten even JUAN, who\\n": 'Voce venceu ate DONA CELINA, que\\n',
    '{PLAYER} received the RAIN BADGE\\n': '{PLAYER} recebeu a RAIN BADGE\\n',
    'from JUAN.$': 'de DONA CELINA.$',
    'Registered GYM LEADER JUAN\\n': 'DONA CELINA registrada\\n',
    'in the POKéNAV.$': 'no POKéNAV.$',
    'BADGE from the GYM in FORTREE.$': 'BADGE no GINASIO de MATA DO MEIO.$',
    'SOOTOPOLIS CITY POKéMON GYM$': "AGUAS DE M'BOI - GINASIO$\n",
    'SOOTOPOLIS CITY POKéMON GYM\\p': "AGUAS DE M'BOI - GINASIO\\p",
    "JUAN'S CERTIFIED TRAINERS:\\n": 'TREINADORES DE CELINA:\\n',
}

LEGACY = ['GYM LEADER JUAN', 'from JUAN.', 'FORTREE.$', 'SOOTOPOLIS CITY POKéMON GYM', "JUAN'S CERTIFIED TRAINERS"]


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
    print('Dona Celina gym surface PASS')


def check():
    bad = validate(TARGET.read_text(encoding='utf-8'))
    if bad:
        print('FAIL:', ', '.join(bad)); return 1
    print('Dona Celina gym surface PASS'); return 0

if __name__ == '__main__':
    p = argparse.ArgumentParser(); p.add_argument('--check', action='store_true'); a = p.parse_args()
    raise SystemExit(check() if a.check else (apply() or 0))
