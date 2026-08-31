#!/usr/bin/env python3
"""The trainers of Route 110 and Route 117: the descent and the daycare road.

A hundred and fifteen blocks either side of Encruzilhada. Route 110 is the long
run down the CYCLING ROAD -- riders who cannot stop, triathletes mid-event, a
collector who wants to look at your team, a fortune teller who did not see this
coming. Route 117 is the flat road on the other side, where the DAY CARE is, and
almost everyone on it is raising something for somebody.

That is the seam this pass writes to. One road is about going fast and the other
is about taking your time, and the trainers on them should not sound alike.

The senior and junior students keep their pairing: DUDA still apologises to ANA
for every loss, and ANA still refuses to lose in front of her.

No payload names a species: the dex is generated, and a line naming a creature
would be wrong the next time it is.
"""
from __future__ import annotations

import argparse
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TRAINERS = ROOT / "data" / "text" / "trainers.inc"
MAX_VISIBLE_WIDTH = 32
CONTROL_RE = re.compile(r"\\[npl]")
PLACEHOLDER_RE = re.compile(r"\{[^}]+\}")

TARGETS: dict[str, tuple[tuple[str, ...], tuple[str, ...]]] = {
    # -- Route 110, the long descent ----------------------------------------
    "Route110_Text_JacobIntro": (("BIKE racing",), (
        "LAERTE: Whoa! Mind the\\n",
        "line!\\p",
        "You've not raced down here\\n",
        "before, have you.$",
    )),
    "Route110_Text_JacobDefeated": (("brakes failed",), (
        "LAERTE: Whoa! No brakes!$",
    )),
    "Route110_Text_JacobPostBattle": (("Flat tires", "Inspect your BIKE"), (
        "LAERTE: Soft tyre, worn\\n",
        "brake, and this road will\\l",
        "put you in the dirt.\\p",
        "Check the BIKE. Every time.$",
    )),
    "Route110_Text_AnthonyIntro": (("keep up with my speed",), (
        "ALFREDO: Can you hold my\\n",
        "pace? Try.$",
    )),
    "Route110_Text_AnthonyDefeated": (("Crash and burn",), (
        "ALFREDO: Down I go.$",
    )),
    "Route110_Text_AnthonyPostBattle": (("Speed alone", "reconsider"), (
        "ALFREDO: Being fast doesn't\\n",
        "win a battle.\\p",
        "I need to think about that.$",
    )),
    "Route110_Text_BenjaminIntro": (("Don't panic",), (
        "ANTONIO: Going fast?\\n",
        "Then don't panic.$",
    )),
    "Route110_Text_BenjaminDefeated": (("shouldn't panic",), (
        "ANTONIO: I panicked. Of\\n",
        "course I panicked.$",
    )),
    "Route110_Text_BenjaminPostBattle": (("no need to panic", "plenty of time"), (
        "ANTONIO: No rush, no panic.\\p",
        "The road's not going\\n",
        "anywhere.$",
    )),
    "Route110_Text_BenjaminRegister": (("keep chugging", "Give me a shout"), (
        "ANTONIO: I'll keep rolling,\\n",
        "unhurried.\\p",
        "Shout if you want another.$",
    )),
    "Route110_Text_BenjaminRematchIntro": (("too fast", "Take it easy"), (
        "ANTONIO: You're going quick\\n",
        "again.\\p",
        "Slow down. Battle me.$",
    )),
    "Route110_Text_BenjaminRematchDefeated": (("didn't panic",), (
        "ANTONIO: Calm the whole\\n",
        "way through, and still\\l",
        "beaten.$",
    )),
    "Route110_Text_BenjaminRematchPostBattle": (("no need to panic", "plenty of time"), (
        "ANTONIO: Still no rush.\\p",
        "There's more time than\\n",
        "anyone tells you.$",
    )),
    "Route110_Text_AbigailIntro": (("triathlon", "three events"), (
        "ADRIANA: A triathlon is\\n",
        "three events, back to back.\\p",
        "Swim, ride, run. It is as\\n",
        "hard as it sounds.$",
    )),
    "Route110_Text_AbigailDefeated": (("battles are hard",), (
        "ADRIANA: Battling is hard\\n",
        "too. Nobody warned me.$",
    )),
    "Route110_Text_AbigailPostBattle": (("need a break", "proper rest"), (
        "ADRIANA: I'm stopping here\\n",
        "a while.\\p",
        "Rest counts as training.\\n",
        "It took me years to learn.$",
    )),
    "Route110_Text_AbigailRegister": (("I like you", "CYCLING ROAD"), (
        "ADRIANA: I like you.\\p",
        "Come back and race me on\\n",
        "the CYCLING ROAD.$",
    )),
    "Route110_Text_AbigailRematchIntro": (("battle while", "cycling"), (
        "ADRIANA: Battling halfway\\n",
        "down a hill.\\p",
        "There's nothing else like\\n",
        "it, is there.$",
    )),
    "Route110_Text_AbigailRematchDefeated": (("How could you be so strong",), (
        "ADRIANA: How are you this\\n",
        "strong already?$",
    )),
    "Route110_Text_AbigailRematchPostBattle": (("going after a record", "held you up"), (
        "ADRIANA: Were you timing a\\n",
        "run just now?\\p",
        "Sorry. I've cost you the\\n",
        "record, haven't I.$",
    )),
    "Route110_Text_JasmineIntro": (("without stopping", "thighs"), (
        "IRACEMA: I haven't stopped\\n",
        "pedalling since dawn.\\p",
        "My legs have gone solid.$",
    )),
    "Route110_Text_JasmineDefeated": (("muscle cramps",), (
        "IRACEMA: Cramp. Any second\\n",
        "now, cramp.$",
    )),
    "Route110_Text_JasminePostBattle": (("GYM BADGES", "so strong"), (
        "IRACEMA: You're carrying\\n",
        "BADGES.\\p",
        "That explains the last\\n",
        "three minutes.$",
    )),
    "Route110_Text_EdwardIntro": (("foreseen", "cannot possibly lose"), (
        "GASPAR: I already know how\\n",
        "this ends.\\p",
        "I cannot lose here.$",
    )),
    "Route110_Text_EdwardDefeated": (("prophesize my own demise",), (
        "GASPAR: I failed to foresee\\n",
        "precisely one thing.$",
    )),
    "Route110_Text_EdwardPostBattle": (("I see your future", "shining light"), (
        "GASPAR: Let me read yours.\\p",
        "Hmm. A light, some way off,\\n",
        "and you walking at it.$",
    )),
    "Route110_Text_JaclynIntro": (("dazzle you",), (
        "IEDA: Ahahaha! Prepare to\\n",
        "be amazed!$",
    )),
    "Route110_Text_JaclynDefeated": (("wondrously lost",), (
        "IEDA: I lost amazingly!$",
    )),
    "Route110_Text_JaclynPostBattle": (("only because it was", "all the time"), (
        "IEDA: That was a fluke.\\p",
        "A marvellous fluke, but a\\n",
        "fluke. Don't get used to it.$",
    )),
    "Route110_Text_EdwinIntro": (("Just one look",), (
        "GERALDO: May I see yours?\\p",
        "One look. That's all.$",
    )),
    "Route110_Text_EdwinDefeated": (("complete", "collection"), (
        "GERALDO: And my list is\\n",
        "still not finished.$",
    )),
    "Route110_Text_EdwinPostBattle": (("passion as a collector",), (
        "GERALDO: One I've never\\n",
        "seen, and I'm off again.\\p",
        "It never stops.$",
    )),
    "Route110_Text_EdwinRegister": (("MATCH CALL", "registrations"), (
        "GERALDO: I collect MATCH\\n",
        "CALL numbers as well.\\p",
        "Yours would suit the set.$",
    )),
    "Route110_Text_EdwinRematchIntro": (("caught any new", "Just one look"), (
        "GERALDO: Anything new since\\n",
        "we met?\\p",
        "One look. Only one.$",
    )),
    "Route110_Text_EdwinRematchDefeated": (("I envy you",), (
        "GERALDO: Yours. I envy you\\n",
        "yours.$",
    )),
    "Route110_Text_EdwinRematchPostBattle": (("rare POKéMON",), (
        "GERALDO: I want every rare\\n",
        "one there is.\\p",
        "I am aware that's a\\n",
        "problem.$",
    )),
    "Route110_Text_DaleIntro": (("sneak up behind me",), (
        "EDGAR: Hey! Don't come up\\n",
        "behind me like that!$",
    )),
    "Route110_Text_DaleDefeated": (("Drat",), (
        "EDGAR: Lost it! Drat!$",
    )),
    "Route110_Text_DalePostBattle": (("concentration", "floater"), (
        "EDGAR: Fishing is all\\n",
        "attention.\\p",
        "Watch the float. Nothing\\n",
        "else. Just the float.$",
    )),
    "Route110_Text_IsabelIntro": (("show", "delightful POKéMON"), (
        "GLAUCIA: I'll go anywhere to\\n",
        "show mine off.\\p",
        "Anywhere at all.$",
    )),
    "Route110_Text_IsabelDefeated": (("this won't do",), (
        "GLAUCIA: Oh dear. This will\\n",
        "not do.$",
    )),
    "Route110_Text_IsabelPostBattle": (("FAN CLUB",), (
        "GLAUCIA: Perhaps I should\\n",
        "stop battling and just take\\l",
        "them to the FAN CLUB.$",
    )),
    "Route110_Text_IsabelRegister": (("captive audience",), (
        "GLAUCIA: That was hardly a\\n",
        "proper showing.\\p",
        "You'll be my audience again.\\n",
        "As often as I can manage.$",
    )),
    "Route110_Text_IsabelRematchIntro": (("as often as you like",), (
        "GLAUCIA: I'd show them to\\n",
        "you every day if you asked.$",
    )),
    "Route110_Text_IsabelRematchDefeated": (("this won't do",), (
        "GLAUCIA: Oh dear. Not\\n",
        "again.$",
    )),
    "Route110_Text_IsabelRematchPostBattle": (("showing off", "I like to battle"), (
        "GLAUCIA: I'll never stop\\n",
        "showing them off.\\p",
        "But I do like the battling\\n",
        "part as well.$",
    )),
    "Route110_Text_TimmyIntro": (("in the grass",), (
        "WALDEMAR: Found something\\n",
        "good in the grass here!$",
    )),
    "Route110_Text_TimmyDefeated": (("Being cool isn't enough",), (
        "WALDEMAR: Looking good\\n",
        "isn't winning.$",
    )),
    "Route110_Text_TimmyPostBattle": (("just caught",), (
        "WALDEMAR: You can't fight\\n",
        "well with one you caught\\l",
        "an hour ago.\\p",
        "I keep learning that.$",
    )),
    "Route110_Text_AlyssaIntro": (("fell off", "embarrassment"), (
        "AURORA: I came off the road\\n",
        "back there.\\p",
        "Battle me so I stop\\n",
        "thinking about it.$",
    )),
    "Route110_Text_AlyssaDefeated": (("ended up losing",), (
        "AURORA: Oh no. And now\\n",
        "this as well.$",
    )),
    "Route110_Text_AlyssaPostBattle": (("humiliating",), (
        "AURORA: Fell off, then\\n",
        "lost.\\p",
        "I'd like the ground to open.$",
    )),
    "Route110_Text_JosephIntro": (("Full-throttle", "left behind"), (
        "MARCIO: Full speed from\\n",
        "here!\\p",
        "Keep up or get left.$",
    )),
    "Route110_Text_JosephDefeated": (("into the groove",), (
        "MARCIO: You kept up. All\\n",
        "right.$",
    )),
    "Route110_Text_JosephPostBattle": (("bring me down", "better man"), (
        "MARCIO: This doesn't put me\\n",
        "down.\\p",
        "Losing sharpens a person.$",
    )),
    "Route110_Text_KalebIntro": (("help each other", "adorable sight"), (
        "MAXIMO: Watch mine work\\n",
        "together.\\p",
        "There's nothing sweeter to\\n",
        "look at anywhere.$",
    )),
    "Route110_Text_KalebDefeated": (("compassion or pity",), (
        "MAXIMO: Have you no heart\\n",
        "at all?$",
    )),
    "Route110_Text_KalebPostBattle": (("done the best you", "my pretties"), (
        "MAXIMO: All right, all\\n",
        "right. You did your best.\\p",
        "Come here, both of you.$",
    )),

    # -- Route 117, the road past the DAY CARE ------------------------------
    "Route117_Text_IsaacIntro": (("POKéMON I'm raising",), (
        "JOSE: Would you battle the\\n",
        "ones I'm raising?\\p",
        "I need to see where they\\n",
        "are.$",
    )),
    "Route117_Text_IsaacDefeat": (("raised yours superbly",), (
        "JOSE: Yours have been\\n",
        "raised well. That shows.$",
    )),
    "Route117_Text_IsaacPostBattle": (("isn't all about power", "unique aspect"), (
        "JOSE: It isn't only power.\\p",
        "Bringing out the one thing\\n",
        "that's theirs alone is a\\l",
        "whole way of doing this.$",
    )),
    "Route117_Text_IsaacRegister": (("redouble my training", "look in on us"), (
        "JOSE: I'm going to train\\n",
        "harder.\\p",
        "Come and look in on us.$",
    )),
    "Route117_Text_IsaacRematchIntro": (("looking good, just like before",), (
        "JOSE: The ones I'm raising\\n",
        "are doing well.\\p",
        "Same as last time.$",
    )),
    "Route117_Text_IsaacRematchDefeat": (("DAY CARE skills",), (
        "JOSE: You know how to raise\\n",
        "them.\\p",
        "The DAY CARE would take you\\n",
        "on tomorrow.$",
    )),
    "Route117_Text_IsaacPostRematch": (("growing good", "CONTESTS"), (
        "JOSE: Yours are coming on\\n",
        "well.\\p",
        "You should put them in a\\n",
        "CONTEST.$",
    )),
    "Route117_Text_LydiaIntro": (("evaluate", "raised your POKéMON"), (
        "MARCIA: Let me see whether\\n",
        "you've raised them right.$",
    )),
    "Route117_Text_LydiaDefeat": (("growing properly",), (
        "MARCIA: Yes. They're coming\\n",
        "along properly.$",
    )),
    "Route117_Text_LydiaPostBattle": (("character traits",), (
        "MARCIA: Raise them by what\\n",
        "each one is like.\\p",
        "Not all the same way.$",
    )),
    "Route117_Text_LydiaRegister": (("superb TRAINER", "see you again"), (
        "MARCIA: I'm glad to have\\n",
        "met a TRAINER like you.\\p",
        "Let's meet again.$",
    )),
    "Route117_Text_LydiaRematchIntro": (("reevaluate",), (
        "MARCIA: Let me look at them\\n",
        "again.$",
    )),
    "Route117_Text_LydiaRematchDefeat": (("growing admirably",), (
        "MARCIA: Admirable. Truly.$",
    )),
    "Route117_Text_LydiaPostRematch": (("depending on their nature",), (
        "MARCIA: What they like to\\n",
        "eat follows their nature.\\p",
        "Learn one and you know the\\n",
        "other.$",
    )),
    "Route117_Text_DylanIntro": (("middle of a triathlon", "whatever"), (
        "FIRMINO: I'm mid-event, but\\n",
        "sure. Let's battle.$",
    )),
    "Route117_Text_DylanDefeat": (("ran out of energy",), (
        "FIRMINO: Nothing left in\\n",
        "the legs.$",
    )),
    "Route117_Text_DylanPostBattle": (("dropped to last",), (
        "FIRMINO: I may have just\\n",
        "dropped to last place.\\p",
        "Worth it. Probably.$",
    )),
    "Route117_Text_DylanRegister": (("train me",), (
        "FIRMINO: They have to be\\n",
        "strong too? Really?\\p",
        "Teach me how you do it.$",
    )),
    "Route117_Text_DylanRematchIntro": (("comfortably ahead", "quick battle"), (
        "FIRMINO: Mid-event again,\\n",
        "but I'm well ahead.\\p",
        "Make it quick.$",
    )),
    "Route117_Text_DylanRematchDefeat": (("out of energy again",), (
        "FIRMINO: Empty again.$",
    )),
    "Route117_Text_DylanPostRematch": (("tops in swimming", "not quite that confident"), (
        "FIRMINO: I'm first in the\\n",
        "swim and the ride.\\p",
        "This part I'm still no\\n",
        "good at.$",
    )),
    "Route117_Text_MariaIntro": (("triathlon training", "confident about my speed"), (
        "MARINA: I train for the\\n",
        "triathlon alongside mine.\\p",
        "We're quick. Both of us.$",
    )),
    "Route117_Text_MariaDefeat": (("more practices",), (
        "MARINA: More sessions.\\n",
        "That's all it is.$",
    )),
    "Route117_Text_MariaPostBattle": (("keep it up regularly", "Tomorrow"), (
        "MARINA: Training counts\\n",
        "only if you keep at it.\\p",
        "Right. Back to it.\\n",
        "Tomorrow.$",
    )),
    "Route117_Text_MariaRegister": (("training properly", "battle you later"), (
        "MARINA: You look like\\n",
        "someone who trains.\\p",
        "I'll take you on again.$",
    )),
    "Route117_Text_MariaRematchIntro": (("keeping up with your training", "evidence"), (
        "MARINA: Still training?\\n",
        "I certainly am.\\p",
        "Here's the proof.$",
    )),
    "Route117_Text_MariaRematchDefeat": (("more practices",), (
        "MARINA: More sessions.\\n",
        "Again.$",
    )),
    "Route117_Text_MariaPostRematch": (("resume training tomorrow",), (
        "MARINA: Back to training.\\n",
        "Tomorrow.\\p",
        "Find me again sometime.$",
    )),
    "Route117_Text_DerekIntro": (("BUG CATCHER", "BUG MANIAC"), (
        "EUCLIDES: I started out\\n",
        "catching the small ones.\\p",
        "Now people call me obsessed.\\p",
        "Nothing about me changed.$",
    )),
    "Route117_Text_DerekDefeat": (("ineptitude",), (
        "EUCLIDES: My uselessness is\\n",
        "also unchanged.$",
    )),
    "Route117_Text_DerekPostBattle": (("follow my heart", "expert on BUG"), (
        "EUCLIDES: I only ever did\\n",
        "the thing I liked.\\p",
        "They named me for it.\\p",
        "Fair enough. I do know more\\n",
        "than they do.$",
    )),
    "Route117_Text_AnnaIntro": (("junior student", "do good"), (
        "ANA: My junior student is\\n",
        "watching.\\p",
        "I had better be good.$",
    )),
    "Route117_Text_AnnaDefeat": (("Let me win",), (
        "ANA: Not in front of her.\\n",
        "Let me win this one.$",
    )),
    "Route117_Text_AnnaPostBattle": (("good", "second only to us"), (
        "ANA: Your team fits\\n",
        "together well.\\p",
        "Second best I've seen.\\n",
        "After ours.$",
    )),
    "Route117_Text_AnnaAndMegRegister": (("can't take this lying down",), (
        "ANA: We're not leaving it\\n",
        "there.\\p",
        "You'll come back, won't you.$",
    )),
    "Route117_Text_AnnaNotEnoughMons": (("bring two",), (
        "ANA: Two of us. Bring two.$",
    )),
    "Route117_Text_MegIntro": (("tag up", "beat you"), (
        "DUDA: I'm with my senior\\n",
        "student, and we're going to\\l",
        "beat you.$",
    )),
    "Route117_Text_MegDefeat": (("let you down",), (
        "DUDA: Oh no. ANA, I'm\\n",
        "sorry. That was me.$",
    )),
    "Route117_Text_MegPostBattle": (("dragged ANA down",), (
        "DUDA: I dragged ANA down.\\p",
        "On her own she'd have\\n",
        "won that.$",
    )),
    "Route117_Text_MegNotEnoughMons": (("only have one", "2-on-2"), (
        "DUDA: Only one?\\p",
        "We want a two-on-two.\\n",
        "Come back with two.$",
    )),
    "Route117_Text_AnnaRematchIntro": (("keep losing in front of",), (
        "ANA: I can't keep losing\\n",
        "in front of her.$",
    )),
    "Route117_Text_AnnaRematchDefeat": (("into the groove",), (
        "ANA: I never found my\\n",
        "rhythm.$",
    )),
    "Route117_Text_AnnaPostRematch": (("second only to us",), (
        "ANA: Your team still fits\\n",
        "together.\\p",
        "Second best. After ours.$",
    )),
    "Route117_Text_AnnaRematchNotEnoughMons": (("bring two",), (
        "ANA: Two of us. Still two.$",
    )),
    "Route117_Text_MegRematchIntro": (("win this time",), (
        "DUDA: With my senior\\n",
        "student again.\\p",
        "This time we win.$",
    )),
    "Route117_Text_MegRematchDefeat": (("Too strong",), (
        "DUDA: Too strong.$",
    )),
    "Route117_Text_MegPostRematch": (("discouraging",), (
        "DUDA: We fought together\\n",
        "and lost anyway.\\p",
        "That's hard to carry.$",
    )),
    "Route117_Text_MegRematchNotEnoughMons": (("only have one", "2-on-2"), (
        "DUDA: One again?\\p",
        "Two-on-two, please.$",
    )),
    "Route117_Text_MelinaIntro": (("pretty flowers",), (
        "NAIR: Isn't this a good\\n",
        "place for it?\\p",
        "Flowers the whole way.$",
    )),
    "Route117_Text_MelinaDefeat": (("quite impressive",), (
        "NAIR: Oh, that was rather\\n",
        "good.$",
    )),
    "Route117_Text_MelinaPostBattle": (("go for a jog",), (
        "NAIR: I run this road most\\n",
        "mornings.\\p",
        "It's the flowers. Nothing\\n",
        "else, really.$",
    )),
    "Route117_Text_BrandiIntro": (("power", "hidden within"), (
        "CELIA: Let me show you what\\n",
        "the quiet ones can do.$",
    )),
    "Route117_Text_BrandiDefeat": (("Astonishing",), (
        "CELIA: Astonishing.$",
    )),
    "Route117_Text_BrandiPostBattle": (("complex", "catching some"), (
        "CELIA: The mind ones are\\n",
        "complicated.\\p",
        "Catch one and find out.$",
    )),
    "Route117_Text_AishaIntro": (("Concentrate on getting the win",), (
        "ALICE: Concentrate. Win.\\p",
        "That is the whole method.$",
    )),
    "Route117_Text_AishaDefeat": (("rather train",), (
        "ALICE: I don't stay angry\\n",
        "about a loss.\\p",
        "I'd rather use the time.$",
    )),
    "Route117_Text_AishaPostBattle": (("worry about losing",), (
        "ALICE: Worry about losing\\n",
        "and you'll lose.\\p",
        "It's not superstition.\\n",
        "It's attention.$",
    )),
}


def block_pattern(label: str) -> re.Pattern[str]:
    return re.compile(
        rf"(?ms)^{re.escape(label)}:\n(?P<body>.*?)(?=^[A-Za-z0-9_]+(?:::|:)(?:\n|$)|\Z)"
    )


def visible_segments(payload: str) -> list[str]:
    cleaned = payload.replace("$", "")
    cleaned = cleaned.replace("{PLAYER}", "PLAYERX")
    cleaned = PLACEHOLDER_RE.sub("", cleaned)
    return [part.strip() for part in CONTROL_RE.split(cleaned)]


def validate_widths() -> None:
    for label, (_, payloads) in TARGETS.items():
        for payload in payloads:
            for segment in visible_segments(payload):
                if len(segment) > MAX_VISIBLE_WIDTH:
                    raise ValueError(
                        f"{label}: visible segment is {len(segment)} chars, "
                        f"max {MAX_VISIBLE_WIDTH}: {segment!r}")


def render(source: str) -> str:
    validate_widths()
    rendered = source
    for label, (markers, payloads) in TARGETS.items():
        matches = list(block_pattern(label).finditer(rendered))
        if len(matches) != 1:
            raise ValueError(f"{label}: expected one text block, found {len(matches)}")
        body = matches[0].group("body")
        if ".string" not in body:
            raise ValueError(f"{label}: target contains no .string payload")
        for marker in markers:
            if marker not in body:
                raise ValueError(f"{label}: source marker missing: {marker!r}")
        new_body = "".join(f'\t.string "{payload}"\n' for payload in payloads) + "\n"
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
        masked = masked[:start] + '\t.string "<ARAUNA_CYCLING_DAYCARE_EN>"\n\n' + masked[end:]
    return masked


def validate_rendered(source: str, rendered: str) -> None:
    if mask(source) != mask(rendered):
        raise ValueError("non-dialogue structure changed while rendering")

    forbidden = ("BUG MANIAC", "my pretties", "wondrously lost",
                 "captive audience", "Crash and burn", "Full-throttle")
    for label in TARGETS:
        body = block_pattern(label).search(rendered).group("body")
        for token in forbidden:
            if token in body:
                raise ValueError(f"{label}: vanilla voice survived: {token}")

    # The senior and junior students are a pair, and each has to keep naming
    # the other or the joke of the pairing disappears.
    pair = "".join("".join(payloads) for label, (_, payloads) in TARGETS.items()
                   if "Meg" in label or "Anna" in label)
    if "ANA" not in pair or "senior" not in pair:
        raise ValueError("Route 117 lost the senior and junior student pairing")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Render the Route 110 and Route 117 trainers in English.")
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--in-place", action="store_true")
    args = parser.parse_args()
    if args.check and args.in_place:
        parser.error("use either --check or --in-place")

    source = TRAINERS.read_text(encoding="utf-8")
    rendered = render(source)
    validate_rendered(source, rendered)

    if args.in_place:
        TRAINERS.write_text(rendered, encoding="utf-8")
    print(f"Cycling road and day care trainers English renderer OK: "
          f"{len(TARGETS)} blocks across Routes 110 and 117.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
