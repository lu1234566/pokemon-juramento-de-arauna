#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

TARGETS = {
    "data/text/pkmn_center_nurse.inc": {
        "gText_WouldYouLikeToRestYourPkmn": [
            ["Bem-vindo ao CENTRO POKéMON."],
            ["Aqui cuidamos da sua equipe", "e recuperamos seus POKéMON."],
            ["Deseja descansar sua equipe?"],
        ],
        "gText_IllTakeYourPkmn": [["Certo. Vou cuidar da sua equipe."]],
        "gText_RestoredPkmnToFullHealth": [
            ["Obrigado por esperar."],
            ["Seus POKéMON estao recuperados."],
        ],
        "gText_WeHopeToSeeYouAgain": [["Volte sempre!"]],
        "gText_WelcomeCutShort": [
            ["Bem-vindo ao CENTRO POKéMON."],
            ["Aqui cuidamos da sua equipe", "e recuperamos seus POKéMON."],
            ["Deseja..."],
        ],
        "gText_NoticesGoldCard": [
            ["Esse cartao...", "Pode ser o CARTAO DOURADO?!"],
            ["As quatro estrelas brilham!"],
            ["Ja vi treinadores com", "CARTAO PRATEADO antes."],
            ["Mas um CARTAO DOURADO e", "a primeira vez que vejo!"],
            ["{PLAYER}, deixe-me cuidar", "da sua equipe com honra!"],
        ],
        "gText_YouWantTheUsual": [
            ["Que bom ver voce, {PLAYER}!"],
            ["O atendimento de sempre?"],
        ],
        "gText_IllTakeYourPkmn2": [["Certo. Vou cuidar da sua equipe."]],
        "gText_ThankYouForWaiting": [["Obrigado por esperar."]],
        "gText_WeHopeToSeeYouAgain2": [["Volte sempre!"]],
    },
    "data/text/mart_clerk.inc": {
        "gText_HowMayIServeYou": [["Bem-vindo!"], ["Como posso ajudar?"]],
        "gText_PleaseComeAgain": [["Volte sempre!"]],
        "gText_PlayerWhatCanIDoForYou": [
            ["{PLAYER}{KUN}, bem-vindo!"],
            ["Como posso ajudar?"],
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
    parser = argparse.ArgumentParser(description="Render shared Pokemon Center nurse and Mart clerk service text in PT-BR.")
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--in-place", action="store_true")
    args = parser.parse_args()
    if args.check and args.in_place:
        parser.error("use either --check or --in-place")

    validate()
    if args.in_place:
        apply_in_place()
        print(f"Shared Center/Mart renderer applied: {sum(len(v) for v in TARGETS.values())} blocks.")
    else:
        print(f"Shared Center/Mart renderer OK: {sum(len(v) for v in TARGETS.values())} blocks.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
