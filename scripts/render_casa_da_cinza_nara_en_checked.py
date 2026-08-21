#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "text" / "arauna" / "en" / "casa_da_cinza.json"
FILES = {
    "town": ROOT / "data" / "maps" / "LavaridgeTown" / "scripts.inc",
    "gym": ROOT / "data" / "maps" / "LavaridgeTown_Gym_1F" / "scripts.inc",
}
EXPECTED_COUNTS = {"town": 19, "gym": 39}
MAX_VISIBLE_WIDTH = 32
CONTROL_RE = re.compile(r"\\[npl]")
PLACEHOLDER_RE = re.compile(r"\{[^}]+\}")

RAW_MARKERS = {
    "LavaridgeTown_Text_MayNiceBadgesTakeThis": ("MAY:",),
    "LavaridgeTown_Text_MayExplainGoGogglesChallengeDad": ("CIRO:",),
    "LavaridgeTown_Text_BrendanNiceBadgesTakeThis": ("BRENDAN:",),
    "LavaridgeTown_Text_BrendanExplainGoGogglesChallengeDad": ("CIRO:",),
    "LavaridgeTown_Text_BatheInHotSpringsEveryDay": ("FLANNERY",),
    "LavaridgeTown_Text_TownSign": ("SERTAO DE DENTRO",),
    "LavaridgeTown_Text_GymSign": ("NARA",),
    "LavaridgeTown_Gym_1F_Text_GymGuideAdvice": ("FLANNERY",),
    "LavaridgeTown_Gym_1F_Text_AxleDefeat": ("FLANNERY",),
    "LavaridgeTown_Gym_B1F_Text_KeeganPostBattle": ("FLANNERY",),
    "LavaridgeTown_Gym_1F_Text_DaniellePostBattle": ("FLANNERY",),
    "LavaridgeTown_Gym_B1F_Text_EliPostBattle": ("FLANNERY",),
    "LavaridgeTown_Gym_1F_Text_FlanneryIntro": ("NARA:",),
    "LavaridgeTown_Gym_1F_Text_ReceivedHeatBadge": ("INSÍGNIA CINZA",),
    "LavaridgeTown_Gym_1F_Text_RegisteredFlannery": ("FLANNERY",),
    "LavaridgeTown_Gym_1F_Text_GymStatue": ("LAVARIDGE",),
    "LavaridgeTown_Gym_1F_Text_GymStatueCertified": ("FLANNERY",),
}

CRITICAL_TOKENS = {
    "town": (
        "ITEM_GO_GOGGLES",
        "FLAG_RECEIVED_GO_GOGGLES",
        "VAR_LAVARIDGE_TOWN_STATE",
        "FLAG_RECEIVED_LAVARIDGE_EGG",
        "SPECIES_WYNAUT",
        "GAME_STAT_ENTERED_HOT_SPRINGS",
    ),
    "gym": (
        "TRAINER_FLANNERY_1",
        "TRAINER_COLE",
        "TRAINER_GERALD",
        "TRAINER_AXLE",
        "TRAINER_DANIELLE",
        "TRAINER_KEEGAN",
        "TRAINER_JACE",
        "TRAINER_JEFF",
        "TRAINER_ELI",
        "FLAG_DEFEATED_LAVARIDGE_GYM",
        "FLAG_BADGE04_GET",
        "ITEM_TM_OVERHEAT",
        "FLAG_RECEIVED_TM_OVERHEAT",
        "FLAG_ENABLE_FLANNERY_MATCH_CALL",
        "VAR_LAVARIDGE_TOWN_STATE",
        "FLAG_WHITEOUT_TO_LAVARIDGE",
    ),
}

STALE_VISIBLE = (
    "MAY:",
    "BRENDAN:",
    "LAVARIDGE",
    "FLANNERY",
    "SERTAO DE DENTRO",
    "RESPONSAVEL",
    "INSÍGNIA",
    "Nao ",
    "nao ",
    "Cinza e ",
)

def load_bank() -> dict[str, dict[str, tuple[str, ...]]]:
    raw = json.loads(DATA.read_text(encoding="utf-8"))
    if set(raw) != set(FILES):
        raise ValueError(f"section contract mismatch: {sorted(raw)}")
    bank: dict[str, dict[str, tuple[str, ...]]] = {}
    for section, expected_count in EXPECTED_COUNTS.items():
        entries = raw[section]
        if not isinstance(entries, dict) or len(entries) != expected_count:
            raise ValueError(f"{section}: expected {expected_count} labels")
        converted: dict[str, tuple[str, ...]] = {}
        for label, payloads in entries.items():
            if not isinstance(payloads, list) or not payloads:
                raise ValueError(f"{label}: expected non-empty payload list")
            payload_tuple = tuple(str(payload) for payload in payloads)
            if any('"' in payload for payload in payload_tuple):
                raise ValueError(f"{label}: raw double quote is not allowed")
            if any("$" in payload for payload in payload_tuple[:-1]):
                raise ValueError(f"{label}: terminator may appear only in final payload")
            if not payload_tuple[-1].endswith("$"):
                raise ValueError(f"{label}: final payload must end with $")
            converted[label] = payload_tuple
        bank[section] = converted
    return bank

def block_pattern(label: str) -> re.Pattern[str]:
    # Historical Arauna text patches sometimes use assembler line continuation,
    # so own consecutive `.string` records plus any physical continuation lines.
    return re.compile(
        rf"(?m)^{re.escape(label)}:\n"
        rf"(?P<body>(?:\t\.string [^\n]*\n"
        rf"(?:^(?!\t|[A-Za-z0-9_]+:|\s*$)[^\n]*\n)*)+)"
    )

def replacement(payloads: tuple[str, ...]) -> str:
    return "".join(f'\t.string "{payload}"\n' for payload in payloads)

def visible_segments(payload: str) -> list[str]:
    cleaned = PLACEHOLDER_RE.sub("LONGPHRASE123456", payload).replace("$", "")
    return [segment.strip() for segment in CONTROL_RE.split(cleaned)]

def validate_widths(bank: dict[str, dict[str, tuple[str, ...]]]) -> None:
    for entries in bank.values():
        for label, payloads in entries.items():
            for payload in payloads:
                for segment in visible_segments(payload):
                    if len(segment) > MAX_VISIBLE_WIDTH:
                        raise ValueError(
                            f"{label}: visible segment is {len(segment)} chars: {segment!r}"
                        )

def render_one(section: str, source: str, entries: dict[str, tuple[str, ...]]) -> str:
    rendered = source
    before_counts = {token: source.count(token) for token in CRITICAL_TOKENS[section]}

    for label, payloads in entries.items():
        matches = list(block_pattern(label).finditer(rendered))
        if len(matches) != 1:
            raise ValueError(f"{label}: expected exactly one text block, found {len(matches)}")
        body = matches[0].group("body")
        new_body = replacement(payloads)
        if body != new_body:
            for marker in RAW_MARKERS.get(label, ()):
                if marker not in body:
                    raise ValueError(f"{label}: expected raw marker missing: {marker!r}")
        start, end = matches[0].span("body")
        rendered = rendered[:start] + new_body + rendered[end:]

    masked_source = source
    masked_rendered = rendered
    for label in entries:
        for name, text in (("source", masked_source), ("rendered", masked_rendered)):
            match = block_pattern(label).search(text)
            if not match:
                raise ValueError(f"{label}: cannot mask {name} block")
            start, end = match.span("body")
            text = text[:start] + "\t.string \"<CASA_DA_CINZA_BLOCK>\"\n" + text[end:]
            if name == "source":
                masked_source = text
            else:
                masked_rendered = text
    if masked_source != masked_rendered:
        raise ValueError(f"{section}: non-dialogue structure changed")

    after_counts = {token: rendered.count(token) for token in CRITICAL_TOKENS[section]}
    if before_counts != after_counts:
        raise ValueError(f"{section}: progression token counts changed: {before_counts} -> {after_counts}")

    for label in entries:
        body = block_pattern(label).search(rendered).group("body")
        for token in STALE_VISIBLE:
            if token in body:
                raise ValueError(f"{label}: stale visible token survived: {token!r}")
    return rendered

def validate_identity(bank: dict[str, dict[str, tuple[str, ...]]]) -> None:
    town = bank["town"]
    gym = bank["gym"]
    if town["LavaridgeTown_Text_MayNiceBadgesTakeThis"] != town["LavaridgeTown_Text_BrendanNiceBadgesTakeThis"]:
        raise ValueError("Ciro first post-Gym gender slots diverged")
    if town["LavaridgeTown_Text_MayExplainGoGogglesChallengeDad"] != town["LavaridgeTown_Text_BrendanExplainGoGogglesChallengeDad"]:
        raise ValueError("Ciro second post-Gym gender slots diverged")
    joined = "\n".join(payload for entries in bank.values() for payloads in entries.values() for payload in payloads)
    for required in ("CASA DA CINZA", "NARA", "ASH BADGE", "CIRO:", "PAMPA DA ESPERA"):
        if required not in joined:
            raise ValueError(f"required story identity missing: {required}")

def main() -> int:
    parser = argparse.ArgumentParser(
        description="Render Casa da Cinza, Ciro post-Gym, and Nara's Gym in English without changing Emerald progression."
    )
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--in-place", action="store_true")
    args = parser.parse_args()
    if args.check and args.in_place:
        parser.error("use either --check or --in-place")

    bank = load_bank()
    validate_widths(bank)
    validate_identity(bank)
    rendered_by_section: dict[str, str] = {}
    for section, path in FILES.items():
        source = path.read_text(encoding="utf-8")
        rendered_by_section[section] = render_one(section, source, bank[section])

    if args.check:
        print(f"Casa da Cinza English renderer OK: {sum(len(v) for v in bank.values())} blocks validated.")
        return 0
    if args.in_place:
        for section, path in FILES.items():
            path.write_text(rendered_by_section[section], encoding="utf-8")
        return 0
    for section in FILES:
        print(f"===== {section} =====")
        print(rendered_by_section[section], end="" if rendered_by_section[section].endswith("\n") else "\n")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
