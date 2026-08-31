#!/usr/bin/env python3
"""Three rooms of the BATTLE CIRCUIT that give a player something to act on.

The FACTORY's waiting room is the only place in the frontier that scouts an
opponent before the battle: one line naming the type they favour, one naming
how they fight. Seventeen types and nine styles, one sentence each, and the
player's whole decision about which rental to swap rests on getting that
sentence right. So both families are generated -- seventeen from a list of
types, nine from a list of styles -- and the renderer checks each line names
its own and nobody else's. A scouting report that says FIRE when the opponent
favours FIGHTING is worse than silence.

Lounge 1 holds the old BREEDER who reads a POKéMON's hidden stats. He gives
two gradings in a row, each a four-rung ladder, and a player calibrates by
hearing several: if two rungs read alike the reading is worthless. Both
ladders are generated and checked for distinctness, and the stat he names is
the one the summary screen names, so a player can look it up.

The PIKE's three-path room is a woman who senses what is down each corridor.
Her seven "you are in the Nth room" lines and her three path readings are
generated from the numbers and directions themselves.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools" / "arauna"))
from textbox import TextBox, glued  # noqa: E402

FACTORY = ROOT / "data" / "maps" / "BattleFrontier_BattleFactoryPreBattleRoom" / "scripts.inc"
LOUNGE1 = ROOT / "data" / "maps" / "BattleFrontier_Lounge1" / "scripts.inc"
PIKE = ROOT / "data" / "maps" / "BattleFrontier_BattlePikeThreePathRoom" / "scripts.inc"
STRINGS = ROOT / "src" / "strings.c"

BOX = TextBox({}, width=34)

WHOLE = ("CIRCUIT PASS", "FACTORY HEAD", "Battle Swap", "Battle Choice",
         "POKéMON BREEDER", "SP. ATK", "SP. DEF")

# The seventeen types the scouting report can name, spelled as prose rather
# than as the six-character abbreviations the summary screen has room for.
TYPES: tuple[str, ...] = (
    "Normal", "Fire", "Water", "Electric", "Grass", "Ice", "Fighting",
    "Poison", "Ground", "Flying", "Psychic", "Bug", "Rock", "Ghost",
    "Dragon", "Dark", "Steel",
)

# The nine ways an opponent is said to fight.
STYLES: dict[str, str] = {
    "SlowAndSteady": "slow and steady",
    "Endurance": "one of endurance",
    "HighRisk": "high risk for high return",
    "DependsOnFlow": "whatever the battle happens to call for",
    "TotalPreparation": "built on total preparation",
    "WeakenFoe": "weakening the opponent before anything else",
    "Flexible": "flexible, and quick to adapt",
    "ImpossibleToPredict": "impossible to predict",
    "Unrestrained": "free-spirited, and entirely unrestrained",
}

ORDINALS = {2: "2nd", 3: "3rd", 4: "4th", 5: "5th", 6: "6th", 7: "7th"}

# The BREEDER's two ladders. Weakest rung first in both.
ABILITY: tuple[tuple[str, str], ...] = (
    ("AverageAbility", "of average ability, taken all round"),
    ("BetterThanAverageAbility", "a little better than average, taken all "
                                 "round"),
    ("ImpressiveAbility", "quite impressive, taken all round"),
    ("OutstandingAbility", "outstanding. Truly outstanding, taken all round"),
)
STAT_GRADE: tuple[tuple[str, str], ...] = (
    ("StatRelativelyGood", "That one is relatively good."),
    ("StatImpressive", "That one is quite impressive."),
    ("StatOutstanding", "That one is outstanding."),
    ("StatFlawless", "That one is flawless. A thing of perfection."),
)

# The stat the BREEDER names, and the symbol in src/strings.c that prints it
# on the summary screen the player will go and check.
BEST_ASPECT: dict[str, tuple[str, str]] = {
    "HP": ("HP", "gText_HP4"),
    "Atk": ("ATTACK", "gText_Attack"),
    "Def": ("DEFENSE", "gText_Defense"),
    "SpAtk": ("SP. ATK", "gText_SpAtk"),
    "SpDef": ("SP. DEF", "gText_SpDef"),
    "Speed": ("SPEED", "gText_Speed"),
}

PIKE_ROOMS = (1, 3, 5, 7, 9, 11, 13)
PIKE_ORDINALS = {1: "1st", 3: "3rd", 5: "5th", 7: "7th", 9: "9th",
                 11: "11th", 13: "13th"}
PIKE_PATHS = {"Right": "on the right", "Center": "in the middle",
              "Left": "on the left"}

FACTORY_BLOCKS: dict[str, tuple[str, ...]] = {
    "HoldMonsChooseFromSelection": (
        "First we will take your own POKéMON and keep them safe.",
        "Then you may choose from ours.",
    ),
    "LetUsRestoreMons": (
        "Thank you for competing.|Let us put your POKéMON right.",
    ),
    "SaveAndQuitGame": (
        "Would you like to save and stop for now?",
    ),
    "RetireFromChallenge": (
        "Would you like to retire from your Battle Swap challenge?",
    ),
    "InvestigatedUpcomingOpponent": (
        "I have made some enquiries about the TRAINER you face next.",
    ),
    "TrainerHasNoClearFavorite": (
        "The TRAINER appears to have no particular preference of type.",
    ),
    "LikeToSwapMon": (
        "Before the battle begins, would you like to swap a POKéMON?",
    ),
    "YourSwapIsComplete": (
        "Thank you.|The swap is done.",
    ),
    "RightThisWay": (
        "This way, if you please.",
    ),
    "SavingDataPleaseWait": (
        "I am saving your data.|One moment.",
    ),
    "RecordLatestBattle": (
        "Would you like your last battle recorded on your CIRCUIT PASS?",
    ),
    "WaitFewMoments": (
        "Excuse me! Excuse me, please!|Might I ask you to wait a moment?",
    ),
    "UnderstoodSirWillDo": (
        "...Uh-huh? What? ...Whoa!|Understood! At once!",
    ),
    "MessageFromHeadComeRightNow": (
        "Oh, my...|So sorry to have kept you.",
        "I have a message from the head of this facility, the FACTORY HEAD.",
        "It says: “We are going to do this. Come here. Now.”",
    ),
    "PreparedToFaceHead": (
        "The FACTORY HEAD is asking for you.|Are you ready for that?",
    ),
    "CantTellAnythingAboutHead": (
        "I am terribly sorry, but I can tell you nothing whatever about the "
        "FACTORY HEAD.",
    ),
}

LOUNGE1_BLOCKS: dict[str, tuple[str, ...]] = {
    "PokemonBreederIntro": (
        "Seventy years I have raised POKéMON.|They call me the greatest "
        "POKéMON BREEDER living, and I let them.",
        "Get as many years in as I have and you will read what a POKéMON can "
        "do at a glance.",
        "You are a TRAINER. Does it not interest you to know what yours are "
        "actually capable of?",
        "Here. Let me look at one.",
    ),
    "LetsLookAtYourPokemon": (
        "Ah, youngster. Curious about what yours can do?",
        "Here, here.|Let me look at one.",
    ),
    "EvenICantTell": (
        "I am an expert, but not even I can read an egg that has not hatched.",
        "Show me a POKéMON.|A POKéMON is what I need.",
    ),
    "NoTimeForMyAdvice": (
        "What?|No time for my advice?",
        "You should always be glad to learn from those who went before you.",
    ),
    "HaveBusinessNeedsTending": (
        "Yes, what is it now?",
        "I have business needing attention.|Save it for next time.",
    ),
    "SaidMyMonIsOutstanding": (
        "He said mine is outstanding!|I am glad I took such care over it!",
    ),
    "DidntDoAnythingSpecialRaisingIt": (
        "He said mine is outstanding!|But I never did anything special "
        "raising it...",
    ),
}

PIKE_BLOCKS: dict[str, tuple[str, ...]] = {
    "ContinueWithChallenge": (
        "Will you go on with your challenge?",
    ),
    "SaveChallengeAndQuit": (
        "Would you like to save your challenge and stop for now?",
    ),
    "RetireFromChallenge": (
        "Do you wish to retire from your Battle Choice challenge?",
    ),
    "AwaitingReturnSaveBeforeResume": (
        "We have been waiting for you...",
        "Before your Battle Choice challenge goes on, let me save the "
        "game...",
    ),
    "PleaseEnjoyChallenge": (
        "Do enjoy your Battle Choice challenge...",
    ),
    "SavingYourData": (
        "I am saving your data...|A little time, please...",
    ),
    "FindingItDifficultToChoose": (
        "I beg your pardon, but...",
        "Are you perhaps finding the choice of path difficult?",
    ),
    "ApologizeForImpertinence": (
        "I see...|Forgive my impertinence...",
    ),
    "AromaOfPokemon": (
        "There is the distinct smell of POKéMON drifting off it...",
    ),
    "PresenceOfPeople": (
        "Is it... a TRAINER?|I sense people down there...",
    ),
    "HeardWhispering": (
        "I thought I heard something...|Whispering, it might have been...",
    ),
    "WaveOfNostaliga": (
        "For some reason I felt a wave of old memory come off it...",
    ),
    "TerrifyingEvent": (
        "I am sorry to say...",
        "Something terrible is about to happen to you. Something horrible.",
        "Take the greatest care, and prepare for the worst...",
    ),
    "DreadfulPresence": (
        "From every one of the paths I sense something dreadful...",
    ),
}

PIKE_SHARED: dict[str, tuple[str, ...]] = {
    "BattleFrontier_BattlePike_Text_PathBlockedNoTurningBack": (
        "The path is blocked!|And there is no going back...",
    ),
}


def build() -> dict[str, dict[str, tuple[str, ...]]]:
    factory = {f"BattleFrontier_BattleFactoryPreBattleRoom_Text_{label}": body
               for label, body in FACTORY_BLOCKS.items()}
    for type_name in TYPES:
        factory[f"BattleFrontier_BattleFactoryPreBattleRoom_Text_"
                f"TrainerSkilledIn{type_name}Type"] = (
            f"The TRAINER is said to be skilled in handling the "
            f"{type_name.upper()} type.",)
    for suffix, style in STYLES.items():
        factory[f"BattleFrontier_BattleFactoryPreBattleRoom_Text_"
                f"Style{suffix}"] = (
            f"The preferred style of battle appears to be {style}.",)
    for number, ordinal in ORDINALS.items():
        lead = "And finally, the" if number == 7 else "The"
        factory[f"BattleFrontier_BattleFactoryPreBattleRoom_Text_"
                f"ReadyFor{ordinal}Opponent"] = (
            f"{lead} {ordinal} match is next.|Are you ready?",)

    lounge = {f"BattleFrontier_Lounge1_Text_{label}": body
              for label, body in LOUNGE1_BLOCKS.items()}
    for suffix, verdict in ABILITY:
        lounge[f"BattleFrontier_Lounge1_Text_{suffix}"] = (
            "...Hmm...",
            f"This one I would call {verdict}.",
        )
    for suffix, (stat, _symbol) in BEST_ASPECT.items():
        lounge[f"BattleFrontier_Lounge1_Text_BestAspect{suffix}"] = (
            f"Its strongest point, I would say, is its {stat}...",)
    for suffix, verdict in STAT_GRADE:
        lounge[f"BattleFrontier_Lounge1_Text_{suffix}"] = (
            f"{verdict}|...Hm. That is how I call it.",)

    pike = {f"BattleFrontier_BattlePikeThreePathRoom_Text_{label}": body
            for label, body in PIKE_BLOCKS.items()}
    pike.update(PIKE_SHARED)
    for number in PIKE_ROOMS:
        pike[f"BattleFrontier_BattlePikeThreePathRoom_Text_"
             f"CurrentlyInRoom{number}"] = (
            f"You are in the {PIKE_ORDINALS[number]} room...",)
    for suffix, where in PIKE_PATHS.items():
        pike[f"BattleFrontier_BattlePikeThreePathRoom_Text_"
             f"SomethingAbout{suffix}Path"] = (
            f"Ah, let me see... There is something about the path {where}...",)
    return {"factory": factory, "lounge": lounge, "pike": pike}


GROUPS = build()
TARGETS: dict[str, tuple[str, ...]] = {
    label: body for group in GROUPS.values() for label, body in group.items()}
FILES = {"factory": FACTORY, "lounge": LOUNGE1, "pike": PIKE}


def which(label: str) -> str:
    for name, group in GROUPS.items():
        if label in group:
            return name
    raise KeyError(label)


def block_pattern(label: str) -> re.Pattern[str]:
    return re.compile(
        rf"(?ms)^{re.escape(label)}::?\n(?P<body>.*?)"
        rf"(?=^[A-Za-z0-9_]+(?:::|:)(?:\n|$)|\Z)"
    )


def payloads() -> dict[str, tuple[str, ...]]:
    composed = {}
    for label, paragraphs in TARGETS.items():
        glued_paragraphs = []
        for paragraph in paragraphs:
            for name in WHOLE:
                paragraph = paragraph.replace(name, glued(name))
            glued_paragraphs.append(paragraph)
        composed[label] = BOX.compose(tuple(glued_paragraphs))
    return composed


def render(sources: dict[str, str]) -> dict[str, str]:
    composed = payloads()
    rendered = dict(sources)
    for label in TARGETS:
        group = which(label)
        matches = list(block_pattern(label).finditer(rendered[group]))
        if len(matches) != 1:
            raise ValueError(f"{label}: expected one text block, found {len(matches)}")
        if ".string" not in matches[0].group("body"):
            raise ValueError(f"{label}: target contains no .string payload")
        new_body = "".join(f'\t.string "{payload}"\n' for payload in composed[label]) + "\n"
        start, end = matches[0].span("body")
        rendered[group] = rendered[group][:start] + new_body + rendered[group][end:]
    return rendered


def mask(texts: dict[str, str]) -> dict[str, str]:
    masked = dict(texts)
    for label in TARGETS:
        group = which(label)
        match = block_pattern(label).search(masked[group])
        if not match:
            raise ValueError(f"cannot mask missing block: {label}")
        start, end = match.span("body")
        masked[group] = (masked[group][:start]
                         + '\t.string "<ARAUNA_FRONTIER_SERVICE_EN>"\n\n'
                         + masked[group][end:])
    return masked


def validate_slots(sources: dict[str, str]) -> None:
    composed = payloads()
    for label in TARGETS:
        body = block_pattern(label).search(sources[which(label)]).group("body")
        available = set(re.findall(r"\{[A-Za-z_0-9]+\}", body))
        used = set(re.findall(r"\{[A-Za-z_0-9]+\}", "".join(composed[label])))
        if used - available:
            raise ValueError(
                f"{label}: uses {sorted(used - available)}, which the engine "
                f"does not fill here; the source uses {sorted(available)}")


def validate_rendered(sources: dict[str, str], rendered: dict[str, str]) -> None:
    if mask(sources) != mask(rendered):
        raise ValueError("non-dialogue structure changed while rendering")

    composed = payloads()
    strings = STRINGS.read_text(encoding="utf-8")

    def flat(label: str) -> str:
        return re.sub(r"\s+", " ",
                      re.sub(r"\\[npl]|\x01", " ",
                             "".join(composed[label]))).strip().rstrip("$")

    # The scouting report is the only information a player gets before
    # choosing what to swap. A line naming the wrong type is worse than none.
    prefix = "BattleFrontier_BattleFactoryPreBattleRoom_Text_"
    for type_name in TYPES:
        line = flat(f"{prefix}TrainerSkilledIn{type_name}Type")
        if type_name.upper() not in line:
            raise ValueError(
                f"TrainerSkilledIn{type_name}Type: no longer names "
                f"{type_name.upper()}")
        for other in TYPES:
            if other != type_name and other.upper() in line:
                raise ValueError(
                    f"TrainerSkilledIn{type_name}Type: also names "
                    f"{other.upper()}, so the report points two ways")
    styles = [flat(f"{prefix}Style{suffix}") for suffix in STYLES]
    if len(set(styles)) != len(styles):
        raise ValueError("two battle styles read alike")

    # The BREEDER's two ladders. A player calibrates by hearing several, so
    # two rungs reading alike make the whole reading worthless.
    for name, rungs in (
            ("ability", [flat(f"BattleFrontier_Lounge1_Text_{s}")
                         for s, _ in ABILITY]),
            ("stat", [flat(f"BattleFrontier_Lounge1_Text_{s}")
                      for s, _ in STAT_GRADE])):
        if len(set(rungs)) != len(rungs):
            raise ValueError(f"two rungs of the {name} ladder read alike")

    # And the stat he names is one the player can go and look up.
    for suffix, (stat, symbol) in BEST_ASPECT.items():
        if f'{symbol}[] = _("{stat}")' not in strings:
            raise ValueError(
                f"BestAspect{suffix}: names the stat {stat!r}, which is not "
                f"what {symbol} in src/strings.c prints")
        if stat not in flat(f"BattleFrontier_Lounge1_Text_BestAspect{suffix}"):
            raise ValueError(f"BestAspect{suffix}: no longer names the stat")

    # Seven rooms, seven numbers; three paths, three directions.
    pike_prefix = "BattleFrontier_BattlePikeThreePathRoom_Text_"
    for number in PIKE_ROOMS:
        line = flat(f"{pike_prefix}CurrentlyInRoom{number}")
        if PIKE_ORDINALS[number] not in line:
            raise ValueError(
                f"CurrentlyInRoom{number}: no longer says which room it is, "
                f"which is the only progress marker the PIKE gives")
    directions = [flat(f"{pike_prefix}SomethingAbout{suffix}Path")
                  for suffix in PIKE_PATHS]
    if len(set(directions)) != len(directions):
        raise ValueError(
            "two of the three path readings read alike, so the player cannot "
            "tell which corridor was meant")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Render three BATTLE CIRCUIT service rooms in English.")
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--in-place", action="store_true")
    args = parser.parse_args()
    if args.check and args.in_place:
        parser.error("use either --check or --in-place")

    sources = {name: path.read_text(encoding="utf-8")
               for name, path in FILES.items()}
    validate_slots(sources)
    rendered = render(sources)
    validate_rendered(sources, rendered)

    if args.in_place:
        for name, path in FILES.items():
            path.write_text(rendered[name], encoding="utf-8")
    print(f"Frontier service rooms English renderer OK: {len(TARGETS)} blocks.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
