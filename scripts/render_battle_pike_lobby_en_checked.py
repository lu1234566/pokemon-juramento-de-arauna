#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BANK = ROOT / "data/text/arauna/en/battle_pike_lobby.json"
TARGET = ROOT / "data/maps/BattleFrontier_BattlePikeLobby/scripts.inc"

EXPECTED = {
    "BattleFrontier_BattlePikeLobby_Text_WelcomeToBattlePike",
    "BattleFrontier_BattlePikeLobby_Text_TakeChallenge",
    "BattleFrontier_BattlePikeLobby_Text_ExplainBattlePike",
    "BattleFrontier_BattlePikeLobby_Text_LookForwardToSeeingYou",
    "BattleFrontier_BattlePikeLobby_Text_WhichChallengeMode",
    "BattleFrontier_BattlePikeLobby_Text_NotEnoughValidMonsLv50",
    "BattleFrontier_BattlePikeLobby_Text_NotEnoughValidMonsLvOpen",
    "BattleFrontier_BattlePikeLobby_Text_PleaseChooseThreeMons",
    "BattleFrontier_BattlePikeLobby_Text_SaveBeforeChallenge",
    "BattleFrontier_BattlePikeLobby_Text_StepThisWay",
    "BattleFrontier_BattlePikeLobby_Text_ChallengeEndedRecordResults",
    "BattleFrontier_BattlePikeLobby_Text_PossessLuckInAbundance",
    "BattleFrontier_BattlePikeLobby_Text_ShallRecordResults",
    "BattleFrontier_BattlePikeLobby_Text_FailedToSaveBeforeQuitting",
    "BattleFrontier_BattlePikeLobby_Text_SnatchedVictoryFromQueen",
    "BattleFrontier_BattlePikeLobby_Text_AwardYouTheseBattlePoints",
    "BattleFrontier_BattlePikeLobby_Text_OneRoomAwayFromGoal",
    "BattleFrontier_BattlePikeLobby_Text_NeverHadToBattleTrainer",
    "BattleFrontier_BattlePikeLobby_Text_ThinkAbilitiesUsefulHere",
    "BattleFrontier_BattlePikeLobby_Text_RulesAreListed",
    "BattleFrontier_BattlePikeLobby_Text_ReadWhichHeading",
    "BattleFrontier_BattlePikeLobby_Text_ExplainPokenavBagRules",
    "BattleFrontier_BattlePikeLobby_Text_ExplainHeldItemRules",
    "BattleFrontier_BattlePikeLobby_Text_ExplainMonOrderRules",
}

CONTROL_RE = re.compile(r"\\[npl]")
PLACEHOLDER_WIDTH = {"{STR_VAR_1}": "LONGPHRASE123456"}


def fail(message: str) -> None:
    raise SystemExit(f"Battle Pike lobby renderer: {message}")


def load_bank() -> dict[str, list[str]]:
    data = json.loads(BANK.read_text(encoding="utf-8"))
    if set(data) != EXPECTED:
        missing = sorted(EXPECTED - set(data))
        extra = sorted(set(data) - EXPECTED)
        fail(f"bank contract mismatch; missing={missing}, extra={extra}")
    for label, segments in data.items():
        if not isinstance(segments, list) or not segments:
            fail(f"{label}: payload must be a non-empty list")
        for i, segment in enumerate(segments):
            if '"' in segment:
                fail(f"{label}: raw double quote is not allowed")
            if "$" in segment and not (i == len(segments) - 1 and segment.endswith("$")):
                fail(f"{label}: $ may appear only at the end of the final segment")
            visible = CONTROL_RE.sub("", segment[:-1] if segment.endswith("$") else segment)
            for placeholder, model in PLACEHOLDER_WIDTH.items():
                visible = visible.replace(placeholder, model)
            if len(visible) > 32:
                fail(f"{label}: visible segment exceeds 32 chars: {visible!r}")
        if not segments[-1].endswith("$"):
            fail(f"{label}: final segment must terminate with $")
    if sum(segment.count("{STR_VAR_1}") for segments in data.values() for segment in segments) != 2:
        fail("bank must preserve exactly two STR_VAR_1 eligibility placeholders")
    return data


def block_rx(label: str) -> re.Pattern[str]:
    return re.compile(
        rf'(?ms)^(?P<label>{re.escape(label)}:{{1,2}}\n)'
        rf'(?P<body>(?:\s*\.string\s+"(?:[^"\\]|\\.)*"\s*\n?)+)'
    )


def render(source: str, bank: dict[str, list[str]]) -> str:
    original = source
    for label in sorted(EXPECTED):
        rx = block_rx(label)
        matches = list(rx.finditer(source))
        if len(matches) != 1:
            fail(f"expected exactly one {label} block, found {len(matches)}")
        lines = "".join(f'\t.string "{segment}"\n' for segment in bank[label])
        source = rx.sub(lambda m: m.group("label") + lines, source, count=1)

    def mask(text: str) -> str:
        for label in sorted(EXPECTED):
            rx = block_rx(label)
            matches = list(rx.finditer(text))
            if len(matches) != 1:
                fail(f"mask expected exactly one {label} block, found {len(matches)}")
            text = rx.sub(lambda m: m.group("label") + "<PIKE_TEXT>\n", text, count=1)
        return text

    if mask(original) != mask(source):
        fail("non-dialogue source changed outside the 24 owned blocks")

    # Mechanical script tokens must remain byte-identical because only text bodies are owned.
    critical = (
        "frontier_checkineligible",
        "ChoosePartyForBattleFrontier",
        "pike_savehelditems",
        "pike_resethelditems",
        "pike_save",
        "frontier_givepoints",
        "frontier_isbrain",
        "FRONTIER_LVL_50",
        "FRONTIER_LVL_OPEN",
        "FRONTIER_PARTY_SIZE",
        "CloseBattlePikeCurtain",
        "MAP_BATTLE_FRONTIER_BATTLE_PIKE_CORRIDOR",
    )
    for token in critical:
        if original.count(token) != source.count(token):
            fail(f"critical token count changed: {token}")

    rendered_payload = "\n".join("".join(bank[label]) for label in sorted(EXPECTED))
    for stale in ("PIKE QUEEN", "luck in abundance", "snatched victory"):
        if stale.lower() in rendered_payload.lower():
            fail(f"stale Pike identity remains in owned payload: {stale}")
    for required in ("BATTLE PIKE", "JACI", "MASTER JACI", "Battle Points"):
        if required not in rendered_payload:
            fail(f"required Pike identity missing: {required}")
    return source


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--in-place", action="store_true")
    args = parser.parse_args()

    bank = load_bank()
    source = TARGET.read_text(encoding="utf-8")
    rendered = render(source, bank)
    # Idempotence model: rendering the rendered output must be byte-identical.
    rerendered = render(rendered, bank)
    if rerendered != rendered:
        fail("second render is not idempotent")
    if args.in_place:
        TARGET.write_text(rendered, encoding="utf-8")
    mode = "render" if args.in_place else "check"
    print(f"Battle Pike lobby {mode}: PASS (24 owned blocks)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
