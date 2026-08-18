#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TARGETS = {
    ROOT / "data/maps/RustboroCity_Flat2_2F/scripts.inc": (
        "O CONSORCIO HORIZONTE ja foi",
        "Meu pai trabalha no HORIZONTE.",
        "Quando crescer, quero trabalhar",
    ),
    ROOT / "data/maps/RustboroCity_Flat2_3F/scripts.inc": (
        "A DIRETORIA DO HORIZONTE guarda",
        "Muita gente daqui coleciona",
    ),
}
FORBIDDEN = ("DEVON", "CORPORATION", "PRESIDENT")
MAX_VISIBLE = 32
STRING_RE = re.compile(r'\.string "(.*)"')


def validate() -> list[str]:
    failures: list[str] = []
    for path, required in TARGETS.items():
        text = path.read_text(encoding="utf-8")
        for needle in required:
            if needle not in text:
                failures.append(f"{path.name}: missing {needle!r}")
        for raw in STRING_RE.findall(text):
            upper = raw.upper()
            for token in FORBIDDEN:
                if token in upper:
                    failures.append(f"{path.name}: legacy token {token!r} remains")
            for segment in re.split(r"\\[npl]", raw):
                visible = segment.replace("$", "")
                if len(visible) > MAX_VISIBLE:
                    failures.append(f"{path.name}: over-width segment {visible!r}")
    return failures


def check() -> int:
    failures = validate()
    if failures:
        print("Serra do Uivo upper-floor surface check FAILED:")
        for failure in failures:
            print(f"- {failure}")
        return 1
    print("Serra do Uivo upper-floor surface PASS.")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    parser.parse_args()
    return check()


if __name__ == "__main__":
    raise SystemExit(main())
