#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / "data" / "maps" / "LittlerootTown_ProfessorBirchsLab" / "scripts.inc"

# Canonical post-game reassignment:
# Scott's structural invitation role is reassigned to Seu Bento, who is already
# the Arauna-facing replacement for Steven/field guidance and Match Call text.
# The destination stays the inherited battle-facility flow; the visible call
# uses established Arauna ports instead of inventing another named location.
TARGETS = {
    "LittlerootTown_ProfessorBirchsLab_Text_PokedexUpgradedToNational": (
        r"POKéDEX atualizada para o\n",
        r"Modo NACIONAL!$",
    ),
    "LittlerootTown_ProfessorBirchsLab_Text_ReceivedJohtoStarter": (
        r"{PLAYER} recebeu {STR_VAR_1}\n",
        r"de PROF. ANAHI!$",
    ),
    "LittlerootTown_ProfessorBirchsLab_Text_NicknameJohtoStarter": (
        r"Quer dar um apelido ao\n",
        r"{STR_VAR_1} que recebeu?$",
    ),
    "LittlerootTown_ProfessorBirchsLab_Text_BetterLeaveOthersAlone": (
        r"Voce ja recebeu o POKéMON\n",
        r"prometido. Deixe os outros.$",
    ),
    "LittlerootTown_ProfessorBirchsLab_Text_DontHaveAnyRoomForPokemon": (
        r"Voce nao tem espaco para\n",
        r"este POKéMON.$",
    ),
    "LittlerootTown_ProfessorBirchsLab_Text_ScottAboardSSTidalCall": (
        r"… … … … … …\n",
        r"… … … … … Bip!\p",
        r"SEU BENTO: {PLAYER}, escute.\n",
        r"Sou eu, BENTO.\p",
        r"ANAHI disse que sua POKéDEX\n",
        r"foi ampliada.\p",
        r"Ha um circuito de batalha\n",
        r"alem da LIGA.\p",
        r"Se quiser testar seu VINCULO,\n",
        r"pegue o barco no PORTO DO SAL\p",
        r"ou na BAIA DAS LUZES.\p",
        r"Eu explico o resto quando\n",
        r"voce chegar. Estarei la!\p",
        r"… … … … … …\n",
        r"… … … … … Bip!$",
    ),
}

FORBIDDEN = (
    "received the",
    "Want to give",
    "You received",
    "Better leave the others alone",
    "don't have any room",
    "SCOTT",
    "S.S. TIDAL",
    "SLATEPORT",
    "LILYCOVE",
)

PLACEHOLDER_WIDTHS = {
    "{PLAYER}": 7,
    "{STR_VAR_1}": 10,
}

MAX_VISIBLE_WIDTH = 32


def render(label: str, lines: tuple[str, ...]) -> str:
    return label + ":\n" + "".join(f'\t.string "{line}"\n' for line in lines)


def block_bounds(text: str, label: str) -> tuple[int, int]:
    marker = label + ":\n"
    start = text.find(marker)
    if start < 0:
        raise RuntimeError(f"Missing Anahi lab system text block: {label}")
    end = text.find("\n\n", start)
    if end < 0:
        end = len(text)
    else:
        end += 1
    return start, end


def extract(text: str, label: str) -> str:
    start, end = block_bounds(text, label)
    return text[start:end]


def visible_segment_width(segment: str) -> int:
    visible = segment
    for token, width in PLACEHOLDER_WIDTHS.items():
        visible = visible.replace(token, "X" * width)
    visible = re.sub(r"\{[^}]+\}", "", visible)
    visible = visible.replace("$", "")
    return len(visible)


def width_failures(label: str, lines: tuple[str, ...]) -> list[str]:
    failures: list[str] = []
    joined = "".join(lines)
    for segment in re.split(r"\\[npl]", joined):
        if not segment:
            continue
        width = visible_segment_width(segment)
        if width > MAX_VISIBLE_WIDTH:
            failures.append(
                f"{label} has a visible segment of {width} characters: {segment!r}"
            )
    return failures


def validate(text: str) -> list[str]:
    failures: list[str] = []
    for label, lines in TARGETS.items():
        block = extract(text, label)
        expected = render(label, lines)
        if block != expected:
            failures.append(f"{label} does not match the canonical generated block")
        for token in FORBIDDEN:
            if token in block:
                failures.append(f"{label} still contains legacy visible token: {token}")
        failures.extend(width_failures(label, lines))

    postgame = extract(
        text, "LittlerootTown_ProfessorBirchsLab_Text_ScottAboardSSTidalCall"
    )
    for required in ("SEU BENTO", "PORTO DO SAL", "BAIA DAS LUZES", "VINCULO"):
        if required not in postgame:
            failures.append(f"Post-game call is missing canonical Arauna term: {required}")

    return failures


def apply() -> int:
    text = TARGET.read_text(encoding="utf-8")
    changed = 0
    for label, lines in TARGETS.items():
        start, end = block_bounds(text, label)
        replacement = render(label, lines)
        if text[start:end] != replacement:
            text = text[:start] + replacement + text[end:]
            changed += 1

    failures = validate(text)
    if failures:
        raise RuntimeError("; ".join(failures))

    TARGET.write_text(text, encoding="utf-8")
    print(f"Anahi lab system cleanup: {changed} changed; {len(TARGETS)} verified.")
    return 0


def check() -> int:
    failures = validate(TARGET.read_text(encoding="utf-8"))
    if failures:
        print("Anahi lab system cleanup check FAILED:")
        for failure in failures:
            print(f"- {failure}")
        return 1
    print(f"Anahi lab system cleanup check PASS: {len(TARGETS)} blocks.")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    return check() if args.check else apply()


if __name__ == "__main__":
    raise SystemExit(main())
