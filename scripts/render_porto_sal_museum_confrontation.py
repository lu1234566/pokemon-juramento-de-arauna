#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MUSEUM_PATH = ROOT / "data" / "maps" / "SlateportCity_OceanicMuseum_2F" / "scripts.inc"
ITEMS_PATH = ROOT / "src" / "data" / "items.h"
ITEM_DESCS_PATH = ROOT / "src" / "data" / "text" / "item_descriptions.h"
MAX_VISIBLE_WIDTH = 32
CONTROL_RE = re.compile(r"\\[npl]")
PLACEHOLDER_RE = re.compile(r"\{[^}]+\}")

SOURCE_SIGNATURES = (
    "HORIZONTE: Nao somos soldados",
    "Hehehe, hold it",
    "CAPT. STERN",
    "OTACILIO diz que",
    "projeto de M'BOI",
    "sensores detectam",
    "sniveling wimp",
    "ARQUIVO VIVO nao",
    "meddling kid",
    "to snatch some parts",
    "OTACILIO: Eu vi o que uma",
    "There's no time to lose",
)

TARGETS: dict[str, tuple[str, ...]] = {
    "SlateportCity_OceanicMuseum_2F_Text_ThankYouForTheParts": (
        "ENGENHEIRO: Sao as PECAS\\n",
        "OCEANICAS que esperavamos!\\p",
        "Com elas podemos calibrar os\\n",
        "sensores de profundidade.$",
    ),
    "SlateportCity_OceanicMuseum_2F_Text_WellTakeThoseParts": (
        "HORIZONTE: Pare ai.\\p",
        "Essas pecas serao requisitadas\\n",
        "para uma operacao de campo.$",
    ),
    "SlateportCity_OceanicMuseum_2F_Text_SternWhoAreYou": (
        "ENGENHEIRO: Requisitadas?\\p",
        "Quem autorizou voces?$",
    ),
    "SlateportCity_OceanicMuseum_2F_Text_WereTeamAqua": (
        "HORIZONTE: Unidade de campo do\\n",
        "HORIZONTE.\\p",
        "Os sensores ajudam a mapear\\n",
        "anomalias sob M'BOI.$",
    ),
    "SlateportCity_OceanicMuseum_2F_Text_Grunt1Defeat": (
        "HORIZONTE: Nao era para isso\\n",
        "virar uma batalha.$",
    ),
    "SlateportCity_OceanicMuseum_2F_Text_BossGoingToBeFurious": (
        "HORIZONTE: O diretor nao vai\\n",
        "gostar se voltarmos sem as pecas.$",
    ),
    "SlateportCity_OceanicMuseum_2F_Text_LetMeTakeCareOfThis": (
        "HORIZONTE: Saia da frente.\\p",
        "Eu resolvo.$",
    ),
    "SlateportCity_OceanicMuseum_2F_Text_Grunt2Defeat": (
        "HORIZONTE: Certo...\\n",
        "nao vamos passar por voce.$",
    ),
    "SlateportCity_OceanicMuseum_2F_Text_MeddlingKid": (
        "HORIZONTE: E agora?\\p",
        "Nao podemos voltar sem nada.$",
    ),
    "SlateportCity_OceanicMuseum_2F_Text_CameToSeeWhatsTakingSoLong": (
        "OTACILIO: Vim ver por que a\\n",
        "equipe estava demorando.\\p",
        "Entao foi voce quem os parou.$",
    ),
    "SlateportCity_OceanicMuseum_2F_Text_ArchieWarning": (
        "OTACILIO: Essas pecas ajudariam\\n",
        "a mapear as cavernas de M'BOI.\\p",
        "Mas transformar um MUSEU em\\n",
        "operacao forcada nao e cuidado.\\p",
        "Recuem. Buscaremos outro jeito.$",
    ),
    "SlateportCity_OceanicMuseum_2F_Text_SternThankYouForSavingUs": (
        "ENGENHEIRO: Obrigado, {PLAYER}.\\p",
        "Agora posso receber as pecas em\\n",
        "seguranca.$",
    ),
    "SlateportCity_OceanicMuseum_2F_Text_SternIveGotToGo": (
        "ENGENHEIRO: Preciso leva-las ao\\n",
        "laboratorio do porto.\\p",
        "A expedicao ao fundo do mar nao\\n",
        "pode esperar muito.\\p",
        "Fique a vontade para visitar o\\n",
        "resto do MUSEU.$",
    ),
}

ITEM_NAME_OLD = '.name = _("DEVON GOODS"),'
ITEM_NAME_NEW = '.name = _("PECAS OCEAN."),'
ITEM_DESC_RE = re.compile(
    r'(?ms)^static const u8 sDevonGoodsDesc\[\] = _\(\n(?P<body>.*?^\s*"[^"\n]*"\);)'
)
ITEM_DESC_NEW = (
    'static const u8 sDevonGoodsDesc[] = _(\n'
    '    "Pecas para pesquisa\\n"\n'
    '    "oceanografica em\\n"\n'
    '    "grande profundidade.");'
)


def block_pattern(label: str) -> re.Pattern[str]:
    return re.compile(rf"(?ms)^{re.escape(label)}:\n(?P<body>.*?)(?=^[A-Za-z0-9_]+(?:::|:)(?:\n|$)|\Z)")


def visible_segments(payload: str) -> list[str]:
    cleaned = PLACEHOLDER_RE.sub("PLAYER", payload).replace("$", "")
    return [part.strip() for part in CONTROL_RE.split(cleaned)]


def validate_widths() -> None:
    for label, payloads in TARGETS.items():
        for payload in payloads:
            for segment in visible_segments(payload):
                if len(segment) > MAX_VISIBLE_WIDTH:
                    raise ValueError(f"{label}: {len(segment)} visible chars: {segment!r}")


def replace_blocks(source: str) -> str:
    rendered = source
    for label, payloads in TARGETS.items():
        pattern = block_pattern(label)
        matches = list(pattern.finditer(rendered))
        if len(matches) != 1:
            raise ValueError(f"{label}: expected one block, found {len(matches)}")
        body = matches[0].group("body")
        if ".string" not in body:
            raise ValueError(f"{label}: target is not text")
        if not any(signature in body for signature in SOURCE_SIGNATURES):
            raise ValueError(f"{label}: source no longer matches known pre-curation surface")
        new_body = "".join(f'\t.string "{payload}"\n' for payload in payloads) + "\n"
        start, end = matches[0].span("body")
        rendered = rendered[:start] + new_body + rendered[end:]
    return rendered


def mask_blocks(source: str) -> str:
    masked = source
    for label in TARGETS:
        match = block_pattern(label).search(masked)
        if not match:
            raise ValueError(f"{label}: cannot mask missing block")
        start, end = match.span("body")
        masked = masked[:start] + '\t.string "<ARAUNA_RENDERED_BLOCK>"\n\n' + masked[end:]
    return masked


def render_museum(source: str) -> str:
    validate_widths()
    rendered = replace_blocks(source)
    if mask_blocks(source) != mask_blocks(rendered):
        raise ValueError("non-dialogue structure changed while rendering museum confrontation")
    for token in ("CAPT. STERN", "sniveling wimp", "meddling kid", "There's no time to lose"):
        for label in TARGETS:
            body = block_pattern(label).search(rendered).group("body")
            if token in body:
                raise ValueError(f"{label}: stale museum token survived: {token}")
    return rendered


def render_items(source: str) -> str:
    count = source.count(ITEM_NAME_OLD)
    if count != 1:
        raise ValueError(f"expected one DEVON GOODS item-name anchor, found {count}")
    rendered = source.replace(ITEM_NAME_OLD, ITEM_NAME_NEW, 1)
    if ITEM_NAME_OLD in rendered or ITEM_NAME_NEW not in rendered:
        raise ValueError("Devon Goods visible-name rendering failed")
    return rendered


def render_item_descs(source: str) -> str:
    matches = list(ITEM_DESC_RE.finditer(source))
    if len(matches) != 1:
        raise ValueError(f"expected one sDevonGoodsDesc block, found {len(matches)}")
    body = matches[0].group("body")
    for marker in ("DEVON's", "machine parts"):
        if marker not in body:
            raise ValueError(f"Devon Goods description marker missing: {marker!r}")
    start, end = matches[0].span()
    rendered = source[:start] + ITEM_DESC_NEW + source[end:]
    if "DEVON's" in rendered[start:start + 180]:
        raise ValueError("legacy Devon Goods description survived")
    return rendered


def main() -> int:
    parser = argparse.ArgumentParser(description="Render Porto do Sal museum confrontation and oceanographic-parts surface.")
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--in-place", action="store_true")
    args = parser.parse_args()
    if args.check and args.in_place:
        parser.error("use either --check or --in-place")

    museum = render_museum(MUSEUM_PATH.read_text(encoding="utf-8"))
    items = render_items(ITEMS_PATH.read_text(encoding="utf-8"))
    descs = render_item_descs(ITEM_DESCS_PATH.read_text(encoding="utf-8"))

    if args.check:
        print(f"Porto do Sal museum renderer OK: {len(TARGETS)} confrontation blocks + oceanographic parts validated.")
        return 0
    if args.in_place:
        MUSEUM_PATH.write_text(museum, encoding="utf-8")
        ITEMS_PATH.write_text(items, encoding="utf-8")
        ITEM_DESCS_PATH.write_text(descs, encoding="utf-8")
        return 0
    print(museum, end="" if museum.endswith("\n") else "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
