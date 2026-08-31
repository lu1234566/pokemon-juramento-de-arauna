#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CITY_PATH = ROOT / "data" / "maps" / "SootopolisCity" / "scripts.inc"
TOWER_PATH = ROOT / "data" / "maps" / "SkyPillar_Outside" / "scripts.inc"
MAX_VISIBLE_WIDTH = 32

CONTROL_RE = re.compile(r"\\[npl]")
PLACEHOLDER_RE = re.compile(r"\{[^}]+\}")

CITY_TARGETS: dict[str, tuple[tuple[str, ...], tuple[str, ...]]] = {
    "SootopolisCity_Text_DoorIsClosed": (
        ("The door is closed",),
        ("A porta foi trancada por ordem\\n", "de emergencia.$"),
    ),
    "SootopolisCity_Text_GiantPokemonSuddenlyAppeared": (
        ("giant POKéMON suddenly appeared",),
        (
            "MENINO: Eu lembrei de uma casa\\n",
            "que nunca vi.\\p",
            "Minha mae esqueceu meu nome\\n",
            "por alguns segundos.$",
        ),
    ),
    "SootopolisCity_Text_WhatIsThatGreenPokemon": (
        ("green POKéMON",),
        (
            "MENINO: Aquilo veio da TORRE?\\p",
            "Ele fez as duas correntes\\n",
            "recuarem.$",
        ),
    ),
    "SootopolisCity_Text_TwoPokemonArentAngry": (
        ("two POKéMON aren't angry",),
        (
            "MENINO: Elas nao parecem com\\n",
            "raiva.\\p",
            "Parece que nenhuma consegue\\n",
            "parar sozinha.$",
        ),
    ),
    "SootopolisCity_Text_FlyingMonStoppedRampage": (
        ("flying POKéMON came down",),
        ("MENINO: O GUARDIAO DA TORRE\\n", "fez as correntes recuarem.$"),
    ),
    "SootopolisCity_Text_ThisIsWicked": (
        ("This is wicked",),
        ("GAROTO: Minha cabeca esta cheia\\n", "de lembrancas de outra pessoa.$"),
    ),
    "SootopolisCity_Text_ThatWasWicked": (
        ("That was wicked",),
        ("GAROTO: Parou...\\p", "Mas eu ainda lembro de coisas\\n", "que nunca vivi.$"),
    ),
    "SootopolisCity_Text_GoRedAndBlueMon": (
        ("red POKéMON", "blue POKéMON"),
        (
            "HOMEM: Uma devolve tudo!\\n",
            "A outra leva tudo embora!\\p",
            "Isso vai partir a cidade!$",
        ),
    ),
    "SootopolisCity_Text_DoYouKnowMonNames": (
        ("names of those",),
        (
            "HOMEM: Voce sabe o que sao\\n",
            "essas correntes?\\p",
            "Por que parecem reconhecer a\\n",
            "gente?$",
        ),
    ),
    "SootopolisCity_Text_GreenOneSettlesThings": (
        ("green one that settles",),
        (
            "HOMEM: O GUARDIAO DA TORRE\\n",
            "separou as duas correntes.\\p",
            "So espero que seja suficiente.$",
        ),
    ),
    "SootopolisCity_Text_SeeingLegendWithOwnEyes": (
        ("ancient legend",),
        (
            "HOMEM: Minha avo falava de\\n",
            "IARA-MAE e ANHANGUERA.\\p",
            "Eu achava que era metafora.$",
        ),
    ),
    "SootopolisCity_Text_SawLegendWithOwnEyes": (
        ("I saw that happen",),
        ("HOMEM: Agora eu sei que as\\n", "historias eram aviso, nao lenda.$"),
    ),
    "SootopolisCity_Text_BigPokemonFighting": (
        ("A big POKéMON",),
        (
            "KIRI: Tem gente chorando por\\n",
            "pessoas que nunca conheceu.\\p",
            "Faz isso parar, por favor.$",
        ),
    ),
    "SootopolisCity_Text_PrettyMonCameFromSky": (
        ("pretty POKéMON",),
        (
            "KIRI: O GUARDIAO veio do ceu...\\p",
            "E por um momento todo mundo\\n",
            "lembrou do proprio nome.$",
        ),
    ),
    "SootopolisCity_Text_SootopolisWillBeWrecked": (
        ("AGUAS DE M'BOI will get wrecked",),
        ("MULHER: AGUAS DE M'BOI vai\\n", "se partir desse jeito!$"),
    ),
    "SootopolisCity_Text_SootopolisDidntGetWrecked": (
        ("AGUAS DE M'BOI didn't get wrecked",),
        ("MULHER: A cidade ficou de pe.\\p", "Nem todas as memorias voltaram.$"),
    ),
    "SootopolisCity_Text_CityRegainedCalm": (
        ("city has regained its calm",),
        ("HOMEM: A agua acalmou.\\p", "As pessoas ainda conferem os\\n", "nomes umas das outras.$"),
    ),
    "SootopolisCity_Text_GiganticPokemonFight": (
        ("two POKéMON that gigantic",),
        ("MULHER: Nao e uma batalha.\\p", "As duas correntes estao puxando\\n", "as mesmas pessoas.$"),
    ),
    "SootopolisCity_Text_FearedWorstWhenPokemonFlewDown": (
        ("third POKéMON flew down",),
        (
            "MULHER: Quando o GUARDIAO\\n",
            "desceu, achei que seria pior.\\p",
            "Foi a primeira coisa que as fez\\n",
            "recuar.$",
        ),
    ),
    "SootopolisCity_Text_YouBroughtFlyingMon": (
        ("you who brought that flying",),
        (
            "MULHER: Foi voce quem subiu a\\n",
            "TORRE DO JURAMENTO?\\p",
            "Entao foi voce que chamou o\\n",
            "GUARDIAO.$",
        ),
    ),
    "SootopolisCity_Text_GroudonPleaseStop": (
        ("resultado de duas ideias", "apagar a dor"),
        (
            "LUZIA: IARA-MAE, pare!\\p",
            "Devolver tudo sem escolha nao\\n",
            "e reparacao.\\p",
            "Eu devia ter entendido antes.$",
        ),
    ),
    "SootopolisCity_Text_AfterAllOurScheming": (
        ("IARA-MAE", "ANHANGUERA"),
        (
            "LUZIA: Passei tanto tempo\\n",
            "combatendo o apagamento\\p",
            "que quase transformei lembrar\\n",
            "em outra obrigacao.\\p",
            "Eu errei.$",
        ),
    ),
    "SootopolisCity_Text_KyogreCalmDown": (
        ("resultado de duas ideias", "apagar a dor"),
        (
            "OTACILIO: ANHANGUERA, pare!\\p",
            "Encerrar a dor sem consentimento\\n",
            "e apenas outra forma de poder.$",
        ),
    ),
    "SootopolisCity_Text_TryingMeaninglessToPokemon": (
        ("IARA-MAE", "ANHANGUERA"),
        (
            "OTACILIO: Eu chamei controle\\n",
            "de cuidado por tempo demais.\\p",
            "M'BOI nao me deu o direito de\\n",
            "escolher pelos outros.$",
        ),
    ),
    "SootopolisCity_Text_InvolvedWithCrisisComeWithMe": (
        ("SEU BENTO: Olhe para a agua", "duas correntes antigas"),
        (
            "SEU BENTO: Olhe para a agua.\\p",
            "IARA-MAE e ANHANGUERA foram\\n",
            "forcados a despertar juntos.\\p",
            "Venha. AMALIA precisa de voce\\n",
            "no nucleo da cidade.$",
        ),
    ),
    "SootopolisCity_Text_DoesThisMakeYourFearPokemon": (
        ("aguas carregam lembrancas",),
        (
            "SEU BENTO: O que voce ve nao\\n",
            "e maldade de POKéMON.\\p",
            "Sao VINCULOS sem escolha,\\n",
            "puxados em direcoes opostas.$",
        ),
    ),
    "SootopolisCity_Text_HereWereAreHelpWallace": (
        ("Quando um nome some",),
        (
            "SEU BENTO: AMALIA esta la\\n",
            "dentro.\\p",
            "Ela conhece a historia da\\n",
            "TORRE DO JURAMENTO.\\p",
            "Escute o que ela descobriu.$",
        ),
    ),
    "SootopolisCity_Text_KnowWhatsNeededToHelpHim": (
        ("Quando um nome some",),
        (
            "SEU BENTO: AMALIA encontrou um\\n",
            "registro antigo da TORRE.\\p",
            "Ela acha que existe uma terceira\\n",
            "forca capaz de separar as duas.$",
        ),
    ),
    "SootopolisCity_Text_NeverBeenToSkyPillar": (
        ("Quando um nome some",),
        (
            "SEU BENTO: A TORRE fica alem\\n",
            "das rotas do oeste.\\p",
            "AMALIA abriu o caminho.\\p",
            "Suba. Eu fico com a cidade.$",
        ),
    ),
    "SootopolisCity_Text_SoThatsRayquaza": (
        ("IARA-MAE", "ANHANGUERA"),
        (
            "SEU BENTO: Entao o GUARDIAO\\n",
            "respondeu ao JURAMENTO.\\p",
            "Nao para decidir por nos.\\p",
            "Para impedir que alguem decida\\n",
            "sozinho por todos.$",
        ),
    ),
    "SootopolisCity_Text_MaxieArchieLeft": (
        ("IARA-MAE", "ANHANGUERA"),
        (
            "SEU BENTO: LUZIA e OTACILIO\\n",
            "voltaram ao MEMORIAL.\\p",
            "Desta vez, para devolver o que\\n",
            "tiraram.$",
        ),
    ),
    "SootopolisCity_Text_LeadSuperiorTrainerToCave": (
        ("superior talent", "AMALIA"),
        (
            "GUARDIA: SEU BENTO pediu que\\n",
            "eu deixasse voce passar.\\p",
            "AMALIA esta no nucleo.\\p",
            "A cidade precisa de uma decisao\\n",
            "que nao venha de uma faccao.$",
        ),
    ),
    "SootopolisCity_Text_AwakenedPokemonClash": (
        ("two awakened", "third POKéMON"),
        (
            "GUARDIA: As duas correntes\\n",
            "cederam diante de uma terceira.\\p",
            "Nunca vi o JURAMENTO responder\\n",
            "assim.$",
        ),
    ),
    "SootopolisCity_Text_CaveOfOriginSleepsToo": (
        ("GRUTA DA ORIGEM", "cave, too, shall sleep"),
        (
            "GUARDIA: O nucleo voltou a\\n",
            "silenciar.\\p",
            "Que continue sendo memoria,\\n",
            "nao ferramenta.$",
        ),
    ),
    "SootopolisCity_Text_HaventYouScaledSkyPillar": (
        ("AMALIA", "Liga tambem tem"),
        (
            "AMALIA: A cidade piora a cada\\n",
            "minuto.\\p",
            "A TORRE DO JURAMENTO ainda\\n",
            "e nossa unica opcao. Va!$",
        ),
    ),
    "SootopolisCity_Text_AquaMagmaDidntMeanHarm": (
        ("AMALIA", "LEMBRANTES and AQUA"),
        (
            "AMALIA: LUZIA e OTACILIO\\n",
            "precisam responder pelo que\\n",
            "fizeram.\\p",
            "Mas primeiro precisamos impedir\\n",
            "que a cidade perca a si mesma.$",
        ),
    ),
    "SootopolisCity_Text_ThankYouForHelpAcceptThis": (
        ("AMALIA", "verdade pela metade"),
        (
            "AMALIA: Voce impediu que duas\\n",
            "ideias virassem sentenca.\\p",
            "Aceite isto. Ainda ha caminho\\n",
            "pela frente.$",
        ),
    ),
    "SootopolisCity_Text_DazzledByMentor": (
        ("AMALIA", "verdade pela metade"),
        (
            "AMALIA: A TORRE respondeu a\\n",
            "voce, nao a uma ordem minha.\\p",
            "Quando entrar no GINASIO,\\n",
            "carregue isso com voce.$",
        ),
    ),
}

TOWER_TARGETS: dict[str, tuple[tuple[str, ...], tuple[str, ...]]] = {
    "SkyPillar_Outside_Text_OpenedDoorToSkyPillar": (
        ("AMALIA: Abri a entrada", "TORRE JURAMENTO"),
        (
            "AMALIA: Abri a entrada.\\p",
            "A TORRE DO JURAMENTO reagiu\\n",
            "ao colapso em M'BOI.\\p",
            "Vamos subir antes que piore.$",
        ),
    ),
    "SkyPillar_Outside_Text_EarthquakeNotMomentToWaste": (
        ("AMALIA: Um tremor", "Precisamos subir"),
        (
            "AMALIA: Outro tremor!\\p",
            "As duas correntes ainda estao\\n",
            "forcando a cidade.\\p",
            "Continue.$",
        ),
    ),
    "SkyPillar_Outside_Text_SituationGettingWorse": (
        ("AMALIA: Espere", "AGUAS DE M'BOI"),
        (
            "AMALIA: Espere...\\p",
            "As leituras mudaram de novo.\\p",
            "Algo em AGUAS DE M'BOI esta\\n",
            "cedendo.$",
        ),
    ),
    "SkyPillar_Outside_Text_GotToGoBackForSootopolis": (
        ("AGUAS DE M'BOI", "RAYQUAZA"),
        (
            "AMALIA: Preciso voltar para\\n",
            "AGUAS DE M'BOI.\\p",
            "Voce continua subindo.\\p",
            "Encontre o GUARDIAO DA TORRE.$",
        ),
    ),
}


def block_pattern(label: str) -> re.Pattern[str]:
    return re.compile(rf"(?ms)^{re.escape(label)}:\n(?P<body>.*?)(?=^[A-Za-z0-9_]+(?:::|:)(?:\n|$)|\Z)")


def visible_segments(payload: str) -> list[str]:
    cleaned = PLACEHOLDER_RE.sub("", payload).replace("$", "")
    return [part.strip() for part in CONTROL_RE.split(cleaned)]


def validate_widths(targets: dict[str, tuple[tuple[str, ...], tuple[str, ...]]]) -> None:
    for label, (_, payloads) in targets.items():
        for payload in payloads:
            for segment in visible_segments(payload):
                if len(segment) > MAX_VISIBLE_WIDTH:
                    raise ValueError(f"{label}: {len(segment)} visible chars: {segment!r}")


def replace_blocks(source: str, targets: dict[str, tuple[tuple[str, ...], tuple[str, ...]]]) -> str:
    rendered = source
    for label, (markers, payloads) in targets.items():
        pattern = block_pattern(label)
        matches = list(pattern.finditer(rendered))
        if len(matches) != 1:
            raise ValueError(f"{label}: expected one block, found {len(matches)}")
        body = matches[0].group("body")
        if ".string" not in body:
            raise ValueError(f"{label}: missing .string data")
        for marker in markers:
            if marker not in body:
                raise ValueError(f"{label}: source marker missing: {marker!r}")
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


def render(source: str, targets: dict[str, tuple[tuple[str, ...], tuple[str, ...]]]) -> str:
    validate_widths(targets)
    rendered = replace_blocks(source, targets)
    labels = tuple(targets)
    if mask_blocks(source, labels) != mask_blocks(rendered, labels):
        raise ValueError("non-dialogue structure changed while rendering")
    return rendered


def render_city(source: str) -> str:
    rendered = render(source, CITY_TARGETS)
    forbidden = (
        "SOOTOPOLIS CITY will get wrecked",
        "SOOTOPOLIS CITY didn't get wrecked",
        "LEMBRANTES and AQUA",
        "WALLACE:",
        "The door is closed",
    )
    for token in forbidden:
        for label in CITY_TARGETS:
            body = block_pattern(label).search(rendered).group("body")
            if token in body:
                raise ValueError(f"{label}: legacy visible token survived: {token}")
    return rendered


def render_tower(source: str) -> str:
    rendered = render(source, TOWER_TARGETS)
    body = block_pattern("SkyPillar_Outside_Text_GotToGoBackForSootopolis").search(rendered).group("body")
    if "RAYQUAZA" in body:
        raise ValueError("visible RAYQUAZA survived tower handoff")
    return rendered


def rendered_sources() -> dict[Path, str]:
    city = CITY_PATH.read_text(encoding="utf-8")
    tower = TOWER_PATH.read_text(encoding="utf-8")
    return {CITY_PATH: render_city(city), TOWER_PATH: render_tower(tower)}


def main() -> int:
    parser = argparse.ArgumentParser(description="Render Aguas de M'Boi crisis and Torre do Juramento handoff surfaces.")
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--in-place", action="store_true")
    args = parser.parse_args()
    if args.check and args.in_place:
        parser.error("use either --check or --in-place")

    rendered = rendered_sources()
    if args.check:
        print(
            "Aguas/Torre renderer OK: "
            f"{len(CITY_TARGETS)} city blocks and {len(TOWER_TARGETS)} tower blocks validated."
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
