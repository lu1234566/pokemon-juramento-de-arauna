#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
METEOR_PATH = ROOT / "data" / "maps" / "MeteorFalls_1F_1R" / "scripts.inc"
MEMORIAL_PATH = ROOT / "data" / "maps" / "MtPyre_Summit" / "scripts.inc"
ITEMS_PATH = ROOT / "src" / "data" / "items.h"
ITEM_DESCS_PATH = ROOT / "src" / "data" / "text" / "item_descriptions.h"
MAX_VISIBLE_WIDTH = 32

CONTROL_RE = re.compile(r"\\[npl]")
PLACEHOLDER_RE = re.compile(r"\{[^}]+\}")

METEOR_TARGETS: dict[str, tuple[tuple[str, ...], tuple[str, ...]]] = {
    "MeteorFalls_1F_1R_Text_WithThisMeteorite": (
        ("METEORITE", "MT. CHIMNEY"),
        (
            "LEMBRANTE: Este METEORITO\\n",
            "faz o amplificador reagir.\\p",
            "Na SERRA DA CINZA vamos\\n",
            "devolver o que foi extraido.$",
        ),
    ),
    "MeteorFalls_1F_1R_Text_DontExpectMercyFromMagma": (
        ("LEMBRANTES", "mercy"),
        ("LEMBRANTE: Se voce entrar\\n", "no caminho, nao espere favor.$"),
    ),
    "MeteorFalls_1F_1R_Text_HoldItRightThereMagma": (
        ("LEMBRANTES", "world"),
        (
            "HORIZONTE: Parem ai!\\p",
            "Esse METEORITO nao pode ser\\n",
            "ativado sem controle.$",
        ),
    ),
    "MeteorFalls_1F_1R_Text_BeSeeingYouTeamAqua": (
        ("CONSORCIO HORIZONTE", "TEAM", "AQUA"),
        (
            "LEMBRANTE: Conseguimos o\\n",
            "METEORITO. Agora, SERRA DA\\n",
            "CINZA.\\p",
            "HORIZONTE, cheguem tarde.$",
        ),
    ),
    "MeteorFalls_1F_1R_Text_ArchieSeenYouBefore": (
        ("OTACILIO", "Preservar"),
        (
            "OTACILIO: Voce outra vez.\\p",
            "Eles nao sabem o que esse\\n",
            "amplificador pode liberar.$",
        ),
    ),
    "MeteorFalls_1F_1R_Text_BossWeShouldChaseMagma": (
        ("BOSS", "LEMBRANTES"),
        ("HORIZONTE: Diretor, precisamos\\n", "ir atras dos LEMBRANTES.$"),
    ),
    "MeteorFalls_1F_1R_Text_ArchieYesNoTellingWhatMagmaWillDo": (
        ("LEMBRANTES", "MT. CHIMNEY"),
        (
            "OTACILIO: Sim. Vamos agora.\\p",
            "LUZIA levou o METEORITO para\\n",
            "a SERRA DA CINZA.$",
        ),
    ),
    "MeteorFalls_1F_1R_Text_ArchieFarewell": (
        ("OTACILIO", "M'BOI"),
        (
            "OTACILIO: Nao confunda\\n",
            "impedi-la com concordar comigo.\\p",
            "Essa disputa ainda nao acabou.$",
        ),
    ),
    "MeteorFalls_1F_1R_Text_MeetProfCozmo": (
        ("COZMO", "PROFESSOR", "METEOR FALLS", "CONSORCIO HORIZONTE"),
        (
            "Sou pesquisador de minerais.\\p",
            "Os LEMBRANTES pediram que eu\\n",
            "os guiasse pelas RUINAS DA\\n",
            "QUEDA.\\p",
            "Depois tomaram meu METEORITO.\\p",
            "Logo o HORIZONTE apareceu.\\p",
            "Nao sei em quem confiar.$",
        ),
    ),
    "MeteorFalls_1F_1R_Text_WhatsTeamMagmaDoingAtMtChimney": (
        ("PROF. COZMO", "MT. CHIMNEY"),
        (
            "PESQUISADOR: Os LEMBRANTES\\n",
            "levaram meu METEORITO para\\n",
            "a SERRA DA CINZA. Por que?$",
        ),
    ),
}

MEMORIAL_TARGETS: dict[str, tuple[tuple[str, ...], tuple[str, ...]]] = {
    "MtPyre_Summit_Text_Grunt1Intro": (
        ("DONA ZILA",),
        ("HORIZONTE: Afaste-se.\\p", "Estas placas serao recolhidas.$"),
    ),
    "MtPyre_Summit_Text_Grunt1Defeat": (
        ("DONA ZILA",),
        ("HORIZONTE: Voce nao entende\\n", "o que estamos tentando conter.$"),
    ),
    "MtPyre_Summit_Text_Grunt1PostBattle": (
        ("DONA ZILA",),
        ("HORIZONTE: Digitalizar primeiro\\n", "nao torna a retirada correta.$"),
    ),
    "MtPyre_Summit_Text_Grunt2Intro": (
        ("Os nomes gravados aqui",),
        ("HORIZONTE: O MEMORIAL esta\\n", "sob protocolo de seguranca.$"),
    ),
    "MtPyre_Summit_Text_Grunt2Defeat": (
        ("funcionario do HORIZONTE",),
        ("HORIZONTE: Nao esperava\\n", "resistencia aqui.$"),
    ),
    "MtPyre_Summit_Text_Grunt2PostBattle": (
        ("DONA ZILA",),
        ("HORIZONTE: Algumas ordens\\n", "parecem piores quando ditas\\n", "em voz alta.$"),
    ),
    "MtPyre_Summit_Text_Grunt3Intro": (
        ("funcionario do HORIZONTE",),
        ("HORIZONTE: Os registros serao\\n", "levados ao ARQUIVO CENTRAL.$"),
    ),
    "MtPyre_Summit_Text_Grunt3Defeat": (
        ("funcionario do HORIZONTE",),
        ("HORIZONTE: Certo... voce\\n", "venceu esta disputa.$"),
    ),
    "MtPyre_Summit_Text_Grunt3PostBattle": (
        ("DONA ZILA",),
        ("HORIZONTE: Catalogar memoria\\n", "nao nos da posse dela.$"),
    ),
    "MtPyre_Summit_Text_Grunt4Intro": (
        ("Os nomes gravados aqui",),
        ("HORIZONTE: Nao toque nas\\n", "placas marcadas para retirada.$"),
    ),
    "MtPyre_Summit_Text_Grunt4Defeat": (
        ("Os nomes gravados aqui",),
        ("HORIZONTE: Isso complica\\n", "a operacao.$"),
    ),
    "MtPyre_Summit_Text_Grunt4PostBattle": (
        ("funcionario do HORIZONTE",),
        (
            "HORIZONTE: OTACILIO acredita\\n",
            "que certas feridas precisam\\n",
            "ser encerradas. Eu ainda penso.$",
        ),
    ),
    "MtPyre_Summit_Text_ArchieWeGotTheOrbLetsGo": (
        ("sensores registram", "ARQUIVO"),
        ("OTACILIO: Temos o REGISTRO-MATRIZ.\\p", "Recolham a equipe. Vamos.$"),
    ),
    "MtPyre_Summit_Text_BothOrbsTakenMagmaLeftThis": (
        ("sensores registram", "ARQUIVO"),
        (
            "GUARDIA: O HORIZONTE levou um\\n",
            "REGISTRO-MATRIZ daqui.\\p",
            "Os LEMBRANTES levaram o outro.\\p",
            "Eles deixaram este emblema.$",
        ),
    ),
    "MtPyre_Summit_Text_OrbsHaveBeenTaken": (
        ("sensores registram", "ARQUIVO"),
        (
            "GUARDIA: Dois REGISTROS-MATRIZ\\n",
            "foram retirados do memorial.\\p",
            "Um pelo HORIZONTE. Outro pelos\\n",
            "LEMBRANTES.$",
        ),
    ),
    "MtPyre_Summit_Text_GroudonKyogreAwakened": (
        ("sensores registram", "ARQUIVO"),
        (
            "GUARDIA: As duas correntes\\n",
            "antigas reagiram ao colapso.\\p",
            "O que foi guardado esta voltando\\n",
            "sem pedir permissao.$",
        ),
    ),
    "MtPyre_Summit_Text_ThoseTwoMenReturnedOrbs": (
        ("sensores registram", "ARQUIVO"),
        (
            "GUARDIA: OTACILIO e LUZIA\\n",
            "devolveram os dois registros.\\p",
            "Nenhum deles saiu daqui com\\n",
            "todas as respostas.$",
        ),
    ),
    "MtPyre_Summit_Text_SuperAncientPokemonTaughtUs": (
        ("embodiments of the land", "super-ancient"),
        (
            "GUARDIA: O colapso mostrou\\n",
            "que memoria e esquecimento\\n",
            "viram violencia quando alguem\\n",
            "escolhe sozinho pelos outros.$",
        ),
    ),
    "MtPyre_Summit_Text_WillYouHearOutMyTale": (
        ("MT. PYRE", "ARAUNA region"),
        (
            "GUARDIA: Este e o MEMORIAL DOS\\n",
            "NOMES. Aqui repetimos historias\\n",
            "para que o silencio nao venca.\\p",
            "Quer ouvir uma delas?$",
        ),
    ),
    "MtPyre_Summit_Text_GroudonKyogreTale": (
        ("sensores registram", "ARQUIVO"),
        (
            "GUARDIA: Antes do HORIZONTE,\\n",
            "ja se falava em duas correntes.\\p",
            "Uma puxa lembrancas de volta.\\n",
            "A outra deixa vinculos terminar.\\p",
            "O JURAMENTO nasceu para que\\n",
            "ninguem escolhesse isso sozinho.$",
        ),
    ),
    "MtPyre_Summit_Text_WellThatTooIsFine": (
        ("Well, that, too, is fine",),
        (
            "GUARDIA: Tudo bem. Uma historia\\n",
            "tambem precisa de quem queira\\n",
            "escuta-la.$",
        ),
    ),
    "MtPyre_Summit_Text_MaxieSilence": (
        ("LUZIA", "HORIZONTE"),
        (
            "LUZIA: Devolvemos o que nunca\\n",
            "tivemos direito de levar.\\p",
            "Nem eu, nem OTACILIO.$",
        ),
    ),
    "MtPyre_Summit_Text_HearTheNewLegendOfHoenn": (
        ("legends", "ARAUNA"),
        (
            "GUARDIA: Depois de M'BOI, a\\n",
            "historia deste memorial mudou.\\p",
            "Quer ouvir a nova versao?$",
        ),
    ),
    "MtPyre_Summit_Text_HoennTrioTale": (
        ("It happened long, long ago", "land", "sea"),
        (
            "GUARDIA: Durante muito tempo,\\n",
            "contamos que lembrar era sempre\\n",
            "justo e esquecer era sempre perda.\\p",
            "M'BOI mostrou que absolutos\\n",
            "tambem ferem.\\p",
            "O novo JURAMENTO nao manda\\n",
            "lembrar tudo nem apagar a dor.\\p",
            "Ele exige que nenhuma pessoa\\n",
            "decida sozinha pelo resto.$",
        ),
    ),
}

ITEM_NAME_OLD = '.name = _("MAGMA EMBLEM"),'
ITEM_NAME_NEW = '.name = _("EMBLEMA LEMB."),'

ITEM_DESC_RE = re.compile(
    r'(?ms)^static const u8 sMagmaEmblemDesc\[\] = _\(\n(?P<body>.*?)^\);'
)
ITEM_DESC_NEW = (
    'static const u8 sMagmaEmblemDesc[] = _(\n'
    '    "Um emblema usado\\n"\n'
    '    "pelos LEMBRANTES.\\n"\n'
    '    "Abre sua base.");'
)


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


def mask_targets(source: str, labels: tuple[str, ...]) -> str:
    masked = source
    for label in labels:
        pattern = block_pattern(label)
        match = pattern.search(masked)
        if not match:
            raise ValueError(f"{label}: cannot mask missing block")
        start, end = match.span("body")
        masked = masked[:start] + "\t.string \"<ARAUANA_RENDERED_BLOCK>\"\n\n" + masked[end:]
    return masked


def validate_only_target_bodies_changed(
    original: str,
    rendered: str,
    targets: dict[str, tuple[tuple[str, ...], tuple[str, ...]]],
) -> None:
    labels = tuple(targets)
    if mask_targets(original, labels) != mask_targets(rendered, labels):
        raise ValueError("non-dialogue structure changed while rendering scene")


def validate_rendered_blocks(
    rendered: str,
    targets: dict[str, tuple[tuple[str, ...], tuple[str, ...]]],
    forbidden: tuple[str, ...],
) -> None:
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


def render_meteor(source: str) -> str:
    validate_widths(METEOR_TARGETS)
    rendered = replace_text_blocks(source, METEOR_TARGETS)
    validate_only_target_bodies_changed(source, rendered, METEOR_TARGETS)
    validate_rendered_blocks(
        rendered,
        METEOR_TARGETS,
        ("TEAM AQUA", "TEAM MAGMA", "METEOR FALLS", "MT. CHIMNEY", "COZMO", "PROF. COZMO"),
    )
    return rendered


def render_memorial(source: str) -> str:
    validate_widths(MEMORIAL_TARGETS)
    rendered = replace_text_blocks(source, MEMORIAL_TARGETS)
    validate_only_target_bodies_changed(source, rendered, MEMORIAL_TARGETS)
    validate_rendered_blocks(
        rendered,
        MEMORIAL_TARGETS,
        ("DONA ZILA", "MT. PYRE", "HOENN", "GROUDON", "KYOGRE", "RAYQUAZA", "TEAM AQUA", "TEAM MAGMA"),
    )
    return rendered


def render_items(source: str) -> str:
    count = source.count(ITEM_NAME_OLD)
    if count != 1:
        raise ValueError(f"expected exactly one MAGMA EMBLEM item-name anchor, found {count}")
    rendered = source.replace(ITEM_NAME_OLD, ITEM_NAME_NEW, 1)
    if ITEM_NAME_OLD in rendered or ITEM_NAME_NEW not in rendered:
        raise ValueError("item-name rendering failed")
    return rendered


def render_item_descs(source: str) -> str:
    matches = list(ITEM_DESC_RE.finditer(source))
    if len(matches) != 1:
        raise ValueError(f"expected one sMagmaEmblemDesc block, found {len(matches)}")
    old_body = matches[0].group("body")
    for marker in ("TEAM MAGMA", "medal-like item"):
        if marker not in old_body:
            raise ValueError(f"item description source marker missing: {marker!r}")
    start, end = matches[0].span()
    rendered = source[:start] + ITEM_DESC_NEW + source[end:]
    if "TEAM MAGMA's mark" in rendered:
        raise ValueError("legacy Magma Emblem description survived")
    return rendered


def rendered_sources() -> dict[Path, str]:
    originals = {
        METEOR_PATH: METEOR_PATH.read_text(encoding="utf-8"),
        MEMORIAL_PATH: MEMORIAL_PATH.read_text(encoding="utf-8"),
        ITEMS_PATH: ITEMS_PATH.read_text(encoding="utf-8"),
        ITEM_DESCS_PATH: ITEM_DESCS_PATH.read_text(encoding="utf-8"),
    }
    return {
        METEOR_PATH: render_meteor(originals[METEOR_PATH]),
        MEMORIAL_PATH: render_memorial(originals[MEMORIAL_PATH]),
        ITEMS_PATH: render_items(originals[ITEMS_PATH]),
        ITEM_DESCS_PATH: render_item_descs(originals[ITEM_DESCS_PATH]),
    }


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Render Ruinas da Queda + Memorial dos Nomes narrative surfaces and the Lembrante emblem."
    )
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--in-place", action="store_true")
    args = parser.parse_args()

    if args.check and args.in_place:
        parser.error("use either --check or --in-place")

    rendered = rendered_sources()

    if args.check:
        print(
            "Ruinas/Memorial renderer OK: "
            f"{len(METEOR_TARGETS)} Ruinas blocks, "
            f"{len(MEMORIAL_TARGETS)} Memorial blocks and Lembrante emblem validated."
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
