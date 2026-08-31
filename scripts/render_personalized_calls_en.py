#!/usr/bin/env python3
"""The sixty-four calls from the trainers who want a rematch.

These are the people you beat once on a road somewhere and who kept your
number. The engine picks one of these blocks per caller and fills in the
name, so the writing has to work for a hiker on SERRA DA CINZA and for a
swimmer off ROUTE 108 alike -- which is why they are about weather, work
and grudges rather than about anyone in particular.

{STR_VAR_2} is not free. src/match_call.c decides, per block, whether the
second slot holds a map name, a species from the caller's party, or a
species from the caller's route, and most blocks are given nothing at all.
Putting {STR_VAR_2} in a block that was never handed one prints garbage,
so WITH_SECOND_VAR below is checked against the payloads.

No payload names a species outright: the dex is generated, and a line
naming a creature would be wrong the next time it is.
"""
from __future__ import annotations

import argparse
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CALLS = ROOT / "data" / "text" / "match_call.inc"
MAX_VISIBLE_WIDTH = 36
NAME_SLOT = "XXXXXXXXXX"
CONTROL_RE = re.compile(r"\\[npl]")
PLACEHOLDER_RE = re.compile(r"\{[^}]+\}")

# The blocks src/match_call.c gives a second string to. Every other block
# gets STRS_NORMAL_MSG, whose second slot is STR_NONE.
WITH_SECOND_VAR = frozenset({
    "MatchCall_PersonalizedText1",   # STR_MAP_NAME
    "MatchCall_PersonalizedText13",  # STR_SPECIES_IN_ROUTE
    "MatchCall_PersonalizedText18",  # STR_SPECIES_IN_PARTY
    "MatchCall_PersonalizedText28",  # STR_SPECIES_IN_PARTY
    "MatchCall_PersonalizedText29",  # STR_SPECIES_IN_PARTY
    "MatchCall_PersonalizedText42",  # STR_SPECIES_IN_PARTY
    "MatchCall_PersonalizedText44",  # STR_SPECIES_IN_PARTY
    "MatchCall_PersonalizedText51",  # STR_MAP_NAME
    "MatchCall_PersonalizedText52",  # STR_SPECIES_IN_PARTY
    "MatchCall_PersonalizedText55",  # STR_MAP_NAME
})

TARGETS: dict[str, tuple[tuple[str, ...], tuple[str, ...]]] = {
    "MatchCall_PersonalizedText1": (("mountain-loving", "appreciate the mountains"), (
        "It's me, the one who loves the\\n",
        "high ground -- {STR_VAR_1}!\\p",
        "Have you come around to the\\n",
        "serra since we met?\\p",
        "I hardly ever see you up here.\\p",
        "Next time, let's meet somewhere\\n",
        "near {STR_VAR_2}.$",
    )),
    "MatchCall_PersonalizedText2": (("about a strong TRAINER", "everyone will admire"), (
        "This is {STR_VAR_1}.\\n",
        "Good to hear you.\\p",
        "I was telling a new TRAINER\\n",
        "about you today.\\p",
        "About someone who carries a\\n",
        "team well and doesn't hurry it.\\p",
        "Be the sort people talk about\\n",
        "like that. See you around!$",
    )),
    "MatchCall_PersonalizedText3": (("sweet aromas", "burst into bloom"), (
        "Hello! {STR_VAR_1} here.\\p",
        "Where I'm standing it smells of\\n",
        "BERRIES and wet earth.\\p",
        "Someone planted a row here and\\n",
        "then simply let it go on.\\p",
        "Come by sometime!$",
    )),
    "MatchCall_PersonalizedText4": (("Thirty years of exploration", "ruins to explore"), (
        "Hello! Thirty years of digging,\\n",
        "{STR_VAR_1} at your service!\\p",
        "Word is you've been all over\\n",
        "the region and then some.\\p",
        "Found any new ruins? If you\\n",
        "have, you must tell me!\\p",
        "Now, excuse me. There is stone\\n",
        "here that wants moving.$",
    )),
    "MatchCall_PersonalizedText5": (("Looking at waves from the beach", "getting hungry"), (
        "It's {STR_VAR_1}!\\p",
        "Know what I'm doing today?\\n",
        "Watching the water, that's what!\\p",
        "Sigh... The light comes off it\\n",
        "all silver. Best view anywhere.\\l",
        "I'm getting hungry, so bye-bye!$",
    )),
    "MatchCall_PersonalizedText6": (("Munch-chew", "fully fueled"), (
        "Munch-chew...\\n",
        "Oh, hi. It's {STR_VAR_1}.\\l",
        "I always eat better on sand.\\p",
        "My team and I are doing fine.\\n",
        "Fed and ready, the both of us!\\l",
        "I'm going for a swim. Bye!$",
    )),
    "MatchCall_PersonalizedText7": (("whole COOLTRAINER thing", "grin and bear it"), (
        "Hello, this is {STR_VAR_1}...\\p",
        "I've gone a little tired of the\\n",
        "whole COOLTRAINER business...\\p",
        "Everyone decides I'm a perfect\\n",
        "TRAINER, and then I spend my\\l",
        "days being what they decided.\\p",
        "But I suppose that comes with\\n",
        "the title.\\p",
        "So I'll put my head down...\\n",
        "and get on with it.\\p",
        "You're the only one I'd say\\n",
        "this out loud to.\\p",
        "Next time we meet, don't worry.\\n",
        "I won't complain!$",
    )),
    "MatchCall_PersonalizedText8": (("Yahoo, it's", "you as the target"), (
        "Yahoo, it's {STR_VAR_1}!\\n",
        "How are you keeping?\\p",
        "I've been raising my team with\\n",
        "you in mind the whole time.\\p",
        "I don't plan to lose when we\\n",
        "battle again.\\p",
        "Isn't it good to have TRAINER\\n",
        "friends? Let's meet again!$",
    )),
    "MatchCall_PersonalizedText9": (("walk away quickly", "Giggle"), (
        "It's {STR_VAR_1}...\\n",
        "Just now, behind you...\\l",
        "Wasn't there something...?\\p",
        "The ones who sleep at\\n",
        "MEMORIAL DOS NOMES have been\\l",
        "talking about you...\\p",
        "You should walk on and not\\n",
        "turn around, not once...\\p",
        "Giggle...\\n",
        "Farewell...$",
    )),
    "MatchCall_PersonalizedText10": (("at a distance", "have my father"), (
        "This is {STR_VAR_1}.\\n",
        "How do you do?\\p",
        "Isn't it a fine thing, that we\\n",
        "can talk across all that road?\\p",
        "Before this, if I wanted to\\n",
        "speak to anyone, someone had to\\l",
        "drive me there.\\p",
        "I should go now.\\n",
        "I'm glad we talked.$",
    )),
    "MatchCall_PersonalizedText11": (("I get lost", "All that tall grass"), (
        "It's {STR_VAR_1}!\\n",
        "Will you hear me out?\\p",
        "I love the RESERVA ARAUNA, but\\n",
        "every time I go in, I get lost.\\p",
        "All that tall grass, and it\\n",
        "goes on and on and on!\\p",
        "There. I feel better for saying\\n",
        "it out loud.\\p",
        "Right, I'm going back in.\\n",
        "Catch you!$",
    )),
    "MatchCall_PersonalizedText12": (("I am rich, yes", "formal dinner"), (
        "Hello, {STR_VAR_1} here.\\n",
        "Yes, correct, I am rich, yes.\\p",
        "I should tell you my fortune\\n",
        "has grown since we last met.\\p",
        "What is more, my team has grown\\n",
        "stronger along with it.\\p",
        "I can't shake the feeling that\\n",
        "the world was arranged for me.\\p",
        "No, no, say nothing!\\n",
        "Everyone knows it's true!\\p",
        "You must excuse me. There is a\\n",
        "dinner I am expected at.$",
    )),
    "MatchCall_PersonalizedText13": (("Ufufufufu", "catching the winner"), (
        "Ufufufufu...\\n",
        "It's me, {STR_VAR_1}...\\p",
        "Can you guess what I'm\\n",
        "watching just now?\\p",
        "A pair of {STR_VAR_2}, fighting.\\p",
        "Maybe I'll catch whichever one\\n",
        "is still standing. Ufufufu...\\p",
        "I... I'm busy now.\\n",
        "I have to go.$",
    )),
    "MatchCall_PersonalizedText14": (("bored of the NAVIO PERDIDO", "the man next"), (
        "Oh, it's {STR_VAR_1}!\\p",
        "I was just thinking I've had my\\n",
        "fill of the NAVIO PERDIDO.\\p",
        "But I'm here already, and I\\n",
        "still owe you one loss, so I'll\\l",
        "hang about a while longer.\\p",
        "If you feel like it, come and\\n",
        "find me.\\p",
        "Today's the day I finally call\\n",
        "out the fellow next door.\\p",
        "Be seeing you!$",
    )),
    "MatchCall_PersonalizedText15": (("The man of the sea", "giant surf rising"), (
        "I'm {STR_VAR_1}!\\n",
        "The man of the sea!\\p",
        "You know what I think?\\p",
        "The TRAINERS out on the water\\n",
        "are the hardest of the lot!\\p",
        "You ought to learn from me and\\n",
        "train where it's deep...\\p",
        "Whoa, here comes a big one!\\p",
        "That's good training weather!\\n",
        "Sorry, but I have to go!$",
    )),
    "MatchCall_PersonalizedText16": (("teaching karate", "Ugwaah"), (
        "It's {STR_VAR_1}! Listen, I've\\n",
        "been teaching my team karate.\\p",
        "Now they're better at it than\\n",
        "I am! All I do these days is\\l",
        "lose to them!\\p",
        "But even if I lose to POKéMON,\\n",
        "I won't lose to another\\l",
        "TRAINER, no sir!\\p",
        "We have to battle again!\\n",
        "Ugwaah!$",
    )),
    "MatchCall_PersonalizedText17": (("travels unwinding", "riffs in my head"), (
        "It's me, {STR_VAR_1}.\\n",
        "How's the road treating you?\\p",
        "...Whoa, is that right?\\n",
        "That's something, that is.\\p",
        "I could get a song out of one\\n",
        "of your days, I reckon.\\p",
        "...Oh, hey. It's coming.\\n",
        "I can hear the riff already.\\p",
        "I'd better write it down before\\n",
        "it goes. Later!$",
    )),
    "MatchCall_PersonalizedText18": (("Hear my new song", "Repeat chorus, fade"), (
        "This is {STR_VAR_1}...\\n",
        "Hear my new song.\\p",
        "Ai, ai, {STR_VAR_2}, {STR_VAR_2},\\n",
        "why do you go where I can't?\\l",
        "Ai, ai, {STR_VAR_2}, {STR_VAR_2},\\l",
        "take me along when you go...\\p",
        "And it fades out there.\\n",
        "Bye!$",
    )),
    "MatchCall_PersonalizedText19": (("the camping expert", "let's go camping"), (
        "I'm {STR_VAR_1}, you know --\\n",
        "the one who knows camps!\\p",
        "When we battled, I couldn't\\n",
        "help but lose to you.\\p",
        "Camping is where my talent is.\\n",
        "Battling never was.\\p",
        "But win or lose, I like a match\\n",
        "with a fire going nearby.\\p",
        "Battle us again, all right?\\n",
        "And bring a tent!$",
    )),
    "MatchCall_PersonalizedText20": (("climb other mountains", "ladies like on SERRA DA CINZA"), (
        "It's me, me, {STR_VAR_1}!\\p",
        "I'd like to climb something\\n",
        "other than this, to be honest.\\p",
        "But I doubt any other slope has\\n",
        "the company SERRA DA CINZA has.\\p",
        "If you know a mountain with\\n",
        "better company, tell me!\\p",
        "Ehehehe, see you around!$",
    )),
    "MatchCall_PersonalizedText21": (("It's {STR_VAR_1}…", "That's all today"), (
        "... ... ... ... ...\\n",
        "... ... ... ... ...\\l",
        "It's {STR_VAR_1}...\\p",
        "... ... ... ... ...\\n",
        "... ... ... ... ...\\l",
        "That's all today...$",
    )),
    "MatchCall_PersonalizedText22": (("feeling I would chat", "by day and by night"), (
        "This is {STR_VAR_1}. Today I\\n",
        "had a feeling we would speak.\\p",
        "My wish to beat you grows by\\n",
        "day and by night.\\p",
        "You have someone like that too,\\n",
        "don't you? I wish it were me...\\p",
        "Thank you for hearing me out.\\n",
        "See you!$",
    )),
    "MatchCall_PersonalizedText23": (("I can sometimes sense", "waiting for your visit"), (
        "It's {STR_VAR_1}.\\p",
        "When a strong TRAINER passes\\n",
        "nearby, I can feel it somehow.\\p",
        "Did you come by here,\\n",
        "{PLAYER}{KUN}? Perhaps that was you.\\p",
        "I'll be waiting for your visit.\\n",
        "Bye!$",
    )),
    "MatchCall_PersonalizedText24": (("traveled around the world", "dazzling"), (
        "Hello, this is {STR_VAR_1}.\\n",
        "You sound well, {PLAYER}{KUN}.\\p",
        "I have travelled a great deal,\\n",
        "but I must say this region has\\l",
        "taken hold of me.\\p",
        "I mean to stay a while yet.\\n",
        "Perhaps we'll meet again?\\p",
        "I have not forgotten how you\\n",
        "handled that battle.\\p",
        "I do hope for a rematch.$",
    )),
    "MatchCall_PersonalizedText25": (("chewed me out in class", "TRAINER'S SCHOOL tomorrow"), (
        "Snivel... It's... {STR_VAR_1}...\\n",
        "...Sob...\\p",
        "DALVA took me apart in class\\n",
        "today.\\p",
        "But I don't dislike her for it.\\p",
        "DALVA tells me exactly what I\\n",
        "got wrong, so I can fix it.\\p",
        "You bet I'm going back to the\\n",
        "TRAINER'S SCHOOL tomorrow!\\p",
        "See you later!$",
    )),
    "MatchCall_PersonalizedText26": (("let me battle with her", "really focus and work"), (
        "It's {STR_VAR_1}!\\p",
        "DALVA let me battle her\\n",
        "yesterday.\\p",
        "The result was what you'd\\n",
        "guess, like you needed to ask.\\p",
        "But I was glad she would even\\n",
        "stand across from me!\\p",
        "You wouldn't believe how much\\n",
        "more I think of her now!\\p",
        "I'm going to work at this\\n",
        "properly. I'd better go!$",
    )),
    "MatchCall_PersonalizedText27": (("junior", "buy the bread as punishment"), (
        "Hi, it's ANA! I've got my\\n",
        "little partner DUDA with me\\l",
        "again today.\\p",
        "I love looking after DUDA and\\n",
        "our POKéMON. They're so sweet!\\p",
        "I'd keep the whole lot of them\\n",
        "like family if I could!\\p",
        "Oh, hi, DUDA!\\n",
        "Did you get the bread?\\p",
        "Huh? No, no, I don't treat you\\n",
        "like a servant!\\p",
        "You lost the match, so buying\\n",
        "the bread is the forfeit!\\p",
        "I'd never treat you like that,\\n",
        "DUDA! You're far too dear!\\p",
        "I have to go now.\\n",
        "It's time we ate!$",
    )),
    "MatchCall_PersonalizedText28": (("from the FAN CLUB", "picture of cuteness"), (
        "I love POKéMON!\\n",
        "{STR_VAR_1}, of the FAN CLUB!\\p",
        "You have to hear this!\\n",
        "My sweet POKéMON...\\p",
        "Snort! Wahaha!\\n",
        "No, I can't say! It's a secret!\\l",
        "It's too dear for words!\\p",
        "Oh, my sweet {STR_VAR_2} is\\n",
        "begging for a {POKEBLOCK}!\\p",
        "The very picture of it!\\p",
        "Sorry, I can't talk now!\\n",
        "You'll hear the rest next time!$",
    )),
    "MatchCall_PersonalizedText29": (("Ohoho!", "leaps straight into my arms"), (
        "Ohoho!\\p",
        "This is {STR_VAR_1}! I can't\\n",
        "wait to tell you about my dear\\l",
        "one!\\p",
        "You must hear this. It is about\\n",
        "my darling {STR_VAR_2}.\\p",
        "Whenever anyone picks it up,\\n",
        "it leaps straight back to me!\\p",
        "Oh... Oh... Could there be\\n",
        "anything sweeter?\\p",
        "Oh, it is heaven itself!\\p",
        "I'm so glad I could share a\\n",
        "little of it with you.\\p",
        "Well, I must be going.\\n",
        "Bye, now!$",
    )),
    "MatchCall_PersonalizedText30": (("People call me an EXPERT", "deep and profound"), (
        "I am... {STR_VAR_1}.\\n",
        "People call me an EXPERT.\\p",
        "But I know one thing.\\n",
        "I could not have become an\\l",
        "EXPERT on my own strength.\\p",
        "Only with POKéMON beside them\\n",
        "does a TRAINER become anything.\\p",
        "Humph! I believe I have said\\n",
        "something worth hearing!\\p",
        "I'll leave you on that note!$",
    )),
    "MatchCall_PersonalizedText31": (("hot-spring tub", "in your old age"), (
        "It's {STR_VAR_1}.\\n",
        "Good to hear from you!\\p",
        "I feel new again, sitting in\\n",
        "this hot water up to my chin.\\p",
        "I have battled a good many\\n",
        "young TRAINERS since we met,\\l",
        "and you are still the best.\\p",
        "You'll be an EXPERT yourself\\n",
        "one day! Ohohoho...$",
    )),
    "MatchCall_PersonalizedText32": (("my shorts seem to", "icky and coarse"), (
        "Yay! This is {STR_VAR_1}!\\n",
        "What's up?\\p",
        "It might be my imagination, but\\n",
        "when I win, my shorts seem to\\l",
        "feel better. Materially.\\p",
        "What do I mean by that?\\n",
        "It's hard to put into words...\\l",
        "How would I say it now...\\l",
        "My shorts feel silkier!\\p",
        "And when I battled you,\\n",
        "{PLAYER}{KUN}, they felt rough and itchy.\\p",
        "... ... ... ... ...\\n",
        "You didn't believe that, did\\l",
        "you? Ehehehe, that's all! Bye!$",
    )),
    "MatchCall_PersonalizedText33": (("fishing with wild", "new fishing spots"), (
        "Ahoy!\\n",
        "{STR_VAR_1} here!\\p",
        "Still fishing, still with no\\n",
        "sense about it at all!\\p",
        "Are there places to fish other\\n",
        "than the sea and the rivers?\\p",
        "I get these urges to drop a\\n",
        "line just about anywhere!\\p",
        "Oh, blast it!\\n",
        "My line's in a knot!\\p",
        "Got to go!\\n",
        "Find me some new water!$",
    )),
    "MatchCall_PersonalizedText34": (("always been placid", "Take it casual"), (
        "Hey, there! It's {STR_VAR_1}.\\n",
        "Taking it easy?\\p",
        "Ever since I was small, you\\n",
        "know, I've been the slow sort.\\p",
        "I never had it in me to fret\\n",
        "or rush at things.\\p",
        "And wouldn't you know it, here\\n",
        "I am, a TRIATHLETE.\\p",
        "You can't tell where life will\\n",
        "put you, if you follow me.\\p",
        "You're a TRAINER now, but who\\n",
        "knows what comes after?\\p",
        "Picture yourself teaching, or\\n",
        "painting. Something, eh?\\p",
        "But, hey, be easy. Take it\\n",
        "slow. See you around.$",
    )),
    "MatchCall_PersonalizedText35": (("cycling is my first love", "CYCLING ROAD record"), (
        "This is {STR_VAR_1}!\\n",
        "I'm on the bike right now.\\p",
        "I like swimming and running,\\n",
        "but the bike came first.\\p",
        "It makes my whole body feel as\\n",
        "though I were part of the wind.\\p",
        "Like flying, near enough!\\p",
        "Right! Today I take the record\\n",
        "on the CYCLING ROAD!\\p",
        "You should have a go too!\\n",
        "See you!$",
    )),
    "MatchCall_PersonalizedText36": (("middle of a triathlon", "as if we shared a heart"), (
        "Yo, this is {STR_VAR_1}! I'm\\n",
        "in the middle of a triathlon!\\p",
        "But I've always got a minute\\n",
        "to talk, me!\\p",
        "Working out alongside POKéMON\\n",
        "feels mighty good!\\p",
        "Not a word between us and we\\n",
        "go as if we shared a heart.\\p",
        "It lifts a person!\\p",
        "Gasp... Talking while running...\\n",
        "I'm running down...\\l",
        "Gasp... Have... to... go...$",
    )),
    "MatchCall_PersonalizedText37": (("high-altitude training", "oxygen starved"), (
        "Hi, it's {STR_VAR_1}.\\n",
        "If you want wind in your lungs,\\l",
        "train high up. That's the way.\\p",
        "Try running along a ridge.\\n",
        "You'll be gasping in no time!\\p",
        "I'm short of air myself!\\n",
        "See you!$",
    )),
    "MatchCall_PersonalizedText38": (("can't seem to reach EVERGRANDE", "going in circles"), (
        "Oh, it's {STR_VAR_1}, hello.\\p",
        "I've been swimming for days and\\n",
        "I still haven't reached the\\l",
        "ESTR. JURAMENTO.\\p",
        "Maybe I've been going in\\n",
        "circles all this time.\\p",
        "No, no, that can't be it.\\n",
        "Wahahaha.\\l",
        "Take care!$",
    )),
    "MatchCall_PersonalizedText39": (("suntan oil", "sunbathing"), (
        "Hey, it's {STR_VAR_1}...\\n",
        "Whoops!\\p",
        "Splash!\\p",
        "Blug-blug-blug-blug...\\p",
        "Sploosh!\\p",
        "Whiff-whiff! Whiff-whiff!\\p",
        "Hey! Sorry about that!\\n",
        "I had just oiled my arms.\\p",
        "So the POKéNAV went straight\\n",
        "out of my hand into the water!\\p",
        "But HORIZONTE builds them\\n",
        "tough. It came up still\\l",
        "talking!\\p",
        "Anyway, I'm busy lying in the\\n",
        "sun, so let's talk another time.$",
    )),
    "MatchCall_PersonalizedText40": (("three triathlon events", "prune-like"), (
        "Hello, this is {STR_VAR_1}.\\p",
        "Of the three triathlon events,\\n",
        "swimming is the one I like.\\p",
        "But if I stay in the sea too\\n",
        "long, don't I go all wrinkled?\\p",
        "Ooh, the triathlon asks a great\\n",
        "deal of a person! Bye!$",
    )),
    "MatchCall_PersonalizedText41": (("DRAGON POKéMON appear to be", "peak form"), (
        "Hello, {PLAYER}{KUN}.\\n",
        "{STR_VAR_1} here.\\p",
        "How is your team keeping?\\p",
        "My DRAGON POKéMON are in the\\n",
        "best shape of their lives.\\l",
        "Bye for now.$",
    )),
    "MatchCall_PersonalizedText42": (("tough than that last time", "wait till next time"), (
        "{STR_VAR_1} here.\\p",
        "My {STR_VAR_2} has come along a\\n",
        "great deal since we last met.\\p",
        "I don't intend to lose to you\\n",
        "a second time. Wait and see!\\p",
        "See you around!$",
    )),
    "MatchCall_PersonalizedText43": (("art of concealment", "Like smoke I disappear"), (
        "It is {STR_VAR_1} here.\\p",
        "I have kept up my study of not\\n",
        "being seen.\\p",
        "But I have done too well at it.\\n",
        "Nobody can find me at all.\\l",
        "My success has made me lonely...\\p",
        "Like smoke, I go!\\n",
        "Farewell!$",
    )),
    "MatchCall_PersonalizedText44": (("training since we met", "Training on a beach"), (
        "This is {STR_VAR_1}.\\n",
        "I've trained every day since\\l",
        "we met.\\p",
        "My {STR_VAR_2} is getting hard\\n",
        "to handle, in the good way.\\p",
        "Training on sand works, just as\\n",
        "I thought it would. Bye now!$",
    )),
    "MatchCall_PersonalizedText45": (("yucky volcanic", "pattern on my parasol"), (
        "How do you do?\\n",
        "This is {STR_VAR_1}.\\p",
        "I wonder when this ash will\\n",
        "stop coming down?\\p",
        "If it settles any deeper it\\n",
        "will cover the pattern on my\\l",
        "parasol...\\p",
        "Let's promise to meet again!$",
    )),
    "MatchCall_PersonalizedText46": (("float in the sea than a pool", "Where am I, anyway"), (
        "Hi, {STR_VAR_1} here.\\p",
        "Did you know it's easier to\\n",
        "float in the sea than a pool?\\p",
        "Lie still and your body does\\n",
        "the rest on its own.\\p",
        "But if you float too long, mind\\n",
        "you don't get carried off.\\p",
        "...Where am I, anyway?\\n",
        "I'd better go!$",
    )),
    "MatchCall_PersonalizedText47": (("pitch my tent here", "tamp"), (
        "Oh, {PLAYER}{KUN}, hello!\\n",
        "This is {STR_VAR_1}.\\l",
        "I'm up in the hills just now.\\p",
        "But the ground is all lumps.\\n",
        "I can't get a tent up here...\\p",
        "Oh, I have had a fine idea!\\p",
        "Maybe my POKéMON can tread the\\n",
        "ground flat for me!\\p",
        "I'm going to try it!\\n",
        "Bye-bye!$",
    )),
    "MatchCall_PersonalizedText48": (("raising POKéMON with VIVI", "number one"), (
        "Oh, hi, hi, this is {STR_VAR_1}!\\p",
        "I'm raising POKéMON with VIVI!\\n",
        "We're trying ever so hard!\\p",
        "If we try harder still, can we\\n",
        "be the best? Bye-bye!$",
    )),
    "MatchCall_PersonalizedText49": (("SAILOR on land be called", "across the waves"), (
        "{STR_VAR_1} here!\\p",
        "I'm a SAILOR, but there's no\\n",
        "boat under me today.\\p",
        "Which makes me wonder -- what\\n",
        "do you call a SAILOR on land?\\p",
        "That's what I've been chewing\\n",
        "on, looking out at the water.\\p",
        "All right. Next time!$",
    )),
    "MatchCall_PersonalizedText50": (("Get any more POKéMON", "won't whine for it"), (
        "It's {STR_VAR_1}.\\n",
        "Well? Caught anything new?\\p",
        "If you catch one I've not seen,\\n",
        "you have to come and show me.\\p",
        "I won't beg for it, honest.\\n",
        "I'll be waiting. See you.$",
    )),
    "MatchCall_PersonalizedText51": (("optimal way", "air is clean where I am"), (
        "This is {STR_VAR_1}.\\p",
        "Are you raising your POKéMON\\n",
        "the way they ought to be?\\p",
        "The air is clean where I am.\\n",
        "There's no better place for it.\\p",
        "If you mean to take that side\\n",
        "of it seriously, come out to\\l",
        "{STR_VAR_2}. Take care now.$",
    )),
    "MatchCall_PersonalizedText52": (("likes and dislikes", "quite fascinating"), (
        "Hi, this is {STR_VAR_1}.\\p",
        "I gave a {POKEBLOCK} to my\\n",
        "{STR_VAR_2}. It went down well.\\p",
        "It seems POKéMON have their own\\n",
        "tastes in {POKEBLOCK}S.\\p",
        "I find that rather interesting.\\n",
        "Do take care.$",
    )),
    "MatchCall_PersonalizedText53": (("comfortable in the wild", "right track"), (
        "{STR_VAR_1} here.\\p",
        "Work with POKéMON and you can\\n",
        "be comfortable out of doors.\\p",
        "More people ought to see that\\n",
        "and work with them properly.\\p",
        "That would be the ideal.\\n",
        "I really do think so.\\p",
        "You're on the right road, you.\\n",
        "Catch you later!$",
    )),
    "MatchCall_PersonalizedText54": (("always prepared", "check my own"), (
        "Hi, it's {STR_VAR_1} -- the one\\n",
        "who's always packed and ready!\\p",
        "{PLAYER}{KUN}, have you items enough?\\n",
        "Is your team fit to go?\\p",
        "Keeping everything squared away\\n",
        "is the whole secret to staying\\l",
        "out on the road.\\p",
        "I'd better go count my own\\n",
        "supplies! Stay ready!$",
    )),
    "MatchCall_PersonalizedText55": (("thoroughfare", "won five battles"), (
        "It's {STR_VAR_1}!\\n",
        "It's {STR_VAR_1}!\\p",
        "{STR_VAR_2} is a busy stretch\\n",
        "of road, so I get challenged by\\l",
        "all sorts every single day.\\p",
        "Today I won five and lost only\\n",
        "three!\\p",
        "How did you do today?\\n",
        "Tell me next time, all right?$",
    )),
    "MatchCall_PersonalizedText56": (("of BUG POKéMON, right?", "started crying"), (
        "It's me, {STR_VAR_1}.\\p",
        "I'm well liked because I keep\\n",
        "so many BUG POKéMON, right?\\p",
        "Well, I took the best ones in\\n",
        "to school with me today.\\p",
        "The girl I like burst into\\n",
        "tears! Go on and laugh.\\p",
        "I'll have to teach her what\\n",
        "makes BUG POKéMON worth it.\\p",
        "Snivel...\\n",
        "See you!$",
    )),
    "MatchCall_PersonalizedText57": (("While climbing", "It's steeper now"), (
        "Hah! Hah! Hah! Hah!\\p",
        "Hi! It's {STR_VAR_1}! Hah! Hah!\\p",
        "Talking...\\n",
        "While climbing...\\l",
        "Is hard work... Hah! Hah!\\p",
        "Urgh! Oof...\\n",
        "It's steeper here...\\l",
        "We'll talk... another time...\\l",
        "Hah! Hah! Hah!$",
    )),
    "MatchCall_PersonalizedText58": (("searching for treasures", "why are you angry"), (
        "Oh, hi!\\p",
        "I'm still hunting for treasure\\n",
        "with IARA!\\p",
        "Maybe there's nothing buried\\n",
        "out here at all...\\p",
        "But what matters is that I'm\\n",
        "looking for it beside IARA.\\p",
        "Oh, hey, IARA!\\n",
        "Wh-why are you angry?\\p",
        "I'm not ignoring you, love!\\n",
        "There's only you!\\p",
        "...{PLAYER}, I have to go, bye!$",
    )),
    "MatchCall_PersonalizedText59": (("PORTO DAS REDES's GYM again", "jealousy thing isn't"), (
        "This is {STR_VAR_1}!\\p",
        "I trained at the PORTO DAS\\n",
        "REDES gym again this week.\\p",
        "ADEMAR, the GYM LEADER, seems\\n",
        "harder than he was.\\p",
        "Something about the waves\\n",
        "knocking him into shape...\\p",
        "But he's as easy about it as\\n",
        "ever. The ladies adore him!\\l",
        "It makes me envious, frankly.\\p",
        "I wonder... is his friend BRUNO\\n",
        "the same way as ADEMAR?\\p",
        "You know -- always sweaty, and\\n",
        "always calling people “big\\l",
        "wave,” that sort of thing.\\p",
        "But this envy isn't a good look\\n",
        "on me, is it?\\p",
        "Forget we had this talk, would\\n",
        "you? So long!$",
    )),
    "MatchCall_PersonalizedText60": (("a young TRAINER like you", "Never be discouraged"), (
        "It's a pleasure to talk with a\\n",
        "young TRAINER like you.\\p",
        "I expect you'll go on enjoying\\n",
        "POKéMON however old you get.\\p",
        "Wouldn't it be good to have a\\n",
        "partnership like ours one day?\\p",
        "Of course, {PLAYER}{KUN}, you already\\n",
        "have the trust and the company\\l",
        "of your POKéMON.\\p",
        "The long friendships are begun\\n",
        "in you already!\\p",
        "Hahaha!\\n",
        "Never be discouraged!$",
    )),
    "MatchCall_PersonalizedText61": (("cool SWIMMER guy", "chews me out whether"), (
        "Hi, this is {STR_VAR_1}!\\n",
        "We just won a battle!\\p",
        "We don't win often, but this\\n",
        "was some smart SWIMMER, too.\\p",
        "My sister was furious!\\p",
        "She wanted to look weak on\\n",
        "purpose, to make an impression!\\p",
        "She scolds me whether we win or\\n",
        "lose, that one!\\p",
        "{PLAYER}{KUN}, would you say something\\n",
        "to her next time?\\p",
        "All right, see you!$",
    )),
    "MatchCall_PersonalizedText62": (("headed out to sea yesterday", "when I discover"), (
        "{STR_VAR_1} here, yes.\\n",
        "I went out to sea yesterday.\\p",
        "I had hoped to turn up some\\n",
        "ruin nobody had opened yet.\\p",
        "But the water carried me back\\n",
        "to where I started from.\\p",
        "And I'm still poor at\\n",
        "battling... Laugh if you like...\\l",
        "But I won't give it up.\\p",
        "My day will come, and there\\n",
        "will be a ruin with my name on\\l",
        "it!\\p",
        "That's all I have to say!\\n",
        "Farewell for now!$",
    )),
    "MatchCall_PersonalizedText63": (("ROUTE 108", "nasty glare"), (
        "Ahoy there!\\n",
        "It's me, {STR_VAR_1}!\\l",
        "I'm out on ROUTE 108 now!\\l",
        "Which is to say, where I\\l",
        "always am!\\p",
        "Today a fine-looking SWIMMER\\n",
        "went by me!\\p",
        "So I gave her a shout to\\n",
        "startle her!\\p",
        "And she gave me a look that\\n",
        "could strip paint!\\p",
        "That's all from ROUTE 108!\\n",
        "Brought to you by {STR_VAR_1}!$",
    )),
    "MatchCall_PersonalizedText64": (("beaten five TRAINERS again", "good rivals"), (
        "It's {STR_VAR_1}!\\p",
        "I'm busy, but I thought you\\n",
        "should know I've beaten five\\l",
        "TRAINERS again today.\\p",
        "If I keep this up, I'll likely\\n",
        "have you next time.\\p",
        "We'll make good rivals, you\\n",
        "and I. Good-bye for now!$",
    )),
}


def block_pattern(label: str) -> re.Pattern[str]:
    return re.compile(
        rf"(?ms)^{re.escape(label)}::?\n(?P<body>.*?)(?=^[A-Za-z0-9_]+(?:::|:)(?:\n|$)|\Z)"
    )


def visible_segments(payload: str) -> list[str]:
    cleaned = payload.replace("$", "")
    cleaned = cleaned.replace("{PLAYER}", "PLAYERX")
    cleaned = cleaned.replace("{STR_VAR_1}", NAME_SLOT).replace("{STR_VAR_2}", NAME_SLOT)
    cleaned = cleaned.replace("{POKEBLOCK}", "POKéBLOCK")
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


def validate_string_vars() -> None:
    """A block only gets {STR_VAR_2} if match_call.c hands it a second string."""
    for label, (_, payloads) in TARGETS.items():
        uses = any("{STR_VAR_2}" in payload for payload in payloads)
        allowed = label in WITH_SECOND_VAR
        if uses and not allowed:
            raise ValueError(f"{label}: uses {{STR_VAR_2}} but is a STRS_NORMAL_MSG block")
        if allowed and not uses:
            raise ValueError(f"{label}: was handed a second string and drops it")


def render(source: str) -> str:
    validate_widths()
    validate_string_vars()
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
        masked = masked[:start] + '\t.string "<ARAUNA_PERSONALIZED_CALLS_EN>"\n\n' + masked[end:]
    return masked


def validate_rendered(source: str, rendered: str) -> None:
    if mask(source) != mask(rendered):
        raise ValueError("non-dialogue structure changed while rendering")

    # EVERGRANDE was the last Hoenn place name left anywhere in this file; it
    # had survived every renaming pass because nothing else spells it unspaced.
    forbidden = ("EVERGRANDE", "HOENN", "PETALBURG", "DEWFORD", "MAUVILLE",
                 "LILYCOVE", "SLATEPORT", "RUSTBORO", "Sucuria")
    for label in TARGETS:
        body = block_pattern(label).search(rendered).group("body")
        for token in forbidden:
            if token in body:
                raise ValueError(f"{label}: stale token survived: {token}")

    # Place names have to stay on one line: a name split across \n is what let
    # earlier renaming passes walk straight past MIRAGE TOWER and JAGGED PASS.
    whole = ("MEMORIAL DOS NOMES", "RESERVA ARAUNA", "NAVIO PERDIDO",
             "SERRA DA CINZA", "ESTR. JURAMENTO", "CYCLING ROAD",
             "TRAINER'S SCHOOL", "ROUTE 108")
    joined = "".join(
        payload for _, payloads in TARGETS.values() for payload in payloads)
    flat = CONTROL_RE.sub(" ", joined)
    for name in whole:
        if name in flat and name not in joined:
            raise ValueError(f"place name is split across a line break: {name}")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Render the rematch callers' personalized text in English.")
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--in-place", action="store_true")
    args = parser.parse_args()
    if args.check and args.in_place:
        parser.error("use either --check or --in-place")

    source = CALLS.read_text(encoding="utf-8")
    rendered = render(source)
    validate_rendered(source, rendered)

    if args.in_place:
        CALLS.write_text(rendered, encoding="utf-8")
    print(f"Personalized Match Call English renderer OK: {len(TARGETS)} blocks.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
