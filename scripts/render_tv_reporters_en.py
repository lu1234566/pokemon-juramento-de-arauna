#!/usr/bin/env python3
"""BIA and TITO, and the other people who point a camera at you.

BIA does the talking and TITO does the filming, and they are the only
television people in the game the player actually meets: they ambush you on a
road, lose to you, and put it out that evening as IN SEARCH OF TRAINERS. So
the road dialogue and the broadcast have to be recognisably the same two
people -- BIA excited on the spot and BIA excited in an edit suite -- which is
what makes this worth doing as one renderer rather than two.

TITO barely speaks. What he says is always about the footage, never about the
battle, and he is right about the footage every time.

Also here: the reporter in the fan club who interviews you about one POKéMON,
the SAFARI FAN CLUB's man in the field, and the CONTEST LIVE UPDATES bulletin
that interrupts itself to interview a woman who has just lost. That last one
is Emerald at its most careless -- the presenter tells a crying contestant her
POKéMON is the wrong colour -- and it is kept, because the joke is that he
has no idea what he has said.

The renderer holds both reporters to their names and to who says what: a line
BIA speaks must be marked BIA, and TITO's must be marked TITO.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools" / "arauna"))
from textbox import TextBox, glued  # noqa: E402

TV = ROOT / "data" / "text" / "tv.inc"

BOX = TextBox({"{PLAYER}": 7, "{STR_VAR_1}": 14, "{STR_VAR_2}": 14,
               "{STR_VAR_3}": 14, "{POKEBLOCK}": 9}, width=34)

TARGETS: dict[str, tuple[tuple[str, ...], tuple[str, ...]]] = {
    # -- the reporter in the fan club -----------------------------------------
    "SlateportCity_PokemonFanClub_Text_InterviewRequest": (
        ("very close to your", "willing to tell"), (
            "Hello -- you and your {STR_VAR_1} look close.",
            "Do you know what I do?|I report for the television.",
            "I go about asking people about their POKéMON.",
            "Would you tell me a little about that {STR_VAR_1}?",
        )),
    "SlateportCity_PokemonFanClub_Text_InterviewRequestHasName": (
        ("lavish", "simple questions"), (
            "Well!",
            "Anyone can see how much that {STR_VAR_1} is loved.",
            "And it's called {STR_VAR_2}.",
            "May I ask you a favour?",
            "I report for the television, and I'm running a survey on POKéMON.",
            "Would you answer a few easy questions for me?",
        )),
    "SlateportCity_PokemonFanClub_Text_HereGoesQuickAnswers": (
        ("Thank you", "quick answers"), (
            "Wonderful! Thank you!",
            "Here we go.|Short answers are fine.",
        )),
    "SlateportCity_PokemonFanClub_Text_DescribeFeelingsFirstMetMon": (
        ("first met", "describe your feelings"), (
            "When you first met {STR_VAR_1}, what did you feel?",
            "How would you put it?",
        )),
    "SlateportCity_PokemonFanClub_Text_LikenMonToSomethingYouLike": (
        ("cared for lovingly", "liken it"), (
            "Your {STR_VAR_1} is well looked after, that's plain.",
            "If you had to say what it is like -- something you're fond of -- "
            "what would you say?",
        )),
    "SlateportCity_PokemonFanClub_Text_WhatAttractedYouAboutMon": (
        ("beloved", "attracted you"), (
            "This one is about that {STR_VAR_1} as well.",
            "What was it about {STR_VAR_1} that got you?",
        )),
    "SlateportCity_PokemonFanClub_Text_WhatDoPokemonMeanToYou": (
        ("makes sense", "mean to you"), (
            "Right. That makes sense.",
            "The next one is a little harder.",
            "Here it is...",
            "What do POKéMON mean to you?",
        )),
    "SlateportCity_PokemonFanClub_Text_TellMeAnythingAboutYourMon": (
        ("thank you", "anything"), (
            "Oh, thank you!",
            "Then tell me whatever you like about your {STR_VAR_1}.",
        )),
    "SlateportCity_PokemonFanClub_Text_ThatsAllForInterview": (
        ("Thanks for helping", "Bye-bye"), (
            "I see!",
            "Hmhm...",
            "There!|Thank you for that.",
            "It was a pleasure, and I learned something.",
            "This may well end up on the television. Do watch for it!",
            "That's everything.|Goodbye!",
        )),
    "SlateportCity_PokemonFanClub_Text_ThatsAllForInterview2": (
        ("interesting account", "Bye-bye"), (
            "Well...|That is worth hearing.",
            "You and {STR_VAR_1} really are close, aren't you.",
            "I think that will make a fine piece of television.",
            "I'll make something worth watching of it. Keep an eye out.",
            "That's everything.|Goodbye!",
        )),
    "SlateportCity_PokemonFanClub_Text_HereIfYouGetUrgeToTellMe": (
        ("get the urge",), (
            "Oh -- of course...",
            "Well, if you ever feel like talking about POKéMON, I'm here.",
        )),
    "SlateportCity_PokemonFanClub_Text_EnjoyDoingInterviews": (
        ("enjoy this job",), (
            "I like this work. You learn about POKéMON by asking after them.",
        )),

    # -- the bulletin that interrupts itself ----------------------------------
    "ContestLadyShow_Text_Intro": (("Sorry to interrupt", "impromptu"), (
        "“POKéMON CONTEST LIVE UPDATES!”",
        "MC: Forgive us for interrupting, and thank you for staying with us!",
        "We are live from a {STR_VAR_1} that has only just ended!",
        "Spectators: ?!!!!",
        "MC: Oh! The competitors are coming this way!",
        "I shall try to get a word for those of you at home!",
        "Spectators: ?!!!!|?!!!!",
    )),
    "ContestLadyShow_Text_Won": (("congratulate you", "Are you watching"), (
        "MC: Excuse me!|Thank you for joining us live!",
        "May I congratulate you on the win?",
        "What made the difference today?",
        "BEAUTY: We gave it everything, my {STR_VAR_2} and I!",
        "But we would never have managed it without all the help we had "
        "getting here!",
        "MC: Is there somebody you'd like to share this with?|Say it now, "
        "live!",
        "BEAUTY: Hello, out there!",
        "{STR_VAR_3}! Are you watching?|We did it!|Thank you!",
    )),
    "ContestLadyShow_Text_Lost": (("heartbreaking", "coloration"), (
        "MC: Excuse me!|Thank you for joining us live!",
        "That must have been a disappointment. Any thoughts?",
        "BEAUTY: It's hard...|My {STR_VAR_2} and I did everything we could...",
        "But I feel I've let down everyone who helped us get here.",
        "MC: I hate to say it, but the POKéMON's colour is a little off.",
        "BEAUTY: {STR_VAR_3}, I'm so sorry...|I'll do better, I swear I "
        "will...|...Sniff... Waaaaah!",
        "Spectators: Look at that.|The poor girl!",
        "MC: Er... Oh dear...",
        "Er... that's all the time we have!|Thank you for watching!",
    )),
    "ContestLadyShow_Text_LostBadly": (("Nothing went right", "coloration"), (
        "MC: Excuse me!|Thank you for joining us live!",
        "How did the CONTEST go for you?",
        "BEAUTY: Nothing went right at all...|For some reason my {STR_VAR_2} "
        "could not get the hall on its side.",
        "MC: I hate to say it, but the POKéMON's colour is a little off.",
        "BEAUTY: ... ... ... ... ...|...Sniff... Waaaaah!",
        "Spectators: Look at that.|The poor girl!",
        "MC: Er... Oh dear...",
        "Er... that's all the time we have!|Thank you for watching!",
    )),

    # -- BIA and TITO on the road ---------------------------------------------
    "GabbyAndTy_Text_GabbyPreFirstBattle": (("spotted a tough", "roll camera"), (
        "BIA: Oh! A tough-looking TRAINER, here of all places!",
        "Right -- camera up!|Let's get this.",
    )),
    "GabbyAndTy_Text_GabbyIntro": (("remember us", "cue interview"), (
        "BIA: Oh! It's {PLAYER}! Hello!|Do you remember us?",
        "Show us how much better you've got. Right -- rolling!",
    )),
    "GabbyAndTy_Text_GabbyDefeatFirstTime": (("eyes didn't lie", "astonishing"), (
        "BIA: My eye did not lie!|I have found an astonishing TRAINER!",
    )),
    "GabbyAndTy_Text_WhoAreYouInterview": (("Who are you", "bit of your time"), (
        "BIA: Extraordinary! Extraordinary!|Who are you?!",
        "I knew there was something the moment we saw you!",
        "Let me explain. We go everywhere, talking to every sort of TRAINER "
        "there is.",
        "So -- would you give us a moment for an interview?",
    )),
    "GabbyAndTy_Text_QuoteFromLastInterview": (("clincher", "never, ever forget"), (
        "BIA: “{STR_VAR_1}!”",
        "Remember? That's what you gave us last time, at the end.",
        "I never forget a line like that. Never.",
    )),
    "GabbyAndTy_Text_YouStompedUsInterviewAgain": (("stomped", "interviewed again"), (
        "Last time we battled, you had us before we were ready...",
        "Anyway -- what do you say?|Another interview?",
    )),
    "GabbyAndTy_Text_YouThrewABallAtUsInterviewAgain": (("POKé BALL at us", "interviewed again"), (
        "Last time we battled -- did you throw a POKé BALL at us?",
        "We were scandalised! We told everybody. Everybody.",
        "Anyway -- what do you say?|Another interview?",
    )),
    "GabbyAndTy_Text_CleverItemSkillsInterviewAgain": (("item", "interviewed again"), (
        "Last time we battled, you did us with the items. Cleverly, too.",
        "Anyway -- what do you say?|Another interview?",
    )),
    "GabbyAndTy_Text_WeLookedRespectableInterviewAgain": (("respectable", "interviewed again"), (
        "Last time we battled, we came out of it looking respectable.",
        "Anyway -- what do you say?|Another interview?",
    )),
    "GabbyAndTy_Text_InterviewAgain": (("interviewed again",), (
        "Anyway -- what do you say?|Another interview?",
    )),
    "GabbyAndTy_Text_DescribeYourFeelings": (("You will?", "short and sweet"), (
        "You will?|Thank you!",
        "Right -- tell me how that battle felt, and keep it short. Go!",
    )),
    "GabbyAndTy_Text_PerfectWellBeSeeingYou": (("perfect clincher", "seeing you"), (
        "BIA: Yes! That's it!|That's the line!",
        "I can feel a good programme in this.",
        "There's every chance it goes out, so watch for us!",
        "Right!|We'll be seeing you!",
    )),
    "GabbyAndTy_Text_DontGiveUpKeepingEyeOut": (("don't give up", "eye out"), (
        "BIA: Oh...",
        "Well -- don't give it up!|We'll be keeping an eye out for you!",
    )),
    "GabbyAndTy_Text_KeepingAnEyeOutForYou": (("eye out",), (
        "BIA: We'll be keeping an eye out for you!",
    )),
    "GabbyAndTy_Text_GabbyNotEnoughMons": (("strong TRAINER", "lot of POKéMON"), (
        "BIA: Is there nobody about with a strong team and more than one of "
        "them?",
    )),
    "GabbyAndTy_Text_GiveUsAnInterviewThisTime": (("gotten a lot stronger", "this time"), (
        "BIA: Well, look at you!",
        "You've come on a very long way since we last battled.",
        "We were right about you the first time we saw you.",
        "So -- what do you say?|Will you give us an interview this time?",
    )),
    "GabbyAndTy_Text_GabbyDefeat": (("intense battle", "on camera"), (
        "BIA: What a battle!|Did you get all of that?",
    )),
    "GabbyAndTy_Text_TyPreFirstBattle": (("lookie here", "rolling"), (
        "TITO: Well, look at that. A tough-looking TRAINER, right here.|"
        "Camera's rolling.",
    )),
    "GabbyAndTy_Text_TyIntro": (("remember you", "camera"), (
        "TITO: Well, look who it is.|I remember you.",
        "I'll get the whole thing on this camera.",
    )),
    "GabbyAndTy_Text_TyPostBattle": (("natural", "footage"), (
        "TITO: You're a natural.|That's good footage, that is.",
    )),
    "GabbyAndTy_Text_TyNotEnoughMons": (("only have the one", "better footage"), (
        "TITO: That's the one POKéMON you've got?",
        "More of them would make better footage, but there it is...",
    )),
    "GabbyAndTy_Text_TyDefeatFirstTime": (("hot", "scoop"), (
        "TITO: We found a real one there.|That's a scoop, that is.",
    )),
    "GabbyAndTy_Text_TyDefeat": (("got it all", "on camera"), (
        "TITO: Got the lot.|Whole battle's on the camera.",
    )),

    # -- and the programme they make of it ------------------------------------
    "gTVInSearchOfTrainersText00": (("IN SEARCH OF TRAINERS", "piqued our interest"), (
        "IN SEARCH OF TRAINERS...",
        "BIA: Hello! Today I'm out near {STR_VAR_1}.",
        "We're looking for people coming up who nobody has heard of yet.",
        "And today we turned the camera on the TRAINER {PLAYER}.",
        "There is something about this one.",
    )),
    "gTVInSearchOfTrainersText01": (("battled", "someone special"), (
        "We have battled {PLAYER} before, and I can tell you the TRAINER has "
        "come on since.",
        "I knew there was something the moment we saw them!",
    )),
    "gTVInSearchOfTrainersText02": (("fastest way is to battle", "ruthlessly strong"), (
        "The surest way to know how strong a TRAINER is...",
        "Well -- the quickest way is to battle them. So we did.",
        "... ...",
        "Which is how we came to be in a battle with {PLAYER}.",
        "We were flattened, rolled up and put away.",
        "{PLAYER} is frighteningly strong...",
        "Here is what we made of it, having been on the wrong end.",
    )),
    "gTVInSearchOfTrainersText03": (("divine", "sign of friendship"), (
        "The pairing of {STR_VAR_1} and {STR_VAR_3} was a wonder!",
        "The two of them holding each other up in the middle of it...",
        "It was a fine thing to watch!",
        "{STR_VAR_2} was the last move the TRAINER used on us.",
        "{STR_VAR_2} is how {STR_VAR_1} and {STR_VAR_3} say they trust one "
        "another!",
    )),
    "gTVInSearchOfTrainersText04": (("lost confidence", "confident TRAINERS"), (
        "...I have rather lost confidence in myself over this.",
        "We were beaten before we landed a single attack.|Ohhh... Snivel...",
        "And even so, {PLAYER}'s battles are worth watching.",
        "Any TRAINER who fancies their chances should go and find {PLAYER}.",
    )),
    "gTVInSearchOfTrainersText05": (("throw a POKé BALL", "please caution"), (
        "There is one thing to be said.|Do not throw a POKé BALL in a TRAINER "
        "battle!",
        "{PLAYER} is strong, certainly, and has not read the rules.",
        "So a request to everyone watching.",
        "If you see {PLAYER}, have a word!",
    )),
    "gTVInSearchOfTrainersText06": (("reading the", "timing of item usage"), (
        "{PLAYER} reads what the other side is going to do.",
        "The timing of those items was something to see!",
    )),
    "gTVInSearchOfTrainersText07": (("pretty good", "ways to go"), (
        "Honestly, I had begun to think I might be rather good.",
        "We lost, but it was a close-run thing.",
        "So if you're finding me hard work, you've a way to go yet, {PLAYER}!",
    )),
    "gTVInSearchOfTrainersText08": (("succinct summary", "next broadcast"), (
        "After the battle we asked {PLAYER} to sum it up.",
        "The reply: “{STR_VAR_1}.”",
        "{PLAYER}'s POKéMON {STR_VAR_2} and {STR_VAR_3}...|And "
        "“{STR_VAR_1}”...",
        "Mmm. There is a great deal in that.",
        "Which is no surprise. A good TRAINER has good things to say.",
        "That's all for today!|Until the next one!",
    )),

    # -- the man in the tall grass --------------------------------------------
    "gTVSafariFanClubText00": (("SAFARI FAN CLUB", "SAFARI GUIDE"), (
        "SAFARI FAN CLUB!",
        "REPORTER: Right, everyone!|Getting those SAFARI BALLS away, are we?",
        "I certainly am -- I'm standing in the SAFARI ZONE, and it is full of "
        "remarkable POKéMON!",
        "Let's have a word with this good fellow, the SAFARI GUIDE!",
        "Right then -- how are the visiting TRAINERS getting on?",
    )),
    "gTVSafariFanClubText01": (("going\\n", "especially well"), (
        "GUIDE: They're all going at it hard enough.",
        "{STR_VAR_1} is doing particularly well.",
        "Caught {STR_VAR_2} POKéMON earlier on, that one.",
    )),
    "gTVSafariFanClubText02": (("clever with", "that time"), (
        "That TRAINER knows what to do with a {POKEBLOCK}.|Used {STR_VAR_2} "
        "that time, I believe.",
    )),
    "gTVSafariFanClubText03": (("didn't use a single", "expert"), (
        "Didn't use a single {POKEBLOCK}! Not one!",
        "There's an expert for you.",
    )),
    "gTVSafariFanClubText04": (("Is that right", "great technique"), (
        "REPORTER: Is that so, now?",
        "Sounds as though {STR_VAR_1} is a proper SAFARI hand!",
        "GUIDE: I hope the TRAINER comes back and shows us that again.",
    )),
    "gTVSafariFanClubText05": (("No one seems", "especially bad"), (
        "GUIDE: Nobody's having much luck today.",
        "{STR_VAR_1} had the worst of it.",
        "Only managed {STR_VAR_2} POKéMON, that one.",
    )),
    "gTVSafariFanClubText06": (("No one seems", "Not a one"), (
        "GUIDE: Nobody's having much luck today.",
        "{STR_VAR_1} had the worst of it.",
        "Didn't catch a single POKéMON. Not one!",
    )),
    "gTVSafariFanClubText07": (("does use", "bit better"), (
        "The TRAINER does use a {POKEBLOCK}.|Used {STR_VAR_2} that time, I "
        "believe.",
        "But I do wish that one would get the hang of it.",
    )),
    "gTVSafariFanClubText08": (("better\\n", "weren't"), (
        "I fancy the TRAINER would do better with a {POKEBLOCK}, which wasn't "
        "used at all that time.",
    )),
    "gTVSafariFanClubText09": (("Is that right", "over and over"), (
        "REPORTER: Is that so, now?",
        "Sounds as though {STR_VAR_1} needs a few more days out here.",
        "GUIDE: I hope the TRAINER comes back until it comes right.",
    )),
    "gTVSafariFanClubText10": (("Quite right", "cheerio"), (
        "REPORTER: Quite right too!|Having a go at a hard thing is what "
        "matters!",
        "Viewers -- come down to the SAFARI and have a go yourselves!",
        "Until next time -- cheerio!",
    )),
}


def block_pattern(label: str) -> re.Pattern[str]:
    return re.compile(
        rf"(?ms)^{re.escape(label)}::?\n(?P<body>.*?)(?=^[A-Za-z0-9_]+(?:::|:)(?:\n|$)|\Z)"
    )


def payloads() -> dict[str, tuple[str, ...]]:
    composed = {}
    for label, (_, paragraphs) in TARGETS.items():
        paragraphs = tuple(p.replace("SAFARI ZONE", glued("SAFARI ZONE"))
                            .replace("POKé BALL", glued("POKé BALL"))
                            .replace("SAFARI BALLS", glued("SAFARI BALLS"))
                           for p in paragraphs)
        composed[label] = BOX.compose(paragraphs)
    return composed


def render(source: str) -> str:
    composed = payloads()
    rendered = source
    for label, (markers, _) in TARGETS.items():
        matches = list(block_pattern(label).finditer(rendered))
        if len(matches) != 1:
            raise ValueError(f"{label}: expected one text block, found {len(matches)}")
        body = matches[0].group("body")
        if ".string" not in body:
            raise ValueError(f"{label}: target contains no .string payload")
        for marker in markers:
            if marker not in body:
                raise ValueError(f"{label}: source marker missing: {marker!r}")
        new_body = "".join(f'\t.string "{payload}"\n' for payload in composed[label]) + "\n"
        start, end = matches[0].span("body")
        rendered = rendered[:start] + new_body + rendered[end:]
    return rendered


def mask(text: str) -> str:
    masked = text
    for label in TARGETS:
        match = block_pattern(label).search(masked)
        if not match:
            raise ValueError(f"cannot mask missing block: {label}")
        start, end = match.span("body")
        masked = masked[:start] + '\t.string "<ARAUNA_TV_REPORTERS_EN>"\n\n' + masked[end:]
    return masked


def validate_slots(source: str) -> None:
    composed = payloads()
    for label in TARGETS:
        body = block_pattern(label).search(source).group("body")
        available = set(re.findall(r"\{STR_VAR_\d\}", body))
        used = set(re.findall(r"\{STR_VAR_\d\}", "".join(composed[label])))
        if used - available:
            raise ValueError(
                f"{label}: uses {sorted(used - available)}, which the engine "
                f"does not fill here; the source uses {sorted(available)}")
        if "{PLAYER}" in "".join(composed[label]) and "{PLAYER}" not in body:
            raise ValueError(f"{label}: names the player where the engine does not")


def validate_rendered(source: str, rendered: str) -> None:
    if mask(source) != mask(rendered):
        raise ValueError("non-dialogue structure changed while rendering")

    composed = payloads()

    # The two of them are one crew but not one person. A line the source gives
    # to one of them must still be spoken by that one.
    for label in TARGETS:
        body = block_pattern(label).search(source).group("body")
        mine = "".join(composed[label])
        for name in ("BIA", "TITO"):
            if f"{name}:" in body and f"{name}:" not in mine:
                raise ValueError(f"{label}: {name} lost the line they speak")
        if "TITO:" in mine and "BIA:" in mine:
            raise ValueError(f"{label}: both reporters speak in one block")

    # TITO talks about the footage. That is the whole of his character, and
    # it is what keeps him from turning into a second BIA.
    for label in TARGETS:
        mine = "".join(composed[label])
        if "TITO:" not in mine:
            continue
        if not re.search(r"camera|footage|scoop|got the lot", mine, re.IGNORECASE):
            raise ValueError(f"{label}: TITO says something that is not about filming")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Render BIA and TITO, and the other reporters.")
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--in-place", action="store_true")
    args = parser.parse_args()
    if args.check and args.in_place:
        parser.error("use either --check or --in-place")

    source = TV.read_text(encoding="utf-8")
    validate_slots(source)
    rendered = render(source)
    validate_rendered(source, rendered)

    if args.in_place:
        TV.write_text(rendered, encoding="utf-8")
    print(f"TV reporters English renderer OK: {len(TARGETS)} blocks.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
