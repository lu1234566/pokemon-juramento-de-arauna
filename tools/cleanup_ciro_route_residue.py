#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

TARGETS = (
    (
        "data/maps/Route104/scripts.inc",
        "Route104_Text_MayWeShouldRegister",
        (
            r"CIRO: Seu POKéNAV ja aceita\n",
            r"contatos, certo?\p",
            r"Registre o meu. Quero comparar\n",
            r"o que encontrarmos pelo caminho.$",
        ),
    ),
    (
        "data/maps/Route104/scripts.inc",
        "Route104_Text_RegisteredMay",
        (r"CIRO foi registrado\n", r"no POKéNAV.$"),
    ),
    (
        "data/maps/Route104/scripts.inc",
        "Route104_Text_BrendanWeShouldRegister",
        (
            r"CIRO: Seu POKéNAV ja aceita\n",
            r"contatos, certo?\p",
            r"Registre o meu. Quero comparar\n",
            r"o que encontrarmos pelo caminho.$",
        ),
    ),
    (
        "data/maps/Route104/scripts.inc",
        "Route104_Text_RegisteredBrendan",
        (r"CIRO foi registrado\n", r"no POKéNAV.$"),
    ),
    (
        "data/maps/Route110/scripts.inc",
        "Route110_Text_MayExplainItemfinder",
        (
            r"CIRO: Isso e um ITEMFINDER.\p",
            r"Ele reage quando ha algo\n",
            r"escondido por perto.\p",
            r"Use direito. Nao vou ficar\n",
            r"marcando tudo para voce.$",
        ),
    ),
    (
        "data/maps/Route110/scripts.inc",
        "Route110_Text_BrendanExplainItemfinder",
        (
            r"CIRO: Isso e um ITEMFINDER.\p",
            r"Ele reage quando ha algo\n",
            r"escondido por perto.\p",
            r"Use direito. Nao vou ficar\n",
            r"marcando tudo para voce.$",
        ),
    ),
)

FORBIDDEN = ("MAY:", "BRENDAN:", "registered MAY", "registered BRENDAN", "DEVON")


def pattern_for(label: str) -> re.Pattern[str]:
    return re.compile(
        rf"(?m)^{re.escape(label)}:\n(?:\t\.string \"[^\n]*\"\n)+"
    )


def replacement(label: str, lines: tuple[str, ...]) -> str:
    return label + ":\n" + "".join(f'\t.string "{line}"\n' for line in lines)


def extract(text: str, label: str) -> str:
    match = pattern_for(label).search(text)
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
            failures.append(f"{rel_path}: {label} still contains {token}")
    return failures


def apply() -> int:
    changed_files: set[Path] = set()
    for rel_path, label, lines in TARGETS:
        path = ROOT / rel_path
        text = path.read_text(encoding="utf-8")
        updated, count = pattern_for(label).subn(
            lambda _match: replacement(label, lines), text, count=1
        )
        if count != 1:
            raise RuntimeError(f"Could not uniquely replace {label} (matches={count})")
        if updated != text:
            path.write_text(updated, encoding="utf-8")
            changed_files.add(path)
        failures = validate(extract(updated, label), rel_path, label, lines)
        if failures:
            raise RuntimeError("; ".join(failures))
    print(
        f"Ciro route cleanup: {len(changed_files)} file(s) changed; "
        f"{len(TARGETS)} block(s) verified."
    )
    return 0


def check() -> int:
    failures: list[str] = []
    for rel_path, label, lines in TARGETS:
        text = (ROOT / rel_path).read_text(encoding="utf-8")
        failures.extend(validate(extract(text, label), rel_path, label, lines))
    if failures:
        print("Ciro route cleanup check FAILED:")
        for failure in failures:
            print(f"- {failure}")
        return 1
    print(f"Ciro route cleanup check PASS: {len(TARGETS)} block(s).")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    return check() if args.check else apply()


if __name__ == "__main__":
    raise SystemExit(main())
