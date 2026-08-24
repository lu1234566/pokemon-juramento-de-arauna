#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_INPUT = ROOT / "data" / "maps" / "MtChimney" / "scripts.inc"
MAX_VISIBLE_WIDTH = 32

TARGETS: dict[str, tuple[tuple[str, ...], tuple[str, ...]]] = {
    "MtChimney_Text_MeteoriteWillActivateVolcano": (
        ("METEORITE", "MT. CHIMNEY"),
        (
            "LUZIA: This METEORITE amplifies\\n",
            "stored BONDS.\\p",
            "With it, I can return what\\n",
            "was taken by force.$",
        ),
    ),
    "MtChimney_Text_MaxieIntro": (
        ("LUZIA", "reescrever"),
        (
            "LUZIA: HORIZON calls this\\n",
            "treatment.\\p",
            "I call it stolen memory.\\p",
            "If you want to stop me from\\n",
            "returning it, then try.$",
        ),
    ),
    "MtChimney_Text_MaxieDefeat": (
        ("LUZIA", "lembrar"),
        (
            "LUZIA: So you chose to stand\\n",
            "in my way...\\p",
            "That does not make HORIZON\\n",
            "right.$",
        ),
    ),
    "MtChimney_Text_MaxieYouHaventSeenLastOfMagma": (
        ("sensores", "ARQUIVO"),
        (
            "LUZIA: This is not over.\\p",
            "No one person decides what\\n",
            "Arauna is allowed to forget.$",
        ),
    ),
    "MtChimney_Text_TabithaIntro": (
        ("METEORITE", "BOSS"),
        (
            "REMEMBRANCER: You're too late.\\p",
            "LUZIA already has the METEORITE.\\p",
            "Beat me if you want through!$",
        ),
    ),
    "MtChimney_Text_TabithaDefeat": (
        ("leader", "awakens"),
        ("REMEMBRANCER: I couldn't\\n", "hold you back...$"),
    ),
    "MtChimney_Text_TabithaPostBattle": (
        ("BOSS", "METEORITE"),
        ("REMEMBRANCER: LUZIA, hurry!\\n", "HORIZON is closing in.$"),
    ),
    "MtChimney_Text_Grunt2Intro": (
        ("LEMBRANTE", "HORIZONTE"),
        (
            "REMEMBRANCER: What was taken\\n",
            "does not belong to HORIZON.\\p",
            "Move.$",
        ),
    ),
    "MtChimney_Text_Grunt2Defeat": (
        ("HORIZONTE", "ARQUIVO VIVO"),
        ("REMEMBRANCER: You're stronger\\n", "than I expected.$"),
    ),
    "MtChimney_Text_Grunt2PostBattle": (
        ("HORIZONTE", "soldados"),
        (
            "REMEMBRANCER: Pain gives no one\\n",
            "the right to erase.\\p",
            "But forcing memory back...\\p",
            "I still think about that.$",
        ),
    ),
    "MtChimney_Text_Grunt1Intro": (
        ("HORIZONTE", "sensores"),
        (
            "REMEMBRANCER: HORIZON calls\\n",
            "erasure treatment.\\p",
            "I won't let them take more.$",
        ),
    ),
    "MtChimney_Text_Grunt1Defeat": (
        ("HORIZONTE", "ARQUIVO VIVO"),
        ("REMEMBRANCER: I'm still not\\n", "strong enough for this choice.$"),
    ),
    "MtChimney_Text_Grunt1PostBattle": (
        ("HORIZONTE", "sensores"),
        (
            "REMEMBRANCER: Remembering isn't\\n",
            "enough.\\p",
            "We must choose how to return it.$",
        ),
    ),
    "MtChimney_Text_TeamAquaAlwaysMessingWithPlans": (
        ("HORIZONTE", "soldados"),
        (
            "REMEMBRANCER: HORIZON always\\n",
            "arrives calling it safety.\\p",
            "Then they decide what vanishes.$",
        ),
    ),
    "MtChimney_Text_MeteoritesPackAmazingPower": (
        ("METEORITES", "amazing power"),
        (
            "REMEMBRANCER: The METEORITE\\n",
            "reacts to stored BONDS.\\p",
            "We don't know how far this goes.$",
        ),
    ),
    "MtChimney_Text_YouBetterNotMessWithUs": (
        ("mess with us", "benefit of everyone"),
        (
            "REMEMBRANCER: Don't interfere.\\p",
            "We're returning records that\\n",
            "should never have been taken.$",
        ),
    ),
    "MtChimney_Text_AquasNameSimilar": (
        ("LEMBRANTE", "LUZIA"),
        (
            "REMEMBRANCER: Stolen memory\\n",
            "stays stolen under a new name.$",
        ),
    ),
    "MtChimney_Text_DouseThemInFire": (
        ("Douse them in fire",),
        ("REMEMBRANCER: Hold the line!\\n", "Don't let the agents through!$"),
    ),
    "MtChimney_Text_KeepMakingMoreLand": (
        ("more land",),
        ("REMEMBRANCER: No archive stays\\n", "buried forever.$"),
    ),
    "MtChimney_Text_ArchieGoStopTeamMagma": (
        ("OTACILIO", "Preservar tudo"),
        (
            "OTACILIO: LUZIA will power the\\n",
            "amplifier with the METEORITE.\\p",
            "Stop her before this ridge\\n",
            "becomes an experiment.$",
        ),
    ),
    "MtChimney_Text_ArchieIHaveMyHandsFull": (
        ("OTACILIO", "M'BOI"),
        (
            "OTACILIO: I'm holding the\\n",
            "REMEMBRANCERS here.\\p",
            "Go. LUZIA is at the machine.$",
        ),
    ),
    "MtChimney_Text_ArchieThankYou": (
        ("OTACILIO", "ARQUIVO VIVO"),
        (
            "OTACILIO: You stopped an\\n",
            "uncontrolled release.\\p",
            "That doesn't settle our dispute,\\n",
            "but it prevented worse today.$",
        ),
    ),
    "MtChimney_Text_MagmaOutnumbersUs": (
        ("LEMBRANTE", "historia"),
        ("HORIZON: There are too many.\\n", "I'm pinned here.$"),
    ),
    "MtChimney_Text_LessHabitatForWaterPokemon": (
        ("WATER POKéMON",),
        (
            "HORIZON: LUZIA will use the\\n",
            "METEORITE as an amplifier.\\p",
            "If it works, memories may return\\n",
            "without consent.$",
        ),
    ),
    "MtChimney_Text_MagmasNameSimilar": (
        ("LEMBRANTE", "historia"),
        (
            "HORIZON: We're technicians and\\n",
            "guards, not owners of memory.\\p",
            "Some here still forget that.$",
        ),
    ),
    "MtChimney_Text_MeteoriteFittedOnMachine": (
        ("METEORITE", "mysterious"),
        (
            "The METEORITE is locked into a\\n",
            "BOND amplifier.\\p",
            "The machine is storing energy.$",
        ),
    ),
    "MtChimney_Text_RemoveTheMeteorite": (
        ("METEORITE", "remove"),
        ("A METEORITE powers this device.\\p", "Remove the METEORITE?$"),
    ),
    "MtChimney_Text_PlayerRemovedMeteorite": (
        ("removed the METEORITE",),
        ("{PLAYER} removed the METEORITE\\n", "from the amplifier.$"),
    ),
    "MtChimney_Text_PlayerLeftMeteorite": (
        ("left the METEORITE",),
        ("{PLAYER} left the METEORITE\\n", "in place.$"),
    ),
    "MtChimney_Text_MachineMakesNoResponse": (
        ("mysterious machine", "no response"),
        ("The amplifier is offline.\\n", "There is no response.$"),
    ),
    "MtChimney_Text_RouteSign": (
        ("JAGGED PATH", "LAVARIDGE TOWN"),
        ("SERRA DA CINZA\\n", "{DOWN_ARROW} SERTAO DE DENTRO$"),
    ),
}

BLOCK_RE_TEMPLATE = r'(?m)^{label}:\n(?P<body>(?:\t\.string "[^\n]*"\n)+)'
CONTROL_RE = re.compile(r"\\[npl]")
PLACEHOLDER_RE = re.compile(r"\{[^}]+\}")


def visible_segments(payload: str) -> list[str]:
    cleaned = PLACEHOLDER_RE.sub("", payload).replace("$", "")
    return [segment.strip() for segment in CONTROL_RE.split(cleaned)]


def validate_widths() -> None:
    for label, (_, payloads) in TARGETS.items():
        for payload in payloads:
            for segment in visible_segments(payload):
                if len(segment) > MAX_VISIBLE_WIDTH:
                    raise ValueError(
                        f"{label}: visible segment is {len(segment)} chars, max {MAX_VISIBLE_WIDTH}: {segment!r}"
                    )


def render(source: str) -> str:
    rendered = source
    for label, (expected_markers, payloads) in TARGETS.items():
        pattern = re.compile(BLOCK_RE_TEMPLATE.format(label=re.escape(label)))
        matches = list(pattern.finditer(rendered))
        if len(matches) != 1:
            raise ValueError(f"{label}: expected one .string block, found {len(matches)}")
        body = matches[0].group("body")
        for marker in expected_markers:
            if marker not in body:
                raise ValueError(f"{label}: expected source marker not found: {marker!r}")
        new_body = "".join(f'\t.string "{payload}"\n' for payload in payloads)
        start, end = matches[0].span("body")
        rendered = rendered[:start] + new_body + rendered[end:]
    return rendered


def validate_rendered(rendered: str) -> None:
    forbidden = (
        "HORIZONTE",
        "LEMBRANTE:",
        "VINCULO",
        "METEORITO",
        "ARQUIVO VIVO",
        "Nao ",
        "Voce ",
    )
    for label, (_, payloads) in TARGETS.items():
        pattern = re.compile(BLOCK_RE_TEMPLATE.format(label=re.escape(label)))
        match = pattern.search(rendered)
        if not match:
            raise ValueError(f"{label}: rendered block missing")
        body = match.group("body")
        for payload in payloads:
            line = f'\t.string "{payload}"'
            if line not in body:
                raise ValueError(f"{label}: rendered line missing: {line}")
        for token in forbidden:
            if token in body:
                raise ValueError(f"{label}: Portuguese visible token survived: {token}")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Render the Serra da Cinza HORIZON/REMEMBRANCER conflict in English without changing Emerald event wiring."
    )
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--in-place", action="store_true")
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()

    if args.output and args.in_place:
        parser.error("use either --output or --in-place, not both")

    validate_widths()
    source = args.input.read_text(encoding="utf-8")
    rendered = render(source)
    validate_rendered(rendered)

    if args.check:
        print(f"Serra da Cinza English renderer OK: {len(TARGETS)} plot blocks validated.")
        return 0

    if args.in_place:
        args.input.write_text(rendered, encoding="utf-8")
    elif args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered, encoding="utf-8")
    else:
        print(rendered, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
