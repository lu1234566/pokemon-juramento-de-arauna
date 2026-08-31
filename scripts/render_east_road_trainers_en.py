#!/usr/bin/env python3
"""The trainers of Route 123 and Route 124: the long east road and the water
below Baia das Luzes.

A hundred and two blocks. Route 123 runs back along the ridge under the
Memorial dos Nomes, and half the people on it are still thinking about the
place -- one trains there, one asks whether yours will sleep there too.
Route 124 is the open water on the other side, where divers, drifters and one
long-suffering older sister are all sharing the same stretch of sea.

Route 123 keeps naming the Memorial, because it is the road that lives in its
shadow, and the renderer will not publish if it stops.

The twins stay twins and the sister and brother stay a sister and brother: LILA
still blames RUI for every loss and RUI still expects to hear about it later.

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
    # -- Route 123, the ridge road under the Memorial -----------------------
    "Route123_Text_WendyIntro": (("how strong you are", "the test"), (
        "BRIGIDA: Want to know how\\n",
        "strong you actually are?\\p",
        "I'll be the measure.$",
    )),
    "Route123_Text_WendyDefeat": (("flying colors",), (
        "BRIGIDA: You passed. Easily.$",
    )),
    "Route123_Text_WendyPostBattle": (("To best even me",), (
        "BRIGIDA: To get past me at\\n",
        "all.\\p",
        "You're something.$",
    )),
    "Route123_Text_BraxtonIntro": (("GYM BADGES", "worthy"), (
        "BALTAZAR: That's a lot of\\n",
        "BADGES you're carrying.\\p",
        "Let's see if you earned\\n",
        "them.$",
    )),
    "Route123_Text_BraxtonDefeat": (("you're worthy",), (
        "BALTAZAR: You earned them.\\n",
        "Every one.$",
    )),
    "Route123_Text_BraxtonPostBattle": (("BADGES proud",), (
        "BALTAZAR: You did those\\n",
        "BADGES credit just now.$",
    )),
    "Route123_Text_VioletIntro": (("good aromas",), (
        "ZORAIDE: They say a good\\n",
        "hour has a good smell to\\l",
        "it.$",
    )),
    "Route123_Text_VioletDefeat": (("bitter scent",), (
        "ZORAIDE: Oh. And this hour\\n",
        "smells bitter.$",
    )),
    "Route123_Text_VioletPostBattle": (("BERRY MASTER's garden",), (
        "ZORAIDE: The BERRY MASTER's\\n",
        "garden is the best-smelling\\l",
        "place on this road.$",
    )),
    "Route123_Text_CameronIntro": (("willpower", "makes me strong"), (
        "CANDIDO: This is all will.\\p",
        "I've decided not to lose.\\n",
        "That's what makes me hard.$",
    )),
    "Route123_Text_CameronDefeat": (("I feel sad",), (
        "CANDIDO: I feel very sad.$",
    )),
    "Route123_Text_CameronPostBattle": (("wouldn't lose to you",), (
        "CANDIDO: It's all will.\\p",
        "I had decided I wouldn't\\n",
        "lose to you.$",
    )),
    "Route123_Text_CameronRegister": (("I sense it", "POKéNAV"), (
        "CANDIDO: I sense we'll meet\\n",
        "again.\\p",
        "I can't sense who wins.\\p",
        "Your POKéNAV, then.$",
    )),
    "Route123_Text_CameronRematchIntro": (("convinced myself",), (
        "CANDIDO: I've convinced\\n",
        "myself I can't lose.\\p",
        "That's the whole method.$",
    )),
    "Route123_Text_CameronRematchDefeat": (("I feel sad",), (
        "CANDIDO: I feel very sad.$",
    )),
    "Route123_Text_CameronPostRematch": (("MEMORIAL DOS NOMES", "never beat you"), (
        "CANDIDO: I should go and\\n",
        "train at the MEMORIAL DOS\\l",
        "NOMES.\\p",
        "I'll never beat you like\\n",
        "this.$",
    )),
    "Route123_Text_JackiIntro": (("psychic powers", "refine those powers"), (
        "HELOISA: Don't celebrate\\n",
        "when yours shows something\\l",
        "unusual.\\p",
        "It's worth nothing until\\n",
        "you sharpen it.$",
    )),
    "Route123_Text_JackiDefeat": (("Overwhelmed",), (
        "HELOISA: Overwhelmed.$",
    )),
    "Route123_Text_JackiPostBattle": (("forgotten how to use them",), (
        "HELOISA: Everyone has\\n",
        "something like it.\\p",
        "Most of us have simply\\n",
        "forgotten how.$",
    )),
    "Route123_Text_JackiRegister": (("face you again",), (
        "HELOISA: I'd like to face\\n",
        "you again. May I?$",
    )),
    "Route123_Text_JackiRematchIntro": (("awoken the psychic",), (
        "HELOISA: Have you woken\\n",
        "anything up in yourself\\l",
        "since we met?$",
    )),
    "Route123_Text_JackiRematchDefeat": (("Astounding",), (
        "HELOISA: Astounding.$",
    )),
    "Route123_Text_JackiPostRematch": (("could be a psychic power",), (
        "HELOISA: What you do with\\n",
        "them.\\p",
        "That may be the same thing\\n",
        "under another name.$",
    )),
    "Route123_Text_MiuIntro": (("won't cry when they lose",), (
        "IZA: Hello, TRAINER.\\p",
        "I hope yours don't cry\\n",
        "when they lose.$",
    )),
    "Route123_Text_MiuDefeat": (("we lost",), (
        "IZA: Oh. We lost.$",
    )),
    "Route123_Text_MiuPostBattle": (("because you are friends",), (
        "IZA: Yours are strong\\n",
        "because they like you.\\p",
        "That's the whole secret,\\n",
        "isn't it.$",
    )),
    "Route123_Text_MiuNotEnoughMons": (("two POKéMON",), (
        "IZA: It isn't any fun\\n",
        "unless you bring two.$",
    )),
    "Route123_Text_YukiIntro": (("Okay", "beating"), (
        "YARA: Right! We're taking\\n",
        "this one!$",
    )),
    "Route123_Text_YukiDefeat": (("we lost",), (
        "YARA: Oh. We lost.$",
    )),
    "Route123_Text_YukiPostBattle": (("never lost before",), (
        "YARA: Why are you so\\n",
        "strong?\\p",
        "We had never lost before.$",
    )),
    "Route123_Text_YukiNotEnoughMons": (("two POKéMON",), (
        "YARA: It isn't any fun\\n",
        "unless you bring two.$",
    )),
    "Route123_Text_KindraIntro": (("MEMORIAL DOS NOMES", "sleep"), (
        "LILIAN: The MEMORIAL DOS\\n",
        "NOMES is up there.\\p",
        "Where they're laid down\\n",
        "and named.\\p",
        "Will yours be, one day?$",
    )),
    "Route123_Text_KindraDefeat": (("Overflowing with vitality",), (
        "LILIAN: So much life in\\n",
        "them. Too much for me.$",
    )),
    "Route123_Text_KindraPostBattle": (("soothes spirits",), (
        "LILIAN: Up at the MEMORIAL\\n",
        "DOS NOMES.\\p",
        "Something there settles\\n",
        "the ones who are grieving.$",
    )),
    "Route123_Text_FernandoIntro": (("lights out", "rip through this tune"), (
        "HELIO: I'll have your\\n",
        "lights out before this\\l",
        "song finishes!$",
    )),
    "Route123_Text_FernandoDefeat": (("still playing the intro",), (
        "HELIO: Hold on! I was still\\n",
        "on the intro!$",
    )),
    "Route123_Text_FernandoPostBattle": (("rock steady", "write a tune"), (
        "HELIO: You're rock steady.\\p",
        "I'd like to write something\\n",
        "about you.$",
    )),
    "Route123_Text_FernandoRegister": (("lend your ears",), (
        "HELIO: Next time, stay for\\n",
        "the whole song.$",
    )),
    "Route123_Text_FernandoRematchIntro": (("before", "finish singing"), (
        "HELIO: Today's the day.\\p",
        "Lights out before the last\\n",
        "chorus.$",
    )),
    "Route123_Text_FernandoRematchDefeat": (("hit the chorus",), (
        "HELIO: Hold on! I hadn't\\n",
        "reached the chorus!$",
    )),
    "Route123_Text_FernandoPostRematch": (("enthralled",), (
        "HELIO: I thought the song\\n",
        "would hold you still long\\l",
        "enough to lose.$",
    )),
    "Route123_Text_DavisIntro": (("big brother got it",), (
        "ELISEU: Look at this one!\\p",
        "My big brother got it for\\n",
        "me.$",
    )),
    "Route123_Text_DavisDefeat": (("You meanie",), (
        "ELISEU: Waaah! You're\\n",
        "horrible!$",
    )),
    "Route123_Text_DavisPostBattle": (("Don't tell my brother",), (
        "ELISEU: Don't tell my\\n",
        "brother I lost.\\p",
        "Promise. Please.$",
    )),
    "Route123_Text_JazmynIntro": (("confidence", "obviously strong"), (
        "IRENE: Beating someone\\n",
        "obviously strong would do\\l",
        "wonders for me.$",
    )),
    "Route123_Text_JazmynDefeat": (("There goes my confidence",), (
        "IRENE: There goes that,\\n",
        "then.$",
    )),
    "Route123_Text_JazmynPostBattle": (("judge a person", "looks don't lie"), (
        "IRENE: They say you can't\\n",
        "tell by looking.\\p",
        "In your case, one look was\\n",
        "quite enough.$",
    )),
    "Route123_Text_FrederickIntro": (("Hello, child", "spare some time"), (
        "HIGINO: Hello there, child.\\p",
        "Could you spare an old man\\n",
        "a moment?$",
    )),
    "Route123_Text_FrederickDefeat": (("allowance",), (
        "HIGINO: A very capable\\n",
        "child indeed.\\p",
        "Let me add something to\\n",
        "your pocket money.$",
    )),
    "Route123_Text_FrederickPostBattle": (("prize money enough",), (
        "HIGINO: Pocket money, I\\n",
        "said?\\p",
        "Wasn't the prize enough?$",
    )),
    "Route123_Text_AlbertoIntro": (("obsession", "Birds are cool"), (
        "AFONSO: I have to tell you.\\p",
        "The ones with wings are my\\n",
        "whole life.\\p",
        "Nothing else comes close.$",
    )),
    "Route123_Text_AlbertoDefeat": (("Even in defeat",), (
        "AFONSO: Even beaten, they\\n",
        "look magnificent.$",
    )),
    "Route123_Text_AlbertoPostBattle": (("feathers", "make a hat"), (
        "AFONSO: I gather the\\n",
        "feathers that come loose\\l",
        "in battle.\\p",
        "There'll be a hat one day.$",
    )),
    "Route123_Text_EdIntro": (("no TRAINERS around", "watch them"), (
        "FLAVIO: When nobody's\\n",
        "about, I let mine battle\\l",
        "each other.\\p",
        "I just watch.$",
    )),
    "Route123_Text_EdDefeat": (("kind of like your POKéMON",), (
        "FLAVIO: I rather like\\n",
        "yours.$",
    )),
    "Route123_Text_EdPostBattle": (("swiping your battling ideas",), (
        "FLAVIO: Hehe. I'm stealing\\n",
        "how you did that.\\p",
        "It'll make me better.$",
    )),
    "Route123_Text_JonasIntro": (("ambush", "trap"), (
        "MANOEL: I lay in wait, and\\n",
        "someone walked into it!$",
    )),
    "Route123_Text_JonasDefeat": (("playing ninja",), (
        "MANOEL: If you don't lose,\\n",
        "how am I meant to enjoy\\l",
        "this?$",
    )),
    "Route123_Text_JonasPostBattle": (("weaker-looking",), (
        "MANOEL: Next time I'll\\n",
        "ambush someone who looks\\l",
        "easier.$",
    )),
    "Route123_Text_KayleyIntro": (("just bought this parasol",), (
        "LETICIA: New parasol.\\p",
        "I reckon it improves me\\n",
        "by a third.$",
    )),
    "Route123_Text_KayleyDefeat": (("five times",), (
        "LETICIA: You're about five\\n",
        "times better than me.$",
    )),
    "Route123_Text_KayleyPostBattle": (("accessories", "fashion appeal"), (
        "LETICIA: What you carry\\n",
        "changes how you're read.\\p",
        "That's most of it, really.$",
    )),

    # -- Route 124, the water below Baia das Luzes --------------------------
    "Route124_Text_SpencerIntro": (("lost at sea", "pilot"), (
        "VALDIR: Are you lost out\\n",
        "here?\\p",
        "Beat mine and I'll pilot\\n",
        "you in.$",
    )),
    "Route124_Text_SpencerDefeat": (("lost my bearings",), (
        "VALDIR: I lost my bearings\\n",
        "mid-battle.$",
    )),
    "Route124_Text_SpencerPostBattle": (("POKéNAV's MAP",), (
        "VALDIR: People lose\\n",
        "themselves out here often.\\p",
        "If that's you, use the MAP\\n",
        "on your POKéNAV.$",
    )),
    "Route124_Text_RolandIntro": (("riding a POKéMON", "envious"), (
        "TARCISIO: You're riding\\n",
        "instead of swimming.\\p",
        "I'm envious.$",
    )),
    "Route124_Text_RolandDefeat": (("I can't",), (
        "TARCISIO: Oh. I can't.$",
    )),
    "Route124_Text_RolandPostBattle": (("getting chilled", "ride a POKéMON"), (
        "TARCISIO: I've gone cold.\\p",
        "Too many hours in the\\n",
        "water.\\p",
        "I wish I could ride, like\\n",
        "you.$",
    )),
    "Route124_Text_JennyIntro": (("just float", "come around to play"), (
        "IVANI: Float here long\\n",
        "enough and they come to\\l",
        "you.$",
    )),
    "Route124_Text_JennyDefeat": (("gone and lost",), (
        "IVANI: Oh, bother. Lost.$",
    )),
    "Route124_Text_JennyPostBattle": (("some just watch", "personalities"), (
        "IVANI: Some of them come\\n",
        "at you. Some only watch.\\p",
        "They're each somebody\\n",
        "different.$",
    )),
    "Route124_Text_JennyRegister": (("on a whim", "POKéNAV"), (
        "IVANI: On a whim, then.\\p",
        "Put me in your POKéNAV.$",
    )),
    "Route124_Text_JennyRematchIntro": (("TRAINERS challenge you",), (
        "IVANI: Float here long\\n",
        "enough and TRAINERS come\\l",
        "to you as well.$",
    )),
    "Route124_Text_JennyRematchDefeat": (("I lost again",), (
        "IVANI: Strange. Beaten\\n",
        "again.$",
    )),
    "Route124_Text_JennyPostRematch": (("CASA DOS TRUQUES",), (
        "IVANI: Unrelated, but I\\n",
        "might go and see the\\l",
        "CASA DOS TRUQUES.$",
    )),
    "Route124_Text_GraceIntro": (("growing bored of swimming",), (
        "EUNICE: I've grown bored\\n",
        "of swimming.\\p",
        "Battle instead?$",
    )),
    "Route124_Text_GraceDefeat": (("no idea that you were",), (
        "EUNICE: I had no idea you\\n",
        "were this strong.$",
    )),
    "Route124_Text_GracePostBattle": (("effort you put in",), (
        "EUNICE: Nobody arrives\\n",
        "here by accident.\\p",
        "You put the hours in.$",
    )),
    "Route124_Text_ChadIntro": (("deep underwater", "Plumbing the depths"), (
        "CESAR: Heheh. I go down\\n",
        "where nobody follows.\\p",
        "The deep is where I'm\\n",
        "good.$",
    )),
    "Route124_Text_ChadDefeat": (("I'm sinking",), (
        "CESAR: Glub. Glub. Down\\n",
        "I go.$",
    )),
    "Route124_Text_ChadPostBattle": (("DIVE spot",), (
        "CESAR: I hear there's a\\n",
        "DIVE spot near here.\\p",
        "Now I want to go down\\n",
        "again.$",
    )),
    "Route124_Text_LilaIntro": (("who's with me", "little brother"), (
        "LILA: Sigh.\\p",
        "The whole sea to myself,\\n",
        "and who is with me?\\p",
        "My little brother.\\p",
        "Battle me so I stop\\n",
        "thinking about it.$",
    )),
    "Route124_Text_LilaDefeat": (("your fault we lost",), (
        "LILA: RUI! That was your\\n",
        "fault!\\p",
        "We'll discuss it later.$",
    )),
    "Route124_Text_LilaPostBattle": (("nice boyfriend",), (
        "LILA: Sigh.\\p",
        "One day I'll swim out here\\n",
        "with someone who chose to\\l",
        "come.$",
    )),
    "Route124_Text_LilaNotEnoughMons": (("two POKéMON",), (
        "LILA: Battle us? Not with\\n",
        "one, you won't.$",
    )),
    "Route124_Text_RoyIntro": (("big sister is tough", "Don't cry"), (
        "RUI: My big sister is very\\n",
        "good at this.\\p",
        "Don't cry when you lose.$",
    )),
    "Route124_Text_RoyDefeat": (("chew me out",), (
        "RUI: Uh-oh. She's going to\\n",
        "have words with me.$",
    )),
    "Route124_Text_RoyPostBattle": (("really scary", "boyfriend"), (
        "RUI: My sister is frightening\\n",
        "when she's angry.\\p",
        "I'd know. I'm usually why.$",
    )),
    "Route124_Text_LilaRoyRegister": (("battle with us again", "take it easy"), (
        "RUI: Battle us again?\\p",
        "Go easier next time,\\n",
        "though. Please.$",
    )),
    "Route124_Text_RoyNotEnoughMons": (("Bring two",), (
        "RUI: Wanted a battle?\\n",
        "Bring two, then.$",
    )),
    "Route124_Text_LilaRematchIntro": (("been a while", "dwell on things"), (
        "LILA: Sigh. Still out here.\\n",
        "Still with my brother.\\p",
        "It's been a while. Battle\\n",
        "me so I stop dwelling.$",
    )),
    "Route124_Text_LilaRematchDefeat": (("training session later",), (
        "LILA: RUI! Your fault\\n",
        "again!\\p",
        "We're training tonight.$",
    )),
    "Route124_Text_LilaPostRematch": (("lovely combinations",), (
        "LILA: Sigh.\\p",
        "With the right partner\\n",
        "beside me we'd beat\\l",
        "anyone out here.$",
    )),
    "Route124_Text_LilaRematchNotEnoughMons": (("two POKéMON",), (
        "LILA: Battle us? Not with\\n",
        "one.$",
    )),
    "Route124_Text_RoyRematchIntro": (("catch heck", "all out"), (
        "RUI: If we lose I'll hear\\n",
        "about it for a week.\\p",
        "So I'm going all out.$",
    )),
    "Route124_Text_RoyRematchDefeat": (("chew me out again",), (
        "RUI: Uh-oh. Words again.$",
    )),
    "Route124_Text_RoyPostRematch": (("train really", "hard with POKéMON later"), (
        "RUI: My sister is\\n",
        "frightening when she's\\l",
        "angry.\\p",
        "I'm training all evening\\n",
        "because of this.$",
    )),
    "Route124_Text_RoyRematchNotEnoughMons": (("Bring two",), (
        "RUI: Wanted a battle?\\n",
        "Bring two.$",
    )),
    "Route124_Text_DeclanIntro": (("by my lonesome", "pathetic"), (
        "ERNANI: The whole sea, and\\n",
        "I'm swimming it alone.\\p",
        "There's no kind word for\\n",
        "that.$",
    )),
    "Route124_Text_DeclanDefeat": (("feeling blue",), (
        "ERNANI: Blue as the sky\\n",
        "over me.$",
    )),
    "Route124_Text_DeclanPostBattle": (("lady SWIMMERS", "long swim"), (
        "ERNANI: I should talk to\\n",
        "the other SWIMMERS.\\p",
        "Ask if anyone wants a long\\n",
        "one out to the point.$",
    )),
    "Route124_Text_IsabellaIntro": (("surfer TRAINER",), (
        "GLORIA: I'm not losing to\\n",
        "someone who arrived by\\l",
        "riding.$",
    )),
    "Route124_Text_IsabellaDefeat": (("sweat in my eyes",), (
        "GLORIA: That's salt water\\n",
        "in my eyes.\\p",
        "I am not crying.$",
    )),
    "Route124_Text_IsabellaPostBattle": (("colored shards",), (
        "GLORIA: There are coloured\\n",
        "shards of things down\\l",
        "there.\\p",
        "People come out just for\\n",
        "them.$",
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
        masked = masked[:start] + '\t.string "<ARAUNA_EAST_ROAD_EN>"\n\n' + masked[end:]
    return masked


def validate_rendered(source: str, rendered: str) -> None:
    if mask(source) != mask(rendered):
        raise ValueError("non-dialogue structure changed while rendering")

    forbidden = ("nice boyfriend", "lady SWIMMERS", "playing ninja",
                 "cuteness should be up", "Contribute to your allowance")
    for label in TARGETS:
        body = block_pattern(label).search(rendered).group("body")
        for token in forbidden:
            if token in body:
                raise ValueError(f"{label}: vanilla voice survived: {token}")

    ridge = "".join("".join(p) for label, (_, p) in TARGETS.items()
                    if label.startswith("Route123"))
    if ridge.count("MEMORIAL DOS") < 2:
        raise ValueError("Route 123 stopped living in the Memorial's shadow")

    siblings = "".join("".join(p) for label, (_, p) in TARGETS.items()
                       if "Lila" in label or "Roy" in label)
    if "RUI" not in siblings or "sister" not in siblings:
        raise ValueError("Route 124 lost the sister and brother")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Render the Route 123 and Route 124 trainers in English.")
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
    print(f"East road trainers English renderer OK: {len(TARGETS)} blocks "
          f"across Routes 123 and 124.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
