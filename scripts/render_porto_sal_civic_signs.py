#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / "data" / "maps" / "SlateportCity" / "scripts.inc"
MAX_VISIBLE_WIDTH = 32
CONTROL_RE = re.compile(r"\\[npl]")
PLACEHOLDER_RE = re.compile(r"\{[^}]+\}")

TARGETS: dict[str, tuple[tuple[str, ...], tuple[str, ...]]] = {
    "SlateportCity_Text_BattleTentSign": (("BATTLE TENT SLATEPORT SITE",), (
        "TENDA DE BATALHA - PORTO DO SAL\\p",
        "Teste equipes e estrategias sem\\n",
        "arriscar a sua jornada.$",
    )),
    "SlateportCity_Text_SternsShipyardWantedSign": (("STERN'S SHIPYARD", "Wanted"), (
        "ESTALEIRO DE PORTO DO SAL\\p",
        "PROCURA-SE: marinheiro veterano\\n",
        "que conheca todas as correntes.$",
    )),
    "SlateportCity_Text_SternsShipyardNearsCompletion": (("S.S. TIDAL", "SLATEPORT", "LILYCOVE"), (
        "ESTALEIRO DE PORTO DO SAL\\p",
        "O BARCO DE LINHA esta na fase\\n",
        "final de construcao.\\p",
        "Rota prevista: PORTO DO SAL -\\n",
        "BAIA DAS LUZES.$",
    )),
    "SlateportCity_Text_SternsShipyardFerryComplete": (("SLATEPORT-LILYCOVE", "S.S. TIDAL"), (
        "ESTALEIRO DE PORTO DO SAL\\p",
        "BARCO DE LINHA concluido.\\p",
        "Embarque e horarios no PORTO.$",
    )),
    "SlateportCity_Text_PokemonFanClubSign": (("POKéMON FAN CLUB",), (
        "CLUBE DE FAS DE POKéMON\\p",
        "Para quem nunca cansa de falar\\n",
        "sobre POKéMON.$",
    )),
    "SlateportCity_Text_OceanicMuseumSign": (("OCEANIC MUSEUM",), (
        "MUSEU OCEANOGRAFICO\\p",
        "O mar sustenta vidas e guarda\\n",
        "historias em suas profundezas.$",
    )),
    "SlateportCity_Text_CitySign": (("ARQUIVO VIVO", "DESENCANTO"), (
        "PORTO DO SAL\\p",
        "Mercado, estaleiro e pesquisa\\n",
        "cresceram junto das mareas.$",
    )),
    "SlateportCity_Text_MarketSign": (("SLATEPORT MARKET",), (
        "MERCADO DE PORTO DO SAL\\p",
        "Produtos de toda Arauna chegam\\n",
        "aqui pelo mar.$",
    )),
    "SlateportCity_Text_HarborFerryUnderConstruction": (("SLATEPORT HARBOR", "S.S. TIDAL"), (
        "PORTO DO SAL - CAIS\\p",
        "BARCO DE LINHA em construcao no\\n",
        "ESTALEIRO.\\p",
        "O servico comeca em breve.$",
    )),
    "SlateportCity_Text_HarborSign": (("SLATEPORT HARBOR", "S.S. TIDAL"), (
        "PORTO DO SAL - CAIS\\p",
        "Embarque no BARCO DE LINHA para\\n",
        "as rotas costeiras.$",
    )),
    "SlateportCity_Text_NameRatersHouseSign": (("NAME RATER'S HOUSE",), (
        "CASA DO AVALIADOR DE NOMES\\p",
        "Apelidos de POKéMON avaliados\\n",
        "aqui.$",
    )),
}


def block_pattern(label: str) -> re.Pattern[str]:
    return re.compile(rf"(?ms)^{re.escape(label)}:\n(?P<body>.*?)(?=^[A-Za-z0-9_]+(?:::|:)(?:\n|$)|\Z)")


def visible_segments(payload: str) -> list[str]:
    cleaned = PLACEHOLDER_RE.sub("PLAYER", payload).replace("$", "")
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
        raise ValueError("non-dialogue structure changed while rendering Porto do Sal civic signs")

    for token in ("SLATEPORT", "LILYCOVE", "S.S. TIDAL", "STERN'S SHIPYARD", "OCEANIC MUSEUM", "NAME RATER'S HOUSE"):
        for label in TARGETS:
            if token in block_pattern(label).search(rendered).group("body"):
                raise ValueError(f"{label}: stale civic token survived: {token}")
    return rendered


def main() -> int:
    parser = argparse.ArgumentParser(description="Render Porto do Sal civic signs and public-facing location identity.")
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--in-place", action="store_true")
    args = parser.parse_args()
    if args.check and args.in_place:
        parser.error("use either --check or --in-place")

    rendered = render(TARGET.read_text(encoding="utf-8"))
    if args.check:
        print(f"Porto do Sal civic-sign renderer OK: {len(TARGETS)} blocks validated.")
        return 0
    if args.in_place:
        TARGET.write_text(rendered, encoding="utf-8")
        return 0
    print(rendered, end="" if rendered.endswith("\n") else "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
