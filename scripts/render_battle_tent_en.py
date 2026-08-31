#!/usr/bin/env python3
"""The three BATTLE TENTs, which are the frontier at one-third scale.

CAMPO DAS CINZAS runs the Set KO Tourney, the same as the BATTLE ARENA.
VALE DO SILENCIO forbids the trainer to give orders, the same as the BATTLE
PALACE. PORTO DO SAL rents you everything and lets you swap after a win, the
same as the BATTLE FACTORY. Three wins instead of seven, a prize instead of
Battle Points, and otherwise the same games.

Which means the tents are where a player learns those rules, months before
reaching the building that uses them -- and a player who learns a rule in one
wording and meets it later in another has been taught it twice and trusts
neither. So the sentences that state a shared rule are the sentences the
matching lobby uses, and the renderer imports those lobbies and checks it:
if the BATTLE PALACE is ever reworded, this file has to move with it or the
check fails.

What is not shared is the scale, and that is where the tents must be exact.
Three TRAINERS, not seven. A prize, not Battle Points. Level 30 rentals at
PORTO DO SAL, and opponents matched to your own levels but never below 30.
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

TENT = ROOT / "data" / "text" / "battle_tent.inc"

BOX = TextBox({"{PLAYER}": 7, "{STR_VAR_1}": 14}, width=34)

WHOLE = ("BATTLE TENT", "CAMPO DAS CINZAS", "VALE DO SILENCIO", "PORTO DO SAL",
         "Set KO Tourney", "Battle Swap", "SINGLE BATTLE", "Open Level",
         "Level 50", "Level 100", "Level 30")

# Sentences a tent shares word for word with the facility it previews.
SHARED_WITH_PALACE = (
    "A TRAINER here may switch a POKéMON in or out. A TRAINER may do "
    "nothing else.",
    "Your POKéMON choose their own moves, according to their nature.",
    "You are to trust them and to watch.",
)
SHARED_WITH_FACTORY = (
    "You are loaned three of them for the event.",
    "Win, and you may take one POKéMON off the TRAINER you beat, in "
    "exchange for one of yours.",
)
SHARED_WITH_ARENA = (
    "You enter with three POKéMON, in the order you want them to appear.",
    "They come out one at a time, in that order, and a POKéMON that has "
    "come out stays out until its battle is decided.",
    "A battle lasts three turns. If nothing is settled by then, the "
    "REFEREE decides it.",
)

TARGETS: dict[str, tuple[str, ...]] = {
    # -- CAMPO DAS CINZAS: the arena's game -----------------------------------
    "FallarborTown_BattleTentLobby_Text_WelcomeToBattleTent": (
        "I welcome you to the BATTLE TENT, CAMPO DAS CINZAS site!",
        "I am your guide to the Set KO Tourney.",
    ),
    "FallarborTown_BattleTentLobby_Text_TakeChallenge": (
        "Now -- do you wish to take the Set KO Tourney challenge?",
    ),
    "FallarborTown_BattleTentLobby_Text_AwaitAnotherChallenge": (
        "We shall await your challenge on another occasion.",
    ),
    "FallarborTown_BattleTentLobby_Text_AwaitAnotherChallenge2": (
        "We shall await your challenge on another occasion.",
    ),
    "FallarborTown_BattleTentLobby_Text_ExplainFallarborTent": (
        "The CAMPO DAS CINZAS BATTLE TENT runs the Set KO Tourney.",
    ) + SHARED_WITH_ARENA + (
        "If you must stop part way, save the game. If you do not save, you "
        "cannot come back to the challenge.",
        "And if you take three TRAINERS one after another, we shall present "
        "you with a fine prize.",
    ),
    "FallarborTown_BattleTentLobby_Text_SaveBeforeChallenge": (
        "Before I show you in, the game must be saved. Is that acceptable?",
    ),
    "FallarborTown_BattleTentLobby_Text_WhichLevelMode": (
        "We offer two levels: Level 50 and Open Level.",
        "Which will you have?",
    ),
    "FallarborTown_BattleTentLobby_Text_SelectThreeMons": (
        "Very well. Select your three POKéMON, if you please.",
    ),
    "FallarborTown_BattleTentLobby_Text_NotEnoughValidMonsLv50": (
        "My dear challenger.",
        "You do not have the three POKéMON entry requires.",
        "No two of them may hold the same kind of item.",
        "EGGS{STR_VAR_1} ineligible.",
        "Do return when you are ready.",
    ),
    "FallarborTown_BattleTentLobby_Text_NotEnoughValidMonsLvOpen": (
        "My dear challenger.",
        "You do not have the three POKéMON entry requires.",
        "They must be three different kinds, and no two may hold the same "
        "kind of item.",
        "EGGS{STR_VAR_1} ineligible.",
        "Do return when you are ready.",
    ),
    "FallarborTown_BattleTentLobby_Text_GuideYouToBattleTent": (
        "I shall show you to the BATTLE TENT.",
    ),
    "FallarborTown_BattleTentLobby_Text_DidntSaveBeforeQuitting": (
        "My dear challenger.",
        "You did not save the game before shutting down.",
        "I am afraid that disqualifies the challenge you were on.",
        "You may of course begin a fresh one.",
    ),
    "FallarborTown_BattleTentLobby_Text_BeatThreeTrainers": (
        "Three TRAINERS, one after another.|How splendid.",
    ),
    "FallarborTown_BattleTentLobby_Text_WaitWhileSaveGame": (
        "Please wait while I save the game.",
    ),
    "FallarborTown_BattleTentLobby_Text_PresentYouWithPrize": (
        "In recognition of three straight wins, we present you with this.",
    ),
    "FallarborTown_BattleTentLobby_Text_ReceivedPrize": (
        "{PLAYER} received the prize {STR_VAR_1}.",
    ),
    "FallarborTown_BattleTentLobby_Text_BagFullReturnForPrize": (
        "Oh?|Your BAG appears to be full.",
        "Clear a little space and come back for it.",
    ),
    "FallarborTown_BattleTentLobby_Text_ThankYouWaitWhileSaving": (
        "Thank you for taking part.",
        "Please wait while I save the game.",
    ),
    "FallarborTown_BattleTentLobby_Text_LookingForwardToArrival": (
        "We have been expecting you.",
        "Before I show you in, I must save the game. One moment.",
    ),

    # -- VALE DO SILENCIO: the palace's game ----------------------------------
    "VerdanturfTown_BattleTentLobby_Text_WelcomeToBattleTent": (
        "I welcome you to the BATTLE TENT, VALE DO SILENCIO site.",
        "Here it is a TRAINER's trust that is put to the question.",
    ),
    "VerdanturfTown_BattleTentLobby_Text_TakeChallenge": (
        "Do you wish to take the VALE DO SILENCIO BATTLE TENT challenge?",
    ),
    "VerdanturfTown_BattleTentLobby_Text_ExplainVerdanturfTent": (
        "The VALE DO SILENCIO BATTLE TENT has one rule, and it governs "
        "everything.",
    ) + SHARED_WITH_PALACE + (
        "Beat three TRAINERS one after another and we shall present you with "
        "a prize.",
        "If you must stop part way, you must save the game. If you do not "
        "save, the challenge is forfeit.",
    ),
    "VerdanturfTown_BattleTentLobby_Text_ReturnFortified": (
        "Return when your heart and your POKéMON are ready.",
    ),
    "VerdanturfTown_BattleTentLobby_Text_WhichLevelMode": (
        "There are two levels: Level 50 and Open Level.",
        "Which will you take?",
    ),
    "VerdanturfTown_BattleTentLobby_Text_NotEnoughValidMonsLv50": (
        "Sigh...",
        "You do not have the three POKéMON the challenge requires.",
        "They must be three different kinds, and no two may hold the same "
        "kind of item.",
        "EGGS{STR_VAR_1} ineligible.",
        "Come back when you are prepared.",
    ),
    "VerdanturfTown_BattleTentLobby_Text_NotEnoughValidMonsLvOpen": (
        "Sigh...",
        "You do not have the three POKéMON the challenge requires.",
        "They must be three different kinds, and no two may hold the same "
        "kind of item.",
        "EGGS{STR_VAR_1} ineligible.",
        "Come back when you are prepared.",
    ),
    "VerdanturfTown_BattleTentLobby_Text_SelectThreeMons": (
        "Good. Now select your three POKéMON.",
    ),
    "VerdanturfTown_BattleTentLobby_Text_SaveBeforeChallenge": (
        "I must save before I show you to the BATTLE TENT. Is that "
        "acceptable?",
    ),
    "VerdanturfTown_BattleTentLobby_Text_NowFollowMe": (
        "Good.|Follow me.",
    ),
    "VerdanturfTown_BattleTentLobby_Text_ResultsWillBeRecorded": (
        "I count it a privilege to have watched your POKéMON.",
        "The result will be recorded. I must ask you to wait a moment.",
    ),
    "VerdanturfTown_BattleTentLobby_Text_AchievedThreeWinStreak": (
        "Three in a row...",
        "What binds you to your POKéMON is evidently firm, and evidently "
        "true.",
    ),
    "VerdanturfTown_BattleTentLobby_Text_FeatWillBeRecorded": (
        "It will be recorded. I must ask you to wait a moment.",
    ),
    "VerdanturfTown_BattleTentLobby_Text_PresentYouWithPrize": (
        "For three wins in a row, we present you with this.",
    ),
    "VerdanturfTown_BattleTentLobby_Text_RulesAreListed": (
        "The VALE DO SILENCIO BATTLE TENT rules are set out here.",
    ),
    "VerdanturfTown_BattleTentLobby_Text_RulesAreListed2": (
        "The VALE DO SILENCIO BATTLE TENT rules are set out here.",
    ),
    "VerdanturfTown_BattleTentLobby_Text_ReadWhichHeading": (
        "Which heading will you read?",
    ),
    "VerdanturfTown_BattleTentLobby_Text_ExplainBasicRules": (
        "Here, a POKéMON decides for itself. You may switch it out and "
        "nothing more.",
        "What it decides depends on its nature -- and a POKéMON raised among "
        "people has more nature in it than a wild one, not less.",
    ),
    "VerdanturfTown_BattleTentLobby_Text_ExplainUnderpoweredRules": (
        "This is the part that decides a challenge.",
        "A POKéMON is poor at any move its nature dislikes, and here nobody "
        "is telling it otherwise.",
        "Bring one whose moves it has no wish to use, and it will not come "
        "near what it is capable of.",
    ),
    "VerdanturfTown_BattleTentLobby_Text_ExplainNatureRules": (
        "One nature would rather attack, whatever the situation.",
        "Another would rather keep itself from harm.",
        "Another enjoys confusing and vexing a foe.",
        "Each nature has moves it is happy with and moves it is not.",
    ),
    "VerdanturfTown_BattleTentLobby_Text_ExplainMoveRules": (
        "A POKéMON weighs its moves in three kinds.",
        "Those that damage a foe directly.",
        "Those that guard, or prepare, or restore HP.",
        "And the odder sort, that leave a foe poisoned or paralysed or "
        "otherwise the worse for it.",
    ),
    "VerdanturfTown_BattleTentLobby_Text_ExplainWhenInDangerRules": (
        "Some natures change their minds when things go badly, and reach for "
        "moves they would not normally touch.",
        "If one of yours starts behaving unlike itself in a tight place, "
        "watch it closely.",
    ),

    # -- PORTO DO SAL: the factory's game -------------------------------------
    "SlateportCity_BattleTentLobby_Text_WelcomeToBattleTent": (
        "Welcome to the BATTLE TENT, PORTO DO SAL site!",
        "I am your guide to the Battle Swap Tournament.",
    ),
    "SlateportCity_BattleTentLobby_Text_TakeChallenge": (
        "Would you like to take the Battle Swap challenge?",
    ),
    "SlateportCity_BattleTentLobby_Text_ExplainSlateportTent": (
        "The PORTO DO SAL BATTLE TENT runs Battle Swap events, fought "
        "entirely with rented POKéMON.",
    ) + SHARED_WITH_FACTORY + (
        "With those three you fight a SINGLE BATTLE.",
        "Battle, swap, battle again. Three wins in a row and you earn a fine "
        "prize.",
        "If you must stop part way, save the game. If you do not save, the "
        "challenge is forfeit.",
    ),
    "SlateportCity_BattleTentLobby_Text_LookForwardToNextVisit": (
        "We shall look forward to your next visit.",
    ),
    "SlateportCity_BattleTentLobby_Text_WhichLevelMode": (
        "Which level will you take?|Level 50, or Level 100?",
    ),
    "SlateportCity_BattleTentLobby_Text_SaveBeforeChallenge": (
        "Before you begin, I must save the data. Is that all right?",
    ),
    "SlateportCity_BattleTentLobby_Text_HoldMonsForSafekeeping": (
        "Then I'll keep your own POKéMON safe while you compete.",
    ),
    "SlateportCity_BattleTentLobby_Text_StepThisWay": (
        "Step this way, please.",
    ),
    "SlateportCity_BattleTentLobby_Text_ReturnRentalMonsSaveResults": (
        "Thank you for taking part.",
        "I'll give you your own POKéMON back and take our rentals.",
        "I must save the results as well. One moment.",
    ),
    "SlateportCity_BattleTentLobby_Text_ReturnMonsExchangeRentals": (
        "I'll give you your own POKéMON back and take our rentals.",
    ),
    "SlateportCity_BattleTentLobby_Text_WonThreeMatchesReturnMons": (
        "Congratulations! Three straight matches!",
        "I'll give you your own POKéMON back and take our rentals.",
        "I must save the results as well. One moment.",
    ),
    "SlateportCity_BattleTentLobby_Text_AwardYouThisPrize": (
        "In recognition of three wins in a row, we award you this.",
    ),
    "SlateportCity_BattleTentLobby_Text_NoRoomInBagMakeRoom": (
        "Oh?|You seem to have no room for this.",
        "Make a little space in your BAG and tell me.",
    ),
    "SlateportCity_BattleTentLobby_Text_BeenWaitingForYou": (
        "We've been waiting for you!",
        "Before we take up where you left off, I must save the game.",
    ),
    "SlateportCity_BattleTentLobby_Text_DidntSaveBeforeQuitting": (
        "I'm sorry to say it, but you didn't save before you stopped playing "
        "last time.",
        "That forfeits the challenge you were on.",
    ),
    "SlateportCity_BattleTentLobby_Text_ReturnPersonalMons": (
        "We'll give you your own POKéMON back.",
    ),
    "SlateportCity_BattleTentLobby_Text_ReceivedPrize": (
        "{PLAYER} received the prize {STR_VAR_1}.",
    ),
    "SlateportCity_BattleTentLobby_Text_RulesAreListed": (
        "The Battle Swap rules are set out here.",
    ),
    "SlateportCity_BattleTentLobby_Text_ReadWhichHeading": (
        "Which heading will you read?",
    ),
    "SlateportCity_BattleTentLobby_Text_ExplainBasicRules": (
        "In a Battle Swap event you use three POKéMON and no more.",
        "Rented or swapped, you may never hold two of the same kind at once.",
    ),
    "SlateportCity_BattleTentLobby_Text_ExplainSwapPartnerRules": (
        "You may only swap with the TRAINER you have just beaten, and only "
        "for a POKéMON that TRAINER actually used.",
    ),
    "SlateportCity_BattleTentLobby_Text_ExplainSwapNumberRules": (
        "One swap after every win.",
        "There is no swap after the third TRAINER -- that one is the last.",
    ),
    "SlateportCity_BattleTentLobby_Text_ExplainSwapNotes": (
        "Two things to know before you swap.",
        "You cannot see the stats of what you are taking. You are choosing "
        "on what you saw it do in the battle.",
        "And your three stay in the order you rented them. A swap changes "
        "the POKéMON, never the position.",
    ),
    "SlateportCity_BattleTentLobby_Text_ExplainMonRules": (
        "Every POKéMON at the PORTO DO SAL BATTLE TENT is a rental.",
        "And every rental is kept at Level 30.",
    ),

    # -- shared by all three ---------------------------------------------------
    "BattleTentLobby_Text_ExplainLevelRules": (
        "At a BATTLE TENT, the TRAINERS you face are set to match the levels "
        "of your own POKéMON.",
        "Though none of them will bring anything below Level 30.",
    ),
}


def block_pattern(label: str) -> re.Pattern[str]:
    return re.compile(
        rf"(?ms)^{re.escape(label)}::?\n(?P<body>.*?)"
        rf"(?=^[A-Za-z0-9_]+(?:::|:)(?:\n|$)|\Z)"
    )


def payloads() -> dict[str, tuple[str, ...]]:
    composed = {}
    for label, paragraphs in TARGETS.items():
        glued_paragraphs = []
        for paragraph in paragraphs:
            for name in WHOLE:
                paragraph = paragraph.replace(name, glued(name))
            glued_paragraphs.append(paragraph)
        composed[label] = BOX.compose(tuple(glued_paragraphs))
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
        masked = masked[:start] + '\t.string "<ARAUNA_BATTLE_TENT_EN>"\n\n' + masked[end:]
    return masked


def validate_slots(source: str) -> None:
    composed = payloads()
    for label in TARGETS:
        available = set(re.findall(r"\{[A-Za-z_0-9]+\}",
                                   block_pattern(label).search(source).group("body")))
        used = set(re.findall(r"\{[A-Za-z_0-9]+\}", "".join(composed[label])))
        if used - available:
            raise ValueError(
                f"{label}: uses {sorted(used - available)}, which the engine "
                f"does not fill here; the source uses {sorted(available)}")


def lobby(name: str) -> str:
    """Everything the matching frontier lobby says, flattened."""
    spec = importlib.util.spec_from_file_location(
        name, ROOT / "scripts" / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    joined = "".join("".join(lines) for lines in module.payloads().values())
    return re.sub(r"\\[npl]", " ", joined)


def validate_rendered(source: str, rendered: str) -> None:
    if mask(source) != mask(rendered):
        raise ValueError("non-dialogue structure changed while rendering")

    composed = payloads()

    def flat(label: str) -> str:
        return re.sub(r"\\[npl]", " ", "".join(composed[label]))

    # A tent is where the rule is learned; the facility is where it is met.
    # If the two word it differently, the player has been taught it twice.
    for name, shared in (
            ("render_battle_palace_lobby_en", SHARED_WITH_PALACE),
            ("render_battle_factory_lobby_en", SHARED_WITH_FACTORY),
            ("render_battle_arena_lobby_en", SHARED_WITH_ARENA)):
        said = lobby(name)
        for sentence in shared:
            if sentence not in said:
                raise ValueError(
                    f"{name} no longer contains a sentence this tent shares "
                    f"with it: {sentence!r}")

    # The scale is the only thing a tent may differ on, so it has to be right.
    for label in ("FallarborTown_BattleTentLobby_Text_ExplainFallarborTent",
                  "VerdanturfTown_BattleTentLobby_Text_ExplainVerdanturfTent",
                  "SlateportCity_BattleTentLobby_Text_ExplainSlateportTent"):
        text = flat(label)
        if "three" not in text:
            raise ValueError(f"{label}: no longer says how many wins it takes")
        if "seven" in text:
            raise ValueError(
                f"{label}: says seven, which is the frontier's number and not "
                f"a tent's")
        if "Battle Point" in text:
            raise ValueError(
                f"{label}: offers Battle Points, which the tents do not give")

    # PORTO DO SAL rents everything at one level, and that level decides
    # whether a player's own team matters at all.
    rentals = flat("SlateportCity_BattleTentLobby_Text_ExplainMonRules")
    if "rental" not in rentals or "Level 30" not in rentals:
        raise ValueError(
            "ExplainMonRules: no longer says the rentals are all Level 30")
    if "Level 30" not in flat("BattleTentLobby_Text_ExplainLevelRules"):
        raise ValueError(
            "ExplainLevelRules: no longer states the floor on opponent levels")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Render the three BATTLE TENT lobbies in English.")
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--in-place", action="store_true")
    args = parser.parse_args()
    if args.check and args.in_place:
        parser.error("use either --check or --in-place")

    source = TENT.read_text(encoding="utf-8")
    validate_slots(source)
    rendered = render(source)
    validate_rendered(source, rendered)

    if args.in_place:
        TENT.write_text(rendered, encoding="utf-8")
    print(f"Battle Tent English renderer OK: {len(TARGETS)} blocks.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
