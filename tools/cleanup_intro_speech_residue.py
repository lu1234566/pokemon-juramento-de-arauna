#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / "data" / "text" / "birch_speech.inc"

TARGETS = {
    "gText_Birch_Welcome": (
        r"ANAHI: Desculpe a espera.\p",
        r"Bem-vindo a ARAUNA.\p",
        r"Meu nome e ANAHI.\p",
        r"Sou pesquisadora de campo.\p",
        r"Estudo POKéMON, memoria e VINCULOS.\p",
        r"$",
    ),
    "gText_Birch_Pokemon": (
        r"Este e um POKéMON.\p",
        r"\n",
        r"$",
    ),
    "gText_Birch_MainSpeech": (
        r"Pessoas e POKéMON vivem lado a lado\n",
        r"por toda ARAUNA.\p",
        r"Trabalhamos, viajamos e criamos\n",
        r"VINCULOS uns com os outros.\p",
        r"Mas alguns desses VINCULOS\n",
        r"estao falhando.\p",
        r"POKéMON esquecem lugares, vozes\n",
        r"e ate quem caminhava com eles.\p",
        r"Chamamos isso de DESENCANTO.\p",
        r"Eu procuro entender o que esta\n",
        r"acontecendo.\p",
        r"Talvez sua jornada encontre respostas\n",
        r"que meu laboratorio nao encontrou.\p",
        r"$",
    ),
    "gText_Birch_AndYouAre": (r"E voce, quem e?$",),
    "gText_Birch_BoyOrGirl": (
        r"Voce e um garoto?\n",
        r"Ou uma garota?$",
    ),
    "gText_Birch_WhatsYourName": (r"Qual e o seu nome?$",),
    "gText_Birch_SoItsPlayer": (r"Entao e {PLAYER}?$",),
    "gText_Birch_YourePlayer": (
        r"Entendi.\p",
        r"Voce e {PLAYER}, que esta se mudando\n",
        r"para VILA AMANHECER.\p",
        r"Agora faz sentido.\p",
        r"$",
    ),
    "gText_Birch_AreYouReady": (
        r"Certo. Esta pronto?\p",
        r"Sua jornada por ARAUNA comeca agora.\p",
        r"Observe os POKéMON. Escute as pessoas.\n",
        r"Memoria nao e um dado sem dono.\p",
        r"Quando chegar a VILA AMANHECER,\n",
        r"procure meu laboratorio.\p",
        r"$",
    ),
}

FORBIDDEN = ("BIRCH", "LITTLEROOT", "world of POKéMON", "POKéMON PROFESSOR")


def pattern(label: str) -> re.Pattern[str]:
    return re.compile(rf"(?m)^{re.escape(label)}::\n(?:\t\.string \"[^\n]*\"\n)+")


def render(label: str, lines: tuple[str, ...]) -> str:
    return label + "::\n" + "".join(f'\t.string "{line}"\n' for line in lines)


def extract(text: str, label: str) -> str:
    match = pattern(label).search(text)
    if not match:
        raise RuntimeError(f"Missing intro text block: {label}")
    return match.group(0)


def validate(text: str) -> list[str]:
    failures: list[str] = []
    for label, lines in TARGETS.items():
        block = extract(text, label)
        for line in lines:
            if f'\t.string "{line}"' not in block:
                failures.append(f"{label} missing expected line: {line}")
        for token in FORBIDDEN:
            if token in block:
                failures.append(f"{label} still contains visible Emerald token: {token}")
    return failures


def apply() -> int:
    text = TARGET.read_text(encoding="utf-8")
    changed = 0
    for label, lines in TARGETS.items():
        updated, count = pattern(label).subn(lambda _m: render(label, lines), text, count=1)
        if count != 1:
            raise RuntimeError(f"Could not uniquely replace {label} (matches={count})")
        if updated != text:
            changed += 1
        text = updated
    failures = validate(text)
    if failures:
        raise RuntimeError("; ".join(failures))
    TARGET.write_text(text, encoding="utf-8")
    print(f"Arauna intro cleanup: {changed} changed; {len(TARGETS)} verified.")
    return 0


def check() -> int:
    failures = validate(TARGET.read_text(encoding="utf-8"))
    if failures:
        print("Arauna intro cleanup check FAILED:")
        for failure in failures:
            print(f"- {failure}")
        return 1
    print(f"Arauna intro cleanup check PASS: {len(TARGETS)} blocks.")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    return check() if args.check else apply()


if __name__ == "__main__":
    raise SystemExit(main())
