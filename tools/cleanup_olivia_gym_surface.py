#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / "data" / "maps" / "MauvilleCity_Gym" / "scripts.inc"
MAX_VISIBLE = 32

TARGETS = {
    "MauvilleCity_Gym_Text_GymGuideAdvice": (
        r"Vai encarar o desafio daqui?\p",
        r"OLIVIA domina POKéMON do tipo\n",
        r"ELECTRIC. Agua nao ajuda muito.\p",
        r"E cuidado com os interruptores:\n",
        r"eles controlam as barreiras.$",
    ),
    "MauvilleCity_Gym_Text_GymGuidePostVictory": (
        r"Boa! Voce venceu OLIVIA e\n",
        r"abriu seu caminho.$",
    ),
    "MauvilleCity_Gym_Text_ShawnIntro": (
        r"Treinei ao lado de OLIVIA!\n",
        r"Nao vou facilitar para voce.$",
    ),
    "MauvilleCity_Gym_Text_ShawnPostBattle": (
        r"OLIVIA entende esta rede como\n",
        r"pouca gente em ENCRUZILHADA.\p",
        r"Ela sempre pensa antes de\n",
        r"mexer em uma fonte de energia.$",
    ),
    "MauvilleCity_Gym_Text_BenPostBattle": (
        r"OLIVIA gosta de testar quem entra\n",
        r"com essas barreiras e chaves.$",
    ),
    "MauvilleCity_Gym_Text_VivianPostBattle": (
        r"OLIVIA conhece cada parte da\n",
        r"rede de ENCRUZILHADA.\p",
        r"Nao e so forca: ela observa\n",
        r"como tudo esta conectado.$",
    ),
    "MauvilleCity_Gym_Text_AngeloPostBattle": (
        r"As luzes daqui quase cegam!\n",
        r"OLIVIA realmente gosta de energia.$",
    ),
    "MauvilleCity_Gym_Text_ReceivedDynamoBadge": (
        r"{PLAYER} recebeu a DYNAMO BADGE\n",
        r"de OLIVIA.$",
    ),
    "MauvilleCity_Gym_Text_ExplainDynamoBadgeTakeThis": (
        r"Com a DYNAMO BADGE, seus POKéMON\n",
        r"podem usar ROCK SMASH fora da luta.\p",
        r"Ela tambem ajuda seus POKéMON\n",
        r"a ficarem um pouco mais rapidos.\p",
        r"Leve isto tambem.$",
    ),
    "MauvilleCity_Gym_Text_ExplainShockWave": (
        r"A TM34 contem SHOCK WAVE.\p",
        r"E um golpe eletrico confiavel\n",
        r"que nao costuma errar.$",
    ),
    "MauvilleCity_Gym_Text_RegisteredWattson": (
        r"LIDER OLIVIA foi registrada\n",
        r"no POKéNAV.$",
    ),
    "MauvilleCity_Gym_Text_GymStatue": (
        r"ENCRUZILHADA - DESAFIO DE OLIVIA$",
    ),
    "MauvilleCity_Gym_Text_GymStatueCertified": (
        r"ENCRUZILHADA - DESAFIO DE OLIVIA\p",
        r"TREINADORES VITORIOSOS:\n",
        r"{PLAYER}$",
    ),
}

FORBIDDEN = (
    "WATTSON",
    "MAUVILLE",
    "GYM LEADER WATTSON",
    "WATTSON'S CERTIFIED",
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
            failures.append(f"{label} does not match canonical Olivia text")
        for token in FORBIDDEN:
            if token.lower() in block.lower():
                failures.append(f"{label} still contains visible Emerald token: {token}")
        for raw in re.findall(r'\.string "(.*)"', block):
            for segment in re.split(r"\\[npl]", raw):
                visible = CONTROL_RE.sub("", segment).replace("$", "")
                if len(visible) > MAX_VISIBLE:
                    failures.append(
                        f"{label} exceeds {MAX_VISIBLE} visible chars: {visible!r}"
                    )
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
    print(f"Olivia gym cleanup: {changed} changed; {len(TARGETS)} verified.")
    return 0


def check() -> int:
    failures = validate(TARGET.read_text(encoding="utf-8"))
    if failures:
        print("Olivia gym cleanup check FAILED:")
        for failure in failures:
            print(f"- {failure}")
        return 1
    print(f"Olivia gym cleanup PASS: {len(TARGETS)} blocks.")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    return check() if args.check else apply()


if __name__ == "__main__":
    raise SystemExit(main())
