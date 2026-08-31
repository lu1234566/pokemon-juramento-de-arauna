#!/usr/bin/env python3
"""The trainers of Routes 111, 112 and 113: the sand, the climb and the ash.

A hundred and twenty-seven blocks along the worst-tempered stretch of road in
the game. Route 111 is the desert, where nobody can see and everyone is wearing
goggles. Route 112 is the climb to Serra da Cinza, where everyone's legs hurt.
Route 113 is the far side, where ash falls all day and people collect it in
sacks.

Weather is the through-line, and each road complains about a different one.
That is the joke the vanilla text was making too; it is only made plainer here.

Two blocks named a creature -- a sandwich thief and a lady with a parasol --
because the species pass put an Arauna name into an Emerald sentence. Those
names are gone: the dex is generated, and a line naming a creature would be
wrong the next time it is.

One collision worth knowing about: the trainer on Route 111 whom the roster
renamed CECILIA shares that name with the leader of Missoes do Ceu. Her lines
here carry no speaker prefix so the two are not confused. Renaming her in
ARAUNA_TRAINER_NAMES.csv would settle it properly.
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
    # -- Route 111, the desert ----------------------------------------------
    "Route111_Text_DrewIntro": (("GO-GOGGLES", "look better"), (
        "FABIO: Those GO-GOGGLES\\n",
        "suit you.\\p",
        "They suit me more.\\n",
        "Let's settle it.$",
    )),
    "Route111_Text_DrewDefeat": (("my sides because",), (
        "FABIO: I couldn't see a\\n",
        "thing at the edges.$",
    )),
    "Route111_Text_DrewPostBattle": (("get through sandstorms",), (
        "FABIO: With these on you\\n",
        "can walk through a\\l",
        "sandstorm.\\p",
        "That still amazes me.$",
    )),
    "Route111_Text_HeidiIntro": (("picnic in the desert",), (
        "FRANCISCA: I'm having a\\n",
        "picnic. In a desert.\\p",
        "There's always someone to\\n",
        "battle, at least.$",
    )),
    "Route111_Text_HeidiDefeat": (("You're mean",), (
        "FRANCISCA: Ohhh! That was\\n",
        "unkind!$",
    )),
    "Route111_Text_HeidiPostBattle": (("watch out", "faint"), (
        "FRANCISCA: In sand like\\n",
        "this, watch their health.\\p",
        "The storm takes it while\\n",
        "you're not looking.$",
    )),
    "Route111_Text_BeauIntro": (("superhero", "nobody can beat me"), (
        "ANIBAL: With the goggles on\\n",
        "I feel unstoppable.\\p",
        "Right now? Nobody.$",
    )),
    "Route111_Text_BeauDefeat": (("spirit alone",), (
        "ANIBAL: Spirit isn't enough\\n",
        "on its own.$",
    )),
    "Route111_Text_BeauPostBattle": (("real hero", "work harder"), (
        "ANIBAL: I'm going to be\\n",
        "someone one day.\\p",
        "We'll both work for it.$",
    )),
    "Route111_Text_BeckyIntro": (("fossils", "Where could they be"), (
        "CARMEM: They say there are\\n",
        "fossils out in this sand.\\p",
        "Where, though?$",
    )),
    "Route111_Text_BeckyDefeat": (("came up short",), (
        "CARMEM: Short again.$",
    )),
    "Route111_Text_BeckyPostBattle": (("must have been a sea",), (
        "CARMEM: If there are\\n",
        "fossils under this sand,\\l",
        "then this was sea once.\\p",
        "All of it. Under water.$",
    )),
    "Route111_Text_DustyIntro": (("thirty years", "ancient ruins"), (
        "FELIPE: Thirty years I've\\n",
        "looked for ruins out here.\\p",
        "And you want to battle?$",
    )),
    "Route111_Text_DustyDefeat": (("not searched for strong",), (
        "FELIPE: I looked for ruins.\\p",
        "I never once looked for a\\n",
        "strong team.$",
    )),
    "Route111_Text_DustyPostBattle": (("was that forty years",), (
        "FELIPE: Thirty years out\\n",
        "here.\\p",
        "No. Forty? Was it forty?$",
    )),
    "Route111_Text_DustyRegister": (("searching for any", "POKéNAVS"), (
        "FELIPE: I've never hunted a\\n",
        "strong team in my life.\\p",
        "I do like a POKéNAV,\\n",
        "though. Odd, that.$",
    )),
    "Route111_Text_DustyRematchIntro": (("am I to be challenged",), (
        "FELIPE: Thirty years. Or\\n",
        "forty. Out here, digging.\\p",
        "Challenging me again?$",
    )),
    "Route111_Text_DustyRematchDefeat": (("found no ruins",), (
        "FELIPE: No ruins, and no\\n",
        "strong team either.$",
    )),
    "Route111_Text_DustyPostRematch": (("even be fifty", "How long have I been"), (
        "FELIPE: Thirty years.\\p",
        "Forty. Fifty, possibly.\\p",
        "How long have I been\\n",
        "standing in this desert?$",
    )),
    "Route111_Text_TravisIntro": (("full of pep",), (
        "XAVIER: I'm full of go\\n",
        "today. So is mine.$",
    )),
    "Route111_Text_TravisDefeat": (("lost its pep",), (
        "XAVIER: All the go has\\n",
        "gone out of us.$",
    )),
    "Route111_Text_TravisPostBattle": (("can't help looking",), (
        "XAVIER: When someone walks\\n",
        "past with that much energy,\\l",
        "I have to stare.$",
    )),
    "Route111_Text_IreneIntro": (("where you're going", "like to battle"), (
        "GISELE: I don't know where\\n",
        "you're headed.\\p",
        "Battle me on the way?$",
    )),
    "Route111_Text_IreneDefeat": (("disgustingly good",), (
        "GISELE: You're horribly\\n",
        "good at this.$",
    )),
    "Route111_Text_IrenePostBattle": (("SERRA DA CINZA", "view around"), (
        "GISELE: I keep meaning to\\n",
        "go up to SERRA DA CINZA.\\p",
        "Then I look around here\\n",
        "and stay another day.$",
    )),
    "Route111_Text_DaisukeIntro": (("challenge all",), (
        "DURVAL: I fight everyone I\\n",
        "meet. That's the training.$",
    )),
    "Route111_Text_DaisukeDefeat": (("I give up",), (
        "DURVAL: Enough! I yield!$",
    )),
    "Route111_Text_DaisukePostBattle": (("keep training", "such"), (
        "DURVAL: All I can do is\\n",
        "keep going until I can\\l",
        "beat people like you.$",
    )),
    "Route111_Text_WiltonIntro": (("how much you've toughened",), (
        "ASSIS: Show me what you've\\n",
        "made of them.$",
    )),
    "Route111_Text_WiltonDefeat": (("toughened them",), (
        "ASSIS: Considerably, then.\\n",
        "I see it.$",
    )),
    "Route111_Text_WiltonPostBattle": (("never give up",), (
        "ASSIS: Both of you learn\\n",
        "from a battle.\\p",
        "What matters is not\\n",
        "stopping after a loss.$",
    )),
    "Route111_Text_WiltonRegister": (("much to be learned", "rematch"), (
        "ASSIS: There's something to\\n",
        "learn in how you train.\\p",
        "A rematch, if you'd allow\\n",
        "it.$",
    )),
    "Route111_Text_WiltonRematchIntro": (("next level", "train with us"), (
        "ASSIS: We're out here\\n",
        "pushing for the next step.\\p",
        "Stay and train with us.$",
    )),
    "Route111_Text_WiltonRematchDefeat": (("you're decent",), (
        "ASSIS: You're better than\\n",
        "decent.$",
    )),
    "Route111_Text_WiltonPostRematch": (("POKéMON LEAGUE",), (
        "ASSIS: At that strength you\\n",
        "should be aiming at the\\l",
        "POKéMON LEAGUE.$",
    )),
    "Route111_Text_BrookeIntro": (("look like serious", "engagement"), (
        "CLARICE: Yours look like\\n",
        "professionals.\\p",
        "I'd like to book you.$",
    )),
    "Route111_Text_BrookeDefeat": (("they are strong",), (
        "CLARICE: They didn't only\\n",
        "look strong.$",
    )),
    "Route111_Text_BrookePostBattle": (("raising my POKéMON", "much to be done"), (
        "CLARICE: I thought I was\\n",
        "raising them carefully.\\p",
        "There's a great deal left\\n",
        "to do.$",
    )),
    "Route111_Text_BrookeRegister": (("become friends", "strong people"), (
        "CLARICE: I'd like to know\\n",
        "more people like you.$",
    )),
    "Route111_Text_BrookeRematchIntro": (("depending on the moves", "What kinds of moves"), (
        "CLARICE: What they know\\n",
        "changes what they are.\\p",
        "What have you taught\\n",
        "yours?$",
    )),
    "Route111_Text_BrookeRematchDefeat": (("taught them good moves",), (
        "CLARICE: You've taught them\\n",
        "well.$",
    )),
    "Route111_Text_BrookePostRematch": (("stopped my", "learned better moves"), (
        "CLARICE: Perhaps I should\\n",
        "have waited before letting\\l",
        "them change.\\p",
        "They'd have learned more\\n",
        "first.$",
    )),
    "Route111_Text_CeliaIntro": (("shouldn't have come", "picnic"), (
        "DAMIANA: A picnic. Here.\\p",
        "What was I thinking.$",
    )),
    "Route111_Text_CeliaDefeat": (("really shouldn't have come",), (
        "DAMIANA: I should not have\\n",
        "come out here at all.$",
    )),
    "Route111_Text_CeliaPostBattle": (("set", "places for a picnic"), (
        "DAMIANA: I can't even lay\\n",
        "the cloth out in this.\\p",
        "The goggles don't help\\n",
        "with sand in the food.$",
    )),
    "Route111_Text_BryanIntro": (("expose that secret",), (
        "BERNARDO: How strong are\\n",
        "you, really?\\p",
        "We'll uncover it.$",
    )),
    "Route111_Text_BryanDefeat": (("shrouded in mystery",), (
        "BERNARDO: Your strength!\\n",
        "It remains a mystery!$",
    )),
    "Route111_Text_BryanPostBattle": (("hoards mysteries",), (
        "BERNARDO: This desert\\n",
        "keeps things.\\p",
        "It moves them around so\\n",
        "you can't find them twice.$",
    )),
    "Route111_Text_BrandenIntro": (("sandwich", "lose"), (
        "AURELIO: I'll split my\\n",
        "sandwich with you.\\p",
        "If you lose.$",
    )),
    "Route111_Text_BrandenDefeat": (("bribe",), (
        "AURELIO: Tch. I thought a\\n",
        "sandwich would do it.$",
    )),
    "Route111_Text_BrandenPostBattle": (("sandwiches",), (
        "AURELIO: Mine eats my\\n",
        "sandwiches. Every day.\\p",
        "I've stopped fighting it.$",
    )),
    "Route111_Text_TyronIntro": (("favorite kind",), (
        "ABILIO: This is my sort.\\n",
        "Exactly my sort.$",
    )),
    "Route111_Text_TyronDefeat": (("good look",), (
        "ABILIO: Wait! Did you even\\n",
        "look at them properly?$",
    )),
    "Route111_Text_TyronPostBattle": (("showing off",), (
        "ABILIO: Half the reason to\\n",
        "battle is showing them to\\l",
        "somebody.\\p",
        "Everyone's the same.$",
    )),
    "Route111_Text_CelinaIntro": (("excitement", "my life"), (
        "DANIELA: Put some\\n",
        "excitement into my day.$",
    )),
    "Route111_Text_CelinaDefeat": (("too much excitement",), (
        "DANIELA: Oh. My.\\p",
        "That was rather too much.$",
    )),
    "Route111_Text_CelinaPostBattle": (("pulse is still racing",), (
        "DANIELA: My heart is still\\n",
        "going.\\p",
        "You're quite something.$",
    )),
    "Route111_Text_HaydenIntro": (("famished", "no room for pity"), (
        "IRINEU: I am too hungry to\\n",
        "go easy on anyone.$",
    )),
    "Route111_Text_HaydenDefeat": (("Groan",), (
        "IRINEU: Ughhh.$",
    )),
    "Route111_Text_HaydenPostBattle": (("stomach is grumbling", "BERRIES"), (
        "IRINEU: My stomach is\\n",
        "making noises.\\p",
        "Maybe I'll grill some\\n",
        "BERRIES over something.$",
    )),
    "Route111_Text_BiancaIntro": (("ENCRUZILHADA", "full of energy"), (
        "Come up from ENCRUZILHADA?\\p",
        "Then you've still got legs\\n",
        "in you. Good.$",
    )),
    "Route111_Text_BiancaDefeat": (("a lot to take",), (
        "That was a lot to take.$",
    )),
    "Route111_Text_BiancaPostBattle": (("quite a ways to travel",), (
        "This road goes a long way.\\p",
        "Further than it looks from\\n",
        "where you're standing.$",
    )),

    # -- Route 112, the climb -----------------------------------------------
    "Route112_Text_BriceIntro": (("Hahahaha", "You and me"), (
        "BENICIO: Hahaha! You and\\n",
        "me! Right here!\\p",
        "Hahahaha!$",
    )),
    "Route112_Text_BriceDefeat": (("I lost",), (
        "BENICIO: Beaten! Hahaha!$",
    )),
    "Route112_Text_BricePostBattle": (("up my nose",), (
        "BENICIO: Hahahaha! Ash!\\n",
        "Up my nose! Hah-tchoo!$",
    )),
    "Route112_Text_TrentIntro": (("legs are solid", "buckle easily"), (
        "ZACARIAS: My legs are solid\\n",
        "from these slopes.\\p",
        "They won't fold, friend.$",
    )),
    "Route112_Text_TrentDefeat": (("legs cramped up",), (
        "ZACARIAS: Ow. Cramp.$",
    )),
    "Route112_Text_TrentPostBattle": (("heavy pack", "serious shape"), (
        "ZACARIAS: Walk these\\n",
        "slopes with a full pack.\\p",
        "Do that for a season and\\n",
        "you'll be a different\\l",
        "shape entirely.$",
    )),
    "Route112_Text_TrentRegister": (("bandages", "that's my POKéNAV"), (
        "ZACARIAS: Cramp again.\\n",
        "Grab the bandages from my\\l",
        "pack, would you?\\p",
        "No, that's the POKéNAV.\\p",
        "Fine. I'll register you.$",
    )),
    "Route112_Text_TrentRematchIntro": (("keeping fit", "Power"), (
        "ZACARIAS: Still walking,\\n",
        "still strong.\\p",
        "Power I have plenty of.$",
    )),
    "Route112_Text_TrentRematchDefeat": (("trumped in power",), (
        "ZACARIAS: Out-muscled?\\n",
        "Me?$",
    )),
    "Route112_Text_TrentRematchPostBattle": (("top of SERRA DA CINZA", "challenge"), (
        "ZACARIAS: They say there\\n",
        "are hard TRAINERS at the\\l",
        "top of SERRA DA CINZA.\\p",
        "I'm going up to find out.$",
    )),
    "Route112_Text_LarryIntro": (("won't cry",), (
        "NILTON: I'm strong. I won't\\n",
        "cry if I lose.$",
    )),
    "Route112_Text_LarryDefeat": (("Waaaah",), (
        "NILTON: Waaaah!$",
    )),
    "Route112_Text_LarryPostBattle": (("miss my mommy",), (
        "NILTON: I'm not crying\\n",
        "about my mother.\\p",
        "Sniff.$",
    )),
    "Route112_Text_CarolIntro": (("sing with me",), (
        "CONSUELO: You cannot picnic\\n",
        "without singing.\\p",
        "Come on. Join in.$",
    )),
    "Route112_Text_CarolDefeat": (("you're so strong",), (
        "CONSUELO: Oh, you're\\n",
        "strong!$",
    )),
    "Route112_Text_CarolPostBattle": (("most fun, you win",), (
        "CONSUELO: Good singer, bad\\n",
        "singer, doesn't matter.\\p",
        "Whoever enjoyed it most\\n",
        "won.$",
    )),
    "Route112_Text_BryantIntro": (("TRILHA DE BRASA",), (
        "BRAULIO: Caught these down\\n",
        "in TRILHA DE BRASA.\\p",
        "Have a look.$",
    )),
    "Route112_Text_BryantDefeat": (("bumpy ride",), (
        "BRAULIO: What a rough ride\\n",
        "that was.$",
    )),
    "Route112_Text_BryantPostBattle": (("certain flair",), (
        "BRAULIO: I like how you\\n",
        "fight.\\p",
        "There's a style to it.$",
    )),
    "Route112_Text_ShaylaIntro": (("adorable TRAINER", "somewhat decent"), (
        "SELMA: What a sweet-looking\\n",
        "TRAINER.\\p",
        "Battle me? I'm better than\\n",
        "I look.$",
    )),
    "Route112_Text_ShaylaDefeat": (("quite a shock",), (
        "SELMA: Oh, you're strong.\\n",
        "What a shock.$",
    )),
    "Route112_Text_ShaylaPostBattle": (("busy right now", "all right if you're busy"), (
        "SELMA: Are you in a hurry?\\p",
        "We could go again now.\\p",
        "Only if you've time,\\n",
        "though.$",
    )),

    # -- Route 113, where the ash falls -------------------------------------
    "Route113_Text_JaylenIntro": (("why it's so cool",), (
        "LEONEL: Guess why it's cool\\n",
        "here and hot everywhere\\l",
        "else.$",
    )),
    "Route113_Text_JaylenDefeat": (("That stinks",), (
        "LEONEL: Pff! That stinks!$",
    )),
    "Route113_Text_JaylenPostBattle": (("blocks the sun", "can't stand heat"), (
        "LEONEL: The ash blocks the\\n",
        "sun. That's the whole\\l",
        "answer.\\p",
        "Suits me. I hate the heat.$",
    )),
    "Route113_Text_DillonIntro": (("earth is alive",), (
        "EURICO: The mountain\\n",
        "erupted.\\p",
        "That's how you know the\\n",
        "ground is still alive.$",
    )),
    "Route113_Text_DillonDefeat": (("some kind of strong",), (
        "EURICO: You're some kind of\\n",
        "strong.$",
    )),
    "Route113_Text_DillonPostBattle": (("eyelashes",), (
        "EURICO: Ow! Ash in my eyes!\\p",
        "In the lashes, even.\\p",
        "Ashes in the lashes.\\p",
        "...I'll stop.$",
    )),
    "Route113_Text_MadelineIntro": (("parasol", "volcanic ash"), (
        "MARIANA: The parasol keeps\\n",
        "the filthy ash off.\\p",
        "Off me, and off mine.$",
    )),
    "Route113_Text_MadelineDefeat": (("I am exhausted",), (
        "MARIANA: Huff. I am worn\\n",
        "through.$",
    )),
    "Route113_Text_MadelinePostBattle": (("I'm impressed",), (
        "MARIANA: You're very good\\n",
        "at this. I'm impressed.$",
    )),
    "Route113_Text_MadelineRegister": (("under my parasol",), (
        "MARIANA: Come in under the\\n",
        "parasol.\\p",
        "Let me take your number.$",
    )),
    "Route113_Text_MadelineRematchIntro": (("hasn't it been a while",), (
        "MARIANA: It's been a while.\\p",
        "Shall we?$",
    )),
    "Route113_Text_MadelineRematchDefeat": (("how super",), (
        "MARIANA: Oh, how splendid.$",
    )),
    "Route113_Text_MadelinePostRematch": (("remained very good",), (
        "MARIANA: Still very good at\\n",
        "this. Still impressed.$",
    )),
    "Route113_Text_LaoIntro": (("out of the ashes",), (
        "NICOLAU: Out of the ash I\\n",
        "come! I challenge thee!$",
    )),
    "Route113_Text_LaoDefeat": (("With honor",), (
        "NICOLAU: I concede, with\\n",
        "honour.$",
    )),
    "Route113_Text_LaoPostBattle": (("art of concealment",), (
        "NICOLAU: My hiding wants\\n",
        "work. I take my leave.$",
    )),
    "Route113_Text_LaoRegister": (("ninja", "POKéNAV registration"), (
        "NICOLAU: Behold! The\\n",
        "ancient art of POKéNAV\\l",
        "registration!$",
    )),
    "Route113_Text_LaoRematchIntro": (("out of the ashes",), (
        "NICOLAU: Out of the ash\\n",
        "again! Face me!$",
    )),
    "Route113_Text_LaoRematchDefeat": (("With honor",), (
        "NICOLAU: Again, with\\n",
        "honour.$",
    )),
    "Route113_Text_LaoPostRematch": (("flawless concealment", "farewell"), (
        "NICOLAU: My hiding was\\n",
        "perfect.\\p",
        "My battling let it down.\\p",
        "I take my leave.$",
    )),
    "Route113_Text_LungIntro": (("Thanks for finding me",), (
        "ORLANDO: You found me!\\p",
        "We still have to battle,\\n",
        "though.$",
    )),
    "Route113_Text_LungDefeat": (("ninjutsu", "already over"), (
        "ORLANDO: Now I use my\\n",
        "secret art! The ASH\\l",
        "CLOAK OF SILENCE!\\p",
        "...It's finished already?$",
    )),
    "Route113_Text_LungPostBattle": (("lonely if no one comes",), (
        "ORLANDO: The trouble with\\n",
        "hiding well.\\p",
        "It's lonely if nobody ever\\n",
        "comes past.$",
    )),
    "Route113_Text_ToriIntro": (("collect ashes",), (
        "TINA: We collect the ash.\\p",
        "We battle as well.$",
    )),
    "Route113_Text_ToriDefeat": (("get some more ashes",), (
        "TINA: Lost. Dull.\\p",
        "I'm going back to the ash.$",
    )),
    "Route113_Text_ToriPostBattle": (("WHITE FLUTE",), (
        "TINA: How much have we\\n",
        "got?\\p",
        "Enough for a WHITE FLUTE,\\n",
        "I hope.$",
    )),
    "Route113_Text_ToriNotEnoughMons": (("2-on-2",), (
        "TINA: Two on two.\\p",
        "Otherwise we lose.$",
    )),
    "Route113_Text_TiaIntro": (("collect ashes",), (
        "MIA: We collect the ash.\\p",
        "We battle as well.$",
    )),
    "Route113_Text_TiaDefeat": (("getting some more ashes",), (
        "MIA: Couldn't win. Dull.\\p",
        "Back to the ash.$",
    )),
    "Route113_Text_TiaPostBattle": (("lot of ashes",), (
        "MIA: We've a lot of it now.\\p",
        "Enough for a WHITE FLUTE,\\n",
        "I think.$",
    )),
    "Route113_Text_TiaNotEnoughMons": (("2-on-2",), (
        "MIA: Two on two.\\p",
        "Otherwise we don't win.$",
    )),
    "Route113_Text_CobyIntro": (("wings", "flick you away"), (
        "DIOGO: One beat of these\\n",
        "wings and you're gone.$",
    )),
    "Route113_Text_CobyDefeat": (("A… What",), (
        "DIOGO: A... what?$",
    )),
    "Route113_Text_CobyPostBattle": (("beaten so easily",), (
        "DIOGO: I don't know what to\\n",
        "say when it goes that\\l",
        "quickly.$",
    )),
    "Route113_Text_SophieIntro": (("drowsy", "stay awake"), (
        "TANIA: The warm air is\\n",
        "making me sleepy.\\p",
        "Battle me so I stay up.$",
    )),
    "Route113_Text_SophieDefeat": (("This is a dream",), (
        "TANIA: This is a dream.\\n",
        "I'm certain of it.$",
    )),
    "Route113_Text_SophiePostBattle": (("sleep right here",), (
        "TANIA: Losing burns.\\p",
        "I'm going to sleep here\\n",
        "instead. Zzz.$",
    )),
    "Route113_Text_LawrenceIntro": (("gathering volcanic ashes",), (
        "NIVALDO: Were you out here\\n",
        "collecting ash as well?$",
    )),
    "Route113_Text_LawrenceDefeat": (("beaten cleanly",), (
        "NIVALDO: Ehehe. Beaten\\n",
        "cleanly.$",
    )),
    "Route113_Text_LawrencePostBattle": (("hide under the ashes",), (
        "NIVALDO: Perhaps I should\\n",
        "bury myself in it too.$",
    )),
    "Route113_Text_WyattIntro": (("just caught",), (
        "AVELINO: Y-you want to\\n",
        "battle me?\\p",
        "I only caught mine an hour\\n",
        "ago.$",
    )),
    "Route113_Text_WyattDefeat": (("happy to win",), (
        "AVELINO: Pleased with\\n",
        "yourself? Beating me?$",
    )),
    "Route113_Text_WyattPostBattle": (("word to", "Humph"), (
        "AVELINO: Oh, now you've a\\n",
        "kind word for the loser.\\p",
        "Aren't you generous.\\n",
        "Humph.$",
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
        masked = masked[:start] + '\t.string "<ARAUNA_DESERT_ASH_EN>"\n\n' + masked[end:]
    return masked


def validate_rendered(source: str, rendered: str) -> None:
    if mask(source) != mask(rendered):
        raise ValueError("non-dialogue structure changed while rendering")

    forbidden = ("Ashes and eyelashes", "romantic battle", "my dear",
                 "Jacarodon", "Bugao", "ninjutsu")
    for label in TARGETS:
        body = block_pattern(label).search(rendered).group("body")
        for token in forbidden:
            if token in body:
                raise ValueError(f"{label}: vanilla voice survived: {token}")

    # The three roads are told apart by what they complain about. If one of
    # those words disappears, a road has stopped having weather.
    joined = {road: "".join("".join(p) for label, (_, p) in TARGETS.items()
                            if label.startswith(road))
              for road in ("Route111", "Route112", "Route113")}
    for road, word in (("Route111", "sand"), ("Route112", "slope"),
                       ("Route113", "ash")):
        if word not in joined[road].lower():
            raise ValueError(f"{road} lost its weather: no mention of {word}")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Render the Route 111, 112 and 113 trainers in English.")
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
    print(f"Desert and ash trainers English renderer OK: {len(TARGETS)} blocks "
          f"across Routes 111, 112 and 113.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
