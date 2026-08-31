#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MAP_PATH = ROOT / "data" / "maps" / "SlateportCity_PokemonFanClub" / "scripts.inc"
ITEMS_PATH = ROOT / "src" / "data" / "items.h"
DESCS_PATH = ROOT / "src" / "data" / "text" / "item_descriptions.h"

TEXT_TARGETS = {
    "SlateportCity_PokemonFanClub_Text_MeetChairman": [
        ["Eu sou o PRESIDENTE do CLUBE", "DE FAS DE POKéMON!"],
        ["Aqui nos reunimos para mostrar", "os POKéMON que criamos."],
        ["Tambem gostamos de conhecer", "POKéMON de outros treinadores."],
        ["Se participar de CONCURSOS,", "volte e me mostre sua equipe!"],
    ],
    "SlateportCity_PokemonFanClub_Text_LikeToSeeEnteredContestPokemon": [["Quero ver um POKéMON que ja", "participou de um CONCURSO."]],
    "SlateportCity_PokemonFanClub_Text_AllowMeToExamineYourPokemon": [
        ["Entao voce participou de um", "CONCURSO POKéMON!"],
        ["Deixe-me ver como voce cuidou", "do seu POKéMON."],
        ["Nada me alegra mais que ver", "um POKéMON bem cuidado."],
        ["Agora, deixe-me avaliar como", "ele se desenvolveu!"],
    ],
    "SlateportCity_PokemonFanClub_Text_HowIsYourPokemonGrowing": [["Como seu POKéMON esta indo?", "Deixe-me examina-lo."]],
    "SlateportCity_PokemonFanClub_Text_HmHmISee": [["Hm, hm...", "Entendo..."]],
    "SlateportCity_PokemonFanClub_Text_GiveMonMorePokeblocks": [["Ainda pode melhorar."], ["Tente cuidar mais dele e usar", "POKéBLOCKS adequados."]],
    "SlateportCity_PokemonFanClub_Text_NoSpaceForReward": [["Seu POKéMON merece um premio,", "mas sua BOLSA esta cheia."], ["Abra espaco e volte a falar", "comigo."]],
    "SlateportCity_PokemonFanClub_Text_MonMostImpressiveGiveItThis": [["Seu {STR_VAR_1} esta muito bem", "desenvolvido!"], ["Quero que ele use isto.", "Vai destacar ainda mais seu dom!"]],
    "SlateportCity_PokemonFanClub_Text_ExplainRedScarf": [["Deixe um POKéMON segurar a", "FITA VERMELHA."], ["Ela realca o ESTILO dele", "nos CONCURSOS."]],
    "SlateportCity_PokemonFanClub_Text_ExplainBlueScarf": [["Deixe um POKéMON segurar a", "FITA AZUL."], ["Ela realca a BELEZA dele", "nos CONCURSOS."]],
    "SlateportCity_PokemonFanClub_Text_ExplainPinkScarf": [["Deixe um POKéMON segurar a", "FITA ROSA."], ["Ela realca a FOFURA dele", "nos CONCURSOS."]],
    "SlateportCity_PokemonFanClub_Text_ExplainGreenScarf": [["Deixe um POKéMON segurar a", "FITA VERDE."], ["Ela realca a ESPERTEZA dele", "nos CONCURSOS."]],
    "SlateportCity_PokemonFanClub_Text_ExplainYellowScarf": [["Deixe um POKéMON segurar a", "FITA AMARELA."], ["Ela realca a RESISTENCIA dele", "nos CONCURSOS."]],
    "SlateportCity_PokemonFanClub_Text_NothingElseToGiveYou": [["Nao tenho mais fitas para dar."], ["Voce ja mostrou grande cuidado", "com seus POKéMON!"]],
    "SlateportCity_PokemonFanClub_Text_ShowMePokemonThatLoveYou": [["Gosto de ver POKéMON que confiam", "em seus treinadores."], ["Trate seu POKéMON com carinho", "e ele vai confiar em voce."], ["Quando essa ligacao for forte,", "venha me mostrar."]],
    "SlateportCity_PokemonFanClub_Text_PokemonAdoresYou": [["Seu POKéMON confia em voce!"], ["Por esse cuidado, receba um", "presente do CLUBE DE FAS."]],
    "SlateportCity_PokemonFanClub_Text_TreatPokemonWithLove": [["POKéMON percebem como sao", "tratados por seus treinadores."], ["Cuide deles com carinho e", "a confianca vai crescer."]],
    "SlateportCity_PokemonFanClub_Text_PokemonDontLikeFainting": [["Se um POKéMON desmaia muitas", "vezes, sua confianca pode cair."], ["Cuide dele e evite forca-lo", "alem do limite."]],
    "SlateportCity_PokemonFanClub_Text_MonEnjoyedProtein": [["POKéMON gostam de certos itens?"], ["O meu ficou animado quando", "recebeu PROTEIN."]],
    "SlateportCity_PokemonFanClub_Text_Skitty": [["Pombim: Fffnyaaaah..."]],
    "SlateportCity_PokemonFanClub_Text_Zigzagoon": [["Pomba-Gira: Kyuuu..."]],
    "SlateportCity_PokemonFanClub_Text_Azumarill": [["Mate: Marimari?"]],
}

ITEM_NAMES = {
    "RED SCARF": "FITA VERMELHA",
    "BLUE SCARF": "FITA AZUL",
    "PINK SCARF": "FITA ROSA",
    "GREEN SCARF": "FITA VERDE",
    "YELLOW SCARF": "FITA AMARELA",
    "SOOTHE BELL": "SINO CALMANTE",
}

ITEM_DESCRIPTIONS = {
    "sRedScarfDesc": ["Item de segurar que", "realca ESTILO em", "CONCURSOS."],
    "sBlueScarfDesc": ["Item de segurar que", "realca BELEZA em", "CONCURSOS."],
    "sPinkScarfDesc": ["Item de segurar que", "realca FOFURA em", "CONCURSOS."],
    "sGreenScarfDesc": ["Item de segurar que", "realca ESPERTEZA em", "CONCURSOS."],
    "sYellowScarfDesc": ["Item de segurar que", "realca RESISTENCIA", "em CONCURSOS."],
    "sSootheBellDesc": ["Item de segurar que", "acalma e aumenta", "a amizade."],
}

STRING_BLOCK_RE_TEMPLATE = r"(?m)^{label}:\n(?:\t\.string .*\n)+"
DESC_BLOCK_RE_TEMPLATE = r'(?ms)^static const u8 {label}\[\] = _\(\n(?P<body>.*?^\s*"[^"\n]*"\);)'


def make_string_block(label: str, pages: list[list[str]]) -> str:
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


def make_desc_block(label: str, lines: list[str]) -> str:
    for text in lines:
        if len(text) > 32:
            raise ValueError(f"{label}: description line exceeds 32 chars: {text}")
    rendered = [f"static const u8 {label}[] = _("]
    for index, text in enumerate(lines):
        suffix = r"\n" if index < len(lines) - 1 else ""
        rendered.append(f'    "{text}{suffix}"')
    rendered[-1] += ");"
    return "\n".join(rendered)


def render_map(source: str) -> str:
    rendered = source
    for label, pages in TEXT_TARGETS.items():
        pattern = re.compile(STRING_BLOCK_RE_TEMPLATE.format(label=re.escape(label)))
        replacement = make_string_block(label, pages)
        rendered, count = pattern.subn(lambda _: replacement, rendered, count=1)
        if count != 1:
            raise ValueError(f"Fan Club: expected exactly one block for {label}, found {count}")
    return rendered


def render_items(source: str) -> str:
    rendered = source
    for old_name, new_name in ITEM_NAMES.items():
        old = f'.name = _("{old_name}"),'
        new = f'.name = _("{new_name}"),'
        count = rendered.count(old)
        if count != 1:
            raise ValueError(f"items.h: expected exactly one name {old_name}, found {count}")
        rendered = rendered.replace(old, new, 1)
    return rendered


def render_item_descs(source: str) -> str:
    rendered = source
    for label, lines in ITEM_DESCRIPTIONS.items():
        pattern = re.compile(DESC_BLOCK_RE_TEMPLATE.format(label=re.escape(label)))
        matches = list(pattern.finditer(rendered))
        if len(matches) != 1:
            raise ValueError(f"item_descriptions.h: expected exactly one block for {label}, found {len(matches)}")
        replacement = make_desc_block(label, lines)
        start, end = matches[0].span()
        rendered = rendered[:start] + replacement + rendered[end:]
    return rendered


def mask_map(source: str) -> str:
    return re.sub(r"(?m)^\t\.string .*\n", "", source)


def validate_rendered() -> None:
    source = MAP_PATH.read_text(encoding="utf-8")
    rendered = render_map(source)
    if mask_map(source) != mask_map(rendered):
        raise ValueError("Fan Club: non-text map structure changed")
    for label, pages in TEXT_TARGETS.items():
        if make_string_block(label, pages) not in rendered:
            raise ValueError(f"Fan Club: missing rendered block {label}")

    items = render_items(ITEMS_PATH.read_text(encoding="utf-8"))
    for new_name in ITEM_NAMES.values():
        if f'.name = _("{new_name}"),' not in items:
            raise ValueError(f"items.h: missing rendered item name {new_name}")

    descs = render_item_descs(DESCS_PATH.read_text(encoding="utf-8"))
    for label, lines in ITEM_DESCRIPTIONS.items():
        if make_desc_block(label, lines) not in descs:
            raise ValueError(f"item_descriptions.h: missing rendered description {label}")


def apply_in_place() -> None:
    map_source = MAP_PATH.read_text(encoding="utf-8")
    map_rendered = render_map(map_source)
    if mask_map(map_source) != mask_map(map_rendered):
        raise ValueError("Fan Club: non-text map structure changed")
    MAP_PATH.write_text(map_rendered, encoding="utf-8")
    ITEMS_PATH.write_text(render_items(ITEMS_PATH.read_text(encoding="utf-8")), encoding="utf-8")
    DESCS_PATH.write_text(render_item_descs(DESCS_PATH.read_text(encoding="utf-8")), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Render Porto do Sal Pokemon Fan Club surface and rewards in PT-BR.")
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--in-place", action="store_true")
    args = parser.parse_args()
    if args.check and args.in_place:
        parser.error("use either --check or --in-place")

    validate_rendered()
    if args.in_place:
        apply_in_place()
        print(f"Porto do Sal Fan Club renderer applied: {len(TEXT_TARGETS)} texts + {len(ITEM_NAMES)} item names + {len(ITEM_DESCRIPTIONS)} descriptions.")
    else:
        print(f"Porto do Sal Fan Club renderer OK: {len(TEXT_TARGETS)} texts + {len(ITEM_NAMES)} item names + {len(ITEM_DESCRIPTIONS)} descriptions.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
