#!/usr/bin/env python3
"""The trainers of Routes 114, 115 and 118: the ridge, the shore and the river.

A hundred and seventeen blocks on the roads either side of Ruinas da Queda.
Route 114 is the descent toward the falls, full of campers and people shouting
at a cliff that will not answer. Route 115 is the training beach north of Serra
do Uivo, where everyone is working on something. Route 118 is the river mouth,
where the fishermen and the bird keepers share a bank and mostly ignore each
other.

One block had ended up naming a creature, because the species pass dropped an
Arauna name into an Emerald sentence. It is gone, under the same rule as the
other slices: the dex is generated, so no payload names a species.

The mentor and her junior keep their pairing -- TAIS taught IVA, and IVA says
so -- and the renderer refuses to publish if that stops being true.
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
    # -- Route 114, down toward the falls -----------------------------------
    "Route114_Text_LennyIntro": (("yodelayhihoo", "echo"), (
        "NOEL: Yodelayhihoo!\\p",
        "... ...\\p",
        "You're meant to shout back.\\n",
        "Nothing echoes here.$",
    )),
    "Route114_Text_LennyDefeat": (("Yodelayhihoo",), (
        "NOEL: Yodelayhihoo...$",
    )),
    "Route114_Text_LennyPostBattle": (("wee tyke", "copying me"), (
        "NOEL: When I was small I\\n",
        "thought someone lived out\\l",
        "there, shouting back.\\p",
        "Nobody does. I still shout.$",
    )),
    "Route114_Text_LucasIntro": (("not prepared", "mountains"), (
        "OLIVIO: Come up here\\n",
        "unprepared and the\\l",
        "mountain decides for you.$",
    )),
    "Route114_Text_LucasDefeat": (("unforgiving",), (
        "OLIVIO: The high ground\\n",
        "forgives nothing.$",
    )),
    "Route114_Text_LucasPostBattle": (("winter", "avalanches"), (
        "OLIVIO: In the cold months\\n",
        "this turns dangerous.\\p",
        "Wind, rockfall, and no one\\n",
        "to hear you.$",
    )),
    "Route114_Text_ShaneIntro": (("Camping's fun", "spooky stories"), (
        "ULISSES: Camping. Fishing,\\n",
        "fire, bad ghost stories.\\p",
        "Best part's the battling,\\n",
        "though.$",
    )),
    "Route114_Text_ShaneDefeat": (("Way too strong",), (
        "ULISSES: Far too strong.$",
    )),
    "Route114_Text_ShanePostBattle": (("go", "camping with my POKéMON"), (
        "ULISSES: Sleeping out here\\n",
        "with them beside me.\\p",
        "There's nothing better.$",
    )),
    "Route114_Text_NancyIntro": (("exercise after a meal",), (
        "NILDA: I've eaten too much.\\p",
        "Battle me. It'll settle.$",
    )),
    "Route114_Text_NancyDefeat": (("Oh, no",), (
        "NILDA: Oh, no.$",
    )),
    "Route114_Text_NancyPostBattle": (("tasty meal", "drowsy"), (
        "NILDA: Good food, and now\\n",
        "I'm falling asleep\\l",
        "standing up.$",
    )),
    "Route114_Text_SteveIntro": (("Ufufufufufu", "battle against"), (
        "VALERIO: Heheh...\\p",
        "Would you like to battle\\n",
        "mine? Really look at them?$",
    )),
    "Route114_Text_SteveDefeat": (("M-My POKéMON",), (
        "VALERIO: M-mine...$",
    )),
    "Route114_Text_StevePostBattle": (("enormous horns", "I wish I had"), (
        "VALERIO: Something heavy.\\p",
        "Horns. Old scars. Teeth\\n",
        "that have been used.\\p",
        "One day I'll have one.$",
    )),
    "Route114_Text_SteveRegister": (("Don't forget what you've done",), (
        "VALERIO: You won't forget\\n",
        "this.\\p",
        "I'll make sure of it.$",
    )),
    "Route114_Text_SteveRematchIntro": (("Come on, battle",), (
        "VALERIO: Heheh...\\p",
        "Come and battle mine\\n",
        "again.$",
    )),
    "Route114_Text_SteveRematchDefeat": (("so lucky",), (
        "VALERIO: I got to see yours\\n",
        "up close. That's enough.$",
    )),
    "Route114_Text_StevePostRematch": (("shivery and shaky",), (
        "VALERIO: Heheh.\\p",
        "Watching two of them go at\\n",
        "each other makes my hands\\l",
        "shake. Every time.$",
    )),
    "Route114_Text_BernieIntro": (("campfire", "water handy"), (
        "ARNALDO: Lighting a fire\\n",
        "out here?\\p",
        "Then keep water where you\\n",
        "can reach it.$",
    )),
    "Route114_Text_BernieDefeat": (("dousing my fire",), (
        "ARNALDO: Well. You put me\\n",
        "out.$",
    )),
    "Route114_Text_BerniePostBattle": (("careful with", "power"), (
        "ARNALDO: Any fire, in any\\n",
        "forest, needs watching.\\p",
        "Don't get comfortable\\n",
        "around it.$",
    )),
    "Route114_Text_BernieRegister": (("spirit on fire", "register"), (
        "ARNALDO: You lit something\\n",
        "in me.\\p",
        "Let's take each other's\\n",
        "numbers.$",
    )),
    "Route114_Text_BernieRematchIntro": (("keep water handy",), (
        "ARNALDO: Learned to keep\\n",
        "the water close yet?$",
    )),
    "Route114_Text_BernieRematchDefeat": (("hosed down",), (
        "ARNALDO: Doused before I\\n",
        "even caught.$",
    )),
    "Route114_Text_BerniePostRematch": (("careful with", "power"), (
        "ARNALDO: Same lesson.\\p",
        "Any fire, any forest.\\n",
        "Never get comfortable.$",
    )),
    "Route114_Text_ClaudeIntro": (("we were fishing", "bring on"), (
        "DEMETRIO: If this were a\\n",
        "fishing contest you'd have\\l",
        "no chance.\\p",
        "It isn't. Go on, then.$",
    )),
    "Route114_Text_ClaudeDefeat": (("I would've won",), (
        "DEMETRIO: With a rod in my\\n",
        "hand I'd have won that.$",
    )),
    "Route114_Text_ClaudePostBattle": (("RUINAS DA QUEDA",), (
        "DEMETRIO: I'm going to try\\n",
        "the water at RUINAS DA\\l",
        "QUEDA.\\p",
        "Something's in there.\\n",
        "I know it.$",
    )),
    "Route114_Text_NolanIntro": (("I like to fish", "even if I'm fishing"), (
        "REINALDO: I fish and I\\n",
        "battle.\\p",
        "Challenge me mid-cast and\\n",
        "I'll still stand up.$",
    )),
    "Route114_Text_NolanDefeat": (("doesn't", "good at it"), (
        "REINALDO: Liking it and\\n",
        "being good at it are two\\l",
        "different things.$",
    )),
    "Route114_Text_NolanPostBattle": (("This time I'll do it", "can't walk"), (
        "REINALDO: Next one. Next\\n",
        "one for certain.\\p",
        "I say that about the fish\\n",
        "as well. I never leave.$",
    )),
    "Route114_Text_TyraIntro": (("in the mood", "teach you"), (
        "TAIS: Go on, then. I'm in\\n",
        "the mood.\\p",
        "I'll show you a thing or\\n",
        "two.$",
    )),
    "Route114_Text_TyraDefeat": (("amazing battle style",), (
        "TAIS: What a way to fight.$",
    )),
    "Route114_Text_TyraPostBattle": (("teaching my junior",), (
        "TAIS: I've been teaching\\n",
        "IVA everything I know.\\p",
        "She learns faster than\\n",
        "I did.$",
    )),
    "Route114_Text_TyraNotEnoughMons": (("just one",), (
        "TAIS: One won't do against\\n",
        "the two of us.$",
    )),
    "Route114_Text_IvyIntro": (("Who taught you",), (
        "IVA: Who taught you how to\\n",
        "do this?$",
    )),
    "Route114_Text_IvyDefeat": (("amazing battle style",), (
        "IVA: What a way to fight.$",
    )),
    "Route114_Text_IvyPostBattle": (("my student mentor",), (
        "IVA: I only started because\\n",
        "TAIS taught me.\\p",
        "All of it came from her.$",
    )),
    "Route114_Text_IvyNotEnoughMons": (("only have one", "lonesome"), (
        "IVA: Only one with you?\\p",
        "That must be lonely for it.$",
    )),
    "Route114_Text_KaiIntro": (("landed a big one",), (
        "MAURO: I landed a big one!\\n",
        "An enormous one!$",
    )),
    "Route114_Text_KaiDefeat": (("lose in size",), (
        "MAURO: What happened?\\n",
        "Was mine not big enough?$",
    )),
    "Route114_Text_KaiPostBattle": (("bigger one",), (
        "MAURO: Right. I'll go and\\n",
        "land a bigger one.$",
    )),
    "Route114_Text_CharlotteIntro": (("just a pretty face",), (
        "DARCI: Me? I'm not only\\n",
        "decorative.$",
    )),
    "Route114_Text_CharlotteDefeat": (("wasn't cute",), (
        "DARCI: There was nothing\\n",
        "charming about that.$",
    )),
    "Route114_Text_CharlottePostBattle": (("quirk",), (
        "DARCI: I don't want one\\n",
        "that's only sweet.\\p",
        "Give me one with a strange\\n",
        "habit or two.$",
    )),
    "Route114_Text_AngelinaIntro": (("made your POKéMON evolve",), (
        "BERENICE: Have you let\\n",
        "yours change much?$",
    )),
    "Route114_Text_AngelinaDefeat": (("good to know",), (
        "BERENICE: I see. That's\\n",
        "worth knowing.$",
    )),
    "Route114_Text_AngelinaPostBattle": (("startling",), (
        "BERENICE: Some of them come\\n",
        "out of it unrecognisable.\\p",
        "It never stops surprising\\n",
        "me.$",
    )),

    # -- Route 115, the training beach --------------------------------------
    "Route115_Text_TimothyIntro": (("rather capable", "keep you company"), (
        "WALDIR: Hm. You look\\n",
        "capable.\\p",
        "Allow me to keep you\\n",
        "company.$",
    )),
    "Route115_Text_TimothyDefeat": (("much stronger",), (
        "WALDIR: Far stronger than\\n",
        "I had assumed.$",
    )),
    "Route115_Text_TimothyPostBattle": (("born genius", "depends on effort"), (
        "WALDIR: Nobody is born\\n",
        "able to do this.\\p",
        "It is all work. I have to\\n",
        "believe that.$",
    )),
    "Route115_Text_TimothyRegister": (("distant memory", "another opportunity"), (
        "WALDIR: I have not lost\\n",
        "that thoroughly in years.\\p",
        "Grant me another chance at\\n",
        "it.$",
    )),
    "Route115_Text_TimothyRematchIntro": (("agility speaks", "keep me company"), (
        "WALDIR: Quick as ever, I\\n",
        "see.\\p",
        "Come. Keep me company.$",
    )),
    "Route115_Text_TimothyRematchDefeat": (("strong as ever",), (
        "WALDIR: As strong as ever.$",
    )),
    "Route115_Text_TimothyPostRematch": (("haven't put in enough",), (
        "WALDIR: It is all work.\\p",
        "I lost because I have not\\n",
        "done enough of it.$",
    )),
    "Route115_Text_KoichiIntro": (("Demand a battle",), (
        "NESTOR: You!\\p",
        "My little swarm!\\p",
        "Demands a battle!$",
    )),
    "Route115_Text_KoichiDefeat": (("Ouch, ouch",), (
        "NESTOR: Ouch, ouch, ouch!$",
    )),
    "Route115_Text_KoichiPostBattle": (("seek power", "grow strong with them"), (
        "NESTOR: My little swarm\\n",
        "wants to get stronger.\\p",
        "So I get stronger with\\n",
        "them. That's the deal.$",
    )),
    "Route115_Text_NobIntro": (("busting bricks",), (
        "RAMIRO: My best trick is\\n",
        "breaking bricks with my\\l",
        "forehead.$",
    )),
    "Route115_Text_NobDefeat": (("head is busted",), (
        "RAMIRO: Ugwaah! My head!$",
    )),
    "Route115_Text_NobPostBattle": (("teaching my POKéMON karate", "excited"), (
        "RAMIRO: I've been teaching\\n",
        "mine to fight properly.\\p",
        "They'll pass me soon.\\n",
        "I'm looking forward to it.$",
    )),
    "Route115_Text_NobRegister": (("impress me", "redo my training"), (
        "RAMIRO: You've impressed\\n",
        "me.\\p",
        "Rematch, after I've put\\n",
        "the work in.$",
    )),
    "Route115_Text_NobRematchIntro": (("trained hard", "give us a rematch"), (
        "RAMIRO: We trained hard\\n",
        "after you beat us.\\p",
        "Come on. Again.$",
    )),
    "Route115_Text_NobRematchDefeat": (("We lost again",), (
        "RAMIRO: Ugwaah! Beaten\\n",
        "again!$",
    )),
    "Route115_Text_NobPostRematch": (("redouble my training",), (
        "RAMIRO: They'll get\\n",
        "stronger.\\p",
        "So will I. Back to work.$",
    )),
    "Route115_Text_CyndyIntro": (("secret training spot", "butting in"), (
        "DULCE: This beach is where\\n",
        "I train. Privately.\\p",
        "Don't make a habit of it.$",
    )),
    "Route115_Text_CyndyDefeat": (("haven't trained enough",), (
        "DULCE: Not enough hours.\\n",
        "That's all that was.$",
    )),
    "Route115_Text_CyndyPostBattle": (("cushion", "perfect place to train"), (
        "DULCE: Sand takes the\\n",
        "impact out of a fall.\\p",
        "That's why I train here\\n",
        "and nowhere else.$",
    )),
    "Route115_Text_CyndyRegister": (("free to come here", "battle you again"), (
        "DULCE: Fine. You may use\\n",
        "the beach.\\p",
        "In exchange I want another\\n",
        "battle.$",
    )),
    "Route115_Text_CyndyRematchIntro": (("get this battle on",), (
        "DULCE: Right. Let's have\\n",
        "it.$",
    )),
    "Route115_Text_CyndyRematchDefeat": (("I can battle but",), (
        "DULCE: I can fight. Mine\\n",
        "still need the hours.$",
    )),
    "Route115_Text_CyndyPostRematch": (("still get some", "love POKéMON"), (
        "DULCE: I enjoy it even\\n",
        "when I lose.\\p",
        "That probably tells you\\n",
        "something about me.$",
    )),
    "Route115_Text_HectorIntro": (("rare POKéMON", "show you"), (
        "ISAIAS: I have something\\n",
        "rare here.\\p",
        "Want to see it?$",
    )),
    "Route115_Text_HectorDefeat": (("You want my POKéMON",), (
        "ISAIAS: You want it now,\\n",
        "don't you.$",
    )),
    "Route115_Text_HectorPostBattle": (("enough to keep me satisfied",), (
        "ISAIAS: One rare thing.\\p",
        "That's all I need to be\\n",
        "content.$",
    )),
    "Route115_Text_KyraIntro": (("battle while I'm running",), (
        "LUCIANA: I'll battle you\\n",
        "and keep running.\\p",
        "Try to stay with me.$",
    )),
    "Route115_Text_KyraDefeat": (("Gasp, gasp",), (
        "LUCIANA: Gasp... gasp...$",
    )),
    "Route115_Text_KyraPostBattle": (("mistake of trying", "calm down"), (
        "LUCIANA: Battling at a run\\n",
        "was a mistake.\\p",
        "I'll go for a run to calm\\n",
        "down about it.$",
    )),
    "Route115_Text_JaidenIntro": (("ninja attack",), (
        "LAURO: Take this!\\n",
        "Ultimate hidden strike!$",
    )),
    "Route115_Text_JaidenDefeat": (("strategy failed",), (
        "LAURO: Waaah! The plan!\\n",
        "The plan failed!$",
    )),
    "Route115_Text_JaidenPostBattle": (("ultra",), (
        "LAURO: But they were\\n",
        "impressive, weren't they?\\p",
        "Say they were impressive.$",
    )),
    "Route115_Text_HeleneIntro": (("black belt-level",), (
        "GABRIELA: Mine hit like\\n",
        "trained fighters.$",
    )),
    "Route115_Text_HeleneDefeat": (("too humiliating",), (
        "GABRIELA: This is\\n",
        "humiliating.$",
    )),
    "Route115_Text_HelenePostBattle": (("rarely meet anyone", "GYM LEADER"), (
        "GABRIELA: Almost nobody\\n",
        "beats me.\\p",
        "Oh. You're a GYM LEADER,\\n",
        "aren't you.$",
    )),
    "Route115_Text_AlixIntro": (("Our eyes met", "no getting away"), (
        "ANGELA: Our eyes met.\\p",
        "You can't walk off from\\n",
        "that.$",
    )),
    "Route115_Text_AlixDefeat": (("Not bad",), (
        "ANGELA: Gah. Not bad.$",
    )),
    "Route115_Text_AlixPostBattle": (("TELEPORT home",), (
        "ANGELA: Never mind.\\p",
        "I'll take the short way\\n",
        "home. Watch this.$",
    )),
    "Route115_Text_MarleneIntro": (("meditation", "punished"), (
        "MATILDE: You've broken my\\n",
        "concentration.\\p",
        "There's a price for that.$",
    )),
    "Route115_Text_MarleneDefeat": (("broken my concentration",), (
        "MATILDE: My concentration.\\n",
        "Gone entirely.$",
    )),
    "Route115_Text_MarlenePostBattle": (("meditating", "isn't very peaceful"), (
        "MATILDE: I came here to sit\\n",
        "quietly with mine.\\p",
        "It is not a quiet beach.$",
    )),

    # -- Route 118, the river mouth -----------------------------------------
    "Route118_Text_RoseIntro": (("aroma of flowers", "body and soul"), (
        "REGINA: A good smell does\\n",
        "something to a person.\\p",
        "Cleans them out.$",
    )),
    "Route118_Text_RoseDefeat": (("seem to have lost",), (
        "REGINA: Oh, dear me. I\\n",
        "appear to have lost.$",
    )),
    "Route118_Text_RosePostBattle": (("Stinky things",), (
        "REGINA: Flowers, creatures,\\n",
        "anything that smells\\l",
        "sweet. I love it all.\\p",
        "The other sort I avoid.$",
    )),
    "Route118_Text_RoseRegister": (("odor", "POKéNAV"), (
        "REGINA: Sniff. Is that a\\n",
        "POKéNAV?\\p",
        "We're registering each\\n",
        "other at once.$",
    )),
    "Route118_Text_RoseRematchIntro": (("drawn here by the sweet",), (
        "REGINA: Did the scent\\n",
        "bring you back?$",
    )),
    "Route118_Text_RoseRematchDefeat": (("didn't seem to do much",), (
        "REGINA: The scent did very\\n",
        "little for me there.$",
    )),
    "Route118_Text_RosePostRematch": (("attracted by it",), (
        "REGINA: Use a sweet smell\\n",
        "properly and they come to\\l",
        "you on their own.$",
    )),
    "Route118_Text_PerryIntro": (("FLY elegantly",), (
        "ROGERIO: The ones that fly\\n",
        "well. Nothing beats them.$",
    )),
    "Route118_Text_PerryDefeat": (("I crashed",), (
        "ROGERIO: Urgh. Down.$",
    )),
    "Route118_Text_PerryPostBattle": (("train mine better",), (
        "ROGERIO: Yours are good.\\p",
        "I'll have to work harder\\n",
        "with mine.$",
    )),
    "Route118_Text_ChesterIntro": (("Take flight",), (
        "CLOVIS: Up! Get up there!$",
    )),
    "Route118_Text_ChesterDefeat": (("did take flight",), (
        "CLOVIS: They went up, at\\n",
        "least.$",
    )),
    "Route118_Text_ChesterPostBattle": (("fly more freely",), (
        "CLOVIS: Stronger wings\\n",
        "means further from here.\\p",
        "That's what I want for\\n",
        "them.$",
    )),
    "Route118_Text_BarnyIntro": (("FISHERMAN", "raising the POKéMON I caught"), (
        "AMILCAR: I'm a FISHERMAN\\n",
        "and a TRAINER.\\p",
        "I'm raising what I pulled\\n",
        "out of this river.$",
    )),
    "Route118_Text_BarnyDefeat": (("doing okay in my",), (
        "AMILCAR: I thought the\\n",
        "training was going well.$",
    )),
    "Route118_Text_BarnyPostBattle": (("half measures",), (
        "AMILCAR: Fishing and\\n",
        "training at once.\\p",
        "Perhaps I've been doing\\n",
        "both by halves.$",
    )),
    "Route118_Text_WadeIntro": (("equipment is the key", "heart"), (
        "AMANCIO: A FISHERMAN needs\\n",
        "good tackle.\\p",
        "A TRAINER needs the team\\n",
        "and the nerve.$",
    )),
    "Route118_Text_WadeDefeat": (("beaten in heart",), (
        "AMANCIO: Out-nerved?\\n",
        "Me?$",
    )),
    "Route118_Text_WadePostBattle": (("fishing is a battle",), (
        "AMANCIO: Come to think of\\n",
        "it, a fish on the line is\\l",
        "a battle too.\\p",
        "Just a quieter one.$",
    )),
    "Route118_Text_DaltonIntro": (("melody rock your soul",), (
        "EDILSON: Let this get in\\n",
        "under your ribs.$",
    )),
    "Route118_Text_DaltonDefeat": (("La-lalala",), (
        "EDILSON: La-lalala...$",
    )),
    "Route118_Text_DaltonPostBattle": (("electric guitar", "heart-stirring"), (
        "EDILSON: An electric guitar\\n",
        "doesn't have to be loud.\\p",
        "Played softly it gets\\n",
        "somewhere else entirely.$",
    )),
    "Route118_Text_DaltonRegister": (("compose better melodies",), (
        "EDILSON: When I've written\\n",
        "something better, come\\l",
        "and hear it.$",
    )),
    "Route118_Text_DaltonRematchIntro": (("deliver it to your soul",), (
        "EDILSON: Something mine\\n",
        "and I wrote.\\p",
        "For you. Listen.$",
    )),
    "Route118_Text_DaltonRematchDefeat": (("La-lalala",), (
        "EDILSON: La-lalala...$",
    )),
    "Route118_Text_DaltonPostRematch": (("emotions should reach",), (
        "EDILSON: What I'm feeling\\n",
        "goes down the strings.\\p",
        "It should reach you. It\\n",
        "usually does.$",
    )),
    "Route118_Text_DeandreIntro": (("POKéMON 1, 2, and 3",), (
        "ERASMO: Go! Number one!\\n",
        "Number two! Number three!$",
    )),
    "Route118_Text_DeandreDefeat": (("Are you okay",), (
        "ERASMO: Number one? Two?\\n",
        "Three? Are you all right?$",
    )),
    "Route118_Text_DeandrePostBattle": (("battle team", "copy me"), (
        "ERASMO: I've got a numbered\\n",
        "team. Isn't that good?\\p",
        "Copy it if you like.\\n",
        "I don't mind.$",
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
        masked = masked[:start] + '\t.string "<ARAUNA_RIVER_RIDGE_EN>"\n\n' + masked[end:]
    return masked


def validate_rendered(source: str, rendered: str) -> None:
    if mask(source) != mask(rendered):
        raise ValueError("non-dialogue structure changed while rendering")

    forbidden = ("Ufufufufu", "Abelhinha", "shivery and shaky",
                 "just a pretty face", "born genius")
    for label in TARGETS:
        body = block_pattern(label).search(rendered).group("body")
        for token in forbidden:
            if token in body:
                raise ValueError(f"{label}: vanilla voice survived: {token}")

    # TAIS taught IVA. If either stops saying so the pairing is gone.
    pair = "".join("".join(p) for label, (_, p) in TARGETS.items()
                   if "Tyra" in label or "Ivy" in label)
    if "TAIS" not in pair or "IVA" not in pair:
        raise ValueError("Route 114 lost the mentor and junior pairing")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Render the Route 114, 115 and 118 trainers in English.")
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
    print(f"River and ridge trainers English renderer OK: {len(TARGETS)} blocks "
          f"across Routes 114, 115 and 118.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
