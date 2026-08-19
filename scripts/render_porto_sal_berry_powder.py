#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CITY = ROOT / "data" / "maps" / "SlateportCity" / "scripts.inc"
STRINGS = ROOT / "src" / "strings.c"
MAX_VISIBLE_WIDTH = 32
CONTROL_RE = re.compile(r"\\[npl]")
PLACEHOLDER_RE = re.compile(r"\{[^}]+\}")

CITY_TARGETS: dict[str, tuple[tuple[str, ...], tuple[str, ...]]] = {
    "SlateportCity_Text_ExplainBerries": (("wild POKéMON", "BERRIES", "powder"), (
        "VENDEDOR: POKéMON selvagens\\n",
        "mastigam BERRIES quando se ferem.\\p",
        "Foi dai que veio a ideia de\\n",
        "transforma-las em remedio.\\p",
        "Primeiro, elas viram PO DE\\n",
        "BERRY.\\p",
        "Voce parece gostar de BERRIES.\\n",
        "Leve isto para comecar.$",
    )),
    "SlateportCity_Text_ExplainBerryPowder": (("BERRY CRUSH", "BERRY POWDER"), (
        "VENDEDOR: Ha maquinas que moem\\n",
        "BERRIES em alguns CENTROS.\\p",
        "Elas ficam no andar de cima.\\p",
        "Use uma para fazer PO DE BERRY\\n",
        "e traga o resultado para mim.\\p",
        "Com bastante po, preparo varios\\n",
        "remedios.$",
    )),
    "SlateportCity_Text_BroughtMeSomeBerryPowder": (("BERRY POWDER",), (
        "VENDEDOR: Trouxe PO DE BERRY?$",
    )),
    "SlateportCity_Text_ExchangeWhatWithIt": (("exchange",), (
        "VENDEDOR: O que deseja receber\\n",
        "em troca?$",
    )),
    "SlateportCity_Text_ExchangeBerryPowderForItem": (("BERRY POWDER", "{STR_VAR_1}"), (
        "Trocar seu PO DE BERRY por\\n",
        "{STR_VAR_1}?$",
    )),
    "SlateportCity_Text_DontHaveEnoughBerryPowder": (("don't have enough", "BERRY POWDER"), (
        "VENDEDOR: Voce nao tem PO DE\\n",
        "BERRY suficiente.$",
    )),
    "SlateportCity_Text_FineBerryPowderTradeSomethingElse": (("fine BERRY POWDER", "trade more"), (
        "VENDEDOR: Este po esta otimo.\\n",
        "Vai render bom remedio.\\p",
        "Quer trocar mais PO DE BERRY por\\n",
        "outra coisa?$",
    )),
    "SlateportCity_Text_WhenYouGetMoreBringItToMe": (("get some more", "BERRY POWDER"), (
        "VENDEDOR: Quando conseguir mais\\n",
        "PO DE BERRY, traga para mim.$",
    )),
    "SlateportCity_Text_ComeBackToTradeBerryPowder": (("trade your", "BERRY POWDER", "bazaar"), (
        "VENDEDOR: Volte quando quiser\\n",
        "trocar PO DE BERRY por remedios.\\p",
        "Minha banca fica sempre aberta.$",
    )),
}

STRING_REPLACEMENTS = {
    'const u8 gText_PowderQty[] = _("POWDER QTY: {STR_VAR_1}{PAUSE_UNTIL_PRESS}");':
        'const u8 gText_PowderQty[] = _("PO DE BERRY: {STR_VAR_1}{PAUSE_UNTIL_PRESS}");',
    'const u8 gText_Powder[] = _("POWDER");':
        'const u8 gText_Powder[] = _("PO DE BERRY");',
}


def block_pattern(label: str) -> re.Pattern[str]:
    return re.compile(rf"(?ms)^{re.escape(label)}:\n(?P<body>.*?)(?=^[A-Za-z0-9_]+(?:::|:)(?:\n|$)|\Z)")


def visible_segments(payload: str) -> list[str]:
    cleaned = PLACEHOLDER_RE.sub("ITEM", payload).replace("$", "")
    return [part.strip() for part in CONTROL_RE.split(cleaned)]


def validate_widths() -> None:
    for label, (_, payloads) in CITY_TARGETS.items():
        for payload in payloads:
            for segment in visible_segments(payload):
                if len(segment) > MAX_VISIBLE_WIDTH:
                    raise ValueError(f"{label}: {len(segment)} visible chars: {segment!r}")


def render_city(source: str) -> str:
    validate_widths()
    rendered = source
    for label, (markers, payloads) in CITY_TARGETS.items():
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
        for label in CITY_TARGETS:
            match = block_pattern(label).search(masked)
            if not match:
                raise ValueError(f"{label}: cannot mask missing block")
            start, end = match.span("body")
            masked = masked[:start] + '\t.string "<ARAUNA_RENDERED_BLOCK>"\n\n' + masked[end:]
        return masked

    if mask(source) != mask(rendered):
        raise ValueError("non-dialogue structure changed while rendering Berry Powder vendor")
    for token in ("BERRY POWDER", "BERRY CRUSH", "bazaar here"):
        for label in CITY_TARGETS:
            if token in block_pattern(label).search(rendered).group("body"):
                raise ValueError(f"{label}: stale Berry Powder token survived: {token}")
    return rendered


def render_strings(source: str) -> str:
    rendered = source
    for old, new in STRING_REPLACEMENTS.items():
        count = rendered.count(old)
        if count != 1:
            raise ValueError(f"expected one string anchor, found {count}: {old[:50]}")
        rendered = rendered.replace(old, new, 1)
    if 'gText_Powder[] = _("POWDER")' in rendered or "POWDER QTY:" in rendered:
        raise ValueError("legacy powder UI survived")
    return rendered


def main() -> int:
    parser = argparse.ArgumentParser(description="Render Porto do Sal Berry Powder vendor and powder-count UI as PO DE BERRY.")
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--in-place", action="store_true")
    args = parser.parse_args()
    if args.check and args.in_place:
        parser.error("use either --check or --in-place")

    city = render_city(CITY.read_text(encoding="utf-8"))
    strings = render_strings(STRINGS.read_text(encoding="utf-8"))
    if args.check:
        print(f"Porto do Sal Berry Powder renderer OK: {len(CITY_TARGETS)} dialogue blocks + 2 UI literals validated.")
        return 0
    if args.in_place:
        CITY.write_text(city, encoding="utf-8")
        STRINGS.write_text(strings, encoding="utf-8")
        return 0
    print(city, end="" if city.endswith("\n") else "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
