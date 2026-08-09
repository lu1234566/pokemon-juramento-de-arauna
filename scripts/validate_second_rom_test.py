#!/usr/bin/env python3
"""Validate the English second-ROM-test package and its reachable test supplies."""

from __future__ import annotations

import re
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
    overworld = Path("src/overworld.c").read_text(encoding="utf-8")
    pokedex = Path("src/pokedex.c").read_text(encoding="utf-8")
    trainers = Path("src/data/trainers.party").read_text(encoding="utf-8")
    flags = Path("include/constants/flags.h").read_text(encoding="utf-8")
    events = Path("data/event_scripts.s").read_text(encoding="utf-8")
    runtime = Path("tools/arauna/validate_english_runtime.py").read_text(encoding="utf-8")
    workflow = Path(".github/workflows/build.yml").read_text(encoding="utf-8")
    makefile = Path("Makefile").read_text(encoding="utf-8")
    checklist = Path("docs/arauna/SECOND_ROM_TEST_CHECKLIST.md").read_text(encoding="utf-8")
    dexnav = Path("include/config/dexnav.h").read_text(encoding="utf-8")
    caps = Path("src/caps.c").read_text(encoding="utf-8")
    cap_config = Path("include/config/caps.h").read_text(encoding="utf-8")
    party_menu = Path("src/party_menu.c").read_text(encoding="utf-8")
    party_menu_data = Path("src/data/party_menu.h").read_text(encoding="utf-8")

    require(makefile, "ARAUNA_LANGUAGE ?= ENGLISH", "English-only build")
    require(makefile, "ARAUNA_LANGUAGE_SUFFIX := en", "English ROM suffix")
    require(workflow, "make ARAUNA_LANGUAGE=ENGLISH", "English CI build")
    require(workflow, "python3 scripts/validate_second_rom_test.py", "second-test CI step")
    require(new_game, "WarpToAraunaOpening();", "reachable campaign entrypoint")
    require(new_game, "MAP_ARAUNA_PLAYER_HOUSE", "reachable Arauna prologue")
    if "WarpToTruck();" in new_game or "MAP_INSIDE_OF_TRUCK" in new_game:
        raise ValueError("the second test still starts in vanilla Emerald")
    callback = block(overworld, "void CB2_NewGame(void)", "#if OW_USE_FAKE_RTC")
    require(
        callback,
        "gFieldCallback = FieldCB_WarpExitFadeFromBlack;",
        "Arauna new-game field callback",
    )
    if "ExecuteTruckSequence" in callback:
        raise ValueError("the Arauna house still executes the Emerald truck sequence")

    scrollbar_marker = "static void SpriteCB_Scrollbar(struct Sprite *sprite)"
    if pokedex.count(scrollbar_marker) < 2:
        raise ValueError("cannot locate the SpriteCB_Scrollbar definition")
    scrollbar = pokedex.rsplit(scrollbar_marker, 1)[1].split(
        "static void SpriteCB_ScrollArrow(struct Sprite *sprite)", 1
    )[0]
    require(
        scrollbar,
        "sPokedexView->pokemonListCount <= 1",
        "single-entry Pokédex guard",
    )
    require(scrollbar, "sprite->y2 = 0;", "single-entry Pokédex guard")

    required_trainers = {
        "TRAINER_ARAUNA_CIRO_PIMPAU": ("Name: CIRO", "Treecko", "Level: 7"),
        "TRAINER_ARAUNA_CIRO_CARAMELO": ("Name: CIRO", "Torchic", "Level: 7"),
        "TRAINER_ARAUNA_CIRO_QUERO": ("Name: CIRO", "Mudkip", "Level: 7"),
        "TRAINER_ARAUNA_TECH_AGENT": ("Name: AGENT", "Seadra", "Level: 12"),
        "TRAINER_ARAUNA_MARE_TRIAL": ("Name: CELINA", "Level: 17"),
        "TRAINER_ARAUNA_UIVO_TRIAL": ("Name: HERMIT", "Level: 27"),
    }
    trainer_blocks: dict[str, str] = {}
    for trainer, tokens in required_trainers.items():
        marker = f"=== {trainer} ==="
        if marker not in trainers:
            raise ValueError(f"scripted Arauna trainer has no party data: {trainer}")
        trainer_block = trainers.split(marker, 1)[1].split("\n=== ", 1)[0]
        trainer_blocks[trainer] = trainer_block
        for token in tokens:
            require(trainer_block, token, f"{trainer} party data")

    boss_groups = (
        (("TRAINER_ARAUNA_CIRO_PIMPAU", "TRAINER_ARAUNA_CIRO_CARAMELO", "TRAINER_ARAUNA_CIRO_QUERO"), 7),
        (("TRAINER_ARAUNA_TECH_AGENT",), 12),
        (("TRAINER_ARAUNA_MARE_TRIAL",), 17),
        (("TRAINER_ARAUNA_UIVO_TRIAL",), 27),
    )
    for trainers_in_group, expected_cap in boss_groups:
        levels = [
            int(level)
            for trainer in trainers_in_group
            for level in re.findall(r"Level:\s*(\d+)", trainer_blocks[trainer])
        ]
        if not levels or max(levels) != expected_cap:
            raise ValueError(
                f"next-boss cap mismatch for {trainers_in_group}: "
                f"expected {expected_cap}, found {max(levels) if levels else 'no levels'}"
            )
        require(caps, f"return {expected_cap};", f"story cap for {trainers_in_group[0]}")

    for token in (
        "bool32 IsAraunaNextBossLevelCapAvailable(void)",
        "return !FlagGet(FLAG_ARAUNA_BADGE_UIVO);",
        "if (FlagGet(FLAG_ARAUNA_BADGE_MARE))",
        "if (FlagGet(FLAG_ARAUNA_PORTO_AGENT_DEFEATED))",
        "if (VarGet(VAR_ARAUNA_STORY_STAGE) >= 8)",
        "return MAX_LEVEL;",
    ):
        require(caps, token, "mandatory-boss level-cap routing")
    level_cap_section = caps.split("u32 GetCurrentLevelCap(void)", 1)[1].split(
        "u32 GetSoftLevelCapExpValue", 1
    )[0]
    if "FLAG_BADGE01_GET" in level_cap_section:
        raise ValueError("vanilla Hoenn badges still control Arauna's level cap")
    require(cap_config, "#define B_RARE_CANDY_CAP                TRUE", "Rare Candy level cap")
    for token in (
        "MENU_LEVEL_CAP",
        "u8 actions[9];",
        "CursorCb_LevelCap",
        "AppendToList(sPartyMenuInternal->actions, &sPartyMenuInternal->numActions, MENU_LEVEL_CAP)",
        "while (GetMonData(mon, MON_DATA_LEVEL) < levelCap)",
        "ExecuteTableBasedItemEffect(mon, ITEM_RARE_CANDY",
        "Task_DisplayLevelUpStatsPg1",
        "Task_TryLearnNewMoves",
        "sLevelCapActionActive",
        "if (sLevelCapActionActive)\n        InitPartyMenu(PARTY_MENU_TYPE_FIELD, PARTY_LAYOUT_SINGLE, PARTY_ACTION_CHOOSE_MON",
    ):
        require(party_menu, token, "LEVEL CAP party-menu action")
    require(
        party_menu_data,
        '[MENU_LEVEL_CAP]       = {COMPOUND_STRING("LEVEL CAP"),',
        "LEVEL CAP menu label",
    )

    require(flags, "FLAG_ARAUNA_BADGE_MARE", "Mare Badge route")
    require(flags, "FLAG_ARAUNA_BADGE_UIVO", "Uivo Badge route")

    complete = block(
        house,
        "AraunaPlayerHouse_EventScript_CompleteChoice::",
        "AraunaPlayerHouse_EventScript_AssignRemainingStarters::",
    )
    require(complete, "setvar VAR_ARAUNA_STORY_STAGE, 2", "starter confirmation")
    require(house, "AraunaPlayerHouse_EventScript_AnahiAfterChoice", "home retry")
    # The Research Center is where the partner is chosen now. What must not be
    # bypassed is the night before it and Dona Zila's founding story after, so
    # check the handoff instead of forbidding the give.
    require(center, "goto AraunaPlayerHouse_EventScript_CompleteChoice",
            "Research Center partner selection")
    require(house, "AraunaPlayerHouse_EventScript_ZilaFoundingStory", "founding story")

    require(dexnav, "#define DEXNAV_ENABLED                FALSE", "DexNav test gate")
    for validator_path in (
        "scripts/validate_arauna_opening.py",
        "scripts/validate_arauna_porto_reuse.py",
        "scripts/validate_arauna_serra_reuse.py",
    ):
        if not Path(validator_path).is_file():
            raise ValueError(f"campaign validator is missing: {validator_path}")
    for token in (
        "Maré Badge",
        "Uivo Badge",
        "new save",
        "Vila Amanhecer",
        "Dona Zila",
        "LEVEL CAP",
        "Ciro — Lv. 7",
        "Consortium Agent — Lv. 12",
        "Dona Celina — Lv. 17",
        "Hermit — Lv. 27",
    ):
        require(checklist, token, "manual test checklist")

    print(
        "Second ROM test validated: English build, reachable Vila Amanhecer "
        "prologue, mandatory-boss LEVEL CAP QoL and route through Uivo Badge"
    )


if __name__ == "__main__":
    main()
