#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MAX_VISIBLE_WIDTH = 32
CONTROL_RE = re.compile(r"\\[npl]")
PLACEHOLDER_RE = re.compile(r"\{[^}]+\}")

PATH_1F = ROOT / "data" / "maps" / "MagmaHideout_1F" / "scripts.inc"
PATH_2F1 = ROOT / "data" / "maps" / "MagmaHideout_2F_1R" / "scripts.inc"
PATH_2F2 = ROOT / "data" / "maps" / "MagmaHideout_2F_2R" / "scripts.inc"

SOURCE_SIGNATURES = (
    "Guardar um nome",
    "HORIZONTE quer uma",
    "Se uma historia",
    "LUZIA diz que",
    "sensores registram",
)

TARGETS_1F = {
    "MagmaHideout_1F_Text_Grunt1Intro": (
        "LEMBRANTE: Esta base guarda\\n",
        "copias que o HORIZONTE tentou\\n",
        "retirar de circulacao.$",
    ),
    "MagmaHideout_1F_Text_Grunt1Defeat": (
        "LEMBRANTE: Nem todo arquivo\\n",
        "perdido foi acidente.\\p",
        "Foi por isso que eu entrei.$",
    ),
    "MagmaHideout_1F_Text_Grunt1PostBattle": (
        "LEMBRANTE: Se subir, vai ver\\n",
        "que nem todos aqui concordam\\n",
        "com LUZIA em tudo.$",
    ),
    "MagmaHideout_1F_Text_Grunt2Intro": (
        "LEMBRANTE: O MEMORIAL guarda\\n",
        "nomes. Aqui guardamos provas\\n",
        "de como tentaram apaga-los.$",
    ),
    "MagmaHideout_1F_Text_Grunt2Defeat": (
        "LEMBRANTE: Eu quero devolver\\n",
        "historias, nao invadir a mente\\n",
        "de ninguem.$",
    ),
    "MagmaHideout_1F_Text_Grunt2PostBattle": (
        "LEMBRANTE: Pergunte la em cima\\n",
        "quem decidiu usar o\\n",
        "REGISTRO-MATRIZ.$",
    ),
}

TARGETS_2F1 = {
    "MagmaHideout_2F_1R_Text_Grunt14Intro": (
        "LEMBRANTE: Estes cadernos vieram\\n",
        "de familias atingidas em M'BOI.$",
    ),
    "MagmaHideout_2F_1R_Text_Grunt14Defeat": (
        "LEMBRANTE: O selo do HORIZONTE\\n",
        "diz 'material terapeutico'.\\p",
        "Para mim, sao testemunhos.$",
    ),
    "MagmaHideout_2F_1R_Text_Grunt14PostBattle": (
        "LEMBRANTE: Copiamos tudo antes\\n",
        "que outra ordem de descarte\\n",
        "chegue.$",
    ),
    "MagmaHideout_2F_1R_Text_Grunt3Intro": (
        "LEMBRANTE: Ha depoimentos aqui\\n",
        "com trechos inteiros cobertos\\n",
        "por tinta.$",
    ),
    "MagmaHideout_2F_1R_Text_Grunt3Defeat": (
        "LEMBRANTE: Nao consigo provar\\n",
        "quem mandou ocultar cada linha.\\p",
        "So que alguem mandou.$",
    ),
    "MagmaHideout_2F_1R_Text_Grunt3PostBattle": (
        "LEMBRANTE:\\n",
        "Prova incompleta ainda e melhor\\n",
        "que silencio perfeito.$",
    ),
    "MagmaHideout_2F_1R_Text_Grunt4Intro": (
        "LEMBRANTE: Este lote saiu de um\\n",
        "deposito que seria incinerado.$",
    ),
    "MagmaHideout_2F_1R_Text_Grunt4Defeat": (
        "LEMBRANTE:\\n",
        "A LIGA e o HORIZONTE assinam\\n",
        "a mesma pasta.$",
    ),
    "MagmaHideout_2F_1R_Text_Grunt4PostBattle": (
        "LEMBRANTE:\\n",
        "ELIAS aparece em varias\\n",
        "aprovacoes. Tambem ha ressalvas.$",
    ),
    "MagmaHideout_2F_1R_Text_Grunt5Intro": (
        "LEMBRANTE: Nao confunda arquivo\\n",
        "com verdade completa.\\p",
        "Documento tambem pode mentir.$",
    ),
    "MagmaHideout_2F_1R_Text_Grunt5Defeat": (
        "LEMBRANTE:\\n",
        "Por isso cruzamos nomes, datas\\n",
        "e testemunhos.$",
    ),
    "MagmaHideout_2F_1R_Text_Grunt5PostBattle": (
        "LEMBRANTE:\\n",
        "LUZIA quer abrir tudo.\\p",
        "Eu ainda acho que algumas vozes\\n",
        "precisam escolher quando falar.$",
    ),
}

TARGETS_2F2 = {
    "MagmaHideout_2F_2R_Text_Grunt15Intro": (
        "LEMBRANTE: Aqui discutimos uma\\n",
        "coisa simples e impossivel:\\p",
        "quem pode devolver uma memoria?$",
    ),
    "MagmaHideout_2F_2R_Text_Grunt15Defeat": (
        "LEMBRANTE:\\n",
        "Se a pessoa pediu para esquecer,\\n",
        "nao devia decidir o contrario.$",
    ),
    "MagmaHideout_2F_2R_Text_Grunt15PostBattle": (
        "LEMBRANTE: LUZIA diz que o roubo\\n",
        "veio antes do consentimento.\\p",
        "Ela nao esta errada nisso.$",
    ),
    "MagmaHideout_2F_2R_Text_Grunt6Intro": (
        "LEMBRANTE: O problema e o passo\\n",
        "seguinte: devolver tudo de uma\\n",
        "vez.$",
    ),
    "MagmaHideout_2F_2R_Text_Grunt6Defeat": (
        "LEMBRANTE:\\n",
        "Uma verdade pode salvar.\\p",
        "Tambem pode esmagar alguem que\\n",
        "nao escolheu recebe-la.$",
    ),
    "MagmaHideout_2F_2R_Text_Grunt6PostBattle": (
        "LEMBRANTE: Eu sigo LUZIA porque\\n",
        "ela enfrenta o apagamento.\\p",
        "Nao porque ela e infalivel.$",
    ),
    "MagmaHideout_2F_2R_Text_Grunt7Intro": (
        "LEMBRANTE:\\n",
        "O HORIZONTE chama isso de\\n",
        "instabilidade.\\p",
        "Nos chamamos de pessoas.$",
    ),
    "MagmaHideout_2F_2R_Text_Grunt7Defeat": (
        "LEMBRANTE: Mas pessoa nao e\\n",
        "arquivo para restaurar sem\\n",
        "perguntar.$",
    ),
    "MagmaHideout_2F_2R_Text_Grunt7PostBattle": (
        "LEMBRANTE:\\n",
        "Talvez o JURAMENTO seja mais\\n",
        "dificil que escolher um lado.$",
    ),
    "MagmaHideout_2F_2R_Text_Grunt8Intro": (
        "LEMBRANTE: RAUL mandou preparar\\n",
        "o andar de cima.\\p",
        "LUZIA vai usar o REGISTRO.$",
    ),
    "MagmaHideout_2F_2R_Text_Grunt8Defeat": (
        "LEMBRANTE: Ninguem sabe como a\\n",
        "corrente vai reagir.$",
    ),
    "MagmaHideout_2F_2R_Text_Grunt8PostBattle": (
        "LEMBRANTE:\\n",
        "Se ela estiver errada, espero\\n",
        "que alguem consiga para-la.$",
    ),
}


def block_pattern(label: str) -> re.Pattern[str]:
    return re.compile(rf"(?ms)^{re.escape(label)}:\n(?P<body>.*?)(?=^[A-Za-z0-9_]+(?:::|:)(?:\n|$)|\Z)")


def visible_segments(payload: str) -> list[str]:
    cleaned = PLACEHOLDER_RE.sub("", payload).replace("$", "")
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
            raise ValueError(f"{label}: target is not a text block")
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
    labels = tuple(targets)
    if mask_blocks(source, labels) != mask_blocks(rendered, labels):
        raise ValueError("non-dialogue structure changed while rendering lower Lembrantes base")
    return rendered


def render_1f(source: str) -> str:
    return render(source, TARGETS_1F)


def render_2f1(source: str) -> str:
    return render(source, TARGETS_2F1)


def render_2f2(source: str) -> str:
    return render(source, TARGETS_2F2)


def rendered_sources() -> dict[Path, str]:
    return {
        PATH_1F: render_1f(PATH_1F.read_text(encoding="utf-8")),
        PATH_2F1: render_2f1(PATH_2F1.read_text(encoding="utf-8")),
        PATH_2F2: render_2f2(PATH_2F2.read_text(encoding="utf-8")),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Render the lower Lembrantes base: entry, archive evidence and internal dissent.")
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--in-place", action="store_true")
    args = parser.parse_args()
    if args.check and args.in_place:
        parser.error("use either --check or --in-place")

    rendered = rendered_sources()
    if args.check:
        print(
            "Lower Lembrantes renderer OK: "
            f"{len(TARGETS_1F) + len(TARGETS_2F1) + len(TARGETS_2F2)} blocks validated."
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
