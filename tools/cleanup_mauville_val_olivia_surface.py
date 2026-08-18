#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / "data" / "maps" / "MauvilleCity" / "scripts.inc"
MAX_VISIBLE = 32

TARGETS = {
    "MauvilleCity_Text_UncleHesTooPeppy": (
        r"TIO: Os POKéMON fizeram muito\n",
        r"bem ao VAL.\p",
        r"Agora ele quer provar tudo\n",
        r"de uma vez. Isso me preocupa.$",
    ),
    "MauvilleCity_Text_WallyWantToChallengeGym": (
        r"VAL: Quero tentar o desafio\n",
        r"da ENCRUZILHADA.\p",
        r"Preciso saber ate onde consigo\n",
        r"ir por conta propria.$",
    ),
    "MauvilleCity_Text_UncleYourePushingIt": (
        r"TIO: Calma, VAL.\p",
        r"Voce ficou mais forte, sim.\n",
        r"Mas nao precisa se apressar.$",
    ),
    "MauvilleCity_Text_WallyWeCanBeatAnyone": (
        r"VAL: Eu sei que ainda tenho\n",
        r"muito a aprender.\p",
        r"Mas quero descobrir isso\n",
        r"lutando do meu jeito.$",
    ),
    "MauvilleCity_Text_WallyWillYouBattleMe": (
        r"VAL: {PLAYER}, lute comigo.\p",
        r"Quero medir meu progresso\n",
        r"contra alguem em quem confio.$",
    ),
    "MauvilleCity_Text_WallyMyUncleWontKnowImStrong": (
        r"VAL: Se eu recuar agora, meu tio\n",
        r"vai achar que ainda nao consigo.\p",
        r"Quando estiver pronto, lute comigo.$",
    ),
    "MauvilleCity_Text_UncleCanYouBattleWally": (
        r"TIO: {PLAYER}, pode lutar com VAL?\p",
        r"Talvez assim ele entenda que\n",
        r"nao precisa correr.$",
    ),
    "MauvilleCity_Text_WallyPleaseBattleMe": (
        r"VAL: Por favor, {PLAYER}.\n",
        r"Lute comigo desta vez.$",
    ),
    "MauvilleCity_Text_WallyHereICome": (
        r"VAL: Certo. Vou com tudo!$",
    ),
    "MauvilleCity_Text_WallyDefeat": (
        r"VAL: Ainda falta muito...$",
    ),
    "MauvilleCity_Text_WallyIllGoBackToVerdanturf": (
        r"VAL: Vou voltar ao\n",
        r"VALE DO SILENCIO.\p",
        r"Preciso pensar no que aprendi.$",
    ),
    "MauvilleCity_Text_ThankYouNotEnoughToBattle": (
        r"VAL: Obrigado, {PLAYER}.\p",
        r"Ter POKéMON nao basta.\n",
        r"Preciso aprender a ouvir eles\n",
        r"e tambem a mim mesmo.$",
    ),
    "MauvilleCity_Text_UncleNoNeedToBeDown": (
        r"TIO: Nao abaixe a cabeca, VAL.\p",
        r"Ficar mais forte leva tempo.\n",
        r"Vamos voltar para casa.$",
    ),
    "MauvilleCity_Text_UncleVisitUsSometime": (
        r"TIO: Entao foi voce quem ajudou\n",
        r"VAL no inicio da viagem.\p",
        r"Visite-nos no VALE DO SILENCIO\n",
        r"quando passar por la.$",
    ),
    "MauvilleCity_Text_WallyPokenavCall": (
        r"VAL: {PLAYER}, sou eu.\p",
        r"Estou treinando no meu ritmo.\n",
        r"Quando nos virmos, quero\n",
        r"mostrar quanto avancei.$",
    ),
    "MauvilleCity_Text_RegisteredWally": (
        r"VAL foi registrado\n",
        r"no POKéNAV.$",
    ),
    "MauvilleCity_Text_ScottYouDidntHoldBack": (
        r"VIAJANTE: Eu vi essa batalha.\p",
        r"Voce nao pegou leve com VAL,\n",
        r"e fez bem.\p",
        r"Respeitar alguem tambem e\n",
        r"leva-lo a serio numa luta.\p",
        r"Continuarei de olho em voce.$",
    ),
    "MauvilleCity_Text_WattsonThanksTakeTM": (
        r"OLIVIA: Bom trabalho, {PLAYER}.\p",
        r"Voce resolveu o problema sem\n",
        r"colocar a rede em risco.\p",
        r"Leve esta TM como agradecimento.\n",
        r"Ela contem THUNDERBOLT.$",
    ),
}

FORBIDDEN = (
    "WALLY",
    "SCOTT:",
    "WATTSON:",
    "VERDANTURF",
    "UNCLE:",
    "Being a TRAINER",
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
            failures.append(f"{label} does not match canonical Arauna text")
        for token in FORBIDDEN:
            if token.lower() in block.lower():
                failures.append(f"{label} still contains legacy token: {token}")
        for raw in re.findall(r'\.string "(.*)"', block):
            for segment in re.split(r"\\[npl]", raw):
                visible = CONTROL_RE.sub("", segment).replace("$", "")
                if len(visible) > MAX_VISIBLE:
                    failures.append(
                        f"{label} exceeds {MAX_VISIBLE} chars: {visible!r}"
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
    print(f"Mauville Val/Olivia cleanup: {changed} changed; {len(TARGETS)} verified.")
    return 0


def check() -> int:
    failures = validate(TARGET.read_text(encoding="utf-8"))
    if failures:
        print("Mauville Val/Olivia cleanup check FAILED:")
        for failure in failures:
            print(f"- {failure}")
        return 1
    print(f"Mauville Val/Olivia cleanup PASS: {len(TARGETS)} blocks.")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    return check() if args.check else apply()


if __name__ == "__main__":
    raise SystemExit(main())
