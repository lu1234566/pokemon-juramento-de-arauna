#!/usr/bin/env python3
"""SPOT THE CUTIES, and POKéMON NEWS reporting from the BATTLE CIRCUIT.

Both shows are lists wearing a presenter. SPOT THE CUTIES walks through a
POKéMON's ribbons one at a time; the frontier bulletin walks through the
circuit's halls one at a time. In each case Emerald wrote out every entry by
hand and the entries agree with each other, which is the part that is easy to
get wrong and impossible to see: change the phrasing of one hall and no test
notices, only a player who wins at two of them.

So the entries are declared as data -- a ribbon is a name, a reason and the
quality it brings out; a hall is a name, a mode and the unit its record is
counted in -- and the sentences are built around them. The presenter's voice
lives in one place and cannot drift between entries.

The RIBBONS themselves are not free text: each name matches a ribbon the
engine awards, so the renderer checks every one still appears.

BATTLE CIRCUIT is this region's name for the place. Its individual halls keep
the names the rest of the project already gave them.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools" / "arauna"))
from textbox import TextBox, glued  # noqa: E402

TV = ROOT / "data" / "text" / "tv.inc"

BOX = TextBox({"{STR_VAR_1}": 14, "{STR_VAR_2}": 14, "{STR_VAR_3}": 14}, width=34)

# label suffix -> (ribbon name, what it was given for, what it brings out)
RIBBONS: dict[str, tuple[str, str, str]] = {
    "Champion": ("CHAMPION RIBBON", "entering the HALL OF FAME", "the courage"),
    "Cool": ("COOL RIBBON", "winning a COOL CONTEST", "the coolness"),
    "Beauty": ("BEAUTY RIBBON", "winning a BEAUTY CONTEST", "the beauty"),
    "Cute": ("CUTE RIBBON", "winning a CUTE CONTEST", "the sweetness"),
    "Smart": ("SMART RIBBON", "winning a SMART CONTEST", "the cleverness"),
    "Tough": ("TOUGH RIBBON", "winning a TOUGH CONTEST", "the toughness"),
    "Winning": ("WINNING RIBBON", "what it did at the BATTLE TOWER", "the strength"),
    "Victory": ("VICTORY RIBBON", "what it did at the BATTLE TOWER",
                "the sheer strength"),
    "Artist": ("ARTIST RIBBON", "sitting as a model for an artist",
               "the star quality"),
    "Effort": ("Hard Worker RIBBON", "never once easing off", "the resolve"),
}

# The CHAMPION RIBBON is called by its short name in the closing line, as the
# engine's own text does.
RIBBON_SHORT = {"Champion": "CHAMP RIBBON"}

# label suffix -> (hall, the challenge within it, how the record reads)
HALLS: dict[str, tuple[str, str, str]] = {
    "01": ("BATTLE TOWER", "SINGLE BATTLE ROOM", "a {STR_VAR_2}-win streak"),
    "02": ("BATTLE TOWER", "DOUBLE BATTLE ROOM", "a {STR_VAR_2}-win streak"),
    "03": ("BATTLE TOWER", "MULTI BATTLE ROOM", "a {STR_VAR_2}-win streak"),
    "04": ("BATTLE TOWER", "LINK MULTI BATTLE ROOM", "a {STR_VAR_2}-win streak"),
    "05": ("BATTLE DOME", "SINGLE BATTLE Tournaments",
           "{STR_VAR_2} titles in a row"),
    "06": ("BATTLE DOME", "DOUBLE BATTLE Tournaments",
           "{STR_VAR_2} titles in a row"),
    "07": ("BATTLE FACTORY", "Battle Swap Single", "a {STR_VAR_2}-win streak"),
    "08": ("BATTLE FACTORY", "Battle Swap Double", "a {STR_VAR_2}-win streak"),
    "09": ("BATTLE PIKE", "Battle Choice", "{STR_VAR_2} rooms cleared"),
    "10": ("BATTLE ARENA", "Set KO Tournaments", "a {STR_VAR_2}-win streak"),
    "11": ("BATTLE PALACE", "SINGLE BATTLE HALL", "a {STR_VAR_2}-win streak"),
    "12": ("BATTLE PALACE", "DOUBLE BATTLE HALL", "a {STR_VAR_2}-win streak"),
    "13": ("BATTLE PYRAMID", "Battle Quest", "{STR_VAR_2} floors cleared"),
}

# Markers proving each generated block is still the one it was written for.
RIBBON_MARKERS = {suffix: (name.split()[0], "super effective")
                  for suffix, (name, _, _) in RIBBONS.items()}
HALL_MARKERS = {suffix: (hall, mode.split()[0])
                for suffix, (hall, mode, _) in HALLS.items()}

HANDWRITTEN: dict[str, tuple[tuple[str, ...], tuple[str, ...]]] = {
    "TVSpotTheCuties_Text_Intro": (("SPOT THE CUTIES", "out on a stroll"), (
        "SPOT THE CUTIES!|POKéMON IN RIBBONS!",
        "Hello, my dears.",
        "You will agree with me, I know: a POKéMON in RIBBONS is a lovely "
        "thing.",
        "Tonight I want to show you one I came across while out walking.",
        "Our POKéMON this evening is {STR_VAR_1}'s {STR_VAR_2}.",
    )),
    "TVSpotTheCuties_Text_RibbonsLow": (("number of RIBBONS", "adores"), (
        "{STR_VAR_2} wears {STR_VAR_3} RIBBONS.",
        "Which tells you a good deal about how {STR_VAR_1} feels.",
    )),
    "TVSpotTheCuties_Text_RibbonsMid": (("amazing", "commitment"), (
        "{STR_VAR_2} wears {STR_VAR_3} RIBBONS!",
        "Which tells you how much {STR_VAR_1} has put into this POKéMON!",
    )),
    "TVSpotTheCuties_Text_RibbonsHigh": (("incredible", "dedication"), (
        "{STR_VAR_2} wears {STR_VAR_3} RIBBONS!",
        "That is a collector, and no mistake!",
    )),
    "TVSpotTheCuties_Text_RibbonIntro": (("closer look",), (
        "Let us look more closely at what {STR_VAR_2} is wearing.",
    )),
    "TVSpotTheCuties_Text_Outro": (("Sigh", "swoon"), (
        "...Sigh...",
        "RIBBONS and POKéMON...|They were made for one another!",
        "And before I lose my composure entirely -- good night to you all!",
    )),
    "gTVPokemonNewsBattleFrontierText00": (("POKéMON NEWS", "BATTLE CIRCUIT"), (
        "Good evening.|It's time for POKéMON NEWS.",
        "And there is good news tonight from the BATTLE CIRCUIT.",
    )),
    "gTVPokemonNewsBattleFrontierText14": (("three POKéMON", "record-breaking"), (
        "And to the three POKéMON -- {STR_VAR_1}, {STR_VAR_2} and "
        "{STR_VAR_3}!",
        "Our congratulations on the record!",
    )),
    "gTVPokemonNewsBattleFrontierText15": (("two POKéMON", "record-breaking"), (
        "And to the two POKéMON -- {STR_VAR_1} and {STR_VAR_2}!",
        "Our congratulations on the record!",
    )),
    "gTVPokemonNewsBattleFrontierText16": (("four POKéMON",), (
        "And to the four POKéMON: {STR_VAR_1}!",
        "{STR_VAR_2}!",
        "{STR_VAR_3}!",
    )),
    "gTVPokemonNewsBattleFrontierText17": (("And", "record-breaking"), (
        "And {STR_VAR_1}!",
        "Our congratulations on the record!",
    )),
    "gTVPokemonNewsBattleFrontierText18": (("more record-setting", "POKéMON NEWS"), (
        "Long may {STR_VAR_1} and those POKéMON go on setting them!",
        "That has been POKéMON NEWS!",
    )),
}


def build() -> dict[str, tuple[tuple[str, ...], tuple[str, ...]]]:
    targets = dict(HANDWRITTEN)
    for suffix, (name, reason, quality) in RIBBONS.items():
        short = RIBBON_SHORT.get(suffix, name)
        targets[f"TVSpotTheCuties_Text_Ribbon{suffix}"] = (
            RIBBON_MARKERS[suffix], (
                f"The {glued(name)} is the one that catches the eye.",
                f"{{STR_VAR_2}} was given it for {reason}.",
                f"And it draws {quality} right out of {{STR_VAR_2}}.",
                f"{{STR_VAR_2}} and the {glued(short)}!|The pair is super effective!",
            ))
    for suffix, (hall, mode, record) in HALLS.items():
        targets[f"gTVPokemonNewsBattleFrontierText{suffix}"] = (
            HALL_MARKERS[suffix], (
                f"The TRAINER {{STR_VAR_1}} has set a new record -- {record} "
                f"-- in the {glued(hall)}'s {glued(mode)}.",
                "Here's to {STR_VAR_1}!",
            ))
    return targets


TARGETS = build()


def block_pattern(label: str) -> re.Pattern[str]:
    return re.compile(
        rf"(?ms)^{re.escape(label)}::?\n(?P<body>.*?)(?=^[A-Za-z0-9_]+(?:::|:)(?:\n|$)|\Z)"
    )


def payloads() -> dict[str, tuple[str, ...]]:
    return {label: BOX.compose(paragraphs)
            for label, (_, paragraphs) in TARGETS.items()}


def render(source: str) -> str:
    composed = payloads()
    rendered = source
    for label, (markers, _) in TARGETS.items():
        matches = list(block_pattern(label).finditer(rendered))
        if len(matches) != 1:
            raise ValueError(f"{label}: expected one text block, found {len(matches)}")
        body = matches[0].group("body")
        if ".string" not in body:
            raise ValueError(f"{label}: target contains no .string payload")
        for marker in markers:
            if marker not in body:
                raise ValueError(f"{label}: source marker missing: {marker!r}")
        new_body = "".join(f'\t.string "{payload}"\n' for payload in composed[label]) + "\n"
        start, end = matches[0].span("body")
        rendered = rendered[:start] + new_body + rendered[end:]
    return rendered


def mask(text: str) -> str:
    masked = text
    for label in TARGETS:
        match = block_pattern(label).search(masked)
        if not match:
            raise ValueError(f"cannot mask missing block: {label}")
        start, end = match.span("body")
        masked = masked[:start] + '\t.string "<ARAUNA_TV_RIBBONS_CIRCUIT_EN>"\n\n' + masked[end:]
    return masked


def validate_slots(source: str) -> None:
    composed = payloads()
    for label in TARGETS:
        available = set(re.findall(r"\{STR_VAR_\d\}",
                                   block_pattern(label).search(source).group("body")))
        used = set(re.findall(r"\{STR_VAR_\d\}", "".join(composed[label])))
        if used - available:
            raise ValueError(
                f"{label}: uses {sorted(used - available)}, which the engine "
                f"does not fill here; the source uses {sorted(available)}")


def validate_rendered(source: str, rendered: str) -> None:
    if mask(source) != mask(rendered):
        raise ValueError("non-dialogue structure changed while rendering")

    composed = payloads()

    def flat(label: str) -> str:
        return re.sub(r"\\[npl]", " ", "".join(composed[label]))

    # Every ribbon has to be called by the name the engine awards, or the
    # viewer is being told about a ribbon that does not exist.
    for suffix, (name, _, _) in RIBBONS.items():
        text = flat(f"TVSpotTheCuties_Text_Ribbon{suffix}")
        if name not in text:
            raise ValueError(f"{suffix}: the ribbon lost its name: {name}")

    # Same for the halls: the bulletin reports a real place and a real
    # challenge, and the two must not drift apart.
    for suffix, (hall, mode, _) in HALLS.items():
        text = flat(f"gTVPokemonNewsBattleFrontierText{suffix}")
        for part in (hall, mode):
            if part not in text:
                raise ValueError(f"{suffix}: the bulletin lost {part!r}")

    if "BATTLE CIRCUIT" not in flat("gTVPokemonNewsBattleFrontierText00"):
        raise ValueError("the bulletin lost the name this region gave the place")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Render SPOT THE CUTIES and the BATTLE CIRCUIT bulletin.")
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--in-place", action="store_true")
    args = parser.parse_args()
    if args.check and args.in_place:
        parser.error("use either --check or --in-place")

    source = TV.read_text(encoding="utf-8")
    validate_slots(source)
    rendered = render(source)
    validate_rendered(source, rendered)

    if args.in_place:
        TV.write_text(rendered, encoding="utf-8")
    print(f"TV ribbons and circuit English renderer OK: {len(TARGETS)} blocks.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
