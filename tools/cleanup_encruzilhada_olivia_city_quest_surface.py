#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / "data/maps/MauvilleCity/scripts.inc"
MAX_VISIBLE = 32

TARGETS = {
    "MauvilleCity_Text_WattsonNeedFavorTakeKey": (
        r"OLIVIA: {PLAYER}, preciso de ajuda.\p",
        r"Uma subestacao antiga continua\n",
        r"ligada sob ENCRUZILHADA.\p",
        r"A rede esta instavel e eu nao\n",
        r"quero arriscar outra descarga.\p",
        r"Leve esta CHAVE e desligue\n",
        r"o gerador principal.$",
    ),
    "MauvilleCity_Text_WattsonWontBeChallenge": (
        r"OLIVIA: A CHAVE abre o acesso\n",
        r"da subestacao antiga.\p",
        r"Desligue o gerador e volte.\n",
        r"Nao mexa no que nao conhecer.$",
    ),
    "MauvilleCity_Text_WattsonThanksTakeTM": (
        r"OLIVIA: A rede estabilizou.\p",
        r"Voce fez exatamente o necessario\n",
        r"e nao tentou forcar o sistema.\p",
        r"Leve esta TM como agradecimento.\n",
        r"Ela contem THUNDERBOLT.$",
    ),
    "MauvilleCity_Text_WattsonYoungTakeCharge": (
        r"OLIVIA: Energia pede cuidado.\p",
        r"Quanto maior a rede, maior\n",
        r"a responsabilidade de quem\n",
        r"decide onde ela deve chegar.$",
    ),
}

FORBIDDEN = ("WATTSON", "MAUVILLE", "Wahahaha", "right choice asking you")
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
            failures.append(f"missing text block: {label}")
            continue
        block = match.group(0)
        if block != render(label, lines):
            failures.append(f"{label} differs from canonical Olivia city text")
        for token in FORBIDDEN:
            if token.lower() in block.lower():
                failures.append(f"{label} still exposes legacy token: {token}")
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
    print(f"Olivia city quest cleanup: {changed} changed; {len(TARGETS)} verified.")
    return 0


def check() -> int:
    failures = validate(TARGET.read_text(encoding="utf-8"))
    if failures:
        print("Olivia city quest check FAILED:")
        for failure in failures:
            print(f"- {failure}")
        return 1
    print(f"Olivia city quest PASS: {len(TARGETS)} blocks.")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    return check() if args.check else apply()


if __name__ == "__main__":
    raise SystemExit(main())
