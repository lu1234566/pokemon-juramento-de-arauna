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


EVER = "data/maps/EverGrandeCity/scripts.inc"
add(EVER, "EverGrandeCity_Text_EnteringVictoryRoad",
    "ESTRADA DO JURAMENTO$")
add(EVER, "EverGrandeCity_Text_EnteringPokemonLeague",
    "CASA MAIOR\\n", "POKéMON LEAGUE ENTRANCE$")
add(EVER, "EverGrandeCity_Text_CitySign",
    "ESTRADA DO JURAMENTO\\p",
    "The LEAGUE is the final rite of\\n", "this journey.\\p",
    "Winning cannot erase what happened.\\p",
    "It only helps define who you choose\\n", "to be afterward.$")

VR1 = "data/maps/VictoryRoad_1F/scripts.inc"
add(VR1, "VictoryRoad_1F_Text_WallyNotGoingToLoseAnymore",
    "VAL: I reached this place at my\\n", "own pace, {PLAYER}.\\p",
    "This time I won't try to become\\n", "someone else.\\p",
    "I want to learn how far I can go\\n", "while still being myself.$")
add(VR1, "VictoryRoad_1F_Text_WallyEntranceDefeat",
    "VAL: I lost... but I didn't retreat.\\p",
    "Once, that would have broken me.\\p",
    "Now it only shows how much room\\n", "I still have to grow.$")
add(VR1, "VictoryRoad_1F_Text_WallyPostEntranceBattle",
    "VAL: Go on, {PLAYER}.\\p",
    "I'll keep going too.\\p",
    "Next time we meet, I want to be\\n", "stronger in my own way.$")
add(VR1, "VictoryRoad_1F_Text_WallyIntro",
    "VAL: CHAMPION or not, I still want\\n", "to measure my pace against yours.\\p",
    "Come on, {PLAYER}. No excuses.$")
add(VR1, "VictoryRoad_1F_Text_WallyDefeat",
    "VAL: Ha! I still have road left\\n", "before I catch up.$")
add(VR1, "VictoryRoad_1F_Text_WallyPostBattle",
    "VAL: Every loss shows me something\\n", "I could not see before.\\p",
    "Next time, I'll come closer.$")
add(VR1, "VictoryRoad_1F_Text_EdgarIntro",
    "I've reached this road before.\\p",
    "The end still feels far away.$")
add(VR1, "VictoryRoad_1F_Text_EdgarDefeat",
    "My dream stops here again...$")
add(VR1, "VictoryRoad_1F_Text_EdgarPostBattle",
    "You came a long way.\\p", "Do not stop now. Reach the LEAGUE.$")
add(VR1, "VictoryRoad_1F_Text_AlbertIntro",
    "I did not come this far to lose.\\p", "That option does not exist!$")
add(VR1, "VictoryRoad_1F_Text_AlbertDefeat",
    "Impossible... I lost?$")
add(VR1, "VictoryRoad_1F_Text_AlbertPostBattle",
    "I lost here.\\p", "I'm not ready for CASA MAIOR yet.$")
add(VR1, "VictoryRoad_1F_Text_HopeIntro",
    "This road feels endless.\\p", "Now I understand its name.$")
add(VR1, "VictoryRoad_1F_Text_HopeDefeat",
    "Your way of battling is amazing.$")
add(VR1, "VictoryRoad_1F_Text_HopePostBattle",
    "You have the strength to reach\\n", "CASA MAIOR.$")
add(VR1, "VictoryRoad_1F_Text_QuincyIntro",
    "What is this road really for?\\p", "Beat me and I'll tell you.$")
add(VR1, "VictoryRoad_1F_Text_QuincyDefeat",
    "All right. You earned the answer.$")
add(VR1, "VictoryRoad_1F_Text_QuincyPostBattle",
    "This is the last road before the\\n", "LEAGUE.\\p",
    "That is why people call it the\\n", "ESTRADA DO JURAMENTO.$")
add(VR1, "VictoryRoad_1F_Text_KatelynnIntro",
    "If you reached this point, I don't\\n", "need to explain anything. Battle!$")
add(VR1, "VictoryRoad_1F_Text_KatelynnDefeat",
    "What a loss...$")
add(VR1, "VictoryRoad_1F_Text_KatelynnPostBattle",
    "Hmph. Go on.\\p", "See if I care.$")

VRB1 = "data/maps/VictoryRoad_B1F/scripts.inc"
add(VRB1, "VictoryRoad_B1F_Text_SamuelIntro",
    "The closer I get to the LEAGUE,\\n", "the more nervous I become.$")
add(VRB1, "VictoryRoad_B1F_Text_SamuelDefeat",
    "I couldn't do anything...$")
add(VRB1, "VictoryRoad_B1F_Text_SamuelPostBattle",
    "CASA MAIOR feels far away again.\\p", "What a disappointment.$")
add(VRB1, "VictoryRoad_B1F_Text_ShannonIntro",
    "At the LEAGUE, you need the trust\\n", "of your POKéMON.$")
add(VRB1, "VictoryRoad_B1F_Text_ShannonDefeat",
    "The trust between you is strong.$")
add(VRB1, "VictoryRoad_B1F_Text_ShannonPostBattle",
    "Time together can deepen a BOND.\\p",
    "But trust still has to be renewed.$")
add(VRB1, "VictoryRoad_B1F_Text_MichelleIntro",
    "This is not the finish.\\p", "It is one more step to CASA MAIOR.$")
add(VRB1, "VictoryRoad_B1F_Text_MichelleDefeat",
    "That's the way forward!$")
add(VRB1, "VictoryRoad_B1F_Text_MichellePostBattle",
    "You'll be fine.\\p", "Your POKéMON look ready.$")
add(VRB1, "VictoryRoad_B1F_Text_MitchellIntro",
    "My POKéMON carry incredible force!$")
add(VRB1, "VictoryRoad_B1F_Text_MitchellDefeat",
    "I've never faced anyone like you.$")
add(VRB1, "VictoryRoad_B1F_Text_MitchellPostBattle",
    "Even outside battle, I can feel the\\n", "strength of your BOND.$")
add(VRB1, "VictoryRoad_B1F_Text_HalleIntro",
    "Hey, loosen up a little.\\p", "Let's battle without all the tension.$")
add(VRB1, "VictoryRoad_B1F_Text_HalleDefeat",
    "Wow! That was wonderful!$")
add(VRB1, "VictoryRoad_B1F_Text_HallePostBattle",
    "Yes, this is ESTRADA DO JURAMENTO.\\p",
    "But it is not so different from the\\n", "roads that brought you here.\\p",
    "Enjoy what remains of the journey.$")

VRB2 = "data/maps/VictoryRoad_B2F/scripts.inc"
add(VRB2, "VictoryRoad_B2F_Text_VitoIntro",
    "I trained with my whole family.\\p", "I won't lose to anyone!$")
add(VRB2, "VictoryRoad_B2F_Text_VitoDefeat",
    "Better than my whole family?$")
add(VRB2, "VictoryRoad_B2F_Text_VitoPostBattle",
    "I was the best at home and had never\\n", "lost before.\\p",
    "Maybe losing is something I needed.$")
add(VRB2, "VictoryRoad_B2F_Text_OwenIntro",
    "I heard about a tough young TRAINER.\\p", "So that was you?$")
add(VRB2, "VictoryRoad_B2F_Text_OwenDefeat",
    "The short one is strong!$")
add(VRB2, "VictoryRoad_B2F_Text_OwenPostBattle",
    "So the stories were true.\\p",
    "That strong young TRAINER came from\\n", "VILA AMANHECER.$")
add(VRB2, "VictoryRoad_B2F_Text_CarolineIntro",
    "You must be getting tired by now.$")
add(VRB2, "VictoryRoad_B2F_Text_CarolineDefeat",
    "Not even a sign of fatigue!$")
add(VRB2, "VictoryRoad_B2F_Text_CarolinePostBattle",
    "ESTRADA DO JURAMENTO and CASA MAIOR\\n", "are long tests.\\p",
    "Do not let exhaustion choose for you.$")
add(VRB2, "VictoryRoad_B2F_Text_JulieIntro",
    "Don't relax just because you earned\\n", "many BADGES.\\p",
    "There is always someone stronger.$")
add(VRB2, "VictoryRoad_B2F_Text_JulieDefeat",
    "You're stronger than I am!$")
add(VRB2, "VictoryRoad_B2F_Text_JuliePostBattle",
    "Look at your BADGES and remember\\n", "the TRAINERS behind each one.$")
add(VRB2, "VictoryRoad_B2F_Text_FelixIntro",
    "I came far, but the pressure is\\n", "getting to my stomach...$")
add(VRB2, "VictoryRoad_B2F_Text_FelixDefeat",
    "Ow... That hurts...$")
add(VRB2, "VictoryRoad_B2F_Text_FelixPostBattle",
    "Just thinking about CASA MAIOR makes\\n", "me tense.\\p",
    "All I can do is pretend I'm calm.$")
add(VRB2, "VictoryRoad_B2F_Text_DianneIntro",
    "The strongest TRAINERS reach this\\n", "cave.\\p",
    "So? What do you think of the road?$")
add(VRB2, "VictoryRoad_B2F_Text_DianneDefeat",
    "You didn't even flinch!$")
add(VRB2, "VictoryRoad_B2F_Text_DiannePostBattle",
    "You've got courage. I like that.\\p", "Keep going.$")

LEAGUE = "data/maps/EverGrandeCity_PokemonLeague_1F/scripts.inc"
add(LEAGUE, "EverGrandeCity_PokemonLeague_1F_Text_MustHaveAllGymBadges",
    "Only TRAINERS with all eight BADGES\\n", "may enter CASA MAIOR.\\p",
    "We'll confirm your record now.$")
add(LEAGUE, "EverGrandeCity_PokemonLeague_1F_Text_HaventObtainedAllBadges",
    "Your record is still missing a BADGE.\\p",
    "Return when all eight are present.$")
add(LEAGUE, "EverGrandeCity_PokemonLeague_1F_Text_GoForth",
    "TRAINER, trust yourself and the\\n", "POKéMON beside you. Go forward.$")

PRESERVED = {
    EVER: ("FLAG_VISITED_EVER_GRANDE_CITY",),
    VR1: ("VAR_VICTORY_ROAD_1F_STATE", "TRAINER_WALLY_VR_1", "TRAINER_WALLY_VR_2", "FLAG_DEFEATED_WALLY_VICTORY_ROAD"),
    VRB1: ("TRAINER_SAMUEL", "TRAINER_SHANNON", "TRAINER_MICHELLE"),
    VRB2: ("TRAINER_VITO", "TRAINER_OWEN", "TRAINER_CAROLINE"),
    LEAGUE: ("FLAG_ENTERED_ELITE_FOUR", "FLAG_BADGE06_GET", "HEAL_LOCATION_EVER_GRANDE_CITY_POKEMON_LEAGUE"),
}


def pattern(label: str) -> re.Pattern[str]:
    return re.compile(rf"(?ms)^{re.escape(label)}:\n(?P<body>.*?)(?=^[A-Za-z0-9_]+(?:::|:)(?:\n|$)|\Z)")


def validate_widths() -> None:
    for rel, blocks in TARGETS.items():
        for label, lines in blocks.items():
            for line in lines:
                clean = PH.sub("PLAYER", line.replace("$", ""))
                for segment in CTRL.split(clean):
                    segment = segment.strip()
                    if len(segment) > MAX:
                        raise ValueError(f"{rel}: {label}: {len(segment)} chars: {segment!r}")


def mask(text: str, labels: tuple[str, ...]) -> str:
    out = text
    for label in labels:
        match = pattern(label).search(out)
        if not match:
            raise ValueError(f"missing text block: {label}")
        start, end = match.span("body")
        out = out[:start] + '\t.string "<ARAUNA_EN>"\n\n' + out[end:]
    return out


def render(rel: str, source: str) -> str:
    out = source
    labels = tuple(TARGETS[rel])
    for label, lines in TARGETS[rel].items():
        matches = list(pattern(label).finditer(out))
        if len(matches) != 1:
            raise ValueError(f"{rel}: {label}: expected 1 block, got {len(matches)}")
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
    print(f"Estrada do Juramento English renderer OK: {total} blocks across {len(TARGETS)} files; {changed} changed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
