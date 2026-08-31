#!/usr/bin/env python3
"""POKéMON NEWS: four stories, each read out at three points in its run.

The engine picks a bulletin by story and by stage -- the thing is coming, the
thing is happening, the thing is nearly over -- so the twelve texts are
twelve views of four facts. Written out longhand, as Emerald writes them,
they drift: its LILYCOVE ending bulletin is byte-for-byte its ongoing one,
and its GAME CORNER ending differs by a single sentence. A player who tunes
in near the close is told the sale has "finally arrived" and never told it is
about to stop.

So the four stories are declared once and the three stages composed from
them, and the renderer holds the stages apart: every ending bulletin has to
say the thing is running out, and no ending may read the same as its own
ongoing. The greeting and the sign-off are shared by all twelve, because a
broadcast that opens differently every time is not a broadcast.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools" / "arauna"))
from textbox import TextBox, glued  # noqa: E402

SOURCE = ROOT / "data" / "text" / "pokemon_news.inc"

BOX = TextBox({"{POKEBLOCK}": 9, "{STR_VAR_1}": 3}, width=34)

WHOLE = ("POKéMON NEWS", "PORTO DO SAL", "ENCRUZILHADA", "BAIA DAS LUZES",
         "ENERGY GURU", "BLEND MASTER", "GAME CORNER", "BERRY BLENDER",
         "DEPARTMENT STORE", "CONTEST HALL", "ARAUNA")

OPENING = "Good day to you.|It is time for POKéMON NEWS."
SIGN_OFF = "And that is the news on POKéMON NEWS."

STAGES = ("Upcoming", "Ongoing", "Ending")

# place    -- named in all three bulletins, so a listener always knows where.
# upcoming -- the announcement. The only stage the engine fills a day count
#             into, so the only stage that may spend {STR_VAR_1}.
# ongoing  -- it is happening now.
# ending   -- it is happening now and it is about to stop.
STORIES: dict[str, dict[str, str | tuple[str, ...]]] = {
    "Slateport": {
        "place": "PORTO DO SAL",
        "upcoming": (
            "PORTO DO SAL's most celebrated man, the ENERGY GURU, is in the "
            "news once more.",
            "He gives his word that he will go at it stupendously in this "
            "many days: {STR_VAR_1}.",
            "He would not be drawn on what he intends to go at. He would say "
            "only this: “Put your money by. You will want it.”",
            "A day in PORTO DO SAL may well repay the walk.",
        ),
        "ongoing": (
            "The news you have all been waiting on.",
            "PORTO DO SAL's ENERGY GURU is going at it stupendously in the "
            "MARKET.",
            "He is promising prices on CALCIUM and PROTEIN that nobody can "
            "match.",
            "PORTO DO SAL, then, and shop to your heart's content.",
        ),
        "ending": (
            "PORTO DO SAL's ENERGY GURU is still going at it stupendously in "
            "the MARKET.",
            "Still unmatched prices on CALCIUM and PROTEIN -- but the stock "
            "will not last, and neither will he.",
            "If you meant to go to PORTO DO SAL, go today.",
        ),
    },
    "GameCorner": {
        "place": "ENCRUZILHADA",
        "upcoming": (
            "It approaches.|At last, it comes.",
            "The GAME CORNER's service day arrives in this many days: "
            "{STR_VAR_1}.",
            "Even those who are never lucky have been known to be lucky on "
            "that particular day.",
            "The GAME CORNER is in ENCRUZILHADA.",
        ),
        "ongoing": (
            "It is here.|It has come at last.",
            "The GAME CORNER's service day has arrived.",
            "Might today be your day at the SLOTS, or at the ROULETTE?",
            "ENCRUZILHADA. That is where you want to be.",
        ),
        "ending": (
            "The GAME CORNER's service day is still running.",
            "The SLOTS and the ROULETTE are still favouring the unlucky -- "
            "but the day is nearly out.",
            "ENCRUZILHADA, and quickly.",
        ),
    },
    "Lilycove": {
        "place": "BAIA DAS LUZES",
        "upcoming": (
            "Wonderful news has reached us from the BAIA DAS LUZES "
            "DEPARTMENT STORE.",
            "Their clear-out sale opens in this many days: {STR_VAR_1}.",
            "That thingamajig, that doodad you have always wanted -- this "
            "may be the week it becomes yours.",
        ),
        "ongoing": (
            "The news you have all been waiting on.",
            "The BAIA DAS LUZES DEPARTMENT STORE's clear-out sale has "
            "opened.",
            "Every thingamajig and doodad you have ever dreamt of, all in "
            "one building.",
            "Go and meet them.",
        ),
        "ending": (
            "The BAIA DAS LUZES DEPARTMENT STORE's clear-out sale is still "
            "on.",
            "The thingamajigs and the doodads are going, though, and the "
            "sale closes shortly.",
            "If you were going to go, go now.",
        ),
    },
    "BlendMaster": {
        "place": "BAIA DAS LUZES",
        "upcoming": (
            "Big news for everyone who has ever made a {POKEBLOCK}.",
            "The legendary BLEND MASTER comes to BAIA DAS LUZES in this many "
            "days: {STR_VAR_1}.",
            "There is nobody in ARAUNA who can turn a BERRY BLENDER like the "
            "BLEND MASTER.",
            "Anyone hoping for a great {POKEBLOCK}, or simply to watch the "
            "MASTER work, would do well to save their BERRIES.",
        ),
        "ongoing": (
            "Big news for everyone who has ever made a {POKEBLOCK}.",
            "The legendary BLEND MASTER has arrived.",
            "The MASTER is turning a BERRY BLENDER in the BAIA DAS LUZES "
            "CONTEST HALL as we speak.",
            "Anyone hoping for a great {POKEBLOCK}, or simply to watch the "
            "MASTER work, should make for BAIA DAS LUZES.",
        ),
        "ending": (
            "It is extraordinary.|Beyond extraordinary.",
            "That BERRY BLENDER is turning at a speed that makes the eyes "
            "water.",
            "The BLEND MASTER is everything the stories said.",
            "But the MASTER leaves BAIA DAS LUZES very shortly.",
            "If you have not seen the MASTER work, do not let it pass. Go to "
            "BAIA DAS LUZES today.",
        ),
    },
}

# Words that make an ending bulletin an ending bulletin. At least one has to
# survive in each, or a listener who tunes in on the last day is told the
# thing has "arrived" and nothing more.
CLOSING_WORDS = ("shortly", "nearly out", "will not last", "closes",
                 "go today", "go now", "quickly", "today")


def build() -> dict[str, tuple[str, ...]]:
    blocks: dict[str, tuple[str, ...]] = {}
    for name, story in STORIES.items():
        for stage in STAGES:
            body = story[stage.lower()]
            if isinstance(body, str):
                raise ValueError(
                    f"{name}.{stage}: is a bare string; it must be a tuple of "
                    f"paragraphs (a trailing comma is probably missing)")
            blocks[f"gPokeNewsText{name}_{stage}"] = (
                (OPENING,) + tuple(body) + (SIGN_OFF,))
    return blocks


TARGETS: dict[str, tuple[str, ...]] = build()


def block_pattern(label: str) -> re.Pattern[str]:
    return re.compile(
        rf"(?ms)^{re.escape(label)}::?\n(?P<body>.*?)"
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
        masked = masked[:start] + '\t.string "<ARAUNA_POKEMON_NEWS_EN>"\n\n' + masked[end:]
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

    def flat(label: str) -> str:
        return re.sub(r"\s+", " ",
                      re.sub(r"\\[npl]|\x01", " ",
                             "".join(composed[label]))).strip().rstrip("$")

    plain_open = re.sub(r"\s+", " ", OPENING.replace("|", " ")).strip()
    plain_close = re.sub(r"\s+", " ", SIGN_OFF.replace("|", " ")).strip()

    for name, story in STORIES.items():
        place = story["place"]
        for stage in STAGES:
            text = flat(f"gPokeNewsText{name}_{stage}")
            # One programme, twelve bulletins. It opens and closes the same
            # way every time or it is not the same programme.
            if not text.startswith(plain_open):
                raise ValueError(f"{name}_{stage}: does not open the bulletin")
            if not text.endswith(plain_close):
                raise ValueError(f"{name}_{stage}: does not sign off")
            # A listener has to be told where to go, in every stage.
            if place not in text:
                raise ValueError(
                    f"{name}_{stage}: no longer says the event is in {place}")

        # The day count is only in scope while the event is still to come.
        if "{STR_VAR_1}" not in flat(f"gPokeNewsText{name}_Upcoming"):
            raise ValueError(
                f"{name}_Upcoming: dropped the day count, which is the only "
                f"thing this bulletin has to tell")
        for stage in ("Ongoing", "Ending"):
            if "{STR_VAR_1}" in flat(f"gPokeNewsText{name}_{stage}"):
                raise ValueError(
                    f"{name}_{stage}: spends {{STR_VAR_1}}, which the engine "
                    f"does not fill once the event has started")

        # Emerald's ending bulletins are its ongoing ones, so a listener who
        # tunes in on the last day is never told it is the last day.
        ending = flat(f"gPokeNewsText{name}_Ending")
        if ending == flat(f"gPokeNewsText{name}_Ongoing"):
            raise ValueError(
                f"{name}_Ending: reads exactly as {name}_Ongoing, so the "
                f"stage the engine went to the trouble of distinguishing says "
                f"nothing new")
        if not any(word in ending.lower() for word in CLOSING_WORDS):
            raise ValueError(
                f"{name}_Ending: no longer says the event is running out")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Render the POKéMON NEWS bulletins in English.")
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
    print(f"POKeMON NEWS English renderer OK: {len(TARGETS)} blocks.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
