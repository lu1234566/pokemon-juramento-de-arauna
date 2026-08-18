#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

TARGETS: dict[str, dict[str, tuple[str, ...]]] = {
    "data/maps/Route104_MrBrineysHouse/scripts.inc": {
        "Route104_MrBrineysHouse_Text_WaitUpPeeko": (
            r"BARQUEIRO: Ei, companheira!\n",
            r"Devagar ai!$",
        ),
        "Route104_MrBrineysHouse_Text_ItsYouLetsSailToDewford": (
            r"BARQUEIRO: {PLAYER}! E voce.\p",
            r"Foi voce quem salvou minha\n",
            r"companheira la nas galerias.\p",
            r"Precisa atravessar o mar?\p",
            r"Uma CARTA vai para o PORTO DAS REDES\n",
            r"e o pacote segue ao PORTO DO SAL.\p",
            r"Posso levar voce.\n",
            r"Primeiro, PORTO DAS REDES.$",
        ),
        "Route104_MrBrineysHouse_Text_SetSailForDewford": (
            r"BARQUEIRO: PORTO DAS REDES, entao.\p",
            r"Vamos aproveitar a mare.$",
        ),
        "Route104_MrBrineysHouse_Text_DeclineDeliverySail": (
            r"BARQUEIRO: Tudo bem.\p",
            r"Quando quiser partir, fale comigo.$",
        ),
        "Route104_MrBrineysHouse_Text_NeedToMakeDeliveriesSailToDewford": (
            r"BARQUEIRO: Ainda esta com a CARTA\n",
            r"e o pacote do HORIZONTE, certo?\p",
            r"Vamos primeiro ao PORTO DAS REDES.\n",
            r"Depois seguimos ao PORTO DO SAL.$",
        ),
        "Route104_MrBrineysHouse_Text_NeedToDeliverPackageSailToDewford": (
            r"BARQUEIRO: O pacote ainda precisa\n",
            r"chegar ao PORTO DO SAL.\p",
            r"Posso deixar voce no PORTO DAS REDES\n",
            r"e seguir pela costa.$",
        ),
        "Route104_MrBrineysHouse_Text_WhereAreWeBound": (
            r"BARQUEIRO: Quer cruzar o mar?\p",
            r"Diga para onde vamos.$",
        ),
        "Route104_MrBrineysHouse_Text_TellMeWheneverYouWantToSail": (
            r"BARQUEIRO: Sem pressa.\p",
            r"Quando precisar navegar,\n",
            r"estarei por aqui.$",
        ),
        "Route104_MrBrineysHouse_Text_Peeko": (
            r"POKéMON: Pii piihyoro!$",
        ),
    },
    "data/maps/DewfordTown/scripts.inc": {
        "DewfordTown_Text_WhereAreWeBound": (
            r"BARQUEIRO: Pronto para partir?\p",
            r"Escolha o destino.$",
        ),
        "DewfordTown_Text_PetalburgWereSettingSail": (
            r"BARQUEIRO: PAMPA DA ESPERA.\n",
            r"Vamos pegar a corrente oeste.$",
        ),
        "DewfordTown_Text_SlateportWereSettingSail": (
            r"BARQUEIRO: PORTO DO SAL.\n",
            r"A mare esta boa para a travessia.$",
        ),
        "DewfordTown_Text_JustTellMeWhenYouNeedToSetSail": (
            r"BARQUEIRO: Tudo bem.\p",
            r"Fale comigo quando quiser partir.$",
        ),
        "DewfordTown_Text_SetSailBackToPetalburg": (
            r"BARQUEIRO: Quer voltar ao\n",
            r"PAMPA DA ESPERA?$",
        ),
        "DewfordTown_Text_GoDeliverIllBeWaiting": (
            r"BARQUEIRO: Entregue a CARTA.\p",
            r"Eu espero voce aqui no cais.$",
        ),
        "DewfordTown_Text_PetalburgWereSettingSail2": (
            r"BARQUEIRO: PAMPA DA ESPERA, entao.\n",
            r"Vamos.$",
        ),
        "DewfordTown_Text_BrineyLandedInDewford": (
            r"BARQUEIRO: Chegamos ao\n",
            r"PORTO DAS REDES.\p",
            r"Quando quiser navegar de novo,\n",
            r"fale comigo.$",
        ),
        "DewfordTown_Text_BrineyLandedInSlateportDeliverGoods": (
            r"BARQUEIRO: Chegamos ao PORTO DO SAL.\p",
            r"O pacote do HORIZONTE deve seguir\n",
            r"para a equipe de embarque.$",
        ),
        "DewfordTown_Text_BrineyLandedInSlateport": (
            r"BARQUEIRO: PORTO DO SAL.\p",
            r"Daqui voce segue por terra.$",
        ),
    },
    "data/maps/Route109/scripts.inc": {
        "Route109_Text_BrineySailToDewfordQuestion": (
            r"BARQUEIRO: O pacote do HORIZONTE\n",
            r"ainda precisa ser entregue.\p",
            r"Quer voltar ao PORTO DAS REDES?$",
        ),
        "Route109_Text_BrineyWhereAreWeBound": (
            r"BARQUEIRO: Quer navegar de novo?\p",
            r"Escolha o destino.$",
        ),
        "Route109_Text_BrineyDewfordItIs": (
            r"BARQUEIRO: PORTO DAS REDES.\n",
            r"Vamos aproveitar a mare.$",
        ),
        "Route109_Text_BrineyDeliverDevonGoods": (
            r"BARQUEIRO: Antes de seguir viagem,\n",
            r"entregue o pacote do HORIZONTE.\p",
            r"Eu espero aqui.$",
        ),
        "Route109_Text_BrineyTellMeWhenYouNeedToSail": (
            r"BARQUEIRO: Certo.\p",
            r"Fale comigo quando quiser partir.$",
        ),
    },
}

FORBIDDEN = (
    "MR. BRINEY",
    "PEEKO",
    "DEWFORD",
    "SLATEPORT",
    "PETALBURG",
    "DEVON",
    "CAPT. STERN",
)


def marker_for(text: str, label: str) -> str:
    for suffix in ("::\n", ":\n"):
        marker = label + suffix
        if marker in text:
            return marker
    raise RuntimeError(f"Missing transport surface block: {label}")


def bounds(text: str, label: str) -> tuple[int, int, str]:
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
        start, end, marker = bounds(text, label)
        block = text[start:end]
        if block != render(marker, lines):
            failures.append(f"{label} differs from canonical Arauna transport text")
        for token in FORBIDDEN:
            if token in block:
                failures.append(f"{label} still exposes Emerald transport token: {token}")
    return failures


def apply() -> int:
    changed_total = 0
    verified_total = 0
    for relpath, targets in TARGETS.items():
        path = ROOT / relpath
        text = path.read_text(encoding="utf-8")
        changed = 0
        for label, lines in targets.items():
            start, end, marker = bounds(text, label)
            replacement = render(marker, lines)
            if text[start:end] != replacement:
                text = text[:start] + replacement + text[end:]
                changed += 1
        failures = validate_file(text, targets)
        if failures:
            raise RuntimeError("; ".join(failures))
        path.write_text(text, encoding="utf-8")
        changed_total += changed
        verified_total += len(targets)
        print(f"{relpath}: {changed} changed; {len(targets)} verified.")
    print(f"Arauna transport cleanup: {changed_total} changed; {verified_total} verified.")
    return 0


def check() -> int:
    failures: list[str] = []
    total = 0
    for relpath, targets in TARGETS.items():
        path = ROOT / relpath
        failures.extend(
            f"{relpath}: {failure}"
            for failure in validate_file(path.read_text(encoding="utf-8"), targets)
        )
        total += len(targets)
    if failures:
        print("Arauna transport cleanup check FAILED:")
        for failure in failures:
            print(f"- {failure}")
        return 1
    print(f"Arauna transport cleanup check PASS: {total} visible blocks.")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    return check() if args.check else apply()


if __name__ == "__main__":
    raise SystemExit(main())
