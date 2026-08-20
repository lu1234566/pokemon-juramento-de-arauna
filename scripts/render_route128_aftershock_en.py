#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / "data" / "maps" / "Route128" / "scripts.inc"
MAX = 32
CTRL = re.compile(r"\\[npl]")
PH = re.compile(r"\{[^}]+\}")

BLOCKS: dict[str, tuple[str, ...]] = {
    "Route128_Text_ArchieWhatHappened": (
        "OTACILIO: I saw what memory\\n",
        "can do to survivors.\\p",
        "The LIVING ARCHIVE exists\\n",
        "so no one must carry their\\n",
        "worst night forever.$",
    ),
    "Route128_Text_ArchieIOnlyWanted": (
        "OTACILIO: Preserving everything\\n",
        "is not compassion.\\p",
        "Sometimes it only keeps a wound\\n",
        "open and calls that respect.$",
    ),
    "Route128_Text_MaxieDoYouUnderstandNow": (
        "LUZIA: Remembering was never\\n",
        "the problem.\\p",
        "The problem is letting power\\n",
        "decide what others may keep.$",
    ),
    "Route128_Text_MaxieResposibilityFallsToArchieAndMe": (
        "OTACILIO: I wanted a way\\n",
        "to stop pain from ruling lives.\\p",
        "I did not understand what would\\n",
        "happen when the ARCHIVE chose.$",
    ),
    "Route128_Text_MaxieThisDefiesBelief": (
        "LUZIA: And I wanted every stolen\\n",
        "memory returned at once.\\p",
        "Neither of us asked what the\\n",
        "people inside those memories\\n",
        "would need.$",
    ),
    "Route128_Text_StevenWhatIsHappening": (
        "SEU BENTO: The sea is carrying\\n",
        "more than water now.\\p",
        "Names and memories are crossing\\n",
        "BONDS that never held them.$",
    ),
    "Route128_Text_StevenWholeWorldWillDrown": (
        "SEU BENTO: If this keeps moving,\\n",
        "the DISENCHANTMENT will spread\\n",
        "through people as fast as tide.\\p",
        "AGUAS DE M'BOI is the center.$",
    ),
    "Route128_Text_StevenImGoingToSootopolis": (
        "SEU BENTO: I'm going to\\n",
        "AGUAS DE M'BOI.\\p",
        "Come when you can, {PLAYER}.\\n",
        "We need witnesses there.$",
    ),
}

PRESERVED = (
    "VAR_ROUTE128_STATE",
    "LOCALID_ROUTE128_ARCHIE",
    "LOCALID_ROUTE128_MAXIE",
    "LOCALID_ROUTE128_STEVEN",
    "FLAG_SYS_WEATHER_CTRL",
    "FLDEFF_NPCFLY_OUT",
)


def pattern(label: str) -> re.Pattern[str]:
    return re.compile(
        rf"(?ms)^{re.escape(label)}:\n(?P<body>.*?)(?=^[A-Za-z0-9_]+(?:::|:)(?:\n|$)|\Z)"
    )


def validate_widths() -> None:
    for label, lines in BLOCKS.items():
        for line in lines:
            clean = PH.sub("PLAYER", line.replace("$", ""))
            for segment in CTRL.split(clean):
                segment = segment.strip()
                if len(segment) > MAX:
                    raise ValueError(f"{label}: {len(segment)} chars: {segment!r}")


def mask(text: str) -> str:
    out = text
    for label in BLOCKS:
        match = pattern(label).search(out)
        if not match:
            raise ValueError(f"missing Route 128 block: {label}")
        start, end = match.span("body")
        out = out[:start] + '\t.string "<ARAUNA_EN>"\n\n' + out[end:]
    return out


def render(source: str) -> str:
    out = source
    for label, lines in BLOCKS.items():
        matches = list(pattern(label).finditer(out))
        if len(matches) != 1:
            raise ValueError(f"{label}: expected 1 block, found {len(matches)}")
        body = "".join(f'\t.string "{line}"\n' for line in lines) + "\n"
        start, end = matches[0].span("body")
        out = out[:start] + body + out[end:]
    if mask(source) != mask(out):
        raise ValueError("Route 128 non-dialogue structure changed")
    for token in PRESERVED:
        if token not in out:
            raise ValueError(f"missing preserved Route 128 token: {token}")
    return out


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--in-place", action="store_true")
    args = parser.parse_args()
    if args.check and args.in_place:
        parser.error("choose --check or --in-place")
    validate_widths()
    source = TARGET.read_text(encoding="utf-8")
    output = render(source)
    if args.in_place and output != source:
        TARGET.write_text(output, encoding="utf-8")
    print(f"Route 128 English aftermath OK: {len(BLOCKS)} blocks.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
