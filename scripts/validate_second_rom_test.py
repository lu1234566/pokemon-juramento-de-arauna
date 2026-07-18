#!/usr/bin/env python3
"""Validate the English second-ROM-test package and its reachable test supplies."""

from __future__ import annotations

from pathlib import Path


def require(source: str, token: str, context: str) -> None:
    if token not in source:
        raise ValueError(f"{context} is missing: {token}")


def block(source: str, start: str, end: str) -> str:
    if start not in source or end not in source:
        raise ValueError(f"cannot locate script block {start}")
    return source.split(start, 1)[1].split(end, 1)[0]


def main() -> None:
    house = Path("data/maps/AraunaPlayerHouse/scripts.inc").read_text(encoding="utf-8")
    center = Path("data/maps/AraunaResearchCenter/scripts.inc").read_text(encoding="utf-8")
    new_game = Path("src/new_game.c").read_text(encoding="utf-8")
    flags = Path("include/constants/flags.h").read_text(encoding="utf-8")
    events = Path("data/event_scripts.s").read_text(encoding="utf-8")
    runtime = Path("tools/arauna/validate_english_runtime.py").read_text(encoding="utf-8")
    workflow = Path(".github/workflows/build.yml").read_text(encoding="utf-8")
    makefile = Path("Makefile").read_text(encoding="utf-8")
    wrapper = Path("data/text/arauna/second_rom_test.inc").read_text(encoding="utf-8")
    text = Path("data/text/arauna/en/second_rom_test.inc").read_text(encoding="utf-8")
    checklist = Path("docs/arauna/SECOND_ROM_TEST_CHECKLIST.md").read_text(encoding="utf-8")
    dexnav = Path("include/config/dexnav.h").read_text(encoding="utf-8")

    require(makefile, "ARAUNA_LANGUAGE ?= ENGLISH", "English-only build")
    require(makefile, "ARAUNA_LANGUAGE_SUFFIX := en", "English ROM suffix")
    require(workflow, "make ARAUNA_LANGUAGE=ENGLISH", "English CI build")
    require(workflow, "python3 scripts/validate_second_rom_test.py", "second-test CI step")
    require(new_game, "WarpToAraunaOpening();", "reachable campaign entrypoint")
    require(new_game, "MAP_ARAUNA_PLAYER_HOUSE", "reachable Arauna prologue")
    if "WarpToTruck();" in new_game or "MAP_INSIDE_OF_TRUCK" in new_game:
        raise ValueError("the second test still starts in vanilla Emerald")

    require(flags, "#define FLAG_ARAUNA_SECOND_TEST_CANDIES_RECEIVED     0x34", "one-time flag")
    require(flags, "FLAG_ARAUNA_BADGE_MARE", "Mare Badge route")
    require(flags, "FLAG_ARAUNA_BADGE_UIVO", "Uivo Badge route")

    supply = center.split(
        "AraunaResearchCenter_EventScript_GiveSecondTestCandies::", 1
    )[1]
    for token in (
        "goto_if_set FLAG_ARAUNA_SECOND_TEST_CANDIES_RECEIVED",
        "checkitemspace ITEM_RARE_CANDY, 999",
        "giveitem ITEM_RARE_CANDY, 999",
        "setflag FLAG_ARAUNA_SECOND_TEST_CANDIES_RECEIVED",
        "AraunaSecondTest_Text_RareCandiesReceived",
        "AraunaSecondTest_Text_RareCandiesBagFull",
    ):
        require(supply, token, "test-supply subroutine")

    complete = block(
        house,
        "AraunaPlayerHouse_EventScript_CompleteChoice::",
        "AraunaPlayerHouse_EventScript_AssignRemainingStarters::",
    )
    require(complete, "setvar VAR_ARAUNA_STORY_STAGE, 2", "starter confirmation")
    require(
        complete,
        "call AraunaResearchCenter_EventScript_GiveSecondTestCandies",
        "immediate reachable delivery",
    )
    require(house, "AraunaPlayerHouse_EventScript_AnahiAfterChoice", "home retry")
    if "givemon " in center:
        raise ValueError("the research annex can still bypass Dona Zila's prologue")

    require(events, '#include "data/text/arauna/second_rom_test.inc"', "runtime text registration")
    require(runtime, '"second_rom_test.inc"', "English runtime pack")
    require(runtime, '"arauna/second_rom_test"', "English runtime wrapper")
    require(wrapper, '.include "data/text/arauna/en/second_rom_test.inc"', "English-only test wrapper")
    if "/pt/" in wrapper or "PORTUGUESE" in wrapper:
        raise ValueError("second-test runtime wrapper must not select Portuguese")
    for token in ("999", "RARE CANDIES", "PROF. ANAHI"):
        require(text, token, "English Rare Candy delivery message")
    for raw in text.splitlines():
        if '.string "' in raw:
            visible = raw.split('.string "', 1)[1].rsplit('"', 1)[0]
            for marker in ("\\n", "\\p", "$"):
                visible = visible.replace(marker, "")
            if len(visible) > 32:
                raise ValueError(f"GBA text line exceeds 32 characters: {visible}")

    require(dexnav, "#define DEXNAV_ENABLED                FALSE", "DexNav test gate")
    for validator_path in (
        "scripts/validate_arauna_opening.py",
        "scripts/validate_arauna_porto_reuse.py",
        "scripts/validate_arauna_serra_reuse.py",
    ):
        if not Path(validator_path).is_file():
            raise ValueError(f"campaign validator is missing: {validator_path}")
    for token in (
        "999 Rare Candies",
        "Maré Badge",
        "Uivo Badge",
        "new save",
        "Vila Amanhecer",
        "Dona Zila",
    ):
        require(checklist, token, "manual test checklist")

    print(
        "Second ROM test validated: English build, reachable Vila Amanhecer "
        "prologue, one-time 999 Rare Candies and route through Uivo Badge"
    )


if __name__ == "__main__":
    main()
