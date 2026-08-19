#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CITY_PATH = ROOT / "data" / "maps" / "SlateportCity" / "scripts.inc"
HARBOR_PATH = ROOT / "data" / "maps" / "SlateportCity_Harbor" / "scripts.inc"
MAX_VISIBLE_WIDTH = 32
CONTROL_RE = re.compile(r"\\[npl]")
PLACEHOLDER_RE = re.compile(r"\{[^}]+\}")

SOURCE_SIGNATURES = (
    "CAPT. STERN",
    "GABBY:",
    "huge discovery",
    "HORIZONTE: Nao somos soldados",
    "What was that all about",
    "projeto de M'BOI",
    "Please, come with me",
    "Those thugs",
    "OTACILIO: Eu vi o que uma",
    "sensores detectam",
)

CITY_TARGETS: dict[str, tuple[str, ...]] = {
    "SlateportCity_Text_SternMoveAheadWithExploration": (
        "ENGENHEIRO: Os novos mapas\\n",
        "confirmam cavernas sob M'BOI.\\p",
        "O submersivel consegue chegar\\n",
        "ate elas.$",
    ),
    "SlateportCity_Text_GabbyWonderfulThanksForInterview": (
        "REPORTER: Entao a expedicao\\n",
        "continua! Obrigada pelo tempo.\\p",
        "Voltaremos quando houver novas\\n",
        "descobertas.$",
    ),
    "SlateportCity_Text_SternWhewFirstInterview": (
        "ENGENHEIRO: Ufa...\\p",
        "Primeira entrevista ao vivo.\\n",
        "Prefiro encarar o fundo do mar.$",
    ),
    "SlateportCity_Text_OhPlayerWeMadeDiscovery": (
        "ENGENHEIRO: {PLAYER}, chegou\\n",
        "na hora.\\p",
        "As leituras sob M'BOI subiram\\n",
        "junto com os ultimos tremores.\\p",
        "Ha uma corrente de VINCULO\\n",
        "se movendo nas cavernas.$",
    ),
    "SlateportCity_Text_AquaWillAssumeControlOfSubmarine": (
        "HORIZONTE: PROTOCOLO DE\\n",
        "EMERGENCIA.\\p",
        "O submersivel sera requisitado\\n",
        "para conter a anomalia em M'BOI.\\p",
        "Equipe do porto, nao interfira.$",
    ),
    "SlateportCity_Text_SternWhatWasAllThat": (
        "ENGENHEIRO: Requisitado?\\p",
        "Essa voz veio do porto!$",
    ),
    "SlateportCity_Text_FromHarborTryingToTakeSub": (
        "FUNCIONARIO: Engenheiro!\\p",
        "O HORIZONTE entrou no hangar.\\n",
        "Eles vao levar o submersivel!$",
    ),
    "SlateportCity_Text_PleaseComeWithMe": (
        "ENGENHEIRO: {PLAYER}, comigo!$",
    ),
}

HARBOR_TARGETS: dict[str, tuple[str, ...]] = {
    "SlateportCity_Harbor_Text_SameThugsTriedToRobAtMuseum": (
        "ENGENHEIRO: HORIZONTE de novo...\\p",
        "Vi os mesmos uniformes no caso\\n",
        "dos equipamentos do MUSEU.$",
    ),
    "SlateportCity_Harbor_Text_ArchieYouAgainHideoutInLilycove": (
        "OTACILIO: Voce de novo.\\p",
        "Este submersivel e o unico que\\n",
        "alcanca as CAVERNAS DE M'BOI.\\p",
        "Primeiro vamos ao ARQUIVO\\n",
        "CENTRAL concluir a carga.\\p",
        "Depois seguimos para M'BOI.\\p",
        "Nao temos tempo para esperar\\n",
        "permissao.$",
    ),
    "SlateportCity_Harbor_Text_CaptSternWhyStealMySubmarine": (
        "ENGENHEIRO: Ele podia ter pedido.\\p",
        "O submersivel foi feito para\\n",
        "pesquisa, nao para uma faccao.\\p",
        "Agora precisamos segui-los.$",
    ),
    "SlateportCity_Harbor_Text_TeamAquaLeftNeedDive": (
        "ENGENHEIRO: O submersivel deixou\\n",
        "o ARQUIVO CENTRAL e mergulhou.\\p",
        "A rota segue para M'BOI.$",
    ),
    "SlateportCity_Harbor_Text_NeedDiveToCatchSub": (
        "ENGENHEIRO: Para alcancar as\\n",
        "CAVERNAS DE M'BOI, voce precisa\\n",
        "mergulhar em mar aberto.\\p",
        "Use DIVE quando estiver pronto.$",
    ),
}


def block_pattern(label: str) -> re.Pattern[str]:
    return re.compile(rf"(?ms)^{re.escape(label)}:\n(?P<body>.*?)(?=^[A-Za-z0-9_]+(?:::|:)(?:\n|$)|\Z)")


def visible_segments(payload: str) -> list[str]:
    cleaned = PLACEHOLDER_RE.sub("PLAYER", payload).replace("$", "")
    return [part.strip() for part in CONTROL_RE.split(cleaned)]


def validate_widths(targets: dict[str, tuple[str, ...]]) -> None:
    for label, payloads in targets.items():
        for payload in payloads:
            for segment in visible_segments(payload):
                if len(segment) > MAX_VISIBLE_WIDTH:
                    raise ValueError(f"{label}: {len(segment)} visible chars: {segment!r}")


def replace_blocks(source: str, targets: dict[str, tuple[str, ...]]) -> str:
    rendered = source
    for label, payloads in targets.items():
        pattern = block_pattern(label)
        matches = list(pattern.finditer(rendered))
        if len(matches) != 1:
            raise ValueError(f"{label}: expected one block, found {len(matches)}")
        body = matches[0].group("body")
        if ".string" not in body:
            raise ValueError(f"{label}: target is not text")
        if not any(signature in body for signature in SOURCE_SIGNATURES):
            raise ValueError(f"{label}: source no longer matches known pre-curation surface")
        new_body = "".join(f'\t.string "{payload}"\n' for payload in payloads) + "\n"
        start, end = matches[0].span("body")
        rendered = rendered[:start] + new_body + rendered[end:]
    return rendered


def mask_blocks(source: str, labels: tuple[str, ...]) -> str:
    masked = source
    for label in labels:
        match = block_pattern(label).search(masked)
        if not match:
            raise ValueError(f"{label}: cannot mask missing block")
        start, end = match.span("body")
        masked = masked[:start] + '\t.string "<ARAUNA_RENDERED_BLOCK>"\n\n' + masked[end:]
    return masked


def render(source: str, targets: dict[str, tuple[str, ...]]) -> str:
    validate_widths(targets)
    rendered = replace_blocks(source, targets)
    if mask_blocks(source, tuple(targets)) != mask_blocks(rendered, tuple(targets)):
        raise ValueError("non-dialogue structure changed while rendering Porto do Sal")
    return rendered


def render_city(source: str) -> str:
    rendered = render(source, CITY_TARGETS)
    for token in ("CAPT. STERN", "GABBY:", "huge discovery", "Please, come with me"):
        for label in CITY_TARGETS:
            body = block_pattern(label).search(rendered).group("body")
            if token in body:
                raise ValueError(f"{label}: stale city token survived: {token}")
    return rendered


def render_harbor(source: str) -> str:
    rendered = render(source, HARBOR_TARGETS)
    for token in ("CAPT. STERN", "LILYCOVE", "Those thugs", "sensores detectam VINCULOS"):
        for label in HARBOR_TARGETS:
            body = block_pattern(label).search(rendered).group("body")
            if token in body:
                raise ValueError(f"{label}: stale harbor token survived: {token}")
    return rendered


def main() -> int:
    parser = argparse.ArgumentParser(description="Render Porto do Sal submarine announcement, requisition and M'Boi pursuit.")
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--in-place", action="store_true")
    args = parser.parse_args()
    if args.check and args.in_place:
        parser.error("use either --check or --in-place")

    city = render_city(CITY_PATH.read_text(encoding="utf-8"))
    harbor = render_harbor(HARBOR_PATH.read_text(encoding="utf-8"))

    if args.check:
        print(
            "Porto do Sal submarine renderer OK: "
            f"{len(CITY_TARGETS)} city blocks and {len(HARBOR_TARGETS)} harbor blocks validated."
        )
        return 0
    if args.in_place:
        CITY_PATH.write_text(city, encoding="utf-8")
        HARBOR_PATH.write_text(harbor, encoding="utf-8")
        return 0
    print(f"===== {CITY_PATH.relative_to(ROOT)} =====")
    print(city, end="" if city.endswith("\n") else "\n")
    print(f"===== {HARBOR_PATH.relative_to(ROOT)} =====")
    print(harbor, end="" if harbor.endswith("\n") else "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
