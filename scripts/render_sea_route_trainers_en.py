#!/usr/bin/env python3
"""The trainers of Routes 105 to 108, the open water.

Ninety blocks, all of them swimmers, fishermen and one triathlete who is only
halfway through her event. Between Porto das Redes and Porto do Sal the player
spends a long stretch on the water, and every line out here was still Emerald's.

Some of it had aged badly and is simply gone: a woman quoting her boyfriend on
how she looks in a bikini, another refusing to say her weight, a third planning
a frilly swimsuit. What replaces them is what a person on the water would
actually say -- about the tide, the depth, the boat, the fish that got away.

Each trainer keeps their hook. The rock collector still cannot stop looking at
the rock, the fisherman still will not leave his rod to find a washroom, the
brother still lost every time until he had his sister beside him.

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
    # -- Route 105, the deep water and the standing rock --------------------
    "Route105_Text_FosterIntro": (("mystical", "rock"), (
        "HERALDO: There's a stone out\\n",
        "here that shouldn't be.\\p",
        "Do you know anything\\n",
        "about it?$",
    )),
    "Route105_Text_FosterDefeated": (("thinking too much", "remained weak"), (
        "HERALDO: I was watching the\\n",
        "stone instead of the battle.$",
    )),
    "Route105_Text_FosterPostBattle": (("staring", "growing bored"), (
        "HERALDO: I can look at a\\n",
        "good stone all afternoon\\l",
        "and not notice the hours.$",
    )),
    "Route105_Text_LuisIntro": (("drowning", "battle"), (
        "ORESTES: I thought you were\\n",
        "in trouble out here.\\p",
        "You're fine. So: battle?$",
    )),
    "Route105_Text_LuisDefeated": (("Glub",), (
        "ORESTES: Glub... glub...$",
    )),
    "Route105_Text_LuisPostBattle": (("wave one arm",), (
        "ORESTES: If you ever are in\\n",
        "trouble out here, one arm\\l",
        "up, toward the beach.\\p",
        "Somebody always sees it.$",
    )),
    "Route105_Text_DominikIntro": (("deep blue sea", "greatest"), (
        "EVANDRO: Deep water.\\p",
        "There's nothing better.$",
    )),
    "Route105_Text_DominikDefeated": (("feeling blue",), (
        "EVANDRO: Lost. Now I match\\n",
        "the water.$",
    )),
    "Route105_Text_DominikPostBattle": (("Why is the sea blue", "MUSEUM"), (
        "EVANDRO: Why is the sea\\n",
        "blue, anyway?\\p",
        "They explained it at the\\n",
        "museum in PORTO DO SAL.\\p",
        "I've forgotten already.$",
    )),
    "Route105_Text_BeverlyIntro": (("body feels lighter",), (
        "CATARINA: Everything is\\n",
        "lighter out here.\\p",
        "Me included.$",
    )),
    "Route105_Text_BeverlyDefeated": (("floating",), (
        "CATARINA: I'm just floating\\n",
        "now.$",
    )),
    "Route105_Text_PostBattle": (("one tenth", "my weight"), (
        "CATARINA: In water you carry\\n",
        "a tenth of what you weigh.\\p",
        "That's the only reason I\\n",
        "swim this far out.$",
    )),
    "Route105_Text_ImaniIntro": (("vast sea", "peaceful"), (
        "GILDA: Sky above, water\\n",
        "below, nothing in between.\\p",
        "It's very quiet here.$",
    )),
    "Route105_Text_ImaniDefeated": (("lounging",), (
        "GILDA: Beaten while I was\\n",
        "drifting.$",
    )),
    "Route105_Text_ImaniPostBattle": (("relaxing to be", "Giggle"), (
        "GILDA: I'd like to be the\\n",
        "kind of person who is\\l",
        "restful to be near.$",
    )),
    "Route105_Text_AndresIntro": (("sea keeps", "secrets"), (
        "ALCEU: The sea is keeping\\n",
        "things from us.\\p",
        "I intend to find out what.$",
    )),
    "Route105_Text_AndresDefeated": (("no good at battling",), (
        "ALCEU: Yes. I'm no good at\\n",
        "this part.$",
    )),
    "Route105_Text_AndresPostBattle": (("many secrets", "find them all"), (
        "ALCEU: Every sea is holding\\n",
        "something back.\\p",
        "I mean to see all of it.$",
    )),
    "Route105_Text_AndresRegister": (("so weak", "POKéNAV"), (
        "ALCEU: I lose constantly,\\n",
        "and you still want me in\\l",
        "your POKéNAV?$",
    )),
    "Route105_Text_AndresRematchIntro": (("I'm weak", "sure you want"), (
        "ALCEU: I did warn you that\\n",
        "I'm not good at this.\\p",
        "Still want to?$",
    )),
    "Route105_Text_AndresRematchDefeated": (("didn't think I could win",), (
        "ALCEU: I never expected to\\n",
        "win that.$",
    )),
    "Route105_Text_AndresRematchPostBattle": (("drive to explore", "travel the seas"), (
        "ALCEU: I'm a poor TRAINER.\\p",
        "Nobody has ever out-wanted\\n",
        "me, though.\\p",
        "I'll see every sea there is.$",
    )),
    "Route105_Text_JosueIntro": (("exhausted from swimming", "change of pace"), (
        "MARTIM: Swimming wears me\\n",
        "out. I'm a land creature.\\p",
        "Battle me instead.$",
    )),
    "Route105_Text_JosueDefeated": (("battled at sea",), (
        "MARTIM: That's what I get\\n",
        "for fighting in water.$",
    )),
    "Route105_Text_JosuePostBattle": (("the sky", "better"), (
        "MARTIM: Give me open sky\\n",
        "over open water.\\p",
        "At least the sky holds\\n",
        "still.$",
    )),

    # -- Route 106, the rod and the reef ------------------------------------
    "Route106_Text_ElliotIntro": (("fishing in the", "stream"), (
        "GILBERTO: Sea fishing or\\n",
        "river fishing?\\p",
        "Pick one. I'll argue.$",
    )),
    "Route106_Text_ElliotDefeated": (("deep-sea fishing", "spectacularly"), (
        "GILBERTO: Went down like a\\n",
        "bad cast.$",
    )),
    "Route106_Text_ElliotPostBattle": (("Fishing is the greatest",), (
        "GILBERTO: Sea or river, it\\n",
        "hardly matters.\\p",
        "You're waiting either way.$",
    )),
    "Route106_Text_ElliotRegister": (("can we meet again",), (
        "GILBERTO: Fishing is good.\\n",
        "So is this.\\p",
        "Come find me again?$",
    )),
    "Route106_Text_ElliotRematchIntro": (("caught a bunch", "impressive battle"), (
        "GILBERTO: The rod's been\\n",
        "kind to me lately.\\p",
        "Watch what came up.$",
    )),
    "Route106_Text_ElliotRematchDefeated": (("lost again spectacularly",), (
        "GILBERTO: Down again, and\\n",
        "just as hard.$",
    )),
    "Route106_Text_ElliotRematchPostBattle": (("Win or lose",), (
        "GILBERTO: Win or lose, I'd\\n",
        "rather be out here than\\l",
        "anywhere they keep chairs.$",
    )),
    "Route106_Text_NedIntro": (("washroom", "big one"), (
        "QUIRINO: I have needed the\\n",
        "washroom for an hour.\\p",
        "The moment I leave, the rod\\n",
        "will go. It always does.$",
    )),
    "Route106_Text_NedDefeated": (("trying to not go",), (
        "QUIRINO: Hard to focus.\\n",
        "You know why.$",
    )),
    "Route106_Text_NedPostBattle": (("I'll hook",), (
        "QUIRINO: Oh no. I can feel\\n",
        "one coming.$",
    )),
    "Route106_Text_DouglasIntro": (("lousy runner", "can't catch me"), (
        "FABIANO: On land you'd have\\n",
        "me in ten steps.\\p",
        "Out here? Try.$",
    )),
    "Route106_Text_DouglasDefeated": (("I give up",), (
        "FABIANO: All right, all\\n",
        "right. You win.$",
    )),
    "Route106_Text_DouglasPostBattle": (("swim race",), (
        "FABIANO: Race me instead\\n",
        "and see how that goes.$",
    )),
    "Route106_Text_KylaIntro": (("my backyard", "because you're a kid"), (
        "LUCIA: This water is my\\n",
        "yard.\\p",
        "I won't go easy just\\n",
        "because you're small.$",
    )),
    "Route106_Text_KylaDefeated": (("take it easy on me",), (
        "LUCIA: Did YOU go easy on\\n",
        "ME just now?$",
    )),
    "Route106_Text_KylaPostBattle": (("Drifting along", "give it a try"), (
        "LUCIA: Stop swimming and\\n",
        "let the water carry you.\\p",
        "Try it once. You'll see.$",
    )),

    # -- Route 107, the crossing and the sister and brother -----------------
    "Route107_Text_DarrinIntro": (("drifted off to sleep",), (
        "EDSON: Mm. I fell asleep\\n",
        "out here again.$",
    )),
    "Route107_Text_DarrinDefeated": (("take a snooze",), (
        "EDSON: Beaten. Back to\\n",
        "sleep, I think.$",
    )),
    "Route107_Text_DarrinPostBattle": (("rocked by", "comfy bed"), (
        "EDSON: The swell rocks you.\\p",
        "Better than any bed I've\\n",
        "ever paid for.$",
    )),
    "Route107_Text_TonyIntro": (("like my backyard", "Let's battle"), (
        "WILSON: This crossing is my\\n",
        "yard. Come on.$",
    )),
    "Route107_Text_TonyDefeated": (("home field",), (
        "WILSON: Beaten in my own\\n",
        "yard. That stings.$",
    )),
    "Route107_Text_TonyPostBattle": (("heart full of", "It's a song"), (
        "WILSON: I swim and I sing.\\p",
        "Mostly the same song.\\n",
        "Nobody has complained yet.$",
    )),
    "Route107_Text_TonyRegister": (("shocked me", "won't forget me"), (
        "WILSON: You rattled me.\\p",
        "Take my number so you\\n",
        "don't forget who did.$",
    )),
    "Route107_Text_TonyRematchIntro": (("big, wide sea", "grown stronger"), (
        "WILSON: Long crossings.\\p",
        "They've made mine strong.$",
    )),
    "Route107_Text_TonyRematchDefeated": (("stayed weak as a TRAINER",), (
        "WILSON: Mine got stronger.\\p",
        "I didn't.$",
    )),
    "Route107_Text_TonyRematchPostBattle": (("waves taught me",), (
        "WILSON: You learn more\\n",
        "losing than swimming.\\p",
        "The water taught me that.$",
    )),
    "Route107_Text_DeniseIntro": (("PORTO DAS REDES",), (
        "ELOISA: Do you know PORTO\\n",
        "DAS REDES? Small place.$",
    )),
    "Route107_Text_DeniseDefeated": (("I hate this",), (
        "ELOISA: Oh, I hate this.$",
    )),
    "Route107_Text_DenisePostBattle": (("trendy", "HALL"), (
        "ELOISA: There's a saying\\n",
        "going round the hall in\\l",
        "PORTO DAS REDES.\\p",
        "Everyone's repeating it.$",
    )),
    "Route107_Text_BethIntro": (("Did you want to battle",), (
        "CAROL: You want a battle?\\p",
        "Sure. Let's go.$",
    )),
    "Route107_Text_BethDefeated": (("wasn't good enough",), (
        "CAROL: Not good enough\\n",
        "today.$",
    )),
    "Route107_Text_BethPostBattle": (("keep getting", "I'll go for it"), (
        "CAROL: You're going to keep\\n",
        "improving, aren't you.\\p",
        "Then so am I.$",
    )),
    "Route107_Text_LisaIntro": (("sister", "brother"), (
        "LISA: Sister and brother.\\p",
        "You take us both.$",
    )),
    "Route107_Text_LisaDefeated": (("different class",), (
        "LISA: You're another class\\n",
        "of tough entirely.$",
    )),
    "Route107_Text_LisaPostBattle": (("go to the beach",), (
        "LISA: Have you got someone\\n",
        "who'd come to the water\\l",
        "with you? Bring them.$",
    )),
    "Route107_Text_LisaNotEnoughPokemon": (("bring more",), (
        "LISA: Two of us. Bring\\n",
        "enough for two.$",
    )),
    "Route107_Text_RayIntro": (("me and my sister", "2-on-2"), (
        "RAI: My sister and I always\\n",
        "battle together.\\p",
        "I lose alone. We don't\\n",
        "lose together.$",
    )),
    "Route107_Text_RayDefeated": (("higher level",), (
        "RAI: You're well above us.$",
    )),
    "Route107_Text_RayPostBattle": (("gave me my POKéMON", "important"), (
        "RAI: My sister gave me my\\n",
        "first one.\\p",
        "I raised it myself.\\n",
        "Now it's mine.$",
    )),
    "Route107_Text_RayNotEnoughPokemon": (("bring some more",), (
        "RAI: Not enough. Go and\\n",
        "come back.$",
    )),
    "Route107_Text_CamronIntro": (("triathlon", "nowhere near tired"), (
        "CARLOS: I'm mid-event and\\n",
        "not tired yet.$",
    )),
    "Route107_Text_CamronDefeated": (("exhausted me",), (
        "CARLOS: All right. Now I'm\\n",
        "tired.$",
    )),
    "Route107_Text_CamronPostBattle": (("swimming and running", "going to be okay"), (
        "CARLOS: Swim leg and run\\n",
        "leg still to come.\\p",
        "Am I going to survive this?$",
    )),

    # -- Route 108, the water around the wreck ------------------------------
    "Route108_Text_JeromeIntro": (("seven",), (
        "LOURIVAL: I want to swim\\n",
        "every sea there is.$",
    )),
    "Route108_Text_JeromeDefeated": (("won't be able to swim",), (
        "LOURIVAL: Not at this rate,\\n",
        "I won't.$",
    )),
    "Route108_Text_JeromePostBattle": (("pleasures of swimming",), (
        "LOURIVAL: The company down\\n",
        "here is half the reason\\l",
        "I keep swimming.$",
    )),
    "Route108_Text_MatthewIntro": (("NAVIO PERDIDO",), (
        "PASCOAL: Heading out to the\\n",
        "NAVIO PERDIDO as well?$",
    )),
    "Route108_Text_MatthewDefeated": (("sinking",), (
        "PASCOAL: Going down. Glub.$",
    )),
    "Route108_Text_MatthewPostBattle": (("go inside",), (
        "PASCOAL: Some people go\\n",
        "inside that wreck.\\p",
        "I stay out here.$",
    )),
    "Route108_Text_TaraIntro": (("boyfriend", "bikini"), (
        "VALERIA: I've been in this\\n",
        "water since morning.\\p",
        "I'm cold, I'm stubborn,\\n",
        "and I'm not getting out.$",
    )),
    "Route108_Text_TaraDefeated": (("Oh, boo",), (
        "VALERIA: Oh, boo.$",
    )),
    "Route108_Text_TaraPostBattle": (("I look great", "so complex"), (
        "VALERIA: Everyone on the\\n",
        "beach says the wreck is\\l",
        "dangerous.\\p",
        "Everyone on the beach has\\n",
        "never been near it.$",
    )),
    "Route108_Text_MissyIntro": (("forget all my worries",), (
        "NELMA: I swim to stop\\n",
        "thinking. It works.$",
    )),
    "Route108_Text_MissyDefeated": (("stressed out",), (
        "NELMA: And now I'm thinking\\n",
        "again.$",
    )),
    "Route108_Text_MissyPostBattle": (("Work off your stress",), (
        "NELMA: Whatever is sitting\\n",
        "on you, swim it off.\\p",
        "It floats away out here.$",
    )),
    "Route108_Text_CoryIntro": (("WATER-type", "other POKéMON"), (
        "DORIVAL: I love the ones\\n",
        "that live in water.\\p",
        "I love the rest too.$",
    )),
    "Route108_Text_CoryDefeated": (("Waaah",), (
        "DORIVAL: Waaah! Beaten!\\n",
        "Waaah!$",
    )),
    "Route108_Text_CoryPostBattle": (("Shouting is good",), (
        "DORIVAL: Shouting helps.\\p",
        "Try it. Nobody out here\\n",
        "will mind.$",
    )),
    "Route108_Text_CoryRegister": (("tough TRAINERS", "POKéNAV"), (
        "DORIVAL: I love a tough\\n",
        "TRAINER too!\\p",
        "Put me in your POKéNAV!$",
    )),
    "Route108_Text_CoryRematchIntro": (("love battling at sea",), (
        "DORIVAL: Win or lose, I\\n",
        "love doing this on water!$",
    )),
    "Route108_Text_CoryRematchDefeated": (("lost again",), (
        "DORIVAL: Waaah! Again!\\n",
        "Waaah!$",
    )),
    "Route108_Text_CoryRematchPostBattle": (("try shouting",), (
        "DORIVAL: When something is\\n",
        "too big for you, go and\\l",
        "shout at the sea about it.$",
    )),
    "Route108_Text_CarolinaIntro": (("huge pride", "speedy battle"), (
        "CRISTINA: I'm proud of\\n",
        "mine, and they're fast.\\p",
        "Watch how fast.$",
    )),
    "Route108_Text_CarolinaDefeated": (("wasn't cute",), (
        "CRISTINA: There was nothing\\n",
        "graceful about that.$",
    )),
    "Route108_Text_CarolinaPostBattle": (("frilly swimsuit",), (
        "CRISTINA: Out here nobody\\n",
        "is watching how you look.\\p",
        "Only how fast you go.$",
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
        masked = masked[:start] + '\t.string "<ARAUNA_SEA_ROUTES_EN>"\n\n' + masked[end:]
    return masked


def validate_rendered(source: str, rendered: str) -> None:
    if mask(source) != mask(rendered):
        raise ValueError("non-dialogue structure changed while rendering")

    # The three lines this pass exists to remove, and the loudest leftovers.
    forbidden = ("bikini", "frilly swimsuit", "not telling you my weight",
                 "seven seas", "We girls are so complex", "my liar of a")
    for label in TARGETS:
        body = block_pattern(label).search(rendered).group("body")
        for token in forbidden:
            if token in body:
                raise ValueError(f"{label}: vanilla voice survived: {token}")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Render the Route 105-108 trainers in English.")
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
    print(f"Sea route trainers English renderer OK: {len(TARGETS)} blocks "
          f"across Routes 105 to 108.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
