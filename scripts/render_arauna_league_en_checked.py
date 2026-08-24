#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data" / "text" / "arauna" / "en" / "league_finale.json"
TRAINERS_PATH = ROOT / "src" / "data" / "trainers.h"
MAX_VISIBLE_WIDTH = 32
CONTROL_RE = re.compile(r"\\[npl]")
PLACEHOLDER_RE = re.compile(r"\{[^}]+\}")

# Width of the longest value each placeholder can expand to at runtime, from
# include/constants/global.h. A blanket 16 overstates {PLAYER}, which the name
# entry screen caps at PLAYER_NAME_LENGTH, and would reject dialogue that fits.
PLACEHOLDER_WIDTHS = {
    "{PLAYER}": 7,     # PLAYER_NAME_LENGTH
    "{RIVAL}": 7,      # rival names use the same cap
    "{STR_VAR_1}": 14, # widest runtime buffer: ITEM_NAME_LENGTH
    "{STR_VAR_2}": 14,
    "{STR_VAR_3}": 14,
}
DEFAULT_PLACEHOLDER_WIDTH = 14


def model_placeholders(text: str) -> str:
    """Expand placeholders to their widest runtime value for width checking."""
    def expand(match: re.Match[str]) -> str:
        token = match.group(0)
        return "X" * PLACEHOLDER_WIDTHS.get(token, DEFAULT_PLACEHOLDER_WIDTH)

    return PLACEHOLDER_RE.sub(expand, text)


FILES = {
    "ever_grande": "data/maps/EverGrandeCity/scripts.inc",
    "center": "data/maps/EverGrandeCity_PokemonCenter_1F/scripts.inc",
    "league_1f": "data/maps/EverGrandeCity_PokemonLeague_1F/scripts.inc",
    "victory_1f": "data/maps/VictoryRoad_1F/scripts.inc",
    "victory_b1f": "data/maps/VictoryRoad_B1F/scripts.inc",
    "victory_b2f": "data/maps/VictoryRoad_B2F/scripts.inc",
    "elite_lazaro": "data/maps/EverGrandeCity_SidneysRoom/scripts.inc",
    "elite_rosa": "data/maps/EverGrandeCity_PhoebesRoom/scripts.inc",
    "elite_clara": "data/maps/EverGrandeCity_GlaciasRoom/scripts.inc",
    "elite_tiburcio": "data/maps/EverGrandeCity_DrakesRoom/scripts.inc",
    "champion": "data/maps/EverGrandeCity_ChampionsRoom/scripts.inc",
}

EXPECTED_COUNTS = {
    "ever_grande": 3,
    "center": 3,
    "league_1f": 3,
    "victory_1f": 21,
    "victory_b1f": 15,
    "victory_b2f": 18,
    "elite_lazaro": 3,
    "elite_rosa": 3,
    "elite_clara": 3,
    "elite_tiburcio": 3,
    "champion": 13,
}

REQUIRED_TOKENS = {
    "ever_grande": (
        "FLAG_VISITED_EVER_GRANDE_CITY",
        "FLAG_SYS_WEATHER_CTRL",
    ),
    "center": (
        "FLAG_MET_SCOTT_IN_EVERGRANDE",
        "VAR_SCOTT_STATE",
        "LOCALID_EVER_GRANDE_SCOTT",
    ),
    "league_1f": (
        "FLAG_ENTERED_ELITE_FOUR",
        "FLAG_BADGE06_GET",
        "MUS_OBTAIN_BADGE",
    ),
    "victory_1f": (
        "TRAINER_WALLY_VR_1",
        "TRAINER_WALLY_VR_2",
        "FLAG_DEFEATED_WALLY_VICTORY_ROAD",
        "VAR_VICTORY_ROAD_1F_STATE",
    ),
    "victory_b1f": (
        "TRAINER_SAMUEL",
        "TRAINER_SHANNON",
        "TRAINER_MICHELLE",
        "TRAINER_MITCHELL",
        "TRAINER_HALLE",
    ),
    "victory_b2f": (
        "TRAINER_VITO",
        "TRAINER_OWEN",
        "TRAINER_CAROLINE",
        "TRAINER_JULIE",
        "TRAINER_FELIX",
        "TRAINER_DIANNE",
    ),
    "elite_lazaro": (
        "TRAINER_SIDNEY",
        "FLAG_DEFEATED_ELITE_4_SIDNEY",
        "VAR_ELITE_4_STATE",
    ),
    "elite_rosa": (
        "TRAINER_PHOEBE",
        "FLAG_DEFEATED_ELITE_4_PHOEBE",
        "VAR_ELITE_4_STATE",
    ),
    "elite_clara": (
        "TRAINER_GLACIA",
        "FLAG_DEFEATED_ELITE_4_GLACIA",
        "VAR_ELITE_4_STATE",
    ),
    "elite_tiburcio": (
        "TRAINER_DRAKE",
        "FLAG_DEFEATED_ELITE_4_DRAKE",
        "FANCOUNTER_DEFEATED_DRAKE",
        "VAR_ELITE_4_STATE",
    ),
    "champion": (
        "TRAINER_WALLACE",
        "MAP_EVER_GRANDE_CITY_HALL_OF_FAME",
        "ProfBirch_EventScript_RatePokedex",
        "LOCALID_CHAMPIONS_ROOM_RIVAL",
    ),
}

TRAINER_NAMES = {
    "TRAINER_SIDNEY": ("SIDNEY", "LAZARO"),
    "TRAINER_PHOEBE": ("PHOEBE", "ROSA"),
    "TRAINER_GLACIA": ("GLACIA", "CLARA"),
    "TRAINER_DRAKE": ("DRAKE", "TIBURCIO"),
}

FORBIDDEN_VISIBLE_RE = re.compile(
    r"\b(?:SIDNEY|PHOEBE|GLACIA|DRAKE|SCOTT|VICTORY ROAD|"
    r"VOCE|NAO|LIGA|INSIGNIAS|CAMPEAO|PERDI|CONQUISTOU)\b",
    re.IGNORECASE,
)


def fail(message: str) -> None:
    raise ValueError(f"League finale English renderer: {message}")


def load_targets() -> dict[str, dict[str, list[str]]]:
    raw = json.loads(DATA_PATH.read_text(encoding="utf-8"))
    if set(raw) != set(FILES):
        missing = sorted(set(FILES) - set(raw))
        extra = sorted(set(raw) - set(FILES))
        fail(f"JSON section mismatch; missing={missing}, extra={extra}")

    for section, expected_count in EXPECTED_COUNTS.items():
        entries = raw[section]
        if not isinstance(entries, dict) or len(entries) != expected_count:
            fail(
                f"{section}: expected {expected_count} labels, "
                f"found {len(entries) if isinstance(entries, dict) else 'non-object'}"
            )
        for label, chunks in entries.items():
            if not re.fullmatch(r"[A-Za-z0-9_]+", label):
                fail(f"{section}: unsafe label {label!r}")
            if not isinstance(chunks, list) or not chunks or not all(
                isinstance(chunk, str) and chunk for chunk in chunks
            ):
                fail(f"{section}:{label}: payload must be a non-empty string list")
            joined = "".join(chunks)
            if joined.count("$") != 1 or not joined.endswith("$"):
                fail(f"{section}:{label}: text must contain one final '$'")
            for chunk in chunks:
                if '"' in chunk:
                    fail(f"{section}:{label}: raw double quote is not allowed")
            for visible in CONTROL_RE.split(joined):
                modeled = model_placeholders(visible).replace("$", "")
                if len(modeled) > MAX_VISIBLE_WIDTH:
                    fail(
                        f"{section}:{label}: visible line exceeds "
                        f"{MAX_VISIBLE_WIDTH} chars: {modeled!r}"
                    )
            if FORBIDDEN_VISIBLE_RE.search(joined):
                fail(f"{section}:{label}: stale Portuguese/Emerald identity survived")
    return raw


def block_pattern(label: str) -> re.Pattern[str]:
    return re.compile(
        rf"(?m)^(?P<label>{re.escape(label)}:\n)"
        rf"(?P<body>(?:\t\.string \"(?:[^\"\\]|\\.)*\"\n)+)"
    )


def render_text(source: str, section: str, targets: dict[str, dict[str, list[str]]]) -> str:
    rendered = source
    for label, chunks in targets[section].items():
        pattern = block_pattern(label)
        matches = list(pattern.finditer(rendered))
        if len(matches) != 1:
            fail(f"{section}:{label}: expected one target block, found {len(matches)}")
        body = "".join(f'\t.string "{chunk}"\n' for chunk in chunks)
        rendered = (
            rendered[: matches[0].start("body")]
            + body
            + rendered[matches[0].end("body") :]
        )
    return rendered


def mask_target_bodies(
    source: str, section: str, targets: dict[str, dict[str, list[str]]]
) -> str:
    masked = source
    for label in targets[section]:
        pattern = block_pattern(label)
        matches = list(pattern.finditer(masked))
        if len(matches) != 1:
            fail(f"{section}:{label}: cannot mask target uniquely")
        masked = (
            masked[: matches[0].start("body")]
            + f'\t.string "<{label}>$"\n'
            + masked[matches[0].end("body") :]
        )
    return masked


def validate_text(
    source: str,
    rendered: str,
    section: str,
    targets: dict[str, dict[str, list[str]]],
) -> None:
    if mask_target_bodies(source, section, targets) != mask_target_bodies(
        rendered, section, targets
    ):
        fail(f"{section}: non-target script structure changed")

    for token in REQUIRED_TOKENS[section]:
        if source.count(token) != rendered.count(token):
            fail(f"{section}: gameplay token count changed for {token}")

    for label in targets[section]:
        match = block_pattern(label).search(rendered)
        if match is None:
            fail(f"{section}:{label}: rendered target missing")
        if FORBIDDEN_VISIBLE_RE.search(match.group("body")):
            fail(f"{section}:{label}: stale visible token survived rendering")


def trainer_entry_pattern(trainer_id: str) -> re.Pattern[str]:
    return re.compile(
        rf"(?ms)^(?P<prefix>\s*\[{re.escape(trainer_id)}\]\s*=\s*\{{.*?"
        rf"^\s*\.trainerName\s*=\s*_\(\")"
        rf"(?P<name>[^\"]+)"
        rf"(?P<suffix>\"\),)"
    )


def render_trainer_names(source: str) -> str:
    rendered = source
    for trainer_id, (legacy, final) in TRAINER_NAMES.items():
        pattern = trainer_entry_pattern(trainer_id)
        matches = list(pattern.finditer(rendered))
        if len(matches) != 1:
            fail(f"{trainer_id}: expected one trainer entry, found {len(matches)}")
        current = matches[0].group("name")
        if current not in (legacy, final):
            fail(f"{trainer_id}: unexpected visible trainer name {current!r}")
        if current == legacy:
            rendered = (
                rendered[: matches[0].start("name")]
                + final
                + rendered[matches[0].end("name") :]
            )

    wallace = trainer_entry_pattern("TRAINER_WALLACE").search(rendered)
    if wallace is None or wallace.group("name") != "AMALIA":
        fail("TRAINER_WALLACE must retain current canonical visible name AMALIA")
    return rendered


def mask_trainer_names(source: str) -> str:
    masked = source
    for trainer_id in TRAINER_NAMES:
        pattern = trainer_entry_pattern(trainer_id)
        match = pattern.search(masked)
        if match is None:
            fail(f"{trainer_id}: cannot mask trainer name")
        masked = (
            masked[: match.start("name")]
            + f"<{trainer_id}>"
            + masked[match.end("name") :]
        )
    return masked


def validate_trainer_names(source: str, rendered: str) -> None:
    if mask_trainer_names(source) != mask_trainer_names(rendered):
        fail("non-Elite trainer data changed")
    for trainer_id, (_, final) in TRAINER_NAMES.items():
        match = trainer_entry_pattern(trainer_id).search(rendered)
        if match is None or match.group("name") != final:
            fail(f"{trainer_id}: final visible name is not {final}")
    for token in (
        "TRAINER_SIDNEY",
        "TRAINER_PHOEBE",
        "TRAINER_GLACIA",
        "TRAINER_DRAKE",
        "TRAINER_WALLACE",
    ):
        if source.count(token) != rendered.count(token):
            fail(f"trainer identifier count changed for {token}")


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Render Oath Road, the Arauna League, the four canonical Elite voices "
            "and Champion Amalia in English while preserving Emerald mechanics."
        )
    )
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--in-place", action="store_true")
    parser.add_argument("--dump-targets", action="store_true")
    args = parser.parse_args()
    if sum(bool(x) for x in (args.check, args.in_place, args.dump_targets)) > 1:
        parser.error("use only one of --check, --in-place or --dump-targets")

    targets = load_targets()
    if args.dump_targets:
        print(json.dumps(targets, ensure_ascii=False, indent=2))
        return 0

    for section, rel_path in FILES.items():
        path = ROOT / rel_path
        source = path.read_text(encoding="utf-8")
        rendered = render_text(source, section, targets)
        validate_text(source, rendered, section, targets)
        if args.in_place:
            path.write_text(rendered, encoding="utf-8")

    trainer_source = TRAINERS_PATH.read_text(encoding="utf-8")
    trainer_rendered = render_trainer_names(trainer_source)
    validate_trainer_names(trainer_source, trainer_rendered)
    if args.in_place:
        TRAINERS_PATH.write_text(trainer_rendered, encoding="utf-8")

    block_count = sum(len(entries) for entries in targets.values())
    mode = "Rendered" if args.in_place else "Validated"
    print(
        f"{mode} Arauna League finale English surface: {block_count} text blocks "
        f"across {len(FILES)} maps plus {len(TRAINER_NAMES)} Elite battle names."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
