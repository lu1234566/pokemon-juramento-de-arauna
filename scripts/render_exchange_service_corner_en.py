#!/usr/bin/env python3
"""The EXCHANGE SERVICE CORNER, where Battle Points are spent.

Thirty prizes, and for each of them a confirmation ("you have chosen the X,
is that correct?") and a line of description in the list window. The
confirmations are one sentence written thirty times, which is exactly the
shape that goes wrong by hand: a prize whose confirmation calls it something
slightly different from the menu entry the player just clicked leaves them
unsure they picked the right thing before spending points they cannot get
back.

So the thirty are generated from one table of prize names, and every name in
that table is checked against the table the menu itself draws from --
src/data/items.h for the items, src/data/decoration/header.h for the dolls,
posters and cushions. A prize renamed in either file and not here fails the
renderer rather than reaching a player.

The doll names stay as the decoration table spells them, SMOOCHUM DOLL and
the rest, because the decorations themselves are not this renderer's to
rename. The woman in the corner talking to her own POKéMON is a different
matter -- that is a live animal, and it is called by the name the species has
in this game.

The descriptions sit in a narrower window than the message box. Vanilla runs
to 192px in it, and that is the ceiling kept here.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools" / "arauna"))
from textbox import TextBox, glued  # noqa: E402
from textwidth import Ruler  # noqa: E402

SOURCE = ROOT / "data" / "maps" / "BattleFrontier_ExchangeServiceCorner" / "scripts.inc"
PREFIX = "BattleFrontier_ExchangeServiceCorner_Text_"

BOX = TextBox({}, width=34)
DESC_BOX = TextBox({}, width=31)
DESC_CEILING = 192

ITEMS_TABLE = ROOT / "src" / "data" / "items.h"
DECOR_TABLE = ROOT / "src" / "data" / "decoration" / "header.h"
SPECIES_TABLE = ROOT / "src" / "data" / "text" / "species_names.h"

WHOLE = ("EXCHANGE SERVICE CORNER", "Battle Point", "Battle Points",
         "KISS POSTER", "KISS CUSHION", "SMOOCHUM DOLL", "TOGEPI DOLL",
         "MEOWTH DOLL", "CLEFAIRY DOLL", "DITTO DOLL", "CYNDAQUIL DOLL",
         "CHIKORITA DOLL", "TOTODILE DOLL", "LAPRAS DOLL", "SNORLAX DOLL",
         "VENUSAUR DOLL", "CHARIZARD DOLL", "BLASTOISE DOLL",
         "WHITE HERB", "QUICK CLAW", "MENTAL HERB", "CHOICE BAND",
         "KING'S ROCK", "FOCUS BAND", "SCOPE LENS", "BRIGHTPOWDER",
         "HP UP", "SP. ATK", "SP. DEF")

# label suffix -> (name as the menu draws it, which table that name lives in)
PRIZES: dict[str, tuple[str, str]] = {
    "KissPoster": ("KISS POSTER", "decor"),
    "KissCushion": ("KISS CUSHION", "decor"),
    "SmoochumDoll": ("SMOOCHUM DOLL", "decor"),
    "TogepiDoll": ("TOGEPI DOLL", "decor"),
    "MeowthDoll": ("MEOWTH DOLL", "decor"),
    "ClefairyDoll": ("CLEFAIRY DOLL", "decor"),
    "DittoDoll": ("DITTO DOLL", "decor"),
    "CyndaquilDoll": ("CYNDAQUIL DOLL", "decor"),
    "ChikoritaDoll": ("CHIKORITA DOLL", "decor"),
    "TotodileDoll": ("TOTODILE DOLL", "decor"),
    "LaprasDoll": ("LAPRAS DOLL", "decor"),
    "SnorlaxDoll": ("SNORLAX DOLL", "decor"),
    "VenusaurDoll": ("VENUSAUR DOLL", "decor"),
    "CharizardDoll": ("CHARIZARD DOLL", "decor"),
    "BlastoiseDoll": ("BLASTOISE DOLL", "decor"),
    "Protein": ("PROTEIN", "item"),
    "Calcium": ("CALCIUM", "item"),
    "Iron": ("IRON", "item"),
    "Zinc": ("ZINC", "item"),
    "Carbos": ("CARBOS", "item"),
    "HPUp": ("HP UP", "item"),
    "Brightpowder": ("BRIGHTPOWDER", "item"),
    "WhiteHerb": ("WHITE HERB", "item"),
    "QuickClaw": ("QUICK CLAW", "item"),
    "MentalHerb": ("MENTAL HERB", "item"),
    "ChoiceBand": ("CHOICE BAND", "item"),
    "KingsRock": ("KING'S ROCK", "item"),
    "FocusBand": ("FOCUS BAND", "item"),
    "ScopeLens": ("SCOPE LENS", "item"),
    "Leftovers": ("LEFTOVERS", "item"),
}

# The five vitamins name a stat, and it has to be the stat the summary
# screen names. Checked against src/strings.c.
VITAMINS: dict[str, tuple[str, str]] = {
    "Protein": ("ATTACK", "gText_Attack"),
    "Calcium": ("SP. ATK", "gText_SpAtk"),
    "Iron": ("DEFENSE", "gText_Defense"),
    "Zinc": ("SP. DEF", "gText_SpDef"),
    "Carbos": ("SPEED", "gText_Speed"),
}

# The five large dolls share one description, so it names no species.
DESCRIPTIONS: dict[str, tuple[str, ...]] = {
    "KissPosterDesc": (
        "A big poster with a SMOOCHUM printed on it.",
    ),
    "KissCushionDesc": (
        "A SMOOCHUM cushion. For a mat or a desk.",
    ),
    "LargeDollDesc": (
        "A large DOLL. For a mat or a desk.",
    ),
    "HPUpDesc": (
        "Raises one POKéMON's HP.",
    ),
    "LeftoversDesc": (
        "Held: restores a little HP each turn of a battle.",
    ),
    "WhiteHerbDesc": (
        "Held: puts back any stat that has been lowered.",
    ),
    "QuickClawDesc": (
        "Held: now and then, lets its holder strike first.",
    ),
    "MentalHerbDesc": (
        "Held: snaps its holder out of infatuation.",
    ),
    "BrightpowderDesc": (
        "Held: throws a glare that spoils the foe's aim.",
    ),
    "ChoiceBandDesc": (
        "Raises a move's power, but allows only that move.",
    ),
    "KingsRockDesc": (
        "Held: a hit from its holder may make the foe flinch.",
    ),
    "FocusBandDesc": (
        "Held: now and then, its holder holds on at 1 HP.",
    ),
    "ScopeLensDesc": (
        "Held: raises the chance of a critical hit.",
    ),
}

# The counter clerk and the four people loitering by the prize case belong
# to render_battle_circuit_public_services_en_checked.py, further down the
# manifest. Writing them here as well would only be discarded. What is left
# is the one line that renderer does not claim.
PEOPLE: dict[str, tuple[str, ...]] = {
    "PleaseChoosePrize": (
        "Choose from the list, if you would.",
    ),
}


def build() -> dict[str, tuple[str, ...]]:
    blocks: dict[str, tuple[str, ...]] = dict(PEOPLE)
    for suffix, (name, _table) in PRIZES.items():
        blocks[f"Confirm{suffix}"] = (
            f"You have chosen the {name}.|Is that correct?",)
    for label, body in DESCRIPTIONS.items():
        blocks[label] = body
    for suffix, (stat, _symbol) in VITAMINS.items():
        blocks[f"{suffix}Desc"] = (f"Raises one POKéMON's {stat}.",)
    # Every small doll is described the same way, by its own name.
    for suffix in ("SmoochumDoll", "TogepiDoll", "MeowthDoll", "ClefairyDoll",
                   "DittoDoll", "CyndaquilDoll", "ChikoritaDoll",
                   "TotodileDoll"):
        name = PRIZES[suffix][0]
        blocks[f"{suffix}Desc"] = (f"A {name}. For a mat or a desk.",)
    return blocks


TARGETS: dict[str, tuple[str, ...]] = build()
DESC_LABELS = frozenset(label for label in TARGETS if label.endswith("Desc"))


def block_pattern(label: str) -> re.Pattern[str]:
    return re.compile(
        rf"(?ms)^{re.escape(PREFIX + label)}::?\n(?P<body>.*?)"
        rf"(?=^[A-Za-z0-9_]+(?:::|:)(?:\n|$)|\Z)"
    )


def payloads() -> dict[str, tuple[str, ...]]:
    composed = {}
    for label, paragraphs in TARGETS.items():
        glued_paragraphs = []
        for paragraph in paragraphs:
            for name in WHOLE:
                paragraph = paragraph.replace(name, glued(name))
            glued_paragraphs.append(paragraph)
        box = DESC_BOX if label in DESC_LABELS else BOX
        composed[label] = box.compose(tuple(glued_paragraphs))
    return composed


def render(source: str) -> str:
    composed = payloads()
    rendered = source
    for label in TARGETS:
        matches = list(block_pattern(label).finditer(rendered))
        if len(matches) != 1:
            raise ValueError(f"{label}: expected one text block, found {len(matches)}")
        if ".string" not in matches[0].group("body"):
            raise ValueError(f"{label}: target contains no .string payload")
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
        masked = masked[:start] + '\t.string "<ARAUNA_EXCHANGE_CORNER_EN>"\n\n' + masked[end:]
    return masked


def validate_slots(source: str) -> None:
    composed = payloads()
    for label in TARGETS:
        available = set(re.findall(r"\{[A-Za-z_0-9]+\}",
                                   block_pattern(label).search(source).group("body")))
        used = set(re.findall(r"\{[A-Za-z_0-9]+\}", "".join(composed[label])))
        if used - available:
            raise ValueError(
                f"{label}: uses {sorted(used - available)}, which the engine "
                f"does not fill here; the source uses {sorted(available)}")


def validate_rendered(source: str, rendered: str) -> None:
    if mask(source) != mask(rendered):
        raise ValueError("non-dialogue structure changed while rendering")

    composed = payloads()
    ruler = Ruler()
    items = ITEMS_TABLE.read_text(encoding="utf-8")
    decor = DECOR_TABLE.read_text(encoding="utf-8")
    species = SPECIES_TABLE.read_text(encoding="utf-8")
    strings = (ROOT / "src" / "strings.c").read_text(encoding="utf-8")

    def flat(label: str) -> str:
        return re.sub(r"\s+", " ",
                      re.sub(r"\\[npl]|\x01", " ",
                             "".join(composed[label]))).strip().rstrip("$")

    # The confirmation is the last thing a player reads before points they
    # cannot get back are spent, so it has to name the prize exactly as the
    # menu named it -- and the menu draws its names from these two tables.
    for suffix, (name, table) in PRIZES.items():
        source_table = items if table == "item" else decor
        if f'.name = _("{name}")' not in source_table:
            raise ValueError(
                f"{suffix}: the corner calls this prize {name!r}, which is "
                f"not a name in "
                f"{'src/data/items.h' if table == 'item' else 'src/data/decoration/header.h'}")
        if name not in flat(f"Confirm{suffix}"):
            raise ValueError(f"Confirm{suffix}: no longer names the prize")

    # Thirty confirmations, thirty different prizes named.
    confirmations = [flat(f"Confirm{suffix}") for suffix in PRIZES]
    if len(set(confirmations)) != len(confirmations):
        raise ValueError("two prizes are confirmed with the same sentence")

    # The vitamins name a stat, and it is the one the summary screen prints.
    for suffix, (stat, symbol) in VITAMINS.items():
        if f'{symbol}[] = _("{stat}")' not in strings:
            raise ValueError(
                f"{suffix}Desc: calls the stat {stat!r}, which is not what "
                f"{symbol} in src/strings.c prints")
        if stat not in flat(f"{suffix}Desc"):
            raise ValueError(f"{suffix}Desc: no longer names the stat it raises")

    # The KISS prizes are printed with a species on them, and the decoration
    # table spells that SMOOCHUM while this game calls the animal something
    # else. The descriptions follow the decoration table, since that is what
    # the menu entry beside them says.
    if '.name = _("SMOOCHUM DOLL")' not in decor:
        raise ValueError(
            "the KISS descriptions say SMOOCHUM because the decoration table "
            "does; it no longer does")
    if "SPECIES_SMOOCHUM]" not in species:
        raise ValueError("SPECIES_SMOOCHUM is gone from species_names.h")

    # The list window is narrower than the message box.
    for label in DESC_LABELS:
        for payload in composed[label]:
            width = ruler.widest(payload)
            if width > DESC_CEILING:
                raise ValueError(
                    f"{label}: {width}px, past the {DESC_CEILING}px the list "
                    f"window can show")

    # A description sits directly under the menu line that already gave the
    # prize's name, so it earns its place only by saying something the name
    # does not: where the thing goes, or what it does in a battle.
    for label in DESC_LABELS:
        text = flat(label)
        suffix = label[:-len("Desc")]
        if suffix in PRIZES:
            text = text.replace(PRIZES[suffix][0], "")
        if len(text.strip(" .")) < 12:
            raise ValueError(
                f"{label}: adds nothing to the prize's own name, which the "
                f"menu line above it has already given")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Render the EXCHANGE SERVICE CORNER in English.")
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--in-place", action="store_true")
    args = parser.parse_args()
    if args.check and args.in_place:
        parser.error("use either --check or --in-place")

    source = SOURCE.read_text(encoding="utf-8")
    validate_slots(source)
    rendered = render(source)
    validate_rendered(source, rendered)

    if args.in_place:
        SOURCE.write_text(rendered, encoding="utf-8")
    print(f"Exchange service corner English renderer OK: {len(TARGETS)} blocks.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
