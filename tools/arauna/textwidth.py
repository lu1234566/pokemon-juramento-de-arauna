#!/usr/bin/env python3
"""How wide a line of dialogue actually is, in pixels.

The GBA font is variable width, so counting characters says nothing useful: in
FONT_NORMAL an "i" is three pixels and a "W" is eight. Anything that lengthens
existing text has to answer whether the line still fits, and the only honest
answer comes from the same two tables the engine reads -- charmap.txt for the
byte behind each character and gFontNormalLatinGlyphWidths for that byte's
width. FONT_NORMAL has letterSpacing 0, so a line is the sum of its glyphs.

Placeholders are the one estimate here. {PLAYER} and {STR_VAR_1} are filled in
at runtime, so they are measured as a typical value rather than as themselves.

Run it directly to print the widest lines the game already ships.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CHARMAP = ROOT / "charmap.txt"
FONTS = ROOT / "src/fonts.c"

# A runtime placeholder stands in for something the player or the game supplies.
# Measured as a plausible worst case rather than as the literal braces.
PLACEHOLDER_WIDTH = {
    "PLAYER": 7 * 6, "RIVAL": 5 * 6, "STR_VAR_1": 10 * 6, "STR_VAR_2": 10 * 6,
    "STR_VAR_3": 10 * 6, "KUN": 0, "LV": 12, "PKMN": 24, "POKEBLOCK": 54,
}
# Codes that render nothing: colour changes, pauses, scrolls, line control.
ZERO_WIDTH = re.compile(
    r"^(COLOR|HIGHLIGHT|SHADOW|COLOR_HIGHLIGHT_SHADOW|PALETTE|SIZE|FONT|PAUSE"
    r"|PAUSE_UNTIL_PRESS|WAIT_SE|PLAY_BGM|PLAY_SE|ESCAPE|SHIFT_RIGHT|SHIFT_DOWN"
    r"|FILL_WINDOW|CLEAR|CLEAR_TO|SKIP|UNKNOWN|JPN|ENG|NO)\b")


def charmap() -> dict[str, int]:
    """Every character the preprocessor knows, and the byte it becomes."""
    out = {}
    for line in CHARMAP.read_text(encoding="utf-8").splitlines():
        line = line.split("@")[0].strip()
        found = re.match(r"^'(\\?.)'\s*=\s*([0-9A-Fa-f]{2})$", line)
        if found:
            char = found.group(1)
            out[{"\\'": "'", "\\\\": "\\"}.get(char, char)] = int(found.group(2), 16)
    return out


def glyph_widths(symbol: str = "gFontNormalLatinGlyphWidths") -> list[int]:
    body = re.search(r"const u8 " + symbol + r"\[\] = \{(.*?)\};",
                     FONTS.read_text(encoding="utf-8"), re.S).group(1)
    return [int(n) for n in re.findall(r"\d+", body)]


class Ruler:
    def __init__(self) -> None:
        self.bytes = charmap()
        self.widths = glyph_widths()

    def width(self, line: str) -> int:
        """Pixel width of one rendered line, placeholders estimated."""
        total, index = 0, 0
        while index < len(line):
            if line[index] == "{":
                end = line.find("}", index)
                if end == -1:
                    index += 1
                    continue
                code = line[index + 1:end]
                if ZERO_WIDTH.match(code):
                    total += 0
                else:
                    total += PLACEHOLDER_WIDTH.get(code.split()[0], 6 * len(code))
                index = end + 1
                continue
            byte = self.bytes.get(line[index])
            if byte is not None and byte < len(self.widths):
                total += self.widths[byte]
            index += 1
        return total

    def lines(self, text: str) -> list[str]:
        r"""A .string body split where the engine breaks it: \n, \l and \p."""
        return re.split(r"\\[nlp]", text)

    def widest(self, text: str) -> int:
        return max((self.width(line) for line in self.lines(text)), default=0)


def main() -> int:
    import subprocess
    ruler = Ruler()
    files = [f for f in subprocess.run(["git", "ls-files", "data"], cwd=ROOT,
                                       capture_output=True, text=True).stdout.split()
             if f.endswith(".inc")]
    found = []
    for name in files:
        body = (ROOT / name).read_text(encoding="utf-8", errors="replace")
        for match in re.finditer(r'\.string "((?:[^"\\]|\\.)*)"', body):
            for line in ruler.lines(match.group(1)):
                found.append((ruler.width(line), name, line))
    found.sort(reverse=True)
    print(f"{len(found)} rendered lines; widest first")
    for width, name, line in found[:15]:
        print(f"  {width:4}px  {name}\n           {line[:60]}")
    for cut in (200, 208, 216, 224):
        print(f"  wider than {cut}px: {sum(1 for w, _, _ in found if w > cut)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
