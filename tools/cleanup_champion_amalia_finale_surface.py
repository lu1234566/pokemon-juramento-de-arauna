#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / "data/maps/EverGrandeCity_ChampionsRoom/scripts.inc"
MAX_VISIBLE = 32

TARGETS = {
    "EverGrandeCity_ChampionsRoom_Text_IntroSpeech": (
        r"AMALIA: Arauna sobreviveu a\n",
        r"verdades pela metade por tempo\n",
        r"demais.\p",
        r"A Liga tambem deve respostas\n",
        r"a quem foi apagado.\p",
        r"Se quer ocupar este lugar,\n",
        r"mostre o que trouxe ate aqui.$",
    ),
    "EverGrandeCity_ChampionsRoom_Text_Defeat": (
        r"AMALIA: ...Entao voce chegou\n",
        r"ate o fim.$",
    ),
    "EverGrandeCity_ChampionsRoom_Text_PostBattleSpeech": (
        r"AMALIA: A partir de agora,\n",
        r"este lugar tambem leva seu nome.\p",
        r"Ser CAMPEAO nao apaga as\n",
        r"dividas da Liga.\p",
        r"Talvez voce possa ajudar\n",
        r"a encara-las.$",
    ),
    "EverGrandeCity_ChampionsRoom_Text_MayAdvice": (
        r"CIRO: {PLAYER}! Eu vim dizer...\p",
        r"Espera. Voce ja venceu?$",
    ),
    "EverGrandeCity_ChampionsRoom_Text_MayItsAlreadyOver": (
        r"CIRO: Claro.\p",
        r"Eu devia ter imaginado.\p",
        r"Nao vou fingir que isso\n",
        r"nao mexe comigo.\p",
        r"Mas parabens.$",
    ),
    "EverGrandeCity_ChampionsRoom_Text_BrendanAdvice": (
        r"CIRO: {PLAYER}! Eu vim dizer...\p",
        r"Espera. Voce ja venceu?$",
    ),
    "EverGrandeCity_ChampionsRoom_Text_BrendanYouveWon": (
        r"CIRO: Voce venceu mesmo.\p",
        r"Ainda tenho coisas para decidir\n",
        r"sobre o HORIZONTE.\p",
        r"Mas hoje isso e seu.\n",
        r"Parabens.$",
    ),
    "EverGrandeCity_ChampionsRoom_Text_BirchArriveRatePokedex": (
        r"ANAHI: Cheguei tarde para\n",
        r"a batalha, pelo jeito.\p",
        r"Deixe-me ver sua POKéDEX\n",
        r"antes do registro.$",
    ),
    "EverGrandeCity_ChampionsRoom_Text_BirchCongratulations": (
        r"ANAHI: E agora voce e CAMPEAO.\p",
        r"Parabens, {PLAYER}.\p",
        r"Ainda temos muito para falar,\n",
        r"mas hoje e seu dia.$",
    ),
    "EverGrandeCity_ChampionsRoom_Text_WallaceComeWithMe": (
        r"AMALIA: {PLAYER}...\p",
        r"Melhor dizendo: novo CAMPEAO\n",
        r"de ARAUNA.\p",
        r"Venha comigo.$",
    ),
    "EverGrandeCity_ChampionsRoom_Text_WallaceWaitOutside": (
        r"AMALIA: Daqui em diante,\n",
        r"so o CAMPEAO entra.\p",
        r"ANAHI, CIRO, esperem aqui.\p",
        r"{PLAYER}, vamos registrar\n",
        r"sua equipe.$",
    ),
    "EverGrandeCity_ChampionsRoom_Text_MayCongratulations": (
        r"CIRO: Vai la.\p",
        r"Depois me conte como e ter\n",
        r"seu nome gravado na Liga.$",
    ),
    "EverGrandeCity_ChampionsRoom_Text_BrendanCongratulations": (
        r"CIRO: Vai la.\p",
        r"Depois me conte como e ter\n",
        r"seu nome gravado na Liga.$",
    ),
}

FORBIDDEN = (
    "WALLACE:",
    "I, the CHAMPION",
    "That was wonderful work",
    "No, let me rephrase",
    "Arauna sobreviveu a\\nverdade pela metade",
    "Voce continua olhando\\npara cada cicatriz",
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
            failures.append(f"missing Champion-room text block: {label}")
            continue
        block = match.group(0)
        if block != render(label, lines):
            failures.append(f"{label} differs from canonical Amalia finale text")
        for token in FORBIDDEN:
            if token.lower() in block.lower():
                failures.append(f"{label} still exposes legacy/repeated text: {token}")
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
    print(f"Amalia finale surface: {changed} changed; {len(TARGETS)} verified.")
    return 0


def check() -> int:
    failures = validate(TARGET.read_text(encoding="utf-8"))
    if failures:
        print("Amalia finale surface check FAILED:")
        for failure in failures:
            print(f"- {failure}")
        return 1
    print(f"Amalia finale surface PASS: {len(TARGETS)} blocks.")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    return check() if args.check else apply()


if __name__ == "__main__":
    raise SystemExit(main())
