#!/usr/bin/env python3
"""The trainers of Routes 119, 120 and 121: the rain, the bridge and the road
up to the Memorial dos Nomes.

A hundred and fifty-two blocks, and the longest single stretch of walking in
the game. Route 119 is the wet forest, where six people have formed a society
whose entire purpose is copying strangers. Route 120 continues it past the
standing rock. Route 121 climbs out of the trees toward the Memorial dos Nomes,
and the closer it gets the quieter the trainers become.

That last part is deliberate. On 121 the jokes thin out, the parasol ladies and
the shoppers give way to someone who has come to leave flowers, and the road
starts to sound like where it is going. The renderer holds it to that: the
Memorial has to be named on 121 or the approach has lost its point.

The MIMIC CIRCLE stays a circle -- six people, one bit, all of them committed --
and the senior and junior students stay a pair.

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
    # -- Route 119, the wet forest and the MIMIC CIRCLE ---------------------
    "Route119_Text_BrentIntro": (("MIMIC CIRCLE",), (
        "BENEDITO: The MIMIC CIRCLE.\\p",
        "That's us. We do what\\n",
        "you do.$",
    )),
    "Route119_Text_BrentDefeat": (("Whoopsie",), (
        "BENEDITO: Whoops. Lost.$",
    )),
    "Route119_Text_BrentPostBattle": (("What's so good about mimicry",), (
        "BENEDITO: You want to know\\n",
        "why we copy people.\\p",
        "Hehe. You won't get it\\n",
        "from asking.$",
    )),
    "Route119_Text_DonaldIntro": (("finally meet", "keep you company"), (
        "EVARISTO: At last. We meet.\\p",
        "Mine will keep you\\n",
        "occupied.$",
    )),
    "Route119_Text_DonaldDefeat": (("never met",), (
        "EVARISTO: I wish we hadn't\\n",
        "met.$",
    )),
    "Route119_Text_DonaldPostBattle": (("hurry up and move",), (
        "EVARISTO: I'd like to copy\\n",
        "you some more.\\p",
        "Could you move? Please?$",
    )),
    "Route119_Text_TaylorIntro": (("step forward", "turn right"), (
        "VITOR: Step forward, we\\n",
        "step forward.\\p",
        "Turn right, we turn right.$",
    )),
    "Route119_Text_TaylorDefeat": (("if you win, I lose",), (
        "VITOR: If you win, I lose.\\p",
        "That part doesn't copy.$",
    )),
    "Route119_Text_TaylorPostBattle": (("can't MIMIC you winning",), (
        "VITOR: I can't copy you\\n",
        "winning.\\p",
        "It can't be done, and it's\\n",
        "eating at me.$",
    )),
    "Route119_Text_DougIntro": (("finally caught me", "avoid me"), (
        "EZEQUIEL: You caught up.\\p",
        "Or were you trying to get\\n",
        "past without stopping?$",
    )),
    "Route119_Text_DougDefeat": (("great match",), (
        "EZEQUIEL: Whoop! Good one!$",
    )),
    "Route119_Text_DougPostBattle": (("enjoyed our performance",), (
        "EZEQUIEL: The MIMIC CIRCLE.\\p",
        "We hope you enjoyed the\\n",
        "performance.$",
    )),
    "Route119_Text_GregIntro": (("don't know who I am", "we'll battle"), (
        "IGOR: You've no idea who\\n",
        "I am.\\p",
        "I've no idea who you are.\\n",
        "So we battle.$",
    )),
    "Route119_Text_GregDefeat": (("pretty strong",), (
        "IGOR: You're strong.$",
    )),
    "Route119_Text_GregPostBattle": (("keep on mimicking",), (
        "IGOR: Until you walk out of\\n",
        "sight, we copy everything\\l",
        "you do.$",
    )),
    "Route119_Text_KentIntro": (("formed by people", "instant we meet"), (
        "MOISES: The CIRCLE is\\n",
        "people who like to copy.\\p",
        "Meeting one of us starts a\\n",
        "battle. Immediately.$",
    )),
    "Route119_Text_KentDefeat": (("I give up",), (
        "MOISES: I yield.$",
    )),
    "Route119_Text_KentPostBattle": (("join our MIMIC CIRCLE",), (
        "MOISES: Would you like to\\n",
        "join the MIMIC CIRCLE?\\p",
        "Think about it.$",
    )),
    "Route119_Text_JacksonIntro": (("knowledge", "RANGERS"), (
        "JUSTINO: Who knows how to\\n",
        "survive out here?\\p",
        "RANGERS. That's who.$",
    )),
    "Route119_Text_JacksonDefeat": (("know-how",), (
        "JUSTINO: I didn't know\\n",
        "enough.$",
    )),
    "Route119_Text_JacksonPostBattle": (("break away from civilization", "vision"), (
        "JUSTINO: Get far enough\\n",
        "from town and something\\l",
        "wakes up in you.\\p",
        "That's what we're for.$",
    )),
    "Route119_Text_JacksonRegister": (("without", "lack of knowledge"), (
        "JUSTINO: Rematch me\\n",
        "sometime.\\p",
        "Without holding my\\n",
        "ignorance against me.$",
    )),
    "Route119_Text_JacksonRematchIntro": (("regain my wild spirit",), (
        "JUSTINO: I'm out here to\\n",
        "get that back.\\p",
        "Them beside me, and no\\n",
        "roof.$",
    )),
    "Route119_Text_JacksonRematchDefeat": (("remained strong",), (
        "JUSTINO: Still strong.$",
    )),
    "Route119_Text_JacksonPostRematch": (("Believe in yourself", "road will reveal"), (
        "JUSTINO: Trust them.\\n",
        "Trust yourself.\\p",
        "The road shows itself to\\n",
        "people who keep walking.$",
    )),
    "Route119_Text_CatherineIntro": (("traveling awfully light",), (
        "DALILA: Look at you.\\p",
        "Travelling this light, on\\n",
        "a road like this.$",
    )),
    "Route119_Text_CatherineDefeat": (("Accidents happen",), (
        "DALILA: Things go wrong\\n",
        "for the unprepared!$",
    )),
    "Route119_Text_CatherinePostBattle": (("everything you need", "physically"), (
        "DALILA: Light, but you have\\n",
        "everything.\\p",
        "You've thought about this\\n",
        "properly. Both halves of\\l",
        "it.$",
    )),
    "Route119_Text_CatherineRegister": (("POKéNAV", "register each other"), (
        "DALILA: Do you carry a\\n",
        "POKéNAV?\\p",
        "You do. Good. Numbers,\\n",
        "then.$",
    )),
    "Route119_Text_CatherineRematchIntro": (("How's your journey",), (
        "DALILA: How's the road\\n",
        "treating you?$",
    )),
    "Route119_Text_CatherineRematchDefeat": (("still missing something",), (
        "DALILA: Something is still\\n",
        "missing from mine.$",
    )),
    "Route119_Text_CatherinePostRematch": (("rely on you",), (
        "DALILA: You lean on them.\\p",
        "They lean on you exactly\\n",
        "as hard. Don't forget the\\l",
        "second part.$",
    )),
    "Route119_Text_HughIntro": (("vast sky", "exhilaration of flight"), (
        "JOAQUIM: All that sky, and\\n",
        "nobody using it.\\p",
        "Nothing compares to being\\n",
        "up there.$",
    )),
    "Route119_Text_HughDefeat": (("Down and out",), (
        "JOAQUIM: Down. Out.$",
    )),
    "Route119_Text_HughPostBattle": (("dreams of", "come true"), (
        "JOAQUIM: I wanted to fly\\n",
        "since I was small.\\p",
        "Mine got me up there.$",
    )),
    "Route119_Text_PhilIntro": (("true potential",), (
        "ROMEU: Watch what we can\\n",
        "actually do.$",
    )),
    "Route119_Text_PhilDefeat": (("lacked potential",), (
        "ROMEU: Not as much as I\\n",
        "thought, then.$",
    )),
    "Route119_Text_PhilPostBattle": (("little kid", "admired"), (
        "ROMEU: I've watched the\\n",
        "ones with wings since I\\l",
        "was small.\\p",
        "Never got over it.$",
    )),
    "Route119_Text_YasuIntro": (("lurk in shadows", "destiny"), (
        "BELMIRO: I keep to the\\n",
        "shadow. It suits me.\\p",
        "I've come out for you.$",
    )),
    "Route119_Text_YasuDefeat": (("I admit defeat",), (
        "BELMIRO: I concede.$",
    )),
    "Route119_Text_YasuPostBattle": (("withdraw", "That, too, is destiny"), (
        "BELMIRO: The beaten go back\\n",
        "into the shadow quietly.\\p",
        "That's part of it as well.$",
    )),
    "Route119_Text_TakashiIntro": (("on your guard", "some pain"), (
        "VIRGILIO: Drop your guard\\n",
        "out here and it will hurt.$",
    )),
    "Route119_Text_TakashiDefeat": (("surprisingly good",), (
        "VIRGILIO: You're better\\n",
        "than you look.$",
    )),
    "Route119_Text_TakashiPostBattle": (("surprise attack",), (
        "VIRGILIO: My ambush did not\\n",
        "go to plan.$",
    )),
    "Route119_Text_HideoIntro": (("hide a tree, use a forest",), (
        "IVO: To hide a tree, use a\\n",
        "forest.$",
    )),
    "Route119_Text_HideoDefeat": (("bow to your superiority",), (
        "IVO: I bow to you.$",
    )),
    "Route119_Text_HideoPostBattle": (("no deep, hidden meaning",), (
        "IVO: To hide a tree, use a\\n",
        "forest.\\p",
        "To hide one of them, use\\n",
        "another.\\p",
        "There's no deeper meaning.\\n",
        "That's all it is.$",
    )),
    "Route119_Text_ChrisIntro": (("You spoke to me", "SURFING"), (
        "DANILO: You spoke first.\\p",
        "That's a challenge.\\p",
        "I'll use what I caught out\\n",
        "on the water.$",
    )),
    "Route119_Text_ChrisDefeat": (("what it", "takes to win"), (
        "DANILO: I've no idea what\\n",
        "winning takes.$",
    )),
    "Route119_Text_ChrisPostBattle": (("fish off its back", "luxuriant"), (
        "DANILO: Ride out on one of\\n",
        "them.\\p",
        "Then fish from its back.\\p",
        "There is nothing better\\n",
        "anywhere.$",
    )),
    "Route119_Text_FabianIntro": (("power chord", "time to shine"), (
        "GUSTAVO: Hit me with a\\n",
        "chord!\\p",
        "This is our hour! Whoa!$",
    )),
    "Route119_Text_FabianDefeat": (("who's the boss", "take the loss"), (
        "GUSTAVO: You showed me the\\n",
        "boss!\\p",
        "Now we take the loss!$",
    )),
    "Route119_Text_FabianPostBattle": (("another power chord", "atone"), (
        "GUSTAVO: One more chord!\\p",
        "Then leave me be!\\n",
        "Your win's on you, not me!$",
    )),
    "Route119_Text_DaytonIntro": (("kid TRAINERS", "good one"), (
        "EMILIO: Hohoho! I do like a\\n",
        "young TRAINER.\\p",
        "Let's have a good one.$",
    )),
    "Route119_Text_DaytonDefeat": (("pretty amazing",), (
        "EMILIO: You're something.\\n",
        "Hohoho!$",
    )),
    "Route119_Text_DaytonPostBattle": (("emulating the pep",), (
        "EMILIO: Hohoho. I'll try to\\n",
        "borrow some of that\\l",
        "energy of yours.$",
    )),
    "Route119_Text_RachelIntro": (("parasol in hand",), (
        "PAULA: Wherever I am, this\\n",
        "parasol is with me.$",
    )),
    "Route119_Text_RachelDefeat": (("not fair",), (
        "PAULA: Oh. But that isn't\\n",
        "fair.$",
    )),
    "Route119_Text_RachelPostBattle": (("BAG is filled",), (
        "PAULA: Is the parasol\\n",
        "heavy, you ask.\\p",
        "Your BAG has more in it\\n",
        "than I have carried in my\\l",
        "life.$",
    )),

    # -- Route 120, on past the standing rock -------------------------------
    "Route120_Text_ColinIntro": (("strike", "flying"), (
        "DJALMA: Do you carry\\n",
        "anything that can reach\\l",
        "something in the air?$",
    )),
    "Route120_Text_ColinDefeat": (("soared above me",), (
        "DJALMA: You went straight\\n",
        "over me.$",
    )),
    "Route120_Text_ColinPostBattle": (("almost no moves",), (
        "DJALMA: While they're up\\n",
        "there, almost nothing can\\l",
        "touch them.\\p",
        "Convenient, isn't it.$",
    )),
    "Route120_Text_RobertIntro": (("How about yours",), (
        "SILVIO: Mine are strong.\\p",
        "And yours?$",
    )),
    "Route120_Text_RobertDefeat": (("were stronger",), (
        "SILVIO: Yours were\\n",
        "stronger.$",
    )),
    "Route120_Text_RobertPostBattle": (("grows steadily", "count on"), (
        "SILVIO: One that improves a\\n",
        "little every week is one\\l",
        "you can rely on.$",
    )),
    "Route120_Text_RobertRegister": (("counted on to get better",), (
        "SILVIO: You'll keep\\n",
        "improving. I can tell.\\p",
        "Let me have your number.$",
    )),
    "Route120_Text_RobertRematchIntro": (("grows steadily", "count on"), (
        "SILVIO: Steady improvement.\\p",
        "That's the only kind worth\\n",
        "having.$",
    )),
    "Route120_Text_RobertRematchDefeat": (("seriously strong",), (
        "SILVIO: Yours are seriously\\n",
        "strong.$",
    )),
    "Route120_Text_RobertPostRematch": (("I have to grow stronger",), (
        "SILVIO: Mine keep getting\\n",
        "stronger.\\p",
        "I have to keep up with\\n",
        "them.$",
    )),
    "Route120_Text_LorenzoIntro": (("fit for the outdoors",), (
        "OLEGARIO: Let me see if\\n",
        "yours could survive a\\l",
        "night out here.$",
    )),
    "Route120_Text_LorenzoDefeat": (("no danger of needing rescue",), (
        "OLEGARIO: With those, you\\n",
        "will never need rescuing.$",
    )),
    "Route120_Text_LorenzoPostBattle": (("wherever your heart", "joy of being"), (
        "OLEGARIO: Going wherever\\n",
        "you like, with them.\\p",
        "That's the whole point of\\n",
        "this.$",
    )),
    "Route120_Text_JennaIntro": (("physical fitness", "critical situations"), (
        "ISABEL: How fit are you,\\n",
        "actually?\\p",
        "It matters more than you\\n",
        "think when things go bad.$",
    )),
    "Route120_Text_JennaDefeat": (("totally fit",), (
        "ISABEL: I'm perfectly fit.\\n",
        "And yet.$",
    )),
    "Route120_Text_JennaPostBattle": (("run with my POKéMON",), (
        "ISABEL: I run every\\n",
        "morning, and they run\\l",
        "with me.$",
    )),
    "Route120_Text_JeffreyIntro": (("Want to battle",), (
        "LIVIO: ... ... ...\\p",
        "... ... ...\\p",
        "Battle?$",
    )),
    "Route120_Text_JeffreyDefeat": (("Lost it",), (
        "LIVIO: ...Lost.$",
    )),
    "Route120_Text_JeffreyPostBattle": (("try harder",), (
        "LIVIO: ... ... ...\\p",
        "I'll do better.$",
    )),
    "Route120_Text_JeffreyRegister": (("Do you have a POKéNAV",), (
        "LIVIO: ... ... ...\\p",
        "Do you have a POKéNAV...?$",
    )),
    "Route120_Text_JeffreyRematchIntro": (("battle again",), (
        "LIVIO: ... ... ...\\p",
        "Again?$",
    )),
    "Route120_Text_JeffreyRematchDefeat": (("lost again",), (
        "LIVIO: ...Lost again.$",
    )),
    "Route120_Text_JeffreyPostRematch": (("precious BUG",), (
        "LIVIO: ... ... ...\\p",
        "I'll do better.\\p",
        "For the small ones.\\n",
        "They deserve better.$",
    )),
    "Route120_Text_JenniferIntro": (("special abilities", "first-class"), (
        "ISADORA: They each have\\n",
        "something they can do.\\p",
        "Learn those and you'll be\\n",
        "a proper TRAINER.$",
    )),
    "Route120_Text_JenniferDefeat": (("obviously thinking",), (
        "ISADORA: You're clearly\\n",
        "thinking about it.$",
    )),
    "Route120_Text_JenniferPostBattle": (("battle styles change",), (
        "ISADORA: What each one can\\n",
        "do changes how the whole\\l",
        "battle goes.$",
    )),
    "Route120_Text_ChipIntro": (("ancient", "ruins"), (
        "CRISTIANO: And who might\\n",
        "you be?\\p",
        "Are you hunting the ruins\\n",
        "that supposedly exist\\l",
        "somewhere near here?$",
    )),
    "Route120_Text_ChipDefeat": (("disgraceful setback",), (
        "CRISTIANO: A disgraceful\\n",
        "setback.$",
    )),
    "Route120_Text_ChipPostBattle": (("giant rock", "no entrance"), (
        "CRISTIANO: That enormous\\n",
        "stone.\\p",
        "I'm certain there's\\n",
        "something inside it.\\p",
        "I cannot find the way in.$",
    )),
    "Route120_Text_ClarissaIntro": (("carrying this parasol", "win against me"), (
        "DENISE: Why do I carry a\\n",
        "parasol?\\p",
        "Beat me and I'll tell you.$",
    )),
    "Route120_Text_ClarissaDefeat": (("ward off",), (
        "DENISE: A parasol turns out\\n",
        "to stop nothing at all.$",
    )),
    "Route120_Text_ClarissaPostBattle": (("strong sunlight", "shield them"), (
        "DENISE: Hard sun isn't good\\n",
        "for mine.\\p",
        "So I hold this over them.\\n",
        "That's the whole answer.$",
    )),
    "Route120_Text_AngelicaIntro": (("picture of beauty",), (
        "BENEDITA: Me, mine, and the\\n",
        "parasol.\\p",
        "Take one away and the\\n",
        "picture is spoiled.$",
    )),
    "Route120_Text_AngelicaDefeat": (("ruined my beauty",), (
        "BENEDITA: You have spoiled\\n",
        "the whole picture.$",
    )),
    "Route120_Text_AngelicaPostBattle": (("wouldn't suit you", "in your way"), (
        "BENEDITA: A parasol would\\n",
        "not suit you.\\p",
        "It would only get in your\\n",
        "way, and you have places\\l",
        "to be.$",
    )),
    "Route120_Text_KeigoIntro": (("new ninja techniques",), (
        "MILTON: I'm building new\\n",
        "techniques from how they\\l",
        "move.$",
    )),
    "Route120_Text_KeigoDefeat": (("distant dream",), (
        "MILTON: New techniques\\n",
        "remain a distant idea.$",
    )),
    "Route120_Text_KeigoPostBattle": (("apprentice under",), (
        "MILTON: Perhaps I should\\n",
        "find someone to teach me\\l",
        "properly.$",
    )),
    "Route120_Text_RileyIntro": (("camouflage cloaks", "didn't know where I was"), (
        "SILVERIO: We hide under\\n",
        "cloaks that match the\\l",
        "ground.\\p",
        "You had no idea, did you.$",
    )),
    "Route120_Text_RileyDefeat": (("camouflage my shame",), (
        "SILVERIO: Beaten! I'd like\\n",
        "to hide the shame as well!$",
    )),
    "Route120_Text_RileyPostBattle": (("handmade",), (
        "SILVERIO: We sew the cloaks\\n",
        "ourselves.\\p",
        "Every one of them.$",
    )),
    "Route120_Text_CallieIntro": (("pay attention", "get hurt"), (
        "CLAUDIA: Pay attention out\\n",
        "here or you'll be hurt.$",
    )),
    "Route120_Text_CallieDefeat": (("one to get hurt",), (
        "CLAUDIA: Ouch. I was the\\n",
        "one who got hurt.$",
    )),
    "Route120_Text_CalliePostBattle": (("Should I evolve", "cute the way they are"), (
        "CLAUDIA: Should I let them\\n",
        "change?\\p",
        "They're lovely as they are.\\n",
        "I keep putting it off.$",
    )),
    "Route120_Text_LeonelIntro": (("different types",), (
        "ODILON: Your team. Is it\\n",
        "all one sort?$",
    )),
    "Route120_Text_LeonelDefeat": (("policy in action",), (
        "ODILON: I've seen how you\\n",
        "do it now.$",
    )),
    "Route120_Text_LeonelPostBattle": (("favorite POKéMON",), (
        "ODILON: You're strong\\n",
        "fighting with the ones you\\l",
        "actually like.\\p",
        "That's the good way to be\\n",
        "strong.$",
    )),

    # -- Route 121, the climb to the Memorial dos Nomes ---------------------
    "Route121_Text_VanessaIntro": (("delightfully",), (
        "WILMA: Come and meet mine.\\p",
        "They're lovely. Truly.$",
    )),
    "Route121_Text_VanessaDefeat": (("isn't what I meant",), (
        "WILMA: That is not what I\\n",
        "meant by meet them.$",
    )),
    "Route121_Text_VanessaPostBattle": (("CONTEST", "MASTER CLASS"), (
        "WILMA: I'm taking them to\\n",
        "a CONTEST in BAIA DAS\\l",
        "LUZES.\\p",
        "They'll walk the MASTER\\n",
        "CLASS.$",
    )),
    "Route121_Text_WalterIntro": (("four corners", "confidence"), (
        "AMERICO: I've taken mine to\\n",
        "the far ends of the world.\\p",
        "I have some confidence in\\n",
        "what we do.$",
    )),
    "Route121_Text_WalterDefeat": (("well played",), (
        "AMERICO: Ah. Well played.$",
    )),
    "Route121_Text_WalterPostBattle": (("circle the globe",), (
        "AMERICO: I'd go round the\\n",
        "whole world again with\\l",
        "them tomorrow.$",
    )),
    "Route121_Text_WalterRegister": (("remarkable", "as a memento"), (
        "AMERICO: What you do is\\n",
        "remarkable.\\p",
        "Let me keep your number,\\n",
        "as a memento.$",
    )),
    "Route121_Text_WalterRematchIntro": (("four corners", "confidence"), (
        "AMERICO: The far ends of\\n",
        "the world, with these.\\p",
        "Some confidence is\\n",
        "warranted.$",
    )),
    "Route121_Text_WalterRematchDefeat": (("well played",), (
        "AMERICO: Ah. Well played\\n",
        "again.$",
    )),
    "Route121_Text_WalterPostRematch": (("even overseas",), (
        "AMERICO: You and yours.\\p",
        "They'd think you strong on\\n",
        "any coast, in any country.$",
    )),
    "Route121_Text_TammyIntro": (("powers beyond our",), (
        "THAIS: There are things\\n",
        "working in this world that\\l",
        "we do not understand.$",
    )),
    "Route121_Text_TammyDefeat": (("I have lost",), (
        "THAIS: I have lost.$",
    )),
    "Route121_Text_TammyPostBattle": (("MEMORIAL DOS NOMES", "mysterious power"), (
        "THAIS: Up there, at the\\n",
        "MEMORIAL DOS NOMES.\\p",
        "Something is at work in\\n",
        "that place.\\p",
        "Go quietly when you go.$",
    )),
    "Route121_Text_KateIntro": (("Together, we're fearless",), (
        "NEIA: Together we're not\\n",
        "afraid of anything.\\p",
        "Watch.$",
    )),
    "Route121_Text_KateDefeat": (("blew it in front of",), (
        "NEIA: In front of my junior\\n",
        "student, as well.$",
    )),
    "Route121_Text_KatePostBattle": (("look cool in front",), (
        "NEIA: When someone is\\n",
        "counting on me I want to\\l",
        "look like I deserve it.$",
    )),
    "Route121_Text_KateNotEnoughMons": (("only got one", "bullying"), (
        "NEIA: One, against two of\\n",
        "us?\\p",
        "That wouldn't be a battle.\\n",
        "It would be bullying.$",
    )),
    "Route121_Text_JoyIntro": (("Together, we're fearless",), (
        "LU: Together we're not\\n",
        "afraid of anything!$",
    )),
    "Route121_Text_JoyDefeat": (("forgive me",), (
        "LU: Forgive me, NEIA!$",
    )),
    "Route121_Text_JoyPostBattle": (("train with", "senior student"), (
        "LU: I'll go and train with\\n",
        "NEIA again.\\p",
        "She's the one who taught\\n",
        "me all of it.$",
    )),
    "Route121_Text_JoyNotEnoughMons": (("at least two",), (
        "LU: Two, at minimum, if\\n",
        "you're taking us on!$",
    )),
    "Route121_Text_JessicaIntro": (("Have a good look",), (
        "IVONE: Stop. Look at mine\\n",
        "properly.$",
    )),
    "Route121_Text_JessicaDefeat": (("how dare you", "so seriously"), (
        "IVONE: How dare you.\\p",
        "You didn't have to take it\\n",
        "that seriously.$",
    )),
    "Route121_Text_JessicaPostBattle": (("catch more POKéMON",), (
        "IVONE: Perhaps I'll go and\\n",
        "catch more at the RESERVA\\l",
        "ARAUNA.$",
    )),
    "Route121_Text_JessicaRegister": (("took it easy",), (
        "IVONE: I went easy on you\\n",
        "this time.\\p",
        "Not next time.$",
    )),
    "Route121_Text_JessicaRematchIntro": (("grew", "good look"), (
        "IVONE: Mine have grown.\\p",
        "Look at them properly.$",
    )),
    "Route121_Text_JessicaRematchDefeat": (("still won't take it easy",), (
        "IVONE: How dare you.\\p",
        "You still won't go easy on\\n",
        "me.$",
    )),
    "Route121_Text_JessicaPostRematch": (("catch more POKéMON",), (
        "IVONE: The RESERVA ARAUNA,\\n",
        "then. More of them.$",
    )),
    "Route121_Text_CristinIntro": (("five TRAINERS a day",), (
        "DORA: I beat five TRAINERS\\n",
        "a day. It's a routine.\\p",
        "You're the fifth.$",
    )),
    "Route121_Text_CristinDefeat": (("You're horrid",), (
        "DORA: No! You're horrid!$",
    )),
    "Route121_Text_CristinPostBattle": (("this easily", "win next time"), (
        "DORA: I did not expect to\\n",
        "lose that quickly.\\p",
        "Next time.$",
    )),
    "Route121_Text_CristinRegister": (("total humiliation", "Hand over"), (
        "DORA: That was humiliating.\\p",
        "I won't forget you.\\n",
        "Give me that POKéNAV.$",
    )),
    "Route121_Text_CristinRematchIntro": (("ten TRAINERS a day",), (
        "DORA: New routine. Ten a\\n",
        "day.\\p",
        "You're the tenth.$",
    )),
    "Route121_Text_CristinRematchDefeat": (("demand a rematch",), (
        "DORA: That's nasty!\\n",
        "I demand another!$",
    )),
    "Route121_Text_CristinPostRematch": (("can't beat", "Snivel"), (
        "DORA: Someone I simply\\n",
        "cannot beat.\\p",
        "Sniff. I don't accept it.$",
    )),
    "Route121_Text_CaleIntro": (("all this", "insist that"), (
        "BRUNO: Can you not see how\\n",
        "much I'm carrying?\\p",
        "And you still want a\\n",
        "battle?$",
    )),
    "Route121_Text_CaleDefeat": (("both hands",), (
        "BRUNO: Of course I lost.\\n",
        "My hands are full!$",
    )),
    "Route121_Text_CalePostBattle": (("DEPT. STORE", "BAG like yours"), (
        "BRUNO: I bought far too\\n",
        "much at the BAIA DAS LUZES\\l",
        "DEPT. STORE.\\p",
        "It's just up the road.\\p",
        "I wish I had a BAG like\\n",
        "yours.$",
    )),
    "Route121_Text_MylesIntro": (("other people's POKéMON",), (
        "PLINIO: There's nothing I\\n",
        "like more than looking at\\l",
        "other people's.$",
    )),
    "Route121_Text_MylesDefeat": (("Super awesome",), (
        "PLINIO: Marvellous!$",
    )),
    "Route121_Text_MylesPostBattle": (("How do you raise them",), (
        "PLINIO: Yours are\\n",
        "wonderful.\\p",
        "How do you raise them?$",
    )),
    "Route121_Text_PatIntro": (("everybody to see",), (
        "OLGA: I want everyone to\\n",
        "see what I've raised.$",
    )),
    "Route121_Text_PatDefeat": (("Spectacular",), (
        "OLGA: Wow. Spectacular.$",
    )),
    "Route121_Text_PatPostBattle": (("pick favorites",), (
        "OLGA: Every one of them\\n",
        "gets the same care.\\p",
        "I don't keep favourites.$",
    )),
    "Route121_Text_MarcelIntro": (("never tasted defeat", "CONTESTS"), (
        "OSVALDO: Mine have never\\n",
        "lost.\\p",
        "One more win and they go\\n",
        "into CONTESTS.$",
    )),
    "Route121_Text_MarcelDefeat": (("now what happened",), (
        "OSVALDO: Well. What\\n",
        "happened there.$",
    )),
    "Route121_Text_MarcelPostBattle": (("train my gang",), (
        "OSVALDO: More training\\n",
        "before any CONTEST, then.$",
    )),
}


def block_pattern(label: str) -> re.Pattern[str]:
    return re.compile(
        rf"(?ms)^{re.escape(label)}:\n(?P<body>.*?)(?=^[A-Za-z0-9_]+(?:::|:)(?:\n|$)|\Z)"
    )


def visible_segments(payload: str) -> list[str]:
    cleaned = payload.replace("$", "").replace("{PLAYER}", "PLAYERX")
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
        masked = masked[:start] + '\t.string "<ARAUNA_FOREST_MEMORIAL_EN>"\n\n' + masked[end:]
    return masked


def validate_rendered(source: str, rendered: str) -> None:
    if mask(source) != mask(rendered):
        raise ValueError("non-dialogue structure changed while rendering")

    forbidden = ("wild spirit within", "picture of beauty", "Hohoho!\\nI like",
                 "sweeping the MASTER", "Snivel")
    for label in TARGETS:
        body = block_pattern(label).search(rendered).group("body")
        for token in forbidden:
            if token in body:
                raise ValueError(f"{label}: vanilla voice survived: {token}")

    # Route 121 is an approach to somewhere. If the Memorial stops being named
    # on it, the road is just another road.
    climb = "".join("".join(p) for label, (_, p) in TARGETS.items()
                    if label.startswith("Route121"))
    if "MEMORIAL DOS NOMES" not in climb:
        raise ValueError("Route 121 no longer names what it climbs toward")

    # Six people, one bit. The CIRCLE has to still be a circle.
    circle = "".join("".join(p) for label, (_, p) in TARGETS.items()
                     if label.startswith("Route119"))
    if circle.count("MIMIC CIRCLE") < 3:
        raise ValueError("the MIMIC CIRCLE stopped introducing itself")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Render the Route 119, 120 and 121 trainers in English.")
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
    print(f"Forest and memorial trainers English renderer OK: {len(TARGETS)} "
          f"blocks across Routes 119, 120 and 121.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
