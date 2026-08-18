#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONTROL_RE = re.compile(r"\\[npl]|\{[^}]+\}")
BLOCK_RE_TEMPLATE = r'(?m)^{label}:\n(?:\t\.string "[^\n]*"\n)+'

TARGETS: dict[Path, dict[str, tuple[str, ...]]] = {
    ROOT / "data/maps/SeafloorCavern_Room9/scripts.inc": {
        "SeafloorCavern_Room9_Text_ArchieHoldItRightThere": (
            r"OTACILIO: Pare ai, {PLAYER}.\p",
            r"Voce ja viu demais para achar\n",
            r"que isto e so pesquisa.\p",
            r"Eu vim encerrar uma ferida que\n",
            r"Arauna deixou aberta.$",
        ),
        "SeafloorCavern_Room9_Text_ArchieSoItWasYou": (
            r"OTACILIO: Foi voce quem rompeu\n",
            r"nossas linhas ate aqui.\p",
            r"Entao veja com seus proprios\n",
            r"olhos o que o ARQUIVO esconde.$",
        ),
        "SeafloorCavern_Room9_Text_ArchieBeholdKyogre": (
            r"OTACILIO: KYOGRE dorme ligado a\n",
            r"VINCULOS que nenhum sensor le.\p",
            r"Se eu quebrar esse ciclo, talvez\n",
            r"M'BOI enfim consiga esquecer.$",
        ),
        "SeafloorCavern_Room9_Text_ArchieYouMustDisappear": (
            r"OTACILIO: Nao vou deixar voce\n",
            r"impedir isso agora.\p",
            r"Se precisa me enfrentar para\n",
            r"seguir, entao venha.$",
        ),
        "SeafloorCavern_Room9_Text_ArchieDefeat": (
            r"OTACILIO: ...Ainda assim voce\n",
            r"continua.$",
        ),
        "SeafloorCavern_Room9_Text_ArchieWithThisRedOrb": (
            r"OTACILIO: O orbe respondeu...\n",
            r"Nao fui eu que o ativei.$",
        ),
        "SeafloorCavern_Room9_Text_RedOrbShinesByItself": (
            r"O orbe vermelho brilha sozinho.$",
        ),
        "SeafloorCavern_Room9_Text_ArchieWhereDidKyogreGo": (
            r"OTACILIO: KYOGRE?!\n",
            r"Onde ele foi?$",
        ),
        "SeafloorCavern_Room9_Text_ArchieAMessageFromOutside": (
            r"OTACILIO: Uma mensagem de fora?$",
        ),
        "SeafloorCavern_Room9_Text_ArchieWhatRainingTooHard": (
            r"OTACILIO: Chuva em toda Arauna?\p",
            r"Isso nao era para acontecer.$",
        ),
        "SeafloorCavern_Room9_Text_ArchieWhyDidKyogreDisappear": (
            r"OTACILIO: O que eu libertei...?$",
        ),
        "SeafloorCavern_Room9_Text_MaxieWhatHaveYouWrought": (
            r"LUZIA: Olhe ao redor, OTACILIO.\p",
            r"Voce tentou apagar a dor e\n",
            r"soltou algo que nao entende.$",
        ),
        "SeafloorCavern_Room9_Text_ArchieDontGetAllHighAndMighty": (
            r"OTACILIO: Nao venha posar de\n",
            r"juiza. Voce faria o oposto sem\n",
            r"perguntar a ninguem.$",
        ),
        "SeafloorCavern_Room9_Text_MaxieWeDontHaveTimeToArgue": (
            r"LUZIA: Nao temos tempo para\n",
            r"discutir.\p",
            r"Precisamos impedir que isso\n",
            r"atinja o resto de Arauna.$",
        ),
        "SeafloorCavern_Room9_Text_MaxieComeOnPlayer": (
            r"LUZIA: {PLAYER}, venha.\p",
            r"Isso tambem e responsabilidade\n",
            r"nossa. Vamos sair daqui.$",
        ),
    },
    ROOT / "data/maps/Route128/scripts.inc": {
        "Route128_Text_ArchieWhatHappened": (
            r"OTACILIO: A chuva...\n",
            r"Ela esta se espalhando.$",
        ),
        "Route128_Text_ArchieIOnlyWanted": (
            r"OTACILIO: Eu so queria romper\n",
            r"os VINCULOS que mantinham a dor.\p",
            r"Nao queria entregar Arauna a\n",
            r"outro desastre.$",
        ),
        "Route128_Text_MaxieDoYouUnderstandNow": (
            r"LUZIA: Entende agora?\p",
            r"Nenhum de nos tinha o direito\n",
            r"de decidir sozinho.$",
        ),
        "Route128_Text_MaxieResposibilityFallsToArchieAndMe": (
            r"LUZIA: A responsabilidade e\n",
            r"nossa, OTACILIO. Dos dois.\p",
            r"Vamos corrigir o que causamos.$",
        ),
        "Route128_Text_MaxieThisDefiesBelief": (
            r"LUZIA: Nem eu consigo explicar\n",
            r"o que esta acontecendo.\p",
            r"Se as correntes chegarem a\n",
            r"AGUAS DE M'BOI, sera pior.$",
        ),
        "Route128_Text_StevenWhatIsHappening": (
            r"SEU BENTO: {PLAYER}! O mar e o\n",
            r"ceu mudaram ao mesmo tempo.\p",
            r"O que aconteceu la embaixo?$",
        ),
        "Route128_Text_StevenWholeWorldWillDrown": (
            r"SEU BENTO: Se isso continuar,\n",
            r"Arauna inteira vai sentir.\p",
            r"Nao e uma tempestade comum.$",
        ),
        "Route128_Text_StevenImGoingToSootopolis": (
            r"SEU BENTO: Vou para AGUAS DE\n",
            r"M'BOI. A origem deve estar la.\p",
            r"Encontre-me assim que puder.$",
        ),
    },
}


def block_re(label: str) -> re.Pattern[str]:
    return re.compile(BLOCK_RE_TEMPLATE.format(label=re.escape(label)))


def render(label: str, lines: tuple[str, ...]) -> str:
    return label + ":\n" + "".join(f'\t.string "{line}"\n' for line in lines)


def visible_segments(line: str) -> list[str]:
    plain = CONTROL_RE.sub("|", line).replace("$", "")
    return [segment for segment in plain.split("|") if segment]


def validate_expected() -> list[str]:
    failures: list[str] = []
    for path, replacements in TARGETS.items():
        text = path.read_text(encoding="utf-8")
        for label, lines in replacements.items():
            expected = render(label, lines)
            if expected not in text:
                failures.append(f"{path}: expected block missing for {label}")
            for line in lines:
                for segment in visible_segments(line):
                    if len(segment) > 32:
                        failures.append(
                            f"{path}: {label}: segment wider than 32 chars: {segment!r}"
                        )
    return failures


def apply() -> int:
    for path, replacements in TARGETS.items():
        text = path.read_text(encoding="utf-8")
        changed = 0
        for label, lines in replacements.items():
            pattern = block_re(label)
            replacement = render(label, lines)
            text, count = pattern.subn(lambda _: replacement, text, count=1)
            if count != 1:
                raise RuntimeError(f"{path}: expected exactly one block for {label}, got {count}")
            changed += 1
        path.write_text(text, encoding="utf-8")
        print(f"{path.relative_to(ROOT)}: {changed} dialogue blocks contextualized")

    failures = validate_expected()
    if failures:
        raise RuntimeError("; ".join(failures))
    return 0


def check() -> int:
    failures = validate_expected()
    if failures:
        print("Caverna Abissal crisis continuity check FAILED:")
        for failure in failures:
            print(f"- {failure}")
        return 1
    print("Caverna Abissal crisis continuity check PASS.")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    return check() if args.check else apply()


if __name__ == "__main__":
    raise SystemExit(main())
