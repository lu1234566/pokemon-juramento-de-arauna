#!/usr/bin/env python3
from pathlib import Path
import argparse

ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / "data/maps/DewfordTown_Gym/scripts.inc"

REPL = {
    'DEWFORD\'s GYM LEADER BRAWLY commands\\n': 'O LIDER ADEMAR, de PORTO DAS REDES,\\n',
    'There\'s no need for BRAWLY to be\\n': 'Nao precisa chamar ADEMAR para\\n',
    'see BRAWLY\'s face…$': 'ver o rosto de ADEMAR…$\n',
    '{PLAYER} received the KNUCKLE BADGE\\n': '{PLAYER} recebeu a KNUCKLE BADGE\\n',
    'from BRAWLY.$': 'de ADEMAR.$',
    'Registered GYM LEADER BRAWLY\\n': 'LIDER ADEMAR registrado\\n',
    'in the POKéNAV.$': 'no POKéNAV.$',
    'DEWFORD TOWN POKéMON GYM$': 'PORTO DAS REDES - GINASIO$\n',
    'DEWFORD TOWN POKéMON GYM\\p': 'PORTO DAS REDES - GINASIO\\p',
    'BRAWLY\'S CERTIFIED TRAINERS:\\n': 'TREINADORES DE ADEMAR:\\n',
}

LEGACY = ['DEWFORD TOWN POKéMON GYM', 'GYM LEADER BRAWLY', 'BRAWLY\'S CERTIFIED TRAINERS', 'from BRAWLY.', 'Registered GYM LEADER BRAWLY']


def validate(text):
    return [x for x in LEGACY if x in text]


def apply():
    text = TARGET.read_text(encoding='utf-8')
    changed = 0
    for old, new in REPL.items():
        if old in text:
            text = text.replace(old, new)
            changed += 1
    bad = validate(text)
    if bad:
        raise RuntimeError('legacy visible strings remain: ' + ', '.join(bad))
    TARGET.write_text(text, encoding='utf-8')
    print(f'Ademar gym surface: {changed} replacements; PASS')


def check():
    bad = validate(TARGET.read_text(encoding='utf-8'))
    if bad:
        print('FAIL:', ', '.join(bad)); return 1
    print('Ademar gym surface PASS'); return 0

if __name__ == '__main__':
    p = argparse.ArgumentParser(); p.add_argument('--check', action='store_true'); a = p.parse_args()
    raise SystemExit(check() if a.check else (apply() or 0))
