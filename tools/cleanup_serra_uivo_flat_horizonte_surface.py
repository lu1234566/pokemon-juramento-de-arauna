#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / "data/maps/RustboroCity_Flat2_1F/scripts.inc"

OLD = (
    'RustboroCity_Flat2_1F_Text_DevonWorkersLiveHere:\n'
    '\t.string "CONSORCIO HORIZONTEORATION\'s workers live in\\n"\n'
    '\t.string "this building.$"\n'
)
NEW = (
    'RustboroCity_Flat2_1F_Text_DevonWorkersLiveHere:\n'
    '\t.string "Muita gente que trabalha no\\n"\n'
    '\t.string "CONSORCIO HORIZONTE mora aqui.$"\n'
)


def validate(text: str) -> list[str]:
    failures: list[str] = []
    if NEW not in text:
        failures.append("canonical Horizonte apartment block is missing")
    if "HORIZONTEORATION" in text:
        failures.append("malformed HORIZONTEORATION token remains")
    return failures


def apply() -> int:
    text = TARGET.read_text(encoding="utf-8")
    if NEW in text and OLD not in text:
        print("Serra do Uivo apartment surface already canonical.")
        return 0
    if text.count(OLD) != 1:
        raise RuntimeError(f"Expected exactly one legacy apartment block, found {text.count(OLD)}")
    text = text.replace(OLD, NEW, 1)
    failures = validate(text)
    if failures:
        raise RuntimeError("; ".join(failures))
    TARGET.write_text(text, encoding="utf-8")
    print("Serra do Uivo apartment surface cleanup applied.")
    return 0


def check() -> int:
    failures = validate(TARGET.read_text(encoding="utf-8"))
    if failures:
        print("Serra do Uivo apartment surface check FAILED:")
        for failure in failures:
            print(f"- {failure}")
        return 1
    print("Serra do Uivo apartment surface PASS.")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    return check() if args.check else apply()


if __name__ == "__main__":
    raise SystemExit(main())
