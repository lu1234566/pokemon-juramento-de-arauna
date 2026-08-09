#!/usr/bin/env python3
"""Validate the two story-masked battles that gate Arauna's first badges."""

from __future__ import annotations

from pathlib import Path


def require(source: str, token: str, context: str) -> None:
    if token not in source:
        raise ValueError(f"{context} is missing: {token}")


def ordered(source: str, tokens: tuple[str, ...], context: str) -> None:
    positions = [source.find(token) for token in tokens]
    if any(position < 0 for position in positions) or positions != sorted(positions):
        raise ValueError(f"{context} is not ordered safely: {tokens}")


def script_block(source: str, start: str, end: str) -> str:
    if start not in source or end not in source:
        raise ValueError(f"cannot locate {start}")
    return source.split(start, 1)[1].split(end, 1)[0]


def validate_text_width(path: str) -> None:
    text = Path(path).read_text(encoding="utf-8")
    for raw in text.splitlines():
        if '.string "' not in raw:
            continue
        visible = raw.split('.string "', 1)[1].rsplit('"', 1)[0]
        for marker in ("\\n", "\\p", "$"):
            visible = visible.replace(marker, "")
        if len(visible) > 32:
            raise ValueError(f"{path} exceeds 32 characters: {visible}")


def main() -> None:
    flags = Path("include/constants/flags.h").read_text(encoding="utf-8")
    opponents = Path("include/constants/opponents.h").read_text(encoding="utf-8")
    porto = Path("data/maps/RustboroCity/scripts.inc").read_text(encoding="utf-8")
    serra = Path("data/maps/Route114/scripts.inc").read_text(encoding="utf-8")
    trainers = Path("src/data/trainers.party").read_text(encoding="utf-8")
    checklist = Path("docs/arauna/SECOND_ROM_TEST_CHECKLIST.md").read_text(encoding="utf-8")
    design = Path("docs/arauna/MASKED_BADGE_TRIALS.md").read_text(encoding="utf-8")

    require(flags, "#define FLAG_ARAUNA_MARE_TRIAL_COMPLETE             0x35", "Maré trial flag")
    require(flags, "#define FLAG_ARAUNA_UIVO_TRIAL_COMPLETE             0x36", "Uivo trial flag")
    require(opponents, "#define TRAINER_ARAUNA_MARE_TRIAL           857", "Maré trial trainer ID")
    require(opponents, "#define TRAINER_ARAUNA_UIVO_TRIAL           858", "Uivo trial trainer ID")
    require(opponents, "#define TRAINERS_COUNT_EMERALD     861", "Emerald trainer count")
    require(opponents, "#define MAX_TRAINERS_COUNT_EMERALD 864", "trainer flag capacity")

    porto_trial = script_block(
        porto,
        "AraunaPorto_EventScript_DonaCelinaAwardBadge::",
        "AraunaPorto_EventScript_DonaCelinaGrantBadge::",
    )
    ordered(
        porto_trial,
        (
            "goto_if_set FLAG_ARAUNA_MARE_TRIAL_COMPLETE",
            "trainerbattle_single TRAINER_ARAUNA_MARE_TRIAL",
            "setflag FLAG_ARAUNA_MARE_TRIAL_COMPLETE",
        ),
        "Tide Vigil",
    )
    porto_reward = porto.split("AraunaPorto_EventScript_DonaCelinaGrantBadge::", 1)[1]
    ordered(
        porto_reward,
        (
            "setflag FLAG_ARAUNA_BADGE_MARE",
            "setflag FLAG_BADGE01_GET",
            "setvar VAR_ARAUNA_BADGE_COUNT, 1",
        ),
        "Maré Badge reward",
    )

    serra_trial = script_block(
        serra,
        "AraunaSerra_EventScript_HermitAwardBadge::",
        "AraunaSerra_EventScript_HermitGrantBadge::",
    )
    ordered(
        serra_trial,
        (
            "goto_if_set FLAG_ARAUNA_UIVO_TRIAL_COMPLETE",
            "trainerbattle_single TRAINER_ARAUNA_UIVO_TRIAL",
            "setflag FLAG_ARAUNA_UIVO_TRIAL_COMPLETE",
        ),
        "Trial of Echoes",
    )
    serra_reward = serra.split("AraunaSerra_EventScript_HermitGrantBadge::", 1)[1]
    ordered(
        serra_reward,
        (
            "setflag FLAG_ARAUNA_BADGE_UIVO",
            "setflag FLAG_BADGE02_GET",
            "setvar VAR_ARAUNA_BADGE_COUNT, 2",
        ),
        "Uivo Badge reward",
    )

    mare_team = script_block(
        trainers,
        "=== TRAINER_ARAUNA_MARE_TRIAL ===",
        "=== TRAINER_ARAUNA_UIVO_TRIAL ===",
    )
    for token in (
        "Name: CELINA", "Pidgey", "Level: 14", "Vulpix", "Level: 15",
        "Venusaur @ Oran Berry", "Level: 17",
    ):
        require(mare_team, token, "provisional Tide Vigil team")

    uivo_team = trainers.split("=== TRAINER_ARAUNA_UIVO_TRIAL ===", 1)[1]
    for token in (
        "Magneton", "Level: 23", "Murkrow", "Level: 24",
        "Jumpluff", "Level: 25", "Dunsparce @ Sitrus Berry", "Level: 27",
    ):
        require(uivo_team, token, "provisional Trial of Echoes team")

    if "wildbattle" in porto_trial or "wildbattle" in serra_trial:
        raise ValueError("story entities must not be turned into badge wild battles")
    for path in (
        "data/text/arauna/en/porto_das_redes.inc",
        "data/text/arauna/en/serra_do_uivo.inc",
    ):
        validate_text_width(path)
    for token in ("TIDE VIGIL", "TRIAL OF ECHOES", "Lose once"):
        require(checklist, token, "manual retry checklist")
    normalized_design = " ".join(design.lower().split())
    for token in ("no new map", "provisional", "story mission"):
        require(normalized_design, token, "badge-trial design contract")

    print("Masked badge trials validated: two mandatory, retry-safe story battles before badge rewards")


if __name__ == "__main__":
    main()
