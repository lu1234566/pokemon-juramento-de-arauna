#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / "data" / "maps" / "PetalburgWoods" / "scripts.inc"

TARGETS: dict[str, tuple[str, ...]] = {
    "PetalburgWoods_Text_NotAOneToBeFound": (
        r"PESQUISADOR: Nada...\p",
        r"Os rastros terminam aqui.$",
    ),
    "PetalburgWoods_Text_HaveYouSeenShroomish": (
        r"PESQUISADOR: Voce viu algum POKéMON\n",
        r"agindo como se nao reconhecesse\n",
        r"esta parte da mata?\p",
        r"Estou registrando sinais de DESENCANTO.$",
    ),
    "PetalburgWoods_Text_IWasGoingToAmbushYou": (
        r"AGENTE HORIZONTE: Finalmente.\p",
        r"Voce demorou demais aqui.\n",
        r"Entregue os registros.$",
    ),
    "PetalburgWoods_Text_HandOverThosePapers": (
        r"AGENTE HORIZONTE: Voce.\p",
        r"Passe os cadernos e os dados\n",
        r"dos sensores. Agora.$",
    ),
    "PetalburgWoods_Text_YouHaveToHelpMe": (
        r"PESQUISADOR: Voce viaja com POKéMON.\p",
        r"Por favor, nao deixe ele levar\n",
        r"meus registros.$",
    ),
    "PetalburgWoods_Text_NoOneCrossesTeamAqua": (
        r"AGENTE HORIZONTE: Isso nao envolve voce.\p",
        r"O CONSORCIO recolhe dados sensiveis\n",
        r"quando eles podem causar panico.\p",
        r"Saia do caminho.$",
    ),
    "PetalburgWoods_Text_YoureKiddingMe": (
        r"AGENTE HORIZONTE: Droga...\n",
        r"Voce sabe lutar.$",
    ),
    "PetalburgWoods_Text_YouveGotSomeNerve": (
        r"AGENTE HORIZONTE: Nao pense que\n",
        r"isso termina aqui.\p",
        r"A SERRA DO UIVO tem material\n",
        r"mais importante do que estes papeis.\p",
        r"Hoje voce teve sorte.$",
    ),
    "PetalburgWoods_Text_ThatWasAwfullyClose": (
        r"PESQUISADOR: Essa foi por pouco.\p",
        r"Estes registros mostram POKéMON\n",
        r"esquecendo rotas familiares.\p",
        r"Nao quero que desaparecam num arquivo.\p",
        r"Pegue isto. E pouco, mas obrigado.$",
    ),
    "PetalburgWoods_Text_TeamAquaAfterSomethingInRustboro": (
        r"PESQUISADOR: Ele falou da\n",
        r"SERRA DO UIVO, nao falou?\p",
        r"O HORIZONTE mantem um centro\n",
        r"tecnico enorme por la.$",
    ),
    "PetalburgWoods_Text_ICantBeWastingTime": (
        r"PESQUISADOR: Preciso entregar\n",
        r"uma copia destes dados antes\n",
        r"que alguem tente apaga-los.$",
    ),
    "PetalburgWoods_Text_YoureLoadedWithItems": (
        r"PESQUISADOR: Sua BOLSA esta cheia.\p",
        r"Guarde algum item e fale comigo.$",
    ),
}

FORBIDDEN = (
    "DEVON",
    "TEAM AQUA",
    "PETALBURG WOODS",
    "RUSTBORO",
)


def marker_for(text: str, label: str) -> str:
    for suffix in ("::\n", ":\n"):
        marker = label + suffix
        if marker in text:
            return marker
    raise RuntimeError(f"Missing woods encounter block: {label}")


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


def validate(text: str) -> list[str]:
    failures: list[str] = []
    for label, lines in TARGETS.items():
        start, end, marker = bounds(text, label)
        block = text[start:end]
        if block != render(marker, lines):
            failures.append(f"{label} differs from canonical Arauna woods text")
        for token in FORBIDDEN:
            if token in block:
                failures.append(f"{label} still exposes Emerald token: {token}")
    return failures


def apply() -> int:
    text = TARGET.read_text(encoding="utf-8")
    changed = 0
    for label, lines in TARGETS.items():
        start, end, marker = bounds(text, label)
        replacement = render(marker, lines)
        if text[start:end] != replacement:
            text = text[:start] + replacement + text[end:]
            changed += 1
    failures = validate(text)
    if failures:
        raise RuntimeError("; ".join(failures))
    TARGET.write_text(text, encoding="utf-8")
    print(f"Woods Horizonte encounter cleanup: {changed} changed; {len(TARGETS)} verified.")
    return 0


def check() -> int:
    failures = validate(TARGET.read_text(encoding="utf-8"))
    if failures:
        print("Woods Horizonte encounter cleanup check FAILED:")
        for failure in failures:
            print(f"- {failure}")
        return 1
    print(f"Woods Horizonte encounter cleanup check PASS: {len(TARGETS)} blocks.")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    return check() if args.check else apply()


if __name__ == "__main__":
    raise SystemExit(main())
