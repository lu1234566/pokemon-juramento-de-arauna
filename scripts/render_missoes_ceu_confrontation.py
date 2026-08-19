#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / "data" / "maps" / "MossdeepCity_SpaceCenter_2F" / "scripts.inc"
MAX_VISIBLE_WIDTH = 32
CONTROL_RE = re.compile(r"\\[npl]")
PLACEHOLDER_RE = re.compile(r"\{[^}]+\}")

SOURCE_SIGNATURES = (
    "MOSSDEEP has mainly",
    "Os engenheiros insistem",
    "If only I was",
    "A rede de comunicacao daqui",
    "I wish ordinary people",
    "Um sinal capaz de atravessar",
    "What's wrong with you",
    "Good answer",
    "Hehehe!",
    "LUZIA: O problema nunca foi",
    "SEU BENTO: Quando um nome some",
    "Os sensores registram duas",
    "All I want",
    "I'm with our leader",
    "LUZIA: Ninguem tem o direito",
)

TARGETS = {
    "MossdeepCity_SpaceCenter_2F_Text_MossdeepIdealForRockets": (
        "CIENTISTA: MISSOES DO CEU tem\\n",
        "ventos estaveis e horizonte\\n",
        "aberto.\\p",
        "Por isso nossas antenas cobrem\\n",
        "quase toda Arauna.$",
    ),
    "MossdeepCity_SpaceCenter_2F_Text_WhyWouldMagmaStealRocketFuel": (
        "CIENTISTA: O uplink regional\\n",
        "pode sincronizar sensores de\\n",
        "VINCULO em toda Arauna.\\p",
        "Os LEMBRANTES querem corta-lo.$",
    ),
    "MossdeepCity_SpaceCenter_2F_Text_WouldveLikedToBeAstronaut": (
        "HOMEM: Quando eu era jovem,\\n",
        "queria ver Arauna do alto.\\p",
        "Talvez ainda nao seja tarde\\n",
        "para aprender algo novo.$",
    ),
    "MossdeepCity_SpaceCenter_2F_Text_MagmaCantGetAwayWithThis": (
        "HOMEM: Cortar uma rede civil\\n",
        "tambem atinge quem nao escolheu\\n",
        "esta disputa.$",
    ),
    "MossdeepCity_SpaceCenter_2F_Text_WishOrdinaryPeopleCouldGoIntoSpace": (
        "GAROTO: Um dia eu quero que o\\n",
        "ceu nao seja privilegio de\\n",
        "cientista ou gente rica.$",
    ),
    "MossdeepCity_SpaceCenter_2F_Text_DoesMagmaWantToGoToSpace": (
        "GAROTO: Os LEMBRANTES nao vieram\\n",
        "pelo ceu.\\p",
        "Eles querem a rede que fala com\\n",
        "toda Arauna.$",
    ),
    "MossdeepCity_SpaceCenter_2F_Text_YoureOutnumberedTakeUsOn": (
        "LEMBRANTE: Somos tres.\\p",
        "Ainda quer passar?$",
    ),
    "MossdeepCity_SpaceCenter_2F_Text_GoodAnswer": (
        "LEMBRANTE: Melhor assim.\\p",
        "Nao precisamos de outra luta.$",
    ),
    "MossdeepCity_SpaceCenter_2F_Text_Grunt5Intro": (
        "LEMBRANTE: Se o HORIZONTE ligar\\n",
        "essa rede ao ARQUIVO VIVO,\\p",
        "o protocolo chega a toda Arauna.$",
    ),
    "MossdeepCity_SpaceCenter_2F_Text_Grunt5Defeat": (
        "LEMBRANTE: Desligar o uplink era\\n",
        "para impedir outro M'BOI.$",
    ),
    "MossdeepCity_SpaceCenter_2F_Text_Grunt5PostBattle": (
        "LEMBRANTE: Mas gente comum usa\\n",
        "esta rede tambem.\\p",
        "Eu sei.$",
    ),
    "MossdeepCity_SpaceCenter_2F_Text_Grunt6Intro": (
        "LEMBRANTE: RAUL mandou segurar\\n",
        "este andar enquanto LUZIA chega\\n",
        "ao transmissor.$",
    ),
    "MossdeepCity_SpaceCenter_2F_Text_Grunt6Defeat": (
        "LEMBRANTE: Nao estamos roubando\\n",
        "combustivel.\\p",
        "Queremos a chave de sincronismo.$",
    ),
    "MossdeepCity_SpaceCenter_2F_Text_Grunt6PostBattle": (
        "LEMBRANTE: Se essa chave ficar\\n",
        "com o HORIZONTE, eles podem\\n",
        "acionar sensores de longe.$",
    ),
    "MossdeepCity_SpaceCenter_2F_Text_Grunt7Intro": (
        "LEMBRANTE: LUZIA quer transmitir\\n",
        "os registros de M'BOI antes de\\n",
        "destruir a chave.$",
    ),
    "MossdeepCity_SpaceCenter_2F_Text_Grunt7Defeat": (
        "LEMBRANTE: Expor a verdade nao\\n",
        "devia exigir tomar uma rede\\n",
        "inteira.$",
    ),
    "MossdeepCity_SpaceCenter_2F_Text_Grunt7PostBattle": (
        "LEMBRANTE:\\n",
        "Talvez SEU BENTO tenha razao.\\p",
        "Nao conte que eu disse.$",
    ),
    "MossdeepCity_SpaceCenter_2F_Text_WellTakeCareOfYou": (
        "RAUL: Outra vez voce.\\p",
        "Viemos impedir a sincronizacao,\\n",
        "nao discutir com voce.\\p",
        "Mas nao vamos sair do caminho.$",
    ),
    "MossdeepCity_SpaceCenter_2F_Text_MaxieDontInterfere": (
        "LUZIA: O HORIZONTE pode usar\\n",
        "este uplink para comandar o\\n",
        "ARQUIVO em escala regional.\\p",
        "Nao vou permitir.$",
    ),
    "MossdeepCity_SpaceCenter_2F_Text_StevenWhyStealRocketFuel": (
        "SEU BENTO: Impedir o HORIZONTE\\n",
        "nao exige tomar uma rede usada\\n",
        "por toda a cidade.\\p",
        "Quem autorizou voces?$",
    ),
    "MossdeepCity_SpaceCenter_2F_Text_MaxieUseFuelToEruptVolcano": (
        "LUZIA:\\n",
        "Quero transmitir as provas de\\n",
        "M'BOI e destruir a chave de\\n",
        "sincronismo.\\p",
        "Depois a rede volta.$",
    ),
    "MossdeepCity_SpaceCenter_2F_Text_StevenAreYouReadyToBattle": (
        "SEU BENTO: {PLAYER}, vou impedir\\n",
        "que tomem o transmissor.\\p",
        "Luta comigo?$",
    ),
    "MossdeepCity_SpaceCenter_2F_Text_StevenHurryGetReadyQuickly": (
        "SEU BENTO: Prepare sua equipe.\\p",
        "Eu seguro a passagem.$",
    ),
    "MossdeepCity_SpaceCenter_2F_Text_JustWantToExpandLand": (
        "LUZIA: Eu so preciso quebrar a\\n",
        "chave antes que o HORIZONTE a\\n",
        "use.$",
    ),
    "MossdeepCity_SpaceCenter_Text_TabithaDefeat": (
        "RAUL: Estou com LUZIA.\\p",
        "Mas queria que houvesse outro\\n",
        "jeito.$",
    ),
    "MossdeepCity_SpaceCenter_2F_Text_MaxieWeFailedIsAquaAlsoMisguided": (
        "LUZIA: Entendi.\\p",
        "Tomar a rede para impedir que\\n",
        "outros a controlem ainda e\\n",
        "tomar a rede.$",
    ),
    "MossdeepCity_SpaceCenter_2F_Text_MaxieWeWillGiveUp": (
        "LUZIA: Vamos sair.\\p",
        "As provas de M'BOI continuam\\n",
        "existindo.\\p",
        "Eu encontro outra forma de\\n",
        "faze-las circular.$",
    ),
    "MossdeepCity_SpaceCenter_2F_Text_StevenThankYouComeSeeMeAtHome": (
        "SEU BENTO: Obrigado, {PLAYER}.\\p",
        "A rede continua livre dos dois\\n",
        "lados.\\p",
        "Passe na minha casa depois.\\n",
        "Quero lhe mostrar uma coisa.$",
    ),
}


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
            raise ValueError(f"{label}: target is not a text block")
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


def render(source: str) -> str:
    validate_widths()
    rendered = replace_blocks(source)
    if mask_blocks(source) != mask_blocks(rendered):
        raise ValueError("non-dialogue structure changed while rendering Missoes do Ceu confrontation")
    for token in ("expand the land mass", "I'm with our leader", "fuel, and we're", "What's wrong with you?"):
        for label in TARGETS:
            body = block_pattern(label).search(rendered).group("body")
            if token in body:
                raise ValueError(f"{label}: stale Space Center token survived: {token}")
    return rendered


def main() -> int:
    parser = argparse.ArgumentParser(description="Render the Missoes do Ceu 2F Lembrantes/Seu Bento confrontation.")
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--in-place", action="store_true")
    args = parser.parse_args()
    if args.check and args.in_place:
        parser.error("use either --check or --in-place")

    source = TARGET.read_text(encoding="utf-8")
    rendered = render(source)
    if args.check:
        print(f"Missoes do Ceu confrontation renderer OK: {len(TARGETS)} blocks validated.")
        return 0
    if args.in_place:
        TARGET.write_text(rendered, encoding="utf-8")
        return 0
    print(rendered, end="" if rendered.endswith("\n") else "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
