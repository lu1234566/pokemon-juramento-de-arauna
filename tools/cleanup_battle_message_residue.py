#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / "src" / "battle_message.c"
OLD = 'static const u8 sText_DontLeaveBirch[] = _("PROF. BIRCH: Don\'t leave me like this!\\p");'
NEW = 'static const u8 sText_DontLeaveBirch[] = _("ANAHI: Nao me deixe aqui!\\p");'


def validate(text: str) -> list[str]:
    failures: list[str] = []
    if NEW not in text:
        failures.append("Arauna rescue battle message is missing")
    if OLD in text:
        failures.append("Professor Birch rescue battle message is still visible")
    return failures


def apply() -> int:
    text = TARGET.read_text(encoding="utf-8")
    if NEW in text and OLD not in text:
        print("Battle-message residue cleanup: already applied.")
        return 0
    count = text.count(OLD)
    if count != 1:
        raise RuntimeError(f"Expected exactly one Professor Birch battle message, found {count}")
    updated = text.replace(OLD, NEW, 1)
    failures = validate(updated)
    if failures:
        raise RuntimeError("; ".join(failures))
    TARGET.write_text(updated, encoding="utf-8")
    print("Battle-message residue cleanup: 1 visible Professor Birch line replaced with Anahi.")
    return 0


def check() -> int:
    failures = validate(TARGET.read_text(encoding="utf-8"))
    if failures:
        print("Battle-message residue cleanup check FAILED:")
        for failure in failures:
            print(f"- {failure}")
        return 1
    print("Battle-message residue cleanup check PASS.")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    return check() if args.check else apply()


if __name__ == "__main__":
    raise SystemExit(main())
