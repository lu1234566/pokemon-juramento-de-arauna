#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from tools import cleanup_littleroot_house_residue as source_contract  # noqa: E402

MAX_VISIBLE_WIDTH = 32
CONTROL_RE = re.compile(r"\\[npl]")
PLACEHOLDER_RE = re.compile(r"\{[^}]+\}")

CIRO_INTRO = (
    "CIRO: So you're {PLAYER}.\\p",
    "ANAHI said you'd arrive.\\p",
    "I expected someone... different.\\p",
    "We'll talk later. I'm late\\n",
    "for fieldwork.$",
)

CIRO_READY = (
    "CIRO: I'm finishing my notes\\n",
    "from ROUTE 103.\\p",
    "HORIZON wants data before dark.$",
)

ENGLISH: dict[str, tuple[str, ...]] = {
    "PlayersHouse_1F_Text_IsntItNiceInHere": (
        "MOM: We're here, {PLAYER}.\\p",
        "Still feels strange, doesn't it?$",
    ),
    "PlayersHouse_1F_Text_MoversPokemonGoSetClock": (
        "The moving POKéMON put\\n",
        "everything in place.\\p",
        "Your room is upstairs.\\n",
        "Go take a look.\\p",
        "ELIAS left a clock for you\\n",
        "before he left.\\p",
        "Don't forget to set it.$",
    ),
    "PlayersHouse_1F_Text_ArentYouInterestedInRoom": (
        "MOM: {PLAYER}, your room is\\n",
        "waiting for you.$",
    ),
    "PlayersHouse_1F_Text_GoSetTheClock": (
        "MOM: Set the clock in your room\\n",
        "before you go out.$",
    ),
    "PlayersHouse_1F_Text_OhComeQuickly": (
        "MOM: {PLAYER}! Come here!\\p",
        "They're talking about ELIAS\\n",
        "on TV.$",
    ),
    "PlayersHouse_1F_Text_MaybeDadWillBeOn": (
        "MOM: Maybe they'll show ELIAS.\\p",
        "He rarely appears in reports\\n",
        "from PAMPA DA ESPERA.$",
    ),
    "PlayersHouse_1F_Text_ItsOverWeMissedHim": (
        "MOM: Oh... it's over.\\p",
        "I think ELIAS was on screen,\\n",
        "but we were too late.$",
    ),
    "PlayersHouse_1F_Text_GoIntroduceYourselfNextDoor": (
        "MOM: PROF. ANAHI works nearby.\\p",
        "Go introduce yourself before\\n",
        "you explore the village.$",
    ),
    "PlayersHouse_1F_Text_SeeYouHoney": (
        "MOM: See you, {PLAYER}.\\p",
        "Don't vanish without a word.$",
    ),
    "PlayersHouse_1F_Text_DidYouMeetProfBirch": (
        "MOM: Did you meet PROF. ANAHI?\\p",
        "She spends more time outdoors\\n",
        "than in the lab.$",
    ),
    "PlayersHouse_1F_Text_YouShouldRestABit": (
        "MOM: You look like you need\\n",
        "rest.\\p",
        "Sleep a little before going\\n",
        "back on the road.$",
    ),
    "PlayersHouse_1F_Text_TakeCareHoney": (
        "MOM: Take care, {PLAYER}.$",
    ),
    "PlayersHouse_1F_Text_GotDadsBadgeHeresSomethingFromMom": (
        "MOM: ELIAS gave you that BADGE?\\p",
        "Then take this too.\\p",
        "This one is from your mother.$",
    ),
    "PlayersHouse_1F_Text_DontPushYourselfTooHard": (
        "You don't need to prove it all\\n",
        "at once, {PLAYER}.\\p",
        "Come home when you need to.\\p",
        "I'll be here.$",
    ),
    "PlayersHouse_1F_Text_IsThatAPokenav": (
        "MOM: Is that a POKéNAV?\\p",
        "Did HORIZON activate its\\n",
        "contact system?\\p",
        "Then register my number.\\p",
        "I want to know you're safe.$",
    ),
    "PlayersHouse_1F_Text_RegisteredMom": (
        "{PLAYER} registered MOM\\n",
        "in the POKéNAV.$",
    ),
    "PlayersHouse_1F_Text_ReportFromPetalburgGym": (
        "REPORTER: Live from\\n",
        "PAMPA DA ESPERA,\\p",
        "where ELIAS welcomed new\\n",
        "challengers this morning.$",
    ),
    "RivalsHouse_1F_Text_OhYoureTheNewNeighbor": (
        "You must be {PLAYER}.\\p",
        "CIRO said someone his age\\n",
        "was moving nearby.\\p",
        "He's upstairs.\\p",
        "Unless he already ran outside.$",
    ),
    "RivalsHouse_1F_Text_LikeChildLikeFather": (
        "CIRO is hardly ever home.\\p",
        "Since HORIZON offered a grant,\\n",
        "he lives among maps, sensors\\n",
        "and POKéMON.$",
    ),
    "RivalsHouse_1F_Text_TooBusyToNoticeVisit": (
        "CIRO didn't notice your visit,\\n",
        "did he?\\p",
        "Once he gets an idea,\\n",
        "everything else disappears.$",
    ),
    "RivalsHouse_1F_Text_WentOutToRoute103": (
        "CIRO left for ROUTE 103\\n",
        "a little while ago.\\p",
        "He said HORIZON had new data\\n",
        "for him to test.$",
    ),
    "RivalsHouse_1F_Text_ShouldGoHomeEverySoOften": (
        "Traveling with POKéMON changes\\n",
        "people.\\p",
        "Still, visit home sometimes.\\p",
        "Your mother will appreciate it.$",
    ),
    "RivalsHouse_1F_Text_MayWhoAreYou": CIRO_INTRO,
    "RivalsHouse_1F_Text_BrendanWhoAreYou": CIRO_INTRO,
    "RivalsHouse_1F_Text_DoYouHavePokemon": (
        "Hi, {PLAYER}!\\p",
        "Are you traveling with your own\\n",
        "POKéMON now?$",
    ),
    "RivalsHouse_2F_Text_MayWhoAreYou": CIRO_INTRO,
    "RivalsHouse_2F_Text_BrendanWhoAreYou": CIRO_INTRO,
    "RivalsHouse_2F_Text_MayGettingReady": CIRO_READY,
    "RivalsHouse_2F_Text_BrendanGettingReady": CIRO_READY,
    "RivalsHouse_2F_Text_ItsRivalsPokeBall": (
        "That POKé BALL belongs to CIRO.\\p",
        "Better leave it where it is.$",
    ),
}


def visible_segments(payload: str) -> list[str]:
    cleaned = payload.replace("$", "")
    cleaned = cleaned.replace("{PLAYER}", "PLAYERX")
    cleaned = PLACEHOLDER_RE.sub("", cleaned)
    return [part.strip() for part in CONTROL_RE.split(cleaned)]


def validate_widths() -> None:
    for label, payloads in ENGLISH.items():
        for payload in payloads:
            for segment in visible_segments(payload):
                if len(segment) > MAX_VISIBLE_WIDTH:
                    raise ValueError(
                        f"{label}: visible segment is {len(segment)} chars, max {MAX_VISIBLE_WIDTH}: {segment!r}"
                    )


def render_block(label: str, payloads: tuple[str, ...]) -> str:
    return label + ":\n" + "".join(f'\t.string "{payload}"\n' for payload in payloads)


def mask_labels(text: str, labels: list[str]) -> str:
    masked = text
    for label in labels:
        pattern = source_contract.block_pattern(label)
        match = pattern.search(masked)
        if not match:
            raise ValueError(f"cannot mask missing house block: {label}")
        masked = masked[: match.start()] + label + ':\n\t.string "<ARAUNA_HOUSE_EN>"\n' + masked[match.end() :]
    return masked


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Render Vila Amanhecer player/CIRO house surfaces in English using the existing cleanup contract as source anchors."
    )
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--in-place", action="store_true")
    args = parser.parse_args()
    if args.check and args.in_place:
        parser.error("use either --check or --in-place")

    validate_widths()

    by_file: dict[str, list[tuple[str, tuple[str, ...], tuple[str, ...]]]] = defaultdict(list)
    for rel_path, label, pt_lines in source_contract.TARGETS:
        if label not in ENGLISH:
            raise ValueError(f"missing English house payload for {label}")
        by_file[rel_path].append((label, pt_lines, ENGLISH[label]))

    if len(ENGLISH) != len(source_contract.TARGETS):
        raise ValueError("English house target count does not match source cleanup contract")

    rendered_files: dict[str, str] = {}
    for rel_path, targets in by_file.items():
        path = ROOT / rel_path
        source = path.read_text(encoding="utf-8")
        rendered = source
        labels = [label for label, _, _ in targets]

        for label, pt_lines, en_lines in targets:
            pattern = source_contract.block_pattern(label)
            matches = list(pattern.finditer(rendered))
            if len(matches) != 1:
                raise ValueError(f"{rel_path}: {label}: expected one source block, found {len(matches)}")
            body = matches[0].group(0)
            for line in pt_lines:
                if f'\t.string "{line}"' not in body:
                    raise ValueError(f"{rel_path}: {label}: source contract line missing: {line!r}")
            replacement = render_block(label, en_lines)
            rendered = rendered[: matches[0].start()] + replacement + rendered[matches[0].end() :]

        if mask_labels(source, labels) != mask_labels(rendered, labels):
            raise ValueError(f"{rel_path}: non-dialogue house structure changed")

        rendered_files[rel_path] = rendered

    forbidden = (
        "MAE:", "PROFESSORA ANAHI", "HORIZONTE", "TENIS", "INSIGNIA",
        "mudanca", "voce", "Nao ", "ROTA 103",
    )
    for rel_path, targets in by_file.items():
        rendered = rendered_files[rel_path]
        for label, _, _ in targets:
            block = source_contract.extract(rendered, label)
            for token in forbidden:
                if token in block:
                    raise ValueError(f"{rel_path}: {label}: Portuguese token survived: {token}")

    if args.check:
        print(f"Vila Amanhecer house English renderer OK: {len(ENGLISH)} text blocks across {len(by_file)} maps validated.")
        return 0
    if args.in_place:
        for rel_path, rendered in rendered_files.items():
            (ROOT / rel_path).write_text(rendered, encoding="utf-8")
        return 0

    for rel_path, rendered in rendered_files.items():
        print(f"===== {rel_path} =====")
        print(rendered, end="" if rendered.endswith("\n") else "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
