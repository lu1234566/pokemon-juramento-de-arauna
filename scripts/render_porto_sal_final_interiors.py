#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

TARGETS = {
    "data/maps/SlateportCity_House/scripts.inc": {
        "SlateportCity_House_Text_NatureToDoWithStatGains": [
            ["Meu POKéMON tem natureza HASTY."],
            ["Ele parece ganhar mais VELOCIDADE", "que outros POKéMON meus."],
            ["A natureza de um POKéMON pode", "mudar como seus atributos crescem."],
        ],
        "SlateportCity_House_Text_MustBeGoingToBattleTent": [
            ["Voce e TREINADOR, nao e?"],
            ["Se veio a PORTO DO SAL, talvez", "queira conhecer a TENDA DE BATALHA."],
        ],
    },
    "data/maps/SlateportCity_Mart/scripts.inc": {
        "SlateportCity_Mart_Text_SomeItemsOnlyAtMart": [
            ["O MERCADO tem coisas bem", "interessantes."],
            ["Mas alguns itens voce so encontra", "num POKé MART."],
        ],
        "SlateportCity_Mart_Text_GreatBallIsBetter": [
            ["A GREAT BALL captura melhor que", "uma POKé BALL."],
            ["Com ela talvez eu consiga pegar", "aquele POKéMON dificil."],
        ],
    },
    "data/maps/SlateportCity_PokemonCenter_1F/scripts.inc": {
        "SlateportCity_PokemonCenter_1F_Text_RaiseDifferentTypesOfPokemon": [
            ["Quer uma dica para batalhas?"],
            ["Crie POKéMON de tipos diferentes", "e mantenha a equipe equilibrada."],
            ["Um unico POKéMON forte pode", "sofrer muito contra um tipo ruim."],
        ],
        "SlateportCity_PokemonCenter_1F_Text_TradedMonWithFriend": [
            ["Eu troco POKéMON com amigos."],
            ["Quando o POKéMON trocado vem com", "um item, a surpresa e ainda melhor!"],
        ],
    },
}

STRING_BLOCK_RE_TEMPLATE = r"(?m)^{label}:\n(?:\t\.string .*\n)+"


def make_block(label: str, pages: list[list[str]]) -> str:
    lines = [f"{label}:"]
    for page_index, page in enumerate(pages):
        if not page or len(page) > 2:
            raise ValueError(f"{label}: each page must contain one or two lines")
        for line_index, text in enumerate(page):
            if len(text) > 32:
                raise ValueError(f"{label}: line exceeds 32 chars ({len(text)}): {text}")
            if line_index < len(page) - 1:
                suffix = r"\n"
            elif page_index < len(pages) - 1:
                suffix = r"\p"
            else:
                suffix = "$"
            lines.append(f'\t.string "{text}{suffix}"')
    return "\n".join(lines) + "\n"


def render(path: Path, source: str) -> str:
    rel = path.relative_to(ROOT).as_posix()
    targets = TARGETS.get(rel)
    if not targets:
        return source
    rendered = source
    for label, pages in targets.items():
        pattern = re.compile(STRING_BLOCK_RE_TEMPLATE.format(label=re.escape(label)))
        replacement = make_block(label, pages)
        rendered, count = pattern.subn(lambda _: replacement, rendered, count=1)
        if count != 1:
            raise ValueError(f"{rel}: expected exactly one block for {label}, found {count}")
    return rendered


def mask_strings(source: str) -> str:
    return re.sub(r"(?m)^\t\.string .*\n", "", source)


def validate() -> None:
    for rel, targets in TARGETS.items():
        path = ROOT / rel
        source = path.read_text(encoding="utf-8")
        rendered = render(path, source)
        if mask_strings(source) != mask_strings(rendered):
            raise ValueError(f"{rel}: non-text structure changed")
        for label, pages in targets.items():
            if make_block(label, pages) not in rendered:
                raise ValueError(f"{rel}: missing rendered block {label}")


def apply_in_place() -> None:
    for rel in TARGETS:
        path = ROOT / rel
        source = path.read_text(encoding="utf-8")
        rendered = render(path, source)
        if mask_strings(source) != mask_strings(rendered):
            raise ValueError(f"{rel}: non-text structure changed")
        path.write_text(rendered, encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Render the last map-specific Porto do Sal interiors in PT-BR.")
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--in-place", action="store_true")
    args = parser.parse_args()
    if args.check and args.in_place:
        parser.error("use either --check or --in-place")

    validate()
    if args.in_place:
        apply_in_place()
        print(f"Porto do Sal final-interiors renderer applied: {sum(len(v) for v in TARGETS.values())} blocks.")
    else:
        print(f"Porto do Sal final-interiors renderer OK: {sum(len(v) for v in TARGETS.values())} blocks.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
