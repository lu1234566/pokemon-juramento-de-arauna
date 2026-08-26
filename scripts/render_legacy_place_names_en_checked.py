#!/usr/bin/env python3
"""Rename the legacy Hoenn places and factions left in dialogue.

The region map, the landmark bar and the story renderers all carry Arauna
names, but ordinary dialogue -- trainers, TV, news, signposts, the Battle
Circuit lobbies -- still called places by their Emerald names. The visible
residue audit had been listing those as an advisory inventory for a while.

This renderer is deliberately content-driven rather than pinned to specific
text: it runs last, after the 66 story renderers have already rewritten large
parts of these files, so what it sees depends on all of them. Instead of
asserting what the text says, it asserts what the transformation may do:

  * only the payload of `.string` directives is touched, never a label,
    a macro argument or a script command;
  * the sequence of control markers (\\n \\l \\p, the $ terminator, and every
    {...} code) is identical before and after;
  * the word sequence is identical to the substituted text, so reflowing
    cannot drop, duplicate or reorder a word;
  * every line whose width does not depend on a runtime buffer fits the
    message box.

MAX_LINE_PX is measured, not guessed. Across all 23,247 placeholder-free
dialogue lines Emerald ships, the widest is exactly 208px in FONT_NORMAL, and
hundreds sit on that value -- it is the box. Lines holding {PLAYER} or
{STR_VAR_n} are excluded from the check because their real width depends on a
name entered at runtime, and vanilla itself exceeds 208 when those are
modelled at their maximum.

Reflow is applied only to a page that actually overflows, so a longer name
does not rewrap dialogue that was already fine.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# Every name the visible-residue audit tracks, plus the two faction names that
# survived in Portuguese. Applied longest-first so PETALBURG WOODS is not eaten
# by PETALBURG, and SLATEPORT BEACH not by SLATEPORT CITY.
CANON = {
    "MR. BRINEY'S COTTAGE": "SAILOR'S COTTAGE",
    "SAFARI ZONE ENTRANCE": "ARAUNA PRESERVE",
    "CONSORCIO HORIZONTE": "HORIZONTE",
    "EVER GRANDE CITY": "ESTR. JURAMENTO",
    "SOOTOPOLIS CITY": "AGUAS DE M'BOI",
    "SLATEPORT BEACH": "PORTO DO SAL BEACH",
    "SEAFLOOR CAVERN": "CAVERNAS M'BOI",
    "PACIFIDLOG TOWN": "CASA DA FOGUEIRA",
    "VERDANTURF TOWN": "VALE DO SILENCIO",
    "DESERT UNDERPASS": "TUNEL DA AREIA",
    "LITTLEROOT TOWN": "VILA AMANHECER",
    "FRONTIER BRAINS": "CIRCUIT MASTERS",
    "SOUTHERN ISLAND": "ILHA DO SUL",
    "BATTLE FRONTIER": "BATTLE CIRCUIT",
    "PETALBURG WOODS": "MATA DA ESPERA",
    "SEALED CHAMBER": "CAMARA SELADA",
    "FALLARBOR TOWN": "CAMPO DAS CINZAS",
    "PETALBURG CITY": "PAMPA DA ESPERA",
    "SLATEPORT CITY": "PORTO DO SAL",
    "RUSTURF TUNNEL": "GALERIAS SERRA",
    "LAVARIDGE TOWN": "SERTAO DE DENTRO",
    "ABANDONED SHIP": "NAVIO PERDIDO",
    "CAVE OF ORIGIN": "M'BOI CORE",
    "OLDALE TOWN": "VILA DA PASSAGEM",
    "SCORCHED SLAB": "LAJE QUEIMADA",
    "MAGMA HIDEOUT": "REMEMBRANCERS BASE",
    "ALTERING CAVE": "TOCA MUTAVEL",
    "MIRAGE ISLAND": "ILHA MIRAGEM",
    "MOSSDEEP CITY": "MISSOES DO CEU",
    "LILYCOVE CITY": "BAIA DAS LUZES",
    "MAUVILLE CITY": "ENCRUZILHADA",
    "RUSTBORO CITY": "SERRA DO UIVO",
    "DESERT RUINS": "RUINAS DA AREIA",
    "DEWFORD TOWN": "PORTO DAS REDES",
    "FRONTIER PASS": "CIRCUIT PASS",
    "GRANITE CAVE": "GRUTA DAS VOZES",
    "FORTREE CITY": "MATA DO MEIO",
    "NEW MAUVILLE": "OLD POWER RELAY",
    "METEOR FALLS": "RUINAS DA QUEDA",
    "MIRAGE TOWER": "TORRE MIRAGEM",
    "ARTISAN CAVE": "LAPA DO ARTESAO",
    "TRAINER HILL": "MORRO DOS DUELOS",
    "ANCIENT TOMB": "TUMBA ANTIGA",
    "ISLAND CAVE": "GRUTA DO GELO",
    "JAGGED PASS": "PASSO CORTADO",
    "LEMBRANTES": "REMEMBRANCERS",
    "SKY PILLAR": "TORRE JURAMENTO",
    "SHOAL CAVE": "FURNA DA MARE",
    "FIERY PATH": "TRILHA DE FOGO",
    "DEVON CORP": "HORIZONTE",
    "TEAM MAGMA": "REMEMBRANCERS",
    "TEAM AQUA": "HORIZONTE",
    "MT. PYRE": "MEMORIAL NOMES",
    "HOENN": "ARAUNA",
    # And the same settlements without the TOWN or CITY after them. Dialogue
    # drops the suffix constantly - "ferry ports in SLATEPORT and LILYCOVE",
    # "I hiked over from MAUVILLE" - and every one of those survived, because
    # the entries above only match the full form. That is where the 137
    # readable mentions of Hoenn in the built ROM were. Applied after the
    # suffixed forms by ORDER, which sorts longest first, so PETALBURG WOODS
    # and NEW MAUVILLE are still taken whole.
    #
    # Each name is the one the region map itself shows, so the town a person
    # names is the town on the map screen.
    "PACIFIDLOG": "CASA DA FOGUEIRA",
    "VERDANTURF": "VALE DO SILENCIO",
    "LITTLEROOT": "VILA AMANHECER",
    "EVER GRANDE": "ESTR. JURAMENTO",
    "SOOTOPOLIS": "AGUAS DE M'BOI",
    "LAVARIDGE": "SERTAO DE DENTRO",
    "PETALBURG": "PAMPA DA ESPERA",
    "FALLARBOR": "CAMPO DAS CINZAS",
    "SLATEPORT": "PORTO DO SAL",
    "MOSSDEEP": "MISSOES DO CEU",
    "RUSTBORO": "SERRA DO UIVO",
    "LILYCOVE": "BAIA DAS LUZES",
    "MAUVILLE": "ENCRUZILHADA",
    "DEWFORD": "PORTO DAS REDES",
    "FORTREE": "MATA DO MEIO",
    "OLDALE": "VILA DA PASSAGEM",
}
ORDER = sorted(CANON, key=len, reverse=True)

# Four location labels in src/strings.c that the story renderers missed. Their
# neighbours in the same block are already Arauna names, and they feed the same
# multichoice menus in src/data/script_menu.h, so they are replaced whole.
C_DECLS = {
    'const u8 gText_SouthernIsland[] = _("SOUTHERN ISLAND");':
        'const u8 gText_SouthernIsland[] = _("ILHA DO SUL");',
    'const u8 gText_CaveOfOrigin[] = _("CAVE OF ORIGIN");':
        'const u8 gText_CaveOfOrigin[] = _("M\'BOI CORE");',
    'const u8 gText_MtPyre[] = _("MT. PYRE");':
        'const u8 gText_MtPyre[] = _("MEMORIAL NOMES");',
    'const u8 gText_SkyPillar[] = _("SKY PILLAR");':
        'const u8 gText_SkyPillar[] = _("TORRE JURAMENTO");',
}
C_DECLS_PATH = ROOT / "src" / "strings.c"

# Visible text the residue audit never looked at, because it only reads .inc
# files and five C files. These carry legacy names into item descriptions, the
# battle-record prompt and a Match Call line.
C_TEXT_FILES = (
    "src/data/text/item_descriptions.h",
    "src/battle_message.c",
    "src/data/text/match_call_messages.h",
)
# Plain substitution would give "REMEMBRANCERS's mark.", which is both a double
# possessive and 116px in a 102px box.
C_LITERAL_OVERRIDES = {
    # Keyed on the text as it stands before substitution.
    '"A medal-like item in\\n" "the same shape as\\n" "TEAM MAGMA\'s mark."':
        '"A medal-like item in\\n" "the same shape as\\n" "the REMEMBRANCERS."',
    # "a distant southern island" is prose in vanilla, but this is the ticket
    # to the Lati@s island, so it names the place instead.
    '"The ticket for a\\n" "ferry to a distant\\n" "southern island."':
        '"The ticket for a\\n" "ferry out to\\n" "ILHA DO SUL."',
    # NEW MAUVILLE is broken across a line here, so the pair never matches as
    # one and the bare name below it takes over: "ENCRUZILHADA beneath" is
    # 117px in a 102px box. Written out whole instead, at 72, 95 and 75px.
    '"The key for NEW\\n" "MAUVILLE beneath\\n" "MAUVILLE CITY."':
        '"Opens the OLD\\n" "POWER RELAY under\\n" "ENCRUZILHADA."',
}
C_LITERAL_RE = re.compile(r'_\(\s*((?:"(?:[^"\\]|\\.)*"\s*)+)\)')
C_ONE_RE = re.compile(r'"((?:[^"\\]|\\.)*)"')
# Runtime buffers in battle text, on top of the overworld ones.
C_RUNTIME_RE = re.compile(r'\{(PLAYER|RIVAL|STR_VAR_\d|POKEBLOCK|B_[A-Z_0-9]+)[^}]*\}')

MAX_LINE_PX = 208

STRING_RE = re.compile(r'(?P<indent>[ \t]*)\.string[ \t]+"(?P<body>(?:[^"\\]|\\.)*)"')
BLOCK_RE = re.compile(r'(?:^[ \t]*\.string[ \t]+"(?:[^"\\]|\\.)*"\n)+', re.M)
MARKER_RE = re.compile(r'\\[nlp]|\{[^}]*\}|\$')
# Reflow is allowed to move a line break inside a page, so \n and \l are
# compared per page rather than as part of the global marker sequence.
STRUCTURE_RE = re.compile(r'\\p|\{[^}]*\}|\$')
# Placeholders whose printed width is only known at runtime.
RUNTIME_RE = re.compile(r'\{(PLAYER|RIVAL|STR_VAR_\d|POKEBLOCK)[^}]*\}')


def fail(message: str) -> None:
    raise SystemExit(f"Legacy place-name renderer FAILED: {message}")


# --- width, using the game's own font metrics -------------------------------

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
# Widest runtime expansion, from include/constants/global.h; every other brace
# code is a control code that draws nothing.
PLACEHOLDER_TEXT = {
    "{PLAYER}": "W" * 7, "{RIVAL}": "W" * 7,
    "{STR_VAR_1}": "W" * 10, "{STR_VAR_2}": "W" * 10, "{STR_VAR_3}": "W" * 10,
    "{POKEBLOCK}": "W" * 10, "{PKMN}": "WW",
    "{UP_ARROW}": "W", "{DOWN_ARROW}": "W", "{LEFT_ARROW}": "W", "{RIGHT_ARROW}": "W",
}
BRACE_RE = re.compile(r"\{[^}]*\}")


def line_px(text: str) -> int:
    expanded = BRACE_RE.sub(lambda m: PLACEHOLDER_TEXT.get(m.group(0), ""), text.replace("$", ""))
    return sum(GLYPH_WIDTHS[CHARMAP[c]] for c in expanded if c in CHARMAP)


# --- transformation ---------------------------------------------------------

def substitute(payload: str) -> str:
    for old in ORDER:
        payload = payload.replace(old, CANON[old])
    return payload


def reflow_page(page: str) -> str:
    """Re-break one page's lines to fit the box, keeping every word."""
    words = re.split(r"\\[nl]", page)
    flat = " ".join(part.strip() for part in words if part.strip()).split(" ")
    lines: list[str] = []
    current = ""
    for word in flat:
        candidate = f"{current} {word}".strip()
        if current and line_px(candidate) > MAX_LINE_PX:
            lines.append(current)
            current = word
        else:
            current = candidate
    if current:
        lines.append(current)
    if not lines:
        return page
    out = lines[0]
    for index, line in enumerate(lines[1:]):
        out += ("\\n" if index == 0 else "\\l") + line
    return out


def page_overflows(page: str) -> bool:
    for line in re.split(r"\\[nl]", page):
        if RUNTIME_RE.search(line):
            continue
        if line_px(line) > MAX_LINE_PX:
            return True
    return False


def render_payload(payload: str) -> str:
    new = substitute(payload)
    if new == payload:
        return payload
    terminator = "$" if new.endswith("$") else ""
    trimmed = new[:-1] if terminator else new
    pages = trimmed.split("\\p")
    pages = [reflow_page(p) if page_overflows(p) else p for p in pages]
    return "\\p".join(pages) + terminator


def structure(payload: str) -> list[str]:
    """Page breaks, control codes and the terminator, in order."""
    return STRUCTURE_RE.findall(payload)


def line_breaks_valid(page: str) -> bool:
    """Within a page the second line uses \\n and every later line uses \\l.

    Only checked on pages this renderer reflowed. 34 pages elsewhere in the
    repository use \\n twice in one page, which overwrites the second line
    instead of scrolling; that predates this renderer and is left alone.
    """
    breaks = re.findall(r"\\[nl]", page)
    if breaks and breaks[0] != "\\n":
        return False
    return all(b == "\\l" for b in breaks[1:])


def words(payload: str) -> list[str]:
    return MARKER_RE.sub(" ", payload).split()


def render_file(source: str, rel: str) -> str:
    out: list[str] = []
    last = 0
    for block in BLOCK_RE.finditer(source):
        payload = "".join(m.group("body") for m in STRING_RE.finditer(block.group(0)))
        if not any(old in payload for old in CANON):
            continue
        rendered = render_payload(payload)
        if rendered == payload:
            continue

        expected = substitute(payload)
        if structure(rendered) != structure(expected):
            fail(f"{rel}: page breaks or control codes changed in {payload[:48]!r}")
        for before, after in zip(expected.split("\\p"), rendered.split("\\p")):
            if before != after and not line_breaks_valid(after):
                fail(f"{rel}: bad line-break pattern in {after[:64]!r}")
        if words(rendered) != words(expected):
            fail(f"{rel}: words changed in {payload[:48]!r}")
        for line in re.split(r"\\[nlp]", rendered):
            if RUNTIME_RE.search(line):
                continue
            if line_px(line) > MAX_LINE_PX:
                fail(f"{rel}: {line_px(line)}px line does not fit the box: {line!r}")

        indent = STRING_RE.search(block.group(0)).group("indent")
        # One .string per printed line, the way the rest of the repo is written.
        pieces = [p for p in re.split(r'(?<=\\n)|(?<=\\l)|(?<=\\p)', rendered) if p]
        body = "".join(f'{indent}.string "{p}"\n' for p in pieces)
        out.append(source[last:block.start()])
        out.append(body)
        last = block.end()
    out.append(source[last:])
    return "".join(out)


def targets() -> list[Path]:
    found = []
    for path in sorted((ROOT / "data").rglob("*.inc")):
        if "/arauna/pt_br/" in path.as_posix():
            continue           # the Portuguese bank is not compiled into the ROM
        text = path.read_text(encoding="utf-8")
        payloads = "".join(m.group("body") for m in STRING_RE.finditer(text))
        if any(old in payloads for old in CANON):
            found.append(path)
    return found


def c_ceiling(source: str) -> int:
    """The widest fixed-width line the file already ships.

    Each of these screens has its own box, so the ceiling is measured per file
    from its own vanilla content rather than assumed.
    """
    widest = 0
    for group in C_LITERAL_RE.finditer(source):
        payload = "".join(C_ONE_RE.findall(group.group(1)))
        for line in re.split(r"\\[nlp]", payload):
            if line.strip() and not C_RUNTIME_RE.search(line):
                widest = max(widest, line_px(line))
    return widest


def render_c_text(source: str, rel: str) -> str:
    ceiling = c_ceiling(source)
    out: list[str] = []
    last = 0
    for group in C_LITERAL_RE.finditer(source):
        raw = group.group(1)
        key = " ".join(raw.split())
        if key in C_LITERAL_OVERRIDES:
            replacement = C_LITERAL_OVERRIDES[key]
        else:
            payload = "".join(C_ONE_RE.findall(raw))
            if not any(old in payload for old in CANON):
                continue
            replacement = C_ONE_RE.sub(lambda m: '"' + substitute(m.group(1)) + '"', raw)
        if replacement == raw:
            continue
        new_payload = "".join(C_ONE_RE.findall(replacement))
        for line in re.split(r"\\[nlp]", new_payload):
            if line.strip() and not C_RUNTIME_RE.search(line) and line_px(line) > ceiling:
                fail(f"{rel}: {line_px(line)}px line does not fit the {ceiling}px box: {line!r}")
        # Keep the source's own line layout: same literals, same whitespace.
        rebuilt = raw
        old_parts = C_ONE_RE.findall(raw)
        new_parts = C_ONE_RE.findall(replacement)
        if len(old_parts) != len(new_parts):
            fail(f"{rel}: literal count changed in {key[:60]!r}")
        for old_part, new_part in zip(old_parts, new_parts):
            if old_part != new_part:
                rebuilt = rebuilt.replace(f'"{old_part}"', f'"{new_part}"', 1)
        out.append(source[last:group.start(1)])
        out.append(rebuilt)
        last = group.end(1)
    out.append(source[last:])
    return "".join(out)


def render_c_decls(source: str) -> str:
    rendered = source
    for old, new in C_DECLS.items():
        old_count = rendered.count(old)
        new_count = rendered.count(new)
        if old_count == 1 and new_count == 0:
            rendered = rendered.replace(old, new, 1)
        elif old_count == 0 and new_count == 1:
            continue
        else:
            fail(f"src/strings.c contract mismatch for {old!r}: "
                 f"old={old_count}, final={new_count}")
    return rendered


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--in-place", action="store_true")
    args = parser.parse_args()
    if args.check and args.in_place:
        parser.error("use either --check or --in-place")

    files = targets()
    renamed = 0
    for path in files:
        rel = path.relative_to(ROOT).as_posix()
        source = path.read_text(encoding="utf-8")
        rendered = render_file(source, rel)
        if rendered == source:
            continue
        surviving = [old for old in CANON
                     if any(old in m.group("body") for m in STRING_RE.finditer(rendered))]
        if surviving:
            fail(f"{rel}: legacy name survived: {', '.join(sorted(surviving))}")
        renamed += 1
        if args.in_place:
            path.write_text(rendered, encoding="utf-8")

    c_source = C_DECLS_PATH.read_text(encoding="utf-8")
    c_rendered = render_c_decls(c_source)
    if args.in_place and c_rendered != c_source:
        C_DECLS_PATH.write_text(c_rendered, encoding="utf-8")

    c_files = 0
    for rel in C_TEXT_FILES:
        path = ROOT / rel
        source = path.read_text(encoding="utf-8")
        rendered = render_c_text(source, rel)
        if rendered == source:
            continue
        surviving = [old for old in CANON
                     if any(old in p for g in C_LITERAL_RE.finditer(rendered)
                            for p in C_ONE_RE.findall(g.group(1)))]
        if surviving:
            fail(f"{rel}: legacy name survived: {', '.join(sorted(surviving))}")
        c_files += 1
        if args.in_place:
            path.write_text(rendered, encoding="utf-8")

    mode = "Renamed" if args.in_place else "Validated"
    print(f"{mode} legacy place names: {renamed} dialogue file(s), "
          f"{len(C_DECLS)} location labels, {c_files} C text file(s), "
          f"{len(CANON)} canonical names.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
