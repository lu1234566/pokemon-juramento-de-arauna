#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MATCH_CALL = ROOT / "data" / "text" / "match_call.inc"
STRINGS = ROOT / "src" / "strings.c"

CALLS: dict[str, tuple[str, ...]] = {
    "MatchCall_Text_Mom1": (
        r"ROSA: {PLAYER}, voce e ELIAS\n",
        r"sempre voltam a falar de POKéMON.\p",
        r"Eu gosto dos que ajudam aqui em casa.\n",
        r"Nem todo VINCULO precisa virar batalha.$",
    ),
    "MatchCall_Text_Mom2": (
        r"ROSA: Oi, {PLAYER}.\p",
        r"ELIAS continua passando quase todo\n",
        r"o tempo no PAMPA DA ESPERA.\p",
        r"Depois da batalha com voce, ele ficou\n",
        r"mais quieto do que costuma admitir.$",
    ),
    "MatchCall_Text_Mom3": (
        r"ROSA: {PLAYER}, nao se preocupe\n",
        r"comigo nem com a casa.\p",
        r"Use esses TENIS DE CORRIDA ate\n",
        r"eles pedirem aposentadoria.\p",
        r"E apareca quando sentir saudade.$",
    ),
}

EXACT = {
    'const u8 gText_MomMatchCallDesc[] = _("CALM & KIND");': 'const u8 gText_MomMatchCallDesc[] = _("MAE DE {PLAYER}");',
    'const u8 gText_MomMatchCallName[] = _("MOM");': 'const u8 gText_MomMatchCallName[] = _("ROSA");',
}

FORBIDDEN = ("MOM:", "PETALBURG", "DAD:", "NORMAN")


def marker_for(text: str, label: str) -> str:
    for suffix in ("::\n", ":\n"):
        marker = label + suffix
        if marker in text:
            return marker
    raise RuntimeError(f"Missing Rosa Match Call block: {label}")


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


def validate_calls(text: str) -> list[str]:
    failures: list[str] = []
    for label, lines in CALLS.items():
        start, end, marker = bounds(text, label)
        block = text[start:end]
        if block != render(marker, lines):
            failures.append(f"{label} differs from canonical Rosa call")
        for token in FORBIDDEN:
            if token in block:
                failures.append(f"{label} still exposes legacy token: {token}")
    return failures


def validate_exact(text: str) -> list[str]:
    failures: list[str] = []
    for old, new in EXACT.items():
        if new not in text:
            failures.append(f"missing Rosa PokéNav constant: {new}")
        if old in text:
            failures.append(f"legacy Mom PokéNav constant remains: {old}")
    return failures


def apply() -> int:
    text = MATCH_CALL.read_text(encoding="utf-8")
    changed_calls = 0
    for label, lines in CALLS.items():
        start, end, marker = bounds(text, label)
        replacement = render(marker, lines)
        if text[start:end] != replacement:
            text = text[:start] + replacement + text[end:]
            changed_calls += 1
    failures = validate_calls(text)
    if failures:
        raise RuntimeError("; ".join(failures))
    MATCH_CALL.write_text(text, encoding="utf-8")

    text = STRINGS.read_text(encoding="utf-8")
    changed_exact = 0
    for old, new in EXACT.items():
        if new in text and old not in text:
            continue
        count = text.count(old)
        if count != 1:
            raise RuntimeError(f"Expected exactly one {old!r}, found {count}")
        text = text.replace(old, new, 1)
        changed_exact += 1
    failures = validate_exact(text)
    if failures:
        raise RuntimeError("; ".join(failures))
    STRINGS.write_text(text, encoding="utf-8")

    print(f"Rosa Match Call cleanup: {changed_calls} calls and {changed_exact} constants changed.")
    return 0


def check() -> int:
    failures = validate_calls(MATCH_CALL.read_text(encoding="utf-8"))
    failures.extend(validate_exact(STRINGS.read_text(encoding="utf-8")))
    if failures:
        print("Rosa Match Call cleanup check FAILED:")
        for failure in failures:
            print(f"- {failure}")
        return 1
    print(f"Rosa Match Call cleanup check PASS: {len(CALLS)} calls and {len(EXACT)} constants.")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    return check() if args.check else apply()


if __name__ == "__main__":
    raise SystemExit(main())
