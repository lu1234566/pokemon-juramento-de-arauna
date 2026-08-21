#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BANK = ROOT / "data" / "text" / "arauna" / "en" / "baia_luzes_interiors.json"
MAX_VISIBLE_WIDTH = 32
CONTROL_RE = re.compile(r"\\[npl]")
PLACEHOLDER_RE = re.compile(r"\{[^}]+\}")

EXPECTED: dict[str, tuple[str, tuple[str, ...]]] = {
    "house1": (
        "data/maps/LilycoveCity_House1/scripts.inc",
        (
            "LilycoveCity_House1_Text_PokemonPartnersNotTools",
            "LilycoveCity_House1_Text_Kecleon",
        ),
    ),
    "house2": (
        "data/maps/LilycoveCity_House2/scripts.inc",
        (
            "LilycoveCity_House2_Text_NotAwakeYetHaveThis",
            "LilycoveCity_House2_Text_SleepIsEssential",
        ),
    ),
    "house3": (
        "data/maps/LilycoveCity_House3/scripts.inc",
        (
            "LilycoveCity_House3_Text_LearnFromMasterOfPokeblocks",
            "LilycoveCity_House3_Text_OhAreYouSure",
            "LilycoveCity_House3_Text_ExplainPokeblocks",
            "LilycoveCity_House3_Text_HappyToHaveQuadruplets",
            "LilycoveCity_House3_Text_GoingToWinMultiBattles",
            "LilycoveCity_House3_Text_LikeMixingAtRecordCorner",
            "LilycoveCity_House3_Text_MakePokeblocksWithBerryBlender",
            "LilycoveCity_House3_Text_GoingToEnterContest",
        ),
    ),
    "house4": (
        "data/maps/LilycoveCity_House4/scripts.inc",
        (
            "LilycoveCity_House4_Text_MysteriesAtBottomOfSea",
            "LilycoveCity_House4_Text_UnderwaterTrenchMossdeepSootopolis",
        ),
    ),
    "move": (
        "data/maps/LilycoveCity_MoveDeletersHouse/scripts.inc",
        (
            "LilycoveCity_MoveDeletersHouse_Text_ICanMakeMonForgetMove",
            "LilycoveCity_MoveDeletersHouse_Text_WhichMonShouldForget",
            "LilycoveCity_MoveDeletersHouse_Text_WhichMoveShouldBeForgotten",
            "LilycoveCity_MoveDeletersHouse_Text_MonOnlyKnowsOneMove",
            "LilycoveCity_MoveDeletersHouse_Text_MonsMoveShouldBeForgotten",
            "LilycoveCity_MoveDeletersHouse_Text_MonHasForgottenMove",
            "LilycoveCity_MoveDeletersHouse_Text_ComeAgain",
            "LilycoveCity_MoveDeletersHouse_Text_EggCantForgetMoves",
            "LilycoveCity_MoveDeletersHouse_Text_CantForgetSurf",
        ),
    ),
    "motel1": (
        "data/maps/LilycoveCity_CoveLilyMotel_1F/scripts.inc",
        (
            "LilycoveCity_CoveLilyMotel_1F_Text_GuestsDoubledByMascot",
            "LilycoveCity_CoveLilyMotel_1F_Text_NoGuestsWithTeamAqua",
            "LilycoveCity_CoveLilyMotel_1F_Text_CantSeeTheTV",
            "LilycoveCity_CoveLilyMotel_1F_Text_MonFoundLostItem",
            "LilycoveCity_CoveLilyMotel_1F_Text_HeardAquaHideoutBusted",
            "LilycoveCity_CoveLilyMotel_1F_Text_HouseSittingMonCaughtBurglar",
            "LilycoveCity_CoveLilyMotel_1F_Text_BetterGetWorkingOnGuestsDinner",
        ),
    ),
    "motel2": (
        "data/maps/LilycoveCity_CoveLilyMotel_2F/scripts.inc",
        (
            "LilycoveCity_CoveLilyMotel_2F_Text_ShowMeCompletedDex",
            "LilycoveCity_CoveLilyMotel_2F_Text_FilledPokedexGiveYouThis",
            "LilycoveCity_CoveLilyMotel_2F_Text_ImTheProgrammer",
            "LilycoveCity_CoveLilyMotel_2F_Text_ImTheGraphicArtist",
            "LilycoveCity_CoveLilyMotel_2F_Text_GirlsAreCute",
            "LilycoveCity_CoveLilyMotel_2F_Text_SeaBreezeTicklesHeart",
            "LilycoveCity_CoveLilyMotel_2F_Text_NeverLeaveWithoutGameBoy",
            "LilycoveCity_CoveLilyMotel_2F_Text_SnoozingPreferBattles",
            "LilycoveCity_CoveLilyMotel_2F_Text_ContestsDoTakeStrategy",
        ),
    ),
    "pc1": (
        "data/maps/LilycoveCity_PokemonCenter_1F/scripts.inc",
        (
            "LilycoveCity_PokemonCenter_1F_Text_HowManyKindsOfPokemon",
            "LilycoveCity_PokemonCenter_1F_Text_HeardAboutRottenScoundrels",
            "LilycoveCity_PokemonCenter_1F_Text_HaventSeenRottenScoundrels",
        ),
    ),
}

PRESERVED: dict[str, tuple[str, ...]] = {
    "house1": ("SPECIES_KECLEON",),
    "house2": ("FLAG_RECEIVED_TM_REST", "ITEM_TM_REST"),
    "house3": ("random 4", "VAR_TEMP_1"),
    "house4": (),
    "move": (
        "IsSelectedMonEgg",
        "GetNumMovesSelectedMonHas",
        "MoveDeleterChooseMoveToForget",
        "IsLastMonThatKnowsSurf",
        "MoveDeleterForgetMove",
        "MAX_MON_MOVES",
    ),
    "motel1": ("FLAG_SYS_GAME_CLEAR", "FLAG_BADGE07_GET", "LOCALID_MOTEL_OWNER"),
    "motel2": (
        "HasAllHoennMons",
        "Special_ShowDiploma",
        "FLAG_MET_SCOTT_IN_LILYCOVE",
        "VAR_SCOTT_STATE",
        "FLAG_TEMP_2",
    ),
    "pc1": (
        "HEAL_LOCATION_LILYCOVE_CITY",
        "CableClub_OnResume",
        "SetLilycoveLadyGfx",
        "FLAG_BADGE07_GET",
    ),
}

FORBIDDEN_VISIBLE = (
    "CONSORCIO HORIZONTE",
    "HORIZONTE",
    "HIDEOUT",
    "GAME FREAK",
    "SCOTT:",
    "MOSSDEEP",
    "SOOTOPOLIS",
    "GAME BOY ADVANCE",
    "rotten scoundrels",
    "METEORITES",
)


def block_pattern(label: str) -> re.Pattern[str]:
    return re.compile(
        rf'(?m)^{re.escape(label)}:\n(?P<body>(?:\t\.string "[^\n]*"\n)+)'
    )


def load_bank() -> dict[str, dict[str, object]]:
    raw = json.loads(BANK.read_text(encoding="utf-8"))
    if raw.get("version") != 1 or raw.get("surface") != "baia_das_luzes_interiors":
        raise ValueError("unexpected Baia das Luzes interior bank header")
    sections = raw.get("sections")
    if not isinstance(sections, dict) or set(sections) != set(EXPECTED):
        raise ValueError("bank sections do not match the exact 8-section contract")

    total = 0
    for section, (expected_path, labels) in EXPECTED.items():
        entry = sections[section]
        if entry.get("path") != expected_path:
            raise ValueError(f"{section}: unexpected source path")
        blocks = entry.get("blocks")
        if not isinstance(blocks, dict) or set(blocks) != set(labels):
            raise ValueError(f"{section}: labels do not match the exact contract")
        for label in labels:
            payloads = blocks[label]
            if not isinstance(payloads, list) or not payloads or not all(isinstance(x, str) for x in payloads):
                raise ValueError(f"{label}: payload list is invalid")
            if not payloads[-1].endswith("$"):
                raise ValueError(f"{label}: final payload must end in $")
            if any("$" in payload for payload in payloads[:-1]):
                raise ValueError(f"{label}: $ terminator appears before final payload")
            if any('"' in payload for payload in payloads):
                raise ValueError(f"{label}: raw quote is not allowed")
            total += 1
    if total != 42:
        raise ValueError(f"expected 42 blocks, found {total}")
    return sections


def visible_segments(payload: str) -> list[str]:
    cleaned = PLACEHOLDER_RE.sub("LONGPHRASE123456", payload).replace("$", "")
    return [segment.strip() for segment in CONTROL_RE.split(cleaned)]


def validate_widths(sections: dict[str, dict[str, object]]) -> None:
    for section in EXPECTED:
        blocks = sections[section]["blocks"]
        for label, payloads in blocks.items():
            for payload in payloads:
                for segment in visible_segments(payload):
                    if len(segment) > MAX_VISIBLE_WIDTH:
                        raise ValueError(
                            f"{label}: visible segment is {len(segment)} chars, "
                            f"max {MAX_VISIBLE_WIDTH}: {segment!r}"
                        )


def render_one(source: str, blocks: dict[str, list[str]]) -> str:
    rendered = source
    for label, payloads in blocks.items():
        pattern = block_pattern(label)
        matches = list(pattern.finditer(rendered))
        if len(matches) != 1:
            raise ValueError(f"{label}: expected one .string block, found {len(matches)}")
        body = "".join(f'\t.string "{payload}"\n' for payload in payloads)
        start, end = matches[0].span("body")
        rendered = rendered[:start] + body + rendered[end:]
    return rendered


def mask_targets(source: str, labels: tuple[str, ...]) -> str:
    masked = source
    for label in labels:
        match = block_pattern(label).search(masked)
        if not match:
            raise ValueError(f"{label}: cannot mask missing block")
        start, end = match.span("body")
        masked = masked[:start] + '\t.string "<ARAUNA_BAIA_INTERIOR>"\n' + masked[end:]
    return masked


def validate_section(
    section: str,
    source: str,
    rendered: str,
    labels: tuple[str, ...],
    blocks: dict[str, list[str]],
) -> None:
    if mask_targets(source, labels) != mask_targets(rendered, labels):
        raise ValueError(f"{section}: non-dialogue structure changed")

    for token in PRESERVED[section]:
        before = source.count(token)
        after = rendered.count(token)
        if before == 0:
            raise ValueError(f"{section}: required gameplay token missing in source: {token}")
        if after != before:
            raise ValueError(f"{section}: gameplay token count changed: {token}")

    for label in labels:
        match = block_pattern(label).search(rendered)
        if not match:
            raise ValueError(f"{label}: rendered block missing")
        body = match.group("body")
        for payload in blocks[label]:
            if f'\t.string "{payload}"' not in body:
                raise ValueError(f"{label}: rendered payload missing: {payload!r}")
        for token in FORBIDDEN_VISIBLE:
            if token in body:
                raise ValueError(f"{label}: legacy visible token survived: {token}")

    if section == "motel2":
        for label in (
            "LilycoveCity_CoveLilyMotel_2F_Text_SnoozingPreferBattles",
            "LilycoveCity_CoveLilyMotel_2F_Text_ContestsDoTakeStrategy",
        ):
            body = block_pattern(label).search(rendered).group("body")
            if "SEU BENTO:" not in body:
                raise ValueError(f"{label}: Seu Bento visible identity missing")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Render Baia das Luzes daily-life interiors in reviewed English."
    )
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--in-place", action="store_true")
    args = parser.parse_args()
    if args.check and args.in_place:
        parser.error("use either --check or --in-place")

    sections = load_bank()
    validate_widths(sections)

    outputs: list[tuple[Path, str]] = []
    for section, (relative_path, labels) in EXPECTED.items():
        path = ROOT / relative_path
        source = path.read_text(encoding="utf-8")
        blocks = sections[section]["blocks"]
        rendered = render_one(source, blocks)
        validate_section(section, source, rendered, labels, blocks)
        outputs.append((path, rendered))

    if args.check:
        print("Baia das Luzes interior renderer OK: 42 blocks across 8 map files.")
        return 0
    if args.in_place:
        for path, rendered in outputs:
            path.write_text(rendered, encoding="utf-8")
        return 0

    for path, rendered in outputs:
        print(f"===== {path.relative_to(ROOT)} =====")
        print(rendered, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
