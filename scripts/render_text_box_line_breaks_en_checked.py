#!/usr/bin/env python3
"""Fix dialogue pages whose third line is drawn outside the message box.

The standard field message window is 4 tiles tall -- 32px -- and FONT_NORMAL
lines are 16px with no line spacing, so exactly two lines fit. Within one page
the second line must therefore use \\n and every later line must use \\l, which
waits for input and scrolls the window up. Vanilla Emerald follows that
without exception across its ~11,600 pages.

110 pages in this repository used \\n twice or more in a single page. The
cursor simply advances past the bottom of the window, so the third line is
never drawn: the text is silently lost in game. The battle message box
(battle_bg.c, B_WIN_MSG), the PokeNav call box (pokenav_match_call_gfx.c) and
the field box (menu.c) are all 4 tiles, so trainer intros, Match Call lines,
the Pokedex rating and ordinary dialogue are all affected.

THREE_LINE_LABELS are the exception: the Battle Frontier move tutor prints
into a 6-tile window (field_specials.c, sBattleFrontierTutor_WindowTemplate),
where three lines are correct and vanilla.

Two shapes of fix, chosen per page:

  * if the words fit in two lines, the page is rewrapped to two lines, so the
    reader is not asked for a keypress the text does not need;
  * otherwise the author's own line breaks are kept exactly and only the
    marker changes, \\n to \\l, which is how vanilla writes a three-line page.
"""
from __future__ import annotations

import argparse
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MAX_LINE_PX = 208

# Printed by ShowBattleFrontierTutorMoveDescription into a 6-tile window.
THREE_LINE_LABELS = re.compile(r"^BattleFrontier_Lounge7_Text_\w+Desc$")

STRING_RE = re.compile(r'(?P<indent>[ \t]*)\.string[ \t]+"(?P<body>(?:[^"\\]|\\.)*)"')
BLOCK_RE = re.compile(r'(?:^[ \t]*\.string[ \t]+"(?:[^"\\]|\\.)*"\n)+', re.M)
LABEL_RE = re.compile(r'^(\w+)::?\s*$', re.M)
STRUCTURE_RE = re.compile(r'\\p|\{[^}]*\}|\$')
RUNTIME_RE = re.compile(r'\{(PLAYER|RIVAL|STR_VAR_\d|POKEBLOCK|B_[A-Z_0-9]+)[^}]*\}')


def fail(message: str) -> None:
    raise SystemExit(f"Text-box line-break renderer FAILED: {message}")


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
PLACEHOLDER_TEXT = {
    "{PLAYER}": "W" * 7, "{RIVAL}": "W" * 7,
    "{STR_VAR_1}": "W" * 10, "{STR_VAR_2}": "W" * 10, "{STR_VAR_3}": "W" * 10,
    "{POKEBLOCK}": "W" * 10, "{PKMN}": "WW",
    "{UP_ARROW}": "W", "{DOWN_ARROW}": "W", "{LEFT_ARROW}": "W", "{RIGHT_ARROW}": "W",
}
BRACE_RE = re.compile(r"\{[^}]*\}")


def line_px(text: str) -> int:
    expanded = BRACE_RE.sub(lambda m: PLACEHOLDER_TEXT.get(m.group(0), ""),
                            text.replace("$", ""))
    return sum(GLYPH_WIDTHS[CHARMAP[c]] for c in expanded if c in CHARMAP)


def page_ok(page: str) -> bool:
    breaks = re.findall(r"\\[nl]", page)
    if not breaks:
        return True
    return breaks[0] == "\\n" and all(b == "\\l" for b in breaks[1:])


def wrap(words: list[str]) -> list[str]:
    lines: list[str] = []
    current = ""
    for word in words:
        candidate = f"{current} {word}".strip()
        if current and line_px(candidate) > MAX_LINE_PX:
            lines.append(current)
            current = word
        else:
            current = candidate
    if current:
        lines.append(current)
    return lines


def join(lines: list[str]) -> str:
    out = lines[0]
    for index, line in enumerate(lines[1:]):
        out += ("\\n" if index == 0 else "\\l") + line
    return out


def fix_page(page: str) -> str:
    parts = [p for p in re.split(r"\\[nl]", page)]
    words = " ".join(p.strip() for p in parts if p.strip()).split()
    if not words:
        return page
    wrapped = wrap(words)
    if len(wrapped) <= 2:
        return join(wrapped)
    # Keep the author's own breaks; only the marker was wrong. Fall back to a
    # rewrap if one of those lines does not fit the box either.
    kept = [p for p in parts if p.strip()]
    if all(line_px(p) <= MAX_LINE_PX or RUNTIME_RE.search(p) for p in kept):
        return join(kept)
    return join(wrapped)


def render_file(source: str, rel: str) -> tuple[str, int]:
    out: list[str] = []
    last = 0
    fixed = 0
    for block in BLOCK_RE.finditer(source):
        labels = LABEL_RE.findall(source[:block.start()])
        label = labels[-1] if labels else ""
        if THREE_LINE_LABELS.match(label):
            continue
        payload = "".join(m.group("body") for m in STRING_RE.finditer(block.group(0)))
        terminator = "$" if payload.endswith("$") else ""
        trimmed = payload[:-1] if terminator else payload
        pages = trimmed.split("\\p")
        if all(page_ok(p) for p in pages):
            continue
        rendered = "\\p".join(p if page_ok(p) else fix_page(p) for p in pages) + terminator

        if STRUCTURE_RE.findall(rendered) != STRUCTURE_RE.findall(payload):
            fail(f"{rel}/{label}: page breaks or control codes changed")
        if re.sub(r"\\[nlp]", " ", rendered).split() != re.sub(r"\\[nlp]", " ", payload).split():
            fail(f"{rel}/{label}: words changed")
        for page in rendered.split("\\p"):
            if not page_ok(page):
                fail(f"{rel}/{label}: still a bad break pattern: {page[:56]!r}")
            for line in re.split(r"\\[nl]", page):
                if line.strip() and not RUNTIME_RE.search(line) and line_px(line) > MAX_LINE_PX:
                    fail(f"{rel}/{label}: {line_px(line)}px line does not fit: {line!r}")

        indent = STRING_RE.search(block.group(0)).group("indent")
        pieces = [p for p in re.split(r'(?<=\\n)|(?<=\\l)|(?<=\\p)', rendered) if p]
        out.append(source[last:block.start()])
        out.append("".join(f'{indent}.string "{p}"\n' for p in pieces))
        last = block.end()
        fixed += 1
    out.append(source[last:])
    return "".join(out), fixed


def targets() -> list[Path]:
    return [p for p in sorted((ROOT / "data").rglob("*.inc"))
            if "/arauna/pt_br/" not in p.as_posix()]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--in-place", action="store_true")
    args = parser.parse_args()
    if args.check and args.in_place:
        parser.error("use either --check or --in-place")

    files = 0
    blocks = 0
    for path in targets():
        rel = path.relative_to(ROOT).as_posix()
        source = path.read_text(encoding="utf-8")
        rendered, fixed = render_file(source, rel)
        if not fixed:
            continue
        files += 1
        blocks += fixed
        if args.in_place:
            path.write_text(rendered, encoding="utf-8")

    # Nothing outside the three-line window may be left with a bad pattern.
    # This catches a page the pass above skipped, not only the ones it fixed.
    survivors: list[str] = []
    exempt = 0
    for path in targets():
        source = path.read_text(encoding="utf-8") if args.in_place else None
        if source is None:
            source, _ = render_file(path.read_text(encoding="utf-8"),
                                    path.relative_to(ROOT).as_posix())
        for block in BLOCK_RE.finditer(source):
            labels = LABEL_RE.findall(source[:block.start()])
            label = labels[-1] if labels else ""
            payload = "".join(m.group("body") for m in STRING_RE.finditer(block.group(0)))
            bad = any(not page_ok(page) for page in payload.rstrip("$").split("\\p"))
            if not bad:
                continue
            if THREE_LINE_LABELS.match(label):
                exempt += 1
                continue
            survivors.append(f"{path.relative_to(ROOT).as_posix()}/{label}")
    if survivors:
        fail("bad break pattern survived in: " + ", ".join(sorted(set(survivors))[:6]))

    mode = "Fixed" if args.in_place else "Validated"
    print(f"{mode} text-box line breaks: {blocks} block(s) in {files} file(s); "
          f"{exempt} three-line-window text(s) left alone.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
