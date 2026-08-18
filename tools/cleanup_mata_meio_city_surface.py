#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / "data/maps/FortreeCity/scripts.inc"
MAX_VISIBLE = 32

TARGETS = {
    "FortreeCity_Text_SawGiganticPokemonInSky": (
        r"Pouca gente acredita, mas vi\n",
        r"um POKéMON enorme no ceu.\p",
        r"Ele seguiu na direcao da\n",
        r"ROTA 131.\p",
        r"Ah... voce esta com cheiro\n",
        r"de cinza.\p",
        r"Passou perto de um vulcao?$",
    ),
    "FortreeCity_Text_SomethingBlockingGym": (
        r"Quero entrar no GINASIO,\n",
        r"mas algo bloqueia o caminho.\p",
        r"Treinei bastante na ROTA 120.$",
    ),
    "FortreeCity_Text_ThisTimeIllBeatWinona": (
        r"Agora o caminho esta livre!\p",
        r"Desta vez vou desafiar LIDIA.$",
    ),
    "FortreeCity_Text_TreesGrowByDrinkingRainwater": (
        r"As arvores daqui bebem muita\n",
        r"agua da chuva.\p",
        r"E por isso que crescem tao\n",
        r"fortes mesmo com tantas casas.$",
    ),
    "FortreeCity_Text_EveryoneHealthyAndLively": (
        r"As casas ficam sobre arvores.\p",
        r"Talvez seja por isso que todo\n",
        r"mundo daqui vive se movendo.\p",
        r"Ate eu me sinto mais jovem.$",
    ),
    "FortreeCity_Text_PokemonThatEvolveWhenTraded": (
        r"Alguns POKéMON evoluem quando\n",
        r"sao trocados entre TRAINERS.\p",
        r"Foi o que me contaram.$",
    ),
    "FortreeCity_Text_SomethingUnseeable": (
        r"Algo invisivel bloqueia\n",
        r"o caminho.$",
    ),
    "FortreeCity_Text_UnseeableUseDevonScope": (
        r"Algo invisivel bloqueia\n",
        r"o caminho.\p",
        r"Usar a LENTE HORIZONTE?$",
    ),
    "FortreeCity_Text_UsedDevonScopePokemonFled": (
        r"{PLAYER} usou a LENTE HORIZONTE.\p",
        r"Um POKéMON invisivel apareceu!\p",
        r"Assustado, ele fugiu!$",
    ),
}

FORBIDDEN = (
    "DEVON SCOPE",
    "WINONA",
    "No one believes me",
    "The CITY consists",
    "There are POKéMON that evolve",
    "Os sensores registram duas",
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
            failures.append(f"missing Mata do Meio text block: {label}")
            continue
        block = match.group(0)
        if block != render(label, lines):
            failures.append(f"{label} differs from canonical Mata do Meio text")
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
    print(f"Mata do Meio city surface: {changed} changed; {len(TARGETS)} verified.")
    return 0


def check() -> int:
    failures = validate(TARGET.read_text(encoding="utf-8"))
    if failures:
        print("Mata do Meio city surface check FAILED:")
        for failure in failures:
            print(f"- {failure}")
        return 1
    print(f"Mata do Meio city surface PASS: {len(TARGETS)} blocks.")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    return check() if args.check else apply()


if __name__ == "__main__":
    raise SystemExit(main())
