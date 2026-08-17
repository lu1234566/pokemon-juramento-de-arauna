#!/usr/bin/env python3
from pathlib import Path
import re

# Regenerate from the current protected main; helper branch is never merged.
ROOT = Path.cwd()
TRAINERS = ROOT / 'src/data/trainers.h'
CLASSES = ROOT / 'src/data/text/trainer_class_names.h'

NAME_REPLACEMENTS = {
    'ROXANNE': 'DALVA',
    'BRAWLY': 'ADEMAR',
    'WATTSON': 'OLIVIA',
    'FLANNERY': 'NARA',
    'NORMAN': 'ELIAS',
    'WINONA': 'LIDIA',
    'TATE&LIZA': 'CEC&CAET',
    'JUAN': 'CELINA',
    'WALLACE': 'AMALIA',
    'STEVEN': 'BENTO',
    'WALLY': 'VAL',
    'MAY': 'CIRO',
    'BRENDAN': 'CIRO',
    'ARCHIE': 'OTACILIO',
    'MAXIE': 'LUZIA',
    'MATT': 'BRENO',
    'SHELLY': 'MARTA',
    'TABITHA': 'RAUL',
    'COURTNEY': 'DORA',
}

CLASS_REPLACEMENTS = {
    'TRAINER_CLASS_TEAM_AQUA': 'HORIZONTE',
    'TRAINER_CLASS_AQUA_ADMIN': 'HORIZ. ADM',
    'TRAINER_CLASS_AQUA_LEADER': 'HORIZONTE',
    'TRAINER_CLASS_TEAM_MAGMA': 'LEMBRANTE',
    'TRAINER_CLASS_MAGMA_ADMIN': 'LEMBRANTE',
    'TRAINER_CLASS_MAGMA_LEADER': 'LEMBRANTE',
    'TRAINER_CLASS_RIVAL': 'RIVAL',
    'TRAINER_CLASS_LEADER': 'LIDER',
    'TRAINER_CLASS_CHAMPION': 'CAMPEA',
    'TRAINER_CLASS_ELITE_FOUR': 'CASA MAIOR',
}


def patch_trainer_names(text: str) -> str:
    counts = {}
    for old, new in NAME_REPLACEMENTS.items():
        old_token = f'.trainerName = _("{old}")'
        new_token = f'.trainerName = _("{new}")'
        count = text.count(old_token)
        counts[old] = count
        if count:
            text = text.replace(old_token, new_token)

    trainer_block = re.compile(r'(\[TRAINER_[^\]]+\]\s*=\s*\{.*?\n    \},)', re.DOTALL)

    def rewrite_block(match: re.Match[str]) -> str:
        block = match.group(1)
        if '.trainerClass = TRAINER_CLASS_TEAM_AQUA' in block:
            block = block.replace('.trainerName = _("GRUNT")', '.trainerName = _("AGENTE")')
        elif '.trainerClass = TRAINER_CLASS_TEAM_MAGMA' in block:
            block = block.replace('.trainerName = _("GRUNT")', '.trainerName = _("ATIVISTA")')
        return block

    text = trainer_block.sub(rewrite_block, text)

    required = ['ROXANNE', 'BRAWLY', 'WATTSON', 'FLANNERY', 'NORMAN', 'WINONA',
                'TATE&LIZA', 'JUAN', 'WALLACE', 'WALLY', 'MAY', 'BRENDAN',
                'ARCHIE', 'MAXIE']
    missing = [name for name in required if counts.get(name, 0) == 0]
    if missing:
        raise RuntimeError(f'Required trainer names not found: {missing}')
    return text


def patch_class_names(text: str) -> str:
    for constant, new_name in CLASS_REPLACEMENTS.items():
        pattern = re.compile(rf'(\[{re.escape(constant)}\]\s*=\s*_\(")[^"]*("\),)')
        text, count = pattern.subn(rf'\1{new_name}\2', text)
        if count != 1:
            raise RuntimeError(f'{constant}: expected one class-name entry, found {count}')
    return text


def validate(trainers: str, classes: str) -> None:
    for expected in ['DALVA', 'ADEMAR', 'OLIVIA', 'NARA', 'ELIAS', 'LIDIA', 'CEC&CAET',
                     'CELINA', 'AMALIA', 'VAL', 'CIRO', 'OTACILIO', 'LUZIA']:
        if f'.trainerName = _("{expected}")' not in trainers:
            raise RuntimeError(f'Missing Arauna trainer name {expected}')
    for expected in ['HORIZONTE', 'LEMBRANTE', 'RIVAL', 'LIDER', 'CAMPEA', 'CASA MAIOR']:
        if f'_("{expected}")' not in classes:
            raise RuntimeError(f'Missing Arauna trainer class display {expected}')
    if '.trainerClass = TRAINER_CLASS_TEAM_AQUA' in trainers and '.trainerName = _("AGENTE")' not in trainers:
        raise RuntimeError('Aqua/Horizonte generic trainer rename failed')
    if '.trainerClass = TRAINER_CLASS_TEAM_MAGMA' in trainers and '.trainerName = _("ATIVISTA")' not in trainers:
        raise RuntimeError('Magma/Lembrantes generic trainer rename failed')


def main() -> None:
    trainers = patch_trainer_names(TRAINERS.read_text(encoding='utf-8'))
    classes = patch_class_names(CLASSES.read_text(encoding='utf-8'))
    validate(trainers, classes)
    TRAINERS.write_text(trainers, encoding='utf-8')
    CLASSES.write_text(classes, encoding='utf-8')
    print('Arauna battle trainer names/classes generated successfully')


if __name__ == '__main__':
    main()
