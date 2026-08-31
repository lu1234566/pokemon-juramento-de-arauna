#!/usr/bin/env python3
"""The BATTLE DOME's tournament board: seedings, scouting notes and results.

Before every round the dome shows the player a card on each opponent: how the
house rates them, how they fight, and which two stats their POKéMON are built
around. It is the only scouting a player gets, and they choose which two of
their three to send out on the strength of it, so this is a readout and not a
speech. The register here is a clipped scouting note, not conversation.

Two things are composed rather than transcribed. The stat cards -- fifteen
pairs and six singles, once for the stats a team leans on and once for the
stats it leaves alone -- are generated from one table of stat names, and the
renderer checks those names against src/strings.c. Emerald writes all
forty-two out by hand and drifts: its cards say "SP. ATTACK" while the
summary screen the player just came from says "SP. ATK", so the two screens
name the same stat differently.

Every line here is drawn on one line in a narrow window with no wrapping, so
each is a single paragraph and the width gate is what keeps them honest.

Left alone: the twenty-one round labels ("Round 1, Match 3"), which are
positions on a bracket and not sentences, and the four sample messages, which
are leftovers from the developers' own testing that no player reaches.
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

SOURCE = ROOT / "data" / "text" / "battle_dome.inc"
PREFIX = "BattleDome_Text_"

BOX = TextBox({"{STR_VAR_1}": 12, "{STR_VAR_2}": 12}, width=40)

WHOLE = ("SP. ATK", "SP. DEF", "BATTLE DOME")

# The window draws one line and does not wrap, so nothing here may exceed
# what the message box can show.
LINE_CEILING = 208

# The stat names the summary screen prints, in the order the dome walks them.
STATS: tuple[tuple[str, str], ...] = (
    ("HP", "gText_HP4"),
    ("Atk", "gText_Attack"),
    ("Def", "gText_Defense"),
    ("Speed", "gText_Speed"),
    ("SpAtk", "gText_SpAtk"),
    ("SpDef", "gText_SpDef"),
)
STAT_NAMES: dict[str, str] = {
    "HP": "HP",
    "Atk": "ATTACK",
    "Def": "DEFENSE",
    "Speed": "SPEED",
    "SpAtk": "SP. ATK",
    "SpDef": "SP. DEF",
}

# Sixteen seedings, strongest first. The dome hands one to every entrant, so
# a player reads several in a row and has to be able to rank them by eye.
POTENTIAL: tuple[str, ...] = (
    "The clear favourite for the title.",
    "Certain to reach the final.",
    "Should finish in the top three.",
    "In contention to finish first.",
    "Top-class potential.",
    "The dark horse of this tournament.",
    "Somewhat above the field.",
    "Middling, for this tournament.",
    "Average potential, no more.",
    "Somewhat below the field.",
    "Still looking for a first win.",
    "One win would make this team proud.",
    "A weak team overall.",
    "Very little potential.",
    "Unlikely to win the tournament.",
    "The least likely team to win.",
)

STYLES: dict[str, str] = {
    "StyleRiskDisaster": "Will risk total disaster at times.",
    "StyleEndureLongBattles": "Built to outlast a long battle.",
    "StyleVariesTactics": "Changes tactics to suit the opponent.",
    "StyleToughWinningPattern": "Works to a hard winning pattern.",
    "StyleUsesVeryRareMove": "Now and then, a very rare move.",
    "StyleUsesStartlingMoves": "Startling, disruptive moves.",
    "StyleConstantlyWatchesHP": "Never stops watching the HP.",
    "StyleStoresAndLoosesPower": "Stores power, then looses it.",
    "StyleEnfeeblesFoes": "Skilled at wearing an opponent down.",
    "StylePrefersLuckTactics": "Prefers tactics that rely on luck.",
    "StyleRegalAtmosphere": "Attacks with a certain grandeur.",
    "StylePowerfulLowPPMoves": "Powerful moves with very little PP.",
    "StyleEnfeebleThenAttack": "Weakens first, attacks after.",
    "StyleBattlesWhileEnduring": "Fights by absorbing what comes.",
    "StyleUpsetsFoesEmotionally": "Skilled at unsettling an opponent.",
    "StyleStrongAndStraightforward": "Strong, straightforward moves.",
    "StyleAggressivelyStrongMoves": "Presses forward with strong moves.",
    "StyleCleverlyDodgesAttacks": "Fights by slipping attacks cleverly.",
    "StyleUsesUpsettingMoves": "Skilled at attacks that unsettle.",
    "StyleUsesPopularMoves": "Sticks to well-known moves.",
    "StyleHasPowerfulComboMoves": "Carries moves that combine well.",
    "StyleUsesHighProbabilityMoves": "Attacks that rarely miss.",
    "StyleAggressivelySpectacularMoves": "Presses forward with showy moves.",
    "StyleEmphasizesOffenseOverDefense": "Offence before defence.",
    "StyleEmphasizesDefenseOverOffense": "Defence before offence.",
    "StyleAttacksQuicklyStrongMoves": "Fast, and strong with it.",
    "StyleUsesAddedEffectMoves": "Often chooses moves with side effects.",
    "StyleUsesBalancedMixOfMoves": "A well-balanced mix of moves.",
}

RESULTS: dict[str, str] = {
    "LetTheBattleBegin": "Let the battle begin!",
    "TrainerWonUsingMove": "{STR_VAR_1} won it with {STR_VAR_2}!",
    "TrainerBecameChamp": "{STR_VAR_1} is the champion!",
    "TrainerWonByDefault": "{STR_VAR_1} won by default!",
    "TrainerWonOutrightByDefault": "{STR_VAR_1} won outright by default!",
    "TrainerWonNoMoves": "{STR_VAR_1} won without using a move!",
    "TrainerWonOutrightNoMoves": "{STR_VAR_1} won outright without a move!",
    "PotentialDomeAceTucker": "Flawless. Unbeaten. The star of the show.",
    "RaisesMonsWellBalanced": "Raises POKéMON in a well-balanced way.",
}


def build() -> dict[str, tuple[str, ...]]:
    blocks: dict[str, tuple[str, ...]] = {}
    for index, line in enumerate(POTENTIAL, start=1):
        blocks[f"Potential{index}"] = (line,)
    for label, line in STYLES.items():
        blocks[label] = (line,)
    for label, line in RESULTS.items():
        blocks[label] = (line,)
    for verb, prefix in (("Emphasizes", "Emphasizes"), ("Neglects", "Neglects")):
        for i, (key_a, _) in enumerate(STATS):
            for key_b, _ in STATS[i + 1:]:
                blocks[f"{prefix}{key_a}And{key_b}"] = (
                    f"{verb} {STAT_NAMES[key_a]} and {STAT_NAMES[key_b]}.",)
        for key, _ in STATS:
            blocks[f"{prefix}{key}"] = (f"{verb} {STAT_NAMES[key]}.",)
    return blocks


TARGETS: dict[str, tuple[str, ...]] = build()

# Positions on a bracket, not sentences; and four strings left behind by the
# developers' own testing. Neither is rewritten, but both are measured.
UNTOUCHED_PREFIXES = ("Round", "Semifinal", "FinalMatch", "StyleSampleMessage")


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
        composed[label] = BOX.compose(tuple(glued_paragraphs))
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
        masked = masked[:start] + '\t.string "<ARAUNA_BATTLE_DOME_BOARD_EN>"\n\n' + masked[end:]
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
    strings = (ROOT / "src" / "strings.c").read_text(encoding="utf-8")

    def flat(label: str) -> str:
        return re.sub(r"\s+", " ",
                      re.sub(r"\\[npl]|\x01", " ",
                             "".join(composed[label]))).strip().rstrip("$")

    # A card the player reads a moment after the summary screen has to call
    # each stat what the summary screen called it.
    for key, symbol in STATS:
        expected = f'{symbol}[] = _("{STAT_NAMES[key]}")'
        if expected not in strings:
            raise ValueError(
                f"{key}: the board calls this stat {STAT_NAMES[key]!r}, which "
                f"is not what {symbol} in src/strings.c prints")

    # Sixteen seedings read one after another. Two that read alike leave the
    # player unable to tell two entrants apart.
    seedings = [flat(f"Potential{i}") for i in range(1, len(POTENTIAL) + 1)]
    if len(set(seedings)) != len(seedings):
        raise ValueError("two of the sixteen seedings read identically")
    if flat("PotentialDomeAceTucker") in seedings:
        raise ValueError(
            "the MASTER's seeding reads as one of the sixteen ordinary ones")

    # Twenty-eight scouting notes, likewise.
    notes = [flat(label) for label in STYLES]
    if len(set(notes)) != len(notes):
        raise ValueError("two scouting notes read identically")

    # Every stat card names its stat or stats, and nothing else's.
    for i, (key_a, _) in enumerate(STATS):
        for key_b, _ in STATS[i + 1:]:
            for verb in ("Emphasizes", "Neglects"):
                card = flat(f"{verb}{key_a}And{key_b}")
                for wanted in (STAT_NAMES[key_a], STAT_NAMES[key_b]):
                    if wanted not in card:
                        raise ValueError(
                            f"{verb}{key_a}And{key_b}: no longer names "
                            f"{wanted}")

    # The window draws one line and will not wrap it, so anything past the
    # ceiling is simply cut off on screen.
    for label in TARGETS:
        for payload in composed[label]:
            width = ruler.widest(payload)
            if width > LINE_CEILING:
                raise ValueError(
                    f"{label}: {width}px, past the {LINE_CEILING}px the board "
                    f"can draw on one line")

    # Nothing else measures the labels this renderer leaves alone.
    for match in re.finditer(rf"(?ms)^{re.escape(PREFIX)}(\w+)::?\n(.*?)(?=^\w+::?|\Z)",
                             rendered):
        label, body = match.group(1), match.group(2)
        if not label.startswith(UNTOUCHED_PREFIXES):
            continue
        for payload in re.findall(r'\.string "(.*?)"', body):
            width = ruler.widest(payload)
            if width > LINE_CEILING:
                raise ValueError(
                    f"{label}: {width}px, past the {LINE_CEILING}px the board "
                    f"can draw on one line")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Render the BATTLE DOME tournament board in English.")
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
    print(f"Battle Dome board English renderer OK: {len(TARGETS)} blocks.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
