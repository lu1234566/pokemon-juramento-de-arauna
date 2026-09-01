#!/usr/bin/env python3
"""Four houses people stop in: the beach bar, the diver, the WINSTRATES, the
tunnellers' hut.

The WINSTRATE house is the interesting one. Inside, the daughter recites the
family's pecking order -- father, mother, herself, grandmother, and a brother
above all of them -- and outside, on ROUTE 111, the family fights you in
exactly that order. The two have to agree, so the order is declared here in
one list and both the recitation and the check are built from it. If the
house says one thing and the doorstep does another, the family stops being a
family.

The tunnellers' hut is the only place the game tells a player what to do if
the TUNNEL is shut: cross to PORTO DAS REDES, sail to PORTO DO SAL, and go
overland through ENCRUZILHADA. That is a three-leg detour and every leg of it
is held.

MR. SEA's bar states the price of a SODA POP, which is stated nowhere else.

The diver's trade board is a table drawn with column stops rather than a
sentence, so it is left exactly as it is -- but the four SHARD-for-stone
pairings on it are checked against src/data/items.h, since a board offering
an item that does not exist is worse than no board.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools" / "arauna"))
from textbox import TextBox, glued  # noqa: E402

SEASHORE = ROOT / "data" / "maps" / "Route109_SeashoreHouse" / "scripts.inc"
DIVER = ROOT / "data" / "maps" / "Route124_DivingTreasureHuntersHouse" / "scripts.inc"
WINSTRATE = ROOT / "data" / "maps" / "Route111_WinstrateFamilysHouse" / "scripts.inc"
TUNNELLERS = ROOT / "data" / "maps" / "Route116_TunnelersRestHouse" / "scripts.inc"
ITEMS_TABLE = ROOT / "src" / "data" / "items.h"

BOX = TextBox({"{STR_VAR_1}": 12, "{STR_VAR_2}": 12}, width=34)

WHOLE = ("SEASHORE HOUSE", "MR. SEA", "SODA POP", "MACHO BRACE",
         "POKéMON LEAGUE", "GALERIAS DA SERRA", "VALE DO SILENCIO",
         "PORTO DAS REDES", "PORTO DO SAL", "ENCRUZILHADA", "RED SHARD",
         "BAG")

# The family, weakest first, as (how they are named as the subject of a
# sentence, how they are named as its object). ROUTE 111 sends them out in
# this order and the daughter recites it indoors; both come from this list.
FAMILY: tuple[tuple[str, str], ...] = (
    ("Daddy", "Daddy"),
    ("Mummy", "Mummy"),
    ("I", "me"),
    ("Grandma", "Grandma"),
)

# The board trades a SHARD for a stone. The board itself is a table and is
# not rewritten, but the pairings on it have to be real items.
SHARD_TRADES: tuple[tuple[str, str], ...] = (
    ("RED SHARD", "FIRE STONE"),
    ("YELLOW SHARD", "THUNDERSTONE"),
    ("BLUE SHARD", "WATER STONE"),
    ("GREEN SHARD", "LEAF STONE"),
)

SEASHORE_BLOCKS: dict[str, tuple[str, ...]] = {
    "SeashoreHouseIntro": (
        "I own the SEASHORE HOUSE.|You may call me MR. SEA.",
        "What I love above everything is a POKéMON battle with some heat in "
        "it.",
        "Show me your heart burns hot.",
        "Beat every TRAINER in here and I shall see you right.",
    ),
    "ShowMeSomeHotMatches": (
        "Show me some hot matches.",
        "That is the only reason I keep this SEASHORE HOUSE at all.",
    ),
    "TakeTheseSodaPopBottles": (
        "You are scorching!|Those battles blazed!|More than satisfied, I "
        "am!",
        "For showing me a run like that, take these.",
        "Half a dozen bottles of SODA POP.",
    ),
    "BagFull": (
        "Oh -- but your BAG is jammed full.|I shall hold on to these for "
        "you.",
    ),
    "WantToBuySodaPop": (
        "After a SODA POP?|POKéMON love the stuff.",
        "¥300 a bottle. Go on.",
    ),
    "HereYouGo": (
        "There you are.",
    ),
    "NotEnoughMoney": (
        "You have not got the money.",
    ),
    "ThatsTooBad": (
        "No?|That is a shame.",
    ),
    "DwayneIntro": (
        "If it is a battle in the SEASHORE HOUSE you are after, you will "
        "find no hotter TRAINER than me, matey.",
    ),
    "DwayneDefeated": (
        "That was a hot battle.|I can take a loss like that, matey.",
    ),
    "DwaynePostBattle": (
        "Whenever I am in PORTO DO SAL it is hot battles and ice-cold "
        "SODA POP.",
    ),
    "JohannaIntro": (
        "A dull battle is not worth the trouble of having.",
        "It is the fiery ones that toughen a TRAINER and a POKéMON both.",
    ),
    "JohannaDefeated": (
        "That was hot!",
    ),
    "JohannaPostBattle": (
        "Whew. I am parched.|Perhaps a SODA POP.",
    ),
    "SimonIntro": (
        "I am going to show you how good my POKéMON are.|Try not to cry.",
    ),
    "SimonDefeated": (
        "...I lost. I am not going to cry...",
    ),
    "SimonPostBattle": (
        "If one of mine knew the move for carrying me across water on its "
        "back, I could be rid of this inner tube.",
    ),
}

DIVER_BLOCKS: dict[str, tuple[str, ...]] = {
    "Greeting": (
        "I am the DIVING TREASURE HUNTER.",
        "The fellow who goes down to the deep water and brings up what is "
        "lying on the bottom.",
    ),
    "HaveYouSeenAnyShards": (
        "Tell me -- have you seen any SHARDS of tools made in ancient times?",
    ),
    "YouHaventGotAnyShards": (
        "No treasure on you for me...",
        "If you find a SHARD -- a RED SHARD, say -- you must bring it here "
        "and trade it.",
    ),
    "ThatsAShardIllTradeYou": (
        "Oh, hey! That...|That is a SHARD! Those are exactly what I am "
        "after!",
        "You have to trade me that.|I shall give you something good for it.",
    ),
    "WhatDoYouWantToTrade": (
        "What are you trading?",
    ),
    "YoullTradeShardForStone": (
        "Your {STR_VAR_1} for my {STR_VAR_2}, then?",
    ),
    "ItsADeal": (
        "Done and done.|Use that wisely.",
    ),
    "TradeSomethingElse": (
        "Anything else you want to trade?",
    ),
    "BagFull": (
        "Whoops -- your BAG is full.|Clear something out, friend.",
    ),
    "ComeBackIfYouChangeMind": (
        "No? What a downer.|Well. Come back if you change your mind.",
    ),
}

WINSTRATE_BLOCKS: dict[str, tuple[str, ...]] = {
    "MySonIsStrongerThanYou": (
        "You are the first TRAINER I have seen handle POKéMON like that.",
        "But I should tell you -- my son is stronger than you are.",
        "He took the POKéMON LEAGUE challenge, I will have you know.",
    ),
    "LikeYouToHaveMachoBrace": (
        "We use this MACHO BRACE to get more out of our training.",
        "You have beaten every one of us, so I doubt you need it. All the "
        "same, we should like you to have our MACHO BRACE.",
    ),
    "PassionateAboutBattles": (
        "Where POKéMON battles are concerned we do rather run hot.",
    ),
    "GrandsonStrong": (
        "There is no question that you are strong.",
        "But battle my grandson and you would be crying with frustration by "
        "the end.",
        "He is stronger than any TRAINER this family knows.",
        "He must be up against the POKéMON LEAGUE CHAMPION by now.",
        "Knowing him, he may be the CHAMPION already.",
    ),
    "GrandsonStrongShort": (
        "My grandson must be up against the POKéMON LEAGUE CHAMPION by now.",
        "Knowing him, he may be the CHAMPION already.",
    ),
}

TUNNELLERS_BLOCKS: dict[str, tuple[str, ...]] = {
    "WeHadToStopBoring": (
        "That GALERIAS DA SERRA...",
        "We started with a full crew and the newest machinery, boring "
        "straight through the rock. Then we had to stop.",
        "It turned out we would have done real harm to the wild POKéMON "
        "living in there.",
        "So now we sit about here with nothing whatever to do.",
    ),
    "ManDiggingHisWayToVerdanturf": (
        "There is a man digging his way to VALE DO SILENCIO on his own. He "
        "is desperate to get through.",
        "He says that going at it little by little, without machines, will "
        "not disturb the POKéMON and will leave the place as he found it.",
        "I wonder whether he has got through yet.",
    ),
    "GetToVerdanturfWithoutTunnel": (
        "To reach VALE DO SILENCIO without this TUNNEL you would have to "
        "cross the sea to PORTO DAS REDES, sail on to PORTO DO SAL, and go "
        "overland through ENCRUZILHADA.",
    ),
    "TunnelHasGoneThrough": (
        "Did you hear? The TUNNEL to VALE DO SILENCIO has gone through.",
        "Hope hard enough for long enough and sometimes it happens.",
    ),
}


def build() -> dict[str, dict[str, tuple[str, ...]]]:
    winstrate = {f"Route111_WinstrateFamilysHouse_Text_{k}": v
                 for k, v in WINSTRATE_BLOCKS.items()}
    # The daughter recites the same order the family fights you in outside.
    lines = []
    for (subject, _), (_, weaker) in zip(FAMILY[1:], FAMILY):
        verb = "am" if subject == "I" else "is"
        lines.append(f"{subject} {verb} stronger than {weaker}.")
    lines.append(f"And my big brother is stronger than {FAMILY[-1][1]}.")
    winstrate["Route111_WinstrateFamilysHouse_Text_StrongerFamilyMembers"] = \
        tuple(lines)
    return {
        "seashore": {f"Route109_SeashoreHouse_Text_{k}": v
                     for k, v in SEASHORE_BLOCKS.items()},
        "diver": {f"Route124_DivingTreasureHuntersHouse_Text_{k}": v
                  for k, v in DIVER_BLOCKS.items()},
        "winstrate": winstrate,
        "tunnellers": {f"Route116_TunnelersRestHouse_Text_{k}": v
                       for k, v in TUNNELLERS_BLOCKS.items()},
    }


GROUPS = build()
TARGETS: dict[str, tuple[str, ...]] = {
    label: body for group in GROUPS.values() for label, body in group.items()}
FILES = {"seashore": SEASHORE, "diver": DIVER, "winstrate": WINSTRATE,
         "tunnellers": TUNNELLERS}


def which(label: str) -> str:
    for name, group in GROUPS.items():
        if label in group:
            return name
    raise KeyError(label)


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


def render(sources: dict[str, str]) -> dict[str, str]:
    composed = payloads()
    rendered = dict(sources)
    for label in TARGETS:
        group = which(label)
        matches = list(block_pattern(label).finditer(rendered[group]))
        if len(matches) != 1:
            raise ValueError(f"{label}: expected one text block, found {len(matches)}")
        if ".string" not in matches[0].group("body"):
            raise ValueError(f"{label}: target contains no .string payload")
        new_body = "".join(f'\t.string "{payload}"\n' for payload in composed[label]) + "\n"
        start, end = matches[0].span("body")
        rendered[group] = rendered[group][:start] + new_body + rendered[group][end:]
    return rendered


def mask(texts: dict[str, str]) -> dict[str, str]:
    masked = dict(texts)
    for label in TARGETS:
        group = which(label)
        match = block_pattern(label).search(masked[group])
        if not match:
            raise ValueError(f"cannot mask missing block: {label}")
        start, end = match.span("body")
        masked[group] = (masked[group][:start]
                         + '\t.string "<ARAUNA_REST_HOUSES_EN>"\n\n'
                         + masked[group][end:])
    return masked


def validate_slots(sources: dict[str, str]) -> None:
    composed = payloads()
    for label in TARGETS:
        body = block_pattern(label).search(sources[which(label)]).group("body")
        available = set(re.findall(r"\{[A-Za-z_0-9]+\}", body))
        used = set(re.findall(r"\{[A-Za-z_0-9]+\}", "".join(composed[label])))
        if used - available:
            raise ValueError(
                f"{label}: uses {sorted(used - available)}, which the engine "
                f"does not fill here; the source uses {sorted(available)}")


def validate_rendered(sources: dict[str, str], rendered: dict[str, str]) -> None:
    if mask(sources) != mask(rendered):
        raise ValueError("non-dialogue structure changed while rendering")

    composed = payloads()
    items = ITEMS_TABLE.read_text(encoding="utf-8")

    def flat(label: str) -> str:
        return re.sub(r"\s+", " ",
                      re.sub(r"\\[npl]|\x01", " ",
                             "".join(composed[label]))).strip().rstrip("$")

    # The order recited indoors is the order they fight you in outside.
    order = flat("Route111_WinstrateFamilysHouse_Text_StrongerFamilyMembers")
    # Every rung of the ladder is one sentence, and they have to appear in
    # the order ROUTE 111 sends the family out in.
    at = -1
    for (subject, _), (_, weaker) in zip(FAMILY[1:], FAMILY):
        verb = "am" if subject == "I" else "is"
        rung = f"{subject} {verb} stronger than {weaker}."
        if rung not in order:
            raise ValueError(
                f"StrongerFamilyMembers: lost the rung {rung!r}, and ROUTE "
                f"111 fights the family in exactly that order")
        position = order.index(rung)
        if position < at:
            raise ValueError(
                "StrongerFamilyMembers: the recited order no longer runs "
                "weakest to strongest, so the house contradicts the doorstep")
        at = position
    if "brother" not in order:
        raise ValueError(
            "StrongerFamilyMembers: no longer names the brother above them "
            "all, and he is the reason the family talks about the LEAGUE")

    # The only detour the game ever describes, and all three of its legs.
    detour = flat("Route116_TunnelersRestHouse_Text_GetToVerdanturfWithoutTunnel")
    for leg in ("PORTO DAS REDES", "PORTO DO SAL", "ENCRUZILHADA"):
        if leg not in detour:
            raise ValueError(
                f"GetToVerdanturfWithoutTunnel: dropped {leg}, and this is "
                f"the only route round the TUNNEL the game gives")

    # Prices and gifts, each stated once.
    if "¥300" not in flat("Route109_SeashoreHouse_Text_WantToBuySodaPop"):
        raise ValueError("WantToBuySodaPop: no longer states the price")
    if "MACHO BRACE" not in flat(
            "Route111_WinstrateFamilysHouse_Text_LikeYouToHaveMachoBrace"):
        raise ValueError("LikeYouToHaveMachoBrace: no longer names the gift")

    # The trade board is left as it is, but nothing on it may be a name the
    # BAG will not recognise.
    board = block_pattern(
        "Route124_DivingTreasureHuntersHouse_Text_ShardTradeBoard").search(
        rendered["diver"])
    if board is None:
        raise ValueError("the diver's trade board has gone missing")
    printed = board.group("body")
    for shard, stone in SHARD_TRADES:
        for name in (shard, stone):
            if f'.name = _("{name}")' not in items:
                raise ValueError(
                    f"the board offers {name!r}, which is not a name in "
                    f"src/data/items.h")
            if name not in printed:
                raise ValueError(f"the board no longer lists {name}")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Render the beach bar, the diver, the WINSTRATES and the "
                    "tunnellers' hut.")
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--in-place", action="store_true")
    args = parser.parse_args()
    if args.check and args.in_place:
        parser.error("use either --check or --in-place")

    sources = {name: path.read_text(encoding="utf-8")
               for name, path in FILES.items()}
    validate_slots(sources)
    rendered = render(sources)
    validate_rendered(sources, rendered)

    if args.in_place:
        for name, path in FILES.items():
            path.write_text(rendered[name], encoding="utf-8")
    print(f"Rest houses English renderer OK: {len(TARGETS)} blocks.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
