#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

import render_aguas_mboi_surface as base

ROOT = Path(__file__).resolve().parents[1]
CITY_PATH = base.CITY_PATH
TOWER_PATH = base.TOWER_PATH
BERRIES_PATH = ROOT / "data" / "text" / "berries.inc"

DAILY_CITY_TARGETS: dict[str, tuple[tuple[str, ...], tuple[str, ...]]] = {
    "SootopolisCity_Text_PhysicallyFitLivingHere": (
        ("Diving in the sea", "physically fit"),
        (
            "HOMEM: Aqui voce mergulha,\\n",
            "sobe escadas, cruza pontes...\\p",
            "Em AGUAS DE M'BOI ate caminhar\\n",
            "e exercicio.$",
        ),
    ),
    "SootopolisCity_Text_WonderWhatWorldIsLike": (
        ("never been out of this city", "round sky"),
        (
            "GAROTO: Nunca sai de AGUAS DE\\n",
            "M'BOI.\\p",
            "Quero ver como o ceu parece\\n",
            "sem a borda da cratera.$",
        ),
    ),
    "SootopolisCity_Text_NoOrdinaryTourist": (
        ("ordinary tourist", "SOOTOPOLIS"),
        (
            "HOMEM: Voce veio de longe?\\p",
            "Pouca gente chega a AGUAS DE\\n",
            "M'BOI por acaso.$",
        ),
    ),
    "SootopolisCity_Text_SootopolisSkyBeautiful": (
        ("SOOTOPOLIS sprang up", "crater of a volcano"),
        (
            "MULHER: A cidade cresceu dentro\\n",
            "de uma cratera.\\p",
            "O ceu aparece como um circulo.\\p",
            "Por isso a noite daqui parece\\n",
            "uma janela aberta.$",
        ),
    ),
    "SootopolisCity_Text_NightSkyFavoriteScenery": (
        ("circle of a night sky", "favorite scenery"),
        (
            "MULHER: A noite, a borda da\\n",
            "cratera vira moldura.\\p",
            "As estrelas parecem boiar sobre\\n",
            "a agua. E meu lugar favorito.$",
        ),
    ),
    "SootopolisCity_Text_WhereDidLegendariesGo": (
        ("resultado de duas ideias", "apagar a dor"),
        (
            "MENINO: As correntes sumiram,\\n",
            "mas a cidade lembra do colapso.\\p",
            "Minha mae anota nossos nomes\\n",
            "antes de dormir agora.$",
        ),
    ),
    "SootopolisCity_Text_WeatherWentWild": (
        ("resultado de duas ideias", "apagar a dor"),
        (
            "MULHER: Antes da crise a agua\\n",
            "mudou primeiro.\\p",
            "Depois vieram memorias que nao\\n",
            "eram nossas.$",
        ),
    ),
    "SootopolisCity_Text_ExplainWaterfallGoToGym": (
        ("HIDDEN MACHINE", "INSÍGNIA NASCENTE", "ÁGUAS DE M'BOI"),
        (
            "AMALIA: Esta HM ensina\\n",
            "WATERFALL.\\p",
            "Com a INSIGNIA NASCENTE, um\\n",
            "POKéMON pode subir cachoeiras.\\p",
            "Voce consegue a insignia no\\n",
            "GINASIO de AGUAS DE M'BOI.$",
        ),
    ),
}

KIRI_TARGETS: dict[str, tuple[tuple[str, ...], tuple[str, ...]]] = {
    "SootopolisCity_Text_NameIsKiriHaveOneOfThese": (
        ("what's your name", "My name is KIRI", "You can have one"),
        (
            "Oi! Qual e o seu nome?\\p",
            "... ... ...\\p",
            "Gostei! Eu sou KIRI.\\p",
            "Meus pais escolheram esse nome\\n",
            "como um desejo de saude e\\n",
            "gentileza.\\p",
            "Pode ficar com uma destas.$",
        ),
    ),
    "SootopolisCity_Text_GiveYouThisBerryToo": (
        ("KIRI will give you this BERRY",),
        ("KIRI: Leve esta BERRY tambem!\\p", "Eu gosto muito dela.$"),
    ),
    "SootopolisCity_Text_WhatKindOfWishInYourName": (
        ("what kind of wish", "your name"),
        ("KIRI: Que desejo sera que\\n", "colocaram no seu nome?$"),
    ),
    "SootopolisCity_Text_LikeSeasonBornIn": (
        ("Spring, summer, autumn", "born in springtime"),
        (
            "KIRI: Primavera, verao, outono,\\n",
            "inverno...\\p",
            "Quem nasce numa estacao acaba\\n",
            "gostando mais dela?$",
        ),
    ),
    "SootopolisCity_Text_ThenILoveAutumn": (
        ("KIRI was born in the autumn", "Which season"),
        (
            "KIRI: Eu nasci no outono,\\n",
            "entao gosto do outono!\\p",
            "E voce, qual estacao prefere?$",
        ),
    ),
    "SootopolisCity_Text_OhDoesntMatter": (
        ("It doesn't matter", "want to know"),
        (
            "KIRI: Ah... tudo bem.\\p",
            "Ainda tenho tanta coisa que\\n",
            "quero descobrir.$",
        ),
    ),
}


def render_city(source: str) -> str:
    rendered = base.render_city(source)
    rendered = base.render(rendered, DAILY_CITY_TARGETS)
    for label in DAILY_CITY_TARGETS:
        body = base.block_pattern(label).search(rendered).group("body")
        for token in ("SOOTOPOLIS", "physically fit", "ordinary tourist", "HIDDEN MACHINE"):
            if token in body:
                raise ValueError(f"{label}: legacy daily token survived: {token}")
    return rendered


def render_tower(source: str) -> str:
    return base.render_tower(source)


def render_berries(source: str) -> str:
    rendered = base.render(source, KIRI_TARGETS)
    for label in KIRI_TARGETS:
        body = base.block_pattern(label).search(rendered).group("body")
        for token in ("My name is KIRI", "It doesn't matter", "Which season"):
            if token in body:
                raise ValueError(f"{label}: legacy Kiri token survived: {token}")
    return rendered


def rendered_sources() -> dict[Path, str]:
    return {
        CITY_PATH: render_city(CITY_PATH.read_text(encoding="utf-8")),
        TOWER_PATH: render_tower(TOWER_PATH.read_text(encoding="utf-8")),
        BERRIES_PATH: render_berries(BERRIES_PATH.read_text(encoding="utf-8")),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Render Aguas de M'Boi daily life and Kiri surfaces on top of the crisis renderer.")
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--in-place", action="store_true")
    args = parser.parse_args()
    if args.check and args.in_place:
        parser.error("use either --check or --in-place")

    rendered = rendered_sources()
    if args.check:
        print(
            "Aguas daily renderer OK: "
            f"{len(DAILY_CITY_TARGETS)} city blocks and {len(KIRI_TARGETS)} Kiri blocks validated."
        )
        return 0
    if args.in_place:
        for path, content in rendered.items():
            path.write_text(content, encoding="utf-8")
        return 0
    for path, content in rendered.items():
        print(f"===== {path.relative_to(ROOT)} =====")
        print(content, end="" if content.endswith("\n") else "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
