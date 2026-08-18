#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MAP_FILE = "data/maps/LittlerootTown/scripts.inc"

TARGETS = (
    ("LittlerootTown_Text_OurNewHomeLetsGoInside", (
        r"MAE: {PLAYER}, chegamos.\p", r"Esta e a VILA AMANHECER.\n",
        r"Nossa nova casa fica logo ali.\p", r"Vai levar um tempo para tudo\n",
        r"parecer nosso de verdade.\p", r"Venha. Quero que veja seu quarto.$",
    )),
    ("LittlerootTown_Text_WaitPlayer", (r"MAE: Espere, {PLAYER}!$",)),
    ("LittlerootTown_Text_WearTheseRunningShoes", (
        r"MAE: {PLAYER}! Encontrou ANAHI?\p", r"E esse POKéMON... entao voces\n",
        r"decidiram viajar juntos.\p", r"ELIAS vai querer saber disso.\p",
        r"Se vai seguir pela estrada,\n", r"leve estes TENIS DE CORRIDA.$",
    )),
    ("LittlerootTown_Text_SwitchShoesWithRunningShoes", (r"{PLAYER} calcou os\n", r"TENIS DE CORRIDA.$")),
    ("LittlerootTown_Text_ExplainRunningShoes", (
        r"MAE: Segure o Botao B para\n", r"correr quando estiver usando\l", r"os TENIS DE CORRIDA.$",
    )),
    ("LittlerootTown_Text_ComeHomeIfAnythingHappens", (
        r"MAE: Agora voce tem seu proprio\n", r"companheiro de viagem.\p",
        r"Nao tente carregar tudo sozinho.\n", r"Se precisar, volte para casa.\p", r"E mande noticias, {PLAYER}.$",
    )),
    ("LittlerootTown_Text_CanUsePCToStoreItems", (
        r"Os PCs guardam itens e dados\n", r"de POKéMON.\p", r"Ainda acho estranho confiar\n", r"tanta coisa a uma tela.$",
    )),
    ("LittlerootTown_Text_BirchSpendsDaysInLab", (
        r"A PROFESSORA ANAHI vive no campo.\p", r"Quando o laboratorio esta vazio,\n",
        r"ela deve estar seguindo alguma\l", r"pista pela mata.$",
    )),
    ("LittlerootTown_Text_IfYouGoInGrassPokemonWillJumpOut", (
        r"Ei! Nao siga pela mata sozinho.\p", r"POKéMON selvagens aparecem no\n", r"capim alto.$",
    )),
    ("LittlerootTown_Text_DangerousIfYouDontHavePokemon", (r"Sem um POKéMON ao seu lado,\n", r"e perigoso seguir por ali.$")),
    ("LittlerootTown_Text_CanYouGoSeeWhatsHappening", (
        r"Tem alguma coisa acontecendo\n", r"mais adiante!\p", r"Ouvi a PROFESSORA ANAHI e um\n",
        r"POKéMON no meio da mata.\p", r"Pode ir ver se ela esta bem?$",
    )),
    ("LittlerootTown_Text_YouSavedBirch", (
        r"Voce ajudou a PROFESSORA ANAHI!\p", r"Eu ouvi a confusao daqui.\n", r"Ainda bem que os dois voltaram.$",
    )),
    ("LittlerootTown_Text_GoodLuckCatchingPokemon", (r"Vai seguir viagem com POKéMON?\n", r"Boa sorte, {PLAYER}!$")),
    ("LittlerootTown_Text_ProfBirchsLab", (r"LABORATORIO DE CAMPO\n", r"PROFESSORA ANAHI.$")),
    ("LittlerootTown_Text_PlayersHouse", (r"CASA DE {PLAYER}$",)),
    ("LittlerootTown_Text_ProfBirchsHouse", (r"CASA DE CIRO$",)),
    ("LittlerootTown_Text_BirchSomethingToShowYouAtLab", (
        r"ANAHI: {PLAYER}, venha comigo.\p", r"Encontrei algo nos registros\n", r"que quero mostrar no laboratorio.$",
    )),
)

FORBIDDEN = ("MOM:", "LITTLEROOT TOWN", "PROF. BIRCH", "PROFESSOR BIRCH", "Your father", "your father")


def pattern(label: str) -> re.Pattern[str]:
    return re.compile(rf"(?m)^{re.escape(label)}:\n(?:\t\.string \"[^\n]*\"\n)+")


def render(label: str, lines: tuple[str, ...]) -> str:
    return label + ":\n" + "".join(f'\t.string "{line}"\n' for line in lines)


def extract(text: str, label: str) -> str:
    match = pattern(label).search(text)
    if not match:
        raise RuntimeError(f"Missing text block: {label}")
    return match.group(0)


def validate(block: str, label: str, lines: tuple[str, ...]) -> list[str]:
    failures: list[str] = []
    for line in lines:
        if f'\t.string "{line}"' not in block:
            failures.append(f"{label} missing expected line: {line}")
    for token in FORBIDDEN:
        if token in block:
            failures.append(f"{label} still contains legacy token: {token}")
    return failures


def apply() -> int:
    path = ROOT / MAP_FILE
    text = path.read_text(encoding="utf-8")
    changed = 0
    for label, lines in TARGETS:
        updated, count = pattern(label).subn(lambda _m: render(label, lines), text, count=1)
        if count != 1:
            raise RuntimeError(f"Could not uniquely replace {label} (matches={count})")
        if updated != text:
            changed += 1
        text = updated
        failures = validate(extract(text, label), label, lines)
        if failures:
            raise RuntimeError("; ".join(failures))
    path.write_text(text, encoding="utf-8")
    print(f"Vila Amanhecer cleanup: {changed} block(s) changed; {len(TARGETS)} verified.")
    return 0


def check() -> int:
    text = (ROOT / MAP_FILE).read_text(encoding="utf-8")
    failures: list[str] = []
    for label, lines in TARGETS:
        failures.extend(validate(extract(text, label), label, lines))
    if failures:
        print("Vila Amanhecer cleanup check FAILED:")
        for failure in failures:
            print(f"- {failure}")
        return 1
    print(f"Vila Amanhecer cleanup check PASS: {len(TARGETS)} block(s).")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    return check() if args.check else apply()


if __name__ == "__main__":
    raise SystemExit(main())
