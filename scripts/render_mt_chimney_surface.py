#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_INPUT = ROOT / "data" / "maps" / "MtChimney" / "scripts.inc"
MAX_VISIBLE_WIDTH = 32

TARGETS: dict[str, tuple[tuple[str, ...], tuple[str, ...]]] = {
    "MtChimney_Text_MeteoriteWillActivateVolcano": (
        ("METEORITE", "MT. CHIMNEY"),
        (
            "LUZIA: Este METEORITO amplifica\\n",
            "VINCULOS guardados.\\p",
            "Com ele, posso devolver o que\\n",
            "foi arrancado a forca.$",
        ),
    ),
    "MtChimney_Text_MaxieIntro": (
        ("LUZIA", "HORIZONTE"),
        (
            "LUZIA: O HORIZONTE chama isso\\n",
            "de tratamento.\\p",
            "Eu chamo de memoria roubada.\\p",
            "Se querem impedir que eu a\\n",
            "devolva, terao de me parar.$",
        ),
    ),
    "MtChimney_Text_MaxieDefeat": (
        ("LUZIA", "lembrar"),
        (
            "LUZIA: Entao voce escolheu\\n",
            "ficar no caminho...\\p",
            "Isso nao torna o HORIZONTE\\n",
            "certo.$",
        ),
    ),
    "MtChimney_Text_MaxieYouHaventSeenLastOfMagma": (
        ("sensores", "ARQUIVO"),
        (
            "LUZIA: Nao acabou.\\p",
            "Ninguem decide sozinho quais\\n",
            "lembrancas Arauna deve perder.$",
        ),
    ),
    "MtChimney_Text_TabithaIntro": (
        ("METEORITE", "BOSS"),
        (
            "LEMBRANTE: Voce chegou tarde.\\p",
            "O METEORITO ja esta com LUZIA.\\p",
            "Para passar, tera de me vencer!$",
        ),
    ),
    "MtChimney_Text_TabithaDefeat": (
        ("leader", "awakens"),
        ("LEMBRANTE: Eu nao consegui\\n", "segurar voce...$"),
    ),
    "MtChimney_Text_TabithaPostBattle": (
        ("BOSS", "METEORITE"),
        ("LEMBRANTE: LUZIA, termine logo!\\n", "O HORIZONTE esta chegando.$"),
    ),
    "MtChimney_Text_Grunt2Intro": (
        ("LEMBRANTE", "HORIZONTE"),
        (
            "LEMBRANTE: O que foi extraido\\n",
            "nao pertence ao HORIZONTE.\\p",
            "Saia do caminho.$",
        ),
    ),
    "MtChimney_Text_Grunt2Defeat": (
        ("HORIZONTE", "ARQUIVO VIVO"),
        ("LEMBRANTE: Voce e mais forte\\n", "do que eu esperava.$"),
    ),
    "MtChimney_Text_Grunt2PostBattle": (
        ("HORIZONTE", "soldados"),
        (
            "LEMBRANTE: Dor nao da direito\\n",
            "de apagar. Devolver a forca...\\p",
            "Eu ainda penso nisso.$",
        ),
    ),
    "MtChimney_Text_Grunt1Intro": (
        ("HORIZONTE", "sensores"),
        (
            "LEMBRANTE: O HORIZONTE chama\\n",
            "apagamento de tratamento.\\p",
            "Nao vou deixar que levem mais.$",
        ),
    ),
    "MtChimney_Text_Grunt1Defeat": (
        ("HORIZONTE", "ARQUIVO VIVO"),
        ("LEMBRANTE: Ainda falta muito\\n", "para eu sustentar essa escolha.$"),
    ),
    "MtChimney_Text_Grunt1PostBattle": (
        ("HORIZONTE", "sensores"),
        ("LEMBRANTE: Nao basta lembrar.\\n", "Temos de escolher como devolver.$"),
    ),
    "MtChimney_Text_TeamAquaAlwaysMessingWithPlans": (
        ("HORIZONTE", "soldados"),
        (
            "LEMBRANTE: O HORIZONTE sempre\\n",
            "chega dizendo que e seguranca.\\p",
            "Depois decide o que some.$",
        ),
    ),
    "MtChimney_Text_MeteoritesPackAmazingPower": (
        ("METEORITES", "amazing power"),
        (
            "LEMBRANTE: O METEORITO reage\\n",
            "aos VINCULOS armazenados.\\p",
            "Nao sabemos ate onde isso vai.$",
        ),
    ),
    "MtChimney_Text_YouBetterNotMessWithUs": (
        ("mess with us", "benefit of everyone"),
        (
            "LEMBRANTE: Nao interfira.\\p",
            "Estamos devolvendo registros\\n",
            "que nunca deveriam ter sido\\n",
            "tomados.$",
        ),
    ),
    "MtChimney_Text_AquasNameSimilar": (
        ("LEMBRANTE", "LUZIA"),
        ("LEMBRANTE: Memoria roubada nao\\n", "vira cura so por mudar de nome.$"),
    ),
    "MtChimney_Text_DouseThemInFire": (
        ("Douse them in fire",),
        ("LEMBRANTE: Segure a linha!\\n", "Nao deixe os agentes passarem!$"),
    ),
    "MtChimney_Text_KeepMakingMoreLand": (
        ("more land",),
        ("LEMBRANTE: Nenhum arquivo fica\\n", "enterrado para sempre.$"),
    ),
    "MtChimney_Text_ArchieGoStopTeamMagma": (
        ("OTACILIO", "Preservar tudo"),
        (
            "OTACILIO: LUZIA vai ativar o\\n",
            "amplificador com o METEORITO.\\p",
            "Pare-a antes que essa serra\\n",
            "vire um experimento.$",
        ),
    ),
    "MtChimney_Text_ArchieIHaveMyHandsFull": (
        ("OTACILIO", "M'BOI"),
        (
            "OTACILIO: Estou contendo os\\n",
            "LEMBRANTES daqui.\\p",
            "Va. LUZIA esta no equipamento.$",
        ),
    ),
    "MtChimney_Text_ArchieThankYou": (
        ("OTACILIO", "ARQUIVO VIVO"),
        (
            "OTACILIO: Voce impediu uma\\n",
            "liberacao sem controle.\\p",
            "Isso nao resolve nossa disputa,\\n",
            "mas evitou algo pior hoje.$",
        ),
    ),
    "MtChimney_Text_MagmaOutnumbersUs": (
        ("LEMBRANTE", "historia"),
        ("HORIZONTE: Eles sao muitos.\\n", "Nao consigo sair daqui agora.$"),
    ),
    "MtChimney_Text_LessHabitatForWaterPokemon": (
        ("WATER POKéMON",),
        (
            "HORIZONTE: LUZIA vai usar o\\n",
            "METEORITO como amplificador.\\p",
            "Se funcionar, memorias podem\\n",
            "voltar sem consentimento.$",
        ),
    ),
    "MtChimney_Text_MagmasNameSimilar": (
        ("LEMBRANTE", "historia"),
        (
            "HORIZONTE: Somos tecnicos e\\n",
            "guardas, nao donos da memoria.\\p",
            "Nem todos aqui lembram disso.$",
        ),
    ),
    "MtChimney_Text_MeteoriteFittedOnMachine": (
        ("METEORITE", "mysterious"),
        (
            "O METEORITO esta preso a um\\n",
            "amplificador de VINCULO.\\p",
            "O aparelho acumula energia.$",
        ),
    ),
    "MtChimney_Text_RemoveTheMeteorite": (
        ("METEORITE", "remove"),
        (
            "Um METEORITO alimenta o\\n",
            "amplificador.\\p",
            "Remover o METEORITO?$",
        ),
    ),
    "MtChimney_Text_PlayerRemovedMeteorite": (
        ("removed the METEORITE",),
        ("{PLAYER} removeu o METEORITO\\n", "do amplificador.$"),
    ),
    "MtChimney_Text_PlayerLeftMeteorite": (
        ("left the METEORITE",),
        ("{PLAYER} deixou o METEORITO\\n", "no lugar.$"),
    ),
    "MtChimney_Text_MachineMakesNoResponse": (
        ("mysterious machine", "no response"),
        ("O amplificador esta desligado.\\n", "Nao ha resposta.$"),
    ),
    "MtChimney_Text_RouteSign": (
        ("JAGGED PATH", "LAVARIDGE TOWN"),
        ("SERRA DA CINZA\\n", "{DOWN_ARROW} SERTAO DE DENTRO$"),
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
    forbidden_by_label = {
        "MtChimney_Text_MeteoriteWillActivateVolcano": ("MT. CHIMNEY",),
        "MtChimney_Text_TabithaIntro": ("BOSS", "METEOR FALLS"),
        "MtChimney_Text_TabithaPostBattle": ("BOSS",),
        "MtChimney_Text_MeteoritesPackAmazingPower": ("amazing power",),
        "MtChimney_Text_YouBetterNotMessWithUs": ("benefit of everyone",),
        "MtChimney_Text_DouseThemInFire": ("Douse them in fire",),
        "MtChimney_Text_KeepMakingMoreLand": ("more land",),
        "MtChimney_Text_LessHabitatForWaterPokemon": ("WATER POKéMON",),
        "MtChimney_Text_RouteSign": ("JAGGED PATH", "LAVARIDGE TOWN"),
    }
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
        for token in forbidden_by_label.get(label, ()):
            if token in body:
                raise ValueError(f"{label}: legacy visible token survived: {token}")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Render the Serra da Cinza Horizonte/Lembrante conflict without changing Emerald event wiring."
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
        print(f"Serra da Cinza renderer OK: {len(TARGETS)} plot blocks validated.")
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
