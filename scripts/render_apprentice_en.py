#!/usr/bin/env python3
"""The sixteen apprentices who ask you how to be a trainer.

Each one finds you, asks to be taught, then comes back with eighteen kinds of
question -- which level, which POKéMON, what to hold, which move, what to say
when they win. The engine indexes the lot by apprentice, so apprentice 9 is
the same person in all eighteen files, and Emerald wrote all two hundred and
eighty-eight blocks out by hand.

Two of them rhyme. One lies about everything. One cries at any provocation.
One is a triathlete with no time and one has a bad back. Keeping sixteen
people straight across eighteen files is not something to trust to typing, so
it is split: the four blocks where the character is established -- the
challenge, the request to be taught, the ask for a winning line, and the
thanks for it -- are written out for each of them, and the fourteen
mechanical questions are built from each voice's own pieces. What a person
says when they are pleased belongs to that person and is written once.

Which slots exist is decided by the map script, not by the apprentice, so a
slot the script buffers is available to all sixteen even where Emerald's text
for one of them happened not to use it. The check below is therefore per
question kind, not per block.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools" / "arauna"))
from textbox import TextBox, glued  # noqa: E402

APPRENTICE = ROOT / "data" / "text" / "apprentice.inc"

BOX = TextBox({"{PLAYER}": 7, "{KUN}": 0, "{STR_VAR_1}": 14,
               "{STR_VAR_2}": 14, "{STR_VAR_3}": 14}, width=34)

KINDS = ("Challenge", "PleaseTeach", "RejectTeaching", "WhichLevelMode",
         "LevelModeThanks", "WhichMon", "MonThanks", "WhichMonFirst",
         "MonFirstThanks", "WhatHeldItem", "HoldNothing",
         "ItemAlreadyRecommended", "ThanksHeldItem", "ThanksNoHeldItem",
         "WhichMove", "MoveThanks", "PickWinSpeech", "WinSpeechThanks")

# What each of the sixteen sounds like. `hail` greets the player mid-errand,
# `cheer` is their noise when something goes well, `stuck` is how they admit
# they cannot decide, and `plead` is what they say when refused.
VOICES: tuple[dict[str, str], ...] = (
    {   # 0 -- cries at everything
        "hail": "Snivel...|Oh, {PLAYER}!",
        "cheer": "Awesome! Wicked! Awoooh!",
        "thanks": "Thank you so much!",
        "ok": "Snivel... I understand!",
        "stuck": "There's something I can't decide and it's making me cry.",
        "ask": "Please, {PLAYER}. Which one?",
        "plead": "Oh... B-but...|Snivel... Waaaaaaah!|Please! I'm begging you!",
    },
    {   # 1 -- brand new and delighted about it
        "hail": "Wowee! {PLAYER}!",
        "cheer": "Wowee!",
        "thanks": "Thanks a lot!",
        "ok": "Right! Got it!",
        "stuck": "I've got stuck on something.",
        "ask": "Which one would you pick?",
        "plead": "Aww, no!|Please? Please please please?",
    },
    {   # 2 -- quiet, apologetic, means it
        "hail": "Um... Hello, {PLAYER}.",
        "cheer": "Oh, good.",
        "thanks": "Thank you very much.",
        "ok": "Um... All right.",
        "stuck": "There's something I can't work out on my own.",
        "ask": "Would you tell me which?",
        "plead": "Oh... I see...|I'm sorry for asking.|...Could I ask again?",
    },
    {   # 3 -- certain it will all go wrong
        "hail": "Oh... it's {PLAYER}...",
        "cheer": "...That's good. That's actually good.",
        "thanks": "Thank you. Really.",
        "ok": "...All right. If you say so.",
        "stuck": "I can't decide, and I'll get it wrong whichever I pick.",
        "ask": "Which would you choose? If it were you?",
        "plead": "...No. Of course not.|I knew that, really.|...But could you?",
    },
    {   # 4 -- friendly and slightly above you
        "hail": "Hey! {PLAYER}!",
        "cheer": "Excellent!",
        "thanks": "Thanks! You're all right, you are.",
        "ok": "Right, that's settled then.",
        "stuck": "I'm stuck on something and you can help.",
        "ask": "So which is it?",
        "plead": "What? No!|Come on. You'll help me.|Say you'll help me.",
    },
    {   # 5 -- busy, three other lives to lead
        "hail": "Ah, {PLAYER}! Good, you're here.",
        "cheer": "Splendid. That's one thing off the list.",
        "thanks": "Thanks. You've saved me an afternoon.",
        "ok": "Noted.",
        "stuck": "I haven't the time to work this one out myself.",
        "ask": "Quickly, if you can -- which?",
        "plead": "No? Ah.|I'm asking because I've no time to find out the "
                 "hard way.|Reconsider?",
    },
    {   # 6 -- excitable, everything is the best idea
        "hail": "A-hah! {PLAYER}!",
        "cheer": "A-hah! Brilliant!",
        "thanks": "Thanks! You're the best!",
        "ok": "Right! Yes! Understood!",
        "stuck": "I've had a thought and now I can't choose between two!",
        "ask": "Which one? Which one?",
        "plead": "No way! Uh-uh!|You have to! It's a great idea!|Please!",
    },
    {   # 7 -- formal to a fault
        "hail": "I beg your pardon, {PLAYER}.",
        "cheer": "How gratifying.",
        "thanks": "You have my thanks.",
        "ok": "Very well. Understood.",
        "stuck": "I find myself unable to settle a question.",
        "ask": "Which would you have me choose?",
        "plead": "Ah... I see...|I hope I have not offended.|Might I ask "
                 "once more?",
    },
    {   # 8 -- startled by being spoken to at all
        "hail": "Eek! {PLAYER}!",
        "cheer": "Eek! Wonderful!",
        "thanks": "Thank you! Thank you!",
        "ok": "Y-yes! Understood!",
        "stuck": "I can't decide and it's making me jumpy!",
        "ask": "Which one should it be?!",
        "plead": "Eek! No?|Oh, please, please!|I'll be no trouble!",
    },
    {   # 9 -- lucky, loud, and pleased about both
        "hail": "Whoa, {PLAYER}! Aren't I lucky!",
        "cheer": "Yeehaw!",
        "thanks": "Much obliged!",
        "ok": "Right you are!",
        "stuck": "I've come to a fork and I can't pick a road.",
        "ask": "So which way, then?",
        "plead": "Aw, no!|Come on now, my luck can't be that bad!|Ask me "
                 "again, go on!",
    },
    {   # 10 -- lies, then admits it
        "hail": "Oh, {PLAYER}. I was just about to send for you.|...That's "
                "a lie.",
        "cheer": "Marvellous. And that's the truth.",
        "thanks": "Thanks. No lie.",
        "ok": "Understood. Honestly, this time.",
        "stuck": "I can't decide. That one's true, worse luck.",
        "ask": "So which is it?",
        "plead": "No? Fine, I don't mind.|...That's a lie.|Please?",
    },
    {   # 11 -- a sailor who will not stop rhyming
        "hail": "A-H-O-Y, {PLAYER}, ahoy!|That's how I greet a fellow boy or "
                "girl of my employ!",
        "cheer": "Oh joy, oh joy!",
        "thanks": "My thanks to you, and that's no ploy!",
        "ok": "Understood, and understood good!",
        "stuck": "I'm stuck between the two, and I don't know what to do!",
        "ask": "So tell me true -- which one for you?",
        "plead": "Oh no, oh no, don't tell me go!|Give me a yes and end my "
                 "woe!",
    },
    {   # 12 -- a guitarist who will not stop either
        "hail": "Say, hey, {PLAYER}, hey!|You turned up on the perfect day!",
        "cheer": "Now that's what I call a chord!",
        "thanks": "Thanks a lot, and that's the plot!",
        "ok": "Received, believed, achieved!",
        "stuck": "I'm caught between a two, and I don't know what to do!",
        "ask": "So which one's true?|I'm asking you!",
        "plead": "Oh no, don't go!|You're my whole show!|Say yes, I beg, "
                 "and steal the stage below!",
    },
    {   # 13 -- training karate on a body that objects
        "hail": "Oh, hi, {PLAYER}.|Ouch... give me a moment...",
        "cheer": "Oof! That's the stuff!",
        "thanks": "Thanks. You're a help.",
        "ok": "Right. Understood. Ouch.",
        "stuck": "I've been turning this over and my head hurts as well now.",
        "ask": "Which do I go with?",
        "plead": "Ouch... no?|Come on, I'm asking nicely and I'm in pain.|"
                 "Have a heart.",
    },
    {   # 14 -- would rather not be looked at
        "hail": "Er... um... {PLAYER}...",
        "cheer": "Oh. Oh, that's a relief.",
        "thanks": "Th-thank you.",
        "ok": "Um. All right then.",
        "stuck": "I'm embarrassed to ask, but I can't decide.",
        "ask": "Which would you say?",
        "plead": "Oh... no...|I knew I shouldn't have asked...|...Unless "
                 "you would?",
    },
    {   # 15 -- not convinced any of this is happening
        "hail": "Hm. {PLAYER}. Still real, I take it.",
        "cheer": "Hm. Better than expected.",
        "thanks": "My thanks, assuming you exist.",
        "ok": "Noted. Provisionally.",
        "stuck": "I have two options and no way to tell them apart.",
        "ask": "Which, in your view?",
        "plead": "No?|Hm.|I shall ask again, and see whether the answer is "
                 "stable.",
    },
)

# The four blocks where a person is established rather than merely consulted.
CHALLENGE: tuple[tuple[str, ...], ...] = (
    ("Um, I'm {STR_VAR_1}'s no. {STR_VAR_2} apprentice.|Snivel... The nerves "
     "are getting to me...",),
    ("I'm {STR_VAR_1}'s no. {STR_VAR_2} apprentice!|Here we come!",),
    ("I'm the no. {STR_VAR_2} apprentice of {STR_VAR_1}.|Please accept my "
     "challenge.",),
    ("Um... I'm {STR_VAR_1}'s no. {STR_VAR_2} apprentice...|Do you think "
     "somebody like me can win?",),
    ("I'm {STR_VAR_1}'s no. {STR_VAR_2} apprentice!|I'll let you challenge "
     "me!",),
    ("I'm terribly busy, but I also happen to be {STR_VAR_1}'s no. "
     "{STR_VAR_2} apprentice.",),
    ("I'm {STR_VAR_1}'s no. {STR_VAR_2} apprentice!|A-hah! Pleased to meet "
     "you!",),
    ("I serve as {STR_VAR_1}'s no. {STR_VAR_2} apprentice.|May I begin?",),
    ("Eek! I'm {STR_VAR_1}'s no. {STR_VAR_2} apprentice!|I'll do my best!",),
    ("Yeehaw! I'm {STR_VAR_1}'s no. {STR_VAR_2} apprentice!|Put 'em up!",),
    ("I'm {STR_VAR_1}'s thousandth apprentice!|...I'm no. {STR_VAR_2}. Here "
     "goes!",),
    ("Ahoy! I'm {STR_VAR_1}'s no. {STR_VAR_2}, and rhyming is my joy!",),
    ("Hey, hey! The name to say is {STR_VAR_1}'s no. {STR_VAR_2} today!",),
    ("Ouch! I'm {STR_VAR_1}'s no. {STR_VAR_2} apprentice.|Good to meet you. "
     "Ouch.",),
    ("This is nerve-racking...|I'm the no. {STR_VAR_2} apprentice of "
     "{STR_VAR_1}.",),
    ("I am {STR_VAR_1}'s no. {STR_VAR_2} apprentice, and that is not a lie.",),
)

PLEASE_TEACH: tuple[tuple[str, ...], ...] = (
    (   # 0
        "Are you... {PLAYER}?|Oh! Sniff... sob...",
        "Oh! S-sorry...|I'm so nervous I've started crying...",
        "I'm {STR_VAR_1}, and I think the world of you, {PLAYER}.",
        "I used to dream about meeting you and asking you about POKéMON.",
        "Please, please, {PLAYER}!|Please teach me about POKéMON!",
    ),
    (   # 1
        "Wowee! You're {PLAYER}, aren't you?|You're terrifically strong, "
        "aren't you?",
        "I'm {STR_VAR_1}!|I only just became a TRAINER!",
        "Please, {PLAYER}!|Will you teach me? I want to know everything "
        "there is about being a TRAINER!",
    ),
    (   # 2
        "Um... are you {PLAYER}?|My name is {STR_VAR_1}.",
        "I want to be a POKéMON TRAINER, but I don't know where to start...",
        "So I thought I might ask you, since everyone knows who you are.",
        "{PLAYER}, would you give me some advice?",
    ),
    (   # 3
        "Oh? What? You're...|No. That can't be right.",
        "Somebody like me doesn't meet {PLAYER}.",
        "...You really are {PLAYER}?|I can't believe I'm talking to you.",
        "When something this good happens, something terrible follows. I "
        "know it does...",
        "...Sorry.|I'm... {STR_VAR_1}...",
        "There's nothing about me worth telling you.",
        "I shouldn't say it anyway. You'll have forgotten by tomorrow...",
        "I used to think that if I ever met you, {PLAYER}, I might ask you "
        "for advice.",
        "But you wouldn't agree to that.",
        "...Or would you? Would you help me?",
    ),
    (   # 4
        "Oh! You're {PLAYER}, aren't you?",
        "I hear you're hard to beat!",
        "I'm {STR_VAR_1}!|I'll be your friend!",
        "Did you know?",
        "You can't win at the BATTLE CIRCUIT on what they teach you at the "
        "TRAINER'S SCHOOL.",
        "I'm willing to hear your advice.|You'll say yes, of course?",
    ),
    (   # 5
        "Oh, hello! {PLAYER}!|I know you, everyone knows you.|Call me "
        "{STR_VAR_1}. Good to meet you!",
        "I'm a TRIATHLETE, so I keep in condition while I raise POKéMON.",
        "There's also the job, and the napping, and the dancing...",
        "Being this busy, it is not easy to become any good at this.",
        "So here is my proposal.",
        "There's a reason we met. {PLAYER}, would you pass on what you know, "
        "now and then?",
    ),
    (   # 6
        "No way! Uh-uh!|Are you the actual {PLAYER}?",
        "A-hah! Marvellous! I'm {STR_VAR_1}, and I am delighted!",
        "{PLAYER}, you're very strong, aren't you.",
        "Everybody talks about you!",
        "Oh! I've just had a wonderful idea!|I'll get advice off you, "
        "{PLAYER}!|That would make me tougher, surely!",
        "Isn't that a good idea?|Please -- I want your advice!",
    ),
    (   # 7
        "I beg your pardon, but...|are you {PLAYER}?",
        "I am {STR_VAR_1}, and I am delighted to make your acquaintance.",
        "I have admired you for a long while...",
        "... ... ... ... ...",
        "Um... I hope this is not too great an imposition, but...",
        "May I become your apprentice, {PLAYER}?",
    ),
    (   # 8
        "Eek! Eek! {PLAYER}!|You spoke to me!|I... I can hardly stand it!",
        "Me! My name is {STR_VAR_1}!|I only just became a TRAINER!",
        "And to have met you, {PLAYER} -- everyone knows that name!",
        "Oh-oh-oh, I know!|May I ask an enormous favour, {PLAYER}?",
        "Please take me on as your apprentice!|I want to learn from you!",
    ),
    (   # 9
        "Whoa. Could you be...|might you be {PLAYER}?|That strong and famous "
        "TRAINER?|Well now, aren't I the lucky one.",
        "Hello. The name's {STR_VAR_1}.",
        "I've been on the lookout for somebody to teach me.",
        "And along you come, at exactly the right hour.",
        "So there it is, {PLAYER}.|Let me apprentice under you.",
    ),
    (   # 10
        "Oh, hey. {PLAYER}, isn't it?|The police were asking after you.",
        "... ... ...|Of course that's a lie.",
        "Me, I'm {STR_VAR_1}. And despite appearances I'm the POKéMON "
        "CHAMPION.|...Also a lie.",
        "This part isn't.|I'm not much good at battling.",
        "So how about it -- will you be my master in all things POKéMON?",
    ),
    (   # 11
        "A-H-O-Y!|That spells ahoy, and ahoy means hi!",
        "I'm {STR_VAR_1}, the rapping SAILOR, aye!",
        "Your turn now -- tell me a thing or two, and don't be shy!",
        "Uh-huh, uh-huh!|{PLAYER}'s the name, and POKéMON's the game!",
        "And you're at the age where the whole world's a stage!",
        "Anyway, here's the thing I want to say: you're the tenth TRAINER "
        "I've talked to today.",
        "So let's mark the occasion, no hesitation -- be my mentor, in "
        "commemoration!",
    ),
    (   # 12
        "Say, hey, aren't you {PLAYER}?|Should I talk to you?|Why not -- "
        "I'm talking to you!",
        "{PLAYER}, are you surprised by me?|Then I'd better say who I "
        "happen to be!",
        "{STR_VAR_1} is what you can call me.|The brightest star in all of "
        "guitardom, that's me!",
        "Are you receiving me?|You are receiving me!",
        "My luck is at its best, so I'll hit you with a request!",
        "{PLAYER}, let me be your underling!|I want you to teach me "
        "everything!",
    ),
    (   # 13
        "Oh, hello! You there!|Could you get my shoulder for me?",
        "...Yes, there! That's it!|Ouch, ouch! Oh, that's better...",
        "My name's {STR_VAR_1}.|I train at karate, but my body wasn't built "
        "for the punishment...",
        "So I decided I'd battle POKéMON and toughen myself up that way.",
        "You're {PLAYER}, aren't you?|The one who took the LEAGUE?",
        "Listen -- could you give me some advice?",
    ),
    (   # 14
        "Er... um...|{PLAYER}...?",
        "Please don't look at me like that.|You're making me self-conscious.",
        "I... I'm {STR_VAR_1}.",
        "It's embarrassing to say, but I go into old ruins and such.",
        "It's more embarrassing to admit I'm interested in the BATTLE "
        "CIRCUIT.",
        "{PLAYER}, they say you're hard to beat...",
        "This is difficult for me, but I want to ask something.",
        "Would you be my teacher, and give me advice?",
    ),
    (   # 15
        "Hm. You appear to be {PLAYER}...|But are you actually real?",
        "You may call me {STR_VAR_1}.",
        "I have been considering apprenticing myself to a strong TRAINER.",
        "So I am fortunate you came along.|...You really are {PLAYER}, yes?",
        "No, no. If you are real, that will do.|I merely want you to "
        "acknowledge me as your apprentice.",
    ),
)

PICK_WIN_SPEECH: tuple[tuple[str, ...], ...] = (
    (   # 0
        "Oh... {PLAYER}?|It is {PLAYER}!|Oh! Sniff... sob... Please listen!",
        "When I battle I get so nervous I cry even when I win...",
        "I wish I had something to say instead...",
        "Please, please, {PLAYER}!|Could you give me something to say when I "
        "win, so I don't cry?",
    ),
    (   # 1
        "{PLAYER}! There you are!",
        "I won a battle and then I just stood there!",
        "Wowee, it was awful! I didn't know what to say!",
        "Give me something to say when I win! Please!",
    ),
    (   # 2
        "Um... {PLAYER}...",
        "When I win, I never know what to say, and the moment goes past.",
        "Would you give me something to say? Something short?",
    ),
    (   # 3
        "Oh... {PLAYER}...",
        "I won a battle. It surprised me more than it surprised them.",
        "And I said nothing, because I don't have anything to say.",
        "...Could you give me something? For when it happens again?",
    ),
    (   # 4
        "Hey! {PLAYER}!",
        "I want a line for when I win.|Something people remember.",
        "You've won a lot, so you'll know one.|Out with it!",
    ),
    (   # 5
        "Ah, {PLAYER}. One more thing while I have you.",
        "I need something to say when I win. I haven't the time to think of "
        "one myself.",
        "Give me a line and I'll use it for years.",
    ),
    (   # 6
        "A-hah! {PLAYER}!",
        "I've had another idea!|When I win, I should say something!",
        "Isn't that good? Everyone would remember me!",
        "So give me one! Give me a good one!",
    ),
    (   # 7
        "I beg your pardon, {PLAYER}.",
        "It has occurred to me that a victory ought to be marked with some "
        "remark.",
        "I have none. Would you furnish me with one?",
    ),
    (   # 8
        "Eek! {PLAYER}!",
        "I won! And then I said nothing at all and went red!",
        "Please give me something to say next time!|Anything!",
    ),
    (   # 9
        "Whoa, {PLAYER}! Good timing again!",
        "I want a line for winning. Something with a bit of swagger.",
        "You'll know one. Let's have it!",
    ),
    (   # 10
        "Oh, {PLAYER}. I've already got a brilliant victory line.",
        "...That's a lie.",
        "I haven't got one at all. Would you give me one?",
    ),
    (   # 11
        "Ahoy, {PLAYER}, and hear my plea!",
        "When I win I've nothing to say, and that's no good for a rhymer "
        "like me!",
        "Give me a line to shout out loud, that I might say it clear and "
        "proud!",
    ),
    (   # 12
        "Hey, hey, {PLAYER}, hey!|I need a line, and I need it today!",
        "When I win there's a silence, and silence won't do!|A song wants "
        "an ending, and so do I too!",
        "Give me the words and I'll make them ring!",
    ),
    (   # 13
        "Oh, hello, {PLAYER}. Ouch.",
        "I won one. And I couldn't think of a thing to say.",
        "Give me a line, would you? Something short. I haven't the breath "
        "for long.",
    ),
    (   # 14
        "Er... {PLAYER}...",
        "When I win, everyone looks at me, and I say nothing at all.",
        "It would be easier if I had something ready.",
        "Could you... give me something to say?",
    ),
    (   # 15
        "Hm. {PLAYER}.",
        "It appears that winning is followed by a silence, and the silence "
        "is expected to be filled.",
        "I have nothing to fill it with. Provide me with something.",
    ),
)

WIN_SPEECH_THANKS: tuple[tuple[str, ...], ...] = (
    (   # 0
        "{STR_VAR_1}",
        "Awesome! Wicked! Awoooh!|That's really good!",
        "Oh... I'm sorry...|I'm so happy I'm crying...",
        "Snivel... {PLAYER}!|Thank you for everything!",
        "I'll battle as well as I can, for your sake.",
        "{PLAYER}...|Next time... we should battle!",
    ),
    (   # 1
        "{STR_VAR_1}",
        "Wowee! That's brilliant!",
        "Thanks, {PLAYER}! Thanks for everything!",
        "I'm going to go and win so I can say it!|And then we should battle!",
    ),
    (   # 2
        "{STR_VAR_1}",
        "Oh... that's lovely. That's exactly right.",
        "Thank you for all of it, {PLAYER}.",
        "I'll try to be worth the trouble.|And one day, would you battle me?",
    ),
    (   # 3
        "{STR_VAR_1}",
        "...That's good. That's better than I'd have managed.",
        "Thank you, {PLAYER}. For everything, not just this.",
        "I'll say it when I win.|...If I win.|Battle me one day?",
    ),
    (   # 4
        "{STR_VAR_1}",
        "Excellent. That'll do nicely.",
        "Thanks, {PLAYER}. You've been all right.",
        "Next time we meet, we're battling. Fair warning.",
    ),
    (   # 5
        "{STR_VAR_1}",
        "Splendid. Short, too. I approve.",
        "Thank you, {PLAYER}. You've saved me a great deal of thinking.",
        "I'll make time for a battle with you. Somehow.",
    ),
    (   # 6
        "{STR_VAR_1}",
        "A-hah! That's the one!|That's exactly the one!",
        "Thank you, {PLAYER}! You're the best!",
        "Now I want to win just so I can say it!|Battle me next time!",
    ),
    (   # 7
        "{STR_VAR_1}",
        "How very fitting. You have my thanks.",
        "For all of it, {PLAYER}. You have been generous with your time.",
        "Should you ever wish for a battle, I am at your disposal.",
    ),
    (   # 8
        "{STR_VAR_1}",
        "Eek! It's perfect!",
        "Thank you! Thank you, {PLAYER}!",
        "I'll say it! I'll say it every time!|And then -- may we battle?",
    ),
    (   # 9
        "{STR_VAR_1}",
        "Yeehaw! Now that's a line!",
        "Much obliged, {PLAYER}. For all of it.",
        "Come and find me for a battle when you fancy one!",
    ),
    (   # 10
        "{STR_VAR_1}",
        "I hate it.|...That's a lie. It's perfect.",
        "Thanks, {PLAYER}. No lie, that one.",
        "Let's battle sometime. That's true as well.",
    ),
    (   # 11
        "{STR_VAR_1}",
        "Oh joy, oh joy! It scans and all!",
        "My thanks to you, {PLAYER}, for every call!",
        "Now come and battle, one and all -- well, you, at any rate!",
    ),
    (   # 12
        "{STR_VAR_1}",
        "Now that's a chord to end a show!",
        "Thanks for everything, {PLAYER}, and now you know!",
        "Next time we meet, let's have a battle -- and I'll take you on in "
        "the final bar!",
    ),
    (   # 13
        "{STR_VAR_1}",
        "Oof! That's a good one.",
        "Thanks, {PLAYER}. You've been a help all the way through.",
        "Come and battle me once my back's forgiven me.",
    ),
    (   # 14
        "{STR_VAR_1}",
        "Oh... that's rather good, isn't it.",
        "Th-thank you, {PLAYER}. For all of it.",
        "I'll try to say it out loud.|And... would you battle me, one day?",
    ),
    (   # 15
        "{STR_VAR_1}",
        "Hm. Serviceable. Better than serviceable.",
        "My thanks, {PLAYER}, for the whole of it.",
        "We should battle, and settle whether either of us is real.",
    ),
)


def questions(voice: dict[str, str]) -> dict[str, tuple[str, ...]]:
    """The fourteen questions every apprentice asks, in their own words."""
    return {
        "RejectTeaching": (voice["plead"],),
        "WhichLevelMode": (
            voice["ok"],
            "Then tell me this. It's about the BATTLE TOWER.",
            "Which suits somebody like me -- Level 50, or the Open Level?",
        ),
        "LevelModeThanks": (
            "{STR_VAR_1}?",
            voice["cheer"],
            voice["thanks"] + "|Talk to me again!",
        ),
        "WhichMon": (
            voice["hail"],
            voice["stuck"],
            "I can't choose between {STR_VAR_1} and {STR_VAR_2}.",
            voice["ask"],
        ),
        "MonThanks": (
            voice["ok"],
            "I'll go and get myself a {STR_VAR_1}.",
            voice["thanks"],
        ),
        "WhichMonFirst": (
            voice["hail"],
            "I want to start battling people, and I don't know what order to "
            "put my POKéMON in.",
            "Which of these would you send out first?",
        ),
        "MonFirstThanks": (
            "{STR_VAR_1} goes first?",
            voice["cheer"],
            voice["thanks"],
        ),
        "WhatHeldItem": (
            voice["hail"],
            voice["stuck"],
            "I don't know what to give my {STR_VAR_1} to hold.",
            voice["ask"],
        ),
        "HoldNothing": (
            "So my {STR_VAR_1} should hold nothing at all?",
        ),
        "ItemAlreadyRecommended": (
            "You gave me {STR_VAR_1} once already.",
            "Or do you mean my {STR_VAR_2} should hold nothing?",
        ),
        "ThanksHeldItem": (
            "A {STR_VAR_1}.|I think I have one of those.",
            voice["cheer"],
            voice["thanks"],
        ),
        "ThanksNoHeldItem": (
            voice["ok"] + "|Nothing at all, then.",
            voice["cheer"],
            voice["thanks"],
        ),
        "WhichMove": (
            voice["hail"],
            "I can't settle on a move for my {STR_VAR_1}.",
            "{STR_VAR_2}, or {STR_VAR_3}?",
        ),
        "MoveThanks": (
            "{STR_VAR_1}?",
            voice["cheer"],
            voice["thanks"],
        ),
    }


def build() -> dict[str, tuple[str, ...]]:
    blocks: dict[str, tuple[str, ...]] = {}
    for index, voice in enumerate(VOICES):
        blocks[f"gText_ApprenticeChallenge{index}"] = CHALLENGE[index]
        blocks[f"gText_ApprenticePleaseTeach{index}"] = PLEASE_TEACH[index]
        blocks[f"gText_ApprenticePickWinSpeech{index}"] = PICK_WIN_SPEECH[index]
        blocks[f"gText_ApprenticeWinSpeechThanks{index}"] = WIN_SPEECH_THANKS[index]
        for kind, paragraphs in questions(voice).items():
            blocks[f"gText_Apprentice{kind}{index}"] = paragraphs
    return blocks


PARAGRAPHS = build()
TARGETS = tuple(PARAGRAPHS)


def block_pattern(label: str) -> re.Pattern[str]:
    return re.compile(
        rf"(?ms)^{re.escape(label)}::?\n(?P<body>.*?)(?=^[A-Za-z0-9_]+(?:::|:)(?:\n|$)|\Z)"
    )


def payloads() -> dict[str, tuple[str, ...]]:
    composed = {}
    for label, paragraphs in PARAGRAPHS.items():
        paragraphs = tuple(
            p.replace("BATTLE TOWER", glued("BATTLE TOWER"))
             .replace("BATTLE CIRCUIT", glued("BATTLE CIRCUIT"))
             .replace("TRAINER'S SCHOOL", glued("TRAINER'S SCHOOL"))
            for p in paragraphs)
        composed[label] = BOX.compose(paragraphs)
    return composed


def slots_by_kind(source: str) -> dict[str, set[str]]:
    """Which slots the map script fills for each question.

    The buffering is done by the script, not by the apprentice, so a slot is
    available to all sixteen even where one of Emerald's sixteen texts did not
    happen to print it. The union across a kind is therefore the right answer
    and the intersection is not.
    """
    available: dict[str, set[str]] = {}
    for kind in KINDS:
        found: set[str] = set()
        for index in range(len(VOICES)):
            body = block_pattern(f"gText_Apprentice{kind}{index}").search(source)
            if not body:
                raise ValueError(f"gText_Apprentice{kind}{index}: missing")
            found |= set(re.findall(r"\{[A-Z_0-9]+\}", body.group("body")))
        available[kind] = found
    return available


def validate_slots(source: str) -> None:
    available = slots_by_kind(source)
    composed = payloads()
    for kind in KINDS:
        for index in range(len(VOICES)):
            label = f"gText_Apprentice{kind}{index}"
            used = set(re.findall(r"\{[A-Z_0-9]+\}", "".join(composed[label])))
            if used - available[kind]:
                raise ValueError(
                    f"{label}: uses {sorted(used - available[kind])}, which "
                    f"the script never fills for {kind}")


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
        masked = masked[:start] + '\t.string "<ARAUNA_APPRENTICE_EN>"\n\n' + masked[end:]
    return masked


def validate_rendered(source: str, rendered: str) -> None:
    if mask(source) != mask(rendered):
        raise ValueError("non-dialogue structure changed while rendering")

    composed = payloads()

    # Sixteen people, not one person sixteen times. Two apprentices who greet
    # the player identically are two apprentices the player cannot tell apart.
    hails = [voice["hail"] for voice in VOICES]
    if len(set(hails)) != len(hails):
        raise ValueError("two apprentices greet the player identically")
    for field in ("cheer", "thanks", "stuck", "plead"):
        values = [voice[field] for voice in VOICES]
        if len(set(values)) != len(values):
            raise ValueError(f"two apprentices share the same {field}")

    # Every apprentice must still say which number apprentice they are, and
    # whose: the challenge screen is where that is established.
    for index in range(len(VOICES)):
        challenge = "".join(composed[f"gText_ApprenticeChallenge{index}"])
        for slot in ("{STR_VAR_1}", "{STR_VAR_2}"):
            if slot not in challenge:
                raise ValueError(
                    f"apprentice {index}: the challenge dropped {slot}")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Render the sixteen Battle Tower apprentices in English.")
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--in-place", action="store_true")
    args = parser.parse_args()
    if args.check and args.in_place:
        parser.error("use either --check or --in-place")

    source = APPRENTICE.read_text(encoding="utf-8")
    validate_slots(source)
    rendered = render(source)
    validate_rendered(source, rendered)

    if args.in_place:
        APPRENTICE.write_text(rendered, encoding="utf-8")
    print(f"Apprentice English renderer OK: {len(TARGETS)} blocks.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
