#!/usr/bin/env python3
"""The trainers of Routes 125 to 129: the eastern sea.

A hundred and thirty-two blocks on the water that runs from the Gruta da Mare
past the white rock of Aguas de M'Boi and out toward Estr. Juramento. This is
the last long swim before the league, and the people on it know it -- half of
them mention where they are going, and several are only out here because they
are on their way there.

That is the through-line, and the renderer holds it: Route 128 has to keep
naming Estr. Juramento, because everyone on it is pointed at the same place.

One block had ended up naming a creature, from the species pass dropping an
Arauna name into an Emerald sentence. It is gone; the dex is generated, so no
payload names a species.

LIS and IRIS stay a pair, still arguing about whether they are actually going
into the cave.
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
    # -- Route 125, the water outside the Gruta da Mare ---------------------
    "Route125_Text_NolenIntro": (("heard you approaching",), (
        "REMIGIO: I heard you coming\\n",
        "and waited.$",
    )),
    "Route125_Text_NolenDefeat": (("I surrender",), (
        "REMIGIO: I surrender.$",
    )),
    "Route125_Text_NolenPostBattle": (("Sound travels faster",), (
        "REMIGIO: Sound moves\\n",
        "faster through water than\\l",
        "through air.\\p",
        "That's how I heard you.$",
    )),
    "Route125_Text_StanIntro": (("sweet POKéMON",), (
        "VALENTIM: Hey! Come and\\n",
        "look at mine!$",
    )),
    "Route125_Text_StanDefeat": (("floundered",), (
        "VALENTIM: I floundered.$",
    )),
    "Route125_Text_StanPostBattle": (("started swimming",), (
        "VALENTIM: I only took up\\n",
        "swimming because of one\\l",
        "of them.\\p",
        "Followed it out here and\\n",
        "never went back.$",
    )),
    "Route125_Text_TanyaIntro": (("tired of swimming",), (
        "VALDIRENE: I'm tired of\\n",
        "swimming.\\p",
        "Battle instead?$",
    )),
    "Route125_Text_TanyaDefeat": (("too much",), (
        "VALDIRENE: You're far too\\n",
        "much.$",
    )),
    "Route125_Text_TanyaPostBattle": (("MISSOES DO CEU",), (
        "VALDIRENE: Whew.\\p",
        "Which way is MISSOES DO\\n",
        "CEU from here?$",
    )),
    "Route125_Text_SharonIntro": (("WATER-type", "I raised"), (
        "SANDRA: These came out of\\n",
        "this water and I raised\\l",
        "them myself.\\p",
        "Care to try them?$",
    )),
    "Route125_Text_SharonDefeat": (("Lost it",), (
        "SANDRA: Lost it.$",
    )),
    "Route125_Text_SharonPostBattle": (("real deal",), (
        "SANDRA: You're the real\\n",
        "thing. I'm amazed.$",
    )),
    "Route125_Text_ErnestIntro": (("SAILOR", "braved the world's seas"), (
        "GILSON: Ahoy! I've sailed\\n",
        "every sea worth sailing!$",
    )),
    "Route125_Text_ErnestDefeat": (("couldn't win",), (
        "GILSON: Gwroar! Beaten!$",
    )),
    "Route125_Text_ErnestPostBattle": (("GRUTA DA MARE", "six hours"), (
        "GILSON: The GRUTA DA MARE\\n",
        "fills and empties.\\p",
        "Six hours from full to\\n",
        "empty. Remember that.$",
    )),
    "Route125_Text_ErnestRegister": (("something good",), (
        "GILSON: Put me in your\\n",
        "POKéNAV and I'll tell you\\l",
        "something worth knowing.$",
    )),
    "Route125_Text_ErnestRematchIntro": (("payback",), (
        "GILSON: Time I had my own\\n",
        "back. Come on.$",
    )),
    "Route125_Text_ErnestRematchDefeat": (("flat out couldn't win",), (
        "GILSON: Couldn't win.\\n",
        "Flatly couldn't win.$",
    )),
    "Route125_Text_ErnestRematchPostBattle": (("rise and fall", "Don't forget"), (
        "GILSON: In the GRUTA DA\\n",
        "MARE, the water decides\\l",
        "where you can walk.\\p",
        "Six hours from full to\\n",
        "empty. Don't forget it.$",
    )),
    "Route125_Text_KimIntro": (("funny old man", "GRUTA DA MARE"), (
        "LIS: They say an odd old\\n",
        "man lives in the GRUTA DA\\l",
        "MARE.\\p",
        "Are you going to see him\\n",
        "as well?$",
    )),
    "Route125_Text_KimDefeat": (("thought we would win",), (
        "LIS: I thought we had that.$",
    )),
    "Route125_Text_KimPostBattle": (("Let's go see him",), (
        "LIS: There really is an old\\n",
        "man in there, isn't there.\\p",
        "Come on, IRIS. Let's go.$",
    )),
    "Route125_Text_KimNotEnoughMons": (("need two",), (
        "LIS: No, no. Two of them,\\n",
        "or it doesn't work.$",
    )),
    "Route125_Text_IrisIntro": (("what we're", "looking for"), (
        "IRIS: LIS. What exactly are\\n",
        "we looking for out here?$",
    )),
    "Route125_Text_IrisDefeat": (("sort of close",), (
        "IRIS: We came fairly close.$",
    )),
    "Route125_Text_IrisPostBattle": (("really going into", "all wet"), (
        "IRIS: LIS, are we actually\\n",
        "going inside?\\p",
        "We'll be soaked through.$",
    )),
    "Route125_Text_IrisNotEnoughMons": (("2-on-1",), (
        "IRIS: Two of us against one\\n",
        "of yours? We couldn't.$",
    )),
    "Route125_Text_PresleyIntro": (("BIRDKEEPER", "out to the sea"), (
        "RONALDO: Why would someone\\n",
        "who keeps birds come all\\l",
        "the way out here?$",
    )),
    "Route125_Text_PresleyDefeat": (("I'll tell you why",), (
        "RONALDO: All right. I'll\\n",
        "tell you why.$",
    )),
    "Route125_Text_PresleyPostBattle": (("message in a bottle",), (
        "RONALDO: I put a note in a\\n",
        "bottle and let the tide\\l",
        "have it.\\p",
        "Someone will find it.\\n",
        "That's the whole idea.$",
    )),
    "Route125_Text_AuronIntro": (("throwing garbage",), (
        "ALVARO: Was that you\\n",
        "throwing rubbish in the\\l",
        "water?$",
    )),
    "Route125_Text_AuronDefeat": (("weren't throwing trash",), (
        "ALVARO: Oh. It wasn't you.$",
    )),
    "Route125_Text_AuronPostBattle": (("bottle bobbing", "pollute the sea"), (
        "ALVARO: I found a bottle\\n",
        "floating out here earlier.\\p",
        "Somebody threw it in.\\n",
        "That makes me furious.$",
    )),

    # -- Route 126, under the white rock ------------------------------------
    "Route126_Text_BarryIntro": (("full-body workout",), (
        "ANDERSON: Swimming works\\n",
        "everything at once.\\p",
        "Look what it's done.$",
    )),
    "Route126_Text_BarryDefeat": (("I admit it",), (
        "ANDERSON: All right.\\n",
        "You win.$",
    )),
    "Route126_Text_BarryPostBattle": (("daily swimming routine", "physique"), (
        "ANDERSON: Every day, in\\n",
        "this water.\\p",
        "That's where all of this\\n",
        "came from.$",
    )),
    "Route126_Text_DeanIntro": (("white mountain", "AGUAS DE M'BOI"), (
        "ENEAS: That white wall of\\n",
        "rock is AGUAS DE M'BOI.$",
    )),
    "Route126_Text_DeanDefeat": (("done in",), (
        "ENEAS: Was I just done in?$",
    )),
    "Route126_Text_DeanPostBattle": (("find the entrance",), (
        "ENEAS: I can't find the way\\n",
        "into AGUAS DE M'BOI.\\p",
        "There must be one.$",
    )),
    "Route126_Text_NikkiIntro": (("mermaid",), (
        "NORMA: Heheh! I'm the thing\\n",
        "sailors tell stories about!$",
    )),
    "Route126_Text_NikkiDefeat": (("fantasy burst",), (
        "NORMA: And there goes the\\n",
        "story. Blub.$",
    )),
    "Route126_Text_NikkiPostBattle": (("wave of despair",), (
        "NORMA: You flattened me.\\p",
        "I'd like the water to take\\n",
        "me now, please.$",
    )),
    "Route126_Text_BrendaIntro": (("Hello, kiddo",), (
        "CIDA: Hello, small one!\\p",
        "Battle me?$",
    )),
    "Route126_Text_BrendaDefeat": (("Oh, noooooh",), (
        "CIDA: Oh, nooooo!$",
    )),
    "Route126_Text_BrendaPostBattle": (("frolicking",), (
        "CIDA: Playing about in the\\n",
        "sea with them.\\p",
        "It's the best thing I do.$",
    )),
    "Route126_Text_PabloIntro": (("sculpted body", "BLACK BELT"), (
        "RICARDO: Look at the shape\\n",
        "of me!\\p",
        "I'm carved better than any\\n",
        "BLACK BELT.$",
    )),
    "Route126_Text_PabloDefeat": (("Not bad at all",), (
        "RICARDO: Whoops! Strong!\\n",
        "Not bad at all!$",
    )),
    "Route126_Text_PabloPostBattle": (("stimulated my senses",), (
        "RICARDO: Losing to you woke\\n",
        "me right up.\\p",
        "We're training harder\\n",
        "after this.$",
    )),
    "Route126_Text_PabloRegister": (("get to know you more",), (
        "RICARDO: You're not bad at\\n",
        "all.\\p",
        "I'd like to know you\\n",
        "better.$",
    )),
    "Route126_Text_PabloRematchIntro": (("beautiful body", "SWIMMER"), (
        "RICARDO: Look at this\\n",
        "shape!\\p",
        "Better lines than any\\n",
        "SWIMMER out here.$",
    )),
    "Route126_Text_PabloRematchDefeat": (("Really too strong",), (
        "RICARDO: Whoops! Far too\\n",
        "strong! Not bad!$",
    )),
    "Route126_Text_PabloPostRematch": (("great motivator", "come back again"), (
        "RICARDO: Harder still,\\n",
        "then.\\p",
        "You get more out of me\\n",
        "than anyone. Come back.$",
    )),
    "Route126_Text_LeonardoIntro": (("couldn't even swim", "capable of anything"), (
        "ODAIR: A year ago I\\n",
        "couldn't swim at all.\\p",
        "Now look. I think I could\\n",
        "learn anything.$",
    )),
    "Route126_Text_LeonardoDefeat": (("getting greedy",), (
        "ODAIR: Getting greedy did\\n",
        "me no favours.$",
    )),
    "Route126_Text_LeonardoPostBattle": (("practice at something", "don't be afraid"), (
        "ODAIR: Practise a thing and\\n",
        "you get better at it.\\p",
        "You're young. Try\\n",
        "everything.$",
    )),
    "Route126_Text_IsobelIntro": (("up your nose",), (
        "HELENA: Seawater up the\\n",
        "nose. Doesn't it just?$",
    )),
    "Route126_Text_IsobelDefeat": (("Ack",), (
        "HELENA: Ack! Why, you...\\n",
        "Glub!$",
    )),
    "Route126_Text_IsobelPostBattle": (("choked on some water",), (
        "HELENA: I've swallowed\\n",
        "half the sea.\\p",
        "Bitter. Salt. Awful.$",
    )),
    "Route126_Text_SiennaIntro": (("whole heart",), (
        "SUELI: I'm putting all of\\n",
        "myself into this one.$",
    )),
    "Route126_Text_SiennaDefeat": (("more heart",), (
        "SUELI: You had more of\\n",
        "yourself to give.$",
    )),
    "Route126_Text_SiennaPostBattle": (("go for a dive",), (
        "SUELI: I need to cool down.\\p",
        "I'll go under for a while.$",
    )),

    # -- Route 127, the crossing ---------------------------------------------
    "Route127_Text_CamdenIntro": (("see it in your face",), (
        "CAMILO: It's on your face.\\p",
        "You want to take me on.$",
    )),
    "Route127_Text_CamdenDefeat": (("Awawawawawa",), (
        "CAMILO: Awawawawa...$",
    )),
    "Route127_Text_CamdenPostBattle": (("refreshed and serene",), (
        "CAMILO: A good match\\n",
        "leaves me clear-headed.\\p",
        "That was a good match.$",
    )),
    "Route127_Text_DonnyIntro": (("rival",), (
        "ERICA: Is there someone you\\n",
        "cannot stand to lose to?$",
    )),
    "Route127_Text_DonnyDefeat": (("hate losing",), (
        "ERICA: Arrgh! I hate\\n",
        "losing!$",
    )),
    "Route127_Text_DonnyPostBattle": (("keep getting", "better"), (
        "ERICA: When there's someone\\n",
        "like that, you can't stop\\l",
        "improving.\\p",
        "You just can't.$",
    )),
    "Route127_Text_JonahIntro": (("becalmed serenity", "demonstrate"), (
        "LUIZ: Fishing has made me\\n",
        "very calm.\\p",
        "Allow me to demonstrate.$",
    )),
    "Route127_Text_JonahDefeat": (("heart remains",), (
        "LUIZ: I have lost. I remain\\n",
        "calm.$",
    )),
    "Route127_Text_JonahPostBattle": (("catch nothing", "line remains"), (
        "LUIZ: It does not matter\\n",
        "that I catch nothing.\\p",
        "The line stays in the\\n",
        "water. That is the point.$",
    )),
    "Route127_Text_HenryIntro": (("snagged",), (
        "ISMAEL: Whoops! Did I just\\n",
        "hook something you were\\l",
        "riding?$",
    )),
    "Route127_Text_HenryDefeat": (("can't keep up",), (
        "ISMAEL: I can't keep up!$",
    )),
    "Route127_Text_HenryPostBattle": (("handful if I hooked",), (
        "ISMAEL: If one of yours\\n",
        "took my line I'd be in\\l",
        "real trouble.$",
    )),
    "Route127_Text_RogerIntro": (("fan and a fishing buff",), (
        "SOCRATES: Well, then! A\\n",
        "TRAINER and a fisherman.\\p",
        "One of each.$",
    )),
    "Route127_Text_RogerDefeat": (("party's over",), (
        "SOCRATES: No! The line's in\\n",
        "knots! Party's over!$",
    )),
    "Route127_Text_RogerPostBattle": (("tangle tango",), (
        "SOCRATES: My line is\\n",
        "dancing.\\p",
        "The tangle tango. Ha!$",
    )),
    "Route127_Text_AidanIntro": (("excellent vision", "great heights"), (
        "ADEMIR: The ones with wings\\n",
        "see everything.\\p",
        "They pick you out from\\n",
        "right up there.$",
    )),
    "Route127_Text_AidanDefeat": (("I give up",), (
        "ADEMIR: Whew. I give up.$",
    )),
    "Route127_Text_AidanPostBattle": (("diving spots", "darker color"), (
        "ADEMIR: There are places to\\n",
        "dive all over this water.\\p",
        "From above they're darker\\n",
        "than the rest.$",
    )),
    "Route127_Text_KojiIntro": (("bare feet", "toughen up your soles"), (
        "NEWTON: Run barefoot.\\p",
        "It hardens the soles of\\n",
        "your feet.$",
    )),
    "Route127_Text_KojiDefeat": (("pebble under a toenail",), (
        "NEWTON: Yowch! Stone under\\n",
        "the toenail!$",
    )),
    "Route127_Text_KojiPostBattle": (("RUNNING SHOES are cool",), (
        "NEWTON: Barefoot is best.\\p",
        "Those RUNNING SHOES look\\n",
        "good, mind you.$",
    )),
    "Route127_Text_KojiRegister": (("people who beat me",), (
        "NEWTON: This is what I do\\n",
        "for people who beat me.\\p",
        "Let's go again sometime.$",
    )),
    "Route127_Text_KojiRematchIntro": (("still run in my bare feet",), (
        "NEWTON: Still barefoot,\\n",
        "still running.\\p",
        "Soles like leather.$",
    )),
    "Route127_Text_KojiRematchDefeat": (("Pebbles dug",), (
        "NEWTON: Yowch! Stones in\\n",
        "the arches!$",
    )),
    "Route127_Text_KojiPostRematch": (("go barefoot for a while",), (
        "NEWTON: Fancy going\\n",
        "barefoot a while?\\p",
        "I'd like a turn in those\\n",
        "RUNNING SHOES.$",
    )),
    "Route127_Text_AthenaIntro": (("slow and methodical",), (
        "BRUNA: Let's do this slowly\\n",
        "and properly.$",
    )),
    "Route127_Text_AthenaDefeat": (("do any strategizing",), (
        "BRUNA: You gave me no time\\n",
        "to think at all.$",
    )),
    "Route127_Text_AthenaPostBattle": (("time slows down",), (
        "BRUNA: Blue below, blue\\n",
        "above.\\p",
        "Out here the hours go\\n",
        "slower.$",
    )),

    # -- Route 128, the last water before Estr. Juramento -------------------
    "Route128_Text_IsaiahIntro": (("ESTR. JURAMENTO", "long ways"), (
        "JOVINO: ESTR. JURAMENTO is\\n",
        "still a long way off.$",
    )),
    "Route128_Text_IsaiahDefeat": (("first victory",), (
        "JOVINO: So is my first\\n",
        "win, apparently.$",
    )),
    "Route128_Text_IsaiahPostBattle": (("never give up",), (
        "JOVINO: I have lost my\\n",
        "whole life.\\p",
        "I'm still going.$",
    )),
    "Route128_Text_IsaiahRegister": (("win eventually", "POKéNAV"), (
        "JOVINO: I'm no good yet.\\p",
        "I will be. Put me in your\\n",
        "POKéNAV and find out.$",
    )),
    "Route128_Text_IsaiahRematchIntro": (("keep on", "swimming to ESTR"), (
        "JOVINO: Still feeling good.\\p",
        "Still swimming toward\\n",
        "ESTR. JURAMENTO.$",
    )),
    "Route128_Text_IsaiahRematchDefeat": (("yet to taste",), (
        "JOVINO: Still no first\\n",
        "win.$",
    )),
    "Route128_Text_IsaiahPostRematch": (("eventually reach",), (
        "JOVINO: I'll reach ESTR.\\n",
        "JURAMENTO eventually.\\p",
        "And win, eventually.$",
    )),
    "Route128_Text_KatelynIntro": (("swim, cycle", "three events"), (
        "JUREMA: Swim, ride, then\\n",
        "run a marathon.\\p",
        "Three events, no stopping\\n",
        "between them.$",
    )),
    "Route128_Text_KatelynDefeat": (("grueling, too",), (
        "JUREMA: A battle is just as\\n",
        "punishing.$",
    )),
    "Route128_Text_KatelynPostBattle": (("throw in the towel",), (
        "JUREMA: The ride's next.\\p",
        "I am very close to giving\\n",
        "up.$",
    )),
    "Route128_Text_KatelynRegister": (("make the best", "rematch"), (
        "JUREMA: Well. I'll make the\\n",
        "best of it.\\p",
        "Rematch me sometime.$",
    )),
    "Route128_Text_KatelynRematchIntro": (("POKéMON CHAMPION", "long and grueling"), (
        "JUREMA: A triathlon is\\n",
        "long.\\p",
        "So is the road to being\\n",
        "CHAMPION, I'm told.$",
    )),
    "Route128_Text_KatelynRematchDefeat": (("harsh", "unforgiving"), (
        "JUREMA: Battling really is\\n",
        "unforgiving.$",
    )),
    "Route128_Text_KatelynPostRematch": (("serious thought", "ESTR. JURAMENTO"), (
        "JUREMA: You should think\\n",
        "seriously about ESTR.\\l",
        "JURAMENTO.\\p",
        "You'd get through it.$",
    )),
    "Route128_Text_AlexaIntro": (("POKéMON LEAGUE challenge", "afford to lose"), (
        "ALZIRA: We've worked for\\n",
        "years to get a LEAGUE\\l",
        "challenge.\\p",
        "We can't lose now.$",
    )),
    "Route128_Text_AlexaDefeat": (("How could this happen",), (
        "ALZIRA: Oh! How did that\\n",
        "happen?$",
    )),
    "Route128_Text_AlexaPostBattle": (("one setback",), (
        "ALZIRA: After everything it\\n",
        "took to get here.\\p",
        "One loss isn't stopping\\n",
        "me.$",
    )),
    "Route128_Text_RubenIntro": (("no stronger TRAINER",), (
        "TIAGO: There is no stronger\\n",
        "TRAINER than me.$",
    )),
    "Route128_Text_RubenDefeat": (("This can't be",), (
        "TIAGO: This cannot be.$",
    )),
    "Route128_Text_RubenPostBattle": (("stronger TRAINER", "than you"), (
        "TIAGO: There is probably no\\n",
        "stronger TRAINER than you.$",
    )),
    "Route128_Text_WayneIntro": (("WATERFALL", "crest the falls"), (
        "AQUILES: I want to reach\\n",
        "ESTR. JURAMENTO.\\p",
        "So I caught something that\\n",
        "can climb the falls.$",
    )),
    "Route128_Text_WayneDefeat": (("crestfallen",), (
        "AQUILES: I'm crestfallen.$",
    )),
    "Route128_Text_WaynePostBattle": (("AGUAS DE M'BOI GYM",), (
        "AQUILES: Phooey.\\p",
        "Mine can climb it, and I\\n",
        "still don't have the AGUAS\\l",
        "DE M'BOI BADGE.$",
    )),
    "Route128_Text_HarrisonIntro": (("awfully tough", "if I can win"), (
        "INACIO: You look tough.\\p",
        "I wonder if I've a chance\\n",
        "at all.$",
    )),
    "Route128_Text_HarrisonDefeat": (("impossible to win",), (
        "INACIO: Ouch. That was\\n",
        "never winnable.$",
    )),
    "Route128_Text_HarrisonPostBattle": (("TRAINERS galore", "out"), (
        "INACIO: The water round\\n",
        "ESTR. JURAMENTO is full of\\l",
        "hard TRAINERS.\\p",
        "Am I out of my depth?$",
    )),
    "Route128_Text_CarleeIntro": (("sunlight seems to be more harsh",), (
        "CLEIDE: The sun is worse\\n",
        "out here than anywhere.$",
    )),
    "Route128_Text_CarleeDefeat": (("sun's glare",), (
        "CLEIDE: I couldn't see for\\n",
        "the glare.$",
    )),
    "Route128_Text_CarleePostBattle": (("reapply my sunscreen",), (
        "CLEIDE: I should head in.\\p",
        "I need to cover up again.$",
    )),

    # -- Route 129, the shallows before the falls ---------------------------
    "Route129_Text_ChaseIntro": (("first triathlon", "tense"), (
        "CLEBER: My first triathlon.\\p",
        "I'm strung tight.$",
    )),
    "Route129_Text_ChaseDefeat": (("failed to win",), (
        "CLEBER: Wroar! Didn't win!$",
    )),
    "Route129_Text_ChasePostBattle": (("tensed up", "give it my all"), (
        "CLEBER: Wound up like this\\n",
        "I can't give it everything.\\p",
        "I need to breathe.$",
    )),
    "Route129_Text_AllisonIntro": (("middle of a triathlon", "why don't we battle"), (
        "ANITA: I'm mid-event.\\p",
        "Sure. Let's battle anyway.$",
    )),
    "Route129_Text_AllisonDefeat": (("sure I'd win",), (
        "ANITA: I was certain I had\\n",
        "that.$",
    )),
    "Route129_Text_AllisonPostBattle": (("greatest thing", "endurance"), (
        "ANITA: Do you know the best\\n",
        "part of a triathlon?\\p",
        "Finding out exactly where\\n",
        "your own edge is.$",
    )),
    "Route129_Text_ReedIntro": (("Say hey", "get on with it"), (
        "SAULO: Hey, hey! Let's get\\n",
        "on with it!$",
    )),
    "Route129_Text_ReedDefeat": (("I'm beaten",), (
        "SAULO: Beat. I'm beaten.\\n",
        "Done.$",
    )),
    "Route129_Text_ReedPostBattle": (("nothing for a loser",), (
        "SAULO: Nothing out here for\\n",
        "a loser.\\p",
        "I'm going home.$",
    )),
    "Route129_Text_TishaIntro": (("What's the hurry", "slow and easy"), (
        "VITORIA: What's the rush?\\p",
        "Let's take this slowly.$",
    )),
    "Route129_Text_TishaDefeat": (("relax a little more",), (
        "VITORIA: Oh, my. I wanted\\n",
        "longer than that.$",
    )),
    "Route129_Text_TishaPostBattle": (("mistakes when", "in a rush"), (
        "VITORIA: You make mistakes\\n",
        "when you hurry.\\p",
        "So I don't hurry.$",
    )),
    "Route129_Text_ClarenceIntro": (("Surfing isn't as easy",), (
        "DARIO: Riding one of them\\n",
        "isn't as easy as it looks,\\l",
        "is it.$",
    )),
    "Route129_Text_ClarenceDefeat": (("Winning sure isn't easy",), (
        "DARIO: Winning isn't easy\\n",
        "either.$",
    )),
    "Route129_Text_ClarencePostBattle": (("POKéMON", "Keep at it"), (
        "DARIO: You're going for the\\n",
        "LEAGUE, aren't you.\\p",
        "Keep at it.$",
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
        masked = masked[:start] + '\t.string "<ARAUNA_OPEN_SEA_EN>"\n\n' + masked[end:]
    return masked


def validate_rendered(source: str, rendered: str) -> None:
    if mask(source) != mask(rendered):
        raise ValueError("non-dialogue structure changed while rendering")

    forbidden = ("Aruanan", "Feast your eyes on this physique", "I'm a mermaid",
                 "girl SWIMMER will", "more cut than a")
    for label in TARGETS:
        body = block_pattern(label).search(rendered).group("body")
        for token in forbidden:
            if token in body:
                raise ValueError(f"{label}: vanilla voice survived: {token}")

    # Everyone on 128 is pointed at the same place. If it stops being named,
    # the last swim before the league has lost what it is for.
    last = "".join("".join(p) for label, (_, p) in TARGETS.items()
                   if label.startswith("Route128"))
    if last.count("ESTR.") < 3:
        raise ValueError("Route 128 stopped pointing at Estr. Juramento")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Render the Route 125-129 trainers in English.")
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
    print(f"Open sea trainers English renderer OK: {len(TARGETS)} blocks "
          f"across Routes 125 to 129.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
