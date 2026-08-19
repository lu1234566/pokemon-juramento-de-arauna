#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_INPUT = ROOT / "data" / "maps" / "PetalburgWoods" / "scripts.inc"
MAX_VISIBLE_WIDTH = 32

TARGETS: dict[str, tuple[tuple[str, ...], tuple[str, ...]]] = {
    "PetalburgWoods_Text_NotAOneToBeFound": (
        ("Not a one to be found",),
        ("Nada...\\n", "Ainda nada por aqui.$"),
    ),
    "PetalburgWoods_Text_HaveYouSeenShroomish": (
        ("SHROOMISH", "I really love that POKéMON"),
        (
            "Ola. Viu algum POKéMON raro\\n",
            "por aqui?\\p",
            "Estou acompanhando a fauna\\n",
            "desta mata.$",
        ),
    ),
    "PetalburgWoods_Text_IWasGoingToAmbushYou": (
        ("ambush you", "PETALBURG WOODS"),
        (
            "Eu ia pegar voce de surpresa,\\n",
            "mas voce demorou demais.\\p",
            "Cansei de esperar. Vim ate aqui.$",
        ),
    ),
    "PetalburgWoods_Text_HandOverThosePapers": (
        ("DEVON RESEARCHER", "Hand over those papers"),
        ("Voce, PESQUISADOR!\\p", "Entregue esses documentos!$"),
    ),
    "PetalburgWoods_Text_YouHaveToHelpMe": (
        ("POKéMON TRAINER", "help me"),
        ("Ei! Voce e treinador, nao e?\\p", "Preciso de ajuda!$"),
    ),
    "PetalburgWoods_Text_NoOneCrossesTeamAqua": (
        ("CONSORCIO HORIZONTE", "battle me"),
        (
            "Vai protege-lo?\\p",
            "Quem interfere no CONSORCIO\\n",
            "HORIZONTE aprende rapido.\\p",
            "Vamos resolver isso numa luta!$",
        ),
    ),
    "PetalburgWoods_Text_YoureKiddingMe": (
        ("You're kidding me",),
        ("Nao pode ser... Voce e forte!$",),
    ),
    "PetalburgWoods_Text_YouveGotSomeNerve": (
        ("CONSORCIO HORIZONTE", "RUSTBORO"),
        (
            "Tsc... Voce tem coragem de\\n",
            "mexer com o CONSORCIO HORIZONTE.\\p",
            "Hoje eu recuo.\\p",
            "Temos trabalho na SERRA DO UIVO.$",
        ),
    ),
    "PetalburgWoods_Text_ThatWasAwfullyClose": (
        ("awfully close", "GREAT BALL"),
        (
            "Foi por pouco.\\p",
            "Obrigado. Esses documentos sao\\n",
            "importantes.\\p",
            "Pegue isto como agradecimento.$",
        ),
    ),
    "PetalburgWoods_Text_TeamAquaAfterSomethingInRustboro": (
        ("CONSORCIO HORIZONTE", "RUSTBORO"),
        (
            "Ele disse que o CONSORCIO\\n",
            "HORIZONTE esta atras de algo\\n",
            "na SERRA DO UIVO, certo?$",
        ),
    ),
    "PetalburgWoods_Text_ICantBeWastingTime": (
        ("crisis", "wasting time"),
        ("Isso e serio.\\n", "Preciso chegar la.$"),
    ),
    "PetalburgWoods_Text_YoureLoadedWithItems": (
        ("loaded with items", "GREAT BALL"),
        ("Sua BOLSA esta cheia.\\n", "Nao consigo entregar isto.$"),
    ),
}

BLOCK_RE_TEMPLATE = r'(?m)^{label}:\n(?P<body>(?:\t\.string "[^\n]*"\n)+)'
CONTROL_RE = re.compile(r"\\[npl]")
PLACEHOLDER_RE = re.compile(r"\{[^}]+\}")


def visible_segments(payload: str) -> list[str]:
    cleaned = PLACEHOLDER_RE.sub("", payload).replace("$", "")
    return [segment.strip() for segment in CONTROL_RE.split(cleaned)]


def validate_widths() -> None:
    for label, (_, payloads) in TARGETS.items():
        for payload in payloads:
            for segment in visible_segments(payload):
                if len(segment) > MAX_VISIBLE_WIDTH:
                    raise ValueError(
                        f"{label}: visible segment is {len(segment)} chars, max {MAX_VISIBLE_WIDTH}: {segment!r}"
                    )


def render(source: str) -> str:
    rendered = source
    for label, (expected_markers, payloads) in TARGETS.items():
        pattern = re.compile(BLOCK_RE_TEMPLATE.format(label=re.escape(label)))
        matches = list(pattern.finditer(rendered))
        if len(matches) != 1:
            raise ValueError(f"{label}: expected one .string block, found {len(matches)}")
        body = matches[0].group("body")
        for marker in expected_markers:
            if marker not in body:
                raise ValueError(f"{label}: expected source marker not found: {marker!r}")
        new_body = "".join(f'\t.string "{payload}"\n' for payload in payloads)
        start, end = matches[0].span("body")
        rendered = rendered[:start] + new_body + rendered[end:]
    return rendered


def validate_rendered(rendered: str) -> None:
    forbidden = ("PETALBURG WOODS", "DEVON RESEARCHER", "RUSTBORO", "TEAM AQUA")
    for label, (_, payloads) in TARGETS.items():
        pattern = re.compile(BLOCK_RE_TEMPLATE.format(label=re.escape(label)))
        match = pattern.search(rendered)
        if not match:
            raise ValueError(f"{label}: rendered block missing")
        body = match.group("body")
        for payload in payloads:
            line = f'\t.string "{payload}"'
            if line not in body:
                raise ValueError(f"{label}: rendered line missing: {line}")
        for token in forbidden:
            if token in body:
                raise ValueError(f"{label}: legacy visible token survived: {token}")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Render Arauna's first Consorcio Horizonte forest encounter without changing event wiring."
    )
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--in-place", action="store_true")
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()

    if args.output and args.in_place:
        parser.error("use either --output or --in-place, not both")

    validate_widths()
    source = args.input.read_text(encoding="utf-8")
    rendered = render(source)
    validate_rendered(rendered)

    if args.check:
        print(f"Horizonte forest renderer OK: {len(TARGETS)} dialogue blocks validated.")
        return 0

    if args.in_place:
        args.input.write_text(rendered, encoding="utf-8")
    elif args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered, encoding="utf-8")
    else:
        print(rendered, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
