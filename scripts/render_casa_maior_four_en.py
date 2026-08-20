#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MAX = 32
CTRL = re.compile(r"\\[npl]")
PH = re.compile(r"\{[^}]+\}")
TARGETS: dict[str, dict[str, tuple[str, ...]]] = {}


def add(path: str, label: str, *lines: str) -> None:
    TARGETS.setdefault(path, {})[label] = lines


SIDNEY = "data/maps/EverGrandeCity_SidneysRoom/scripts.inc"
add(SIDNEY, "EverGrandeCity_SidneysRoom_Text_IntroSpeech",
    "SIDNEY: Welcome to CASA MAIOR.\\p",
    "Darkness does not make a choice\\n", "wrong by itself.\\p",
    "What matters is what you do\\n", "when no one can excuse it.\\p",
    "Show me what your road made.$")
add(SIDNEY, "EverGrandeCity_SidneysRoom_Text_Defeat",
    "SIDNEY: Good.\\p",
    "You did not hide in the past.$")
add(SIDNEY, "EverGrandeCity_SidneysRoom_Text_PostBattleSpeech",
    "SIDNEY: Go on.\\p",
    "The next room asks a\\n", "different question.$")

PHOEBE = "data/maps/EverGrandeCity_PhoebesRoom/scripts.inc"
add(PHOEBE, "EverGrandeCity_PhoebesRoom_Text_IntroSpeech",
    "PHOEBE: I hear what remains.\\p",
    "A memory can guide the living.\\p",
    "It must not become a cage\\n", "for them.\\p",
    "Show me how your BONDS answer.$")
add(PHOEBE, "EverGrandeCity_PhoebesRoom_Text_Defeat",
    "PHOEBE: Your BONDS stayed alive.\\p",
    "That is why I lost.$")
add(PHOEBE, "EverGrandeCity_PhoebesRoom_Text_PostBattleSpeech",
    "PHOEBE: Remember without\\n", "freezing the people you recall.\\p",
    "Go on.$")

GLACIA = "data/maps/EverGrandeCity_GlaciasRoom/scripts.inc"
add(GLACIA, "EverGrandeCity_GlaciasRoom_Text_IntroSpeech",
    "GLACIA: Keeping tempts us.\\p",
    "Ice can keep a shape unchanged.\\p",
    "But life must still be able\\n", "to change.\\p",
    "Show me what you chose to carry.$")
add(GLACIA, "EverGrandeCity_GlaciasRoom_Text_Defeat",
    "GLACIA: Pressure changed you\\n", "without erasing who you are.$")
add(GLACIA, "EverGrandeCity_GlaciasRoom_Text_PostBattleSpeech",
    "GLACIA: Do not confuse\\n", "permanence with care.\\p",
    "The last member waits ahead.$")

DRAKE = "data/maps/EverGrandeCity_DrakesRoom/scripts.inc"
add(DRAKE, "EverGrandeCity_DrakesRoom_Text_IntroSpeech",
    "DRAKE: Power adds weight\\n", "to every choice.\\p",
    "POKéMON are partners, not proof\\n", "of a TRAINER's worth.\\p",
    "If you know that, show me.$")
add(DRAKE, "EverGrandeCity_DrakesRoom_Text_Defeat",
    "DRAKE: You carried power well.$")
add(DRAKE, "EverGrandeCity_DrakesRoom_Text_PostBattleSpeech",
    "DRAKE: AMALIA waits ahead.\\p",
    "Do not enter to erase\\n", "the road behind you.\\p",
    "Enter knowing what it taught.$")

PRESERVED = {
    SIDNEY: ("TRAINER_SIDNEY", "FLAG_DEFEATED_ELITE_4_SIDNEY", "VAR_ELITE_4_STATE"),
    PHOEBE: ("TRAINER_PHOEBE", "FLAG_DEFEATED_ELITE_4_PHOEBE", "VAR_ELITE_4_STATE"),
    GLACIA: ("TRAINER_GLACIA", "FLAG_DEFEATED_ELITE_4_GLACIA", "VAR_ELITE_4_STATE"),
    DRAKE: ("TRAINER_DRAKE", "FLAG_DEFEATED_ELITE_4_DRAKE", "VAR_ELITE_4_STATE"),
}


def pattern(label: str) -> re.Pattern[str]:
    return re.compile(
        rf"(?ms)^{re.escape(label)}:\n(?P<body>.*?)(?=^[A-Za-z0-9_]+(?:::|:)(?:\n|$)|\Z)"
    )


def validate_widths() -> None:
    for rel, blocks in TARGETS.items():
        for label, lines in blocks.items():
            for line in lines:
                clean = PH.sub("PLAYER", line.replace("$", ""))
                for segment in CTRL.split(clean):
                    segment = segment.strip()
                    if len(segment) > MAX:
                        raise ValueError(
                            f"{rel}: {label}: {len(segment)} chars: {segment!r}"
                        )


def mask(text: str, labels: tuple[str, ...]) -> str:
    out = text
    for label in labels:
        match = pattern(label).search(out)
        if not match:
            raise ValueError(f"missing block: {label}")
        start, end = match.span("body")
        out = out[:start] + '\t.string "<ARAUNA_EN>"\n\n' + out[end:]
    return out


def render(rel: str, source: str) -> str:
    out = source
    labels = tuple(TARGETS[rel])
    for label, lines in TARGETS[rel].items():
        matches = list(pattern(label).finditer(out))
        if len(matches) != 1:
            raise ValueError(f"{rel}: {label}: expected 1 block, found {len(matches)}")
        body = "".join(f'\t.string "{line}"\n' for line in lines) + "\n"
        start, end = matches[0].span("body")
        out = out[:start] + body + out[end:]
    if mask(source, labels) != mask(out, labels):
        raise ValueError(f"{rel}: non-dialogue structure changed")
    for token in PRESERVED[rel]:
        if token not in out:
            raise ValueError(f"{rel}: missing preserved token {token}")
    return out


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--in-place", action="store_true")
    args = parser.parse_args()
    if args.check and args.in_place:
        parser.error("choose --check or --in-place")
    validate_widths()
    total = sum(len(v) for v in TARGETS.values())
    changed = 0
    for rel in TARGETS:
        path = ROOT / rel
        source = path.read_text(encoding="utf-8")
        output = render(rel, source)
        if output != source:
            changed += 1
            if args.in_place:
                path.write_text(output, encoding="utf-8")
    print(
        f"Casa Maior four English renderer OK: {total} blocks across "
        f"{len(TARGETS)} files; {changed} changed."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
