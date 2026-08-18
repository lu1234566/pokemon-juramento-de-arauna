#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

TARGETS: dict[str, dict[str, tuple[str, ...]]] = {
    "data/maps/Route102/scripts.inc": {
        "Route102_Text_WatchMeCatchPokemon": (
            r"VAL: {PLAYER}... fica aqui comigo?\p",
            r"Eu ainda travo quando preciso\n",
            r"agir sozinho.\p",
            r"Quero tentar capturar um POKéMON\n",
            r"sem que facam isso por mim.$",
        ),
        "Route102_Text_WallyIDidIt": (
            r"VAL: Eu consegui!\p",
            r"Ainda tremi, mas nao parei.\n",
            r"Acho que isso ja conta.$",
        ),
        "Route102_Text_LetsGoBack": (
            r"VAL: Obrigado, {PLAYER}.\n",
            r"Vamos voltar ao PAMPA DA ESPERA.$",
        ),
        "Route102_Text_RouteSignOldale": (
            r"ROTA 102\n",
            r"{RIGHT_ARROW} VILA DA PASSAGEM$",
        ),
        "Route102_Text_RouteSignPetalburg": (
            r"ROTA 102\n",
            r"{LEFT_ARROW} PAMPA DA ESPERA$",
        ),
    },
    "data/maps/PetalburgCity/scripts.inc": {
        "PetalburgCity_Text_WhereIsWally": (
            r"MAE DE VAL: VAL saiu com o pai.\p",
            r"Ele estava nervoso, mas queria\n",
            r"tentar por conta propria.$",
        ),
        "PetalburgCity_Text_WallyHouseSign": (
            r"CASA DA FAMILIA DE VAL$",
        ),
        "PetalburgCity_Text_ThisIsPetalburgGym": (
            r"Aqui fica o posto de ELIAS,\n",
            r"responsavel pelo PAMPA DA ESPERA.$",
        ),
    },
    "data/maps/MauvilleCity/scripts.inc": {
        "MauvilleCity_Text_UncleHesTooPeppy": (
            r"TIO: VAL ganhou folego desde que\n",
            r"comecou a viajar com POKéMON.\p",
            r"Agora preciso lembra-lo de nao\n",
            r"se cobrar tanto.$",
        ),
        "MauvilleCity_Text_WallyWantToChallengeGym": (
            r"VAL: Tio, eu quero desafiar OLIVIA.\p",
            r"Quero saber ate onde consigo ir.$",
        ),
        "MauvilleCity_Text_UncleYourePushingIt": (
            r"TIO: Calma, VAL.\p",
            r"Voce cresceu muito, mas nao precisa\n",
            r"provar tudo de uma vez.$",
        ),
        "MauvilleCity_Text_WallyWeCanBeatAnyone": (
            r"VAL: Eu sei.\p",
            r"Mas se eu esperar o medo passar,\n",
            r"nunca vou descobrir o que consigo.$",
        ),
        "MauvilleCity_Text_WallyWillYouBattleMe": (
            r"VAL: {PLAYER}, luta comigo?\p",
            r"Quero testar o que aprendi sem\n",
            r"fingir que nao estou nervoso.$",
        ),
        "MauvilleCity_Text_WallyMyUncleWontKnowImStrong": (
            r"VAL: Se eu recuar agora, meu tio\n",
            r"vai achar que ainda nao estou pronto.\p",
            r"Por favor, luta comigo.$",
        ),
        "MauvilleCity_Text_WallyPleaseBattleMe": (
            r"VAL: {PLAYER}, por favor.\n",
            r"So uma batalha.$",
        ),
        "MauvilleCity_Text_WallyHereICome": (
            r"VAL: Certo... eu consigo.\n",
            r"Vamos!$",
        ),
        "MauvilleCity_Text_WallyDefeat": (
            r"VAL: Perdi... mas consegui\n",
            r"ficar ate o fim.$",
        ),
        "MauvilleCity_Text_WallyIllGoBackToVerdanturf": (
            r"VAL: Vou voltar ao VALE DO SILENCIO\n",
            r"por um tempo.\p",
            r"Ainda tenho muito para aprender.$",
        ),
        "MauvilleCity_Text_ThankYouNotEnoughToBattle": (
            r"VAL: Obrigado, {PLAYER}.\p",
            r"Ter POKéMON nao basta. Eu preciso\n",
            r"aprender a decidir por mim tambem.$",
        ),
        "MauvilleCity_Text_UncleNoNeedToBeDown": (
            r"TIO: VAL, nao abaixe a cabeca.\p",
            r"Voce terminou a batalha. Isso ja e\n",
            r"mais do que conseguia antes.\p",
            r"Vamos para casa.$",
        ),
        "MauvilleCity_Text_UncleCanYouBattleWally": (
            r"TIO: {PLAYER}, pode batalhar com VAL?\p",
            r"Ele precisa descobrir o proprio limite\n",
            r"sem que eu escolha por ele.$",
        ),
        "MauvilleCity_Text_UncleVisitUsSometime": (
            r"TIO: {PLAYER}, agora entendi.\p",
            r"Voce foi quem ajudou VAL a capturar\n",
            r"o primeiro POKéMON.\p",
            r"Visite-nos no VALE DO SILENCIO.$",
        ),
        "MauvilleCity_Text_WallyPokenavCall": (
            r"VAL: {PLAYER}? Sou eu.\p",
            r"Ainda fico nervoso antes de sair,\n",
            r"mas agora saio mesmo assim.\p",
            r"Quando estiver pronto, quero\n",
            r"batalhar de novo.$",
        ),
        "MauvilleCity_Text_RegisteredWally": (
            r"VAL foi registrado\n",
            r"no POKéNAV.$",
        ),
        "MauvilleCity_Text_ScottYouDidntHoldBack": (
            r"VIAJANTE: Eu vi a batalha.\p",
            r"Voce nao facilitou para VAL.\n",
            r"Acho que era disso que ele precisava.\p",
            r"Vou lembrar de voce.$",
        ),
    },
    "data/maps/VerdanturfTown_WandasHouse/scripts.inc": {
        "VerdanturfTown_WandasHouse_Text_StrongerSpeech": (
            r"VAL: Aqui eu consigo respirar melhor.\p",
            r"Ainda tenho medo de sair sozinho,\n",
            r"mas nao quero que ele escolha por mim.$",
        ),
        "VerdanturfTown_WandasHouse_Text_StrongerSpeechShort": (
            r"VAL: Ainda tenho medo.\p",
            r"Agora sei que posso caminhar\n",
            r"mesmo lembrando dele.$",
        ),
        "VerdanturfTown_WandasHouse_Text_WallysNextDoor": (
            r"TIO: VAL esta no quarto ao lado.\p",
            r"Desde que chegou ao VALE DO SILENCIO,\n",
            r"fala muito mais de viajar.$",
        ),
        "VerdanturfTown_WandasHouse_Text_WallySlippedOff": (
            r"TIO: VAL saiu sem avisar.\p",
            r"Eu estou preocupado, claro.\n",
            r"Mas ele precisava escolher quando partir.$",
        ),
        "VerdanturfTown_WandasHouse_Text_WallyGoneThatFar": (
            r"TIO: Entao VAL chegou a\n",
            r"ESTRADA DO JURAMENTO...\p",
            r"Nunca pensei que iria tao longe\n",
            r"por vontade propria.$",
        ),
        "VerdanturfTown_WandasHouse_Text_MeetWanda": (
            r"WANDA: Voce e {PLAYER}?\p",
            r"VAL falou de voce. Sou prima dele.\p",
            r"Desde que veio ao VALE DO SILENCIO,\n",
            r"ele parece mais leve.$",
        ),
        "VerdanturfTown_WandasHouse_Text_DontWorryAboutWally": (
            r"WANDA: Nao se preocupe tanto com VAL.\p",
            r"Ele ainda tem medo, mas agora\n",
            r"sabe quando pedir ajuda.$",
        ),
        "VerdanturfTown_WandasHouse_Text_IfAnythingHappenedToWally": (
            r"TIA: VAL saiu de novo.\p",
            r"Se algo acontecer, espero que lembre\n",
            r"que sempre pode voltar.$",
        ),
        "VerdanturfTown_WandasHouse_Text_WallyWasInEverGrande": (
            r"TIA: Disseram que VAL chegou a\n",
            r"ESTRADA DO JURAMENTO.\p",
            r"Ele foi muito mais longe do que\n",
            r"imaginavamos.$",
        ),
    },
    "data/maps/VictoryRoad_1F/scripts.inc": {
        "VictoryRoad_1F_Text_WallyNotGoingToLoseAnymore": (
            r"VAL: {PLAYER}... eu sabia que\n",
            r"encontraria voce aqui.\p",
            r"Antes eu queria provar que nao era fraco.\n",
            r"Agora quero descobrir meu caminho.\p",
            r"Batalha comigo.$",
        ),
        "VictoryRoad_1F_Text_WallyEntranceDefeat": (
            r"VAL: Ainda nao foi desta vez...\p",
            r"Mas eu nao quero fugir da derrota.$",
        ),
        "VictoryRoad_1F_Text_WallyPostEntranceBattle": (
            r"VAL: Vou continuar.\p",
            r"A ESTRADA DO JURAMENTO nao precisa\n",
            r"ser vencida de uma vez.$",
        ),
        "VictoryRoad_1F_Text_WallyIntro": (
            r"VAL: {PLAYER}, agora sei que\n",
            r"consigo chegar ate aqui.\p",
            r"Nao quero copiar seu caminho.\n",
            r"Quero testar o meu.$",
        ),
        "VictoryRoad_1F_Text_WallyDefeat": (
            r"VAL: Voce ainda esta a frente.\n",
            r"Tudo bem.$",
        ),
        "VictoryRoad_1F_Text_WallyPostBattle": (
            r"VAL: Vou continuar no meu ritmo.\p",
            r"Quando nos encontrarmos de novo,\n",
            r"quero que veja ate onde fui.$",
        ),
    },
    "data/text/match_call.inc": {
        "MatchCall_Text_Wally1": (
            r"VAL: Oi, {PLAYER}.\p",
            r"Estou com mais folego e saindo\n",
            r"de casa com mais frequencia.\p",
            r"Ainda quero batalhar como voce,\n",
            r"mas no meu tempo.$",
        ),
        "MatchCall_Text_Wally2": (
            r"VAL: {PLAYER}, as GALERIAS DA SERRA\n",
            r"foram abertas.\p",
            r"A WANDA ficou muito feliz.\n",
            r"Da para ouvir pela voz dela.$",
        ),
        "MatchCall_Text_Wally3": (
            r"VAL: Eu sai do VALE DO SILENCIO\n",
            r"sem avisar direito.\p",
            r"Meu tio deve estar preocupado.\n",
            r"Mas eu precisava escolher sozinho.$",
        ),
        "MatchCall_Text_Wally4": (
            r"VAL: {PLAYER}? Sou eu.\p",
            r"Viajar com meu POKéMON mudou tudo.\n",
            r"Eu encontro gente nova em cada parada.\p",
            r"Ainda assusta. Tambem anima.$",
        ),
        "MatchCall_Text_Wally5": (
            r"VAL: {PLAYER}, lembra do POKéMON\n",
            r"que capturei com voce?\p",
            r"Ele evoluiu!\p",
            r"Eu quase disse que foi talento meu,\n",
            r"mas ele fez a maior parte do trabalho.$",
        ),
        "MatchCall_Text_Wally6": (
            r"VAL parece estar fora da area\n",
            r"de sinal do POKéNAV...$",
        ),
        "MatchCall_Text_Wally7": (
            r"VAL: Antes de conhecer voce,\n",
            r"eu quase nao saia de casa.\p",
            r"Agora estou na estrada com meu POKéMON.\p",
            r"Ainda tenho medo. A diferenca e\n",
            r"que ele nao decide mais por mim.$",
        ),
    },
}

FORBIDDEN = (
    "WALLY",
    "OLDALE",
    "PETALBURG",
    "MAUVILLE",
    "VERDANTURF",
    "VICTORY ROAD",
    "EVER GRANDE",
    "RUSTURF TUNNEL",
    "SCOTT:",
)


def marker_for(text: str, label: str) -> str:
    double = label + "::\n"
    single = label + ":\n"
    if double in text:
        return double
    if single in text:
        return single
    raise RuntimeError(f"Missing Val arc text block: {label}")


def block_bounds(text: str, label: str) -> tuple[int, int, str]:
    marker = marker_for(text, label)
    start = text.find(marker)
    end = text.find("\n\n", start)
    if end < 0:
        end = len(text)
    else:
        end += 1
    return start, end, marker


def render(marker: str, lines: tuple[str, ...]) -> str:
    return marker + "".join(f'\t.string "{line}"\n' for line in lines)


def validate_file(text: str, targets: dict[str, tuple[str, ...]]) -> list[str]:
    failures: list[str] = []
    for label, lines in targets.items():
        start, end, marker = block_bounds(text, label)
        block = text[start:end]
        expected = render(marker, lines)
        if block != expected:
            failures.append(f"{label} does not match the canonical generated block")
        for token in FORBIDDEN:
            if token in block:
                failures.append(f"{label} still contains visible Emerald token: {token}")
    return failures


def apply() -> int:
    total_changed = 0
    total_verified = 0
    for relpath, targets in TARGETS.items():
        path = ROOT / relpath
        text = path.read_text(encoding="utf-8")
        changed = 0
        for label, lines in targets.items():
            start, end, marker = block_bounds(text, label)
            replacement = render(marker, lines)
            if text[start:end] != replacement:
                text = text[:start] + replacement + text[end:]
                changed += 1
        failures = validate_file(text, targets)
        if failures:
            raise RuntimeError("; ".join(failures))
        path.write_text(text, encoding="utf-8")
        total_changed += changed
        total_verified += len(targets)
        print(f"{relpath}: {changed} changed; {len(targets)} verified.")
    print(f"Val arc cleanup: {total_changed} changed; {total_verified} verified.")
    return 0


def check() -> int:
    failures: list[str] = []
    total = 0
    for relpath, targets in TARGETS.items():
        path = ROOT / relpath
        failures.extend(f"{relpath}: {failure}" for failure in validate_file(path.read_text(encoding="utf-8"), targets))
        total += len(targets)
    if failures:
        print("Val arc cleanup check FAILED:")
        for failure in failures:
            print(f"- {failure}")
        return 1
    print(f"Val arc cleanup check PASS: {total} visible text blocks.")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    return check() if args.check else apply()


if __name__ == "__main__":
    raise SystemExit(main())
