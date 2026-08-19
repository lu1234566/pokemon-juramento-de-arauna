#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / "data" / "maps" / "SlateportCity_NameRatersHouse" / "scripts.inc"
MAX_VISIBLE_WIDTH = 32
CONTROL_RE = re.compile(r"\\[npl]")
PLACEHOLDER_RE = re.compile(r"\{[^}]+\}")

TARGETS: dict[str, tuple[tuple[str, ...], tuple[str, ...]]] = {
    "SlateportCity_NameRatersHouse_Text_PleasedToRateMonNickname": (("NAME RATER", "fortune-teller"), (
        "AVALIADOR: Ola! Eu avalio nomes\\n",
        "de POKéMON.\\p",
        "Quer que eu examine o apelido de\\n",
        "um deles?$",
    )),
    "SlateportCity_NameRatersHouse_Text_CritiqueWhichMonNickname": (("Which POKéMON", "critique"), (
        "AVALIADOR: Qual POKéMON deseja\\n",
        "avaliar?$",
    )),
    "SlateportCity_NameRatersHouse_Text_FineNameSuggestBetterOne": (("fine name", "better name"), (
        "AVALIADOR: {STR_VAR_1}?\\p",
        "E um bom nome, sem duvida.\\p",
        "Mas talvez possamos encontrar\\n",
        "outro ainda melhor. Quer tentar?$",
    )),
    "SlateportCity_NameRatersHouse_Text_WhatShallNewNameBe": (("new", "nickname"), (
        "AVALIADOR: Qual sera o novo\\n",
        "apelido?$",
    )),
    "SlateportCity_NameRatersHouse_Text_MonShallBeKnownAsName": (("shall be known as", "fortunate"), (
        "AVALIADOR: Pronto!\\p",
        "Agora este POKéMON se chama\\n",
        "{STR_VAR_1}.\\p",
        "Cuide bem desse nome.$",
    )),
    "SlateportCity_NameRatersHouse_Text_DoVisitAgain": (("visit again",), (
        "AVALIADOR: Tudo bem.\\n",
        "Volte quando quiser.$",
    )),
    "SlateportCity_NameRatersHouse_Text_NameNoDifferentYetSuperior": (("no different", "superior"), (
        "AVALIADOR: Pronto... {STR_VAR_1}.\\p",
        "Continua igual ao nome anterior.\\p",
        "As vezes o melhor nome e o que\\n",
        "ja estava certo.$",
    )),
    "SlateportCity_NameRatersHouse_Text_MagnificentName": (("magnificent nickname", "cherish"), (
        "AVALIADOR: {STR_VAR_1} e um belo\\n",
        "apelido.\\p",
        "Ele veio de outro TREINADOR,\\n",
        "entao eu nao devo altera-lo.\\p",
        "Guarde esse nome com carinho.$",
    )),
    "SlateportCity_NameRatersHouse_Text_ThatIsMerelyAnEgg": (("merely an EGG",), (
        "AVALIADOR: Isso ainda e um OVO.\\p",
        "Vamos esperar ele nascer.$",
    )),
}


def block_pattern(label: str) -> re.Pattern[str]:
    return re.compile(rf"(?ms)^{re.escape(label)}:\n(?P<body>.*?)(?=^[A-Za-z0-9_]+(?:::|:)(?:\n|$)|\Z)")


def visible_segments(payload: str) -> list[str]:
    cleaned = PLACEHOLDER_RE.sub("NOME", payload).replace("$", "")
    return [part.strip() for part in CONTROL_RE.split(cleaned)]


def validate_widths() -> None:
    for label, (_, payloads) in TARGETS.items():
        for payload in payloads:
            for segment in visible_segments(payload):
                if len(segment) > MAX_VISIBLE_WIDTH:
                    raise ValueError(f"{label}: {len(segment)} visible chars: {segment!r}")


def render(source: str) -> str:
    validate_widths()
    rendered = source
    for label, (markers, payloads) in TARGETS.items():
        pattern = block_pattern(label)
        matches = list(pattern.finditer(rendered))
        if len(matches) != 1:
            raise ValueError(f"{label}: expected one block, found {len(matches)}")
        body = matches[0].group("body")
        for marker in markers:
            if marker not in body:
                raise ValueError(f"{label}: source marker missing: {marker!r}")
        new_body = "".join(f'\t.string "{payload}"\n' for payload in payloads) + "\n"
        start, end = matches[0].span("body")
        rendered = rendered[:start] + new_body + rendered[end:]

    def mask(text: str) -> str:
        masked = text
        for label in TARGETS:
            match = block_pattern(label).search(masked)
            if not match:
                raise ValueError(f"{label}: cannot mask missing block")
            start, end = match.span("body")
            masked = masked[:start] + '\t.string "<ARAUNA_RENDERED_BLOCK>"\n\n' + masked[end:]
        return masked

    if mask(source) != mask(rendered):
        raise ValueError("non-dialogue structure changed while rendering Name Rater")
    for token in ("NAME RATER", "fortune-teller", "magnificent nickname", "merely an EGG"):
        for label in TARGETS:
            if token in block_pattern(label).search(rendered).group("body"):
                raise ValueError(f"{label}: stale Name Rater token survived: {token}")
    return rendered


def main() -> int:
    parser = argparse.ArgumentParser(description="Render Porto do Sal Name Rater dialogue in PT-BR.")
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--in-place", action="store_true")
    args = parser.parse_args()
    if args.check and args.in_place:
        parser.error("use either --check or --in-place")

    rendered = render(TARGET.read_text(encoding="utf-8"))
    if args.check:
        print(f"Porto do Sal Name Rater renderer OK: {len(TARGETS)} blocks validated.")
        return 0
    if args.in_place:
        TARGET.write_text(rendered, encoding="utf-8")
        return 0
    print(rendered, end="" if rendered.endswith("\n") else "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
