#!/usr/bin/env python3
"""The named PokeNav callers that no earlier renderer had claimed.

Your mother, the five of the league, Ciro's call about the thing that crossed
the sky, and the professor's unused line. These were still Emerald's -- your
mother talking about a gym in Petalburg, Drake about the Battle Frontier.

Everyone else who rings you is already spoken for.
render_pokenav_named_calls_en_checked.py, further down the manifest, owns
Otacilio, Anahi, Elias, Val, Scott, both of Ciro's fifteen-call lists and all
twenty-eight gym-leader rematch blocks, and it draws them from a reviewed
payload bank. Writing those blocks here as well would not conflict -- it would
be worse than that, because the later renderer wins in silence and the text
here would never reach a player. So this renderer stops where that one starts.

Ciro's sky call exists twice because the engine keeps a separate call list
depending on who the player is. Both say the same thing in slightly different
words, exactly as the original did.

No payload names a species: the dex is generated, and a line naming a creature
would be wrong the next time it is.
"""
from __future__ import annotations

import argparse
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CALLS = ROOT / "data" / "text" / "match_call.inc"
MAX_VISIBLE_WIDTH = 34
CONTROL_RE = re.compile(r"\\[npl]")
PLACEHOLDER_RE = re.compile(r"\{[^}]+\}")

TARGETS: dict[str, tuple[tuple[str, ...], tuple[str, ...]]] = {
    # -- home ---------------------------------------------------------------
    "MatchCall_Text_Mom1": (("Your father and you", "everyday chores"), (
        "MOM: Your father, and now you.\\p",
        "Both of you, taken with them.\\p",
        "What is it about them?\\p",
        "Me? I like the ones that help\\n",
        "around the house.$",
    )),
    "MatchCall_Text_Mom2": (("PAMPA DA ESPERA GYM", "big blow to his pride"), (
        "MOM: Hello, {PLAYER}!\\p",
        "Your father has shut himself in\\n",
        "the PAMPA DA ESPERA GYM again.\\p",
        "He comes home now and then.\\p",
        "He eats everything in the house\\n",
        "and goes straight back.\\p",
        "Losing to you took something\\n",
        "out of him, I think.$",
    )),
    "MatchCall_Text_Mom3": (("Don't worry about me", "RUNNING SHOES"), (
        "MOM: {PLAYER}.\\p",
        "Don't think about me or the\\n",
        "house.\\p",
        "Wear those RUNNING SHOES until\\n",
        "there's nothing left of them.$",
    )),

    # -- the league ---------------------------------------------------------
    "MatchCall_Text_Sidney": (("come on back", "waiting"), (
        "LAZARO: {PLAYER}.\\p",
        "If you want another go at me,\\n",
        "come back to the LEAGUE.\\p",
        "I don't go anywhere.\\n",
        "I'll be here.$",
    )),
    "MatchCall_Text_Phoebe": (("coming back here", "bond has grown"), (
        "ROSA: Hello, {PLAYER}.\\p",
        "Come back and see us sometime.\\p",
        "I'd like to see how much closer\\n",
        "you and yours have become.$",
    )),
    "MatchCall_Text_Glacia": (("complacent", "cool your"), (
        "CLARA: Hello, {PLAYER}.\\p",
        "You haven't grown comfortable\\n",
        "with your own strength?\\p",
        "If you ever need cooling down,\\n",
        "the LEAGUE is where I am.$",
    )),
    "MatchCall_Text_Drake": (("BATTLE", "no substitute"), (
        "TIBURCIO: That voice.\\n",
        "{PLAYER}, isn't it.\\p",
        "You sound well.\\p",
        "They've built a place that tests\\n",
        "a TRAINER's skill, I hear.\\p",
        "For a real battle, though,\\n",
        "nothing replaces the LEAGUE.\\p",
        "You agree with me. I know you do.$",
    )),
    "MatchCall_Text_Wallace": (("Have you met BENTO", "METEORITE"), (
        "AMALIA: Hello, {PLAYER}{KUN}.\\p",
        "Have you met BENTO yet?\\p",
        "He is better than almost anyone,\\n",
        "and he almost never battles.\\p",
        "He would rather be looking for\\n",
        "stones.\\p",
        "He's in a cave somewhere right\\n",
        "now. I'd put money on it.$",
    )),

    # -- Ciro, calling as the rival -----------------------------------------
    "MatchCall_Text_MayRayquazaCall": (("giant green", "major discovery"), (
        "... ... ... ... ...\\n",
        "... ... ... ... Beep!\\p",
        "CIRO: {PLAYER}{KUN}!\\p",
        "I was over in CASA DA FOGUEIRA\\n",
        "just now.\\p",
        "Something enormous and green\\n",
        "went over, very high up.\\p",
        "I've never seen anything like\\n",
        "it. I don't know what it was.\\p",
        "... ... ... ... ...\\n",
        "... ... ... ... Click!$",
    )),
    "MatchCall_Text_BrendanRayquazaCall": (("huge green", "wish you could've seen"), (
        "... ... ... ... ...\\n",
        "... ... ... ... Beep!\\p",
        "CIRO: {PLAYER}!\\p",
        "I was in CASA DA FOGUEIRA just\\n",
        "now.\\p",
        "Something huge and green crossed\\n",
        "the whole sky.\\p",
        "I wish you'd been there to see\\n",
        "it.\\p",
        "... ... ... ... ...\\n",
        "... ... ... ... Click!$",
    )),

    "MatchCall_Text_UnusedProfBirch": (("POKéDEX and POKéNAV",), (
        "PROF. ANAHI: With the POKéDEX\\n",
        "and the POKéNAV both in hand,\\l",
        "the work gets interesting.$",
    )),

}


def block_pattern(label: str) -> re.Pattern[str]:
    return re.compile(
        rf"(?ms)^{re.escape(label)}::?\n(?P<body>.*?)(?=^[A-Za-z0-9_]+(?:::|:)(?:\n|$)|\Z)"
    )


def visible_segments(payload: str) -> list[str]:
    cleaned = payload.replace("$", "").replace("{PLAYER}", "PLAYERX")
    cleaned = PLACEHOLDER_RE.sub("", cleaned)
    return [part.strip() for part in CONTROL_RE.split(cleaned)]


def validate_widths() -> None:
    for label, (_, payloads) in TARGETS.items():
        for payload in payloads:
            for segment in visible_segments(payload):
                if len(segment) > MAX_VISIBLE_WIDTH:
                    raise ValueError(
                        f"{label}: visible segment is {len(segment)} chars, "
                        f"max {MAX_VISIBLE_WIDTH}: {segment!r}")


def render(source: str) -> str:
    validate_widths()
    rendered = source
    for label, (markers, payloads) in TARGETS.items():
        matches = list(block_pattern(label).finditer(rendered))
        if len(matches) != 1:
            raise ValueError(f"{label}: expected one text block, found {len(matches)}")
        body = matches[0].group("body")
        if ".string" not in body:
            raise ValueError(f"{label}: target contains no .string payload")
        for marker in markers:
            if marker not in body:
                raise ValueError(f"{label}: source marker missing: {marker!r}")
        new_body = "".join(f'\t.string "{payload}"\n' for payload in payloads) + "\n"
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
        masked = masked[:start] + '\t.string "<ARAUNA_MATCH_CALL_PEOPLE_EN>"\n\n' + masked[end:]
    return masked


def validate_rendered(source: str, rendered: str) -> None:
    if mask(source) != mask(rendered):
        raise ValueError("non-dialogue structure changed while rendering")

    # Two place names had escaped the earlier passes because the source split
    # them across a line break. They must not survive here.
    forbidden = ("MIRAGE\\nTOWER", "MIRAGE TOWER", "JAGGED", "TEAM MAGMA",
                 "GROU", "Sucuria")
    for label in TARGETS:
        body = block_pattern(label).search(rendered).group("body")
        for token in forbidden:
            if token in body:
                raise ValueError(f"{label}: stale token survived: {token}")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Render the named PokeNav callers in English.")
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--in-place", action="store_true")
    args = parser.parse_args()
    if args.check and args.in_place:
        parser.error("use either --check or --in-place")

    source = CALLS.read_text(encoding="utf-8")
    rendered = render(source)
    validate_rendered(source, rendered)

    if args.in_place:
        CALLS.write_text(rendered, encoding="utf-8")
    print(f"Match Call people English renderer OK: {len(TARGETS)} blocks.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
