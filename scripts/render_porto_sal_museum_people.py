#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CITY_PATH = ROOT / "data" / "maps" / "SlateportCity" / "scripts.inc"
MUSEUM_PATH = ROOT / "data" / "maps" / "SlateportCity_OceanicMuseum_1F" / "scripts.inc"
MAX_VISIBLE_WIDTH = 32
CONTROL_RE = re.compile(r"\\[npl]")
PLACEHOLDER_RE = re.compile(r"\{[^}]+\}")

CITY_TARGETS: dict[str, tuple[tuple[str, ...], tuple[str, ...]]] = {
    "SlateportCity_Text_WhatsLongLineOverThere": (("long line",), (
        "HOMEM: O que esta acontecendo?\\n", "Olha o tamanho dessa fila.$",
    )),
    "SlateportCity_Text_VisitedMuseumOften": (("visited", "MUSEUM"), (
        "MULHER: Eu vinha muito ao MUSEU\\n", "quando era crianca.\\p",
        "Foi aqui que aprendi a gostar\\n", "dos misterios do mar.$",
    )),
    "SlateportCity_Text_QuitPushing": (("Quit pushing",), (
        "HORIZONTE: Sem empurrar.\\p", "A fila comeca aqui.$",
    )),
    "SlateportCity_Text_AquaHasPolicy": (("projeto de M'BOI",), (
        "HORIZONTE: A ordem e entrar sem\\n", "chamar atencao.\\p",
        "Entao sim, vamos pagar ingresso.$",
    )),
    "SlateportCity_Text_BossIsBrilliant": (("Nao somos soldados",), (
        "HORIZONTE: O diretor quer avaliar\\n", "equipamentos oceanograficos.\\p",
        "Nao sei por que tanta gente veio.$",
    )),
    "SlateportCity_Text_WhatsNewSchemeIWonder": (("new scheme",), (
        "HORIZONTE: Disseram apenas\\n", "'inspecao de campo'.\\p",
        "Quando a ordem e vaga assim, eu\\n", "fico mais preocupado.$",
    )),
    "SlateportCity_Text_ShouldTakeItAll": (("take it all",), (
        "HORIZONTE: Se o equipamento for\\n", "essencial, deviamos requisitar.\\p",
        "Foi para isso que viemos, nao?$",
    )),
    "SlateportCity_Text_DontButtIn": (("Don't butt in",), (
        "HORIZONTE: Ei, respeite a fila.$",
    )),
    "SlateportCity_Text_RemindsMeOfLongLineForGames": (("smash-hit games",), (
        "HORIZONTE: Faz tempo que nao vejo\\n", "uma fila desse tamanho.\\p",
        "Parece lancamento de jogo.$",
    )),
    "SlateportCity_Text_WhyAreWeLiningUp": (("lining up and paying",), (
        "HORIZONTE: Por que estamos pagando\\n", "para entrar?\\p",
        "HORIZONTE: Porque e um MUSEU\\n", "civil. Pague e entre.$",
    )),
    "SlateportCity_Text_WhatDoYouWant": (("What do you want",), (
        "HORIZONTE: Precisa de algo?$",
    )),
    "SlateportCity_Text_IllReadSignForYou": (("read this sign",), (
        "HORIZONTE: Quer ler a placa?\\n", "Eu leio para voce.$",
    )),
    "SlateportCity_Text_SaysSomethingLikeSeaIsEndless": (("life in the sea",), (
        "HORIZONTE: Diz que a vida no mar\\n", "nao tem fim.\\p",
        "Bonito. Acho que e isso.$",
    )),
    "SlateportCity_Text_ShouldveBroughtMyGameBoy": (("Game Boy",), (
        "HORIZONTE: Devia ter trazido algo\\n", "para passar o tempo.\\p",
        "Essa fila nao anda.$",
    )),
    "SlateportCity_Text_HotSpringsAfterOperation": (("hot spring",), (
        "HORIZONTE: Quando a missao acabar,\\n", "eu pago o jantar.\\p",
        "Se a gente sair daqui hoje.$",
    )),
}

MUSEUM_TARGETS: dict[str, tuple[tuple[str, ...], tuple[str, ...]]] = {
    "SlateportCity_OceanicMuseum_1F_Text_WouldYouLikeToEnter": (("entrance fee",), (
        "RECEPCAO: Bem-vindo ao MUSEU\\n", "OCEANOGRAFICO.\\p",
        "A entrada custa ¥50.\\n", "Deseja entrar?$",
    )),
    "SlateportCity_OceanicMuseum_1F_Text_PleaseEnjoyYourself": (("Please enjoy",), (
        "RECEPCAO: Aproveite a visita.$",
    )),
    "SlateportCity_OceanicMuseum_1F_Text_NotEnoughMoney": (("enough money",), (
        "RECEPCAO: Desculpe, voce nao tem\\n", "dinheiro suficiente.$",
    )),
    "SlateportCity_OceanicMuseum_1F_Text_CatchUpWithYourGroup": (("catch up",), (
        "RECEPCAO: Voce veio com o grupo\\n", "de tecnicos?\\p",
        "Eles ja subiram. Pode entrar.$",
    )),
    "SlateportCity_OceanicMuseum_1F_Text_AquaExistForGoodOfAll": (("projeto de M'BOI",), (
        "HORIZONTE: Sou tecnico de campo,\\n", "nao turista.\\p",
        "Mas ja que paguei, vou olhar.$",
    )),
    "SlateportCity_OceanicMuseum_1F_Text_OurBossIsntHere": (("ARQUIVO VIVO",), (
        "HORIZONTE: OTACILIO ainda nao\\n", "chegou.\\p",
        "A equipe devia so observar.$",
    )),
    "SlateportCity_OceanicMuseum_1F_Text_WouldStuffHereMakeMeRich": (("make me rich",), (
        "HORIZONTE: Tem equipamento caro\\n", "aqui.\\p",
        "Nao, nao viemos roubar isso.$",
    )),
    "SlateportCity_OceanicMuseum_1F_Text_CanLearnForNefariousDeeds": (("nefarious deeds",), (
        "HORIZONTE: Esses modelos explicam\\n", "correntes e pressao.\\p",
        "Isso pode ser util em campo.$",
    )),
    "SlateportCity_OceanicMuseum_1F_Text_RustboroBungled": (("RUSTBORO",), (
        "HORIZONTE: Se a operacao anterior\\n", "tivesse dado certo, eu nao estaria\\n", "aqui hoje.$",
    )),
    "SlateportCity_OceanicMuseum_1F_Text_DidntHaveMoney": (("didn't have ¥50",), (
        "HORIZONTE: Tive que pagar ¥50\\n", "como todo mundo.\\p",
        "Ordem e ordem.$",
    )),
    "SlateportCity_OceanicMuseum_1F_Text_LearnAboutSeaForBattling": (("sensores registram",), (
        "VISITANTE: Vim aprender sobre o\\n", "mar para entender meus POKéMON.$",
    )),
    "SlateportCity_OceanicMuseum_1F_Text_SternIsRoleModel": (("CAPT. STERN",), (
        "VISITANTE: O ENGENHEIRO DO PORTO\\n", "e minha maior inspiracao.\\p",
        "Quero explorar o fundo do mar.$",
    )),
    "SlateportCity_OceanicMuseum_1F_Text_MustBePokemonWeDontKnow": (("many POKéMON",), (
        "VISITANTE: O mar parece nao ter\\n", "fim.\\p",
        "Quantos POKéMON ainda vivem onde\\n", "ninguem conseguiu chegar?$",
    )),
    "SlateportCity_OceanicMuseum_1F_Text_WantSeaPokemon": (("sea POKéMON",), (
        "VISITANTE: Quero um POKéMON do\\n", "mar.\\p",
        "Deve ser gelado e gostoso de\\n", "abracar.$",
    )),
    "SlateportCity_OceanicMuseum_1F_Text_RememberMeTakeThis": (("projeto de M'BOI",), (
        "HORIZONTE: Voce me derrotou antes.\\p",
        "Esta TM nao devia estar comigo.\\n", "Leve. Considere uma divida.$",
    )),
    "SlateportCity_OceanicMuseum_1F_Text_HopeINeverSeeYouAgain": (("Hope I never see",), (
        "HORIZONTE: Pronto. Estamos quites.\\p",
        "Espero que da proxima vez a gente\\n", "nao esteja em lados opostos.$",
    )),
    "SlateportCity_OceanicMuseum_1F_Text_YouHaveToTakeThis": (("have to take this",), (
        "HORIZONTE: Sua bolsa esta cheia?\\p",
        "Volte com espaco. Eu ainda preciso\\n", "lhe entregar essa TM.$",
    )),
}


def block_pattern(label: str) -> re.Pattern[str]:
    return re.compile(rf"(?ms)^{re.escape(label)}:\n(?P<body>.*?)(?=^[A-Za-z0-9_]+(?:::|:)(?:\n|$)|\Z)")


def visible_segments(payload: str) -> list[str]:
    cleaned = PLACEHOLDER_RE.sub("PLAYER", payload).replace("$", "")
    return [part.strip() for part in CONTROL_RE.split(cleaned)]


def validate_widths(targets: dict[str, tuple[tuple[str, ...], tuple[str, ...]]]) -> None:
    for label, (_, payloads) in targets.items():
        for payload in payloads:
            for segment in visible_segments(payload):
                if len(segment) > MAX_VISIBLE_WIDTH:
                    raise ValueError(f"{label}: {len(segment)} visible chars: {segment!r}")


def render(source: str, targets: dict[str, tuple[tuple[str, ...], tuple[str, ...]]]) -> str:
    validate_widths(targets)
    rendered = source
    for label, (markers, payloads) in targets.items():
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
        for label in targets:
            match = block_pattern(label).search(masked)
            if not match:
                raise ValueError(f"{label}: cannot mask missing block")
            start, end = match.span("body")
            masked = masked[:start] + '\t.string "<ARAUNA_RENDERED_BLOCK>"\n\n' + masked[end:]
        return masked

    if mask(source) != mask(rendered):
        raise ValueError("non-dialogue structure changed while rendering museum people")
    return rendered


def render_city(source: str) -> str:
    rendered = render(source, CITY_TARGETS)
    for token in ("Game Boy", "new scheme", "take it all", "hot spring"):
        for label in CITY_TARGETS:
            if token in block_pattern(label).search(rendered).group("body"):
                raise ValueError(f"{label}: stale queue token survived: {token}")
    return rendered


def render_museum(source: str) -> str:
    rendered = render(source, MUSEUM_TARGETS)
    for token in ("CAPT. STERN", "RUSTBORO", "nefarious deeds", "Hope I never see"):
        for label in MUSEUM_TARGETS:
            if token in block_pattern(label).search(rendered).group("body"):
                raise ValueError(f"{label}: stale museum-person token survived: {token}")
    return rendered


def main() -> int:
    parser = argparse.ArgumentParser(description="Render Porto do Sal museum queue, reception, people and TM handoff.")
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--in-place", action="store_true")
    args = parser.parse_args()
    if args.check and args.in_place:
        parser.error("use either --check or --in-place")

    city = render_city(CITY_PATH.read_text(encoding="utf-8"))
    museum = render_museum(MUSEUM_PATH.read_text(encoding="utf-8"))
    if args.check:
        print(
            "Porto do Sal museum people renderer OK: "
            f"{len(CITY_TARGETS)} queue blocks and {len(MUSEUM_TARGETS)} museum blocks validated."
        )
        return 0
    if args.in_place:
        CITY_PATH.write_text(city, encoding="utf-8")
        MUSEUM_PATH.write_text(museum, encoding="utf-8")
        return 0
    print(city, end="" if city.endswith("\n") else "\n")
    print(museum, end="" if museum.endswith("\n") else "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
