#!/usr/bin/env python3
"""The four lounges: the gossip, the tout, the girl who reads POKéMON, and
the two old women who teach moves.

Lounge 2 is a man who collects information about the frontier and is dying to
give it away. Emerald has him name each MASTER by title -- the SALON MAIDEN,
the DOME ACE -- but this project aliases all seven of those titles to MASTER,
which would make him say the same sentence seven times about seven different
people. So he names them: MAIRA, DARIO, NILO, JACI, RITA, AMARO, TADEU. Those
are the names the rest of the game gives them, and they are the only thing
that tells his seven reports apart.

Lounge 3 is a man running a book on other people's challenges, and every one
of his twenty-four lines is the same line with a facility in it. Written by
hand, that is twenty-four chances to send a player to the wrong hall.

Lounge 5 is a small girl who says she can hear what a POKéMON is thinking.
What she is actually reading out is its nature, in the same three
categories the BATTLE PALACE explains in adult words: whether it would rather
attack, guard itself, or make trouble. She keeps her own vocabulary -- she
would not say "status move" -- but the three kinds are the palace's three
kinds, and the renderer checks the mapping is complete and consistent.

Lounge 7 is two women who dislike each other and teach moves for Battle
Points. Their twenty move descriptions are NOT rewritten: they are drawn in a
96px window, three lines of about eighteen characters, and there is no voice
to add to "A fiery punch that may burn the foe." The renderer measures them
where they stand instead, so a later edit cannot quietly clip one.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools" / "arauna"))
from textbox import TextBox, glued  # noqa: E402
from textwidth import Ruler  # noqa: E402

LOUNGES = {n: ROOT / "data" / "maps" / f"BattleFrontier_Lounge{n}" / "scripts.inc"
           for n in (2, 3, 5, 7)}

BOX = TextBox({"{PLAYER}": 7, "{STR_VAR_1}": 14, "{STR_VAR_2}": 6}, width=34)

# The move-tutor menu draws in its own small window.
DESCRIPTION_CEILING = 96

WHOLE = ("BATTLE FRONTIER", "BATTLE TOWER", "BATTLE DOME", "BATTLE FACTORY",
         "BATTLE PALACE", "BATTLE ARENA", "BATTLE PIKE", "BATTLE PYRAMID",
         "BATTLE SALON", "SINGLE BATTLE", "DOUBLE BATTLE", "MULTI BATTLE",
         "LINK MULTI", "Battle Swap", "Set KO Tourney", "Battle Choice",
         "Battle Quest", "Battle Point", "Battle Points", "SEU BENTO",
         "FRONTIER MANIAC")

# The seven who run the halls: name, what he makes of them, the team they
# bring when they are weighing you up, and the team they bring when they mean
# it. The rosters are described by type and by dex category, never by species
# name, because the dex is generated and a species name would go stale.
BRAINS: dict[str, tuple[str, str, tuple[str, ...], tuple[str, ...]]] = {
    "SalonMaiden": ("MAIRA", "quiet, and impossible to read", (
        "a PSYCHIC-type PSI POKéMON",
        "a FIRE-type VOLCANO POKéMON",
        "and a NORMAL-type SLEEPING POKéMON"), (
        "a DRAGON and PSYCHIC EON POKéMON",
        "an ELECTRIC-type THUNDER POKéMON",
        "and a NORMAL-type SLEEPING POKéMON")),
    "DomeAce": ("DARIO", "showy, and good enough to get away with it", (
        "a DRAGON and FLYING DRAGON POKéMON",
        "a WATER and GROUND MUD FISH POKéMON",
        "and a FIRE and FLYING FLAME POKéMON"), (
        "a DRAGON and FLYING EON POKéMON",
        "a WATER and GROUND MUD FISH POKéMON",
        "and a STEEL and PSYCHIC IRON LEG POKéMON")),
    "FactoryHead": ("NILO", "odd, and cleverer than he looks", (), ()),
    "PikeQueen": ("JACI", "not somebody to be near when she's cross", (
        "a POISON-type FANG SNAKE POKéMON",
        "a BUG and ROCK MOLD POKéMON",
        "and a WATER-type TENDER POKéMON"), (
        "a POISON-type FANG SNAKE POKéMON",
        "a STEEL and GROUND IRON SNAKE POKéMON",
        "and a WATER and FLYING ATROCIOUS POKéMON")),
    "ArenaTycoon": ("RITA", "small, cheerful, and merciless", (
        "a BUG and FIGHTING SINGLE HORN POKéMON",
        "a DARK-type MOONLIGHT POKéMON",
        "and a BUG and GHOST SHED POKéMON"), (
        "a DARK-type MOONLIGHT POKéMON",
        "a GHOST and POISON SHADOW POKéMON",
        "and a GRASS and FIGHTING MUSHROOM POKéMON")),
    "PalaceMaven": ("AMARO", "still, and watching more than he says", (
        "a POISON and FLYING BAT POKéMON",
        "a NORMAL-type LAZY POKéMON",
        "and a WATER and ICE TRANSPORT POKéMON"), (
        "a FIRE-type LEGENDARY POKéMON",
        "a NORMAL-type LAZY POKéMON",
        "and a WATER-type AURORA POKéMON")),
    "PyramidKing": ("TADEU", "loud, and hotter than the PYRAMID is", (
        "a ROCK-type ROCK PEAK POKéMON",
        "an ICE-type ICEBERG POKéMON",
        "and a STEEL-type IRON POKéMON"), (
        "an ICE and FLYING FREEZE POKéMON",
        "an ELECTRIC and FLYING ELECTRIC POKéMON",
        "and a FIRE and FLYING FLAME POKéMON")),
}

# The twelve challenges the tout bets on: label suffix -> what to call it.
EVENTS: dict[str, str] = {
    "BattleTowerSingle": "the BATTLE TOWER's SINGLE BATTLE ROOMS",
    "BattleTowerDouble": "the BATTLE TOWER's DOUBLE BATTLE ROOMS",
    "BattleTowerMulti": "the BATTLE TOWER's MULTI BATTLE ROOMS",
    "BattleDomeSingle": "the BATTLE DOME's SINGLE BATTLE Tourney",
    "BattleDomeDouble": "the BATTLE DOME's DOUBLE BATTLE Tourney",
    "BattleFactorySingle": "the BATTLE FACTORY's Battle Swap Single Tourney",
    "BattleFactoryDouble": "the BATTLE FACTORY's Battle Swap Double Tourney",
    "BattlePalaceSingle": "the BATTLE PALACE's SINGLE BATTLE HALLS",
    "BattlePalaceDouble": "the BATTLE PALACE's DOUBLE BATTLE HALLS",
    "BattleArena": "the BATTLE ARENA's Set KO Tourney",
    "BattlePike": "the BATTLE PIKE's Battle Choice",
    "BattlePyramid": "the BATTLE PYRAMID's Battle Quest",
}

# What the girl hears. The three preferences are the BATTLE PALACE's three
# kinds of move in a child's words; the second half is what changes when the
# POKéMON is in trouble.
FIGHT, GUARD, TRICKS = "fight", "guard", "tricks"
SAME, TO_FIGHT, TO_GUARD, TO_TRICKS = "same", "to fight", "to guard", "to tricks"
CHILD = {
    FIGHT: "it likes fighting",
    GUARD: "it looks after itself",
    TRICKS: "it likes playing tricks",
}
CHANGE = {
    SAME: "And it says it goes on doing that even with lots of ouchies!",
    TO_FIGHT: "But with enough ouchies, it hits back!",
    TO_GUARD: "But with enough ouchies, it starts worrying about itself!",
    TO_TRICKS: "But with enough ouchies, it turns tricky!",
}
NATURES: dict[str, tuple[str, str]] = {
    "Hardy": (FIGHT, SAME),
    "Lonely": (TRICKS, TO_FIGHT),
    "Brave": (FIGHT, TO_GUARD),
    "Adamant": (FIGHT, SAME),
    "Naughty": (GUARD, TO_FIGHT),
    "Bold": (TRICKS, TO_GUARD),
    "DocileNaiveQuietQuirky": (FIGHT, SAME),
    "Relaxed": (TRICKS, TO_FIGHT),
    "Impish": (FIGHT, TO_GUARD),
    "Lax": (TRICKS, SAME),
    "Timid": (FIGHT, TO_TRICKS),
    "Hasty": (FIGHT, SAME),
    "Serious": (TRICKS, SAME),
    "Jolly": (TRICKS, TO_GUARD),
    "Modest": (GUARD, SAME),
    "Mild": (GUARD, TO_TRICKS),
    "Bashful": (GUARD, SAME),
    "Rash": (TRICKS, SAME),
    "Calm": (GUARD, SAME),
    "Gentle": (GUARD, TO_FIGHT),
    "Sassy": (FIGHT, TO_TRICKS),
    "Careful": (GUARD, TO_TRICKS),
}

# Nine Lounge2 blocks and one Lounge3 block are rendered further down the
# manifest, by render_battle_circuit_analyst_en_checked.py and
# render_battle_circuit_lounge_identity_en_checked.py. Writing them here too
# would only be discarded, so this renderer leaves them alone and validates
# the seams against what those two produce.
HANDWRITTEN: dict[str, tuple[str, ...]] = {
    # -- Lounge 2: the man who knows things -----------------------------------
    "BattleFrontier_Lounge2_Text_SwingByForTheLatestWord": (
        "Hello! Come to squeeze the latest out of me?|Go on, then!",
    ),
    "BattleFrontier_Lounge2_Text_MyInformationsBeenUsefulRight": (
        "Well? Well? Well?",
        "My information's been some use to you, hasn't it?",
    ),
    "BattleFrontier_Lounge2_Text_FacilityIsHottest": (
        "Let me think...",
        "Word is the {STR_VAR_1} is where everything is happening.",
    ),
    "BattleFrontier_Lounge2_Text_BattleTowerIsHottest": (
        "Let me think...",
        "Word is the BATTLE TOWER {STR_VAR_1} is where everything is "
        "happening.",
    ),
    "BattleFrontier_Lounge2_Text_DoubleBattleAdvice2": (
        "Mind yourself in there, though.",
        "I hear some of those TRAINERS have worked out things that only "
        "happen in a DOUBLE BATTLE.",
    ),
    "BattleFrontier_Lounge2_Text_DoubleBattleAdvice3": (
        "And once you're comfortable there, go and try the other places that "
        "run DOUBLE BATTLES.",
    ),
    "BattleFrontier_Lounge2_Text_MultiBattleAdvice": (
        "All sorts turn up in the BATTLE SALON.",
        "You might find a friend in there. Or somebody who's been following "
        "you. Look properly!",
    ),
    "BattleFrontier_Lounge2_Text_LinkMultiBattleAdvice": (
        "If you've a friend with you, go to the LINK MULTI BATTLE ROOM.",
        "Bring a strong one and you'll be given strong ones to face.",
    ),
    "BattleFrontier_Lounge2_Text_NewsGatheringPower": (
        "What a nose for a story!|There's nobody like my mentor!",
    ),
    "BattleFrontier_Lounge2_Text_AmazingPowersOfObservation": (
        "What an eye!|There's nobody like my mentor!",
    ),
    "BattleFrontier_Lounge2_Text_AmazingPowerOfPersuasion": (
        "What a way with people!|There's nobody like my mentor!",
    ),
    "BattleFrontier_Lounge2_Text_ThisPlaceIsScaringMe": (
        "...What is this place?|It's beginning to frighten me...",
    ),

    # -- Lounge 3: the man running a book -------------------------------------
    "BattleFrontier_Lounge3_Text_CantYouSeeWereBusyHere": (
        "...What is it you want?",
        "Can't you see we're busy?|Whatever it is, it can wait.",
    ),
    "BattleFrontier_Lounge3_Text_HowAboutEnteringEventForMe": (
        "You'd do well out of it too. So how about it?",
        "How about entering that one for me?",
    ),
    "BattleFrontier_Lounge3_Text_SpotMeSomeBattlePoints": (
        "Perfect. Now -- how about lending me some of your Battle Points?",
        "Trust me. You'll see my gratitude afterwards.",
    ),
    "BattleFrontier_Lounge3_Text_HowMuchCanYouSpot": (
        "Good, good!|How much can you spare?",
    ),
    "BattleFrontier_Lounge3_Text_YouDontHaveEnoughPoints": (
        "No, no, no!|You haven't got that many Battle Points!",
        "Don't waste everybody's afternoon.",
    ),
    "BattleFrontier_Lounge3_Text_ThanksOffYouGo": (
        "Heheh! Much obliged!|Off you go, then!",
    ),
    "BattleFrontier_Lounge3_Text_NiceTryCantReturnPoints": (
        "Oh. It's you...|Good try...",
        "I hate to say it, but I can't give your Battle Points back...",
        "Let it be a spur to us both, eh?",
    ),
    "BattleFrontier_Lounge3_Text_HelloChampHeresYourPoints": (
        "Yes! Hello there, champion!",
        "I knew you could!|I knew you would!|We've both come out of this "
        "well!",
        "Here are your Battle Points, and a little extra from me.",
    ),
    "BattleFrontier_Lounge3_Text_ObtainedBattlePoints": (
        "{PLAYER} obtained {STR_VAR_1} Battle Points.",
    ),
    "BattleFrontier_Lounge3_Text_ThinkOfMeForAnotherChallenge": (
        "If you fancy another go, think of me!",
    ),
    "BattleFrontier_Lounge3_Text_NotInterested": (
        "Not interested?|You shouldn't be so shy of a chance!",
    ),
    "BattleFrontier_Lounge3_Text_Oh": (
        "Oh...",
    ),
    "BattleFrontier_Lounge3_Text_BackedWrongTrainer": (
        "Backed the wrong one again!",
        "Perhaps I should just battle, like everybody else...",
    ),
    "BattleFrontier_Lounge3_Text_TrainerGoodButRattled": (
        "That TRAINER...",
        "Good enough. But rattles too easily to last in the BATTLE DOME...",
    ),
    "BattleFrontier_Lounge3_Text_KnowWinnerWhenISeeOne": (
        "Giggle!|I know a winner when one walks in!",
    ),
    "BattleFrontier_Lounge3_Text_ShouldBeTakingChallenges": (
        "Those TRAINERS...|What are they doing standing about?",
        "They should be taking challenges.",
    ),

    # -- Lounge 5: the girl and the people watching her -----------------------
    "BattleFrontier_Lounge5_Text_NatureGirlGreeting": (
        "Ehehe!|I can tell what POKéMON are thinking!",
        "Please!|Can I see yours?",
    ),
    "BattleFrontier_Lounge5_Text_NatureGirlNoneShown": (
        "Boo!|Meanie!",
    ),
    "BattleFrontier_Lounge5_Text_NatureGirlEgg": (
        "That's silly! An EGG is asleep!|I can't talk to it!",
    ),
    "BattleFrontier_Lounge5_Text_LadyClaimsSheUnderstandsPokemon": (
        "How sweet!|That little one says she can understand POKéMON!",
    ),
    "BattleFrontier_Lounge5_Text_GirlSayingSomethingProfound": (
        "I have the feeling that child is saying something rather deep.",
    ),
    "BattleFrontier_Lounge5_Text_GirlPlaysAtRedHouseALot": (
        "I know something!",
        "That little girl is always playing at the red house!",
    ),

    # -- Lounge 7: the two tutors and the two watching them -------------------
    "BattleFrontier_Lounge7_Text_LeftTutorIntro": (
        "Buhahaha!",
        "You wouldn't know it to look at me now, but I was a hard TRAINER "
        "once.",
        "The hardest BEAUTY in the region, they said.",
        "... ... ... ... ...",
        "What is it?|You don't believe me.",
        "I'm not like that windbag over there. I can actually do it.",
        "Let me show you. I'll teach your POKéMON moves that are special and "
        "pretty with it.",
        "My lessons aren't free, mind. A few Battle Points will do.",
    ),
    "BattleFrontier_Lounge7_Text_LeftTutorWelcomeBack": (
        "Buhahaha!",
        "Back for more moves that are special and pretty with it?",
    ),
    "BattleFrontier_Lounge7_Text_RightTutorIntro": (
        "Ihihihi!",
        "Hard to see it now, I know, but I was a splendid TRAINER once.",
        "The most unbeatable SWIMMER in the region, they said.",
        "... ... ... ... ...",
        "What's the matter?|You don't believe me.",
        "I'm not like that clown over there. I have actually done it.",
        "I can show you. I'll teach your POKéMON moves that are hard and "
        "handsome with it.",
        "My lessons aren't free, mind. A few Battle Points will do.",
    ),
    "BattleFrontier_Lounge7_Text_RightTutorWelcomeBack": (
        "Ihihihi!",
        "Come for moves that are hard and handsome with it?",
    ),
    "BattleFrontier_Lounge7_Text_TeachWhichMove": (
        "Right, right. Look here.|Which shall I teach?",
    ),
    "BattleFrontier_Lounge7_Text_MoveWillBeXBattlePoints": (
        "{STR_VAR_1}, is it?|That'll be {STR_VAR_2} Battle Points.",
    ),
    "BattleFrontier_Lounge7_Text_TeachMoveToWhichMon": (
        "Right, right. Now pick which one I'm teaching it to.",
    ),
    "BattleFrontier_Lounge7_Text_HaventGotEnoughPoints": (
        "What's this?|You haven't got the Battle Points!",
    ),
    "BattleFrontier_Lounge7_Text_IllTakeBattlePoints": (
        "See what I can do?|I'll take those Battle Points, thank you.",
    ),
    "BattleFrontier_Lounge7_Text_YouDontWantTo": (
        "What's that?|You'd rather not...",
        "Well. If you ever want to see what I can do, you know where I am.",
    ),
    "BattleFrontier_Lounge7_Text_ThinkLadiesDontGetAlong": (
        "The way those two talk about each other, you'd think they couldn't "
        "stand it.",
        "But if that were true they wouldn't sit out here together, would "
        "they.",
    ),
    "BattleFrontier_Lounge7_Text_LadiesWereStrongAndBeautiful": (
        "When I was a YOUNGSTER, those two were strong and they were "
        "beautiful.",
        "Every TRAINER I knew wanted to be one of them.",
        "And the years haven't taken any of it away.",
        "If anything the moves they teach have got finer.",
        "But... I can't help feeling it all the same...",
        "Time is a cruel thing.",
    ),
}


def build() -> dict[str, tuple[str, ...]]:
    blocks = dict(HANDWRITTEN)
    prefix2 = "BattleFrontier_Lounge2_Text_"
    for title, (name, character, silver, gold) in BRAINS.items():
        # The report further up the manifest names only the hall and the
        # title. Here is where the man puts a person behind it, so the
        # first of the two roster lines carries the character sketch.
        sketch = f"{name} runs that one. {character[0].upper()}{character[1:]}."
        if silver:
            blocks[f"{prefix2}{title}SilverMons"] = (
                f"Have you battled {name} yet?|{sketch}",
                "When they're only taking your measure, the word is they "
                "bring these three:",
                ", ".join(silver) + ".",
            )
            blocks[f"{prefix2}{title}GoldMons"] = (
                f"Have you battled {name} in earnest?",
                "When they mean it, the word is they bring these three:",
                ", ".join(gold) + ".",
            )
        else:
            blocks[f"{prefix2}{title}SilverMons"] = (
                f"Have you battled {name} yet?|{sketch}",
                "Let me think... he takes three rentals, same as anyone.",
                "He fights under very near the same conditions you do.",
            )
            blocks[f"{prefix2}{title}GoldMons"] = (
                f"Have you battled {name} in earnest?",
                "Still three rentals, even then.",
                "He fights under very near the same conditions you do.",
            )

    prefix3 = "BattleFrontier_Lounge3_Text_"
    for suffix, event in EVENTS.items():
        blocks[f"{prefix3}Challenge{suffix}"] = (
            f"What I want is a TRAINER about to take {event}.",
            "And so far I haven't seen one with the look of a winner.",
        )
        blocks[f"{prefix3}GetTo{suffix}"] = (
            f"Get yourself to {event}, and quickly!",
            "This one has to be won!|Don't waste it!|We're both riding on "
            "you!",
        )

    prefix5 = "BattleFrontier_Lounge5_Text_"
    for nature, (likes, change) in NATURES.items():
        blocks[f"{prefix5}NatureGirl{nature}"] = (
            "Hmhm...",
            f"This one says {CHILD[likes]}!|{CHANGE[change]}",
        )
    return blocks


PARAGRAPHS = build()
TARGETS = tuple(PARAGRAPHS)


def which(label: str) -> int:
    return int(re.search(r"Lounge(\d)", label).group(1))


def block_pattern(label: str) -> re.Pattern[str]:
    return re.compile(
        rf"(?ms)^{re.escape(label)}::?\n(?P<body>.*?)"
        rf"(?=^[A-Za-z0-9_]+(?:::|:)(?:\n|$)|\Z)"
    )


def payloads() -> dict[str, tuple[str, ...]]:
    composed = {}
    for label, paragraphs in PARAGRAPHS.items():
        glued_paragraphs = []
        for paragraph in paragraphs:
            for name in WHOLE:
                paragraph = paragraph.replace(name, glued(name))
            glued_paragraphs.append(paragraph)
        composed[label] = BOX.compose(tuple(glued_paragraphs))
    return composed


def render(sources: dict[int, str]) -> dict[int, str]:
    composed = payloads()
    rendered = dict(sources)
    for label in TARGETS:
        n = which(label)
        matches = list(block_pattern(label).finditer(rendered[n]))
        if len(matches) != 1:
            raise ValueError(f"{label}: expected one text block, found {len(matches)}")
        if ".string" not in matches[0].group("body"):
            raise ValueError(f"{label}: target contains no .string payload")
        new_body = "".join(f'\t.string "{payload}"\n' for payload in composed[label]) + "\n"
        start, end = matches[0].span("body")
        rendered[n] = rendered[n][:start] + new_body + rendered[n][end:]
    return rendered


def mask(texts: dict[int, str]) -> dict[int, str]:
    masked = dict(texts)
    for label in TARGETS:
        n = which(label)
        match = block_pattern(label).search(masked[n])
        if not match:
            raise ValueError(f"cannot mask missing block: {label}")
        start, end = match.span("body")
        masked[n] = (masked[n][:start]
                     + '\t.string "<ARAUNA_FRONTIER_LOUNGES_EN>"\n\n'
                     + masked[n][end:])
    return masked


def validate_slots(sources: dict[int, str]) -> None:
    composed = payloads()
    for label in TARGETS:
        body = block_pattern(label).search(sources[which(label)]).group("body")
        available = set(re.findall(r"\{[A-Za-z_0-9]+\}", body))
        used = set(re.findall(r"\{[A-Za-z_0-9]+\}", "".join(composed[label])))
        if used - available:
            raise ValueError(
                f"{label}: uses {sorted(used - available)}, which the engine "
                f"does not fill here; the source uses {sorted(available)}")


def validate_rendered(sources: dict[int, str], rendered: dict[int, str]) -> None:
    if mask(sources) != mask(rendered):
        raise ValueError("non-dialogue structure changed while rendering")

    composed = payloads()

    def flat(label: str) -> str:
        return re.sub(r"\\[npl]", " ", "".join(composed[label]))

    # Seven halls, seven people. If two sketches read alike, the man who
    # collects information has stopped distinguishing them.
    sketches = [flat(f"BattleFrontier_Lounge2_Text_{title}SilverMons")
                for title in BRAINS]
    if len(set(sketches)) != len(sketches):
        raise ValueError("two of the seven MASTERS are introduced identically")
    for title, (name, _, _, _) in BRAINS.items():
        for kind in ("SilverMons", "GoldMons"):
            if name not in flat(f"BattleFrontier_Lounge2_Text_{title}{kind}"):
                raise ValueError(
                    f"{title}{kind}: no longer names {name}, and the seven "
                    f"reports are only told apart by the name")

    # The tout sends a player to a specific hall. Twenty-four lines, each
    # naming its own, and none naming another's.
    for suffix, event in EVENTS.items():
        for shape in ("Challenge", "GetTo"):
            text = flat(f"BattleFrontier_Lounge3_Text_{shape}{suffix}")
            if event not in text:
                raise ValueError(f"{shape}{suffix}: no longer names {event!r}")

    # The girl reads the same three kinds the BATTLE PALACE explains, and
    # every nature the engine can hand her has to be covered.
    for nature, (likes, change) in NATURES.items():
        text = flat(f"BattleFrontier_Lounge5_Text_NatureGirl{nature}")
        if CHILD[likes] not in text:
            raise ValueError(f"NatureGirl{nature}: lost what it prefers")
        if CHANGE[change].rstrip("!") not in text:
            raise ValueError(f"NatureGirl{nature}: lost what it does in trouble")
    if len(set(CHILD.values())) != 3:
        raise ValueError("the girl no longer has three kinds to tell apart")

    # The move descriptions are not ours, but they are drawn in a 96px window
    # and nothing else measures them.
    ruler = Ruler()
    string = re.compile(r'\.string "((?:[^"\\]|\\.)*)"')
    for match in re.finditer(
            r"(?ms)^BattleFrontier_Lounge7_Text_([A-Za-z0-9]+Desc)::?\n(?P<b>.*?)"
            r"(?=^[A-Za-z0-9_]+::?(?:\n|$)|\Z)", rendered[7]):
        for literal in string.findall(match.group("b")):
            for line in ruler.lines(literal):
                if line and ruler.width(line) > DESCRIPTION_CEILING:
                    raise ValueError(
                        f"{match.group(1)}: {ruler.width(line)}px is past the "
                        f"{DESCRIPTION_CEILING}px the tutor menu draws: {line!r}")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Render the four BATTLE FRONTIER lounges in English.")
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--in-place", action="store_true")
    args = parser.parse_args()
    if args.check and args.in_place:
        parser.error("use either --check or --in-place")

    sources = {n: path.read_text(encoding="utf-8") for n, path in LOUNGES.items()}
    validate_slots(sources)
    rendered = render(sources)
    validate_rendered(sources, rendered)

    if args.in_place:
        for n, path in LOUNGES.items():
            path.write_text(rendered[n], encoding="utf-8")
    print(f"Frontier lounges English renderer OK: {len(TARGETS)} blocks.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
