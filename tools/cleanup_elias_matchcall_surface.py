#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MATCH_CALL = ROOT / "data" / "text" / "match_call.inc"
ROUTE105 = ROOT / "data" / "maps" / "Route105" / "scripts.inc"
STRINGS = ROOT / "src" / "strings.c"

CALLS: dict[str, tuple[str, ...]] = {
    "MatchCall_Text_Norman1": (
        r"ELIAS: {PLAYER}, na SERRA DO UIVO\n",
        r"ha gente que conhece atalhos antigos.\p",
        r"Se precisar abrir caminho, procure\n",
        r"quem trabalha com as trilhas locais.$",
    ),
    "MatchCall_Text_Norman2": (
        r"ELIAS: Voce esta ficando mais forte.\p",
        r"Parte de mim se orgulha. Outra parte\n",
        r"percebe o quanto voce ja nao precisa\n",
        r"que eu escolha o caminho por voce.$",
    ),
    "MatchCall_Text_Norman3": (
        r"ELIAS: Quatro INSIGNIAS...\p",
        r"Entao chegou a hora de cumprir\n",
        r"o que prometi.\p",
        r"Volte ao PAMPA DA ESPERA.\n",
        r"Eu vou enfrentar voce.$",
    ),
    "MatchCall_Text_Norman4": (
        r"ELIAS: Passe em casa de vez em quando.\p",
        r"Sua mae tenta nao demonstrar,\n",
        r"mas acompanha cada noticia sua.\p",
        r"Eu continuarei treinando aqui.$",
    ),
    "MatchCall_Text_Norman5": (
        r"ELIAS: Um EMBLEMA dos LEMBRANTES?\p",
        r"Se veio da SERRA DA CINZA,\n",
        r"nao trate isso como lembranca qualquer.\p",
        r"LUZIA raramente deixa simbolos ao acaso.$",
    ),
    "MatchCall_Text_Norman_Preparing": (
        r"ELIAS: {PLAYER}?\p",
        r"Voce me pegou treinando.\p",
        r"Nao quero que nossa proxima batalha\n",
        r"seja decidida pelo meu passado.$",
    ),
    "MatchCall_Text_Norman_PreparingPostGame": (
        r"ELIAS: Campeao de ARAUNA...\p",
        r"Eu ainda estou me acostumando\n",
        r"a dizer isso sobre meu proprio filho.\p",
        r"Nao significa que vou parar de treinar.$",
    ),
    "MatchCall_Text_Norman_RematchReady": (
        r"ELIAS: {PLAYER}, boa hora.\p",
        r"Quero outra batalha.\p",
        r"Estou esperando no posto do\n",
        r"PAMPA DA ESPERA.$",
    ),
    "MatchCall_Text_Norman_PostRematch": (
        r"ELIAS: Voce continua me surpreendendo.\p",
        r"Desta vez, quero aprender com isso\n",
        r"em vez de tentar controlar o resultado.$",
    ),
}

ROUTE_CALLS: dict[str, tuple[str, ...]] = {
    "Route104_Text_DadPokenavCall": (
        r"... ... ... Beep!\p",
        r"ELIAS: {PLAYER}? Sou eu.\p",
        r"O HORIZONTE avisou que seu POKéNAV\n",
        r"entrou na rede de contatos.\p",
        r"Parece que voce esta bem.\n",
        r"Nao vou prender voce no telefone.\p",
        r"Se cuide.$",
    ),
    "Route104_Text_RegisteredDadInPokenav": (
        r"ELIAS foi registrado\n",
        r"no POKéNAV.$",
    ),
}

EXACT = {
    'const u8 gText_NormanMatchCallDesc[] = _("RELIABLE ONE");': 'const u8 gText_NormanMatchCallDesc[] = _("PAI DE {PLAYER}");',
    'const u8 gText_NormanMatchCallName[] = _("DAD");': 'const u8 gText_NormanMatchCallName[] = _("ELIAS");',
}

FORBIDDEN = (
    "DAD:",
    "NORMAN",
    "RUSTBORO",
    "PETALBURG",
    "MAGMA",
    "DEVON",
    "MR. STONE",
)


def marker_for(text: str, label: str) -> str:
    for suffix in ("::\n", ":\n"):
        marker = label + suffix
        if marker in text:
            return marker
    raise RuntimeError(f"Missing Elias text block: {label}")


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


def validate_blocks(text: str, targets: dict[str, tuple[str, ...]]) -> list[str]:
    failures: list[str] = []
    for label, lines in targets.items():
        start, end, marker = bounds(text, label)
        block = text[start:end]
        if block != render(marker, lines):
            failures.append(f"{label} differs from canonical Elias text")
        for token in FORBIDDEN:
            if token in block:
                failures.append(f"{label} still exposes legacy token: {token}")
    return failures


def validate_exact(text: str) -> list[str]:
    failures: list[str] = []
    for old, new in EXACT.items():
        if new not in text:
            failures.append(f"missing Elias PokéNav constant: {new}")
        if old in text:
            failures.append(f"legacy Norman PokéNav constant remains: {old}")
    return failures


def replace_blocks(path: Path, targets: dict[str, tuple[str, ...]]) -> int:
    text = path.read_text(encoding="utf-8")
    changed = 0
    for label, lines in targets.items():
        start, end, marker = bounds(text, label)
        replacement = render(marker, lines)
        if text[start:end] != replacement:
            text = text[:start] + replacement + text[end:]
            changed += 1
    failures = validate_blocks(text, targets)
    if failures:
        raise RuntimeError("; ".join(failures))
    path.write_text(text, encoding="utf-8")
    return changed


def apply() -> int:
    call_changed = replace_blocks(MATCH_CALL, CALLS)
    route_changed = replace_blocks(ROUTE105, ROUTE_CALLS)

    text = STRINGS.read_text(encoding="utf-8")
    exact_changed = 0
    for old, new in EXACT.items():
        if new in text and old not in text:
            continue
        count = text.count(old)
        if count != 1:
            raise RuntimeError(f"Expected exactly one {old!r}, found {count}")
        text = text.replace(old, new, 1)
        exact_changed += 1
    failures = validate_exact(text)
    if failures:
        raise RuntimeError("; ".join(failures))
    STRINGS.write_text(text, encoding="utf-8")

    print(
        f"Elias cleanup: {call_changed} Match Calls, {route_changed} route blocks, "
        f"{exact_changed} PokéNav constants changed."
    )
    return 0


def check() -> int:
    failures = validate_blocks(MATCH_CALL.read_text(encoding="utf-8"), CALLS)
    failures.extend(validate_blocks(ROUTE105.read_text(encoding="utf-8"), ROUTE_CALLS))
    failures.extend(validate_exact(STRINGS.read_text(encoding="utf-8")))
    if failures:
        print("Elias cleanup check FAILED:")
        for failure in failures:
            print(f"- {failure}")
        return 1
    print(
        f"Elias cleanup check PASS: {len(CALLS)} Match Calls, "
        f"{len(ROUTE_CALLS)} route blocks and {len(EXACT)} constants."
    )
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    return check() if args.check else apply()


if __name__ == "__main__":
    raise SystemExit(main())
