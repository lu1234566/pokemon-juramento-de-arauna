#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / "data/maps/Route120/scripts.inc"
MAX_VISIBLE = 32

TARGETS = {
    "Route120_Text_StevenGreeting": (
        r"SEU BENTO: {PLAYER}, pare um\n",
        r"instante.\p",
        r"Tem algo escondido nesta ponte.\p",
        r"Trouxe uma LENTE HORIZONTE.\p",
        r"Quer descobrir o que e?$",
    ),
    "Route120_Text_StevenIllWaitHere": (
        r"SEU BENTO: Tudo bem.\p",
        r"Eu espero aqui.\p",
        r"Volte quando quiser observar\n",
        r"isso comigo.$",
    ),
    "Route120_Text_StevenReadyForBattle": (
        r"SEU BENTO: Pronto para olhar?\p",
        r"Se a lente revelar um POKéMON,\n",
        r"ele pode se assustar.$",
    ),
    "Route120_Text_StevenShowMeYourPower": (
        r"SEU BENTO: Entao fique atento.\p",
        r"Nao sabemos como ele vai reagir.$",
    ),
    "Route120_Text_StevenUsedDevonScope": (
        r"SEU BENTO ajustou a\n",
        r"LENTE HORIZONTE.$",
    ),
    "Route120_Text_StevenGiveDevonScope": (
        r"SEU BENTO: Voce lidou bem.\p",
        r"Fique com a lente.\p",
        r"Ela pode revelar outros\n",
        r"caminhos ocultos.$",
    ),
    "Route120_Text_StevenGoodbye": (
        r"SEU BENTO: Vou seguir para\n",
        r"MATA DO MEIO.\p",
        r"Ainda tenho trilhas para rever.\n",
        r"A gente se ve.$",
    ),
    "Kecleon_Text_SomethingUnseeable": (
        r"Algo invisivel bloqueia\n",
        r"o caminho.$",
    ),
    "Kecleon_Text_WantToUseDevonScope": (
        r"Algo invisivel bloqueia\n",
        r"o caminho.\p",
        r"Usar a LENTE HORIZONTE?$",
    ),
    "Kecleon_Text_UseDevonScopeMonAttacked": (
        r"{PLAYER} usou a LENTE HORIZONTE.\p",
        r"Um POKéMON invisivel apareceu!\p",
        r"Assustado, ele atacou!$",
    ),
    "Route120_Text_RouteSignFortree": (
        r"ROTA 120\n",
        r"{LEFT_ARROW} MATA DO MEIO$",
    ),
    "Route120_Text_RouteSign121": (
        r"{RIGHT_ARROW} ROTA 121\n",
        r"{LEFT_ARROW} ROTA 120$",
    ),
}

FORBIDDEN = (
    "DEVON SCOPE",
    "FORTREE CITY",
    "Something unseeable",
    "When a name",
)
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
            failures.append(f"missing Route 120 text block: {label}")
            continue
        block = match.group(0)
        if block != render(label, lines):
            failures.append(f"{label} differs from canonical Bento/lens text")
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
    print(f"Route 120 Bento/lens surface: {changed} changed; {len(TARGETS)} verified.")
    return 0


def check() -> int:
    failures = validate(TARGET.read_text(encoding="utf-8"))
    if failures:
        print("Route 120 Bento/lens surface check FAILED:")
        for failure in failures:
            print(f"- {failure}")
        return 1
    print(f"Route 120 Bento/lens surface PASS: {len(TARGETS)} blocks.")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    return check() if args.check else apply()


if __name__ == "__main__":
    raise SystemExit(main())
