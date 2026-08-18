#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / "data" / "maps" / "RustboroCity_Gym" / "scripts.inc"
MAX_VISIBLE = 32

# Badge receive/explanation and badge-referencing post-victory blocks are
# intentionally excluded: the dedicated badge integration lot owns them.
TARGETS = {
    "RustboroCity_Gym_Text_GymGuideAdvice": (
        r"Quer iniciar sua jornada por aqui?\p",
        r"DALVA usa POKéMON do tipo ROCK.\p",
        r"WATER e GRASS costumam ser\n",
        r"boas respostas contra eles.\p",
        r"Prepare-se e siga em frente.$",
    ),
    "RustboroCity_Gym_Text_TommyIntro": (
        r"Se nao passar por mim, nao vai\n",
        r"ter chance contra DALVA!$",
    ),
    "RustboroCity_Gym_Text_TommyPostBattle": (
        r"DALVA e muito mais forte que eu.\n",
        r"Nao baixe a guarda.$",
    ),
    "RustboroCity_Gym_Text_ExplainRockTomb": (
        r"A TM39 contem ROCK TOMB.\p",
        r"O golpe causa dano e reduz SPEED.\p",
        r"Pense bem antes de usar a TM.$",
    ),
    "RustboroCity_Gym_Text_GymStatue": (
        r"SERRA DO UIVO - DESAFIO DE DALVA$",
    ),
    "RustboroCity_Gym_Text_GymStatueCertified": (
        r"SERRA DO UIVO - DESAFIO DE DALVA\p",
        r"TREINADORES VITORIOSOS:\n",
        r"{PLAYER}$",
    ),
    "RustboroCity_Gym_Text_RoxanneRegisterCall": (
        r"DALVA: Ola, {PLAYER}.\p",
        r"Sou eu, de SERRA DO UIVO.\p",
        r"Soube que voce segue avancando.\n",
        r"Quando quiser voltar, estarei\n",
        r"pronta para outra batalha.$",
    ),
    "RustboroCity_Gym_Text_RegisteredRoxanne": (
        r"LIDER DALVA foi registrada\n",
        r"no POKéNAV.$",
    ),
}

FORBIDDEN = (
    "ROXANNE",
    "RUSTBORO",
    "BRAWLY",
    "ROXANNE'S CERTIFIED",
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
            failures.append(f"missing text block: {label}")
            continue
        block = match.group(0)
        if block != render(label, lines):
            failures.append(f"{label} does not match canonical Dalva text")
        for token in FORBIDDEN:
            if token.lower() in block.lower():
                failures.append(f"{label} still contains visible Emerald token: {token}")
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
    print(f"Dalva gym cleanup: {changed} changed; {len(TARGETS)} verified.")
    return 0


def check() -> int:
    failures = validate(TARGET.read_text(encoding="utf-8"))
    if failures:
        print("Dalva gym cleanup check FAILED:")
        for failure in failures:
            print(f"- {failure}")
        return 1
    print(f"Dalva gym cleanup PASS: {len(TARGETS)} blocks.")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    return check() if args.check else apply()


if __name__ == "__main__":
    raise SystemExit(main())
