#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SHIPYARD_1F = ROOT / "data" / "maps" / "SlateportCity_SternsShipyard_1F" / "scripts.inc"
SHIPYARD_2F = ROOT / "data" / "maps" / "SlateportCity_SternsShipyard_2F" / "scripts.inc"
MAX_VISIBLE_WIDTH = 32
CONTROL_RE = re.compile(r"\\[npl]")
PLACEHOLDER_RE = re.compile(r"\{[^}]+\}")

TARGETS_1F: dict[str, tuple[tuple[str, ...], tuple[str, ...]]] = {
    "SlateportCity_SternsShipyard_1F_Text_CantMakeHeadsOrTails": (("heads or tails",), (
        "MESTRE: Se esta peca vai aqui...\\p",
        "entao aquela vai onde?\\p",
        "Projeto novo sempre parece facil\\n",
        "ate chegar ao casco.$",
    )),
    "SlateportCity_SternsShipyard_1F_Text_MeetDockDeliverToStern": (("projeto de M'BOI",), (
        "MESTRE: Voce trouxe as PECAS\\n",
        "OCEANICAS?\\p",
        "Eu cuido de casco e estrutura.\\n",
        "Procure o ENGENHEIRO no MUSEU.$",
    )),
    "SlateportCity_SternsShipyard_1F_Text_CouldYouFindStern": (("CAPT. STERN",), (
        "MESTRE: O ENGENHEIRO DO PORTO\\n",
        "deve estar no MUSEU.\\p",
        "Entregue as PECAS OCEANICAS a\\n",
        "ele, por favor.$",
    )),
    "SlateportCity_SternsShipyard_1F_Text_CouldUseAdviceFromVeteran": (("Shipbuilding is an art",), (
        "MESTRE: Construir navio e arte.\\p",
        "Nem tudo cabe numa planilha.\\p",
        "Preciso de marinheiro veterano\\n",
        "que conheca estas correntes.$",
    )),
    "SlateportCity_SternsShipyard_1F_Text_BrineyJoinedUs": (("MR. BRINEY", "veteran sailor"), (
        "MESTRE: Um MARINHEIRO VETERANO\\n",
        "veio nos ajudar.\\p",
        "Com a experiencia dele, o BARCO\\n",
        "DE LINHA esta tomando forma.$",
    )),
    "SlateportCity_SternsShipyard_1F_Text_FerryIsReady": (("MARE ALTA",), (
        "MESTRE: O BARCO DE LINHA ficou\\n",
        "pronto!\\p",
        "E o melhor projeto que fizemos.\\p",
        "Mas todo barco ensina como fazer\\n",
        "o proximo ainda melhor.$",
    )),
    "SlateportCity_SternsShipyard_1F_Text_DecidedToHelpDock": (("MR. BRINEY", "sea dog's"), (
        "VETERANO: {PLAYER}! Faz tempo!\\p",
        "Resolvi ajudar este estaleiro.\\p",
        "O MESTRE entende de projeto.\\n",
        "Eu conheco o mar e as correntes.\\p",
        "Juntos vamos fazer um bom barco.$",
    )),
    "SlateportCity_SternsShipyard_1F_Text_SeaIsLikeLivingThing": (("sea is like a living thing",), (
        "TECNICO: Estacao, clima, lua...\\p",
        "Tudo muda a forma do mar.\\p",
        "Quem trabalha aqui aprende cedo:\\n",
        "o mar nunca fica igual.$",
    )),
    "SlateportCity_SternsShipyard_1F_Text_GetSeasickEasily": (("seasick",), (
        "TECNICO: Eu enjoo facil no mar.\\p",
        "Por isso trabalho melhor aqui,\\n",
        "com os pes no chao.$",
    )),
}

TARGETS_2F: dict[str, tuple[tuple[str, ...], tuple[str, ...]]] = {
    "SlateportCity_SternsShipyard_2F_Text_ShipDesignMoreLikeBuilding": (("large ship", "big building"), (
        "TECNICO: Projetar navio grande\\n",
        "parece mais erguer um predio do\\n",
        "que montar um veiculo.$",
    )),
    "SlateportCity_SternsShipyard_2F_Text_FloatsBecauseBuoyancy": (("heavy iron", "buoyancy"), (
        "TECNICO: Muito metal flutuando,\\n",
        "nao e?\\p",
        "O casco desloca agua suficiente.\\n",
        "Chamamos isso de flutuacao.$",
    )),
}


def block_pattern(label: str) -> re.Pattern[str]:
    return re.compile(rf"(?ms)^{re.escape(label)}:\n(?P<body>.*?)(?=^[A-Za-z0-9_]+(?:::|:)(?:\n|$)|\Z)")


def visible_segments(payload: str) -> list[str]:
    cleaned = PLACEHOLDER_RE.sub("PLAYER", payload).replace("$", "")
    return [part.strip() for part in CONTROL_RE.split(cleaned)]


def validate_widths(targets: dict[str, tuple[tuple[str, ...], tuple[str, ...]]]) -> None:
    for label, (_, payloads) in targets.items():
        for payload in payloads:
            for segment in visible_segments(payload):
                if len(segment) > MAX_VISIBLE_WIDTH:
                    raise ValueError(f"{label}: {len(segment)} visible chars: {segment!r}")


def render(source: str, targets: dict[str, tuple[tuple[str, ...], tuple[str, ...]]], scope: str) -> str:
    validate_widths(targets)
    rendered = source
    for label, (markers, payloads) in targets.items():
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
        for label in targets:
            match = block_pattern(label).search(masked)
            if not match:
                raise ValueError(f"{label}: cannot mask missing block")
            start, end = match.span("body")
            masked = masked[:start] + '\t.string "<ARAUNA_RENDERED_BLOCK>"\n\n' + masked[end:]
        return masked

    if mask(source) != mask(rendered):
        raise ValueError(f"non-dialogue structure changed while rendering {scope}")
    return rendered


def render_1f(source: str) -> str:
    rendered = render(source, TARGETS_1F, "Porto do Sal shipyard 1F")
    for token in ("CAPT. STERN", "MR. BRINEY", "S.S. TIDAL", "HORIZONTE: O projeto"):
        for label in TARGETS_1F:
            if token in block_pattern(label).search(rendered).group("body"):
                raise ValueError(f"{label}: stale shipyard token survived: {token}")
    return rendered


def render_2f(source: str) -> str:
    return render(source, TARGETS_2F, "Porto do Sal shipyard 2F")


def main() -> int:
    parser = argparse.ArgumentParser(description="Render Porto do Sal shipyard and ferry-construction surface.")
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--in-place", action="store_true")
    args = parser.parse_args()
    if args.check and args.in_place:
        parser.error("use either --check or --in-place")

    one = render_1f(SHIPYARD_1F.read_text(encoding="utf-8"))
    two = render_2f(SHIPYARD_2F.read_text(encoding="utf-8"))

    if args.check:
        print(
            "Porto do Sal shipyard renderer OK: "
            f"{len(TARGETS_1F)} 1F blocks and {len(TARGETS_2F)} 2F blocks validated."
        )
        return 0
    if args.in_place:
        SHIPYARD_1F.write_text(one, encoding="utf-8")
        SHIPYARD_2F.write_text(two, encoding="utf-8")
        return 0
    print(one, end="" if one.endswith("\n") else "\n")
    print(two, end="" if two.endswith("\n") else "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
