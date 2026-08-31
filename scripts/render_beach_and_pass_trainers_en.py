#!/usr/bin/env python3
"""The trainers of Route 109 and Route 116: the beach and the mountain road.

Ninety-two blocks in two places the player cannot avoid. Route 109 is the sand
outside Porto do Sal -- sailors off the boats, children who cannot swim without
a ring, a couple who would rather you had not come past. Route 116 is the climb
from Serra do Uivo to the tunnel, full of school pupils who have just been
taught something and want to try it on a stranger.

The two roads are written to sound different from each other, because they are:
one is a working harbour beach where everyone is off duty, and the other is a
road where everyone is on their way somewhere and slightly out of breath.

The school pupils name their teacher, and their teacher is DALVA, which is who
the badge in Serra do Uivo is from. That thread was already in the text and is
kept.

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
    # -- Route 109, the beach below Porto do Sal ----------------------------
    "Route109_Text_DavidIntro": (("chiseled abs",), (
        "EDUARDO: Look at the work\\n",
        "I've put into this.\\p",
        "Now watch it do nothing.$",
    )),
    "Route109_Text_DavidDefeated": (("Flubbed out",), (
        "EDUARDO: Aiyah! Flat!$",
    )),
    "Route109_Text_DavidPostBattle": (("nothing to do", "POKéMON battles"), (
        "EDUARDO: I train every day.\\p",
        "None of it helps in a\\n",
        "battle. I do it anyway.$",
    )),
    "Route109_Text_AliceIntro": (("protected against", "sun"), (
        "ANDREIA: Are you covered\\n",
        "up? The sun here bites.$",
    )),
    "Route109_Text_AliceDefeated": (("Ouch, ouch",), (
        "ANDREIA: Ouch, ouch, ouch.$",
    )),
    "Route109_Text_AlicePostBattle": (("Cheeks", "burning"), (
        "ANDREIA: It's always the\\n",
        "cheeks that go first.\\p",
        "Cover them.$",
    )),
    "Route109_Text_HueyIntro": (("laid anchor", "PORTO DO SAL"), (
        "JERONIMO: I've tied up in\\n",
        "harbours all over.\\p",
        "PORTO DO SAL is the one\\n",
        "I keep coming back to.$",
    )),
    "Route109_Text_HueyDefeated": (("You're the best",), (
        "JERONIMO: You're the best\\n",
        "thing in it, then.$",
    )),
    "Route109_Text_HueyPostBattle": (("best port", "best"), (
        "JERONIMO: Best port on the\\n",
        "coast, and the best TRAINER\\l",
        "standing on it.$",
    )),
    "Route109_Text_EdmondIntro": (("Urrrrppp", "Battle"), (
        "GABRIEL: Urrp... you want\\n",
        "to battle? Now?$",
    )),
    "Route109_Text_EdmondDefeated": (("Ooooooohhhhhh",), (
        "GABRIEL: Ohhhh. Urrp.$",
    )),
    "Route109_Text_EdmondPostBattle": (("seasick", "SAILOR"), (
        "GABRIEL: I'm better than\\n",
        "that, I promise.\\p",
        "I'm a SAILOR and the sea\\n",
        "makes me ill. Don't say it.$",
    )),
    "Route109_Text_RickyIntro": (("thirsty", "SEASHORE HOUSE"), (
        "SILAS: I'd trade this whole\\n",
        "beach for a cold drink at\\l",
        "the SEASHORE HOUSE.$",
    )),
    "Route109_Text_RickyDefeated": (("Groan",), (
        "SILAS: Ughhh.$",
    )),
    "Route109_Text_RickyPostBattle": (("famished", "doughnut"), (
        "SILAS: I'm so hungry my own\\n",
        "ring is starting to look\\l",
        "like something to eat.$",
    )),
    "Route109_Text_RickyRegister": (("another match", "thirsty"), (
        "SILAS: Battle me again when\\n",
        "I've had a drink?$",
    )),
    "Route109_Text_RickyRematchIntro": (("hungry", "pep"), (
        "SILAS: Still hungry. Still\\n",
        "up for this.$",
    )),
    "Route109_Text_RickyRematchDefeated": (("because I'm hungry",), (
        "SILAS: I lost because I\\n",
        "haven't eaten. That's why.$",
    )),
    "Route109_Text_RickyRematchPostBattle": (("eat on a beach",), (
        "SILAS: Food tastes better\\n",
        "on sand. Everyone knows\\l",
        "it. Nobody knows why.$",
    )),
    "Route109_Text_LolaIntro": (("beach umbrella", "giant flower"), (
        "MARA: Doesn't an umbrella\\n",
        "look like a big flower?$",
    )),
    "Route109_Text_LolaDefeated": (("Mommy",), (
        "MARA: Maaaam!$",
    )),
    "Route109_Text_LolaPostBattle": (("from the sky", "flower garden"), (
        "MARA: From up high the\\n",
        "whole beach must look\\l",
        "like a garden.$",
    )),
    "Route109_Text_LolaRegister": (("here every day",), (
        "MARA: Me? I'm here every\\n",
        "single day.$",
    )),
    "Route109_Text_LolaRematchIntro": (("not losing", "inner tube"), (
        "MARA: Not this time.\\p",
        "I brought my ring.$",
    )),
    "Route109_Text_LolaRematchDefeated": (("Mommy",), (
        "MARA: Maaaam!$",
    )),
    "Route109_Text_LolaRematchPostBattle": (("cuteness goes way up",), (
        "MARA: With the ring, both\\n",
        "of us look better.\\p",
        "That's just true.$",
    )),
    "Route109_Text_AustinaIntro": (("can't swim without", "won't lose"), (
        "CAMILA: I can't swim without\\n",
        "this ring.\\p",
        "I can still beat you.$",
    )),
    "Route109_Text_AustinaDefeated": (("Did I lose because",), (
        "CAMILA: Was it the ring?\\n",
        "It was the ring.$",
    )),
    "Route109_Text_AustinaPostBattle": (("fashion item", "can't be seen"), (
        "CAMILA: The ring isn't for\\n",
        "swimming. It's the look.\\p",
        "I don't go out without it.$",
    )),
    "Route109_Text_GwenIntro": (("big TRAINER", "battle with me"), (
        "EVA: Hello, big TRAINER.\\p",
        "Will you battle me?$",
    )),
    "Route109_Text_GwenDefeated": (("you're strong",), (
        "EVA: Oh. You're strong.$",
    )),
    "Route109_Text_GwenPostBattle": (("How did you get to be",), (
        "EVA: How do you get like\\n",
        "that? Does it take long?$",
    )),
    "Route109_Text_CarterIntro": (("catch", "big one"), (
        "CASSIANO: This man is going\\n",
        "to land a big one today!$",
    )),
    "Route109_Text_CarterDefeated": (("just lost one",), (
        "CASSIANO: This man just\\n",
        "lost one.$",
    )),
    "Route109_Text_CarterPostBattle": (("big-one-to-be",), (
        "CASSIANO: This man thinks\\n",
        "you're a big one.\\p",
        "Give it a year. Then\\n",
        "you'll be the big one.$",
    )),
    "Route109_Text_PaulIntro": (("mood-breaker", "precious time"), (
        "SAUL: Ah. You found us.\\p",
        "We came down here to be\\n",
        "away from everyone.$",
    )),
    "Route109_Text_PaulDefeated": (("I give up",), (
        "SAUL: Fine. You win.$",
    )),
    "Route109_Text_PaulPostBattle": (("don't tell anyone", "private world"), (
        "SAUL: Don't tell anyone\\n",
        "this spot is here.\\p",
        "It's the only quiet stretch\\n",
        "left on this beach.$",
    )),
    "Route109_Text_PaulNotEnoughPokemon": (("deeply in love", "battle"), (
        "SAUL: There are two of us.\\p",
        "Bring enough for two.$",
    )),
    "Route109_Text_MelIntro": (("totally in love", "romance"), (
        "MEL: We came here together\\n",
        "and we battle together.\\p",
        "That's the whole system.$",
    )),
    "Route109_Text_MelDefeated": (("my fault", "hate me"), (
        "MEL: That one was mine.\\n",
        "Sorry, SAUL.$",
    )),
    "Route109_Text_MelPostBattle": (("angry with me",), (
        "MEL: SAUL. Are you cross\\n",
        "with me?\\p",
        "Don't be cross with me.$",
    )),
    "Route109_Text_MelNotEnoughPokemon": (("deeply and truly", "battle together"), (
        "MEL: Two of us, remember.\\p",
        "Come back with two.$",
    )),
    "Route109_Text_ChandlerIntro": (("Tadaah", "round"), (
        "CICERO: Look! Look at it!\\n",
        "It's completely round!$",
    )),
    "Route109_Text_ChandlerDefeated": (("Too bad",), (
        "CICERO: Oh! Oh no!$",
    )),
    "Route109_Text_ChandlerPostBattle": (("showed you my round",), (
        "CICERO: And I showed you\\n",
        "the ring and everything.$",
    )),
    "Route109_Text_HaileyIntro": (("can't swim", "pretending"), (
        "FABIANA: I can't swim, so\\n",
        "I'm pretending to.\\p",
        "Nobody's noticed yet.$",
    )),
    "Route109_Text_HaileyDefeated": (("didn't think we could win",), (
        "FABIANA: I knew it. I knew\\n",
        "we wouldn't.$",
    )),
    "Route109_Text_HaileyPostBattle": (("learn how to swim",), (
        "FABIANA: Once I learn to\\n",
        "swim properly, we'll both\\l",
        "be better. I'm sure of it.$",
    )),
    "Route109_Text_ElijahIntro": (("macho", "perfect match"), (
        "GETULIO: A man like me\\n",
        "needs a partner with some\\l",
        "weight behind it.$",
    )),
    "Route109_Text_ElijahDefeated": (("cool even in defeat",), (
        "GETULIO: Still handsome,\\n",
        "though. Yes?$",
    )),
    "Route109_Text_ElijahPostBattle": (("a port", "perfect setting"), (
        "GETULIO: A man like me\\n",
        "belongs in a harbour.\\p",
        "I'll walk up to PORTO DO\\n",
        "SAL and be admired there.$",
    )),

    # -- Route 116, the climb toward the tunnel -----------------------------
    "Route116_Text_ClarkIntro": (("tunnel", "over the top"), (
        "DAVI: If the tunnel stays\\n",
        "shut, I'll go over the top.$",
    )),
    "Route116_Text_ClarkDefeat": (("Losing made me tired",), (
        "DAVI: Gasp... losing is\\n",
        "harder work than climbing.$",
    )),
    "Route116_Text_ClarkPostBattle": (("mountains are roads",), (
        "DAVI: No tunnel, no problem.\\p",
        "To someone who walks, a\\n",
        "mountain is just a road.$",
    )),
    "Route116_Text_JoeyIntro": (("rule", "Check them out"), (
        "LUCIANO: Mine are the best\\n",
        "on this hill. Look!$",
    )),
    "Route116_Text_JoeyDefeat": (("scrape", "bandage"), (
        "LUCIANO: Ow! Scraped it!\\n",
        "That's a bandage for sure!$",
    )),
    "Route116_Text_JoeyPostBattle": (("Bandages", "toughness"), (
        "LUCIANO: Every bandage is\\n",
        "proof of something.\\p",
        "I've got another one now.$",
    )),
    "Route116_Text_JoseIntro": (("BUG POKéMON are tough",), (
        "MARCELO: The small ones are\\n",
        "tougher than they look.\\p",
        "Let's go.$",
    )),
    "Route116_Text_JoseDefeat": (("thought I had you",), (
        "MARCELO: I had you! I was\\n",
        "sure I had you!$",
    )),
    "Route116_Text_JosePostBattle": (("evolve quickly",), (
        "MARCELO: The small ones\\n",
        "grow up fast.\\p",
        "Blink and they've changed.$",
    )),
    "Route116_Text_JaniceIntro": (("how strong", "adorable"), (
        "IOLANDA: Mine is sweet AND\\n",
        "strong. Let me show you\\l",
        "the second part.$",
    )),
    "Route116_Text_JaniceDefeat": (("notch above me",), (
        "IOLANDA: You're a step\\n",
        "above me.$",
    )),
    "Route116_Text_JanicePostBattle": (("cuteness and", "ideal"), (
        "IOLANDA: Sweet and strong\\n",
        "at once.\\p",
        "That's what I'm after.$",
    )),
    "Route116_Text_JerryIntro": (("TRAINER'S SCHOOL", "test things out"), (
        "LUCAS: They teach us plenty\\n",
        "at the TRAINER'S SCHOOL.\\p",
        "I want to try it on someone\\n",
        "who isn't a classmate.$",
    )),
    "Route116_Text_JerryDefeat": (("slacked off",), (
        "LUCAS: I didn't pay\\n",
        "attention. That's why.$",
    )),
    "Route116_Text_JerryPostBattle": (("redo some courses", "DALVA"), (
        "LUCAS: I'm retaking half of\\n",
        "those classes.\\p",
        "DALVA is going to have\\n",
        "something to say.$",
    )),
    "Route116_Text_JerryRegister1": (("POKéNAV can register", "just try it"), (
        "LUCAS: School says a\\n",
        "POKéNAV can register\\l",
        "TRAINERS.\\p",
        "I don't really follow it.\\n",
        "Can I just try?$",
    )),
    "Route116_Text_JerryRegister2": (("POKéNAV can register", "just try it"), (
        "LUCAS: School says a\\n",
        "POKéNAV can register\\l",
        "TRAINERS.\\p",
        "I don't really follow it.\\n",
        "Can I just try?$",
    )),
    "Route116_Text_JerryRematchIntro": (("studying seriously",), (
        "LUCAS: I've been paying\\n",
        "attention this term.\\p",
        "It won't go like last time.$",
    )),
    "Route116_Text_JerryRematchDefeat": (("studied diligently",), (
        "LUCAS: But I studied.\\n",
        "I actually studied.$",
    )),
    "Route116_Text_JerryPostRematch": (("redo some courses", "DALVA"), (
        "LUCAS: Back to those\\n",
        "classes again.\\p",
        "DALVA will hear about this.$",
    )),
    "Route116_Text_KarenIntro": (("study at school", "way home"), (
        "JULIANA: I study at school\\n",
        "and on the walk home.$",
    )),
    "Route116_Text_KarenDefeat": (("in shock",), (
        "JULIANA: I lost? I lost.$",
    )),
    "Route116_Text_KarenPostBattle": (("elegant", "DALVA"), (
        "JULIANA: I'll never carry\\n",
        "myself like DALVA at this\\l",
        "rate.$",
    )),
    "Route116_Text_KarenRegister1": (("POKéNAV", "register me"), (
        "JULIANA: Oh, a POKéNAV!\\n",
        "I've got one too.\\p",
        "Register me, please!$",
    )),
    "Route116_Text_KarenRegister2": (("POKéNAV", "register me"), (
        "JULIANA: Oh, a POKéNAV!\\n",
        "I've got one too.\\p",
        "Register me, please!$",
    )),
    "Route116_Text_KarenRematchIntro": (("studied a whole lot", "achievements"), (
        "JULIANA: I've studied since\\n",
        "we last met.\\p",
        "Come and see.$",
    )),
    "Route116_Text_KarenRematchDefeat": (("lost again",), (
        "JULIANA: Beaten twice.\\n",
        "I'm stunned.$",
    )),
    "Route116_Text_KarenPostRematch": (("beaten DALVA", "Not yet"), (
        "JULIANA: You've beaten\\n",
        "DALVA?\\p",
        "Then I'm not beating you.\\n",
        "Not this year.$",
    )),
    "Route116_Text_SarahIntro": (("never once been",), (
        "ROSELI: I have never been\\n",
        "bested at anything.\\p",
        "Not once. Ever.$",
    )),
    "Route116_Text_SarahDefeat": (("new experience",), (
        "ROSELI: Oh, my goodness.\\p",
        "This is entirely new.$",
    )),
    "Route116_Text_SarahPostBattle": (("life of luxury", "no meaning"), (
        "ROSELI: I can have anything\\n",
        "I want brought to me.\\p",
        "None of that reaches in\\n",
        "here. Not one bit of it.$",
    )),
    "Route116_Text_DawsonIntro": (("gorgeous fur", "helpless"), (
        "EMILIANO: Wait until you\\n",
        "see the coat on mine.\\p",
        "You'll lose your footing.$",
    )),
    "Route116_Text_DawsonDefeat": (("say it isn't so",), (
        "EMILIANO: Oh, no. No, no.$",
    )),
    "Route116_Text_DawsonPostBattle": (("mussed up", "stylist"), (
        "EMILIANO: Look at the state\\n",
        "of that coat now.\\p",
        "Mine as well. Both of us\\n",
        "ruined in one afternoon.$",
    )),
    "Route116_Text_DevanIntro": (("rock you",), (
        "EUGENIO: We'll take you\\n",
        "apart. Loudly.$",
    )),
    "Route116_Text_DevanDefeat": (("No contest",), (
        "EUGENIO: Aiyiyi. That was\\n",
        "no contest at all.$",
    )),
    "Route116_Text_DevanPostBattle": (("different POKéMON",), (
        "EUGENIO: I've been bringing\\n",
        "the same sort every time.\\p",
        "That's the problem, isn't\\n",
        "it.$",
    )),
    "Route116_Text_JohnsonIntro": (("dead end", "bored"), (
        "LUIS: This path stops here.\\p",
        "I'm bored. Battle me?$",
    )),
    "Route116_Text_JohnsonDefeat": (("fun even though I lost",), (
        "LUIS: Lost, and enjoyed it.$",
    )),
    "Route116_Text_JohnsonPostBattle": (("keep", "company"), (
        "LUIS: Stay up here a while?\\p",
        "It's a long walk back down\\n",
        "on your own.$",
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
        masked = masked[:start] + '\t.string "<ARAUNA_BEACH_PASS_EN>"\n\n' + masked[end:]
    return masked


def validate_rendered(source: str, rendered: str) -> None:
    if mask(source) != mask(rendered):
        raise ValueError("non-dialogue structure changed while rendering")

    forbidden = ("chiseled abs", "sculpted abs", "private world of two",
                 "call my stylist", "as macho as me", "life of luxury")
    for label in TARGETS:
        body = block_pattern(label).search(rendered).group("body")
        for token in forbidden:
            if token in body:
                raise ValueError(f"{label}: vanilla voice survived: {token}")

    # The school thread runs through Route 116 and has to keep pointing at the
    # leader whose badge the player is there for.
    school = "".join("".join(payloads) for label, (_, payloads) in TARGETS.items()
                     if label.startswith("Route116"))
    if school.count("DALVA") < 3:
        raise ValueError("Route 116 lost the thread back to DALVA")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Render the Route 109 and Route 116 trainers in English.")
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
    print(f"Beach and pass trainers English renderer OK: {len(TARGETS)} blocks "
          f"across Routes 109 and 116.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
