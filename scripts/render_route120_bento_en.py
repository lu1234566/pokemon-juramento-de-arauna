#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MAP_PATH = ROOT / "data" / "maps" / "Route120" / "scripts.inc"
ITEMS_PATH = ROOT / "src" / "data" / "items.h"
ITEM_DESCS_PATH = ROOT / "src" / "data" / "text" / "item_descriptions.h"
MAX_VISIBLE_WIDTH = 32

TARGETS: dict[str, tuple[tuple[str, ...], tuple[str, ...]]] = {
    "Route120_Text_StevenGreeting": (
        ("SEU BENTO:", "Quando um nome"),
        (
            "SEU BENTO: There you are,\\n",
            "{PLAYER}.\\p",
            "CIRO came through from\\n",
            "MATA DO MEIO.\\p",
            "He kept replaying that POKéMON\\n",
            "freezing when someone called.\\p",
            "He stared at his HORIZON device.\\p",
            "For once, he said nothing.\\p",
            "Want to see something strange?$",
        ),
    ),
    "Route120_Text_StevenIllWaitHere": (
        ("SEU BENTO:", "Quando um nome"),
        (
            "SEU BENTO: All right. I'll wait.\\p",
            "Some things are clearer when\\n",
            "you choose to look.$",
        ),
    ),
    "Route120_Text_StevenReadyForBattle": (
        ("sensores registram", "correntes antigas"),
        (
            "SEU BENTO: Ready now?\\p",
            "The bridge ahead looks empty,\\n",
            "but it isn't.$",
        ),
    ),
    "Route120_Text_StevenShowMeYourPower": (
        ("SEU BENTO:", "Quando um nome"),
        (
            "SEU BENTO: Don't fight the path.\\p",
            "Watch what refuses to move.$",
        ),
    ),
    "Route120_Text_StevenUsedDevonScope": (
        ("SEU BENTO:", "Quando um nome"),
        ("SEU BENTO used the FIELD SCOPE.$",),
    ),
    "Route120_Text_StevenGiveDevonScope": (
        ("SEU BENTO:", "Quando um nome"),
        (
            "SEU BENTO: Take this.\\p",
            "It's a FIELD SCOPE.\\p",
            "It reveals what the eye misses.\\p",
            "CIRO needs that lesson too.$",
        ),
    ),
    "Route120_Text_StevenGoodbye": (
        ("SEU BENTO:", "Quando um nome"),
        (
            "SEU BENTO: I'm heading east.\\p",
            "If CIRO reaches the memorial,\\n",
            "listen before choosing a side.$",
        ),
    ),
    "Route120_Text_RouteSignFortree": (
        ("ROUTE 120", "FORTREE CITY"),
        ("ROUTE 120\\n", "{LEFT_ARROW} MATA DO MEIO$"),
    ),
}

CONTROL_RE = re.compile(r"\\[npl]")
PLACEHOLDER_RE = re.compile(r"\{[^}]+\}")
ITEM_NAME_OLD = '.name = _("DEVON SCOPE"),'
ITEM_NAME_NEW = '.name = _("FIELD SCOPE"),'
ITEM_DESC_RE = re.compile(
    r'(?ms)^static const u8 sDevonScopeDesc\[\] = _\(\n'
    r'(?P<body>.*?^\s*"[^"\n]*"\);)'
)
ITEM_DESC_NEW = (
    'static const u8 sDevonScopeDesc[] = _(\n'
    '    "A field device that\\n"\n'
    '    "reveals hidden\\n"\n'
    '    "POKéMON nearby.");'
)


def block_pattern(label: str) -> re.Pattern[str]:
    # Route 120 contains legacy physical backslash-newline string continuations.
    return re.compile(
        rf"(?ms)^(?P<label>{re.escape(label)}:)\n(?P<body>.*?)(?=^[A-Za-z0-9_]+:)",
    )


def visible_segments(payload: str) -> list[str]:
    cleaned = PLACEHOLDER_RE.sub("", payload).replace("$", "")
    return [part.strip() for part in CONTROL_RE.split(cleaned)]


def validate_widths() -> None:
    for label, (_, payloads) in TARGETS.items():
        for payload in payloads:
            for segment in visible_segments(payload):
                if len(segment) > MAX_VISIBLE_WIDTH:
                    raise ValueError(
                        f"{label}: visible segment is {len(segment)} chars, max {MAX_VISIBLE_WIDTH}: {segment!r}"
                    )


def render_map(source: str) -> str:
    rendered = source
    for label, (markers, payloads) in TARGETS.items():
        pattern = block_pattern(label)
        matches = list(pattern.finditer(rendered))
        if len(matches) != 1:
            raise ValueError(f"{label}: expected one text block, found {len(matches)}")
        body = matches[0].group("body")
        for marker in markers:
            if marker not in body:
                raise ValueError(f"{label}: expected source marker not found: {marker!r}")
        new_body = "".join(f'\t.string "{payload}"\n' for payload in payloads) + "\n"
        start, end = matches[0].span("body")
        rendered = rendered[:start] + new_body + rendered[end:]
    return rendered


def render_items(source: str) -> str:
    count = source.count(ITEM_NAME_OLD)
    if count != 1:
        raise ValueError(f"expected one DEVON SCOPE item name, found {count}")
    return source.replace(ITEM_NAME_OLD, ITEM_NAME_NEW, 1)


def render_item_descs(source: str) -> str:
    matches = list(ITEM_DESC_RE.finditer(source))
    if len(matches) != 1:
        raise ValueError(f"expected one sDevonScopeDesc block, found {len(matches)}")
    return ITEM_DESC_RE.sub(ITEM_DESC_NEW, source, count=1)


def validate_rendered(map_text: str, items: str, descs: str) -> None:
    forbidden = (
        "Quando um nome",
        "sensores registram",
        "VINCULOS",
        "FORTREE CITY",
        "DEVON SCOPE",
    )
    for label, (_, payloads) in TARGETS.items():
        match = block_pattern(label).search(map_text)
        if not match:
            raise ValueError(f"{label}: rendered block missing")
        body = match.group("body")
        for payload in payloads:
            if f'\t.string "{payload}"' not in body:
                raise ValueError(f"{label}: rendered payload missing: {payload!r}")
        for token in forbidden:
            if token in body:
                raise ValueError(f"{label}: legacy/Portuguese token survived: {token}")

    if ITEM_NAME_NEW not in items or ITEM_NAME_OLD in items:
        raise ValueError("FIELD SCOPE item-name surface was not rendered correctly")
    if "A field device that" not in descs or "A device by DEVON" in descs:
        raise ValueError("FIELD SCOPE item description was not rendered correctly")

    preserved = (
        "SPECIES_KECLEON",
        "giveitem ITEM_DEVON_SCOPE",
        "setflag FLAG_RECEIVED_DEVON_SCOPE",
        "FLAG_NOT_READY_FOR_BATTLE_ROUTE_120",
        "FLDEFF_NPCFLY_OUT",
        "GetBattleOutcome",
    )
    for token in preserved:
        if token not in map_text:
            raise ValueError(f"preserved Route 120 gameplay token missing: {token}")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Render Route 120 Seu Bento / Ciro bridge and FIELD SCOPE surface in English."
    )
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--in-place", action="store_true")
    args = parser.parse_args()

    validate_widths()
    map_source = MAP_PATH.read_text(encoding="utf-8")
    item_source = ITEMS_PATH.read_text(encoding="utf-8")
    desc_source = ITEM_DESCS_PATH.read_text(encoding="utf-8")

    map_rendered = render_map(map_source)
    item_rendered = render_items(item_source)
    desc_rendered = render_item_descs(desc_source)
    validate_rendered(map_rendered, item_rendered, desc_rendered)

    if args.check:
        print(f"Route 120 English bridge OK: {len(TARGETS)} text blocks plus FIELD SCOPE validated.")
        return 0
    if args.in_place:
        MAP_PATH.write_text(map_rendered, encoding="utf-8")
        ITEMS_PATH.write_text(item_rendered, encoding="utf-8")
        ITEM_DESCS_PATH.write_text(desc_rendered, encoding="utf-8")
        return 0

    print(map_rendered)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
