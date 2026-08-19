#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MAX_VISIBLE_WIDTH = 32
CONTROL_RE = re.compile(r"\\[npl]")
PLACEHOLDER_RE = re.compile(r"\{[^}]+\}")

PATH_3F1 = ROOT / "data" / "maps" / "MagmaHideout_3F_1R" / "scripts.inc"
PATH_3F2 = ROOT / "data" / "maps" / "MagmaHideout_3F_2R" / "scripts.inc"
PATH_4F = ROOT / "data" / "maps" / "MagmaHideout_4F" / "scripts.inc"

SOURCE_SIGNATURES = (
    "Guardar um nome",
    "HORIZONTE quer uma",
    "Se uma historia",
    "LUZIA diz que",
    "sensores registram",
    "Taken down again",
    "LUZIA: O problema nunca foi",
    "LUZIA: Se devolver as memorias",
)

TARGETS_3F1 = {
    "MagmaHideout_3F_1R_Text_Grunt9Intro": (
        "LEMBRANTE: O REGISTRO-MATRIZ\\n",
        "responde a VINCULOS antigos.$",
    ),
    "MagmaHideout_3F_1R_Text_Grunt9Defeat": (
        "LEMBRANTE:\\n",
        "Ele nao contem memoria.\\p",
        "Aponta para onde ela foi\\n",
        "empurrada.$",
    ),
    "MagmaHideout_3F_1R_Text_Grunt9PostBattle": (
        "LEMBRANTE: LUZIA quer abrir a\\n",
        "corrente e deixar tudo voltar.$",
    ),
    "MagmaHideout_3F_1R_Text_Grunt16Intro": (
        "LEMBRANTE: Os sensores ja estao\\n",
        "fora da escala.$",
    ),
    "MagmaHideout_3F_1R_Text_Grunt16Defeat": (
        "LEMBRANTE: Isso nao parece uma\\n",
        "restauracao controlada.$",
    ),
    "MagmaHideout_3F_1R_Text_Grunt16PostBattle": (
        "LEMBRANTE: Se chegar a LUZIA,\\n",
        "pergunte se ela ainda distingue\\n",
        "justica de urgencia.$",
    ),
}

TARGETS_3F2 = {
    "MagmaHideout_3F_2R_Text_Grunt10Intro": (
        "LEMBRANTE: RAUL fechou o acesso.\\p",
        "A ativacao ja comecou.$",
    ),
    "MagmaHideout_3F_2R_Text_Grunt10Defeat": (
        "LEMBRANTE: Eu devia estar la em\\n",
        "cima ajudando.\\p",
        "Parte de mim esta aliviada.$",
    ),
    "MagmaHideout_3F_2R_Text_Grunt10PostBattle": (
        "LEMBRANTE: Nao deixe o HORIZONTE\\n",
        "levar o REGISTRO.\\p",
        "Mas nao deixe LUZIA usa-lo sem\\n",
        "limite tambem.$",
    ),
}

TARGETS_4F = {
    "MagmaHideout_4F_Text_Grunt11Intro": (
        "LEMBRANTE:\\n",
        "O nucleo esta reagindo.\\p",
        "Fique longe do equipamento.$",
    ),
    "MagmaHideout_4F_Text_Grunt11Defeat": (
        "LEMBRANTE: As leituras subiram\\n",
        "quando LUZIA tocou o REGISTRO.$",
    ),
    "MagmaHideout_4F_Text_Grunt11PostBattle": (
        "LEMBRANTE:\\n",
        "Isso nao devolve uma historia\\n",
        "por vez.\\p",
        "Esta puxando milhares.$",
    ),
    "MagmaHideout_4F_Text_Grunt12Intro": (
        "LEMBRANTE:\\n",
        "LUZIA pediu confianca.\\p",
        "Eu queria ter pedido um plano.$",
    ),
    "MagmaHideout_4F_Text_Grunt12Defeat": (
        "LEMBRANTE: O HORIZONTE vai usar\\n",
        "isso contra todos nos.$",
    ),
    "MagmaHideout_4F_Text_Grunt12PostBattle": (
        "LEMBRANTE: E talvez tenha razao\\n",
        "sobre o risco.\\p",
        "Odio admitir isso.$",
    ),
    "MagmaHideout_4F_Text_Grunt13Intro": (
        "LEMBRANTE:\\n",
        "O REGISTRO abriu uma passagem\\n",
        "que nao sabemos fechar.$",
    ),
    "MagmaHideout_4F_Text_Grunt13Defeat": (
        "LEMBRANTE:\\n",
        "Nao consigo mais chamar isso\\n",
        "apenas de devolucao.$",
    ),
    "MagmaHideout_4F_Text_Grunt13PostBattle": (
        "LEMBRANTE:\\n",
        "Va. Se LUZIA nao ouvir a gente,\\n",
        "talvez ouca voce.$",
    ),
    "MagmaHideout_4F_Text_TabithaIntro": (
        "RAUL: Chega.\\p",
        "Voce ja viu mais desta base do\\n",
        "que deveria.$",
    ),
    "MagmaHideout_4F_Text_TabithaDefeat": (
        "RAUL: Droga...\\p",
        "Entao passe. Mas nao confunda\\n",
        "vencer comigo com estar certo.$",
    ),
    "MagmaHideout_4F_Text_TabithaPostBattle": (
        "RAUL: Eu sigo LUZIA porque vi\\n",
        "familias apagadas dos registros.\\p",
        "Isso nao significa que eu nao\\n",
        "tenha medo do que ela fara.$",
    ),
    "MagmaHideout_4F_Text_MaxieAwakenGroudon": (
        "LUZIA: Este REGISTRO-MATRIZ foi\\n",
        "feito para localizar o que o\\n",
        "ARQUIVO arrancou.\\p",
        "Hoje isso volta para Arauna.$",
    ),
    "MagmaHideout_4F_Text_MaxieGroudonWhatsWrong": (
        "LUZIA: Espere...\\p",
        "A corrente nao esta seguindo o\\n",
        "REGISTRO.\\p",
        "Ela esta puxando tudo.$",
    ),
    "MagmaHideout_4F_Text_MaxieOhItWasYou": (
        "LUZIA: Voce chegou ate aqui.\\p",
        "Se veio me impedir, vai ter que\\n",
        "me mostrar outra saida.$",
    ),
    "MagmaHideout_4F_Text_MaxieDefeat": (
        "LUZIA: Perder uma batalha nao\\n",
        "torna o HORIZONTE correto.\\p",
        "Mas eu ouvi o que voce mostrou.$",
    ),
    "MagmaHideout_4F_Text_MaxieImGoingAfterGroudon": (
        "LUZIA: A corrente saiu da base.\\p",
        "Os sinais seguem para o litoral.\\p",
        "Vou ao PORTO DO SAL antes que o\\n",
        "HORIZONTE chegue primeiro.$",
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
        raise ValueError("non-dialogue structure changed while rendering Lembrantes base")
    return rendered


def render_3f1(source: str) -> str:
    return render(source, TARGETS_3F1)


def render_3f2(source: str) -> str:
    return render(source, TARGETS_3F2)


def render_4f(source: str) -> str:
    rendered = render(source, TARGETS_4F)
    for token in ("Taken down again", "Hehe", "sensores registram duas"):
        for label in TARGETS_4F:
            body = block_pattern(label).search(rendered).group("body")
            if token in body:
                raise ValueError(f"{label}: stale Lembrantes core token survived: {token}")
    return rendered


def rendered_sources() -> dict[Path, str]:
    return {
        PATH_3F1: render_3f1(PATH_3F1.read_text(encoding="utf-8")),
        PATH_3F2: render_3f2(PATH_3F2.read_text(encoding="utf-8")),
        PATH_4F: render_4f(PATH_4F.read_text(encoding="utf-8")),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Render the upper Lembrantes base and Luzia activation sequence.")
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--in-place", action="store_true")
    args = parser.parse_args()
    if args.check and args.in_place:
        parser.error("use either --check or --in-place")

    rendered = rendered_sources()
    if args.check:
        print(
            "Lembrantes core renderer OK: "
            f"{len(TARGETS_3F1) + len(TARGETS_3F2) + len(TARGETS_4F)} blocks validated."
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
