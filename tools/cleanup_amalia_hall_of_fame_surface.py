#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / "data/maps/EverGrandeCity_HallOfFame/scripts.inc"
MAX_VISIBLE = 32

TARGETS = {
    "EverGrandeCity_HallOfFame_Text_HereWeHonorLeagueChampions": (
        r"AMALIA: Aqui ficam os nomes\n",
        r"dos CAMPEOES de ARAUNA.\p",
        r"Nao para torna-los eternos,\n",
        r"mas para lembrar quem chegou.$",
    ),
    "EverGrandeCity_HallOfFame_Text_LetsRecordYouAndYourPartnersNames": (
        r"AMALIA: Agora registraremos\n",
        r"voce e seus parceiros.\p",
        r"Cada nome aqui pertence\n",
        r"a jornada que trouxe voces.\p",
        r"Este registro e de todos.$",
    ),
}

BLOCK_RE_TEMPLATE = r'(?m)^{label}:\n(?:\t\.string "[^\n]*"\n)+'
CONTROL_RE = re.compile(r"\\[npl]|\{[^}]+\}")


def block_re(label: str) -> re.Pattern[str]:
    return re.compile(BLOCK_RE_TEMPLATE.format(label=re.escape(label)))


def render(label: str, lines: tuple[str, ...]) -> str:
    return label + ":\n" + "".join(f'\t.string "{line}"\n' for line in lines)


def validate(text: str) -> list[str]:
    failures: list[str] = []
    for label, lines in TARGETS.items():
        match = block_re(label).search(text)
        if not match:
            failures.append(f"missing Hall of Fame text block: {label}")
            continue
        block = match.group(0)
        if block != render(label, lines):
            failures.append(f"{label} differs from canonical Amalia Hall of Fame text")
        if "Arauna sobreviveu a" in block:
            failures.append(f"{label} still contains repeated pre-battle monologue")
        for raw in re.findall(r'\.string "(.*)"', block):
            for segment in re.split(r"\\[npl]", raw):
                visible = CONTROL_RE.sub("", segment).replace("$", "")
                if len(visible) > MAX_VISIBLE:
                    failures.append(f"{label} exceeds {MAX_VISIBLE} visible chars: {visible!r}")
    return failures


def apply() -> int:
    text = TARGET.read_text(encoding="utf-8")
    changed = 0
    for label, lines in TARGETS.items():
        updated, count = block_re(label).subn(lambda _m: render(label, lines), text, count=1)
        if count != 1:
            raise RuntimeError(f"Could not uniquely replace {label} (matches={count})")
        if updated != text:
            changed += 1
        text = updated
    failures = validate(text)
    if failures:
        raise RuntimeError("; ".join(failures))
    TARGET.write_text(text, encoding="utf-8")
    print(f"Amalia Hall of Fame surface: {changed} changed; {len(TARGETS)} verified.")
    return 0


def check() -> int:
    failures = validate(TARGET.read_text(encoding="utf-8"))
    if failures:
        print("Amalia Hall of Fame surface check FAILED:")
        for failure in failures:
            print(f"- {failure}")
        return 1
    print(f"Amalia Hall of Fame surface PASS: {len(TARGETS)} blocks.")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    return check() if args.check else apply()


if __name__ == "__main__":
    raise SystemExit(main())
