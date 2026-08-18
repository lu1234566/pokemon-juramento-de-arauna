#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CAVE = ROOT / "data/maps/CaveOfOrigin_B1F/scripts.inc"
TOWER = ROOT / "data/maps/SkyPillar_Outside/scripts.inc"
STRINGS = ROOT / "src/strings.c"
MAX_VISIBLE = 32

CAVE_TARGETS = {
    "CaveOfOrigin_B1F_Text_WallaceStory": (
        r"AMALIA: Entao voce e {PLAYER}.\p",
        r"Sou AMALIA, da LIGA de ARAUNA.\p",
        r"GROUDON e KYOGRE despertaram\n",
        r"e levam a regiao ao limite.\p",
        r"Ha registros de um terceiro\n",
        r"POKéMON antigo: RAYQUAZA.\p",
        r"Dizem que ele ja separou os dois\n",
        r"em uma crise muito antiga.\p",
        r"Mas nao sabemos onde esta agora.$",
    ),
    "CaveOfOrigin_B1F_Text_WhereIsRayquaza": (
        r"AMALIA: {PLAYER}, voce sabe onde\n",
        r"RAYQUAZA pode estar agora?\p",
        r"Se souber, me diga.$",
    ),
    "CaveOfOrigin_B1F_Text_ButWereInCaveOfOrigin": (
        r"AMALIA: Aqui?\p",
        r"Ja estamos na CAVERNA DA ORIGEM.\p",
        r"Temos de pensar em outro lugar.$",
    ),
    "CaveOfOrigin_B1F_Text_OldLadyDidntMentionThat": (
        r"AMALIA: MEMORIAL NOMES?\p",
        r"Passei por la antes de vir.\p",
        r"Nao encontrei sinal de RAYQUAZA.\p",
        r"Tente outra possibilidade.$",
    ),
    "CaveOfOrigin_B1F_Text_CantYouRememberSomehow": (
        r"AMALIA: Nao lembra?\p",
        r"Pense nas historias antigas.\n",
        r"Algum lugar alto, isolado...$",
    ),
    "CaveOfOrigin_B1F_Text_WellHeadToSkyPillar": (
        r"AMALIA: TORRE JURAMENTO?\p",
        r"Isso faz sentido.\p",
        r"Ela esta nos registros antigos.\p",
        r"Nao temos tempo a perder.\n",
        r"Vamos para la agora.$",
    ),
}

TOWER_TARGETS = {
    "SkyPillar_Outside_Text_DoorIsClosed": (
        r"A porta esta fechada.$",
    ),
    "SkyPillar_Outside_Text_OpenedDoorToSkyPillar": (
        r"AMALIA: Abri a entrada.\p",
        r"A TORRE JURAMENTO reage ao\n",
        r"clima que cobre ARAUNA.\p",
        r"Vamos subir antes que piore.$",
    ),
    "SkyPillar_Outside_Text_EarthquakeNotMomentToWaste": (
        r"AMALIA: Um tremor!\p",
        r"A situacao esta piorando.\n",
        r"Precisamos subir.$",
    ),
    "SkyPillar_Outside_Text_SituationGettingWorse": (
        r"AMALIA: Espere...\p",
        r"O clima mudou de novo.\n",
        r"Algo mudou em AGUAS DE M'BOI.$",
    ),
    "SkyPillar_Outside_Text_GotToGoBackForSootopolis": (
        r"AMALIA: Eu preciso voltar\n",
        r"para AGUAS DE M'BOI.\p",
        r"Voce continua subindo.\n",
        r"Encontre RAYQUAZA.$",
    ),
}

MENU_REPLACEMENTS = {
    'const u8 gText_CaveOfOrigin[] = _("CAVE OF ORIGIN");':
        'const u8 gText_CaveOfOrigin[] = _("CAVERNA ORIGEM");',
    'const u8 gText_MtPyre[] = _("MT. PYRE");':
        'const u8 gText_MtPyre[] = _("MEMORIAL NOMES");',
    'const u8 gText_SkyPillar[] = _("SKY PILLAR");':
        'const u8 gText_SkyPillar[] = _("TORRE JURAMENTO");',
    'const u8 gText_DontRemember[] = _("Don\'t remember");':
        'const u8 gText_DontRemember[] = _("NAO LEMBRO");',
}

BLOCK_RE_TEMPLATE = r'(?m)^{label}:\n(?:\t\.string "[^\n]*"\n)+'
CONTROL_RE = re.compile(r"\\[npl]|\{[^}]+\}")
FORBIDDEN_VISIBLE = (
    "WALLACE:",
    "SOOTOPOLIS",
    "JUAN",
    "MT. PYRE",
    "SKY PILLAR",
    "The door is closed",
    "Arauna sobreviveu a",
)


def block_re(label: str) -> re.Pattern[str]:
    return re.compile(BLOCK_RE_TEMPLATE.format(label=re.escape(label)))


def render(label: str, lines: tuple[str, ...]) -> str:
    return label + ":\n" + "".join(f'\t.string "{line}"\n' for line in lines)


def validate_blocks(text: str, targets: dict[str, tuple[str, ...]]) -> list[str]:
    failures: list[str] = []
    for label, lines in targets.items():
        match = block_re(label).search(text)
        if not match:
            failures.append(f"missing crisis text block: {label}")
            continue
        block = match.group(0)
        if block != render(label, lines):
            failures.append(f"{label} differs from canonical Amalia crisis text")
        for token in FORBIDDEN_VISIBLE:
            if token.lower() in block.lower():
                failures.append(f"{label} still exposes legacy/misassigned text: {token}")
        for raw in re.findall(r'\.string "(.*)"', block):
            for segment in re.split(r"\\[npl]", raw):
                visible = CONTROL_RE.sub("", segment).replace("$", "")
                if len(visible) > MAX_VISIBLE:
                    failures.append(f"{label} exceeds {MAX_VISIBLE} visible chars: {visible!r}")
    return failures


def replace_blocks(path: Path, targets: dict[str, tuple[str, ...]]) -> int:
    text = path.read_text(encoding="utf-8")
    changed = 0
    for label, lines in targets.items():
        updated, count = block_re(label).subn(lambda _m: render(label, lines), text, count=1)
        if count != 1:
            raise RuntimeError(f"Could not uniquely replace {label} (matches={count})")
        if updated != text:
            changed += 1
        text = updated
    failures = validate_blocks(text, targets)
    if failures:
        raise RuntimeError("; ".join(failures))
    path.write_text(text, encoding="utf-8")
    return changed


def validate_menu(text: str) -> list[str]:
    failures: list[str] = []
    for old, new in MENU_REPLACEMENTS.items():
        if old in text:
            failures.append(f"legacy Rayquaza menu string remains: {old}")
        if new not in text:
            failures.append(f"missing Arauna Rayquaza menu string: {new}")
    return failures


def apply() -> int:
    cave_changed = replace_blocks(CAVE, CAVE_TARGETS)
    tower_changed = replace_blocks(TOWER, TOWER_TARGETS)

    text = STRINGS.read_text(encoding="utf-8")
    menu_changed = 0
    for old, new in MENU_REPLACEMENTS.items():
        if new in text and old not in text:
            continue
        count = text.count(old)
        if count != 1:
            raise RuntimeError(f"Expected exactly one menu string {old!r}, found {count}")
        text = text.replace(old, new, 1)
        menu_changed += 1
    failures = validate_menu(text)
    if failures:
        raise RuntimeError("; ".join(failures))
    STRINGS.write_text(text, encoding="utf-8")

    print(
        f"Amalia Rayquaza crisis cleanup: {cave_changed} cave blocks, "
        f"{tower_changed} tower blocks and {menu_changed} menu strings changed."
    )
    return 0


def check() -> int:
    failures = validate_blocks(CAVE.read_text(encoding="utf-8"), CAVE_TARGETS)
    failures.extend(validate_blocks(TOWER.read_text(encoding="utf-8"), TOWER_TARGETS))
    failures.extend(validate_menu(STRINGS.read_text(encoding="utf-8")))
    if failures:
        print("Amalia Rayquaza crisis check FAILED:")
        for failure in failures:
            print(f"- {failure}")
        return 1
    print(
        f"Amalia Rayquaza crisis PASS: {len(CAVE_TARGETS)} cave blocks, "
        f"{len(TOWER_TARGETS)} tower blocks and {len(MENU_REPLACEMENTS)} menu strings."
    )
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    return check() if args.check else apply()


if __name__ == "__main__":
    raise SystemExit(main())
