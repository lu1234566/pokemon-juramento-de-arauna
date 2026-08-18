#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / "data/maps/SootopolisCity/scripts.inc"
MAX_VISIBLE = 32

# The badge/HM explanation block SootopolisCity_Text_ExplainWaterfallGoToGym is
# intentionally excluded because the dedicated badge PR owns that surface.
TARGETS = {
    "SootopolisCity_Text_InvolvedWithCrisisComeWithMe": (
        r"SEU BENTO: Olhe para a agua.\p",
        r"Nao e so uma tempestade.\p",
        r"GROUDON e KYOGRE despertaram\n",
        r"quase ao mesmo tempo.\p",
        r"Venha comigo.\p",
        r"AMALIA esta na entrada da\n",
        r"CAVERNA DA ORIGEM.$",
    ),
    "SootopolisCity_Text_HereWereAreHelpWallace": (
        r"SEU BENTO: E aqui.\p",
        r"AMALIA esta esperando la dentro.\p",
        r"Ela conhece os registros da Liga\n",
        r"sobre esta crise.$",
    ),
    "SootopolisCity_Text_KnowWhatsNeededToHelpHim": (
        r"SEU BENTO: AMALIA tenta achar\n",
        r"uma forma de conter os dois.\p",
        r"Se ela pediu tempo, vamos dar.$",
    ),
    "SootopolisCity_Text_MaxieArchieLeft": (
        r"SEU BENTO: A cidade ainda\n",
        r"esta sob risco.\p",
        r"LUZIA e OTACILIO ja sairam daqui.\p",
        r"Agora precisamos cuidar do resto.$",
    ),
    "SootopolisCity_Text_NeverBeenToSkyPillar": (
        r"SEU BENTO: Nunca subi a\n",
        r"TORRE JURAMENTO.\p",
        r"Mas AMALIA conhece os registros.\p",
        r"Se foi para la, ha um motivo.$",
    ),
    "SootopolisCity_Text_SoThatsRayquaza": (
        r"SEU BENTO: Entao esse e\n",
        r"RAYQUAZA...\p",
        r"Agora entendo por que AMALIA\n",
        r"procurava a torre.$",
    ),
    "SootopolisCity_Text_HaventYouScaledSkyPillar": (
        r"AMALIA: Ainda nao foi para a\n",
        r"TORRE JURAMENTO?\p",
        r"Nao podemos esperar mais.\n",
        r"Suba e encontre RAYQUAZA.$",
    ),
    "SootopolisCity_Text_AquaMagmaDidntMeanHarm": (
        r"AMALIA: {PLAYER}, antes de seguir,\n",
        r"fale com LUZIA e OTACILIO.\p",
        r"Eles precisam explicar o que\n",
        r"fizeram aqui.$",
    ),
    "SootopolisCity_Text_ThankYouForHelpAcceptThis": (
        r"AMALIA: Obrigada por ajudar\n",
        r"AGUAS DE M'BOI.\p",
        r"Leve isto.\n",
        r"Voce ainda vai precisar dele.$",
    ),
    "SootopolisCity_Text_DazzledByMentor": (
        r"AMALIA: DONA CELINA espera\n",
        r"no GINASIO.\p",
        r"Quando estiver pronto, entre.$",
    ),
}

FORBIDDEN = (
    "WALLACE:",
    "LEMBRANTES and AQUA",
    "Arauna sobreviveu a",
    "Quando um nome some",
    "IARA-MAE puxa VINCULOS",
    "SKY PILLAR",
    "SOOTOPOLIS",
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
            failures.append(f"missing Aguas de M'Boi crisis block: {label}")
            continue
        block = match.group(0)
        if block != render(label, lines):
            failures.append(f"{label} differs from canonical crisis text")
        for token in FORBIDDEN:
            if token.lower() in block.lower():
                failures.append(f"{label} still exposes legacy/misassigned text: {token}")
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
    print(f"Aguas de M'Boi crisis surface: {changed} changed; {len(TARGETS)} verified.")
    return 0


def check() -> int:
    failures = validate(TARGET.read_text(encoding="utf-8"))
    if failures:
        print("Aguas de M'Boi crisis surface check FAILED:")
        for failure in failures:
            print(f"- {failure}")
        return 1
    print(f"Aguas de M'Boi crisis surface PASS: {len(TARGETS)} blocks.")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    return check() if args.check else apply()


if __name__ == "__main__":
    raise SystemExit(main())
