#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / "data" / "maps" / "MossdeepCity_SpaceCenter_1F" / "scripts.inc"
MAX_VISIBLE_WIDTH = 32
CONTROL_RE = re.compile(r"\\[npl]")
PLACEHOLDER_RE = re.compile(r"\{[^}]+\}")

SOURCE_SIGNATURES = (
    "rocket's launch",
    "rocket launched safely",
    "haywire right now",
    "rocket launch demands",
    "Um sinal capaz de atravessar",
    "taking a stroll down the beach",
    "ARAUNA region has been famous",
    "A rede de comunicacao daqui",
    "With LEMBRANTES around",
    "POKéMON came",
    "CONSORCIO HORIZONTE should",
    "giant chunk of metal",
    "SEU BENTO: Quando um nome some",
    "Os engenheiros insistem",
)

TARGETS = {
    "MossdeepCity_SpaceCenter_1F_Text_RocketLaunchImminent": (
        "CENTRAL: O proximo lancamento\\n",
        "esta prestes a comecar!$",
    ),
    "MossdeepCity_SpaceCenter_1F_Text_SuccessfulLaunchNumber": (
        "CENTRAL: Lancamento concluido\\n",
        "com seguranca!\\p",
        "Este foi o lancamento n.\\n",
        "{STR_VAR_1}!$",
    ),
    "MossdeepCity_SpaceCenter_1F_Text_HaywireButRocketLaunchImminent": (
        "CENTRAL: A ocupacao alterou a\\n",
        "rotina, mas a janela orbital\\n",
        "continua aberta.\\p",
        "O lancamento e iminente.$",
    ),
    "MossdeepCity_SpaceCenter_1F_Text_HaywireButSuccessfulLaunchNumber": (
        "CENTRAL: Mesmo com a ocupacao,\\n",
        "o lancamento foi seguro.\\p",
        "Este foi o lancamento n.\\n",
        "{STR_VAR_1}!$",
    ),
    "MossdeepCity_SpaceCenter_1F_Text_RocketLaunchDemandsPerfection": (
        "CIENTISTA: Um lancamento nao\\n",
        "aceita erro pequeno.\\p",
        "Um por cento basta para perder\\n",
        "anos de trabalho.\\p",
        "Ainda assim, tentamos de novo.\\n",
        "E por isso que estamos aqui.$",
    ),
    "MossdeepCity_SpaceCenter_1F_Text_MagmaHaveSightsOnSpaceCenter": (
        "CIENTISTA: Os LEMBRANTES querem\\n",
        "o uplink regional.\\p",
        "Ele conversa com estacoes em\\n",
        "quase toda Arauna.$",
    ),
    "MossdeepCity_SpaceCenter_1F_Text_FoundThisYouCanHaveIt": (
        "HOMEM: Encontrei esta pedra numa\\n",
        "caminhada perto da costa.\\p",
        "Nao tenho uso para ela.\\n",
        "Pode ficar.$",
    ),
    "MossdeepCity_SpaceCenter_1F_Text_HoennFamousForMeteorShowers": (
        "HOMEM: Arauna recebe chuvas de\\n",
        "meteoros ha muitas geracoes.\\p",
        "Foi assim que MISSOES DO CEU\\n",
        "comecou a observar o alto.$",
    ),
    "MossdeepCity_SpaceCenter_1F_Text_MagmaCantStealFuelTakeThis": (
        "HOMEM: Antes que a ocupacao\\n",
        "piore, leve esta pedra.\\p",
        "Prefiro que saia daqui com voce.$",
    ),
    "MossdeepCity_SpaceCenter_1F_Text_CantStrollOnBeachWithMagma": (
        "HOMEM: Com o predio ocupado,\\n",
        "ninguem pensa em caminhar pela\\n",
        "costa agora.$",
    ),
    "MossdeepCity_SpaceCenter_1F_Text_DidPokemonComeFromSpace": (
        "MULHER: Alguns pesquisadores\\n",
        "acham que certos POKéMON podem\\n",
        "ter vindo do espaco.\\p",
        "Eu ainda gosto da pergunta.$",
    ),
    "MossdeepCity_SpaceCenter_1F_Text_AquaShouldBeatMagma": (
        "MULHER: Queria que tirassem\\n",
        "os LEMBRANTES daqui.\\p",
        "Mas entregar o predio ao\\n",
        "HORIZONTE tambem me assusta.$",
    ),
    "MossdeepCity_SpaceCenter_1F_Text_RocketsBoggleMyMind": (
        "VELHO: Uma maquina enorme rompe\\n",
        "o ceu e continua subindo.\\p",
        "Mesmo depois de tantos anos,\\n",
        "isso ainda me espanta.$",
    ),
    "MossdeepCity_SpaceCenter_1F_Text_MagmaWantsToSpoilMyDream": (
        "VELHO: Esperei anos para ver um\\n",
        "lancamento de perto.\\p",
        "Agora duas faccoes transformaram\\n",
        "o centro em campo de disputa.$",
    ),
    "MossdeepCity_SpaceCenter_1F_Text_StevenMagmaCantBeAllowedToTakeFuel": (
        "SEU BENTO: O andar de cima tem\\n",
        "a chave do uplink regional.\\p",
        "Nao podemos deixar uma faccao\\n",
        "decidir sozinha por toda Arauna.$",
    ),
    "MossdeepCity_SpaceCenter_1F_Text_Grunt3Intro": (
        "LEMBRANTE: O transmissor alcanca\\n",
        "sensores muito alem desta ilha.$",
    ),
    "MossdeepCity_SpaceCenter_1F_Text_Grunt3Defeat": (
        "LEMBRANTE: Se o HORIZONTE ligar\\n",
        "isso ao ARQUIVO, a escala muda.$",
    ),
    "MossdeepCity_SpaceCenter_1F_Text_Grunt3PostBattle": (
        "LEMBRANTE: RAUL esta no andar\\n",
        "superior. Ele sabe da chave.$",
    ),
    "MossdeepCity_SpaceCenter_1F_Text_Grunt1Intro": (
        "LEMBRANTE: Isto nao e base do\\n",
        "HORIZONTE. Eu sei.\\p",
        "Mas a rede pode virar uma.$",
    ),
    "MossdeepCity_SpaceCenter_1F_Text_Grunt1Defeat": (
        "LEMBRANTE: Civil tambem usa este\\n",
        "uplink... Eu sei.$",
    ),
    "MossdeepCity_SpaceCenter_1F_Text_Grunt1PostBattle": (
        "LEMBRANTE: Nao gosto de ocupar\\n",
        "um centro publico.\\p",
        "Gosto menos da alternativa.$",
    ),
    "MossdeepCity_SpaceCenter_1F_Text_Grunt4Intro": (
        "LEMBRANTE: O uplink nao leva\\n",
        "memorias. Ele leva comandos.$",
    ),
    "MossdeepCity_SpaceCenter_1F_Text_Grunt4Defeat": (
        "LEMBRANTE: Um comando remoto\\n",
        "pode ativar muitos sensores.$",
    ),
    "MossdeepCity_SpaceCenter_1F_Text_Grunt4PostBattle": (
        "LEMBRANTE: E esse e exatamente\\n",
        "o tipo de atalho que M'BOI devia\\n",
        "ter nos ensinado a temer.$",
    ),
    "MossdeepCity_SpaceCenter_1F_Text_Grunt2Intro": (
        "LEMBRANTE: A escada fechou.\\p",
        "LUZIA e RAUL estao la em cima.$",
    ),
    "MossdeepCity_SpaceCenter_1F_Text_Grunt2Defeat": (
        "LEMBRANTE: Certo... passe.\\p",
        "Mas escute antes de escolher um\\n",
        "lado.$",
    ),
    "MossdeepCity_SpaceCenter_1F_Text_Grunt2PostBattle": (
        "LEMBRANTE: O problema nao e o\\n",
        "centro espacial.\\p",
        "E quem controla a chave.$",
    ),
    "MossdeepCity_SpaceCenter_1F_Text_MagmaIntentToStealNotice": (
        "AVISO DOS LEMBRANTES:\\p",
        "O uplink regional sera desligado\\n",
        "ate a chave de sincronismo ser\\n",
        "neutralizada.\\p",
        "Nenhum dado civil sera apagado.$",
    ),
}


def block_pattern(label: str) -> re.Pattern[str]:
    return re.compile(rf"(?ms)^{re.escape(label)}:\n(?P<body>.*?)(?=^[A-Za-z0-9_]+(?:::|:)(?:\n|$)|\Z)")


def visible_segments(payload: str) -> list[str]:
    cleaned = PLACEHOLDER_RE.sub("9999", payload).replace("$", "")
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
        raise ValueError("non-dialogue structure changed while rendering Missoes do Ceu ground floor")
    for token in ("The rocket", "HOENN", "With LEMBRANTES around", "CONSORCIO HORIZONTE should", "When a name"):
        for label in TARGETS:
            body = block_pattern(label).search(rendered).group("body")
            if token in body:
                raise ValueError(f"{label}: stale ground-floor token survived: {token}")
    return rendered


def main() -> int:
    parser = argparse.ArgumentParser(description="Render Missoes do Ceu 1F daily operations and Lembrantes occupation.")
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--in-place", action="store_true")
    args = parser.parse_args()
    if args.check and args.in_place:
        parser.error("use either --check or --in-place")

    source = TARGET.read_text(encoding="utf-8")
    rendered = render(source)
    if args.check:
        print(f"Missoes do Ceu 1F renderer OK: {len(TARGETS)} blocks validated.")
        return 0
    if args.in_place:
        TARGET.write_text(rendered, encoding="utf-8")
        return 0
    print(rendered, end="" if rendered.endswith("\n") else "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
