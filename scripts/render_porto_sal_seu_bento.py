#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / "data" / "maps" / "SlateportCity" / "scripts.inc"
MAX_VISIBLE_WIDTH = 32
CONTROL_RE = re.compile(r"\\[npl]")
PLACEHOLDER_RE = re.compile(r"\{[^}]+\}")

TARGETS: dict[str, tuple[tuple[str, ...], tuple[str, ...]]] = {
    "SlateportCity_Text_YouDroveTeamAquaAway": (("HORIZONTE: Nao somos soldados",), (
        "SEU BENTO: Entao foi voce quem\\n",
        "barrou aquela equipe no MUSEU.\\p",
        "Gosto de saber quem age quando\\n",
        "uma historia sai do papel.$",
    )),
    "SlateportCity_Text_MaybeThisTrainer": (("CIRO:", "HORIZONTE"), (
        "SEU BENTO: Tenho acompanhado\\n",
        "alguns treinadores por Arauna.\\p",
        "Voce acabou de entrar no meu\\n",
        "caderno.$",
    )),
    "SlateportCity_Text_LetsRegisterEachOther": (("SCOTT:", "POKéNAVS"), (
        "SEU BENTO: Vamos registrar um\\n",
        "ao outro no POKéNAV.\\p",
        "Assim eu aviso quando encontrar\\n",
        "uma pista que valha a viagem.$",
    )),
    "SlateportCity_Text_RegisteredScott": (("SCOTT", "POKéNAV"), (
        "SEU BENTO foi registrado no\\n",
        "POKéNAV.$",
    )),
    "SlateportCity_Text_KeepEyeOnTrainersBeSeeingYou": (("SCOTT:", "other towns"), (
        "SEU BENTO: Eu ficaria por aqui,\\n",
        "mas ha muito caminho para ver.\\p",
        "Vou circular por outras cidades\\n",
        "e anotar o que encontrar.\\p",
        "A gente se ve, {PLAYER}.$",
    )),
    "SlateportCity_Text_TakingBattleTentChallenge": (("SCOTT:", "BATTLE TENT"), (
        "SEU BENTO: {PLAYER}!\\p",
        "Vai testar a equipe na TENDA DE\\n",
        "BATALHA? Boa escolha.\\p",
        "Lugar assim mostra o que um\\n",
        "treinador faz sem roteiro.\\p",
        "Quero ouvir como foi depois.$",
    )),
}


def block_pattern(label: str) -> re.Pattern[str]:
    return re.compile(rf"(?ms)^{re.escape(label)}:\n(?P<body>.*?)(?=^[A-Za-z0-9_]+(?:::|:)(?:\n|$)|\Z)")


def visible_segments(payload: str) -> list[str]:
    cleaned = PLACEHOLDER_RE.sub("PLAYER", payload).replace("$", "")
    return [part.strip() for part in CONTROL_RE.split(cleaned)]


def validate_widths() -> None:
    for label, (_, payloads) in TARGETS.items():
        for payload in payloads:
            for segment in visible_segments(payload):
                if len(segment) > MAX_VISIBLE_WIDTH:
                    raise ValueError(f"{label}: {len(segment)} visible chars: {segment!r}")


def render(source: str) -> str:
    validate_widths()
    rendered = source
    for label, (markers, payloads) in TARGETS.items():
        pattern = block_pattern(label)
        matches = list(pattern.finditer(rendered))
        if len(matches) != 1:
            raise ValueError(f"{label}: expected one block, found {len(matches)}")
        body = matches[0].group("body")
        for marker in markers:
            if marker not in body:
                raise ValueError(f"{label}: source marker missing: {marker!r}")
        new_body = "".join(f'\t.string "{payload}"\n' for payload in payloads) + "\n"
        start, end = matches[0].span("body")
        rendered = rendered[:start] + new_body + rendered[end:]

    def mask(text: str) -> str:
        masked = text
        for label in TARGETS:
            match = block_pattern(label).search(masked)
            if not match:
                raise ValueError(f"{label}: cannot mask missing block")
            start, end = match.span("body")
            masked = masked[:start] + '\t.string "<ARAUNA_RENDERED_BLOCK>"\n\n' + masked[end:]
        return masked

    if mask(source) != mask(rendered):
        raise ValueError("non-dialogue structure changed while rendering Seu Bento in Porto do Sal")

    for token in ("SCOTT", "CIRO:", "BATTLE TENT", "other towns"):
        for label in TARGETS:
            if token in block_pattern(label).search(rendered).group("body"):
                raise ValueError(f"{label}: stale Seu Bento token survived: {token}")
    for label in TARGETS:
        body = block_pattern(label).search(rendered).group("body")
        if "SEU BENTO" not in body and label != "SlateportCity_Text_RegisteredScott":
            raise ValueError(f"{label}: expected SEU BENTO identity is missing")
    return rendered


def main() -> int:
    parser = argparse.ArgumentParser(description="Render the visible Scott surface in Porto do Sal as Seu Bento.")
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--in-place", action="store_true")
    args = parser.parse_args()
    if args.check and args.in_place:
        parser.error("use either --check or --in-place")

    rendered = render(TARGET.read_text(encoding="utf-8"))
    if args.check:
        print(f"Porto do Sal Seu Bento renderer OK: {len(TARGETS)} blocks validated.")
        return 0
    if args.in_place:
        TARGET.write_text(rendered, encoding="utf-8")
        return 0
    print(rendered, end="" if rendered.endswith("\n") else "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
