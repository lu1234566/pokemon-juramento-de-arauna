#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

PLAYER_HOUSE = "data/maps/LittlerootTown_BrendansHouse_1F/scripts.inc"
RIVAL_HOUSE_1F = "data/maps/LittlerootTown_MaysHouse_1F/scripts.inc"
RIVAL_HOUSE_2F = "data/maps/LittlerootTown_MaysHouse_2F/scripts.inc"

CIRO_INTRO = (
    r"CIRO: Entao voce e {PLAYER}.\p",
    r"ANAHI falou que voce chegaria.\n",
    r"Eu esperava alguem... diferente.\p",
    r"Depois conversamos. Estou\n",
    r"atrasado para o campo.$",
)

CIRO_READY = (
    r"CIRO: Estou terminando minhas\n",
    r"anotacoes da ROTA 103.\p",
    r"O HORIZONTE quer dados antes\n",
    r"do anoitecer.$",
)

TARGETS = (
    (PLAYER_HOUSE, "PlayersHouse_1F_Text_IsntItNiceInHere", (
        r"MAE: Chegamos, {PLAYER}.\n",
        r"Ainda parece estranho, nao?$",
    )),
    (PLAYER_HOUSE, "PlayersHouse_1F_Text_MoversPokemonGoSetClock", (
        r"Os POKéMON da mudanca\n",
        r"deixaram tudo no lugar.\p",
        r"Seu quarto fica no andar\n",
        r"de cima. Va dar uma olhada.\p",
        r"ELIAS deixou um relogio para\n",
        r"voce antes de partir.\n",
        r"Nao esqueca de acerta-lo.$",
    )),
    (PLAYER_HOUSE, "PlayersHouse_1F_Text_ArentYouInterestedInRoom", (
        r"MAE: {PLAYER}, seu quarto\n",
        r"esta esperando por voce.$",
    )),
    (PLAYER_HOUSE, "PlayersHouse_1F_Text_GoSetTheClock", (
        r"MAE: Acerte o relogio do\n",
        r"seu quarto antes de sair.$",
    )),
    (PLAYER_HOUSE, "PlayersHouse_1F_Text_OhComeQuickly", (
        r"MAE: {PLAYER}! Venha aqui!\n",
        r"Estao falando de ELIAS na TV.$",
    )),
    (PLAYER_HOUSE, "PlayersHouse_1F_Text_MaybeDadWillBeOn", (
        r"MAE: Talvez mostrem ELIAS.\p",
        r"Ele quase nunca aparece nas\n",
        r"reportagens do PAMPA DA ESPERA.$",
    )),
    (PLAYER_HOUSE, "PlayersHouse_1F_Text_ItsOverWeMissedHim", (
        r"MAE: Ah... acabou.\p",
        r"Acho que ELIAS apareceu, mas\n",
        r"chegamos tarde demais.$",
    )),
    (PLAYER_HOUSE, "PlayersHouse_1F_Text_GoIntroduceYourselfNextDoor", (
        r"MAE: A PROFESSORA ANAHI trabalha\n",
        r"bem aqui perto.\p",
        r"Va se apresentar antes de\n",
        r"seguir pela vila.$",
    )),
    (PLAYER_HOUSE, "PlayersHouse_1F_Text_SeeYouHoney", (
        r"MAE: Ate mais, {PLAYER}.\n",
        r"Nao suma sem avisar.$",
    )),
    (PLAYER_HOUSE, "PlayersHouse_1F_Text_DidYouMeetProfBirch", (
        r"MAE: Encontrou a PROFESSORA\n",
        r"ANAHI?\p",
        r"Ela passa mais tempo no campo\n",
        r"do que no laboratorio.$",
    )),
    (PLAYER_HOUSE, "PlayersHouse_1F_Text_YouShouldRestABit", (
        r"MAE: Voce esta com cara de\n",
        r"quem precisa descansar.\p",
        r"Durma um pouco antes de\n",
        r"voltar para a estrada.$",
    )),
    (PLAYER_HOUSE, "PlayersHouse_1F_Text_TakeCareHoney", (
        r"MAE: Se cuide, {PLAYER}.$",
    )),
    (PLAYER_HOUSE, "PlayersHouse_1F_Text_GotDadsBadgeHeresSomethingFromMom", (
        r"MAE: ELIAS entregou essa\n",
        r"INSIGNIA a voce?\p",
        r"Entao leve isto tambem.\n",
        r"Desta vez, da sua mae.$",
    )),
    (PLAYER_HOUSE, "PlayersHouse_1F_Text_DontPushYourselfTooHard", (
        r"Nao precisa provar tudo de uma\n",
        r"vez, {PLAYER}.\p",
        r"Quando precisar, volte para\n",
        r"casa. Eu estarei aqui.$",
    )),
    (PLAYER_HOUSE, "PlayersHouse_1F_Text_IsThatAPokenav", (
        r"MAE: Isso e um POKéNAV?\p",
        r"Foi o HORIZONTE que ativou\n",
        r"esse sistema de contatos?\p",
        r"Entao registre meu numero.\n",
        r"Quero saber quando esta bem.$",
    )),
    (PLAYER_HOUSE, "PlayersHouse_1F_Text_RegisteredMom", (
        r"MAE foi registrada\n",
        r"no POKéNAV.$",
    )),
    (PLAYER_HOUSE, "PlayersHouse_1F_Text_ReportFromPetalburgGym", (
        r"REPORTER: Direto do\n",
        r"PAMPA DA ESPERA,\p",
        r"onde ELIAS recebeu novos\n",
        r"desafiantes esta manha.$",
    )),
    (RIVAL_HOUSE_1F, "RivalsHouse_1F_Text_OhYoureTheNewNeighbor", (
        r"Ah, voce deve ser {PLAYER}.\p",
        r"CIRO comentou que alguem da\n",
        r"idade dele viria morar perto.\p",
        r"Ele esta no andar de cima.\n",
        r"Se ainda nao saiu correndo.$",
    )),
    (RIVAL_HOUSE_1F, "RivalsHouse_1F_Text_LikeChildLikeFather", (
        r"CIRO quase nao para em casa.\p",
        r"Desde que o HORIZONTE ofereceu\n",
        r"aquela bolsa, ele vive entre\n",
        r"mapas, sensores e POKéMON.$",
    )),
    (RIVAL_HOUSE_1F, "RivalsHouse_1F_Text_TooBusyToNoticeVisit", (
        r"CIRO nem percebeu que voce\n",
        r"veio, nao e?\p",
        r"Quando coloca uma ideia na\n",
        r"cabeca, esquece o resto.$",
    )),
    (RIVAL_HOUSE_1F, "RivalsHouse_1F_Text_WentOutToRoute103", (
        r"CIRO saiu para a ROTA 103\n",
        r"ha pouco.\p",
        r"Disse que precisava testar\n",
        r"dados novos do HORIZONTE.$",
    )),
    (RIVAL_HOUSE_1F, "RivalsHouse_1F_Text_ShouldGoHomeEverySoOften", (
        r"Viajar com POKéMON muda a\n",
        r"gente.\p",
        r"Mas volte para casa de vez em\n",
        r"quando. Sua mae vai gostar.$",
    )),
    (RIVAL_HOUSE_1F, "RivalsHouse_1F_Text_MayWhoAreYou", CIRO_INTRO),
    (RIVAL_HOUSE_1F, "RivalsHouse_1F_Text_BrendanWhoAreYou", CIRO_INTRO),
    (RIVAL_HOUSE_1F, "RivalsHouse_1F_Text_DoYouHavePokemon", (
        r"Oi, {PLAYER}!\p",
        r"Voce ja viaja com seu proprio\n",
        r"POKéMON?$",
    )),
    (RIVAL_HOUSE_2F, "RivalsHouse_2F_Text_MayWhoAreYou", CIRO_INTRO),
    (RIVAL_HOUSE_2F, "RivalsHouse_2F_Text_BrendanWhoAreYou", CIRO_INTRO),
    (RIVAL_HOUSE_2F, "RivalsHouse_2F_Text_MayGettingReady", CIRO_READY),
    (RIVAL_HOUSE_2F, "RivalsHouse_2F_Text_BrendanGettingReady", CIRO_READY),
    (RIVAL_HOUSE_2F, "RivalsHouse_2F_Text_ItsRivalsPokeBall", (
        r"Essa POKé BOLA e de CIRO.\p",
        r"Melhor deixar onde esta.$",
    )),
)

FORBIDDEN = (
    "MOM:",
    "DAD",
    "DEVON",
    "PETALBURG",
    "PROF. BIRCH",
    "PROFESSOR BIRCH",
    "Like child, like father",
    "new next-door",
)


def block_pattern(label: str) -> re.Pattern[str]:
    return re.compile(rf"(?m)^{re.escape(label)}:\n(?:\t\.string \"[^\n]*\"\n)+")


def render(label: str, lines: tuple[str, ...]) -> str:
    return label + ":\n" + "".join(f'\t.string "{line}"\n' for line in lines)


def extract(text: str, label: str) -> str:
    match = block_pattern(label).search(text)
    if not match:
        raise RuntimeError(f"Missing text block: {label}")
    return match.group(0)


def validate(block: str, rel_path: str, label: str, lines: tuple[str, ...]) -> list[str]:
    failures: list[str] = []
    for line in lines:
        if f'\t.string "{line}"' not in block:
            failures.append(f"{rel_path}: {label} missing expected line: {line}")
    for token in FORBIDDEN:
        if token in block:
            failures.append(f"{rel_path}: {label} still contains legacy token: {token}")
    return failures


def apply() -> int:
    changed_files: set[Path] = set()
    for rel_path, label, lines in TARGETS:
        path = ROOT / rel_path
        text = path.read_text(encoding="utf-8")
        updated, count = block_pattern(label).subn(lambda _m: render(label, lines), text, count=1)
        if count != 1:
            raise RuntimeError(f"Could not uniquely replace {label} (matches={count})")
        if updated != text:
            path.write_text(updated, encoding="utf-8")
            changed_files.add(path)
        failures = validate(extract(updated, label), rel_path, label, lines)
        if failures:
            raise RuntimeError("; ".join(failures))
    print(
        f"Littleroot house cleanup: {len(changed_files)} file(s) changed; "
        f"{len(TARGETS)} block(s) verified."
    )
    return 0


def check() -> int:
    failures: list[str] = []
    for rel_path, label, lines in TARGETS:
        text = (ROOT / rel_path).read_text(encoding="utf-8")
        failures.extend(validate(extract(text, label), rel_path, label, lines))
    if failures:
        print("Littleroot house cleanup check FAILED:")
        for failure in failures:
            print(f"- {failure}")
        return 1
    print(f"Littleroot house cleanup check PASS: {len(TARGETS)} block(s).")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    return check() if args.check else apply()


if __name__ == "__main__":
    raise SystemExit(main())
