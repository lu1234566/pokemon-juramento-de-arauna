#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ROOM9_PATH = ROOT / "data" / "maps" / "SeafloorCavern_Room9" / "scripts.inc"
MAX_VISIBLE_WIDTH = 32
CONTROL_RE = re.compile(r"\\[npl]")
PLACEHOLDER_RE = re.compile(r"\{[^}]+\}")

TARGETS: dict[str, tuple[tuple[str, ...], tuple[str, ...]]] = {
    "SeafloorCavern_Room9_Text_ArchieHoldItRightThere": (
        ("OTACILIO", "ARQUIVO VIVO"),
        ("OTACILIO: Pare ai.\\p", "Nao toque no nucleo do ARQUIVO.$"),
    ),
    "SeafloorCavern_Room9_Text_ArchieSoItWasYou": (
        ("OTACILIO", "M'BOI"),
        (
            "OTACILIO: Entao foi voce quem\\n",
            "abriu os arquivos de M'BOI.\\p",
            "Agora entende por que vim.$",
        ),
    ),
    "SeafloorCavern_Room9_Text_ArchieBeholdKyogre": (
        ("O ARQUIVO reage", "controle humano"),
        (
            "OTACILIO: Foi aqui que tudo\\n",
            "comecou.\\p",
            "Sob M'BOI existe uma corrente\\n",
            "que puxa VINCULOS de volta.$",
        ),
    ),
    "SeafloorCavern_Room9_Text_ArchieYouMustDisappear": (
        ("OTACILIO", "sofrimento"),
        (
            "OTACILIO: Se desligar agora,\\n",
            "perdemos a unica chance de\\n",
            "controlar o DESENCANTO.\\p",
            "Nao vou permitir.$",
        ),
    ),
    "SeafloorCavern_Room9_Text_ArchieDefeat": (
        ("OTACILIO", "Preservar tudo"),
        (
            "OTACILIO: Mesmo vencendo, voce\\n",
            "ainda nao entende o que esta\\n",
            "em jogo.$",
        ),
    ),
    "SeafloorCavern_Room9_Text_ArchieWithThisRedOrb": (
        ("sensores enlouquecem", "cavernas de M'BOI"),
        (
            "OTACILIO: O REGISTRO-MATRIZ\\n",
            "vai sincronizar o ARQUIVO com\\n",
            "essa corrente antiga.$",
        ),
    ),
    "SeafloorCavern_Room9_Text_RedOrbShinesByItself": (
        ("O ARQUIVO reage", "controle humano"),
        (
            "O REGISTRO-MATRIZ responde\\n",
            "sem comando.\\p",
            "O ARQUIVO perde o controle.$",
        ),
    ),
    "SeafloorCavern_Room9_Text_ArchieWhereDidKyogreGo": (
        ("sensores enlouquecem", "cavernas de M'BOI"),
        ("OTACILIO: Nao...\\p", "Eu nao ordenei isso.$"),
    ),
    "SeafloorCavern_Room9_Text_ArchieAMessageFromOutside": (
        ("OTACILIO", "M'BOI"),
        ("OTACILIO: Central, responda.\\p", "O que esta acontecendo la fora?$"),
    ),
    "SeafloorCavern_Room9_Text_ArchieWhatRainingTooHard": (
        ("sensores enlouquecem", "cavernas de M'BOI"),
        (
            "OTACILIO: Leituras subindo em\\n",
            "toda Arauna? Isso nao era\\n",
            "possivel.$",
        ),
    ),
    "SeafloorCavern_Room9_Text_ArchieWhyDidKyogreDisappear": (
        ("Gravacoes antigas", "exclusao"),
        (
            "OTACILIO: O ARQUIVO nao esta\\n",
            "contendo a corrente.\\p",
            "Ele a espalhou.$",
        ),
    ),
    "SeafloorCavern_Room9_Text_MaxieWhatHaveYouWrought": (
        ("OTACILIO e LUZIA", "escolha"),
        (
            "LUZIA: OTACILIO, o que voce fez?\\p",
            "Voce abriu M'BOI para toda\\n",
            "Arauna.$",
        ),
    ),
    "SeafloorCavern_Room9_Text_ArchieDontGetAllHighAndMighty": (
        ("Gravacoes antigas", "exclusao"),
        (
            "OTACILIO: Eu queria encerrar\\n",
            "a dor, nao espalha-la.\\p",
            "Isso nao deveria acontecer.$",
        ),
    ),
    "SeafloorCavern_Room9_Text_MaxieWeDontHaveTimeToArgue": (
        ("LUZIA", "problema nunca foi"),
        (
            "LUZIA: Nao temos tempo para\\n",
            "discutir culpa.\\p",
            "As duas correntes reagiram.$",
        ),
    ),
    "SeafloorCavern_Room9_Text_MaxieComeOnPlayer": (
        ("LUZIA", "HORIZONTE"),
        (
            "LUZIA: Venha.\\p",
            "Precisamos ver o que aconteceu\\n",
            "nas AGUAS DE M'BOI.$",
        ),
    ),
}


def block_pattern(label: str) -> re.Pattern[str]:
    return re.compile(rf'(?ms)^{re.escape(label)}:\n(?P<body>.*?)(?=^[A-Za-z0-9_]+(?:::|:)(?:\n|$)|\Z)')


def visible_segments(payload: str) -> list[str]:
    cleaned = PLACEHOLDER_RE.sub("", payload).replace("$", "")
    return [segment.strip() for segment in CONTROL_RE.split(cleaned)]


def validate_widths() -> None:
    for label, (_, payloads) in TARGETS.items():
        for payload in payloads:
            for segment in visible_segments(payload):
                if len(segment) > MAX_VISIBLE_WIDTH:
                    raise ValueError(f"{label}: {len(segment)} visible chars exceeds {MAX_VISIBLE_WIDTH}: {segment!r}")


def replace_blocks(source: str) -> str:
    rendered = source
    for label, (markers, payloads) in TARGETS.items():
        pattern = block_pattern(label)
        matches = list(pattern.finditer(rendered))
        if len(matches) != 1:
            raise ValueError(f"{label}: expected one block, found {len(matches)}")
        body = matches[0].group("body")
        if ".string" not in body:
            raise ValueError(f"{label}: target has no .string data")
        for marker in markers:
            if marker not in body:
                raise ValueError(f"{label}: missing source marker {marker!r}")
        new_body = "".join(f'\t.string "{payload}"\n' for payload in payloads) + "\n"
        start, end = matches[0].span("body")
        rendered = rendered[:start] + new_body + rendered[end:]
    return rendered


def mask(source: str) -> str:
    masked = source
    for label in TARGETS:
        match = block_pattern(label).search(masked)
        if not match:
            raise ValueError(f"{label}: cannot mask missing block")
        start, end = match.span("body")
        masked = masked[:start] + '\t.string "<ARAUANA_RENDERED_BLOCK>"\n\n' + masked[end:]
    return masked


def render(source: str) -> str:
    validate_widths()
    rendered = replace_blocks(source)
    if mask(source) != mask(rendered):
        raise ValueError("non-dialogue structure changed in Cavernas de M'Boi climax")
    for label, (_, payloads) in TARGETS.items():
        body = block_pattern(label).search(rendered).group("body")
        for payload in payloads:
            if f'\t.string "{payload}"' not in body:
                raise ValueError(f"{label}: rendered payload missing")
    return rendered


def main() -> int:
    parser = argparse.ArgumentParser(description="Render the Cavernas de M'Boi climax without changing Emerald progression wiring.")
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--in-place", action="store_true")
    args = parser.parse_args()
    if args.check and args.in_place:
        parser.error("use either --check or --in-place")

    source = ROOM9_PATH.read_text(encoding="utf-8")
    rendered = render(source)

    if args.check:
        print(f"M'Boi climax renderer OK: {len(TARGETS)} dialogue blocks validated.")
        return 0
    if args.in_place:
        ROOM9_PATH.write_text(rendered, encoding="utf-8")
        return 0
    print(rendered, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
