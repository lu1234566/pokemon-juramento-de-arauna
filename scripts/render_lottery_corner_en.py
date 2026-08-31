#!/usr/bin/env python3
"""The POKéMON LOTTERY CORNER on the ground floor of the DEPARTMENT STORE.

One draw a day. A five-digit ticket is checked against the ID number of every
POKéMON the player owns, in the party and in the PC alike, and the prize
depends on how many digits from the right agree.

That ladder is the only thing here worth being careful about. Four prizes are
announced by four almost identical sentences, differing in a digit count and
a prize rank, and a player reads at most one of them a day -- so if two rungs
drift out of step, nobody ever notices and the prize they were told they won
is not the prize they won. The four are generated from one table, ordered,
and checked for order.

The rest is a clerk being pleasant.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools" / "arauna"))
from textbox import TextBox, glued  # noqa: E402

SOURCE = ROOT / "data" / "text" / "lottery_corner.inc"
PREFIX = "LilycoveCity_DepartmentStore_1F_Text_"

BOX = TextBox({"{PLAYER}": 7, "{STR_VAR_1}": 12}, width=34)

WHOLE = ("LOTO TICKET", "LOTTERY CORNER", "DEPARTMENT STORE", "ID number",
         "BAG")

# digits matched -> (label, how the prize is ranked). Fewest first.
LADDER: tuple[tuple[int, str, str], ...] = (
    (2, "TwoDigitsMatched", "third prize"),
    (3, "ThreeDigitsMatched", "second prize"),
    (4, "FourDigitsMatched", "first prize"),
)

HANDWRITTEN: dict[str, tuple[str, ...]] = {
    "LotteryCornerDrawTicket": (
        "This is the POKéMON LOTTERY CORNER.",
        "Everyone who shops at our DEPARTMENT STORE may draw a POKéMON LOTO "
        "TICKET.",
        "If the number on it matches the ID number of one of your POKéMON, "
        "there is a gift for you.",
        "Would you like to draw a POKéMON LOTO TICKET?",
    ),
    "ComeBackTomorrow": (
        "Do come back tomorrow.",
    ),
    "PleaseVisitAgain": (
        "Do please visit us again.",
    ),
    "PleaseVisitAgain2": (
        "Do please visit us again.",
    ),
    "PleasePickTicket": (
        "Take a LOTO TICKET, please.|...",
    ),
    "TicketNumberIsXPleaseWait": (
        "The LOTO TICKET number is {STR_VAR_1}.",
        "I shall check it against the ID number of every POKéMON you have. "
        "One moment.",
    ),
    "TicketMatchesPartyMon": (
        "Congratulations.",
        "The ID number of the {STR_VAR_1} on your team matches your LOTO "
        "TICKET.",
    ),
    "TicketMatchesPCMon": (
        "Congratulations.",
        "The ID number of the {STR_VAR_1} in your PC matches your LOTO "
        "TICKET.",
    ),
    "NoNumbersMatched": (
        "I am sorry.|Not one number matched.",
    ),
    "AllFiveDigitsMatched": (
        "Oh, my word -- all five digits!",
        "That is the jackpot.|You have won the {STR_VAR_1}!",
    ),
    "NoRoomForThis": (
        "Oh?|You appear to have no room for it.",
        "Make some space in your BAG and come and tell me.",
    ),
    "PrizeWeveBeenHolding": (
        "{PLAYER}?|Yes, I have been expecting you.",
        "This is the prize we have been holding for you.",
    ),
}


def build() -> dict[str, tuple[str, ...]]:
    blocks: dict[str, tuple[str, ...]] = dict(HANDWRITTEN)
    for digits, label, rank in LADDER:
        blocks[label] = (
            f"{('Two', 'Three', 'Four')[digits - 2]} digits matched, so you "
            f"take the {rank}.|You have won the {{STR_VAR_1}}!",
        )
    return blocks


TARGETS: dict[str, tuple[str, ...]] = build()


def block_pattern(label: str) -> re.Pattern[str]:
    return re.compile(
        rf"(?ms)^{re.escape(PREFIX + label)}::?\n(?P<body>.*?)"
        rf"(?=^[A-Za-z0-9_]+(?:::|:)(?:\n|$)|\Z)"
    )


TRAILING_CODES = re.compile(r"((?:\{[A-Z_0-9 ]+\})+)\$$")


def trailing_codes(source: str) -> dict[str, str]:
    """The pause run each vanilla block ends on, reattached verbatim.

    The clerk's draw line holds the box open while the ticket is read. That
    is timing, not writing.
    """
    codes: dict[str, str] = {}
    for label in TARGETS:
        payloads_ = re.findall(
            r'\.string "(.*?)"',
            block_pattern(label).search(source).group("body"))
        match = TRAILING_CODES.search(payloads_[-1]) if payloads_ else None
        codes[label] = match.group(1) if match else ""
    return codes


def payloads(source: str) -> dict[str, tuple[str, ...]]:
    codes = trailing_codes(source)
    composed = {}
    for label, paragraphs in TARGETS.items():
        glued_paragraphs = []
        for paragraph in paragraphs:
            for name in WHOLE:
                paragraph = paragraph.replace(name, glued(name))
            glued_paragraphs.append(paragraph)
        lines = list(BOX.compose(tuple(glued_paragraphs)))
        if codes[label]:
            lines[-1] = lines[-1][:-1] + codes[label] + "$"
        composed[label] = tuple(lines)
    return composed


def render(source: str) -> str:
    composed = payloads(source)
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
        masked = masked[:start] + '\t.string "<ARAUNA_LOTTERY_EN>"\n\n' + masked[end:]
    return masked


def validate_slots(source: str) -> None:
    composed = payloads(source)
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

    composed = payloads(source)
    codes = trailing_codes(source)

    def flat(label: str) -> str:
        text = re.sub(r"\{PAUSE[^}]*\}", "", "".join(composed[label]))
        return re.sub(r"\s+", " ",
                      re.sub(r"\\[npl]|\x01", " ", text)).strip().rstrip("$")

    for label, run in codes.items():
        if run and not composed[label][-1].endswith(run + "$"):
            raise ValueError(f"{label}: lost the pause run it ended on")

    # The rules are stated once, at the counter, and never again.
    rules = flat("LotteryCornerDrawTicket")
    for fact in ("LOTO TICKET", "ID number"):
        if fact not in rules:
            raise ValueError(
                f"LotteryCornerDrawTicket: dropped {fact!r}, and nothing else "
                f"explains what the draw is checked against")

    # Four rungs, each naming its own digit count and its own rank. A player
    # sees at most one a day, so a rung out of step is never noticed.
    seen_ranks = []
    for digits, label, rank in LADDER:
        text = flat(label)
        word = ("Two", "Three", "Four")[digits - 2]
        if word not in text:
            raise ValueError(f"{label}: no longer says {word.lower()} digits matched")
        if rank not in text:
            raise ValueError(f"{label}: no longer names the {rank}")
        seen_ranks.append(rank)
    if len(set(seen_ranks)) != len(seen_ranks):
        raise ValueError("two prize ranks read alike")
    jackpot = flat("AllFiveDigitsMatched")
    if "five" not in jackpot or "jackpot" not in jackpot:
        raise ValueError(
            "AllFiveDigitsMatched: no longer says five digits, or no longer "
            "says it is the jackpot")

    # Both match announcements must say where the POKéMON was found, since
    # the player may have forgotten what is in the PC.
    if "team" not in flat("TicketMatchesPartyMon"):
        raise ValueError("TicketMatchesPartyMon: no longer says it is on the team")
    if "PC" not in flat("TicketMatchesPCMon"):
        raise ValueError("TicketMatchesPCMon: no longer says it is in the PC")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Render the POKéMON LOTTERY CORNER in English.")
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
    print(f"Lottery corner English renderer OK: {len(TARGETS)} blocks.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
