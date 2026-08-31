#!/usr/bin/env python3
"""The trainers of Routes 102, 103 and 104, in Arauna's voice.

These are the first hundred text blocks a player reads after leaving Vila
Amanhecer, and they were still Emerald's: a boy shouting that eye contact is a
rule, a rich kid explaining that he has a lot of money. The names on the
nameplates are Brazilian now; the voices were not.

Every trainer keeps the hook that made them different -- the fisherman is still
furious at his line, the guitarist still plays to nobody, the twins still refuse
to fight you one-on-two -- because that variety is what makes a route readable.
What changes is how they talk: shorter, plainer, of this place. Nothing here
invents story. These people are strangers on a road.

No payload names a species. The dex is generated, and a line that names a
creature would be wrong the next time it is regenerated.
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

# label: ((markers that must be in the vanilla body), (the new lines))
TARGETS: dict[str, tuple[tuple[str, ...], tuple[str, ...]]] = {
    # -- Route 102, the pampa road out of Vila da Passagem ------------------
    "Route102_Text_CalvinIntro": (("official POKéMON TRAINER", "challenge"), (
        "CAIO: You've got POKéMON.\\n",
        "That makes this fair.\\p",
        "Let's see what you learned!$",
    )),
    "Route102_Text_CalvinDefeated": (("Arrgh, I lost", "trained mine more"), (
        "CAIO: I lost.\\p",
        "I'll train harder before\\n",
        "the next one.$",
    )),
    "Route102_Text_CalvinPostBattle": (("If you're strong", "told me before"), (
        "CAIO: You could have warned\\n",
        "me you were good.\\p",
        "...Fine. Good match.$",
    )),
    "Route102_Text_CalvinRegister": (("working hard", "POKéNAV"), (
        "CAIO: I've been at it since\\n",
        "the day we met.\\p",
        "Put me in your POKéNAV.\\n",
        "I want another go.$",
    )),
    "Route102_Text_CalvinRegisterShort": (("battle you again", "POKéNAV"), (
        "CAIO: Put me in your POKéNAV.\\n",
        "I want another go.$",
    )),
    "Route102_Text_CalvinRematchIntro": (("desperately", "challenge"), (
        "CAIO: I trained every day\\n",
        "since you beat me.\\p",
        "Let's go again!$",
    )),
    "Route102_Text_CalvinRematchDefeated": (("training method",), (
        "CAIO: Still not enough.\\p",
        "What am I doing wrong?$",
    )),
    "Route102_Text_CalvinRematchPostBattle": (("get stronger",), (
        "CAIO: You get stronger,\\n",
        "I get stronger.\\p",
        "That's the deal.$",
    )),
    "Route102_Text_AllenIntro": (("just become a TRAINER", "beginners"), (
        "AIRTON: You started recently\\n",
        "too, didn't you?\\p",
        "So did I. Come on.$",
    )),
    "Route102_Text_AllenDefeated": (("thought", "beat you"), (
        "AIRTON: I really thought\\n",
        "I had that one.$",
    )),
    "Route102_Text_AllenPostBattle": (("haven't won once",), (
        "AIRTON: Still no wins.\\p",
        "One of these days.$",
    )),
    "Route102_Text_RickIntro": (("Our eyes met", "BUG POKéMON"), (
        "SEVERINO: You looked at me.\\p",
        "Everything small out here\\n",
        "is mine. Watch.$",
    )),
    "Route102_Text_RickDefeated": (("Down and out",), (
        "SEVERINO: Flat on my back.$",
    )),
    "Route102_Text_RickPostBattle": (("lock eyes", "It's a rule"), (
        "SEVERINO: Out here, if you\\n",
        "meet someone's eyes, you\\l",
        "battle. Nobody wrote it down.$",
    )),
    "Route102_Text_TianaIntro": (("keep winning", "career"), (
        "VILMA: I intend to win a lot.\\p",
        "Start me off.$",
    )),
    "Route102_Text_TianaDefeated": (("furthering your career",), (
        "VILMA: I started you off\\n",
        "instead.$",
    )),
    "Route102_Text_TianaPostBattle": (("catch more POKéMON",), (
        "VILMA: A longer team, then.\\p",
        "I'll go find one.$",
    )),

    # -- Route 103, the beach and shallows above Vila Amanhecer -------------
    "Route103_Text_DaisyIntro": (("soul-soothing fragrance",), (
        "EDINA: Did the smell of the\\n",
        "herbs stop you?\\p",
        "It stops most people.$",
    )),
    "Route103_Text_DaisyDefeated": (("led astray by our aroma",), (
        "EDINA: You walked straight\\n",
        "through it.$",
    )),
    "Route103_Text_DaisyPostBattle": (("Aromatherapy", "fragrances"), (
        "EDINA: A smell can settle a\\n",
        "frightened animal faster\\l",
        "than any word will.$",
    )),
    "Route103_Text_AmyIntro": (("I'm ANE", "little sister"), (
        "ANE: I'm ANE. This is VIVI.\\p",
        "We only battle together.$",
    )),
    "Route103_Text_AmyDefeated": (("we lost",), (
        "ANE: Both of us, beaten.$",
    )),
    "Route103_Text_AmyPostBattle": (("two TRAINERS",), (
        "ANE: Two of us means twice\\n",
        "as much to keep track of.\\p",
        "You managed it.$",
    )),
    "Route103_Text_AmyNotEnoughPokemon": (("only one",), (
        "ANE: You've brought one.\\p",
        "There are two of us.\\n",
        "Come back even.$",
    )),
    "Route103_Text_LivIntro": (("battle together as one",), (
        "VIVI: One team. Always.$",
    )),
    "Route103_Text_LivDefeated": (("big sister",), (
        "VIVI: Sorry, big sister...$",
    )),
    "Route103_Text_LivPostBattle": (("perfectly together",), (
        "VIVI: We fit together so\\n",
        "well.\\p",
        "And we still lost.$",
    )),
    "Route103_Text_AmyLivRegister": (("we're a lot better",), (
        "VIVI: We're better than\\n",
        "that. You'll see.$",
    )),
    "Route103_Text_LivNotEnoughPokemon": (("two POKéMON", "not fair"), (
        "VIVI: Two of us, one of you.\\p",
        "That isn't a battle.$",
    )),
    "Route103_Text_AmyRematchIntro": (("I'm ANE", "little sister"), (
        "ANE: Us again. Still two.$",
    )),
    "Route103_Text_AmyRematchDefeated": (("couldn't win again",), (
        "ANE: Twice now.$",
    )),
    "Route103_Text_AmyRematchPostBattle": (("two TRAINERS",), (
        "ANE: You keep track of both\\n",
        "of us at once.\\p",
        "That's the hard part.$",
    )),
    "Route103_Text_AmyRematchNotEnoughPokemon": (("only one",), (
        "ANE: One again? No.\\n",
        "Come back even.$",
    )),
    "Route103_Text_LivRematchIntro": (("battle together as one",), (
        "VIVI: One team. Still.$",
    )),
    "Route103_Text_LivRematchDefeated": (("we lost again",), (
        "VIVI: Again, big sister...$",
    )),
    "Route103_Text_LivRematchPostBattle": (("why did we lose",), (
        "VIVI: We fit together.\\p",
        "So why does that keep\\n",
        "not being enough?$",
    )),
    "Route103_Text_LivRematchNotEnoughPokemon": (("two POKéMON", "not fair"), (
        "VIVI: Two of us. One of you.\\p",
        "You know the answer.$",
    )),
    "Route103_Text_AndrewIntro": (("fishing line", "Battle me"), (
        "ALCIDES: My line is a knot.\\p",
        "I have been here since\\n",
        "sunrise. Fight me.$",
    )),
    "Route103_Text_AndrewDefeated": (("more annoyed",), (
        "ALCIDES: Now the knot AND\\n",
        "the loss.$",
    )),
    "Route103_Text_AndrewPostBattle": (("boiling mad",), (
        "ALCIDES: Grrr. The line is\\n",
        "still a knot.$",
    )),
    "Route103_Text_MiguelIntro": (("delightfully adorable", "shy"), (
        "PAULO: Mine is the sweetest\\n",
        "thing on this beach.\\p",
        "Look. Just look.$",
    )),
    "Route103_Text_MiguelDefeated": (("darling POKéMON",), (
        "PAULO: Oh, my sweet thing!$",
    )),
    "Route103_Text_MiguelPostBattle": (("even when it's fainted",), (
        "PAULO: Even worn out, it's\\n",
        "the sweetest thing here.$",
    )),
    "Route103_Text_MiguelRegister": (("come out and look",), (
        "PAULO: Come see it again.\\p",
        "You'll agree eventually.$",
    )),
    "Route103_Text_MiguelRematchIntro": (("more darling",), (
        "PAULO: It has got sweeter.\\p",
        "I didn't think that was\\n",
        "possible either.$",
    )),
    "Route103_Text_MiguelRematchDefeated": (("darling POKéMON",), (
        "PAULO: My sweet thing...$",
    )),
    "Route103_Text_MiguelRematchPostBattle": (("the more adorable",), (
        "PAULO: The longer we're\\n",
        "together, the sweeter it\\l",
        "gets. That's how it works.$",
    )),
    "Route103_Text_PeteIntro": (("distance", "swim it"), (
        "ROLANDO: That's nothing.\\p",
        "You could swim that.$",
    )),
    "Route103_Text_PeteDefeated": (("good going",), (
        "ROLANDO: Well swum.$",
    )),
    "Route103_Text_PetePostBattle": (("SURF on it",), (
        "ROLANDO: I see it now.\\p",
        "With one you trust that\\n",
        "much, I'd cross on it too.$",
    )),
    "Route103_Text_IsabelleIntro": (("Watch where you're going", "crash"), (
        "GRAZIELA: Careful! I don't\\n",
        "steer well!$",
    )),
    "Route103_Text_IsabelleDefeated": (("Groan",), (
        "GRAZIELA: Ohhh...$",
    )),
    "Route103_Text_IsabellePostBattle": (("poor swimmer", "practicing"), (
        "GRAZIELA: I swim badly.\\p",
        "That's why I'm out here.\\n",
        "Sorry about the near miss.$",
    )),
    "Route103_Text_RhettIntro": (("space this small",), (
        "SERAFIM: How did you fit\\n",
        "in here?$",
    )),
    "Route103_Text_RhettDefeated": (("The kid can rock",), (
        "SERAFIM: Whoa. The kid can\\n",
        "hit.$",
    )),
    "Route103_Text_RhettPostBattle": (("cramped quarters",), (
        "SERAFIM: Small places suit\\n",
        "me. Less room to run.$",
    )),
    "Route103_Text_MarcosIntro": (("guitar's wailing",), (
        "OTAVIO: Did the guitar\\n",
        "bring you over?$",
    )),
    "Route103_Text_MarcosDefeated": (("one-man show",), (
        "OTAVIO: There goes the show.$",
    )),
    "Route103_Text_MarcosPostBattle": (("turn pro",), (
        "OTAVIO: I came out here\\n",
        "because nobody was around.\\p",
        "Now look at the crowd.\\p",
        "Maybe I should charge.$",
    )),

    # -- Route 104, the beach and the woods road ----------------------------
    "Route104_Text_GinaIntro": (("let's battle",), (
        "NINA: Right. Both of us,\\n",
        "both of you.$",
    )),
    "Route104_Text_GinaDefeat": (("upsets me",), (
        "NINA: I hate losing.$",
    )),
    "Route104_Text_GinaPostBattle": (("You are strong",), (
        "NINA: You're strong.\\p",
        "We're going to train.$",
    )),
    "Route104_Text_GinaNotEnoughMons": (("Only one", "lonesome"), (
        "NINA: Only one?\\p",
        "Then it would be out there\\n",
        "alone. We won't do that.$",
    )),
    "Route104_Text_MiaIntro": (("twins",), (
        "GI: We're twins. We battle\\n",
        "the way we do everything.$",
    )),
    "Route104_Text_MiaDefeat": (("both lost",), (
        "GI: Together, and beaten\\n",
        "together.$",
    )),
    "Route104_Text_MiaPostBattle": (("train our POKéMON more",), (
        "GI: We'll train until we're\\n",
        "as strong as you.$",
    )),
    "Route104_Text_MiaNotEnoughMons": (("two", "too strong"), (
        "GI: Battle us with one?\\p",
        "Bring two. We're not going\\n",
        "to go easy.$",
    )),
    "Route104_Text_IvanIntro": (("WATER POKéMON expert", "don't know me"), (
        "JUCA: I know this water\\n",
        "better than anyone.\\p",
        "You've never heard of me?$",
    )),
    "Route104_Text_IvanDefeat": (("wasn't too bad",), (
        "JUCA: I thought I was good\\n",
        "at this. Bleah.$",
    )),
    "Route104_Text_IvanPostBattle": (("too into fishing",), (
        "JUCA: I fish all day and\\n",
        "forget to train.\\p",
        "That's the whole problem.$",
    )),
    "Route104_Text_BillyIntro": (("footprints in the sand",), (
        "ARTUR: Look at the tracks\\n",
        "I'm leaving!$",
    )),
    "Route104_Text_BillyDefeat": (("sand in my runners",), (
        "ARTUR: Waah! Sand in my\\n",
        "shoes!$",
    )),
    "Route104_Text_BillyPostBattle": (("disappear quickly",), (
        "ARTUR: I want tracks all\\n",
        "along this beach.\\p",
        "The tide keeps taking them.$",
    )),
    "Route104_Text_HaleyIntro": (("Or shouldn't I", "sure, I will battle"), (
        "FATIMA: Should I?\\n",
        "Or shouldn't I?\\p",
        "...Yes. Let's battle.$",
    )),
    "Route104_Text_HaleyDefeat": (("shouldn't have battled",), (
        "FATIMA: I should have\\n",
        "picked the other one.$",
    )),
    "Route104_Text_HaleyPostBattle": (("let someone else choose",), (
        "FATIMA: When you can't\\n",
        "decide, decide anyway.\\p",
        "Let someone choose for you\\n",
        "and you'll regret it either\\l",
        "way.$",
    )),
    "Route104_Text_HaleyRegister1": (("register", "Maybe I shouldn't"), (
        "FATIMA: Should I put you in\\n",
        "my POKéNAV?\\p",
        "Maybe not... no. Yes.\\n",
        "Yes, I'm registering you.$",
    )),
    "Route104_Text_HaleyRegister2": (("register", "Maybe I shouldn't"), (
        "FATIMA: Should I put you in\\n",
        "my POKéNAV?\\p",
        "Maybe not... no. Yes.\\n",
        "Yes, I'm registering you.$",
    )),
    "Route104_Text_HaleyRematchIntro": (("battle with me",), (
        "FATIMA: Battle me. I've\\n",
        "already decided.$",
    )),
    "Route104_Text_HaleyRematchDefeat": (("thought I could win",), (
        "FATIMA: Ohh. I was sure\\n",
        "that time.$",
    )),
    "Route104_Text_HaleyPostRematch": (("accept this loss", "still upset"), (
        "FATIMA: I chose to battle,\\n",
        "so I'll take the loss.\\p",
        "I'm still furious about it.$",
    )),
    "Route104_Text_WinstonIntro": (("lot of money",), (
        "ATILIO: Certainly, I accept.\\p",
        "I can afford to lose.$",
    )),
    "Route104_Text_WinstonDefeat": (("Why couldn't I win",), (
        "ATILIO: Why didn't that\\n",
        "work?$",
    )),
    "Route104_Text_WinstonPostBattle": (("money can't buy",), (
        "ATILIO: Some things aren't\\n",
        "for sale.\\p",
        "This is one of them.$",
    )),
    "Route104_Text_WinstonRegister1": (("obtained a POKéNAV", "plenty of money"), (
        "ATILIO: Ah, a POKéNAV.\\p",
        "I'll register. It costs me\\n",
        "nothing.$",
    )),
    "Route104_Text_WinstonRegister2": (("obtained a POKéNAV", "plenty of money"), (
        "ATILIO: Ah, a POKéNAV.\\p",
        "I'll register. It costs me\\n",
        "nothing.$",
    )),
    "Route104_Text_WinstonRematchIntro": (("learned a bunch",), (
        "ATILIO: I studied after you\\n",
        "beat me.\\p",
        "Properly, this time.$",
    )),
    "Route104_Text_WinstonRematchDefeat": (("lost again",), (
        "ATILIO: Beaten twice.\\p",
        "Why?$",
    )),
    "Route104_Text_WinstonPostRematch": (("fabulously wealthy", "so deep"), (
        "ATILIO: I can buy nearly\\n",
        "anything.\\p",
        "Not this. It goes deeper\\n",
        "than I can reach.$",
    )),
    "Route104_Text_CindyIntro": (("fated to meet",), (
        "DEBORA: We were going to\\n",
        "meet sooner or later.\\p",
        "Battle me?$",
    )),
    "Route104_Text_CindyDefeat": (("Oh, my",), (
        "DEBORA: Oh, my.$",
    )),
    "Route104_Text_CindyPostBattle": (("beginning of", "meet again"), (
        "DEBORA: Every hello is the\\n",
        "front half of a goodbye.\\p",
        "See you at the next one.$",
    )),
    "Route104_Text_CindyRegister1": (("drawn together", "POKéNAV"), (
        "DEBORA: Here you are again.\\p",
        "We keep crossing paths.\\n",
        "Let's trade POKéNAV numbers.$",
    )),
    "Route104_Text_CindyRegister2": (("drawn to each other", "POKéNAV"), (
        "DEBORA: Twice is a pattern.\\p",
        "Let's trade POKéNAV numbers\\n",
        "and make it official.$",
    )),
    "Route104_Text_CindyRematchIntro": (("we meet again",), (
        "DEBORA: Here we are again.\\p",
        "One more?$",
    )),
    "Route104_Text_CindyRematchDefeat": (("best that I could",), (
        "DEBORA: Oh, my.\\p",
        "That was everything I had.$",
    )),
    "Route104_Text_CindyPostRematch": (("beginning of", "meet again"), (
        "DEBORA: Every hello is the\\n",
        "front half of a goodbye.\\p",
        "Until the next one.$",
    )),
    "Route104_Text_DarianIntro": (("fished up", "looks tough"), (
        "EDMUNDO: Look what came up\\n",
        "on my line!\\p",
        "There's something uncanny\\n",
        "about it. Look at it!$",
    )),
    "Route104_Text_DarianDefeat": (("What the",), (
        "EDMUNDO: What...$",
    )),
    "Route104_Text_DarianPostBattle": (("live up",), (
        "EDMUNDO: All that fuss on\\n",
        "the line, and then this.\\p",
        "You didn't live up to the\\n",
        "story, did you.$",
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
    """Everything that is not one of these bodies, so nothing else can move."""
    masked = text
    for label in TARGETS:
        match = block_pattern(label).search(masked)
        if not match:
            raise ValueError(f"cannot mask missing block: {label}")
        start, end = match.span("body")
        masked = masked[:start] + '\t.string "<ARAUNA_EARLY_ROUTES_EN>"\n\n' + masked[end:]
    return masked


def validate_rendered(source: str, rendered: str) -> None:
    if mask(source) != mask(rendered):
        raise ValueError("non-dialogue structure changed while rendering")

    # Voices that must be gone from the blocks this renderer owns.
    forbidden = ("It's a rule!", "furthering your career", "Aromatherapy",
                 "I have a lot of money", "fabulously wealthy",
                 "delightfully adorable", "one-man show", "big sister…")
    for label in TARGETS:
        body = block_pattern(label).search(rendered).group("body")
        for token in forbidden:
            if token in body:
                raise ValueError(f"{label}: vanilla voice survived: {token}")

    # The people are the point: every block must still name whoever speaks it,
    # or introduce them by class, so a route reads as a road with people on it.
    for label, (_, payloads) in TARGETS.items():
        joined = "".join(payloads)
        if not any(ch.isalpha() for ch in joined):
            raise ValueError(f"{label}: empty payload")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Render the Route 102/103/104 trainers in English.")
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
    print(f"Early route trainers English renderer OK: {len(TARGETS)} blocks "
          f"across Routes 102, 103 and 104.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
