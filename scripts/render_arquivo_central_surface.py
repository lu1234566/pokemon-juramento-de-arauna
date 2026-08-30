#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
B1F_PATH = ROOT / "data" / "maps" / "AquaHideout_B1F" / "scripts.inc"
B2F_PATH = ROOT / "data" / "maps" / "AquaHideout_B2F" / "scripts.inc"
MAX_VISIBLE_WIDTH = 32

CONTROL_RE = re.compile(r"\\[npl]")
PLACEHOLDER_RE = re.compile(r"\{[^}]+\}")

B1F_TARGETS: dict[str, tuple[tuple[str, ...], tuple[str, ...]]] = {
    "AquaHideout_B1F_Text_Grunt2Intro": (
        ("projeto de M'BOI", "relatorios"),
        ("HORIZONTE: Voce abriu a pasta\\n", "M'BOI. Isso nao devia acontecer.$"),
    ),
    "AquaHideout_B1F_Text_Grunt2Defeat": (
        ("OTACILIO", "prisao"),
        (
            "HORIZONTE: ANAHI ajudou a criar\\n",
            "os primeiros sensores de\\n",
            "VINCULO.$",
        ),
    ),
    "AquaHideout_B1F_Text_Grunt2PostBattle": (
        ("Nao somos soldados", "ordens"),
        (
            "HORIZONTE: Os relatorios chamam\\n",
            "M'BOI de falha operacional.\\p",
            "Nao parece palavra suficiente.$",
        ),
    ),
    "AquaHideout_B1F_Text_Grunt3Intro": (
        ("OTACILIO", "prisao"),
        ("HORIZONTE: O pai de CIRO esta\\n", "nessa lista de mortos.$"),
    ),
    "AquaHideout_B1F_Text_Grunt3Defeat": (
        ("Nao somos soldados", "ordens"),
        ("HORIZONTE: CIRO recebeu apoio\\n", "anos depois. Nao sei o que sabe.$"),
    ),
    "AquaHideout_B1F_Text_Grunt3PostBattle": (
        ("ARQUIVO VIVO", "trauma"),
        ("HORIZONTE: Se ele descobrir por\\n", "voce, tambem sera culpa nossa.$"),
    ),
    "AquaHideout_B1F_Text_Grunt5Intro": (
        ("Nao somos soldados", "ordens"),
        ("HORIZONTE: ELIAS aprovou parte\\n", "dos protocolos de M'BOI.$"),
    ),
    "AquaHideout_B1F_Text_Grunt5Defeat": (
        ("ARQUIVO VIVO", "trauma"),
        ("HORIZONTE: Culpa nao apaga uma\\n", "assinatura. Nem explica tudo.$"),
    ),
    "AquaHideout_B1F_Text_Grunt5PostBattle": (
        ("ARQUIVO VIVO", "trauma"),
        ("HORIZONTE: Ha paginas inteiras\\n", "so de aprovacoes e ressalvas.$"),
    ),
    "AquaHideout_B1F_Text_Grunt7Intro": (
        ("ARQUIVO VIVO", "trauma"),
        ("HORIZONTE: OTACILIO perdeu\\n", "familia em M'BOI.$"),
    ),
    "AquaHideout_B1F_Text_Grunt7Defeat": (
        ("Nao somos soldados", "ordens"),
        (
            "HORIZONTE: Depois de M'BOI,\\n",
            "o ARQUIVO VIVO virou\\n",
            "projeto de vida.$",
        ),
    ),
    "AquaHideout_B1F_Text_Grunt7PostBattle": (
        ("projeto de M'BOI", "relatorios"),
        ("HORIZONTE: Entender a dor dele\\n", "nao justifica todas as ordens.$"),
    ),
}

B2F_TARGETS: dict[str, tuple[tuple[str, ...], tuple[str, ...]]] = {
    "AquaHideout_B2F_Text_MattIntro": (
        ("Got here already", "GRUNTS", "pulverize"),
        (
            "BRENO: Chegou mais cedo\\n",
            "do que o previsto.\\p",
            "O embarque ja comecou.\\p",
            "Meu trabalho e atrasar voce.$",
        ),
    ),
    "AquaHideout_B2F_Text_MattDefeat": (
        ("So, I lost",),
        ("BRENO: Certo...\\n", "Nao consigo ganhar mais tempo.$"),
    ),
    "AquaHideout_B2F_Text_OurBossGotThroughHisPreparations": (
        ("ARQUIVO VIVO", "trauma"),
        (
            "BRENO: Tarde demais.\\p",
            "OTACILIO terminou a carga\\n",
            "e embarcou para M'BOI.$",
        ),
    ),
    "AquaHideout_B2F_Text_MattPostBattle": (
        ("Our BOSS", "BAIA DAS LUZES", "cave under the sea"),
        (
            "BRENO: Se vai persegui-lo,\\n",
            "siga alem da BAIA DAS LUZES.\\p",
            "As cavernas ficam sob o mar.$",
        ),
    ),
    "AquaHideout_B2F_Text_Grunt4Intro": (
        ("sensores detectam", "DESENCANTO"),
        (
            "HORIZONTE: Estamos apagando\\n",
            "copias locais. O ARQUIVO segue\\n",
            "no submersivel.$",
        ),
    ),
    "AquaHideout_B2F_Text_Grunt4Defeat": (
        ("Nao somos soldados", "ordens"),
        ("HORIZONTE: Nao da mais para\\n", "fingir que isso e manutencao.$"),
    ),
    "AquaHideout_B2F_Text_Grunt4PostBattle": (
        ("projeto de M'BOI", "relatorios"),
        ("HORIZONTE: Os servidores de\\n", "M'BOI foram carregados primeiro.$"),
    ),
    "AquaHideout_B2F_Text_Grunt6Intro": (
        ("Nao somos soldados", "ordens"),
        ("HORIZONTE: O protocolo manda\\n", "evacuar dados e destruir chaves.$"),
    ),
    "AquaHideout_B2F_Text_Grunt6Defeat": (
        ("sensores detectam", "DESENCANTO"),
        ("HORIZONTE: Voce quer provas.\\p", "Eu entendo.$"),
    ),
    "AquaHideout_B2F_Text_Grunt6PostBattle": (
        ("OTACILIO", "prisao"),
        (
            "HORIZONTE: A rota do submersivel\\n",
            "termina nas CAVERNAS DE M'BOI.$",
        ),
    ),
    "AquaHideout_B2F_Text_Grunt8Intro": (
        ("ARQUIVO VIVO", "trauma"),
        (
            "HORIZONTE: OTACILIO levou\\n",
            "a copia integral dos registros\\n",
            "de VINCULO.$",
        ),
    ),
    "AquaHideout_B2F_Text_Grunt8Defeat": (
        ("Nao somos soldados", "ordens"),
        ("HORIZONTE: Nem todos aqui sabem\\n", "o que aconteceu em M'BOI.$"),
    ),
    "AquaHideout_B2F_Text_Grunt8PostBattle": (
        ("sensores detectam", "DESENCANTO"),
        (
            "HORIZONTE: Quando a verdade\\n",
            "depende de permissao interna,\\n",
            "ela ja esta presa.$",
        ),
    ),
}


def block_pattern(label: str) -> re.Pattern[str]:
    return re.compile(
        rf'(?ms)^{re.escape(label)}:\n(?P<body>.*?)(?=^[A-Za-z0-9_]+(?:::|:)(?:\n|$)|\Z)'
    )


def visible_segments(payload: str) -> list[str]:
    cleaned = PLACEHOLDER_RE.sub("", payload).replace("$", "")
    return [segment.strip() for segment in CONTROL_RE.split(cleaned)]


def validate_widths(targets: dict[str, tuple[tuple[str, ...], tuple[str, ...]]]) -> None:
    for label, (_, payloads) in targets.items():
        for payload in payloads:
            for segment in visible_segments(payload):
                if len(segment) > MAX_VISIBLE_WIDTH:
                    raise ValueError(
                        f"{label}: visible segment is {len(segment)} chars, max {MAX_VISIBLE_WIDTH}: {segment!r}"
                    )


def replace_text_blocks(
    source: str,
    targets: dict[str, tuple[tuple[str, ...], tuple[str, ...]]],
) -> str:
    rendered = source
    for label, (markers, payloads) in targets.items():
        pattern = block_pattern(label)
        matches = list(pattern.finditer(rendered))
        if len(matches) != 1:
            raise ValueError(f"{label}: expected one text block, found {len(matches)}")
        body = matches[0].group("body")
        if ".string" not in body:
            raise ValueError(f"{label}: target body does not contain .string data")
        for marker in markers:
            if marker not in body:
                raise ValueError(f"{label}: expected source marker not found: {marker!r}")
        new_body = "".join(f'\t.string "{payload}"\n' for payload in payloads) + "\n"
        start, end = matches[0].span("body")
        rendered = rendered[:start] + new_body + rendered[end:]
    return rendered


def mask_targets(source: str, targets: dict[str, tuple[tuple[str, ...], tuple[str, ...]]]) -> str:
    masked = source
    for label in targets:
        match = block_pattern(label).search(masked)
        if not match:
            raise ValueError(f"{label}: cannot mask missing block")
        start, end = match.span("body")
        masked = masked[:start] + '\t.string "<ARAUANA_RENDERED_BLOCK>"\n\n' + masked[end:]
    return masked


def render_scene(
    source: str,
    targets: dict[str, tuple[tuple[str, ...], tuple[str, ...]]],
    forbidden: tuple[str, ...],
) -> str:
    validate_widths(targets)
    rendered = replace_text_blocks(source, targets)
    if mask_targets(source, targets) != mask_targets(rendered, targets):
        raise ValueError("non-dialogue structure changed while rendering Arquivo Central")

    for label, (_, payloads) in targets.items():
        match = block_pattern(label).search(rendered)
        if not match:
            raise ValueError(f"{label}: rendered block missing")
        body = match.group("body")
        for payload in payloads:
            if f'\t.string "{payload}"' not in body:
                raise ValueError(f"{label}: rendered payload missing: {payload!r}")
        for token in forbidden:
            if token in body:
                raise ValueError(f"{label}: legacy visible token survived: {token}")
    return rendered


def render_b1f(source: str) -> str:
    return render_scene(source, B1F_TARGETS, ("Nao somos soldados", "trauma de identidade", "consta nos relatorios"))


def render_b2f(source: str) -> str:
    return render_scene(
        source,
        B2F_TARGETS,
        ("Our BOSS", "LILYCOVE", "Got here already", "pulverize", "cave under the sea"),
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="Render the deeper Arquivo Central story surface without changing Emerald event wiring.")
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--in-place", action="store_true")
    args = parser.parse_args()

    if args.check and args.in_place:
        parser.error("use either --check or --in-place")

    originals = {
        B1F_PATH: B1F_PATH.read_text(encoding="utf-8"),
        B2F_PATH: B2F_PATH.read_text(encoding="utf-8"),
    }
    rendered = {
        B1F_PATH: render_b1f(originals[B1F_PATH]),
        B2F_PATH: render_b2f(originals[B2F_PATH]),
    }

    if args.check:
        print(
            "Arquivo Central renderer OK: "
            f"{len(B1F_TARGETS)} B1F blocks and {len(B2F_TARGETS)} B2F blocks validated."
        )
        return 0

    if args.in_place:
        for path, content in rendered.items():
            path.write_text(content, encoding="utf-8")
        return 0

    for path, content in rendered.items():
        print(f"===== {path.relative_to(ROOT)} =====")
        print(content, end="" if content.endswith("\n") else "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
