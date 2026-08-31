#!/usr/bin/env python3
"""The PokeNav calls from the people who know you.

Seventy-two blocks: your mother, your father, Ciro, Val, Seu Bento's president,
Scott, and the four of the league. These are the calls that ring while you are
walking, and every one of them was still Emerald's -- your father talking about
Rustboro, Ciro about Team Magma, your mother about a gym in Petalburg.

The names had already been fixed by earlier passes; the sentences around them
had not. Three place names had escaped those passes entirely because they were
split across a line break in the source -- MIRAGE TOWER and JAGGED PASS -- and
they are corrected here in the rewriting.

Ciro is one person with two sets of lines, because the engine keeps a separate
call list depending on who the player is. Both sets say the same things in
slightly different words, exactly as the original did.

No payload names a species: the dex is generated, and a line naming a creature
would be wrong the next time it is.
"""
from __future__ import annotations

import argparse
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CALLS = ROOT / "data" / "text" / "match_call.inc"
MAX_VISIBLE_WIDTH = 34
CONTROL_RE = re.compile(r"\\[npl]")
PLACEHOLDER_RE = re.compile(r"\{[^}]+\}")

TARGETS: dict[str, tuple[tuple[str, ...], tuple[str, ...]]] = {
    # -- home ---------------------------------------------------------------
    "MatchCall_Text_Mom1": (("Your father and you", "everyday chores"), (
        "MOM: Your father, and now you.\\p",
        "Both of you, taken with them.\\p",
        "What is it about them?\\p",
        "Me? I like the ones that help\\n",
        "around the house.$",
    )),
    "MatchCall_Text_Mom2": (("PAMPA DA ESPERA GYM", "big blow to his pride"), (
        "MOM: Hello, {PLAYER}!\\p",
        "Your father has shut himself in\\n",
        "the PAMPA DA ESPERA GYM again.\\p",
        "He comes home now and then.\\p",
        "He eats everything in the house\\n",
        "and goes straight back.\\p",
        "Losing to you took something\\n",
        "out of him, I think.$",
    )),
    "MatchCall_Text_Mom3": (("Don't worry about me", "RUNNING SHOES"), (
        "MOM: {PLAYER}.\\p",
        "Don't think about me or the\\n",
        "house.\\p",
        "Wear those RUNNING SHOES until\\n",
        "there's nothing left of them.$",
    )),

    # -- the league ---------------------------------------------------------
    "MatchCall_Text_Sidney": (("come on back", "waiting"), (
        "LAZARO: {PLAYER}.\\p",
        "If you want another go at me,\\n",
        "come back to the LEAGUE.\\p",
        "I don't go anywhere.\\n",
        "I'll be here.$",
    )),
    "MatchCall_Text_Phoebe": (("coming back here", "bond has grown"), (
        "ROSA: Hello, {PLAYER}.\\p",
        "Come back and see us sometime.\\p",
        "I'd like to see how much closer\\n",
        "you and yours have become.$",
    )),
    "MatchCall_Text_Glacia": (("complacent", "cool your"), (
        "CLARA: Hello, {PLAYER}.\\p",
        "You haven't grown comfortable\\n",
        "with your own strength?\\p",
        "If you ever need cooling down,\\n",
        "the LEAGUE is where I am.$",
    )),
    "MatchCall_Text_Drake": (("BATTLE", "no substitute"), (
        "TIBURCIO: That voice.\\n",
        "{PLAYER}, isn't it.\\p",
        "You sound well.\\p",
        "They've built a place that tests\\n",
        "a TRAINER's skill, I hear.\\p",
        "For a real battle, though,\\n",
        "nothing replaces the LEAGUE.\\p",
        "You agree with me. I know you do.$",
    )),
    "MatchCall_Text_Wallace": (("Have you met BENTO", "METEORITE"), (
        "AMALIA: Hello, {PLAYER}{KUN}.\\p",
        "Have you met BENTO yet?\\p",
        "He is better than almost anyone,\\n",
        "and he almost never battles.\\p",
        "He would rather be looking for\\n",
        "stones.\\p",
        "He's in a cave somewhere right\\n",
        "now. I'd put money on it.$",
    )),

    # -- Ciro, calling as the rival -----------------------------------------
    "MatchCall_Text_MayRayquazaCall": (("giant green", "major discovery"), (
        "... ... ... ... ...\\n",
        "... ... ... ... Beep!\\p",
        "CIRO: {PLAYER}{KUN}!\\p",
        "I was over in CASA DA FOGUEIRA\\n",
        "just now.\\p",
        "Something enormous and green\\n",
        "went over, very high up.\\p",
        "I've never seen anything like\\n",
        "it. I don't know what it was.\\p",
        "... ... ... ... ...\\n",
        "... ... ... ... Click!$",
    )),
    "MatchCall_Text_BrendanRayquazaCall": (("huge green", "wish you could've seen"), (
        "... ... ... ... ...\\n",
        "... ... ... ... Beep!\\p",
        "CIRO: {PLAYER}!\\p",
        "I was in CASA DA FOGUEIRA just\\n",
        "now.\\p",
        "Something huge and green crossed\\n",
        "the whole sky.\\p",
        "I wish you'd been there to see\\n",
        "it.\\p",
        "... ... ... ... ...\\n",
        "... ... ... ... Click!$",
    )),
    "MatchCall_Text_May1": (("SAILOR retired", "love the sea"), (
        "CIRO: Hello, {PLAYER}{KUN}!\\p",
        "THE SAILOR has retired, but I\\n",
        "still see him out on the water\\l",
        "with PEEKO.\\p",
        "Retiring didn't take the sea\\n",
        "out of him.$",
    )),
    "MatchCall_Text_May2": (("doesn't have a GYM", "apply to be the LEADER"), (
        "CIRO: Hello, {PLAYER}{KUN}!\\p",
        "Small places like PAMPA DA\\n",
        "ESPERA and PORTO DAS REDES have\\l",
        "GYMS.\\p",
        "The biggest port in the region\\n",
        "doesn't. Isn't that strange?\\p",
        "When they build one in PORTO DO\\n",
        "SAL, I'm applying to run it.$",
    )),
    "MatchCall_Text_May3": (("CUTTER", "ROCK SMASH GUY"), (
        "CIRO: Hello, {PLAYER}{KUN}!\\p",
        "Do you remember the CUTTER, in\\n",
        "SERRA DO UIVO?\\p",
        "His younger brother lives in\\n",
        "ENCRUZILHADA.\\p",
        "Guess what they call him.\\p",
        "... ... ... ... ...\\p",
        "The ROCK SMASH GUY.$",
    )),
    "MatchCall_Text_May5": (("ROUTE 111", "old"), (
        "CIRO: {PLAYER}{KUN}, how are you?\\p",
        "I'm out on ROUTE 111.\\p",
        "There's an old woman living just\\n",
        "north of the desert.\\p",
        "She's letting me rest here.$",
    )),
    "MatchCall_Text_May6": (("TOWER in the desert", "come and go"), (
        "CIRO: Hello, {PLAYER}{KUN}!\\p",
        "Have you heard about the TORRE\\n",
        "MIRAGEM, out in the sand?\\p",
        "They say it appears and goes\\n",
        "again like a mirage.\\p",
        "I'd love to see it once.$",
    )),
    "MatchCall_Text_May7": (("ROUTE 119", "got soaked"), (
        "CIRO: {PLAYER}{KUN}, hello!\\p",
        "I'm on ROUTE 119.\\p",
        "Big river, and it rains almost\\n",
        "constantly.\\p",
        "I am completely soaked.$",
    )),
    "MatchCall_Text_May9": (("hot", "bad-looking"), (
        "CIRO: Hello, {PLAYER}{KUN}!\\p",
        "I was heading for the hot spring\\n",
        "at SERTAO DE DENTRO.\\p",
        "Around PASSO CORTADO I passed\\n",
        "some people I didn't like the\\l",
        "look of.\\p",
        "The mood up there was ugly.$",
    )),
    "MatchCall_Text_May10": (("CAPT. STERN discovered", "CAVERNAS M'BOI"), (
        "CIRO: Hello, {PLAYER}{KUN}!\\p",
        "Did you see the news?\\p",
        "CAPT. STERN found the CAVERNAS\\n",
        "M'BOI on his last dive.$",
    )),
    "MatchCall_Text_May11": (("cross the sea", "bottom of the sea"), (
        "CIRO: Hello, {PLAYER}{KUN}!\\p",
        "Isn't it remarkable?\\p",
        "With no boat at all, one of them\\n",
        "will carry you across.\\p",
        "And there's another that takes\\n",
        "you to the bottom.$",
    )),
    "MatchCall_Text_May12": (("blocked", "come up to the surface"), (
        "CIRO: Hello, {PLAYER}{KUN}!\\p",
        "Ever found the way ahead shut\\n",
        "while you were out on the water?\\p",
        "Go under. Follow the trenches\\n",
        "along the bottom.\\p",
        "Come up on the other side. It's\\n",
        "that simple.$",
    )),
    "MatchCall_Text_May13": (("super-ancient", "three of them"), (
        "CIRO: Hello, {PLAYER}{KUN}!\\p",
        "How's the POKéDEX coming?\\p",
        "There's a rumour of three very\\n",
        "old things, sealed away.\\p",
        "I'd give a lot to see even one.$",
    )),
    "MatchCall_Text_May14": (("AGUAS DE M'BOI GYM", "far"), (
        "CIRO: {PLAYER}{KUN}!\\p",
        "I heard. You beat the AGUAS DE\\n",
        "M'BOI GYM LEADER.\\p",
        "There isn't much road left in\\n",
        "front of you, is there.$",
    )),
    "MatchCall_Text_May15": (("single TRAINER", "surprised"), (
        "CIRO: There isn't a TRAINER left\\n",
        "in ARAUNA who doesn't know your\\l",
        "name, {PLAYER}{KUN}.\\p",
        "When I tell people we're\\n",
        "friends, they don't believe me\\l",
        "at first.$",
    )),
    "MatchCall_Text_Brendan1": (("SAILOR retired", "love"), (
        "CIRO: Hey, {PLAYER}!\\p",
        "THE SAILOR retired, and he's\\n",
        "still out there with PEEKO.\\p",
        "Some people can't leave the\\n",
        "water alone.$",
    )),
    "MatchCall_Text_Brendan2": (("don't get how", "apply to be the LEADER"), (
        "CIRO: Hey, {PLAYER}!\\p",
        "PAMPA DA ESPERA has a GYM.\\n",
        "PORTO DAS REDES has a GYM.\\p",
        "The biggest port in the region\\n",
        "doesn't. Explain that to me.\\p",
        "When PORTO DO SAL gets one,\\n",
        "I'm putting my name in.$",
    )),
    "MatchCall_Text_Brendan3": (("CUTTER", "ROCK SMASH GUY"), (
        "CIRO: Yo, {PLAYER}!\\p",
        "Remember the CUTTER, up in\\n",
        "SERRA DO UIVO?\\p",
        "Turns out his little brother\\n",
        "lives in ENCRUZILHADA.\\p",
        "Guess what he's called.\\p",
        "... ... ... ... ...\\p",
        "The ROCK SMASH GUY.$",
    )),
    "MatchCall_Text_Brendan4": (("joins SERRA DO UIVO",), (
        "CIRO: That voice. {PLAYER}?\\p",
        "The GALERIAS DA SERRA got its\\n",
        "name from what it joins.\\p",
        "SERRA DO UIVO on one side,\\n",
        "VALE DO SILENCIO on the other.$",
    )),
    "MatchCall_Text_Brendan5": (("ROUTE 111", "visit her"), (
        "CIRO: {PLAYER}, what's happening?\\p",
        "I'm out on ROUTE 111.\\p",
        "There's an old woman north of\\n",
        "the desert putting me up.\\p",
        "Call in on her if you pass.$",
    )),
    "MatchCall_Text_Brendan6": (("TOWER in the desert", "only sometimes"), (
        "CIRO: Hey, {PLAYER}!\\p",
        "Heard of the TORRE MIRAGEM out\\n",
        "in the sand?\\p",
        "It's only there some of the\\n",
        "time. Like a mirage.\\p",
        "I want to see that.$",
    )),
    "MatchCall_Text_Brendan7": (("ROUTE 119", "soaked to the bone"), (
        "CIRO: Who's this? {PLAYER}!\\p",
        "I'm on ROUTE 119.\\p",
        "Big river, rain that doesn't\\n",
        "stop.\\p",
        "Soaked to the bone.$",
    )),
    "MatchCall_Text_Brendan9": (("hot", "TEAM MAGMA"), (
        "CIRO: Hey there, {PLAYER}.\\p",
        "I was going back to the hot\\n",
        "spring at SERTAO DE DENTRO.\\p",
        "Around PASSO CORTADO I ran into\\n",
        "some unpleasant people.\\p",
        "LEMBRANTES, I'm fairly sure.$",
    )),
    "MatchCall_Text_Brendan10": (("catch the news", "CAVERNAS M'BOI"), (
        "CIRO: Hi, {PLAYER}!\\p",
        "Did you catch the news?\\p",
        "CAPT. STERN found the CAVERNAS\\n",
        "M'BOI while he was down there.$",
    )),
    "MatchCall_Text_Brendan11": (("awesome", "anything"), (
        "CIRO: Hey there, {PLAYER}!\\p",
        "Doesn't it get you?\\p",
        "No boat, and one of them takes\\n",
        "you clean across the water.\\p",
        "There's another that takes you\\n",
        "under it.\\p",
        "They can do anything.$",
    )),
    "MatchCall_Text_Brendan12": (("side blocked", "Simple"), (
        "CIRO: Howdy, {PLAYER}!\\p",
        "Ever hit a dead end out on the\\n",
        "water?\\p",
        "Dive. Follow the trenches along\\n",
        "the bottom.\\p",
        "Surface on the far side.\\n",
        "Simple.$",
    )),
    "MatchCall_Text_Brendan13": (("Filling up your", "three"), (
        "CIRO: Hey there, {PLAYER}!\\p",
        "Is the POKéDEX filling up?\\p",
        "There's a rumour about three\\n",
        "very old things, sealed away.\\p",
        "I'd love to find even one.$",
    )),
    "MatchCall_Text_Brendan14": (("AGUAS DE M'BOI GYM", "close"), (
        "CIRO: {PLAYER}!\\p",
        "I heard about AGUAS DE M'BOI.\\n",
        "You beat their LEADER.\\p",
        "You're close now. Very close.$",
    )),
    "MatchCall_Text_Brendan15": (("all of ARAUNA", "envious"), (
        "CIRO: There isn't a TRAINER in\\n",
        "all of ARAUNA who doesn't know\\l",
        "your name, {PLAYER}.\\p",
        "I tell people we're friends and\\n",
        "watch their faces.$",
    )),

    # -- Val ----------------------------------------------------------------
    "MatchCall_Text_Wally1": (("physically fit", "TRAINER like"), (
        "VAL: Oh, {PLAYER}!\\p",
        "I've been getting stronger.\\n",
        "Properly stronger, I mean.\\p",
        "I want to be a TRAINER like you\\n",
        "one day.$",
    )),
    "MatchCall_Text_Wally2": (("WANDA",), (
        "VAL: {PLAYER}, hello!\\p",
        "Since the GALERIAS DA SERRA\\n",
        "opened, WANDA has been happier\\l",
        "than I've ever seen her.$",
    )),
    "MatchCall_Text_Wally3": (("without telling", "furious"), (
        "VAL: Oh, {PLAYER}.\\p",
        "I left my uncle's house in VALE\\n",
        "DO SILENCIO without saying\\l",
        "anything.\\p",
        "He must be furious with me.\\p",
        "You understand why I went,\\n",
        "though. Don't you?$",
    )),
    "MatchCall_Text_Wally4": (("world of TRAINERS", "connected"), (
        "VAL: {PLAYER}? It's me.\\p",
        "This world is extraordinary.\\p",
        "When I have mine beside me,\\n",
        "strangers say hello to me.\\p",
        "As if everyone were joined up\\n",
        "through them somehow.$",
    )),
    "MatchCall_Text_Wally5": (("we caught together", "praised"), (
        "VAL: {PLAYER}! The one we caught\\n",
        "together.\\p",
        "It changed. It grew up.\\p",
        "Maybe I'm good at this after\\n",
        "all.\\p",
        "No. That's the wrong way round.\\p",
        "It did the growing. Not me.$",
    )),
    "MatchCall_Text_Wally6": (("service area",), (
        "... ... ... ... ...\\n",
        "... ... ... ... ...\\p",
        "VAL seems to be out of range\\n",
        "of the POKéNAV...$",
    )),
    "MatchCall_Text_Wally7": (("hardly ever", "Thank you"), (
        "VAL: Oh, {PLAYER}.\\p",
        "Before I met you I barely left\\n",
        "the house.\\p",
        "Now I'm out here, with my own,\\n",
        "going somewhere.\\p",
        "{PLAYER}.\\p",
        "Thank you.$",
    )),

    # -- Scott ---------------------------------------------------------------
    "MatchCall_Text_Scott1": (("found", "everywhere"), (
        "SCOTT: Howdy, {PLAYER}{KUN}!\\p",
        "They turn up everywhere, don't\\n",
        "they. Mountain, sea, grass.\\p",
        "TRAINERS are exactly the same.\\p",
        "Which means I have to be\\n",
        "everywhere too. Busy, busy!$",
    )),
    "MatchCall_Text_Scott2": (("ROUTE 119", "ticklish"), (
        "SCOTT: I'm on ROUTE 119.\\p",
        "The place is crawling with\\n",
        "TRAINERS.\\p",
        "Also with grass up to here.\\p",
        "In these shorts it's unbearable.$",
    )),
    "MatchCall_Text_Scott3": (("MEMORIAL DOS NOMES", "climb to the top"), (
        "SCOTT: Hi, hi, {PLAYER}{KUN}!\\p",
        "Have you been up the MEMORIAL\\n",
        "DOS NOMES yet?\\p",
        "It's where the ones who are gone\\n",
        "are kept and named.\\p",
        "Every TRAINER should climb it\\n",
        "once. Every one.$",
    )),
    "MatchCall_Text_Scott4": (("odd", "thugs"), (
        "SCOTT: Hi, {PLAYER}{KUN}!\\p",
        "I keep hearing about these\\n",
        "outfits causing trouble.\\p",
        "LEMBRANTES and CONSORCIO\\n",
        "HORIZONTE, I think.\\p",
        "There must be real TRAINERS in\\n",
        "among them.\\p",
        "...If they weren't what they\\n",
        "are.$",
    )),
    "MatchCall_Text_Scott5": (("bottom of the sea", "can't swim"), (
        "SCOTT: Oh, hello, {PLAYER}{KUN}.\\p",
        "Do you suppose there are hard\\n",
        "TRAINERS on the seabed?\\p",
        "I can't go and look. I can't\\n",
        "swim, and I don't raise them.$",
    )),
    "MatchCall_Text_Scott6": (("all the GYM BADGES", "HALL"), (
        "SCOTT: Hi, hi, {PLAYER}{KUN}!\\p",
        "Every BADGE, and the LEAGUE\\n",
        "opens to you. You know that.\\p",
        "With what you've got, CHAMPION\\n",
        "isn't a daydream.\\p",
        "But there's somewhere better\\n",
        "than that.\\p",
        "That's all you're getting from\\n",
        "me for now.\\p",
        "Something to look forward to,\\n",
        "once your name is on that wall.$",
    )),
    "MatchCall_Text_Scott7": (("service area",), (
        "... ... ... ... ...\\n",
        "... ... ... ... ...\\p",
        "SCOTT seems to be out of range\\n",
        "of the POKéNAV...$",
    )),

    # -- Elias, as your father ------------------------------------------------
    "MatchCall_Text_Norman1": (("CUTTER", "pay him a visit"), (
        "DAD: There's a man in SERRA DO\\n",
        "UIVO they call the CUTTER.\\p",
        "If you pass through, go and see\\n",
        "him.$",
    )),
    "MatchCall_Text_Norman2": (("getting", "hard to explain"), (
        "DAD: Little by little, and quite\\n",
        "certainly, you're getting\\l",
        "stronger.\\p",
        "The stronger you get, the\\n",
        "further you go from your mother\\l",
        "and me.\\p",
        "I don't have the words for what\\n",
        "that feels like.$",
    )),
    "MatchCall_Text_Norman3": (("four GYM BADGES", "waiting for you"), (
        "DAD: Four BADGES.\\p",
        "Then there's no putting it off.\\n",
        "We battle, as I said we would.\\p",
        "Come whenever you like.\\n",
        "We'll be here.$",
    )),
    "MatchCall_Text_Norman4": (("visit", "deep"), (
        "DAD: {PLAYER}. Go and see your\\n",
        "mother now and then.\\p",
        "I'm staying here and training\\n",
        "harder.\\p",
        "This work goes deeper than\\n",
        "anyone tells you, and it does\\l",
        "not forgive.$",
    )),
    "MatchCall_Text_Norman5": (("MAGMA EMBLEM", "volcano"), (
        "DAD: Oh, {PLAYER}.\\p",
        "A what? An EMBLEM?\\p",
        "I've no idea what that is.\\p",
        "With a name like that, it must\\n",
        "have something to do with the\\l",
        "mountain.$",
    )),
    "MatchCall_Text_Norman_Preparing": (("training session",), (
        "DAD: Hah! Haah!\\p",
        "...Oh. {PLAYER}.\\p",
        "You've caught me in the middle\\n",
        "of a session.$",
    )),
    "MatchCall_Text_Norman_PreparingPostGame": (("CHAMPION", "left behind"), (
        "DAD: {PLAYER}.\\p",
        "My own child, CHAMPION of the\\n",
        "LEAGUE.\\p",
        "Right. I'm not being left\\n",
        "behind.$",
    )),
    "MatchCall_Text_Norman_RematchReady": (("challenge", "PAMPA DA ESPERA GYM"), (
        "DAD: {PLAYER}? Good timing.\\p",
        "This time I'm the one doing the\\n",
        "challenging.\\p",
        "I'm at the PAMPA DA ESPERA GYM.\\n",
        "Come when you're ready.$",
    )),
    "MatchCall_Text_Norman_PostRematch": (("How much higher",), (
        "DAD: You astonish me.\\p",
        "How much further does this go?$",
    )),
    "MatchCall_Text_UnusedProfBirch": (("POKéDEX and POKéNAV",), (
        "PROF. ANAHI: With the POKéDEX\\n",
        "and the POKéNAV both in hand,\\l",
        "the work gets interesting.$",
    )),

    # -- Seu Bento's president ------------------------------------------------
    "MatchCall_Text_MrStone1": (("office window", "Wahahaha"), (
        "MR. STONE: {PLAYER}{KUN}!\\p",
        "You've called me, so the POKéNAV\\n",
        "is working.\\p",
        "Others will register\\n",
        "themselves. Ring them too.\\p",
        "You sound pleased with\\n",
        "yourself.\\p",
        "How do I know? I'm watching you\\n",
        "from my office window.\\p",
        "Wahahaha! Goodbye!$",
    )),
    "MatchCall_Text_MrStone2": (("errand", "busy PRESIDENT"), (
        "MR. STONE: {PLAYER}{KUN}!\\p",
        "Have you forgotten my errand?\\p",
        "The letter goes to BENTO, in\\n",
        "PORTO DAS REDES.\\p",
        "Then the parcel to CAPT. STERN,\\n",
        "in PORTO DO SAL.\\p",
        "You remember now.\\p",
        "I'm a busy man. Goodbye!$",
    )),
    "MatchCall_Text_MrStone3": (("met BENTO", "reward"), (
        "MR. STONE: {PLAYER}{KUN}!\\p",
        "You've met BENTO. Then you're\\n",
        "owed something.\\p",
        "Next time you're in SERRA DO\\n",
        "UIVO, come up to the office.\\p",
        "I'll be waiting.$",
    )),
    "MatchCall_Text_MrStone4": (("shut down the operation", "live in peace"), (
        "MR. STONE: {PLAYER}{KUN}!\\p",
        "Did you know HORIZONTE was\\n",
        "cutting the GALERIAS DA SERRA?\\p",
        "We stopped the work. There were\\n",
        "things living in there.\\p",
        "It isn't complicated. They were\\n",
        "there first.$",
    )),
    "MatchCall_Text_MrStone5": (("ELIAS's",), (
        "MR. STONE: Hello, hello,\\n",
        "{PLAYER}{KUN}!\\p",
        "Someone in PAMPA DA ESPERA tells\\n",
        "me you're ELIAS's child.\\p",
        "Well. That explains a great\\n",
        "deal.$",
    )),
    "MatchCall_Text_MrStone6": (("own father", "Wahaha"), (
        "MR. STONE: What's this?\\p",
        "You battled your own father and\\n",
        "won?\\p",
        "Astounding.\\p",
        "I had no idea the company I was\\n",
        "keeping. Wahaha!$",
    )),
    "MatchCall_Text_MrStone7": (("gone out", "just as busy"), (
        "Hello. HORIZONTE speaking...\\p",
        "Oh. {PLAYER}.\\p",
        "The PRESIDENT was here a moment\\n",
        "ago and has gone out again.\\p",
        "He's a busy man. You sound just\\n",
        "as busy.$",
    )),
    "MatchCall_Text_MrStone8": (("breaking up", "BZZZZ"), (
        "...What? Say again?\\p",
        "OXU... yes? ...MARA?\\p",
        "You're breaking up.\\n",
        "I can't hear you...\\p",
        "BZZZZ...$",
    )),
    "MatchCall_Text_MrStone9": (("breaking up", "BZZZZ"), (
        "...What? Say again?\\p",
        "Caver... yes? ...M'BOI?\\p",
        "You're breaking up.\\n",
        "I can't hear you...\\p",
        "BZZZZ...$",
    )),
    "MatchCall_Text_MrStone10": (("in your corner", "road you believe"), (
        "MR. STONE: {PLAYER}{KUN}! It's me.\\p",
        "You've been caught up in\\n",
        "something, and being busy, I\\l",
        "have no idea what.\\p",
        "Walk the road you believe in.\\p",
        "I'll be behind you either way.\\n",
        "Take care of yourself.$",
    )),
    "MatchCall_Text_MrStone11": (("full of confidence", "visit us"), (
        "MR. STONE: ... ... ...\\p",
        "Is that {PLAYER}{KUN}?\\p",
        "Your voice has changed. I didn't\\n",
        "know you for a moment.\\p",
        "Come and see us at HORIZONTE\\n",
        "when you can.$",
    )),
}


def block_pattern(label: str) -> re.Pattern[str]:
    return re.compile(
        rf"(?ms)^{re.escape(label)}::?\n(?P<body>.*?)(?=^[A-Za-z0-9_]+(?:::|:)(?:\n|$)|\Z)"
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
        masked = masked[:start] + '\t.string "<ARAUNA_MATCH_CALL_PEOPLE_EN>"\n\n' + masked[end:]
    return masked


def validate_rendered(source: str, rendered: str) -> None:
    if mask(source) != mask(rendered):
        raise ValueError("non-dialogue structure changed while rendering")

    # Two place names had escaped the earlier passes because the source split
    # them across a line break. They must not survive here.
    forbidden = ("MIRAGE\\nTOWER", "MIRAGE TOWER", "JAGGED", "TEAM MAGMA",
                 "GROU", "Sucuria")
    for label in TARGETS:
        body = block_pattern(label).search(rendered).group("body")
        for token in forbidden:
            if token in body:
                raise ValueError(f"{label}: stale token survived: {token}")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Render the named PokeNav callers in English.")
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
    print(f"Match Call people English renderer OK: {len(TARGETS)} blocks.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
