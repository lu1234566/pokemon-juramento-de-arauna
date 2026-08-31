#!/usr/bin/env python3
"""The trainers of Routes 130 to 134: the far water.

A hundred and six blocks, the last of the route trainers. This is the drifting
end of the map -- the current runs hard, the boats get away from people, and
half of everyone out here is from Casa da Fogueira, the floating town, and says
so.

Two blocks named a creature, from the species pass dropping an Arauna name into
an Emerald sentence. Both gone; the dex is generated, so no payload names a
species. One line about men staring at a woman's swimsuit is gone as well.

Casa da Fogueira has to keep being named, because the siblings and the calm man
out here are all explaining the same town to you, and that is the only thread
this stretch of water has.

The elderly couple keep losing each other, which is the joke, and the siblings
stay siblings.
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
    # -- Route 130, the empty water ------------------------------------------
    "Route130_Text_RodneyIntro": (("didn't expect", "out in the sea"), (
        "SIQUEIRA: A TRAINER. Out\\n",
        "here. I didn't expect that.\\p",
        "We should battle.$",
    )),
    "Route130_Text_RodneyDefeat": (("awfully tough",), (
        "SIQUEIRA: This one is\\n",
        "tough.$",
    )),
    "Route130_Text_RodneyPostBattle": (("that look of someone", "suits you"), (
        "SIQUEIRA: You've the eyes\\n",
        "of someone who's had a\\l",
        "hard time of it and came\\l",
        "through.\\p",
        "It suits you.$",
    )),
    "Route130_Text_KatieIntro": (("shattered blue heart",), (
        "LAURA: Out in the deep\\n",
        "blue, a heavy heart\\l",
        "gets lighter.$",
    )),
    "Route130_Text_KatieDefeat": (("depths beyond belief",), (
        "LAURA: Like this sea, what\\n",
        "they can do goes deeper\\l",
        "than anyone has looked.$",
    )),
    "Route130_Text_KatiePostBattle": (("becoming", "CHAMPION"), (
        "LAURA: Every child in the\\n",
        "world wants to be CHAMPION\\l",
        "one day.\\p",
        "Very few keep swimming.$",
    )),
    "Route130_Text_SantiagoIntro": (("Floating on the open sea",), (
        "TOBIAS: Just floating out\\n",
        "here.\\p",
        "It's very peaceful.$",
    )),
    "Route130_Text_SantiagoDefeat": (("less peaceful",), (
        "TOBIAS: I should have been\\n",
        "less peaceful about it.$",
    )),
    "Route130_Text_SantiagoPostBattle": (("one happy guy",), (
        "TOBIAS: Swimming, then\\n",
        "battling, then swimming.\\p",
        "I'm a contented man.$",
    )),

    # -- Route 131, the water around Casa da Fogueira -----------------------
    "Route131_Text_RichardIntro": (("teeming", "not easy swimming"), (
        "SERGIO: This water is full\\n",
        "of them.\\p",
        "Swimming it is not the\\n",
        "restful part.$",
    )),
    "Route131_Text_RichardDefeat": (("raised by TRAINERS",), (
        "SERGIO: Ones raised by a\\n",
        "TRAINER hit differently.$",
    )),
    "Route131_Text_RichardPostBattle": (("leaving", "return trip"), (
        "SERGIO: Gasp... I'm spent.\\p",
        "Coming out is easy.\\n",
        "Getting back is the work.\\p",
        "Have I anything left for\\n",
        "the swim home?$",
    )),
    "Route131_Text_HermanIntro": (("sick and tired of the sea",), (
        "IVAN: Sea. Sea. Sea.\\p",
        "Sea as far as I can look.\\p",
        "I am sick of the sea.$",
    )),
    "Route131_Text_HermanDefeat": (("Bleah",), (
        "IVAN: Bleah!$",
    )),
    "Route131_Text_HermanPostBattle": (("born swimmer",), (
        "IVAN: Bored of it, and out\\n",
        "in it every day.\\p",
        "I was born for the water.\\n",
        "That's the trouble.$",
    )),
    "Route131_Text_SusieIntro": (("wait", "battle, you and I"), (
        "TATIANA: Wait, love!\\p",
        "You and me. Come on.$",
    )),
    "Route131_Text_SusieDefeat": (("in spite of the way",), (
        "TATIANA: Tougher than you\\n",
        "look, aren't you.$",
    )),
    "Route131_Text_SusiePostBattle": (("bored of the sea", "in love with the sea"), (
        "TATIANA: Did you meet the\\n",
        "man complaining about the\\l",
        "sea?\\p",
        "All talk. He loves it more\\n",
        "than any of us.$",
    )),
    "Route131_Text_KaraIntro": (("bathing suits", "ogle"), (
        "JULIA: I've been out here\\n",
        "since first light.\\p",
        "The current is turning.\\n",
        "Battle me before it does.$",
    )),
    "Route131_Text_KaraDefeat": (("out of my depth",), (
        "JULIA: I'm out of my depth.$",
    )),
    "Route131_Text_KaraPostBattle": (("my beauty",), (
        "JULIA: People come out here\\n",
        "and stare at the water for\\l",
        "hours.\\p",
        "I understand it. I do the\\n",
        "same thing.$",
    )),
    "Route131_Text_ReliIntro": (("work together as siblings",), (
        "NELI: The two of us,\\n",
        "together, against you.$",
    )),
    "Route131_Text_ReliDefeat": (("worked together",), (
        "NELI: Together, and still\\n",
        "beaten.$",
    )),
    "Route131_Text_ReliPostBattle": (("CASA DA FOGUEIRA", "born"), (
        "NELI: People from CASA DA\\n",
        "FOGUEIRA are in the water\\l",
        "from the day they're born.\\p",
        "It isn't a skill. It's\\n",
        "where we live.$",
    )),
    "Route131_Text_ReliNotEnoughMons": (("two POKéMON",), (
        "NELI: Only one? Then\\n",
        "there's no battle here.$",
    )),
    "Route131_Text_IanIntro": (("my sis",), (
        "IAN: Me and my sister.\\n",
        "Doing our best.$",
    )),
    "Route131_Text_IanDefeat": (("still couldn't win",), (
        "IAN: We both tried and we\\n",
        "still lost.$",
    )),
    "Route131_Text_IanPostBattle": (("floating town", "part of CASA DA FOGUEIRA"), (
        "IAN: CASA DA FOGUEIRA\\n",
        "floats. You know that?\\p",
        "So anywhere there's water,\\n",
        "that's a bit of home.$",
    )),
    "Route131_Text_IanNotEnoughMons": (("two POKéMON",), (
        "IAN: Bring two and we'll\\n",
        "take you on!$",
    )),
    "Route131_Text_TaliaIntro": (("great information",), (
        "TEREZA: Beat me and I'll\\n",
        "tell you something worth\\l",
        "knowing.$",
    )),
    "Route131_Text_TaliaDefeat": (("Did I lose",), (
        "TEREZA: Oh? Did I lose?$",
    )),
    "Route131_Text_TaliaPostBattle": (("huge tower", "take a look"), (
        "TEREZA: There's a strange\\n",
        "place near here.\\p",
        "A tower, out on its own.\\p",
        "Go and look at it.$",
    )),
    "Route131_Text_KevinIntro": (("peaceful bunch", "never get angry"), (
        "MURILO: People from CASA DA\\n",
        "FOGUEIRA don't get angry.\\p",
        "Not ever. Me included.$",
    )),
    "Route131_Text_KevinDefeat": (("Oops",), (
        "MURILO: Oops.$",
    )),
    "Route131_Text_KevinPostBattle": (("I'm not angry", "you're strong"), (
        "MURILO: Tch. ...No. Wait.\\p",
        "I am not angry. Honestly.\\p",
        "But you are strong.\\n",
        "Hahaha!$",
    )),

    # -- Route 132, the currents ---------------------------------------------
    "Route132_Text_GilbertIntro": (("catch colds", "totally fit"), (
        "HUMBERTO: I was ill every\\n",
        "winter as a boy.\\p",
        "Then I started swimming.\\n",
        "Not since.$",
    )),
    "Route132_Text_GilbertDefeat": (("crave more power",), (
        "HUMBERTO: I want more than\\n",
        "this.$",
    )),
    "Route132_Text_GilbertPostBattle": (("fields and", "mountains"), (
        "HUMBERTO: TRAINERS walk\\n",
        "the whole region.\\p",
        "You'd have to be fit for\\n",
        "that too.$",
    )),
    "Route132_Text_DanaIntro": (("currents", "too strong"), (
        "EDITE: I try not to swim\\n",
        "where the current is\\l",
        "strongest.$",
    )),
    "Route132_Text_DanaDefeat": (("Oh, please, no",), (
        "EDITE: Oh, please. No.$",
    )),
    "Route132_Text_DanaPostBattle": (("swept away", "sense of place"), (
        "EDITE: If it takes me, I\\n",
        "won't know where I am.\\p",
        "That frightens me more\\n",
        "than drowning.$",
    )),
    "Route132_Text_RonaldIntro": (("never know until",), (
        "TEODORO: You never know\\n",
        "until you go.$",
    )),
    "Route132_Text_RonaldDefeat": (("sank in defeat",), (
        "TEODORO: Waah! Down I go!$",
    )),
    "Route132_Text_RonaldPostBattle": (("razor's edge",), (
        "TEODORO: I don't battle\\n",
        "when I know I'll win.\\p",
        "The edge is the whole\\n",
        "point.$",
    )),
    "Route132_Text_KiyoIntro": (("24 hours a day", "possibly beat me"), (
        "NELSON: I think about them\\n",
        "every waking hour.\\p",
        "How could you beat that?$",
    )),
    "Route132_Text_KiyoDefeat": (("concede defeat",), (
        "NELSON: I lose. I concede.$",
    )),
    "Route132_Text_KiyoPostBattle": (("fanatic",), (
        "NELSON: Urgh.\\p",
        "You think about them all\\n",
        "day too, don't you.\\p",
        "I can tell.$",
    )),
    "Route132_Text_MakaylaIntro": (("my husband", "without him"), (
        "MARILDA: I'm always with my\\n",
        "husband.\\p",
        "I can still win without\\n",
        "him.$",
    )),
    "Route132_Text_MakaylaDefeat": (("wasn't good enough",), (
        "MARILDA: Not good enough,\\n",
        "then.$",
    )),
    "Route132_Text_MakaylaPostBattle": (("looks just", "making me blush"), (
        "MARILDA: That young man\\n",
        "over there.\\p",
        "He's the image of my\\n",
        "husband at that age.$",
    )),
    "Route132_Text_JonathanIntro": (("watching me intently",), (
        "MANUEL: Someone has been\\n",
        "watching me.\\p",
        "Was it you?$",
    )),
    "Route132_Text_JonathanDefeat": (("pretty strong",), (
        "MANUEL: Wow. That's strong.$",
    )),
    "Route132_Text_JonathanPostBattle": (("can't concentrate",), (
        "MANUEL: I still feel eyes\\n",
        "on me.\\p",
        "I can't settle.$",
    )),
    "Route132_Text_PaxtonIntro": (("where could my wife", "on my own"), (
        "RODRIGO: Where has my wife\\n",
        "gone?\\p",
        "We're always together.\\p",
        "Can I even win on my own?$",
    )),
    "Route132_Text_PaxtonDefeat": (("couldn't manage",), (
        "RODRIGO: Ah. Apparently\\n",
        "not on my own.$",
    )),
    "Route132_Text_PaxtonPostBattle": (("looking for me",), (
        "RODRIGO: She'll be looking\\n",
        "for me by now.\\p",
        "I'd better go and be\\n",
        "found.$",
    )),
    "Route132_Text_DarcyIntro": (("training here by myself", "all these people"), (
        "ELIANA: I liked training\\n",
        "here when it was empty.\\p",
        "Look at it now.$",
    )),
    "Route132_Text_DarcyDefeat": (("won't complain",), (
        "ELIANA: Fine. I won't\\n",
        "complain about the crowd.$",
    )),
    "Route132_Text_DarcyPostBattle": (("partner up",), (
        "ELIANA: Perhaps I'll team\\n",
        "up with that old man and\\l",
        "take on the other two.$",
    )),

    # -- Route 133, where things wash up -------------------------------------
    "Route133_Text_FranklinIntro": (("currents carry you", "fated"), (
        "HERMES: The current brought\\n",
        "you here too?\\p",
        "Then this was meant to\\n",
        "happen. Battle me.$",
    )),
    "Route133_Text_FranklinDefeat": (("Too much so",), (
        "HERMES: Strong. Far too\\n",
        "strong.$",
    )),
    "Route133_Text_FranklinPostBattle": (("must be cursed",), (
        "HERMES: Of all the people\\n",
        "the sea could have washed\\l",
        "up here, it sent you.\\p",
        "I must be cursed.$",
    )),
    "Route133_Text_DebraIntro": (("cast away", "drifted"), (
        "ELISA: I have had a\\n",
        "miserable life.\\p",
        "I was cast off, and this\\n",
        "is where I fetched up.$",
    )),
    "Route133_Text_DebraDefeat": (("Another loss",), (
        "ELISA: Another loss.$",
    )),
    "Route133_Text_DebraPostBattle": (("don't want it anymore",), (
        "ELISA: A life spent\\n",
        "drifting.\\p",
        "I don't want it any more.$",
    )),
    "Route133_Text_LindaIntro": (("expecting you",), (
        "MANUELA: Welcome!\\p",
        "I've been expecting you.$",
    )),
    "Route133_Text_LindaDefeat": (("No! Please",), (
        "MANUELA: No! Please!$",
    )),
    "Route133_Text_LindaPostBattle": (("annoying",), (
        "MANUELA: A strong child.\\p",
        "How very irritating.$",
    )),
    "Route133_Text_WarrenIntro": (("like everyone else",), (
        "ANACLETO: I want to win as\\n",
        "much as anyone.\\p",
        "I won't get there the way\\n",
        "everyone else does.$",
    )),
    "Route133_Text_WarrenDefeat": (("too slack",), (
        "ANACLETO: My way is still\\n",
        "too soft.$",
    )),
    "Route133_Text_WarrenPostBattle": (("way more fun", "that's obvious"), (
        "ANACLETO: Doing it my way\\n",
        "is more fun than doing it\\l",
        "theirs.\\p",
        "That much is obvious.$",
    )),
    "Route133_Text_BeckIntro": (("all the way out here",), (
        "ANSELMO: I came all this\\n",
        "way with mine.\\p",
        "On the wing, most of it.$",
    )),
    "Route133_Text_BeckDefeat": (("stunningly cool",), (
        "ANSELMO: You're\\n",
        "extraordinary.$",
    )),
    "Route133_Text_BeckPostBattle": (("MATA DO MEIO", "grown to like this place"), (
        "ANSELMO: I mean to go back\\n",
        "to MATA DO MEIO.\\p",
        "I've grown fond of out\\n",
        "here, though.$",
    )),
    "Route133_Text_MollieIntro": (("thousands", "lost count"), (
        "NEUSA: I've battled\\n",
        "thousands of times.\\p",
        "I stopped counting a long\\n",
        "while ago.$",
    )),
    "Route133_Text_MollieDefeat": (("still stings",), (
        "NEUSA: Thousands of losses\\n",
        "and each one still stings.$",
    )),
    "Route133_Text_MolliePostBattle": (("my husband and me",), (
        "NEUSA: Keep at it, young\\n",
        "one.\\p",
        "You could end up like my\\n",
        "husband and me.$",
    )),
    "Route133_Text_ConorIntro": (("go with", "without direction"), (
        "DONATO: Young people let\\n",
        "themselves be carried.\\p",
        "No direction of their own.$",
    )),
    "Route133_Text_ConorDefeat": (("firm sense of purpose",), (
        "DONATO: You know exactly\\n",
        "where you're going.$",
    )),
    "Route133_Text_ConorPostBattle": (("lead you astray", "as you grow older"), (
        "DONATO: Don't let people\\n",
        "steer you.\\p",
        "And don't lose your own\\n",
        "direction as you age.$",
    )),

    # -- Route 134, the hard current ------------------------------------------
    "Route134_Text_JackIntro": (("carried along by the rapid",), (
        "JURANDIR: Even the ones\\n",
        "built for water get taken\\l",
        "by this current.$",
    )),
    "Route134_Text_JackDefeat": (("Aiyeeeeh",), (
        "JURANDIR: Aiyeeeh!$",
    )),
    "Route134_Text_JackPostBattle": (("fast-running",), (
        "JURANDIR: I think they\\n",
        "enjoy the fast water.\\p",
        "They keep coming back to\\n",
        "it.$",
    )),
    "Route134_Text_LaurelIntro": (("fun", "match"), (
        "LURDES: Mine are after a\\n",
        "friendly match.\\p",
        "Will you join us?$",
    )),
    "Route134_Text_LaurelDefeat": (("Oopsie",), (
        "LURDES: Oopsie!$",
    )),
    "Route134_Text_LaurelPostBattle": (("collector who's after",), (
        "LURDES: There's a collector\\n",
        "somewhere out here.\\p",
        "He wants what mine shed.\\n",
        "He can ask them himself.$",
    )),
    "Route134_Text_AlexIntro": (("enough rest",), (
        "AILTON: Right! Rest is\\n",
        "over, all of you!\\p",
        "Time to work.$",
    )),
    "Route134_Text_AlexDefeat": (("Tuckered out",), (
        "AILTON: Worn out. Again.$",
    )),
    "Route134_Text_AlexPostBattle": (("long flight",), (
        "AILTON: Mine tire fast\\n",
        "after a long flight.\\p",
        "It's a long way out here.$",
    )),
    "Route134_Text_HitoshiIntro": (("No need for words",), (
        "JAIME: You're a TRAINER.\\p",
        "No words needed. We\\n",
        "battle.$",
    )),
    "Route134_Text_HitoshiDefeat": (("… … … … … …",), (
        "JAIME: ... ... ...\\p",
        "... ... ...$",
    )),
    "Route134_Text_HitoshiPostBattle": (("deeply shamed",), (
        "JAIME: I challenged you,\\n",
        "and I lost.\\p",
        "I am ashamed.$",
    )),
    "Route134_Text_AaronIntro": (("savage tide",), (
        "ABEL: This tide is brutal.\\p",
        "That's exactly why we\\n",
        "train in it.$",
    )),
    "Route134_Text_AaronDefeat": (("willingly concede",), (
        "ABEL: I concede, and\\n",
        "gladly.$",
    )),
    "Route134_Text_AaronPostBattle": (("RUINAS DA QUEDA", "toughen you up"), (
        "ABEL: We're going back to\\n",
        "train at RUINAS DA QUEDA.\\p",
        "Come if you like. It will\\n",
        "harden you.$",
    )),
    "Route134_Text_KelvinIntro": (("our boat", "tide carried it"), (
        "MOACIR: Our boat!\\p",
        "The tide has taken our\\n",
        "boat!$",
    )),
    "Route134_Text_KelvinDefeat": (("Please, stop",), (
        "MOACIR: Awawah! Please!\\n",
        "Stop! Please!$",
    )),
    "Route134_Text_KelvinPostBattle": (("get home", "feels wrong"), (
        "MOACIR: No boat. How do we\\n",
        "get home?\\p",
        "I know a worn-out one can\\n",
        "still carry us.\\p",
        "I don't want to ask that.$",
    )),
    "Route134_Text_MarleyIntro": (("lightning-quick",), (
        "MILENA: Can yours get out\\n",
        "of the way in time?$",
    )),
    "Route134_Text_MarleyDefeat": (("technique existed",), (
        "MILENA: I've never seen\\n",
        "that done before.\\p",
        "You took us apart.$",
    )),
    "Route134_Text_MarleyPostBattle": (("passion for speed",), (
        "MILENA: I still want to be\\n",
        "the fastest thing here.\\p",
        "I'll work at it.$",
    )),
    "Route134_Text_ReynaIntro": (("can't be taken down",), (
        "PRISCILA: Mine do not go\\n",
        "down easily.$",
    )),
    "Route134_Text_ReynaDefeat": (("Explain how I lost",), (
        "PRISCILA: You're joking.\\n",
        "Explain how I lost that.$",
    )),
    "Route134_Text_ReynaPostBattle": (("work my way back up",), (
        "PRISCILA: Ha! You won\\n",
        "outright.\\p",
        "I'll climb back up through\\n",
        "whoever I meet.$",
    )),
    "Route134_Text_HudsonIntro": (("another SAILOR",), (
        "JANUARIO: Have you seen\\n",
        "another SAILOR out here?$",
    )),
    "Route134_Text_HudsonDefeat": (("that's something",), (
        "JANUARIO: Now, that is\\n",
        "something.$",
    )),
    "Route134_Text_HudsonPostBattle": (("drifted out to sea", "timid"), (
        "JANUARIO: Our boat drifted\\n",
        "off.\\p",
        "My friend frightens\\n",
        "easily. I'm worried about\\l",
        "him.$",
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
        masked = masked[:start] + '\t.string "<ARAUNA_FAR_WATER_EN>"\n\n' + masked[end:]
    return masked


def validate_rendered(source: str, rendered: str) -> None:
    if mask(source) != mask(rendered):
        raise ValueError("non-dialogue structure changed while rendering")

    forbidden = ("Violeiro", "bathing suit", "It must be my beauty",
                 "ogle", "I'm one happy guy")
    for label in TARGETS:
        body = block_pattern(label).search(rendered).group("body")
        for token in forbidden:
            if token in body:
                raise ValueError(f"{label}: vanilla voice survived: {token}")

    # The floating town is the only thread this stretch of water has.
    town = "".join("".join(p) for label, (_, p) in TARGETS.items()
                   if label.startswith("Route131"))
    if town.count("CASA DA") < 3:
        raise ValueError("Route 131 stopped being about Casa da Fogueira")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Render the Route 130-134 trainers in English.")
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
    print(f"Far water trainers English renderer OK: {len(TARGETS)} blocks "
          f"across Routes 130 to 134.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
