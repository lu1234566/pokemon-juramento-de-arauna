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
    "SlateportCity_Text_EnergyGuruSellWhatYouNeed": (("ENERGY GURU",), (
        "LOJISTA: Precisa fortalecer seu\\n",
        "POKéMON? Tenho o que procura.$",
    )),
    "SlateportCity_Text_OhYourPokemon": (("Your {STR_VAR_1}",), (
        "AVALIADORA: Ah...\\n",
        "seu {STR_VAR_1}.$",
    )),
    "SlateportCity_Text_PleaseGiveItThisEffortRibbon": (("EFFORT RIBBON",), (
        "AVALIADORA: Treinou de verdade!\\p",
        "Ele merece esta FITA DE\\n",
        "ESFORCO.$",
    )),
    "SlateportCity_Text_ReceivedEffortRibbon": (("received the EFFORT RIBBON",), (
        "{PLAYER} recebeu a FITA DE\\n",
        "ESFORCO!$",
    )),
    "SlateportCity_Text_PutEffortRibbonOnMon": (("put the EFFORT RIBBON",), (
        "{PLAYER} colocou a FITA DE\\n",
        "ESFORCO em {STR_VAR_1}.$",
    )),
    "SlateportCity_Text_GoForItLittleHarder": (("little harder",), (
        "AVALIADORA: Ainda pode melhorar.\\p",
        "Continue treinando e eu terei\\n",
        "algo especial para seu POKéMON.$",
    )),
    "SlateportCity_Text_EffortRibbonLooksGoodOnIt": (("RIBBON looks good",), (
        "AVALIADORA: A FITA DE ESFORCO\\n",
        "combina com seu {STR_VAR_1}!$",
    )),
    "SlateportCity_Text_WonderIfLighthouseStartlesPokemon": (("lighthouse", "startle POKéMON"), (
        "HOMEM: A luz do farol vai muito\\n",
        "longe pelo mar.\\p",
        "Sera que ela assusta os POKéMON\\n",
        "que nadam la fora?$",
    )),
    "SlateportCity_Text_SeaweedFullOfLife": (("seaweed", "full of life"), (
        "COZINHEIRO: Olhe esta alga!\\p",
        "A daqui chega fresca e cheia de\\n",
        "vida. Quase parece que vai\\n",
        "saltar da banca.$",
    )),
    "SlateportCity_Text_HowTownIsBornAndGrows": (("how a town is born",), (
        "SENHORA: Agua limpa traz pesca e\\n",
        "colheita.\\p",
        "Onde produtos e pessoas se\\n",
        "encontram, nasce um mercado.\\p",
        "Foi assim que a cidade cresceu.$",
    )),
    "SlateportCity_Text_SlateportWonderfulPlace": (("PORTO DO SAL", "wonderful place"), (
        "GAROTA: Comprar sentindo cheiro\\n",
        "do mar e bom demais.\\p",
        "PORTO DO SAL e um lugar unico.$",
    )),
    "SlateportCity_Text_BuyBricksSoDecorWontGetDirty": (("DOLLS", "CUSHIONS", "BRICKS"), (
        "GAROTA: BONECOS e ALMOFADAS no\\n",
        "chao acabam sujando.\\p",
        "Vou comprar blocos para deixar\\n",
        "minhas decoracoes elevadas.$",
    )),
    "SlateportCity_Text_GoingToCompeteInBattleTent": (("BATTLE TENT", "catch"), (
        "RAPAZ: Eu tambem vou competir na\\n",
        "TENDA DE BATALHA!\\p",
        "Antes disso, preciso montar uma\\n",
        "equipe melhor.$",
    )),
    "SlateportCity_Text_BushedHikingFromMauville": (("ENCRUZILHADA", "BIKE"), (
        "HOMEM: Ufa... estou acabado.\\p",
        "Vim caminhando desde o interior.\\p",
        "Se soubesse que a cidade era tao\\n",
        "grande, teria vindo de BIKE.$",
    )),
    "SlateportCity_Text_EveryoneCallsHimCaptStern": (("CAPT. STERN", "MUSEUM"), (
        "HOMEM: O ENGENHEIRO DO PORTO\\n",
        "ajudou a construir o MUSEU e\\n",
        "lidera expedicoes submarinas.$",
    )),
    "SlateportCity_Text_SeaIsSoWet": (("sea is just so vast", "tears"), (
        "MARINHEIRO: O mar e enorme...\\p",
        "Sera que caberiam nele todas as\\n",
        "lagrimas de POKéMON?$",
    )),
    "SlateportCity_Text_SinkOldBoats": (("old", "ships", "habitats"), (
        "MARINHEIRO: Navio velho demais\\n",
        "para navegar pode virar abrigo.\\p",
        "Afundado com cuidado, vira casa\\n",
        "para muitos POKéMON.$",
    )),
    "SlateportCity_Text_BuyTooMuch": (("buy too much",), (
        "MULHER: Sempre que venho ao\\n",
        "MERCADO, compro demais.$",
    )),
    "SlateportCity_Text_GetNameRaterToHelpYou": (("NAME", "RATER"), (
        "HOMEM: Quer mudar o apelido do\\n",
        "seu POKéMON?\\p",
        "Procure o AVALIADOR DE NOMES.$",
    )),
    "SlateportCity_Text_CantChangeTradeMonName": (("trade", "nickname", "TRAINER"), (
        "MULHER: POKéMON de troca mantem\\n",
        "o apelido original.\\p",
        "E uma lembranca do TREINADOR que\\n",
        "cuidou dele primeiro.$",
    )),
    "SlateportCity_Text_BattleTentBuiltRecently": (("BATTLE TENT", "PORTO DO SAL"), (
        "HOMEM: A TENDA DE BATALHA chegou\\n",
        "ha pouco tempo a PORTO DO SAL.\\p",
        "E diferente de um GINASIO, mas\\n",
        "tambem exige boa equipe.$",
    )),
    "SlateportCity_Text_CaptSternBeingInterviewed": (("CAPT. STERN", "interviewed"), (
        "SENHORA: Pensei que fosse algum\\n",
        "artista famoso.\\p",
        "Mas e o ENGENHEIRO DO PORTO!$",
    )),
    "SlateportCity_Text_InterviewerSoCool": (("interviewer", "journalist"), (
        "GAROTA: Essa reporter e legal.\\p",
        "Quando crescer, quero contar\\n",
        "historias pelo mundo inteiro.$",
    )),
    "SlateportCity_Text_SternSaysDiscoveredSomething": (("CAPT. STERN", "bottom of the sea"), (
        "RAPAZ: O ENGENHEIRO disse que\\n",
        "acharam algo no fundo do mar.\\p",
        "O que sera?$",
    )),
    "SlateportCity_Text_CaptainComeBackWithBigFish": (("CAPTAIN", "big fish"), (
        "COZINHEIRO: O que houve?\\p",
        "Sera que a expedicao voltou com\\n",
        "um peixe enorme?$",
    )),
    "SlateportCity_Text_AmIOnTV": (("Am I on TV",), (
        "HOMEM: Ei! Estou aparecendo na\\n",
        "TV?$",
    )),
    "SlateportCity_Text_CaptainsACelebrity": (("CAPTAIN", "celebrity"), (
        "HOMEM: Entrevista ao vivo aqui?\\p",
        "O ENGENHEIRO virou celebridade.$",
    )),
    "SlateportCity_Text_BigSmileForCamera": (("TITO:", "CAPT. STERN"), (
        "CAMERAMAN: ENGENHEIRO, sorria\\n",
        "para a camera!$",
    )),
    "SlateportCity_Text_MostInvaluableExperience": (("BIA:", "invaluable experience"), (
        "REPORTER: Entendo...\\p",
        "Foi uma experiencia importante.$",
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
        raise ValueError("non-dialogue structure changed while rendering Porto do Sal daily life")

    for token in ("ENERGY GURU", "EFFORT RIBBON", "MAUVILLE CITY", "CAPT. STERN", "BIA:", "TITO:"):
        for label in TARGETS:
            if token in block_pattern(label).search(rendered).group("body"):
                raise ValueError(f"{label}: stale daily-life token survived: {token}")
    return rendered


def main() -> int:
    parser = argparse.ArgumentParser(description="Render Porto do Sal everyday NPC and interview-bystander surface.")
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--in-place", action="store_true")
    args = parser.parse_args()
    if args.check and args.in_place:
        parser.error("use either --check or --in-place")

    rendered = render(TARGET.read_text(encoding="utf-8"))
    if args.check:
        print(f"Porto do Sal daily-life renderer OK: {len(TARGETS)} blocks validated.")
        return 0
    if args.in_place:
        TARGET.write_text(rendered, encoding="utf-8")
        return 0
    print(rendered, end="" if rendered.endswith("\n") else "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
