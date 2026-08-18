#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / "data" / "maps" / "PetalburgCity_WallysHouse" / "scripts.inc"

TARGETS = {
    "PetalburgCity_WallysHouse_Text_ThanksForPlayingWithWally": (
        r"Obrigado por ter ajudado VAL.\p",
        r"Ele fala de voce como alguem\n",
        r"que o tratou com paciencia.\p",
        r"Isso fez bem a ele.$",
    ),
    "PetalburgCity_WallysHouse_Text_WonderHowWallyIsDoing": (
        r"VAL nao manda noticias ha alguns dias.\p",
        r"Quando ele coloca uma viagem na\n",
        r"cabeca, esquece do resto.\p",
        r"Espero que esteja bem.$",
    ),
    "PetalburgCity_WallysHouse_Text_PleaseExcuseUs": (
        r"{PLAYER}! Desculpe trazer voce\n",
        r"ate aqui desse jeito.\p",
        r"VAL melhorou muito desde que foi\n",
        r"para o VALE DO SILENCIO.\p",
        r"Voce o ajudou quando ele ainda\n",
        r"tinha medo de viajar sozinho.\p",
        r"Como pai, eu nao esqueco disso.\p",
        r"Quero que leve isto.$",
    ),
    "PetalburgCity_WallysHouse_Text_SurfGoAllSortsOfPlaces": (
        r"Com SURF, seu POKéMON pode cruzar\n",
        r"trechos de agua e abrir novos caminhos.$",
    ),
    "PetalburgCity_WallysHouse_Text_WallyIsComingHomeSoon": (
        r"VAL disse que pretende voltar em breve.\p",
        r"Acho que agora ele viaja porque quer,\n",
        r"nao porque precisa provar alguma coisa.$",
    ),
    "PetalburgCity_WallysHouse_Text_YouMetWallyInEverGrandeCity": (
        r"Voce encontrou VAL na\n",
        r"ESTRADA DO JURAMENTO?\p",
        r"Ele voltou diferente: mais seguro,\n",
        r"mas ainda sendo ele mesmo.\p",
        r"Obrigado por caminhar ao lado dele.$",
    ),
    "PetalburgCity_WallysHouse_Text_WallyWasReallyHappy": (
        r"VAL ficou muito feliz depois\n",
        r"de conhecer voce.\p",
        r"Fazia tempo que eu nao via meu filho\n",
        r"falar de uma viagem com entusiasmo.$",
    ),
    "PetalburgCity_WallysHouse_Text_WallyLeftWithoutTelling": (
        r"VAL saiu sem avisar direito.\p",
        r"Eu me preocupo, claro. Mas tambem\n",
        r"sei que ele precisava escolher\l",
        r"o proprio caminho.$",
    ),
}

FORBIDDEN = ("WALLY", "VERDANTURF", "EVER GRANDE")


def render(label: str, lines: tuple[str, ...]) -> str:
    return label + ":\n" + "".join(f'\t.string "{line}"\n' for line in lines)


def block_bounds(text: str, label: str) -> tuple[int, int]:
    marker = label + ":\n"
    start = text.find(marker)
    if start < 0:
        raise RuntimeError(f"Missing Val household text block: {label}")
    end = text.find("\n\n", start)
    if end < 0:
        end = len(text)
    else:
        end += 1
    return start, end


def extract(text: str, label: str) -> str:
    start, end = block_bounds(text, label)
    return text[start:end]


def validate(text: str) -> list[str]:
    failures: list[str] = []
    for label, lines in TARGETS.items():
        block = extract(text, label)
        expected = render(label, lines)
        if block != expected:
            failures.append(f"{label} does not match the canonical generated block")
        for token in FORBIDDEN:
            if token in block:
                failures.append(f"{label} still contains visible Emerald token: {token}")
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
    print(f"Val household cleanup: {changed} changed; {len(TARGETS)} verified.")
    return 0


def check() -> int:
    failures = validate(TARGET.read_text(encoding="utf-8"))
    if failures:
        print("Val household cleanup check FAILED:")
        for failure in failures:
            print(f"- {failure}")
        return 1
    print(f"Val household cleanup check PASS: {len(TARGETS)} blocks.")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    return check() if args.check else apply()


if __name__ == "__main__":
    raise SystemExit(main())
