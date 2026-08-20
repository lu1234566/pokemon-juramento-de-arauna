#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MATCH = ROOT / "data" / "text" / "match_call.inc"
STRINGS = ROOT / "src" / "strings.c"
MAX = 32
CTRL = re.compile(r"\\[npl]")
PH = re.compile(r"\{[^}]+\}")

BLOCKS: dict[str, tuple[str, ...]] = {
    "MatchCall_Text_Steven1": (
        "SEU BENTO: {PLAYER}, I found an\\n",
        "old note today.\\p",
        "One name appears three times,\\n",
        "then vanishes on the next page.\\p",
        "Keep listening to people.\\n",
        "Paper alone is not enough.$",
    ),
    "MatchCall_Text_Steven2": (
        "SEU BENTO: The mountain path\\n",
        "is breathing again.\\p",
        "Old marks appeared where\\n",
        "the stone was opened.\\p",
        "Write down what you see.\\n",
        "I'll compare my notebooks.$",
    ),
    "MatchCall_Text_Steven3": (
        "SEU BENTO: Some objects keep\\n",
        "more than history.\\p",
        "Do not confuse memory\\n",
        "with an answer.\\p",
        "A clue can lie too.$",
    ),
    "MatchCall_Text_Steven4": (
        "SEU BENTO: Activity along\\n",
        "the coast changed suddenly.\\p",
        "Equipment is disappearing\\n",
        "from official records.\\p",
        "At the port, check every list\\n",
        "twice.$",
    ),
    "MatchCall_Text_Steven5": (
        "SEU BENTO: MISSOES DO CEU\\n",
        "is hearing too many signals.\\p",
        "When every network speaks,\\n",
        "silence matters more.\\p",
        "Trust what you saw.$",
    ),
    "MatchCall_Text_Steven6": (
        "SEU BENTO's signal does not\\n",
        "answer.\\p",
        "Only static and distant water\\n",
        "come through.$",
    ),
    "MatchCall_Text_Steven7": (
        "SEU BENTO: {PLAYER}, my notes\\n",
        "do not record everything.\\p",
        "Maybe that is for the best.\\p",
        "Some things must stay alive\\n",
        "in people's voices.$",
    ),
    "MatchCall_Text_BirchRegisterCall": (
        "ANAHI: {PLAYER}, your POKéNAV\\n",
        "can receive calls now.\\p",
        "Register my contact too.\\p",
        "If I find something strange,\\n",
        "I'll tell you first.$",
    ),
    "MatchCall_Text_RegisteredBirch": (
        "PROF. ANAHI was registered\\n",
        "in the POKéNAV.$",
    ),
}

# Replace by stable C symbol rather than by one historical source sentence.
# The repository has passed through English and Portuguese cleanup waves, so
# exact old-text anchors are brittle even when the runtime symbol is unchanged.
STRING_VALUES = {
    "gText_StevenMatchCallDesc": "KEEPS NAMES",
    "gText_StevenMatchCallName": "SEU BENTO",
    "gText_ProfBirchMatchCallName": "PROF. ANAHI",
    "gText_ProfBirchMatchCallDesc": "RESEARCHER",
    "gText_HOFDexRating": (
        "Seen POKéMON: {STR_VAR_1}!\\nRecorded: {STR_VAR_2}!\\p"
        "PROF. ANAHI's POKéDEX rating!\\pANAHI: Let's see…\\p"
    ),
    "gText_BirchInTrouble": "ANAHI is in trouble!\\nRelease a POKéMON and help her!",
}


def pattern(label: str) -> re.Pattern[str]:
    return re.compile(
        rf"(?ms)^{re.escape(label)}::\n(?P<body>.*?)(?=^[A-Za-z0-9_]+::(?:\n|$)|\Z)"
    )


def string_decl_pattern(symbol: str) -> re.Pattern[str]:
    return re.compile(
        rf'(?m)^const u8 {re.escape(symbol)}\[\] = _\("(?:\\.|[^"\\])*"\);$'
    )


def validate_widths() -> None:
    for label, lines in BLOCKS.items():
        for line in lines:
            clean = PH.sub("PLAYER", line.replace("$", ""))
            for segment in CTRL.split(clean):
                segment = segment.strip()
                if len(segment) > MAX:
                    raise ValueError(f"{label}: {len(segment)} chars: {segment!r}")


def mask_blocks(text: str) -> str:
    out = text
    for label in BLOCKS:
        match = pattern(label).search(out)
        if not match:
            raise ValueError(f"missing Match Call block: {label}")
        start, end = match.span("body")
        out = out[:start] + '\t.string "<ARAUNA_EN>"\n\n' + out[end:]
    return out


def render_match(source: str) -> str:
    out = source
    for label, lines in BLOCKS.items():
        matches = list(pattern(label).finditer(out))
        if len(matches) != 1:
            raise ValueError(f"{label}: expected 1 block, found {len(matches)}")
        body = "".join(f'\t.string "{line}"\n' for line in lines) + "\n"
        start, end = matches[0].span("body")
        out = out[:start] + body + out[end:]
    if mask_blocks(source) != mask_blocks(out):
        raise ValueError("Match Call non-target structure changed")
    return out


def render_strings(source: str) -> str:
    out = source
    for symbol, value in STRING_VALUES.items():
        rx = string_decl_pattern(symbol)
        matches = list(rx.finditer(out))
        if len(matches) != 1:
            raise ValueError(f"strings.c: expected one declaration for {symbol}, found {len(matches)}")
        replacement = f'const u8 {symbol}[] = _("{value}");'
        out = rx.sub(lambda _: replacement, out, count=1)
    return out


def validate_strings(out: str) -> None:
    # Validate only the declarations owned by this renderer. Other historical
    # symbols (for example gText_Steven[]) are audited globally by the English
    # surface auditor and must not make this focused renderer fail spuriously.
    for symbol, value in STRING_VALUES.items():
        rx = string_decl_pattern(symbol)
        matches = list(rx.finditer(out))
        if len(matches) != 1:
            raise ValueError(f"strings.c: expected one rendered declaration for {symbol}")
        expected = f'const u8 {symbol}[] = _("{value}");'
        if matches[0].group(0) != expected:
            raise ValueError(f"strings.c: unexpected rendered value for {symbol}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--in-place", action="store_true")
    args = parser.parse_args()
    if args.check and args.in_place:
        parser.error("choose --check or --in-place")

    validate_widths()
    match_source = MATCH.read_text(encoding="utf-8")
    strings_source = STRINGS.read_text(encoding="utf-8")
    match_out = render_match(match_source)
    strings_out = render_strings(strings_source)
    validate_strings(strings_out)

    if args.in_place:
        if match_out != match_source:
            MATCH.write_text(match_out, encoding="utf-8")
        if strings_out != strings_source:
            STRINGS.write_text(strings_out, encoding="utf-8")

    print(f"Match Call English identity OK: {len(BLOCKS)} blocks + {len(STRING_VALUES)} shared strings.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
