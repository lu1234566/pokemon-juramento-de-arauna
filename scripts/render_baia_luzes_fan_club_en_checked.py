#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BANK_PATH = ROOT / "data" / "text" / "arauna" / "en" / "baia_luzes_fan_club.json"
CLUB_PATH = ROOT / "data" / "maps" / "LilycoveCity_PokemonTrainerFanClub" / "scripts.inc"
TV_PATH = ROOT / "data" / "text" / "tv.inc"
MAX_VISIBLE_WIDTH = 32
PLACEHOLDER_SAMPLE = "LONGPHRASE123456"
CONTROL_RE = re.compile(r"\\[npl]")
PLACEHOLDER_RE = re.compile(r"\{[^}]+\}")

EXPECTED_CLUB = {
    "LilycoveCity_PokemonTrainerFanClub_Text_OhWowItsPlayer",
    "LilycoveCity_PokemonTrainerFanClub_Text_HeardAboutYouImYourFan",
    "LilycoveCity_PokemonTrainerFanClub_Text_YoureOneWeWantToWin",
    "LilycoveCity_PokemonTrainerFanClub_Text_OthersDontKnowYoureTheBest",
    "LilycoveCity_PokemonTrainerFanClub_Text_TrainersPowerIsOutOfTheOrdinary",
    "LilycoveCity_PokemonTrainerFanClub_Text_TrainerIsBestNoOneWantsToListen",
    "LilycoveCity_PokemonTrainerFanClub_Text_HearingAboutToughNewTrainer",
    "LilycoveCity_PokemonTrainerFanClub_Text_ImPullingForYou",
    "LilycoveCity_PokemonTrainerFanClub_Text_BrawlyNoImYourFan",
    "LilycoveCity_PokemonTrainerFanClub_Text_ICantHelpLikingBrawly",
    "LilycoveCity_PokemonTrainerFanClub_Text_NobodyUnderstandsBrawly",
    "LilycoveCity_PokemonTrainerFanClub_Text_MyFavoriteTrainerIsBrawly",
    "LilycoveCity_PokemonTrainerFanClub_Text_YouveSurpassedYourFather",
    "LilycoveCity_PokemonTrainerFanClub_Text_YourFatherNeverGaveUpSoKeepOnBattling",
    "LilycoveCity_PokemonTrainerFanClub_Text_LongWayToGoComparedToNorman",
    "LilycoveCity_PokemonTrainerFanClub_Text_YouAndNormanAreDifferent",
    "LilycoveCity_PokemonTrainerFanClub_Text_WeDiscussStrongestTrainers",
    "LilycoveCity_PokemonTrainerFanClub_Text_OhWoweeItsPlayer",
    "LilycoveCity_PokemonTrainerFanClub_Text_AlwaysCheerForYou",
    "LilycoveCity_PokemonTrainerFanClub_Text_EveryoneThinksTrainerIsCool",
    "LilycoveCity_PokemonTrainerFanClub_Text_TrainerIsReallyCoolItsJustMe",
    "LilycoveCity_PokemonTrainerFanClub_Text_WishThereWasTrainerLikeThat",
    "LilycoveCity_PokemonTrainerFanClub_Text_WantToBeStrongLikeYou",
    "LilycoveCity_PokemonTrainerFanClub_Text_OnlyOneWhoCheersForYou",
    "LilycoveCity_PokemonTrainerFanClub_Text_TrainerIsWickedlyCool",
    "LilycoveCity_PokemonTrainerFanClub_Text_NeverGoingToStopBeingTrainersFan",
    "LilycoveCity_PokemonTrainerFanClub_Text_YoureAmazingAfterAll",
    "LilycoveCity_PokemonTrainerFanClub_Text_ImInYourCorner",
    "LilycoveCity_PokemonTrainerFanClub_Text_ThinkTrainerIsNumberOne",
    "LilycoveCity_PokemonTrainerFanClub_Text_YoureMaybeStrongerThanTrainer",
    "LilycoveCity_PokemonTrainerFanClub_Text_YouChangedMyMind",
    "LilycoveCity_PokemonTrainerFanClub_Text_YouBattleAttractivelyInToughSituation",
    "LilycoveCity_PokemonTrainerFanClub_Text_TrainerIsStandout",
    "LilycoveCity_PokemonTrainerFanClub_Text_NoOneCanKnockYouButTrainerStronger",
    "LilycoveCity_PokemonTrainerFanClub_Text_YouImpressive",
    "LilycoveCity_PokemonTrainerFanClub_Text_OnlyIRecognizeYourTrueWorth",
    "LilycoveCity_PokemonTrainerFanClub_Text_HaventRealizedPotential",
    "LilycoveCity_PokemonTrainerFanClub_Text_YourePowerfulButNotTrueStrength",
}

EXPECTED_TV = {
    "LilycoveCity_PokemonTrainerFanClub_Text_WhatsYourOpinionOfTrainer",
    "LilycoveCity_PokemonTrainerFanClub_Text_ThatsWhatYouThink",
    "LilycoveCity_PokemonTrainerFanClub_Text_HaveYouForgottenTrainer",
    "LilycoveCity_PokemonTrainerFanClub_Text_WhatsYourOpinionOfTrainer2",
    "LilycoveCity_PokemonTrainerFanClub_Text_HowStrongRateTrainer",
    "LilycoveCity_PokemonTrainerFanClub_Text_HaveYouForgottenTrainer2",
    "LilycoveCity_PokemonTrainerFanClub_Text_YouShouldMeetTrainer",
    "LilycoveCity_PokemonTrainerFanClub_Text_ThankYouIllShareThisInfo",
    "LilycoveCity_PokemonTrainerFanClub_HopeYouCatchTVSpecial",
    "gTVTrainerFanClubSpecialText00",
    "gTVTrainerFanClubSpecialText01",
    "gTVTrainerFanClubSpecialText02",
    "gTVTrainerFanClubSpecialText03",
    "gTVTrainerFanClubSpecialText04",
    "gTVTrainerFanClubSpecialText05",
}

CLUB_GAMEPLAY_TOKENS = (
    "VAR_LILYCOVE_FAN_CLUB_STATE",
    "FANCLUB_MEMBER1",
    "FANCLUB_MEMBER2",
    "FANCLUB_MEMBER3",
    "FANCLUB_MEMBER4",
    "FANCLUB_MEMBER5",
    "FANCLUB_MEMBER6",
    "FANCLUB_MEMBER7",
    "FANCLUB_MEMBER8",
    "TryLoseFansFromPlayTime",
    "TryPutTrainerFanClubOnAir",
    "IsFanClubMemberFanOfPlayer",
    "GetNumFansOfPlayerInTrainerFanClub",
    "FLAG_HIDE_LILYCOVE_FAN_CLUB_INTERVIEWER",
    "FLAG_FAN_CLUB_STRENGTH_SHARED",
    "TVSHOW_FAN_CLUB_SPECIAL",
    "InterviewBefore",
    "EASY_CHAT_TYPE_FAN_QUESTION",
    "SCROLL_MULTI_POKEMON_FAN_CLUB_RATER",
    "PutFanClubSpecialOnTheAir",
)


def load_bank() -> dict[str, dict[str, list[str]]]:
    bank = json.loads(BANK_PATH.read_text(encoding="utf-8"))
    if set(bank) != {"club", "tv"}:
        raise ValueError(f"bank sections must be club/tv, found {sorted(bank)}")
    if set(bank["club"]) != EXPECTED_CLUB:
        missing = sorted(EXPECTED_CLUB - set(bank["club"]))
        extra = sorted(set(bank["club"]) - EXPECTED_CLUB)
        raise ValueError(f"club label contract mismatch; missing={missing}, extra={extra}")
    if set(bank["tv"]) != EXPECTED_TV:
        missing = sorted(EXPECTED_TV - set(bank["tv"]))
        extra = sorted(set(bank["tv"]) - EXPECTED_TV)
        raise ValueError(f"tv label contract mismatch; missing={missing}, extra={extra}")
    return bank


def validate_payloads(bank: dict[str, dict[str, list[str]]]) -> None:
    for section_name, section in bank.items():
        for label, payloads in section.items():
            if not payloads or not all(isinstance(item, str) and item for item in payloads):
                raise ValueError(f"{section_name}/{label}: payload list must contain strings")
            if not payloads[-1].endswith("$"):
                raise ValueError(f"{section_name}/{label}: final payload must end with $")
            if any("$" in payload for payload in payloads[:-1]):
                raise ValueError(f"{section_name}/{label}: early $ terminator")
            for payload in payloads:
                if '"' in payload:
                    raise ValueError(f"{section_name}/{label}: raw quote is not assembler-safe")
                visible = PLACEHOLDER_RE.sub(PLACEHOLDER_SAMPLE, payload).replace("$", "")
                for segment in CONTROL_RE.split(visible):
                    segment = segment.strip()
                    if len(segment) > MAX_VISIBLE_WIDTH:
                        raise ValueError(
                            f"{section_name}/{label}: visible segment is {len(segment)} chars: {segment!r}"
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
    rendered = source
    spans: list[tuple[int, int, str]] = []
    for label, payloads in targets.items():
        start, end = body_span(source, label)
        new_body = "".join(f'\t.string "{payload}"\n' for payload in payloads)
        spans.append((start, end, new_body))
    for start, end, new_body in sorted(spans, reverse=True):
        rendered = rendered[:start] + new_body + rendered[end:]
    return rendered


def mask_targets(source: str, labels: set[str], marker: str) -> str:
    spans = []
    for label in labels:
        start, end = body_span(source, label)
        spans.append((start, end))
    masked = source
    for start, end in sorted(spans, reverse=True):
        masked = masked[:start] + f'\t.string "<{marker}>"\n' + masked[end:]
    return masked


def validate_structure(source: str, rendered: str, labels: set[str], marker: str) -> None:
    if mask_targets(source, labels, marker) != mask_targets(rendered, labels, marker):
        raise ValueError(f"{marker}: non-dialogue structure changed")


def validate_gameplay_counts(source: str, rendered: str) -> None:
    for token in CLUB_GAMEPLAY_TOKENS:
        before = source.count(token)
        after = rendered.count(token)
        if before == 0:
            raise ValueError(f"expected Fan Club gameplay token missing in source: {token}")
        if before != after:
            raise ValueError(f"Fan Club gameplay token count changed: {token}: {before} -> {after}")


def validate_rendered(club: str, tv: str, bank: dict[str, dict[str, list[str]]]) -> None:
    for label, payloads in bank["club"].items():
        start, end = body_span(club, label)
        body = club[start:end]
        for payload in payloads:
            if f'\t.string "{payload}"' not in body:
                raise ValueError(f"club/{label}: rendered payload missing: {payload!r}")
    for label, payloads in bank["tv"].items():
        start, end = body_span(tv, label)
        body = tv[start:end]
        for payload in payloads:
            if f'\t.string "{payload}"' not in body:
                raise ValueError(f"tv/{label}: rendered payload missing: {payload!r}")

    owned = "\n".join(
        club[body_span(club, label)[0]:body_span(club, label)[1]] for label in EXPECTED_CLUB
    ) + "\n" + "\n".join(
        tv[body_span(tv, label)[0]:body_span(tv, label)[1]] for label in EXPECTED_TV
    )
    for stale in (
        "ADEMAR: O mar devolve",
        "ELIAS: Ser seu pai",
        "all over HOENN",
        "mere sidekick",
        "underling",
    ):
        if stale in owned:
            raise ValueError(f"legacy Fan Club surface survived: {stale}")
    for required in ("ADEMAR", "ELIAS", "ARAUNA", "opinion", "Reputations can change"):
        if required not in owned:
            raise ValueError(f"required Fan Club identity missing: {required}")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Render the complete Baia das Luzes Trainer Fan Club and its TV interview/special in English."
    )
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--in-place", action="store_true")
    args = parser.parse_args()
    if args.check and args.in_place:
        parser.error("use either --check or --in-place")

    bank = load_bank()
    validate_payloads(bank)
    club_source = CLUB_PATH.read_text(encoding="utf-8")
    tv_source = TV_PATH.read_text(encoding="utf-8")
    club_rendered = render_text(club_source, bank["club"])
    tv_rendered = render_text(tv_source, bank["tv"])

    validate_structure(club_source, club_rendered, EXPECTED_CLUB, "ARAUNA_FAN_CLUB")
    validate_structure(tv_source, tv_rendered, EXPECTED_TV, "ARAUNA_FAN_TV")
    validate_gameplay_counts(club_source, club_rendered)
    validate_rendered(club_rendered, tv_rendered, bank)

    if args.check:
        print(
            f"Baia das Luzes Fan Club English renderer OK: "
            f"{len(EXPECTED_CLUB) + len(EXPECTED_TV)} text blocks validated."
        )
        return 0
    if args.in_place:
        CLUB_PATH.write_text(club_rendered, encoding="utf-8")
        TV_PATH.write_text(tv_rendered, encoding="utf-8")
        return 0

    print(club_rendered, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
