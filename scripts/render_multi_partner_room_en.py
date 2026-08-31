#!/usr/bin/env python3
"""The sixty-eight people waiting to be asked to be your tag partner.

One room, sixty-eight trainers, and each of them says the same five things:
who they are, what the first of their two POKéMON is, what the second is and
will you team up, thank you, and never mind then. Eight hundred and forty
strings of it, all Emerald's, and the only thing separating any two of them
is the class they belong to and the way they take a refusal.

Written out by hand that is eight hundred and forty chances to give two
trainers the same sentence. So the room is a table: each entry is a class
name, the way that person shows off their pair, the way they ask, the way
they thank you and the way they take a no. The frame around them is written
once.

The pair itself is a seam. "...one {STR_VAR_2} with {STR_VAR_1} and" is a
separate block from "one {STR_VAR_2} with {STR_VAR_1}!", and the engine prints
them end to end as one sentence -- so the first must not close and the second
must not open. Vanilla has two phrasings of that seam and both are kept,
because a room of sixty-eight people who all phrase it identically is a room
that reads as one person.

Sixteen of them are the BATTLE TOWER apprentices, who also have two hundred
and eighty-eight lines of their own in data/text/apprentice.inc. They are the
same sixteen people, so this renderer checks its versions against the voices
declared there rather than inventing them twice.
"""
from __future__ import annotations

import argparse
import importlib.util
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools" / "arauna"))
from textbox import TextBox, glued  # noqa: E402

ROOM = (ROOT / "data" / "maps" / "BattleFrontier_BattleTowerMultiPartnerRoom"
        / "scripts.inc")
PREFIX = "BattleFrontier_BattleTowerMultiPartnerRoom_Text_"

# The slots hold a move name and a species name.
BOX = TextBox({"{STR_VAR_1}": 13, "{STR_VAR_2}": 11, "{STR_VAR_3}": 10}, width=34)

WITH = ("one {STR_VAR_2} with {STR_VAR_1} and", "one {STR_VAR_2} with {STR_VAR_1}.")
USING = ("one {STR_VAR_1}-using {STR_VAR_2}", "and one {STR_VAR_1}-using {STR_VAR_2}.")

# key -> (introduction, how they show the pair, how they ask,
#         how they thank you, how they take a no, seam style)
PARTNERS: dict[str, tuple[str, str, str, str, str, str]] = {
    "AromaLady": (
        "Pleased to meet you.|I'm {STR_VAR_1}. An AROMA LADY, if you like.",
        "I travel in the company of", "I hope they suit you.|Would you care to partner me?",
        "I'm honoured you said yes.|I'll go and register at once.",
        "It would be lovely if we could team up the next time we meet.",
        "with"),
    "BattleGirl": (
        "I'm BATTLE GIRL {STR_VAR_1}!",
        "I've been toughening up", "Like the look of that?|You and me, then?",
        "Thanks!|I'll get us registered right now!",
        "I thought we could have been the hardest pair in the building...",
        "using"),
    "Beauty": (
        "Hello!|I'm {STR_VAR_1}, and I'm a BEAUTY!",
        "Do you know what I've been raising?",
        "What do you think?|Shall we make a team of it?",
        "Wonderful!|I'll see to the registration now!",
        "What a shame!|The two of us would have been the best of them!",
        "with"),
    "BirdKeeper": (
        "I'm BIRD KEEPER {STR_VAR_1}!",
        "What have I got? I've got",
        "Wouldn't we make a decent team, the pair of us?",
        "Thanks!|I'll look after the registration!",
        "My POKéMON and I are strong. That's a letdown.",
        "with"),
    "BlackBelt": (
        "Hiyah!|I am BLACK BELT {STR_VAR_1}.",
        "For company I have",
        "Please, grant me this!|Let me stand beside you!",
        "Hiyah!|I shall register at once!",
        "I see... Then I shall hope for the next time we meet...",
        "using"),
    "BugCatcher": (
        "Hiya!|I'm BUG CATCHER {STR_VAR_1}!",
        "Look what I've got!",
        "So, listen!|Do you want to make a team?",
        "Got it!|I'll go and do the registration at the counter.",
        "Aww. My POKéMON are brilliant.|Don't come crying to me.",
        "with"),
    "BugManiac": (
        "Hello.|I'm {STR_VAR_1}, and I'm a BUG MANIAC.",
        "I found these myself, yes.",
        "Could I interest you in a team?",
        "Right! Understood!|I shan't be long registering!",
        "With the ones I found, we wouldn't have lost...",
        "with"),
    "Camper": (
        "I'm {STR_VAR_1}, and I'm a CAMPER!",
        "I've been raising",
        "Wouldn't it be good fun to team up?|I think it would!",
        "Right!|Off I go to register!",
        "Next time, then?|I want to be on your side.",
        "using"),
    "Collector": (
        "Hello. I'm {STR_VAR_1}.|I'm a COLLECTOR.",
        "The jewels of the collection are",
        "Handsome, aren't they?|We ought to be on a team together.",
        "Excellent!|Let's not waste the day. I'll register us both.",
        "Well, that's upsetting.|You don't appreciate what I have.",
        "with"),
    "CoolTrainerF": (
        "I'm COOLTRAINER {STR_VAR_1}!",
        "The team I've brought on is",
        "Does that sound all right?|Shall we be partners?",
        "Sounds good to me!|I'd better go and register.",
        "I was thinking what a hard team we'd have made...",
        "with"),
    "CoolTrainerM": (
        "I'm COOLTRAINER {STR_VAR_1}!",
        "What I've got on me is",
        "Not bad, eh?|Wouldn't we make a fine team?",
        "Good!|I'll have the registration done in no time!",
        "I thought we'd have made the best team in here.",
        "with"),
    "CyclingTriathleteF": (
        "I'm TRIATHLETE {STR_VAR_1}!",
        "What I've got...",
        "Please?|Will you make a team with me?",
        "Thanks!|I'll go and register at the counter.",
        "The two of us would have been hard to stop, I'm sure of it!",
        "with"),
    "CyclingTriathleteM": (
        "I'm TRIATHLETE {STR_VAR_1}!",
        "I've been riding out with a pair --",
        "We could be a team.|Wouldn't that be something?",
        "Thank you!|I'll go and register us. Right now.",
        "Aww, that's a pity. We'd have been the toughest pair going!",
        "with"),
    "DragonTamer": (
        "I'm DRAGON TAMER {STR_VAR_1}!",
        "The team I've been hardening up is",
        "How about it?|Want to be my partner?",
        "Right, I'll give it everything!|I'll go and register, shall I?",
        "You won't find many partners tougher than me!",
        "with"),
    "ExpertF": (
        "Hello, hello.|I'm {STR_VAR_1}, and I'm an EXPERT.",
        "I've raised mine thoroughly.",
        "Wouldn't you like to team up with me?",
        "Good, good.|I'll see to the registration directly.",
        "Perhaps we can make a team the next time we meet.",
        "with"),
    "ExpertM": (
        "Hm!|I am {STR_VAR_1}, and an EXPERT I am!",
        "The ones I have hardened are",
        "What do you say to a team with me?",
        "Hm!|I shall register us at once!|Let us both do well!",
        "I shall hope your choice proves the right one...",
        "with"),
    "Fisherman": (
        "Yo!|You know who I am?|I'm {STR_VAR_1} the FISHERMAN!",
        "I've got with me a team of",
        "So how about it?|Will you battle at my side?",
        "Good, good!|Leave it to me!|I'll go and register us now.",
        "We'd have matched up perfectly, too...",
        "using"),
    "Gentleman": (
        "Pleased to meet you.|I am {STR_VAR_1}, a GENTLEMAN.",
        "I am accompanied by",
        "Might I ask you to enter into a partnership with me?",
        "Ah. I thank you for the trust.|I shall see to the registration.",
        "That is most unfortunate...|I shall hope for another occasion...",
        "using"),
    "Guitarist": (
        "Yay-hey!|Call me GUITARIST {STR_VAR_1}!",
        "Have a look at the band!",
        "Yay-hey! Wild, isn't it?|We'll have to play a duet!",
        "Yay-hey! Right on!|I'll go and do the registration!",
        "My POKéMON play hard!|You'll be sorry, I tell you!",
        "with"),
    "HexManiac": (
        "Greetings...|I am HEX MANIAC {STR_VAR_1}...",
        "I bear with me",
        "I beseech you...|Join me...",
        "I thank you...|I shall register us...",
        "I so wanted to go with you...",
        "using"),
    "Hiker": (
        "Yahoo!|I'm HIKER {STR_VAR_1}!",
        "Know what I've got with me?",
        "Sounds good, eh?|Want to make a team?",
        "Yahoo!|I'll go and do the registering, then.",
        "I'd have liked to battle with you beside me.",
        "using"),
    "Kindler": (
        "Yo, there!|I'm KINDLER {STR_VAR_1}!",
        "Know what the training turned out?",
        "Well, what do you say?|Want to make a team?",
        "All right!|I'll get on with the registration.",
        "Promise you'll partner me the next time we run into each other.",
        "with"),
    "Lady": (
        "Glad to make your acquaintance.|I am {STR_VAR_1}, a LADY.",
        "I am accompanied by",
        "I hope I meet with your approval.|I should like you as my partner.",
        "I thank you sincerely.|I shall handle the registration.",
        "I'm quite sure you will regret not having me beside you.",
        "with"),
    "Lass": (
        "I'm {STR_VAR_1}, and I'm a LASS!",
        "What I've got is",
        "Will you be my partner?",
        "Thank you!|I'll go and do the registration!",
        "You don't want to be my partner?|You'll be sorry later!",
        "with"),
    "NinjaBoy": (
        "I'm NINJA BOY {STR_VAR_1}!",
        "My team is",
        "Let's be on a team together!",
        "Yes!|Let me go and register!",
        "You'll regret not having my POKéMON on your side!",
        "with"),
    "ParasolLady": (
        "Hello!|I'm PARASOL LADY {STR_VAR_1}!",
        "Escorting me just now are",
        "Aren't they fine?|Care to join us?",
        "Thanks so much!|I'll register at the counter.|Let's not let each "
        "other down!",
        "My POKéMON are tremendously strong. How disappointing...",
        "with"),
    "Picnicker": (
        "Hello!|I'm {STR_VAR_1}, and I'm a PICNICKER!",
        "The ones I take about with me are",
        "Would you like to join me on a team?",
        "Why, thank you!|I'll do the registration now.",
        "It would be nice if I could join you some other time.",
        "with"),
    "PkmnBreederF": (
        "Hiya! The name's {STR_VAR_1}!|I'm a POKéMON BREEDER!",
        "The ones I've raised are",
        "Sound interesting?|Shall we make a team, then?",
        "Right you are!|Leave the registration to me!",
        "You have to team up with me next time. All right?",
        "using"),
    "PkmnBreederM": (
        "How do you do? I'm {STR_VAR_1}, and I'm a POKéMON BREEDER!",
        "I've raised a couple of good ones!",
        "How about it?|Feel like making a team with me?",
        "Thank you kindly!|I'll take care of the registration, so wait here!",
        "I was looking forward to being your partner...",
        "with"),
    "PkmnRangerF": (
        "My name's {STR_VAR_1}.|I'm a POKéMON RANGER!",
        "Let me tell you about the team. I have",
        "How would you like to make a team with my little outfit?",
        "We'll be at our best!|I'll get the registration done quickly!",
        "I hope you'll choose my POKéMON next time.",
        "with"),
    "PkmnRangerM": (
        "Howdy. I'm {STR_VAR_1}.|I'm a POKéMON RANGER.",
        "Keeping me company are",
        "Don't you think we'd make an impressive pair?",
        "That's grand!|I'll deal with the registration now.",
        "Next time, choose my POKéMON, would you?",
        "using"),
    "PokefanF": (
        "I'm {STR_VAR_1}, and I'm proud to say I'm a POKéFAN.",
        "The darlings I've raised are",
        "Aren't they the sweetest things?|We ought to make a team!",
        "Thank you, dear!|I'll be off to register!",
        "My darlings are the best there are, I'll have you know. How "
        "annoying.",
        "with"),
    "PokefanM": (
        "Hello. I'm {STR_VAR_1}, and I'm a POKéFAN.",
        "I have with me just now",
        "Do you like what you see?|Why not be my partner?",
        "Thank you!|I'll look after the registration!",
        "My POKéMON are of the first order... A pity you can't see it.",
        "with"),
    "Pokemaniac": (
        "Heyo!|I'm {STR_VAR_1}, the POKéMANIAC!",
        "What does a man like me have? I have",
        "Let's do it!|We'll go through them as a pair!",
        "Good call!|I'll register the both of us!",
        "My POKéMON are brutal!|Don't blame me when you regret it!",
        "with"),
    "PsychicF": (
        "I'm {STR_VAR_1}.|I'm a PSYCHIC.",
        "My disciples are",
        "Does the idea of a partnership not intrigue you?",
        "Thank you.|I'll go and deal with the registration.",
        "I hope there will be another chance to make an alliance.",
        "with"),
    "PsychicM": (
        "I'm PSYCHIC {STR_VAR_1}!",
        "The two I've been raising are",
        "Would you like to make a team with me?",
        "Certainly!|I'll take care of the registration!",
        "If we meet again, that's when I'd like to team up with you.",
        "with"),
    "RichBoy": (
        "Yo! Let me tell you who I am!|I'm RICH BOY {STR_VAR_1}!",
        "Guess what I've got!",
        "I'm prepared to offer you a place on a team with me.",
        "Smart move!|I'll have the registration finished in no time!",
        "You'd turn down me, of all people?|You'll regret that, for certain!",
        "with"),
    "RuinManiac": (
        "Want to know who I am?|I'm {STR_VAR_1}, the RUIN MANIAC!",
        "The ones I have with me are",
        "Intriguing, eh?|How about you and I partner up?",
        "A sound decision!|I'll go and do the paperwork.",
        "Hmm...|I rather think my POKéMON are tough...",
        "with"),
    "RunningTriathleteF": (
        "Well, hello!|I'm TRIATHLETE {STR_VAR_1}!",
        "Want to know what I run with?",
        "Well?|Want to be on a team with me?",
        "Good going!|I'll be quick about the registration!",
        "You and me -- we'd have been the best of them. What a pity...",
        "with"),
    "RunningTriathleteM": (
        "Hey, there! My name's {STR_VAR_1}!|I'm a TRIATHLETE!",
        "I go out running with a durable pair --",
        "Not too shabby, eh?|We should be on a team together!",
        "All right!|I'll go and register in a flash!",
        "I really did want to battle beside you...",
        "with"),
    "Sailor": (
        "Ahoy, there!|I'm SAILOR {STR_VAR_1}!",
        "Let me show you my pride and joy!",
        "You're not going to turn me down, of course.|We'll team up, yes?",
        "I expected nothing less!|I'll go and register now.",
        "We'd have gone straight through them!|What a waste!",
        "with"),
    "SchoolKidF": (
        "I'm SCHOOL KID {STR_VAR_1}!",
        "My pair is",
        "May I please be your partner?",
        "Ooh, thank you!|I'll register at the counter right away!",
        "Please?|May I join you the next time?",
        "using"),
    "SchoolKidM": (
        "Good day!|I'm SCHOOL KID {STR_VAR_1}!",
        "What I've been raising is",
        "Not too bad, don't you think?|Would you care to make a team?",
        "Thank you very much!|I'll get the registration done.",
        "That's a pity...|I was hoping I might learn from you...",
        "with"),
    "SwimmerF": (
        "Hello. I'm SWIMMER {STR_VAR_1}.",
        "What I've trained is",
        "You and me. Let's make a team.",
        "That's good!|I'll register the two of us.",
        "If we meet again, you owe me a team!",
        "using"),
    "SwimmerM": (
        "Hello there! Hello!|I'm {STR_VAR_1}, and I'm a SWIMMER!",
        "Have a look at what I've raised!",
        "Good, aren't they?|It'd be good to make a team as well!",
        "Much obliged!|I'll get this registration business done!",
        "If we meet again you have to team up with me. You will, won't you?",
        "with"),
    "SwimmingTriathleteF": (
        "I'm the TRIATHLETE {STR_VAR_1}!",
        "My pair is",
        "What do you think?|We'd make a good team, I'd say.",
        "I like that answer!|I'll be quick about the registration!",
        "You'll give me another chance at a partnership, won't you?",
        "with"),
    "SwimmingTriathleteM": (
        "What's happening?|I'm {STR_VAR_1}, and I'm a TRIATHLETE.",
        "I've got a couple of decent ones.",
        "It'd be neat if we made a team, so how about it?",
        "Right on!|You wait while I register, all right?",
        "You'll let me join you next time. How's that?",
        "with"),
    "TuberF": (
        "Hello there!|I'm {STR_VAR_1}, and I'm a TUBER!",
        "I'll tell you what I have.",
        "May I please be on your team?",
        "Thank you!|I'll go and register us now!",
        "If we'd been partners, we could have been so strong!",
        "with"),
    "TuberM": (
        "Me?|I'm TUBER {STR_VAR_1}!",
        "What do I have with me?",
        "Hey?|You'll team up with me, won't you?",
        "Right!|I'll go and register!|Let's be excellent together!",
        "My POKéMON are tough, for certain...|A pity you don't want them.",
        "with"),
    "Youngster": (
        "Hello!|I'm YOUNGSTER {STR_VAR_1}!",
        "Want to know what I have?",
        "You'll be my partner, won't you?",
        "Yes!|I'll go and register, all right?",
        "Aww! With my POKéMON beside yours we'd have been unstoppable!",
        "with"),
}

# The class name each introduction has to keep, because it is how the room
# tells one stranger from another.
CLASS_NAMES = {
    "AromaLady": "AROMA LADY", "BattleGirl": "BATTLE GIRL", "Beauty": "BEAUTY",
    "BirdKeeper": "BIRD KEEPER", "BlackBelt": "BLACK BELT",
    "BugCatcher": "BUG CATCHER", "BugManiac": "BUG MANIAC", "Camper": "CAMPER",
    "Collector": "COLLECTOR", "CoolTrainerF": "COOLTRAINER",
    "CoolTrainerM": "COOLTRAINER", "CyclingTriathleteF": "TRIATHLETE",
    "CyclingTriathleteM": "TRIATHLETE", "DragonTamer": "DRAGON TAMER",
    "ExpertF": "EXPERT", "ExpertM": "EXPERT", "Fisherman": "FISHERMAN",
    "Gentleman": "GENTLEMAN", "Guitarist": "GUITARIST",
    "HexManiac": "HEX MANIAC", "Hiker": "HIKER", "Kindler": "KINDLER",
    "Lady": "LADY", "Lass": "LASS", "NinjaBoy": "NINJA BOY",
    "ParasolLady": "PARASOL LADY", "Picnicker": "PICNICKER",
    "PkmnBreederF": "POKéMON BREEDER", "PkmnBreederM": "POKéMON BREEDER",
    "PkmnRangerF": "POKéMON RANGER", "PkmnRangerM": "POKéMON RANGER",
    "PokefanF": "POKéFAN", "PokefanM": "POKéFAN", "Pokemaniac": "POKéMANIAC",
    "PsychicF": "PSYCHIC", "PsychicM": "PSYCHIC", "RichBoy": "RICH BOY",
    "RuinManiac": "RUIN MANIAC", "RunningTriathleteF": "TRIATHLETE",
    "RunningTriathleteM": "TRIATHLETE", "Sailor": "SAILOR",
    "SchoolKidF": "SCHOOL KID", "SchoolKidM": "SCHOOL KID",
    "SwimmerF": "SWIMMER", "SwimmerM": "SWIMMER",
    "SwimmingTriathleteF": "TRIATHLETE", "SwimmingTriathleteM": "TRIATHLETE",
    "TuberF": "TUBER", "TuberM": "TUBER", "Youngster": "YOUNGSTER",
}

# The apprentices are the same sixteen people as in data/text/apprentice.inc,
# one-based here and zero-based there. Their introduction names their mentor
# and their number; the rest is their own voice.
APPRENTICE_ASK = (
    "Snivel...|Please, please team up with me!",
    "Wowee! Be my partner, will you?",
    "Um... would you be my partner?",
    "...You wouldn't want me on your team. Would you?",
    "You'll have me, of course. Won't you?",
    "I've the time for this and little else. Shall we?",
    "A-hah! Team up with me! It'll be brilliant!",
    "Might I ask you to take me as your partner?",
    "Please -- can you grant me my wish?|I want to be on your team!",
    "Come on then, partner up with me. My luck's in today!",
    "Be my partner.|...And that isn't a lie, for once.",
    "So partner up with me, and we'll go through them, you and I!",
    "So take me on and let's begin!|Two of us make a better din!",
    "Ouch... So. Team up with me?",
    "Er... would you... be my partner?",
    "You may take me as your partner, if you are real.",
)
APPRENTICE_YES = (
    "Oh, really? You will?|Awesome! Wicked! Awoooh!|Oh... I'm sorry...|I'm "
    "so happy I'm crying...|I'll go and register. Don't go away!",
    "Wowee! I'll go and register!",
    "Oh... thank you.|I'll go and register us.",
    "...You will? Really?|...I'll go and register before you change your "
    "mind.",
    "Excellent!|I'll go and register us.",
    "Splendid. I'll register on the way past.",
    "A-hah! Wonderful!|I'll go and register at once!",
    "You have my thanks.|I shall see to the registration.",
    "Eek! I feel giddy!|Thank you!|I'll go and register us right away!",
    "Yeehaw! I'll go and register!",
    "You won't regret it.|...That one might be a lie. I'll go and register.",
    "Oh joy! Now watch me go -- I'll register us both below!",
    "Now that's a chord!|I'll register us and strike the first bar!",
    "Oof. Right. I'll go and register.",
    "Oh... th-thank you.|I'll go and register.",
    "Hm. Acceptable.|I shall register us.",
)
APPRENTICE_NO = (
    "Oh, b-but...|Sob... Waaaaah!",
    "Aww! But I'd have tried so hard!",
    "Oh... of course. I'm sorry to have asked.",
    "...I knew that. I did know that.",
    "What? But I'd have been useful!",
    "A pity. I'd made the time and everything.",
    "No way! Uh-uh! It was such a good idea!",
    "I quite understand. Forgive the imposition.",
    "Waaah! Have you no pity?|...Though that does make you cooler...",
    "Aw, no! And my luck was in, too!",
    "I don't mind at all.|...That's a lie.",
    "Oh no, oh no, you tell me go!|And now I've nowhere left to go!",
    "No? Then the song ends on a bum note, and I'll be singing it all day!",
    "Ouch. That's two things hurting now.",
    "Oh... no... I shouldn't have asked...",
    "Hm. Then you may not be real after all.",
)
APPRENTICE_INTRO = (
    "Um, my name's {STR_VAR_3}, and I'm {STR_VAR_1}'s no. {STR_VAR_2} "
    "apprentice.|Snivel...|I'm sorry! The nerves are making me cry...",
    "Wowee! I'm {STR_VAR_3}!|I'm {STR_VAR_1}'s no. {STR_VAR_2} apprentice!",
    "Um... I'm {STR_VAR_3}.|I'm {STR_VAR_1}'s no. {STR_VAR_2} apprentice.",
    "I'm... {STR_VAR_3}.|{STR_VAR_1}'s no. {STR_VAR_2} apprentice. Not that "
    "it matters.",
    "I'm {STR_VAR_3}!|{STR_VAR_1}'s no. {STR_VAR_2} apprentice, that's me!",
    "{STR_VAR_3}. Busy, but I'm also {STR_VAR_1}'s no. {STR_VAR_2} "
    "apprentice.",
    "A-hah! I'm {STR_VAR_3}!|{STR_VAR_1}'s no. {STR_VAR_2} apprentice!",
    "I am {STR_VAR_3}, {STR_VAR_1}'s no. {STR_VAR_2} apprentice.|A pleasure.",
    "Eek! You spoke to me!|I... I can hardly stand it!|I'm {STR_VAR_3}! "
    "{STR_VAR_1}'s no. {STR_VAR_2} apprentice!",
    "Whoa, my luck's in!|I'm {STR_VAR_3}, {STR_VAR_1}'s no. {STR_VAR_2} "
    "apprentice!",
    "I'm {STR_VAR_3}, the POKéMON CHAMPION.|...I'm {STR_VAR_1}'s no. "
    "{STR_VAR_2} apprentice. That part's true.",
    "Ahoy! {STR_VAR_3}'s the name, and rhyming is my game!|I'm {STR_VAR_1}'s "
    "no. {STR_VAR_2}, and that's my claim!",
    "Hey, hey! {STR_VAR_3} today!|{STR_VAR_1}'s no. {STR_VAR_2}, if I may!",
    "Ouch... I'm {STR_VAR_3}.|{STR_VAR_1}'s no. {STR_VAR_2} apprentice.",
    "Er... um... I'm {STR_VAR_3}...|{STR_VAR_1}'s no. {STR_VAR_2} "
    "apprentice...",
    "I am {STR_VAR_3}.|{STR_VAR_1}'s no. {STR_VAR_2} apprentice, assuming "
    "any of this is real.",
)
APPRENTICE_SHOW = "On {STR_VAR_3}'s advice I trained"

# Seven of the sixteen have a noise that is theirs and nobody else's. Those
# are checkable across the two files: the token has to appear both in what
# they say here and in the cheer declared in render_apprentice_en.py. The
# other nine are quiet enough that no single word identifies them, and a
# check that guessed at one would only fire on the wrong thing.
SIGNATURES: tuple[str | None, ...] = (
    "Awesome", "Wowee", None, None, None, "Splendid", "A-hah",
    None, "Eek", "Yeehaw", None, "joy", "chord", "Oof", None, None,
)

KINDS = ("Intro", "Mon1", "Mon2Ask", "Accept", "Reject")


def build() -> dict[str, tuple[str, ...]]:
    blocks: dict[str, tuple[str, ...]] = {}

    def add(who: str, intro, show: str, ask: str, yes: str, no: str,
            style: str) -> None:
        first, second = WITH if style == "with" else USING
        # The pair continues the sentence the lead-in started, unless the
        # lead-in closed one -- then it begins a new sentence and needs the
        # capital. Vanilla makes the same distinction, and getting it wrong
        # prints a lowercase word at the start of a line.
        if show.rstrip().endswith((".", "!", "?")):
            first = first[0].upper() + first[1:]
        blocks[f"{who}Intro"] = intro if isinstance(intro, tuple) else (intro,)
        blocks[f"{who}Mon1"] = (f"{show} {first}",)
        blocks[f"{who}Mon2Ask"] = (second, ask)
        blocks[f"{who}Accept"] = (yes,)
        blocks[f"{who}Reject"] = (no,)

    for who, (intro, show, ask, yes, no, style) in PARTNERS.items():
        add(who, intro, show, ask, yes, no, style)

    for index in range(16):
        add(f"Apprentice{index + 1}", APPRENTICE_INTRO[index],
            APPRENTICE_SHOW, APPRENTICE_ASK[index], APPRENTICE_YES[index],
            APPRENTICE_NO[index], "with" if index % 2 == 0 else "using")
    # The two apprentices the engine never reaches keep a voice anyway, so
    # that a future script that does reach them finds something written.
    for slot, index in (("UnusedApprentice1", 0), ("UnusedApprentice2", 8)):
        add(slot, APPRENTICE_INTRO[index], APPRENTICE_SHOW,
            APPRENTICE_ASK[index], APPRENTICE_YES[index],
            APPRENTICE_NO[index], "with")
    return blocks


PARAGRAPHS = build()
TARGETS = tuple(PARAGRAPHS)


def block_pattern(label: str) -> re.Pattern[str]:
    return re.compile(
        rf"(?ms)^{re.escape(PREFIX + label)}::?\n(?P<body>.*?)"
        rf"(?=^[A-Za-z0-9_]+(?:::|:)(?:\n|$)|\Z)"
    )


def payloads() -> dict[str, tuple[str, ...]]:
    composed = {}
    for label, paragraphs in PARAGRAPHS.items():
        paragraphs = tuple(
            p.replace("POKéMON BREEDER", glued("POKéMON BREEDER"))
             .replace("POKéMON RANGER", glued("POKéMON RANGER"))
             .replace("POKéMON CHAMPION", glued("POKéMON CHAMPION"))
             .replace("AROMA LADY", glued("AROMA LADY"))
             .replace("BATTLE GIRL", glued("BATTLE GIRL"))
             .replace("BIRD KEEPER", glued("BIRD KEEPER"))
             .replace("BLACK BELT", glued("BLACK BELT"))
             .replace("BUG CATCHER", glued("BUG CATCHER"))
             .replace("BUG MANIAC", glued("BUG MANIAC"))
             .replace("DRAGON TAMER", glued("DRAGON TAMER"))
             .replace("HEX MANIAC", glued("HEX MANIAC"))
             .replace("NINJA BOY", glued("NINJA BOY"))
             .replace("PARASOL LADY", glued("PARASOL LADY"))
             .replace("RICH BOY", glued("RICH BOY"))
             .replace("RUIN MANIAC", glued("RUIN MANIAC"))
             .replace("SCHOOL KID", glued("SCHOOL KID"))
            for p in paragraphs)
        composed[label] = BOX.compose(paragraphs)
    return composed


def render(source: str) -> str:
    composed = payloads()
    rendered = source
    for label in TARGETS:
        matches = list(block_pattern(label).finditer(rendered))
        if len(matches) != 1:
            raise ValueError(f"{label}: expected one text block, found {len(matches)}")
        if ".string" not in matches[0].group("body"):
            raise ValueError(f"{label}: target contains no .string payload")
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
        masked = masked[:start] + '\t.string "<ARAUNA_MULTI_PARTNER_EN>"\n\n' + masked[end:]
    return masked


def validate_slots(source: str) -> None:
    composed = payloads()
    for label in TARGETS:
        available = set(re.findall(r"\{[A-Z_0-9]+\}",
                                   block_pattern(label).search(source).group("body")))
        used = set(re.findall(r"\{[A-Z_0-9]+\}", "".join(composed[label])))
        if used - available:
            raise ValueError(
                f"{label}: uses {sorted(used - available)}, which the engine "
                f"does not fill here; the source uses {sorted(available)}")


def apprentice_voices() -> tuple[dict[str, str], ...]:
    spec = importlib.util.spec_from_file_location(
        "apprentice", ROOT / "scripts" / "render_apprentice_en.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.VOICES


def validate_rendered(source: str, rendered: str) -> None:
    if mask(source) != mask(rendered):
        raise ValueError("non-dialogue structure changed while rendering")

    composed = payloads()

    # The pair is one sentence split across two blocks the engine prints end
    # to end. The first may not close it and the second may not open one.
    for label in TARGETS:
        first = composed[f"{label[:-4]}Mon1"][-1] if label.endswith("Mon1") else None
        if first is None:
            continue
        if first.rstrip("$").rstrip().endswith((".", "!", "?")):
            raise ValueError(f"{label}: closes a sentence the next block finishes")
    for label in TARGETS:
        if not label.endswith("Mon2Ask"):
            continue
        opener = composed[label][0]
        if not opener.startswith(("one ", "and one ")):
            raise ValueError(
                f"{label}: must continue the previous block, not start a new "
                f"sentence: {opener!r}")

    # A room of sixty-eight strangers who all phrase things the same way is
    # a room the player reads as one person.
    for kind in ("Accept", "Reject"):
        lines = [ "".join(composed[f"{who}{kind}"]) for who in PARTNERS ]
        if len(set(lines)) != len(lines):
            raise ValueError(f"two partners give the same {kind}")

    # Each introduction still has to say which class the stranger belongs to.
    for who, name in CLASS_NAMES.items():
        flat = re.sub(r"\\[npl]", " ", "".join(composed[f"{who}Intro"]))
        if name not in flat:
            raise ValueError(f"{who}: the introduction dropped {name}")

    # The sixteen apprentices are the sixteen from data/text/apprentice.inc.
    # Their noise of pleasure here has to be the one declared there.
    voices = apprentice_voices()
    if len(voices) != 16:
        raise ValueError("the apprentice renderer no longer declares sixteen voices")
    for index, voice in enumerate(voices):
        signature = SIGNATURES[index]
        if signature is None:
            continue
        if signature.lower() not in APPRENTICE_YES[index].lower():
            raise ValueError(
                f"apprentice {index + 1}: lost {signature!r}, which is how "
                f"they sound in this room")
        if signature.lower() not in voice["cheer"].lower():
            raise ValueError(
                f"apprentice {index + 1}: {signature!r} no longer matches the "
                f"cheer in render_apprentice_en.py -- the same person now "
                f"sounds like two people in two files")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Render the multi battle partner room in English.")
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--in-place", action="store_true")
    args = parser.parse_args()
    if args.check and args.in_place:
        parser.error("use either --check or --in-place")

    source = ROOM.read_text(encoding="utf-8")
    validate_slots(source)
    rendered = render(source)
    validate_rendered(source, rendered)

    if args.in_place:
        ROOM.write_text(rendered, encoding="utf-8")
    print(f"Multi partner room English renderer OK: {len(TARGETS)} blocks.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
