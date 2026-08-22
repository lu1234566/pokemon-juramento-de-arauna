#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BANK_PATH = ROOT / "data" / "text" / "arauna" / "en" / "baia_luzes_museum.json"
FILES = {
    "1f": ROOT / "data" / "maps" / "LilycoveCity_LilycoveMuseum_1F" / "scripts.inc",
    "2f": ROOT / "data" / "maps" / "LilycoveCity_LilycoveMuseum_2F" / "scripts.inc",
}
EXPECTED = {
    "1f": {
        "LilycoveCity_LilycoveMuseum_1F_Text_WelcomeToLilycoveMuseum",
        "LilycoveCity_LilycoveMuseum_1F_Text_ImCuratorHaveYouViewedOurPaintings",
        "LilycoveCity_LilycoveMuseum_1F_Text_NotDisturbYouTakeYourTime",
        "LilycoveCity_LilycoveMuseum_1F_Text_HaveYouAnInterestInPaintings",
        "LilycoveCity_LilycoveMuseum_1F_Text_HonoredYoudVisitInSpiteOfThat",
        "LilycoveCity_LilycoveMuseum_1F_Text_ExcellentCanYouComeWithMe",
        "LilycoveCity_LilycoveMuseum_1F_Text_VeryOldPainting",
        "LilycoveCity_LilycoveMuseum_1F_Text_OddLandscapeFantasticScenery",
        "LilycoveCity_LilycoveMuseum_1F_Text_PaintingOfBeautifulWoman",
        "LilycoveCity_LilycoveMuseum_1F_Text_PaintingOfLegendaryPokemon",
        "LilycoveCity_LilycoveMuseum_1F_Text_PaintingOfGrassPokemon",
        "LilycoveCity_LilycoveMuseum_1F_Text_PaintingOfBerries",
        "LilycoveCity_LilycoveMuseum_Text_BirdPokemonSculptureReplica",
        "LilycoveCity_LilycoveMuseum_1F_Text_BigPokeBallCarvedFromStone",
        "LilycoveCity_LilycoveMuseum_1F_Text_StoneTabletWithAncientText",
        "LilycoveCity_LilycoveMuseum_1F_Text_WorksOfMagnificence",
        "LilycoveCity_LilycoveMuseum_1F_Text_MustntForgetLoveForFineArts",
        "LilycoveCity_LilycoveMuseum_1F_Text_ThisMuseumIsInspiration",
        "LilycoveCity_LilycoveMuseum_1F_Text_ThisLadyIsPretty",
        "LilycoveCity_LilycoveMuseum_1F_Text_ThisPokemonIsAdorable",
        "LilycoveCity_LilycoveMuseum_1F_Text_HeardMuseumGotNewPaintings",
        "LilycoveCity_LilycoveMuseum_1F_Text_CuratorHasBeenCheerful",
        "LilycoveCity_LilycoveMuseum_1F_Text_AimToSeeGreatPaintings",
        "LilycoveCity_LilycoveMuseum_1F_Text_MuseumTouristDestination",
    },
    "2f": {
        "LilycoveCity_LilycoveMuseum_2F_Text_ThisIsExhibitHall",
        "LilycoveCity_LilycoveMuseum_2F_Text_ExplainExhibitHall",
        "LilycoveCity_LilycoveMuseum_2F_Text_PleaseObtainPaintingsForExhibit",
        "LilycoveCity_LilycoveMuseum_2F_Text_WishToFillExhibit",
        "LilycoveCity_LilycoveMuseum_2F_Text_ThanksAddedNewPainting",
        "LilycoveCity_LilycoveMuseum_2F_Text_ItsYouPlayer",
        "LilycoveCity_LilycoveMuseum_2F_Text_PaintingsAttractedMoreGuests",
        "LilycoveCity_LilycoveMuseum_2F_Text_TokenOfGratitude",
        "LilycoveCity_LilycoveMuseum_2F_Text_KeepThisForYou",
        "LilycoveCity_LilycoveMuseum_2F_Text_HonorToHaveYouVisit",
        "LilycoveCity_LilycoveMuseum_2F_Text_ItsPinkPictureFrame",
        "LilycoveCity_LilycoveMuseum_2F_Text_ItsYellowPictureFrame",
        "LilycoveCity_LilycoveMuseum_2F_Text_ItsBluePictureFrame",
        "LilycoveCity_LilycoveMuseum_2F_Text_ItsRedPictureFrame",
        "LilycoveCity_LilycoveMuseum_2F_Text_ItsGreenPictureFrame",
        "LilycoveCity_LilycoveMuseum_2F_Text_ItsPaintingOfPokemon",
        "LilycoveCity_LilycoveMuseum_2F_Text_NewPaintingsSurprisedMe",
        "LilycoveCity_LilycoveMuseum_2F_Text_NewPaintingsRatherAmusing",
        "LilycoveCity_LilycoveMuseum_2F_Text_ThesePaintingsOfYourPokemon",
    },
}
GAMEPLAY_TOKENS = {
    "1f": (
        "MULTI_VIEWED_PAINTINGS",
        "VAR_FACING",
        "MAP_LILYCOVE_CITY_LILYCOVE_MUSEUM_2F",
        "LOCALID_MUSEUM_1F_CURATOR",
        "Common_Movement_FacePlayer",
        "warp MAP_LILYCOVE_CITY_LILYCOVE_MUSEUM_2F",
    ),
    "2f": (
        "FLAG_COOL_PAINTING_MADE",
        "FLAG_BEAUTY_PAINTING_MADE",
        "FLAG_CUTE_PAINTING_MADE",
        "FLAG_SMART_PAINTING_MADE",
        "FLAG_TOUGH_PAINTING_MADE",
        "VAR_LILYCOVE_MUSEUM_2F_STATE",
        "CountPlayerMuseumPaintings",
        "DECOR_GLASS_ORNAMENT",
        "FLAG_RECEIVED_GLASS_ORNAMENT",
        "CONTEST_WINNER_MUSEUM_COOL",
        "CONTEST_WINNER_MUSEUM_BEAUTY",
        "CONTEST_WINNER_MUSEUM_CUTE",
        "CONTEST_WINNER_MUSEUM_SMART",
        "CONTEST_WINNER_MUSEUM_TOUGH",
    ),
}
MAX_VISIBLE_WIDTH = 32
PLACEHOLDER_SAMPLE = "LONGPHRASE123456"
CONTROL_RE = re.compile(r"\\[npl]")
PLACEHOLDER_RE = re.compile(r"\{[^}]+\}")


def load_bank() -> dict[str, dict[str, list[str]]]:
    bank = json.loads(BANK_PATH.read_text(encoding="utf-8"))
    if set(bank) != set(FILES):
        raise ValueError(f"bank sections mismatch: {sorted(bank)}")
    for section, expected in EXPECTED.items():
        actual = set(bank[section])
        if actual != expected:
            raise ValueError(
                f"{section}: label contract mismatch; "
                f"missing={sorted(expected - actual)}, extra={sorted(actual - expected)}"
            )
    return bank


def validate_payloads(bank: dict[str, dict[str, list[str]]]) -> None:
    for section, entries in bank.items():
        for label, payloads in entries.items():
            if not payloads or not all(isinstance(x, str) and x for x in payloads):
                raise ValueError(f"{section}/{label}: payloads must be non-empty strings")
            if not payloads[-1].endswith("$"):
                raise ValueError(f"{section}/{label}: final payload must end with $")
            if any("$" in payload for payload in payloads[:-1]):
                raise ValueError(f"{section}/{label}: early $ terminator")
            for payload in payloads:
                if '"' in payload:
                    raise ValueError(f"{section}/{label}: raw quote is not assembler-safe")
                visible = PLACEHOLDER_RE.sub(PLACEHOLDER_SAMPLE, payload).replace("$", "")
                for segment in CONTROL_RE.split(visible):
                    segment = segment.strip()
                    if len(segment) > MAX_VISIBLE_WIDTH:
                        raise ValueError(
                            f"{section}/{label}: visible segment is "
                            f"{len(segment)} chars: {segment!r}"
                        )


def label_match(source: str, label: str) -> re.Match[str]:
    pattern = re.compile(rf"(?m)^{re.escape(label)}::?\n")
    matches = list(pattern.finditer(source))
    if len(matches) != 1:
        raise ValueError(f"{label}: expected one label, found {len(matches)}")
    return matches[0]


def body_span(source: str, label: str) -> tuple[int, int]:
    match = label_match(source, label)
    start = match.end()
    pos = start
    saw_string = False
    continuation = False
    while pos < len(source):
        newline = source.find("\n", pos)
        end = len(source) if newline < 0 else newline + 1
        line = source[pos:end]
        stripped = line.lstrip(" \t")
        is_string = stripped.startswith(".string ")
        if is_string or continuation:
            saw_string = saw_string or is_string
            continuation = line.rstrip("\n").endswith("\\")
            pos = end
            continue
        break
    if not saw_string:
        raise ValueError(f"{label}: no consecutive .string body found")
    return start, pos


def render_text(source: str, targets: dict[str, list[str]]) -> str:
    spans: list[tuple[int, int, str]] = []
    for label, payloads in targets.items():
        start, end = body_span(source, label)
        new_body = "".join(f'\t.string "{payload}"\n' for payload in payloads)
        spans.append((start, end, new_body))
    rendered = source
    for start, end, new_body in sorted(spans, reverse=True):
        rendered = rendered[:start] + new_body + rendered[end:]
    return rendered


def mask_targets(source: str, labels: set[str], marker: str) -> str:
    spans = [body_span(source, label) for label in labels]
    masked = source
    for start, end in sorted(spans, reverse=True):
        masked = masked[:start] + f'\t.string "<{marker}>"\n' + masked[end:]
    return masked


def validate_structure(section: str, source: str, rendered: str) -> None:
    marker = f"ARAUNA_MUSEUM_{section.upper()}"
    if mask_targets(source, EXPECTED[section], marker) != mask_targets(
        rendered, EXPECTED[section], marker
    ):
        raise ValueError(f"{section}: non-dialogue Museum structure changed")


def validate_gameplay_counts(section: str, source: str, rendered: str) -> None:
    for token in GAMEPLAY_TOKENS[section]:
        before = source.count(token)
        after = rendered.count(token)
        if before == 0:
            raise ValueError(f"{section}: expected Museum gameplay token missing: {token}")
        if before != after:
            raise ValueError(
                f"{section}: Museum gameplay token count changed: "
                f"{token}: {before} -> {after}"
            )


def validate_rendered(section: str, rendered: str, targets: dict[str, list[str]]) -> None:
    for label, payloads in targets.items():
        start, end = body_span(rendered, label)
        body = rendered[start:end]
        for payload in payloads:
            if f'\t.string "{payload}"' not in body:
                raise ValueError(f"{section}/{label}: rendered payload missing: {payload!r}")

    owned = "\n".join(
        rendered[body_span(rendered, label)[0]:body_span(rendered, label)[1]]
        for label in EXPECTED[section]
    )
    if "Welcome to LILYCOVE MUSEUM" in owned or "great for LILYCOVE" in owned:
        raise ValueError(f"{section}: legacy LILYCOVE museum identity survived")
    if section == "1f" and "BAIA DAS LUZES MUSEUM" not in owned:
        raise ValueError("1f: BAIA DAS LUZES MUSEUM identity missing")
    if section == "2f":
        for required in ("maker's permission", "Permission comes before display"):
            if required not in owned:
                raise ValueError(f"2f: permission/provenance identity missing: {required}")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Render Baia das Luzes Museum 1F/2F local English surface."
    )
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--in-place", action="store_true")
    args = parser.parse_args()
    if args.check and args.in_place:
        parser.error("use either --check or --in-place")

    bank = load_bank()
    validate_payloads(bank)
    outputs: dict[str, str] = {}
    for section, path in FILES.items():
        source = path.read_text(encoding="utf-8")
        rendered = render_text(source, bank[section])
        validate_structure(section, source, rendered)
        validate_gameplay_counts(section, source, rendered)
        validate_rendered(section, rendered, bank[section])
        outputs[section] = rendered

    if args.check:
        print(
            "Baia das Luzes Museum English renderer OK: "
            f"{sum(len(labels) for labels in EXPECTED.values())} text blocks validated."
        )
        return 0
    if args.in_place:
        for section, path in FILES.items():
            path.write_text(outputs[section], encoding="utf-8")
        return 0

    print(outputs["1f"], end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
