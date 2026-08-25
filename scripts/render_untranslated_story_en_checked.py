#!/usr/bin/env python3
"""Translate the story dialogue that was still shipping in Portuguese.

The build is English-only, but fourteen blocks of Arauna's own story text --
CIRO on Route 104, the HORIZONTE guards on Route 119, the agent at the
CAVERNAS M'BOI entrance, AMALIA at the LEAGUE, and three place signs -- were
never translated. check_english_only_policy.py checks the build wiring and
the residue audit's Portuguese markers are all accented, so unaccented
Portuguese passed both.

This runs before render_legacy_place_names_en_checked.py, so the two
Seafloor blocks are keyed on LEMBRANTES, the name they still carry at that
point; the English text uses REMEMBRANCERS, which that renderer then leaves
alone.

Each entry is pinned to the exact payload it replaces, so the renderer fails
loudly rather than half-matching if the upstream text is edited. Several
payloads appear under more than one label, which is why replacement is keyed
on the text rather than the label.

MAX_LINE_PX matches render_legacy_place_names_en_checked.py: 208px in
FONT_NORMAL, measured off the widest placeholder-free line Emerald ships.
"""
from __future__ import annotations

import argparse
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MAX_LINE_PX = 208

FILES = (
    "data/maps/EverGrandeCity_HallOfFame/scripts.inc",
    "data/maps/LittlerootTown/scripts.inc",
    "data/maps/LittlerootTown_MaysHouse_2F/scripts.inc",
    "data/maps/Route104/scripts.inc",
    "data/maps/Route119/scripts.inc",
    "data/maps/SeafloorCavern_Entrance/scripts.inc",
    "data/maps/SkyPillar_Top/scripts.inc",
    "data/maps/SootopolisCity/scripts.inc",
    "data/maps/SootopolisCity_PokemonCenter_1F/scripts.inc",
)

TRANSLATIONS = {
    "AMALIA: A Liga registra quem\\nchega ate aqui sem apagar\\pas marcas do caminho.$":
        "AMALIA: The LEAGUE records who\\ngets this far without erasing\\lthe marks the road left.$",

    "AMALIA: Seu nome e o dos seus\\nparceiros entram agora\\pna memoria de Arauna.$":
        "AMALIA: Your name and your\\npartners' names enter the\\lmemory of Arauna now.$",

    "VILA AMANHECER. Aqui o\\nJuramento ainda e contado de\\pboca em boca. Dona Zila diz que\\num nome so morre quando ninguem\\pmais o pronuncia.$":
        "VILA AMANHECER. Here the\\nJURAMENTO is still passed on\\lby word of mouth.\\pDONA ZILA says a name only\\ndies when nobody says it\\lany more.$",

    "CIRO: O HORIZONTE nao me pediu\\npara esquecer nada. So me\\pmostrou que existe um futuro\\nque nao precisa ser governado\\ppelo passado.$":
        "CIRO: HORIZONTE never asked me\\nto forget anything.\\pIt only showed me there is a\\nfuture that does not have to\\lbe ruled by the past.$",

    "CIRO: Nao confunda minha pressa\\ncom falta de memoria. Eu lembro\\po bastante para saber que nao\\nquero viver preso ao que perdi.$":
        "CIRO: Don't mistake my hurry\\nfor a short memory.\\pI remember enough to know I\\ndon't want to live tied to\\lwhat I lost.$",

    "CIRO: Voce continua olhando\\npara cada cicatriz como se ela\\pfosse uma resposta. Eu quero\\nsaber o que existe depois dela.$":
        "CIRO: You keep looking at every\\nscar as if it were an answer.\\pI want to know what comes\\nafter it.$",

    "HORIZONTE: Estamos isolando\\no INSTITUTO DAS AGUAS.\\pNao se aproxime enquanto a\\noperacao estiver em andamento.$":
        "HORIZONTE: We are sealing off\\nthe INSTITUTO DAS AGUAS.\\pStay back while the operation\\nis under way.$",

    "HORIZONTE: Vigiar esta ponte\\ne mais tedioso do que parece.\\pMesmo assim, nao chegue perto\\ndo INSTITUTO DAS AGUAS.$":
        "HORIZONTE: Watching this bridge\\nis duller than it sounds.\\pEven so, keep away from the\\nINSTITUTO DAS AGUAS.$",

    "AGENTE: Recebemos noticia dos\\nLEMBRANTES perto de MISSOES DO\\nCEU.\\pLUZIA esta mobilizando gente\\nfora daqui. OTACILIO mandou\\nmanter o foco em M'BOI.$":
        "AGENT: Word came in about the\\nREMEMBRANCERS near MISSOES DO\\lCEU.\\pLUZIA is pulling people out.\\nOTACILIO said keep the focus\\lon M'BOI.$",

    "LEMBRANTES perto de MISSOES DO\\nCEU... e nos presos aqui.$":
        "REMEMBRANCERS near MISSOES DO\\nCEU... and here we are, stuck.$",

    "O JURAMENTO nunca prometeu\\nmemoria perfeita. Prometeu que\\pnenhuma pessoa escolheria\\nsozinha o que todos os outros\\pdeveriam esquecer.$":
        "The JURAMENTO never promised\\nperfect memory.\\pIt promised that no one person\\nwould decide alone what\\leveryone else must forget.$",

    "AGUAS DE M'BOI. O colapso do\\nArquivo espalha lembrancas\\palheias e vazios de memoria por\\ntoda Arauna.$":
        "AGUAS DE M'BOI. The collapse of\\nthe ARCHIVE spreads other\\lpeople's memories, and gaps\\lwhere memory should be, right\\lacross Arauna.$",

    "As aguas carregam lembrancas\\nque nao pertencem a quem as\\precebe. Pessoas reconhecem\\nnomes que nunca ouviram e\\pesquecem rostos que amam.$":
        "The waters carry memories that\\nbelong to someone else.\\pPeople know names they never\\nheard, and forget faces they\\llove.$",

    "AMALIA: Arauna sobreviveu a\\nverdade pela metade por tempo\\pdemais. A Liga tambem tem\\ndividas com quem foi apagado.$":
        "AMALIA: Arauna has lived on\\nhalf the truth for far too\\llong.\\pThe LEAGUE owes a debt too, to\\neveryone who was erased.$",
}

STRING_RE = re.compile(r'(?P<indent>[ \t]*)\.string[ \t]+"(?P<body>(?:[^"\\]|\\.)*)"')
BLOCK_RE = re.compile(r'(?:^[ \t]*\.string[ \t]+"(?:[^"\\]|\\.)*"\n)+', re.M)


def fail(message: str) -> None:
    raise SystemExit(f"Untranslated story renderer FAILED: {message}")


def _load_metrics() -> tuple[list[int], dict[str, int]]:
    fonts = (ROOT / "src" / "fonts.c").read_text(encoding="utf-8")
    body = re.search(r"gFontNormalLatinGlyphWidths\[\] = \{(.*?)\};", fonts, re.S)
    widths = [int(n) for n in re.findall(r"\d+", body.group(1))]
    charmap: dict[str, int] = {}
    for line in (ROOT / "charmap.txt").read_text(encoding="utf-8").splitlines():
        line = line.split("@")[0].strip()
        match = re.match(r"^'(\\?.)'\s*=\s*([0-9A-Fa-f]{2})$", line)
        if match:
            char = match.group(1)
            charmap["'" if char == "\\'" else char] = int(match.group(2), 16)
    return widths, charmap


GLYPH_WIDTHS, CHARMAP = _load_metrics()
BRACE_RE = re.compile(r"\{[^}]*\}")


def line_px(text: str) -> int:
    return sum(GLYPH_WIDTHS[CHARMAP[c]] for c in BRACE_RE.sub("", text.replace("$", ""))
               if c in CHARMAP)


def validate_translations() -> None:
    for portuguese, english in TRANSLATIONS.items():
        if portuguese.endswith("$") != english.endswith("$"):
            fail(f"terminator lost: {portuguese[:40]!r}")
        for line in re.split(r"\\[nlp]", english):
            if line.strip() and line_px(line) > MAX_LINE_PX:
                fail(f"{line_px(line)}px line does not fit the box: {line!r}")
        for page in english.split("\\p"):
            breaks = re.findall(r"\\[nl]", page)
            if breaks and (breaks[0] != "\\n" or any(b != "\\l" for b in breaks[1:])):
                fail(f"bad line-break pattern in {page[:48]!r}")


def render_file(source: str, rel: str) -> tuple[str, int]:
    out: list[str] = []
    last = 0
    hits = 0
    for block in BLOCK_RE.finditer(source):
        payload = "".join(m.group("body") for m in STRING_RE.finditer(block.group(0)))
        english = TRANSLATIONS.get(payload)
        if english is None:
            continue
        indent = STRING_RE.search(block.group(0)).group("indent")
        pieces = [p for p in re.split(r'(?<=\\n)|(?<=\\l)|(?<=\\p)', english) if p]
        out.append(source[last:block.start()])
        out.append("".join(f'{indent}.string "{p}"\n' for p in pieces))
        last = block.end()
        hits += 1
    out.append(source[last:])
    return "".join(out), hits


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--in-place", action="store_true")
    args = parser.parse_args()
    if args.check and args.in_place:
        parser.error("use either --check or --in-place")

    validate_translations()

    total = 0
    for rel in FILES:
        path = ROOT / rel
        source = path.read_text(encoding="utf-8")
        rendered, hits = render_file(source, rel)
        if hits == 0 and not any(e in source for e in TRANSLATIONS.values()):
            fail(f"{rel}: no block matched and no translation is present")
        total += hits
        if args.in_place and rendered != source:
            path.write_text(rendered, encoding="utf-8")

    mode = "Translated" if args.in_place else "Validated"
    print(f"{mode} Portuguese story dialogue: {total} block site(s), "
          f"{len(TRANSLATIONS)} texts.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
