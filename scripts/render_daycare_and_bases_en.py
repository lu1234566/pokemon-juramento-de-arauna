#!/usr/bin/env python3
"""The DAY-CARE couple, the SECRET BASE machinery, and the profile collector.

Three surfaces a player uses rather than watches, and each carries a rule
that appears nowhere else in the game.

The DAY-CARE takes at most two POKéMON and charges to give one back. Both
facts live only at that counter, and a player who leaves without them will
wonder why a third is refused and why the money is gone.

The SECRET BASE system has three: one base per player, ten bases in the
registry, and a registered base persists until its owner moves it. The
registry text is the only place they are stated together.

The profile collector explains the four-phrase editor. His explanation is the
game's only account of how that editor works, so the count and the grouping
are held. His three unused replies -- and the MYSTERY EVENT CLUB greeting
Emerald marks unreachable -- are rewritten with the rest, so no stretch of
the script is left in another game's voice.

Two pairs are composed rather than doubled: the SECRET POWER prompts are the
plain observation plus the question, which is exactly how Emerald builds them
and exactly where two hand-written copies would drift.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools" / "arauna"))
from textbox import TextBox, glued  # noqa: E402

DAY_CARE = ROOT / "data" / "scripts" / "day_care.inc"
SECRET_BASE = ROOT / "data" / "scripts" / "secret_base.inc"
PROFILE_MAN = ROOT / "data" / "scripts" / "profile_man.inc"
SPECIES_TABLE = ROOT / "src" / "data" / "text" / "species_names.h"

BOX = TextBox({"{PLAYER}": 7, "{STR_VAR_1}": 12, "{STR_VAR_2}": 12,
               "{STR_VAR_3}": 12}, width=34)

WHOLE = ("DAY-CARE MAN", "DAY-CARE LADY", "DAY-CARE", "SECRET BASE",
         "SECRET POWER", "BATTLE TOWER", "MYSTERY EVENT CLUB", "MAIL")

# The two entrances a SECRET POWER can open, and what a player sees before
# they have the move. The prompt is the observation plus the question, so
# the two cannot come apart.
ENTRANCES: dict[str, tuple[str, str]] = {
    "Tree": (
        "If some vines came down, this tree could be climbed.",
        "SecretBase_Text_TreeCanBeClimbed",
    ),
    "Clump": (
        "If this clump of grass could be shifted, there might be a way in.",
        "SecretBase_Text_ClumpOfGrass",
    ),
}

DAY_CARE_BLOCKS: dict[str, tuple[str, ...]] = {
    "Route117_Text_SeeWifeIfYoudLikeMeToRaiseMon": (
        "I am the DAY-CARE MAN.",
        "We look after POKéMON for TRAINERS who cannot for a while.",
        "If you want one of yours raised, have a word with my wife.",
    ),
    "Route117_Text_SeeWifeIfYouWantToPickUpMon": (
        "If you have come to collect a POKéMON, have a word with my wife.",
    ),
    "Route117_Text_DoYouWantEgg": (
        "Ah, it is you!",
        "We were raising your POKéMON and, my word, did we have a surprise.",
        "There was an EGG.",
        "We have no idea how it got there. But there it was.",
        "You will want it, yes?",
    ),
    "Route117_Text_IWillKeepDoYouWantIt": (
        "I shall keep it, then. I really shall.|You do want it, yes?",
    ),
    "Route117_Text_YourMonIsDoingFine": (
        "Ah, it is you. Good to see you.|Your {STR_VAR_1} is doing fine.",
    ),
    "Route117_Text_YourMonsAreDoingFine": (
        "Ah, it is you. Your {STR_VAR_1} and {STR_VAR_2} are both doing "
        "fine.",
    ),
    "Route117_Text_IllKeepIt": (
        "Very well, I shall keep it.|Thank you.",
    ),
    "Route117_Text_YouHaveNoRoomForIt": (
        "You have nowhere to put it...|Come back when you have made room.",
    ),
    "Route117_Text_ReceivedEgg": (
        "{PLAYER} received the EGG from the DAY-CARE MAN.",
    ),
    "Route117_Text_TakeGoodCareOfIt": (
        "Take good care of it.",
    ),
    "Route117_Text_FriendlyWithOtherTrainersMon": (
        "By the way -- your {STR_VAR_1} seemed rather friendly with "
        "{STR_VAR_2}'s {STR_VAR_3}.",
        "I believe I saw it being handed a piece of MAIL.",
    ),
    "Route117_PokemonDayCare_Text_WouldYouLikeUsToRaiseAMon": (
        "I am the DAY-CARE LADY.",
        "We raise POKéMON here, for anyone who asks.",
        "Would you like us to raise one of yours?",
    ),
    "Route117_PokemonDayCare_Text_WhichMonShouldWeRaise": (
        "Which one shall we raise for you?",
    ),
    "Route117_PokemonDayCare_Text_WellRaiseYourMon": (
        "Very good. We shall raise your {STR_VAR_1} for a while.",
        "Come back for it when you are ready.",
    ),
    "Route117_PokemonDayCare_Text_WeCanRaiseOneMore": (
        "We can take two at a time.|Would you like us to raise another?",
    ),
    "Route117_PokemonDayCare_Text_HusbandWasLookingForYou": (
        "My husband was after you.",
    ),
    "Route117_PokemonDayCare_Text_FineThenComeAgain": (
        "Oh, very well.|Come again.",
    ),
    "Route117_PokemonDayCare_Text_ComeAgain": (
        "Very good.|Come again.",
    ),
    "Route117_PokemonDayCare_Text_NotEnoughMoney": (
        "You have not the money for that...",
    ),
    "Route117_PokemonDayCare_Text_TakeOtherOneBackToo": (
        "Will you take the other one back as well?",
    ),
    "Route117_PokemonDayCare_Text_GoodToSeeYou": (
        "Ah, it is you. Good to see you.|Your POKéMON can only have "
        "improved.",
    ),
    "Route117_PokemonDayCare_Text_YourMonHasGrownXLevels": (
        "Your {STR_VAR_1} has come on by {STR_VAR_2} levels.",
    ),
    "Route117_PokemonDayCare_Text_YourTeamIsFull": (
        "Your team is full.|Make room and come and see me.",
    ),
    "Route117_PokemonDayCare_Text_TakeBackWhichMon": (
        "Which one will you take back?",
    ),
    "Route117_PokemonDayCare_Text_ItWillCostX": (
        "To have your {STR_VAR_1} back it will be ¥{STR_VAR_2}.",
    ),
    "Route117_PokemonDayCare_Text_HeresYourMon": (
        "Lovely.|Here is your POKéMON.",
    ),
    "Route117_PokemonDayCare_Text_TookBackMon": (
        "{PLAYER} took {STR_VAR_1} back from the DAY-CARE LADY.",
    ),
    "Route117_PokemonDayCare_Text_YouHaveJustOneMon": (
        "Oh? But you have only the one POKéMON.",
        "Come back another time.",
    ),
    "Route117_PokemonDayCare_Text_TakeYourMonBack": (
        "Will you take your POKéMON back?",
    ),
    "Route117_PokemonDayCare_Text_WhatWillYouBattleWith": (
        "If you leave that one with me, what will you battle with?",
        "Come back another time.",
    ),
    "Route117_PokemonDayCare_Text_YoullBeLeftWithJustOne": (
        "Hm?|Now, now.",
        "Leave that one with me and you will be down to a single POKéMON.",
        "You would do better to go and catch a few more first, I dare say.",
    ),
    "Text_EggHatchHuh": (
        "Huh?",
    ),
}

SECRET_BASE_BLOCKS: dict[str, tuple[str, ...]] = {
    "SecretBase_Text_VineDroppedDown": (
        "A thick vine came down!",
    ),
    "SecretBase_Text_DiscoveredSmallEntrance": (
        "Found a small way in!",
    ),
    "SecretBase_Text_AllDecorationsWillBeReturned": (
        "Every decoration and every piece of furniture in your SECRET BASE "
        "will go back to your PC.",
        "Is that all right?",
    ),
    "SecretBase_Text_WantToRegisterSecretBase": (
        "Register {STR_VAR_1}'s SECRET BASE?",
    ),
    "SecretBase_Text_AlreadyRegisteredDelete": (
        "This one is registered already.|Delete it?",
    ),
    "SecretBase_Text_TooManyBasesDeleteSome": (
        "Ten locations is the most that can be registered.",
        "Delete one if you want to register another.",
    ),
    "SecretBase_Text_RegistrationCompleted": (
        "Registered.",
    ),
    "SecretBase_Text_DataUnregistered": (
        "The entry has been removed.",
    ),
    "SecretBase_Text_BootUpPC": (
        "{PLAYER} started up the PC.",
    ),
    "SecretBase_Text_WhatWouldYouLikeToDo": (
        "What would you like to do?",
    ),
    "SecretBase_Text_RegistryInfo": (
        "Once registered, a SECRET BASE stays where it is until the TRAINER "
        "who owns it moves.",
        "Delete one from the list and another may take its place.",
        "Ten SECRET BASE locations may be registered at once.",
    ),
    "SecretBase_Text_BattleTowerShield": (
        "A shield of {STR_VAR_2}, for winning {STR_VAR_1} in a row at the "
        "BATTLE TOWER.",
    ),
    "SecretBase_Text_ToyTV": (
        "A toy television, and a convincing one. Easily taken for the real "
        "thing.",
    ),
    "SecretBase_Text_SeedotTV": (
        "A toy television shaped like a Bumba-Boi.|It looks ready to roll "
        "off on its own...",
    ),
    "SecretBase_Text_SkittyTV": (
        "A toy television shaped like a Pombim.|It looks ready to wander "
        "off...",
    ),
    "SecretBase_Text_WouldYouLikeToMoveBases": (
        "You may only keep one SECRET BASE.",
        "Would you like to move out of the one near {STR_VAR_1}?",
    ),
    "SecretBase_Text_MovingCompletedUseSecretPower": (
        "Moved.",
        "Would you like to use the SECRET POWER?",
    ),
}

# The two TVs are named after species. If the species table is renamed and
# these are not, the decoration describes an animal that does not exist.
TV_SPECIES: dict[str, tuple[str, str]] = {
    "SecretBase_Text_SeedotTV": ("SEEDOT", "Bumba-Boi"),
    "SecretBase_Text_SkittyTV": ("SKITTY", "Pombim"),
}

PROFILE_BLOCKS: dict[str, tuple[str, ...]] = {
    "ProfileMan_Text_CollectTrainerProfiles": (
        "Hello there, TRAINER.|That is a wonderful smile you have.",
        "I collect them, you see. Profiles. The profiles of POKéMON "
        "TRAINERS.",
    ),
    "ProfileMan_Text_YouHaveWonderfulSmile": (
        "Hello there, TRAINER.|That is a wonderful smile you have.",
    ),
    "ProfileMan_Text_MayISeeYourProfile": (
        "So. How about it?|May I see your profile?",
    ),
    "ProfileMan_Text_MayISeeYourNewProfile": (
        "May I see your new profile?",
    ),
    "ProfileMan_Text_EasyChatExplanation": (
        "You make a profile by putting four words or phrases together.",
        "Here -- I shall show you one made of four, so you can see the shape "
        "of it.",
        "Any of the four may be swapped for another, in whatever order you "
        "like, until it says what you want it to say.",
        "There are a great many phrases to choose from.",
        "They are sorted into groups -- POKéMON, ways of living, things "
        "people enjoy -- so that finding one is not a chore.",
        "So: pick a group first, and it will show you what is in it.",
        "Then pick the phrase you want out of the list.",
        "Do that four times over and the profile is yours.",
    ),
    "ProfileMan_Text_LetsSeeItThen": (
        "Yes! Thank you.|Let us see it, then.",
    ),
    "ProfileMan_Text_EvenBetterThanLastProfile": (
        "Yes! Thank you.",
        "I do hope it is better still than the one you showed me before.",
    ),
    "ProfileMan_Text_ImagineYouWouldHaveWonderfulProfile": (
        "Oh, no. Really?",
        "I should have thought someone like you would have a wonderful "
        "profile...",
    ),
    "ProfileMan_Text_NotIntoItRightNow": (
        "Oh? Not in the mood just now?",
        "Any time suits me. Any time at all.",
    ),
    "ProfileMan_Text_LikeProfileWayItIs": (
        "Ah, you are happy with it as it stands.",
        "I do not blame you. It is a wonderful profile as it is.",
    ),
    "ProfileMan_Text_FantasticProfile": (
        "F-fantastic!",
        "Your profile -- it is wonderful.|It says exactly what you are.",
        "Anybody hearing that would be quite taken with you.",
        "Thank you.",
    ),
    "ProfileMan_Text_YouKnowSecretSaying": (
        "Oh?|You know the secret saying!",
        "That makes you a fellow member of the MYSTERY EVENT CLUB.",
    ),
}


def build() -> dict[str, dict[str, tuple[str, ...]]]:
    bases = dict(SECRET_BASE_BLOCKS)
    for name, (observation, plain_label) in ENTRANCES.items():
        bases[plain_label] = (observation,)
        bases[f"SecretBase_Text_{name}UseSecretPower"] = (
            observation,
            "Use the SECRET POWER?",
        )
    return {
        "daycare": dict(DAY_CARE_BLOCKS),
        "bases": bases,
        "profile": dict(PROFILE_BLOCKS),
    }


GROUPS = build()
TARGETS: dict[str, tuple[str, ...]] = {
    label: body for group in GROUPS.values() for label, body in group.items()}
FILES = {"daycare": DAY_CARE, "bases": SECRET_BASE, "profile": PROFILE_MAN}


def which(label: str) -> str:
    for name, group in GROUPS.items():
        if label in group:
            return name
    raise KeyError(label)


def block_pattern(label: str) -> re.Pattern[str]:
    return re.compile(
        rf"(?ms)^{re.escape(label)}::?\n(?P<body>.*?)"
        # secret_base.inc pulls the resident trainers in with a .include, so
        # that line ends a block just as a new label would. Matched with
        # [ \t] rather than \s so the blank line before it stays inside the
        # body and the block keeps the shape it had.
        rf"(?=^[A-Za-z0-9_]+(?:::|:)(?:\n|$)|^[ \t]*\.include|\Z)"
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
                         + '\t.string "<ARAUNA_DAYCARE_BASES_EN>"\n\n'
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
    species = SPECIES_TABLE.read_text(encoding="utf-8")

    def flat(label: str) -> str:
        return re.sub(r"\s+", " ",
                      re.sub(r"\\[npl]|\x01", " ",
                             "".join(composed[label]))).strip().rstrip("$")

    # Two DAY-CARE rules, each stated at that counter and nowhere else.
    if "two" not in flat("Route117_PokemonDayCare_Text_WeCanRaiseOneMore"):
        raise ValueError(
            "WeCanRaiseOneMore: no longer says two is the limit, and nothing "
            "else in the game says it")
    if "¥{STR_VAR_2}" not in flat("Route117_PokemonDayCare_Text_ItWillCostX"):
        raise ValueError(
            "ItWillCostX: no longer states the fee, which is the only warning "
            "a player gets that collecting costs money")

    # Three SECRET BASE rules, stated together in the registry text and the
    # move prompt.
    registry = flat("SecretBase_Text_RegistryInfo")
    if "Ten" not in registry and "ten" not in registry:
        raise ValueError("RegistryInfo: no longer says how many may be registered")
    if "moves" not in registry:
        raise ValueError(
            "RegistryInfo: no longer says a registered base lasts until its "
            "owner moves")
    if "one SECRET BASE" not in flat("SecretBase_Text_WouldYouLikeToMoveBases"):
        raise ValueError(
            "WouldYouLikeToMoveBases: no longer says only one base may be "
            "kept, so a player will not understand what moving costs them")

    # The prompt is the observation plus the question. Two hand-written
    # copies would drift; these cannot.
    for name, (observation, plain_label) in ENTRANCES.items():
        plain = flat(plain_label)
        prompt = flat(f"SecretBase_Text_{name}UseSecretPower")
        if not prompt.startswith(plain):
            raise ValueError(
                f"{name}UseSecretPower: no longer opens on the same "
                f"observation the plain look gives")
        if "SECRET POWER" not in prompt:
            raise ValueError(f"{name}UseSecretPower: no longer names the move")

    # The two toy televisions are named after species.
    for label, (constant, name) in TV_SPECIES.items():
        if f'[SPECIES_{constant}] = _("{name}")' not in species:
            raise ValueError(
                f"{label}: describes a {name}, which is not what "
                f"species_names.h calls SPECIES_{constant}")
        if name not in flat(label):
            raise ValueError(f"{label}: no longer names the {name}")

    # The profile editor is explained once.
    explanation = flat("ProfileMan_Text_EasyChatExplanation")
    if "four" not in explanation:
        raise ValueError(
            "EasyChatExplanation: no longer says how many phrases a profile "
            "takes")
    if "group" not in explanation:
        raise ValueError(
            "EasyChatExplanation: no longer says the phrases are grouped, "
            "which is how a player finds one")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Render the DAY-CARE, SECRET BASE system and profile man.")
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
    print(f"Day-care and bases English renderer OK: {len(TARGETS)} blocks.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
