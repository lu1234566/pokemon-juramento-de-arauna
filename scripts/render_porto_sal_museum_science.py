#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MUSEUM_1F = ROOT / "data" / "maps" / "SlateportCity_OceanicMuseum_1F" / "scripts.inc"
MUSEUM_2F = ROOT / "data" / "maps" / "SlateportCity_OceanicMuseum_2F" / "scripts.inc"
MAX_VISIBLE_WIDTH = 32
CONTROL_RE = re.compile(r"\\[npl]")
PLACEHOLDER_RE = re.compile(r"\{[^}]+\}")

TARGETS_1F: dict[str, tuple[tuple[str, ...], tuple[str, ...]]] = {
    "SlateportCity_OceanicMuseum_1F_Text_WhirlpoolExperiment": (("blue fluid", "WHIRLPOOL"), (
        "Um fluido azul gira dentro de\\n",
        "um recipiente de vidro.\\p",
        "EXPERIMENTO: criar um redemoinho\\n",
        "artificial usando fluxo de ar.$",
    )),
    "SlateportCity_OceanicMuseum_1F_Text_WaterfallExperiment": (("red ball", "WATERFALL"), (
        "Uma esfera vermelha sobe e desce\\n",
        "dentro de um recipiente.\\p",
        "EXPERIMENTO: simular uma queda\\n",
        "d'agua usando flutuacao.$",
    )),
    "SlateportCity_OceanicMuseum_1F_Text_OceanSoilDisplay": (("soil from the ocean", "sedimentary"), (
        "AMOSTRA: SOLO OCEANICO\\p",
        "Restos de vida se acumulam no\\n",
        "fundo do mar por muitos anos.\\p",
        "As camadas de sedimento ajudam\\n",
        "a reconstruir o passado.$",
    )),
    "SlateportCity_OceanicMuseum_1F_Text_BeachSandDisplay": (("beach sand", "Stones from mountains"), (
        "AMOSTRA: AREIA COSTEIRA\\p",
        "Pedras descem dos montes pelos\\n",
        "rios e se desgastam no caminho.\\p",
        "Os graos menores acabam formando\\n",
        "as praias.$",
    )),
    "SlateportCity_OceanicMuseum_1F_Text_OceanicMinifact1": (("OCEANIC MINIFACT 1", "seawater blue"), (
        "MINIFATO OCEANICO 1\\p",
        "Por que o mar parece azul?\\p",
        "A agua absorve varias cores da\\n",
        "luz antes do azul.\\p",
        "Por isso vemos mais azul.$",
    )),
    "SlateportCity_OceanicMuseum_1F_Text_OceanicMinifact2": (("OCEANIC MINIFACT 2", "sea salty"), (
        "MINIFATO OCEANICO 2\\p",
        "Por que o mar e salgado?\\p",
        "A chuva carrega sais das rochas\\n",
        "para rios e oceanos.\\p",
        "Com o tempo, eles se concentram.$",
    )),
    "SlateportCity_OceanicMuseum_1F_Text_OceanicMinifact3": (("OCEANIC MINIFACT 3", "70%"), (
        "MINIFATO OCEANICO 3\\p",
        "O que ocupa mais: mar ou terra?\\p",
        "O mar cobre cerca de 70% do\\n",
        "planeta.$",
    )),
    "SlateportCity_OceanicMuseum_1F_Text_FossilDisplay": (("fossil", "ripple mark"), (
        "FOSSIL: MARCA DE ONDA\\p",
        "Correntes deixam pequenos sulcos\\n",
        "no solo do fundo do mar.\\p",
        "Quando endurecem em rocha, esses\\n",
        "sulcos podem virar fosseis.$",
    )),
    "SlateportCity_OceanicMuseum_1F_Text_DepthMeasuringMachine": (("strange machine", "measuring the depth"), (
        "MEDIDOR DE PROFUNDIDADE\\p",
        "Uma maquina gira sob a cupula.\\p",
        "Ela usa ecos para estimar a\\n",
        "distancia ate o fundo.$",
    )),
}

TARGETS_2F: dict[str, tuple[tuple[str, ...], tuple[str, ...]]] = {
    "SlateportCity_OceanicMuseum_2F_Text_WaterQualitySample1": (("WATER QUALITY SAMPLE 1",), (
        "AMOSTRA DE AGUA 1\\p",
        "O mar e conectado, mas a agua\\n",
        "muda de uma regiao para outra.$",
    )),
    "SlateportCity_OceanicMuseum_2F_Text_WaterQualitySample2": (("WATER QUALITY SAMPLE 2",), (
        "AMOSTRA DE AGUA 2\\p",
        "A quantidade de sal tambem muda\\n",
        "entre diferentes regioes.$",
    )),
    "SlateportCity_OceanicMuseum_2F_Text_PressureExperiment": (("rubber ball", "pressure"), (
        "EXPERIMENTO DE PRESSAO\\p",
        "Uma esfera de borracha expande\\n",
        "e encolhe.\\p",
        "Quanto maior a profundidade,\\n",
        "maior a pressao da agua.$",
    )),
    "SlateportCity_OceanicMuseum_2F_Text_HoennModel": (("MODEL OF ARAUNA REGION", "VILA AMANHECER"), (
        "MODELO DA REGIAO DE ARAUNA\\p",
        "Uma miniatura mostra cidades,\\n",
        "rios, serras e rotas costeiras.$",
    )),
    "SlateportCity_OceanicMuseum_2F_Text_DeepSeawaterDisplay": (("flow of seawater", "temperature and salinity"), (
        "CORRENTES PROFUNDAS\\p",
        "Perto do fundo, temperatura e\\n",
        "salinidade movem grandes massas\\n",
        "de agua.$",
    )),
    "SlateportCity_OceanicMuseum_2F_Text_SurfaceSeawaterDisplay": (("Toward the surface", "winds"), (
        "CORRENTES DE SUPERFICIE\\p",
        "Perto da superficie, o vento\\n",
        "empurra grandes fluxos de agua.$",
    )),
    "SlateportCity_OceanicMuseum_2F_Text_SSTidalReplica": (("S.S. TIDAL", "STERN'S SHIPYARD"), (
        "REPLICA: BARCO DE LINHA\\p",
        "Modelo do barco construido para\\n",
        "ligar os portos de Arauna.$",
    )),
    "SlateportCity_OceanicMuseum_2F_Text_SubmarineReplica": (("sensores detectam", "DESENCANTO"), (
        "REPLICA: SUBMERSIVEL\\p",
        "Veiculo de pesquisa feito para\\n",
        "alcancar grandes profundidades.$",
    )),
    "SlateportCity_OceanicMuseum_2F_Text_SumbersibleReplica": (("SUBMERSIBLE POD", "unmanned"), (
        "REPLICA: SONDA SUBMERSIVEL\\p",
        "Sonda compacta e nao tripulada\\n",
        "para explorar o fundo do mar.$",
    )),
    "SlateportCity_OceanicMuseum_2F_Text_SSAnneReplica": (("S.S. ANNE", "luxury liner"), (
        "REPLICA: NAVIO HISTORICO\\p",
        "Modelo de antigo transatlantico\\n",
        "que cruzava oceanos inteiros.$",
    )),
    "SlateportCity_OceanicMuseum_2F_Text_RemindsMeOfAbandonedShip": (("ABANDONED SHIP", "PORTO DAS REDES"), (
        "VISITANTE: Esse modelo me lembra\\n",
        "um navio encalhado na costa.$",
    )),
    "SlateportCity_OceanicMuseum_2F_Text_DontRunInMuseum": (("Don't you dare run",), (
        "VISITANTE: Nada de correr dentro\\n",
        "do MUSEU, ouviu?$",
    )),
    "SlateportCity_OceanicMuseum_2F_Text_WantToRideSubmarine": (("Nao somos soldados",), (
        "VISITANTE: Eu queria viajar num\\n",
        "submersivel de pesquisa.\\p",
        "Deve ser assustador e incrivel.$",
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
    rendered = render(source, TARGETS_1F, "Porto do Sal museum 1F science")
    for token in ("WHIRLPOOL artificially", "OCEANIC MINIFACT", "ancient past is revealed"):
        for label in TARGETS_1F:
            if token in block_pattern(label).search(rendered).group("body"):
                raise ValueError(f"{label}: stale 1F science token survived: {token}")
    return rendered


def render_2f(source: str) -> str:
    rendered = render(source, TARGETS_2F, "Porto do Sal museum 2F science")
    for token in ("LITTLEROOT", "S.S. TIDAL", "S.S. ANNE", "ABANDONED SHIP", "DEWFORD"):
        for label in TARGETS_2F:
            if token in block_pattern(label).search(rendered).group("body"):
                raise ValueError(f"{label}: stale 2F museum token survived: {token}")
    return rendered


def main() -> int:
    parser = argparse.ArgumentParser(description="Render Porto do Sal museum scientific exhibits and remaining 2F patrons.")
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--in-place", action="store_true")
    args = parser.parse_args()
    if args.check and args.in_place:
        parser.error("use either --check or --in-place")

    one = render_1f(MUSEUM_1F.read_text(encoding="utf-8"))
    two = render_2f(MUSEUM_2F.read_text(encoding="utf-8"))

    if args.check:
        print(
            "Porto do Sal museum science renderer OK: "
            f"{len(TARGETS_1F)} 1F blocks and {len(TARGETS_2F)} 2F blocks validated."
        )
        return 0
    if args.in_place:
        MUSEUM_1F.write_text(one, encoding="utf-8")
        MUSEUM_2F.write_text(two, encoding="utf-8")
        return 0
    print(one, end="" if one.endswith("\n") else "\n")
    print(two, end="" if two.endswith("\n") else "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
