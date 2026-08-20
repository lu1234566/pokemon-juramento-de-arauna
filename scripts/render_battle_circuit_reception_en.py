#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / "data" / "maps" / "BattleFrontier_ReceptionGate" / "scripts.inc"
MAX = 32
CTRL = re.compile(r"\\[npl]")
PH = re.compile(r"\{[^}]+\}")

BLOCKS: dict[str, tuple[str, ...]] = {
    "BattleFrontier_ReceptionGate_Text_FirstTimeHereThisWay": (
        "First visit?\\n", "Please come this way!$"),
    "BattleFrontier_ReceptionGate_Text_WelcomeToBattleFrontier": (
        "This is CIRCUITO DE BATALHA!\\n", "Welcome to the final challenge.$"),
    "BattleFrontier_ReceptionGate_Text_IssueFrontierPass": (
        "First-time visitors receive\\n", "a CIRCUIT PASS.\\p",
        "It works at every facility.\\p", "Here you are!$"),
    "BattleFrontier_ReceptionGate_Text_ObtainedFrontierPass": (
        "{PLAYER} received the\\n", "CIRCUIT PASS.$"),
    "BattleFrontier_ReceptionGate_Text_PlacedTrainerCardInFrontierPass": (
        "TRAINER data was added\\n", "to the CIRCUIT PASS.$"),
    "BattleFrontier_ReceptionGate_Text_EnjoyBattleFrontier": (
        "Enjoy everything offered by\\n", "CIRCUITO DE BATALHA!$"),
    "BattleFrontier_ReceptionGate_Text_IfItIsntPlayerYouCame": (
        "???: {PLAYER}{KUN}! You came.$",),
    "BattleFrontier_ReceptionGate_Text_OhMrScottGoodDay": (
        "GUIDE: Ah! SEU BENTO!\\n", "Good day, sir!$"),
    "BattleFrontier_ReceptionGate_Text_ScottGreatToSeeYouHere": (
        "SEU BENTO: Good to see you.\\n", "Explore at your own pace.\\p",
        "I want to see how far\\n", "your battle style can go.\\p",
        "I have a room nearby.\\n", "Visit whenever you want.$"),
    "BattleFrontier_ReceptionGate_Text_YourGuideToFacilities": (
        "I guide visitors through\\n", "CIRCUITO DE BATALHA.$"),
    "BattleFrontier_ReceptionGate_Text_LearnAboutWhich2": (
        "Which place interests you?$",),
    "BattleFrontier_ReceptionGate_Text_BattleTowerInfo": (
        "BATTLE TOWER is the tall tower\\n", "and symbol of the CIRCUITO.\\p",
        "It offers SINGLE, DOUBLE,\\n", "MULTI and LINK MULTI.$"),
    "BattleFrontier_ReceptionGate_Text_BattleDomeInfo": (
        "BATTLE DOME is the round\\n", "building shaped like an egg.\\p",
        "It hosts SINGLE and DOUBLE\\n", "tournaments.$"),
    "BattleFrontier_ReceptionGate_Text_BattlePalaceInfo": (
        "BATTLE PALACE is the red\\n", "building on the right.\\p",
        "It offers SINGLE and DOUBLE.$"),
    "BattleFrontier_ReceptionGate_Text_BattleArenaInfo": (
        "BATTLE ARENA stands on\\n", "the center-right side.\\p",
        "Its short tournament is judged\\n", "by battle performance.$"),
    "BattleFrontier_ReceptionGate_Text_BattleFactoryInfo": (
        "BATTLE FACTORY is near\\n", "the main entrance.\\p",
        "You battle with rental POKéMON\\n", "and may trade them.\\p",
        "It offers SINGLE and DOUBLE.$"),
    "BattleFrontier_ReceptionGate_Text_BattlePikeInfo": (
        "BATTLE PIKE is the long\\n", "POKéMON-shaped building.\\p",
        "Each room makes you choose\\n", "before moving on.$"),
    "BattleFrontier_ReceptionGate_Text_BattlePyramidInfo": (
        "BATTLE PYRAMID is the huge\\n", "pyramid in the complex.\\p",
        "Explore, battle and reach\\n", "the top.$"),
    "BattleFrontier_ReceptionGate_Text_RankingHallInfo": (
        "RANKING HALL is near\\n", "BATTLE TOWER.\\p",
        "It keeps the best CIRCUITO\\n", "challenge records.$"),
    "BattleFrontier_ReceptionGate_Text_ExchangeCornerInfo": (
        "EXCHANGE CORNER is near\\n", "BATTLE TOWER.\\p",
        "Trade Battle Points there\\n", "for rewards.$"),
    "BattleFrontier_ReceptionGate_Text_YourGuideToRules": (
        "I explain the common rules\\n", "used across the CIRCUITO.$"),
    "BattleFrontier_ReceptionGate_Text_LearnAboutWhat": (
        "Which rule interests you?$",),
    "BattleFrontier_ReceptionGate_Text_LevelModeInfo": (
        "Challenges use two modes:\\n", "Level 50 and Open Level.$"),
    "BattleFrontier_ReceptionGate_Text_Level50Info": (
        "Level 50 accepts POKéMON\\n", "at Lv. 50 or lower.\\p",
        "Opponents never use POKéMON\\n", "below Lv. 50.\\p",
        "It is a good place to start.$"),
    "BattleFrontier_ReceptionGate_Text_OpenLevelInfo": (
        "Open Level has no entry cap.\\p",
        "Opponents match your team's\\n", "level, but never below Lv. 60.$"),
    "BattleFrontier_ReceptionGate_Text_MonEntryInfo": (
        "Most POKéMON may enter.\\p", "EGGS and some species cannot.\\p",
        "Team size varies by facility.\\p",
        "Do not enter two POKéMON\\n", "of the same species.$"),
    "BattleFrontier_ReceptionGate_Text_HoldItemsInfo": (
        "Entered POKéMON cannot hold\\n", "duplicate items.\\p",
        "Each team member needs\\n", "a different held item.$"),
    "BattleFrontier_ReceptionGate_Text_YourGuideToFrontierPass": (
        "I explain the CIRCUIT PASS.$",),
    "BattleFrontier_ReceptionGate_Text_LearnAboutWhich1": (
        "Which part interests you?$",),
    "BattleFrontier_ReceptionGate_Text_SymbolsInfo": (
        "The CIRCUITO has seven\\n", "major facilities.\\p",
        "Strong challengers can earn\\n", "one SYMBOL at each.\\p",
        "You must win repeatedly.\\p", "It will not be easy. Good luck!$"),
    "BattleFrontier_ReceptionGate_Text_RecordedBattleInfo": (
        "The PASS can store one\\n", "battle recording.\\p",
        "It may be a friend battle\\n", "or a CIRCUITO challenge,\\p",
        "except BATTLE PIKE and\\n", "BATTLE PYRAMID matches.\\p",
        "Choose at battle's end\\n", "whether to save it.$"),
    "BattleFrontier_ReceptionGate_Text_BattlePointsInfo": (
        "Battle Points reward strong\\n", "CIRCUITO results.\\p",
        "Trade them for rewards\\n", "at EXCHANGE CORNER.$"),
}

REQUIRED_INTERNAL = (
    "VAR_HAS_ENTERED_BATTLE_FRONTIER",
    "FLAG_SYS_FRONTIER_PASS",
    "LOCALID_FRONTIER_RECEPTION_SCOTT",
    "SCROLL_MULTI_BF_RECEPTIONIST",
    "MULTI_FRONTIER_RULES",
    "MULTI_FRONTIER_PASS_INFO",
)


def pattern(label: str) -> re.Pattern[str]:
    return re.compile(
        rf"(?ms)^{re.escape(label)}:\n(?P<body>.*?)(?=^[A-Za-z0-9_]+(?:::|:)(?:\n|$)|\Z)"
    )


def validate_widths() -> None:
    for label, lines in BLOCKS.items():
        for line in lines:
            clean = PH.sub("PLAYER", line.replace("$", ""))
            for segment in CTRL.split(clean):
                segment = segment.strip()
                if len(segment) > MAX:
                    raise ValueError(f"{label}: {len(segment)} chars: {segment!r}")


def mask(text: str) -> str:
    out = text
    for label in BLOCKS:
        match = pattern(label).search(out)
        if not match:
            raise ValueError(f"missing reception block: {label}")
        start, end = match.span("body")
        out = out[:start] + '\t.string "<ARAUNA_EN>"\n\n' + out[end:]
    return out


def render(source: str) -> str:
    out = source
    for label, lines in BLOCKS.items():
        matches = list(pattern(label).finditer(out))
        if len(matches) != 1:
            raise ValueError(f"{label}: expected 1 block, found {len(matches)}")
        body = "".join(f'\t.string "{line}"\n' for line in lines) + "\n"
        start, end = matches[0].span("body")
        out = out[:start] + body + out[end:]
    if mask(source) != mask(out):
        raise ValueError("Reception Gate non-dialogue structure changed")
    for token in REQUIRED_INTERNAL:
        if token not in out:
            raise ValueError(f"missing preserved Reception Gate token: {token}")
    return out


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--in-place", action="store_true")
    args = parser.parse_args()
    if args.check and args.in_place:
        parser.error("choose --check or --in-place")
    validate_widths()
    source = TARGET.read_text(encoding="utf-8")
    out = render(source)
    if args.in_place and out != source:
        TARGET.write_text(out, encoding="utf-8")
    print(f"Battle Circuit reception English overlay OK: {len(BLOCKS)} blocks.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
