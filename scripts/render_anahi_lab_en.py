#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / "data" / "maps" / "LittlerootTown_ProfessorBirchsLab" / "scripts.inc"
MAX_VISIBLE_WIDTH = 32
CONTROL_RE = re.compile(r"\\[npl]")
PLACEHOLDER_RE = re.compile(r"\{[^}]+\}")

TARGETS: dict[str, tuple[str, ...]] = {
    "LittlerootTown_ProfessorBirchsLab_Text_BirchAwayOnFieldwork": (
        "AIDE: ANAHI is in the field.\\p",
        "She rarely stays behind a desk.\\p",
        "If she found a new trail,\\n",
        "she'll follow it herself.$",
    ),
    "LittlerootTown_ProfessorBirchsLab_Text_BirchIsntOneForDeskWork": (
        "AIDE: ANAHI helped design the\\n",
        "first BOND sensors.\\p",
        "She says measuring something\\n",
        "is not the same as knowing it.$",
    ),
    "LittlerootTown_ProfessorBirchsLab_Text_BirchEnjoysRivalsHelpToo": (
        "AIDE: DESECHANTMENT can break\\n",
        "more than memory.\\p",
        "People, places and POKéMON can\\n",
        "stop recognizing each other.$",
    ),
    "LittlerootTown_ProfessorBirchsLab_Text_LikeYouToHavePokemon": (
        "ANAHI: That POKéMON chose to\\n",
        "stay beside you.\\p",
        "Don't treat that as ownership.\\p",
        "A BOND lasts while both sides\\n",
        "keep choosing it.$",
    ),
    "LittlerootTown_ProfessorBirchsLab_Text_WhyNotGiveNicknameToMon": (
        "ANAHI: A name can become memory.\\p",
        "Want to name {STR_VAR_1}?$",
    ),
    "LittlerootTown_ProfessorBirchsLab_Text_MightBeGoodIdeaToGoSeeRival": (
        "ANAHI: CIRO is on ROUTE 103.\\p",
        "HORIZON backs his fieldwork.\\p",
        "He thinks their data proves he\\n",
        "already understands the world.\\p",
        "Go meet him.$",
    ),
    "LittlerootTown_ProfessorBirchsLab_Text_GetRivalToTeachYou": (
        "ANAHI: Find CIRO on ROUTE 103.\\p",
        "Watch how your POKéMON react\\n",
        "to each other.$",
    ),
    "LittlerootTown_ProfessorBirchsLab_Text_DontBeThatWay": (
        "ANAHI: You needn't like CIRO.\\p",
        "Hear what he chose to believe\\n",
        "before choosing for yourself.$",
    ),
    "LittlerootTown_ProfessorBirchsLab_Text_BirchRivalGoneHome": (
        "ANAHI: CIRO left again.\\p",
        "Since HORIZON gave him a grant,\\n",
        "he barely stays home.$",
    ),
    "LittlerootTown_ProfessorBirchsLab_Text_HeardYouBeatRivalTakePokedex": (
        "ANAHI: CIRO told me about the\\n",
        "battle.\\p",
        "Winning matters less than this:\\n",
        "your POKéMON reacted in a way\\n",
        "my BOND sensors did not predict.\\p",
        "Take this POKéDEX. Record what\\n",
        "you find.$",
    ),
    "LittlerootTown_ProfessorBirchsLab_Text_ReceivedPokedex": (
        "{PLAYER} received the POKéDEX!$",
    ),
    "LittlerootTown_ProfessorBirchsLab_Text_ExplainPokedex": (
        "ANAHI: The POKéDEX records\\n",
        "species and encounters.\\p",
        "Record something else too:\\n",
        "memory gaps, changed behavior,\\n",
        "any sign of DESECHANTMENT.$",
    ),
    "LittlerootTown_ProfessorBirchsLab_Text_CountlessPokemonAwait": (
        "ANAHI: Don't turn this journey\\n",
        "into a list of numbers.\\p",
        "Notice who recalls and forgets,\\n",
        "and who decides that for them.$",
    ),
    "LittlerootTown_ProfessorBirchsLab_Text_MayGotPokedexTooTakeThese": (
        "CIRO: So she gave you a POKéDEX\\n",
        "too. Fine.\\p",
        "Take these POKé BALLS.\\p",
        "Let's see how long it takes you\\n",
        "to catch up.$",
    ),
    "LittlerootTown_ProfessorBirchsLab_Text_CatchCutePokemonWithPokeBalls": (
        "CIRO: I'll follow HORIZON's\\n",
        "survey points.\\p",
        "They say some POKéMON out there\\n",
        "show almost no DESECHANTMENT.$",
    ),
    "LittlerootTown_ProfessorBirchsLab_Text_OhYourBagsFull": (
        "Your BAG is full.$",
    ),
    "LittlerootTown_ProfessorBirchsLab_Text_MayWhereShouldIGoNext": (
        "CIRO: HORIZON has teams across\\n",
        "Arauna.\\p",
        "If their data is right, I'll be\\n",
        "at the next answer before you.$",
    ),
    "LittlerootTown_ProfessorBirchsLab_Text_BrendanGotPokedexTooTakeThese": (
        "CIRO: So she gave you a POKéDEX\\n",
        "too. Fine.\\p",
        "Take these POKé BALLS.\\p",
        "Let's see how long it takes you\\n",
        "to catch up.$",
    ),
    "LittlerootTown_ProfessorBirchsLab_Text_CatchCoolPokemonWithPokeBalls": (
        "CIRO: I'll follow HORIZON's\\n",
        "survey points.\\p",
        "They say some POKéMON out there\\n",
        "show almost no DESECHANTMENT.$",
    ),
    "LittlerootTown_ProfessorBirchsLab_Text_HeyYourBagsFull": (
        "Your BAG is full.$",
    ),
    "LittlerootTown_ProfessorBirchsLab_Text_BrendanWhereShouldIGoNext": (
        "CIRO: HORIZON has teams across\\n",
        "Arauna.\\p",
        "If their data is right, I'll be\\n",
        "at the next answer before you.$",
    ),
    "LittlerootTown_ProfessorBirchsLab_Text_SeriousLookingMachine": (
        "A BOND sensor fills most of\\n",
        "the workbench.\\p",
        "Its wear marks predate HORIZON's\\n",
        "current project.$",
    ),
    "LittlerootTown_ProfessorBirchsLab_Text_PCUsedForResearch": (
        "The PC holds field data on\\n",
        "POKéMON that stopped recognizing\\n",
        "familiar people and places.$",
    ),
    "LittlerootTown_ProfessorBirchsLab_Text_CrammedWithBooksOnPokemon": (
        "Field notebooks share the shelf\\n",
        "with books on memory, grief and\\n",
        "POKéMON behavior.$",
    ),
    "LittlerootTown_ProfessorBirchsLab_Text_BookTooHardToRead": (
        "The notes mix POKéMON neurology,\\n",
        "BOND theory and handwritten\\n",
        "corrections.$",
    ),
    "LittlerootTown_ProfessorBirchsLab_Text_OtherRegionsUpgradeToNational": (
        "ANAHI: Your records now reach\\n",
        "beyond Arauna.\\p",
        "More data helps only if we keep\\n",
        "asking better questions.$",
    ),
    "LittlerootTown_ProfessorBirchsLab_Text_MayUpgradeSoCool": (
        "CIRO: More data won't repair\\n",
        "a bad question.\\p",
        "But it can expose one.$",
    ),
    "LittlerootTown_ProfessorBirchsLab_Text_BrendanYouCanThankMe": (
        "CIRO: More data won't repair\\n",
        "a bad question.\\p",
        "But it can expose one.$",
    ),
    "LittlerootTown_ProfessorBirchsLab_Text_OkayAllDone": (
        "ANAHI: Done. More species,\\n",
        "same responsibility.\\p",
        "Record what happened. Don't pick\\n",
        "what others should remember.$",
    ),
    "LittlerootTown_ProfessorBirchsLab_Text_PokedexUpgradedToNational": (
        "POKéDEX upgraded to\\n",
        "NATIONAL MODE!$",
    ),
    "LittlerootTown_ProfessorBirchsLab_Text_GrassyPatchWaiting2": (
        "ANAHI: There are still places\\n",
        "your records haven't reached.\\p",
        "Keep looking without assuming\\n",
        "you already know the answer.$",
    ),
    "LittlerootTown_ProfessorBirchsLab_Text_MayTakeBreakFromFieldwork": (
        "CIRO: I hate standing still.\\p",
        "Rushing can be another way\\n",
        "to avoid looking back.$",
    ),
    "LittlerootTown_ProfessorBirchsLab_Text_BrendanTakeBreakFromFieldwork": (
        "CIRO: I hate standing still.\\p",
        "Rushing can be another way\\n",
        "to avoid looking back.$",
    ),
    "LittlerootTown_ProfessorBirchsLab_Text_CompletedDexChoosePokemon": (
        "ANAHI: You documented every\\n",
        "native species.\\p",
        "I promised you a choice.\\p",
        "Three partners are waiting.$",
    ),
    "LittlerootTown_ProfessorBirchsLab_Text_CanHaveAnyOneOfRarePokemon": (
        "ANAHI: Choose one of the three.\\p",
        "The others will stay here.$",
    ),
    "LittlerootTown_ProfessorBirchsLab_Text_YoullTakeCyndaquil": (
        "ANAHI: Choose Coruja?$",
    ),
    "LittlerootTown_ProfessorBirchsLab_Text_YoullTakeTotodile": (
        "ANAHI: Choose Seriema?$",
    ),
    "LittlerootTown_ProfessorBirchsLab_Text_YoullTakeChikorita": (
        "ANAHI: Choose Gaviao?$",
    ),
    "LittlerootTown_ProfessorBirchsLab_Text_TakeYourTimeAllInvaluable": (
        "ANAHI: Take your time.\\p",
        "A partner isn't a prize.$",
    ),
    "LittlerootTown_ProfessorBirchsLab_Text_PickedFinePokemon": (
        "ANAHI: Good choice.\\p",
        "Take care of each other.$",
    ),
    "LittlerootTown_ProfessorBirchsLab_Text_ReceivedJohtoStarter": (
        "{PLAYER} received {STR_VAR_1}\\n",
        "from PROF. ANAHI!$",
    ),
    "LittlerootTown_ProfessorBirchsLab_Text_NicknameJohtoStarter": (
        "Give a nickname to\\n",
        "{STR_VAR_1}?$",
    ),
    "LittlerootTown_ProfessorBirchsLab_Text_GrassyPatchWaiting": (
        "ANAHI: Take care of each other.\\p",
        "A new BOND won't erase old ones.$",
    ),
    "LittlerootTown_ProfessorBirchsLab_Text_BetterLeaveOthersAlone": (
        "You already chose a POKéMON.\\p",
        "Leave the others here.$",
    ),
    "LittlerootTown_ProfessorBirchsLab_Text_DontHaveAnyRoomForPokemon": (
        "You don't have room for this\\n",
        "POKéMON.$",
    ),
    "LittlerootTown_ProfessorBirchsLab_Text_MayWhatNextImStayingHere": (
        "CIRO: I used to think moving on\\n",
        "meant leaving every scar behind.\\p",
        "Now I think it means choosing\\n",
        "what to carry.$",
    ),
    "LittlerootTown_ProfessorBirchsLab_Text_BrendanPreferCollectingSlowly": (
        "CIRO: I used to think moving on\\n",
        "meant leaving every scar behind.\\p",
        "Now I think it means choosing\\n",
        "what to carry.$",
    ),
    "LittlerootTown_ProfessorBirchsLab_Text_MayHaveYouGoneToBattleFrontier": (
        "CIRO: Been to BATTLE CIRCUIT?\\p",
        "Winning there won't solve M'BOI.\\p",
        "It may show what we've learned.$",
    ),
    "LittlerootTown_ProfessorBirchsLab_Text_BrendanHaveYouGoneToBattleFrontier": (
        "CIRO: Been to BATTLE CIRCUIT?\\p",
        "Winning there won't solve M'BOI.\\p",
        "It may show what we've learned.$",
    ),
    "LittlerootTown_ProfessorBirchsLab_Text_ScottAboardSSTidalCall": (
        "... ... ... ... ... ...\\n",
        "... ... ... ... ... Beep!\\p",
        "SEU BENTO: {PLAYER}, listen.\\n",
        "It's BENTO.\\p",
        "ANAHI said your POKéDEX\\n",
        "was expanded.\\p",
        "There's a BATTLE CIRCUIT\\n",
        "beyond the LEAGUE.\\p",
        "If you want to test your BOND,\\n",
        "take the ferry at PORTO DO SAL\\p",
        "or BAIA DAS LUZES.\\p",
        "I'll explain the rest when\\n",
        "you arrive. I'll be there!\\p",
        "... ... ... ... ... ...\\n",
        "... ... ... ... ... Beep!$",
    ),
}

SOURCE_MARKERS = (
    "ANAHI:",
    "CIRO:",
    "HORIZONTE",
    "VINCULO",
    "DESENCANTO",
    "POKéDEX",
    "BOLSA",
    "POKéMON",
    "SEU BENTO:",
    "PROF. ANAHI",
)


def block_pattern(label: str) -> re.Pattern[str]:
    return re.compile(
        rf"(?ms)^{re.escape(label)}:\n(?P<body>.*?)(?=^(?:@[^\n]*\n)*[A-Za-z0-9_]+(?:::|:)(?:\n|$)|\Z)"
    )


def visible_segments(payload: str) -> list[str]:
    cleaned = payload.replace("$", "")
    cleaned = cleaned.replace("{PLAYER}", "PLAYERX")
    cleaned = cleaned.replace("{STR_VAR_1}", "XXXXXXXXXX")
    cleaned = PLACEHOLDER_RE.sub("", cleaned)
    return [part.strip() for part in CONTROL_RE.split(cleaned)]


def validate_widths() -> None:
    for label, payloads in TARGETS.items():
        for payload in payloads:
            for segment in visible_segments(payload):
                if len(segment) > MAX_VISIBLE_WIDTH:
                    raise ValueError(
                        f"{label}: visible segment is {len(segment)} chars, max {MAX_VISIBLE_WIDTH}: {segment!r}"
                    )


def render(source: str) -> str:
    validate_widths()
    rendered = source
    for label, payloads in TARGETS.items():
        pattern = block_pattern(label)
        matches = list(pattern.finditer(rendered))
        if len(matches) != 1:
            raise ValueError(f"{label}: expected one text block, found {len(matches)}")
        body = matches[0].group("body")
        if ".string" not in body:
            raise ValueError(f"{label}: target has no .string payload")
        if not any(marker in body for marker in SOURCE_MARKERS):
            raise ValueError(f"{label}: source no longer resembles the curated Arauna lab surface")
        new_body = "".join(f'\t.string "{payload}"\n' for payload in payloads) + "\n"
        start, end = matches[0].span("body")
        rendered = rendered[:start] + new_body + rendered[end:]
    return rendered


def mask_targets(text: str) -> str:
    masked = text
    for label in TARGETS:
        match = block_pattern(label).search(masked)
        if not match:
            raise ValueError(f"cannot mask missing lab block: {label}")
        start, end = match.span("body")
        masked = masked[:start] + '\t.string "<ARAUNA_ANAHI_LAB_EN>"\n\n' + masked[end:]
    return masked


def validate_rendered(source: str, rendered: str) -> None:
    if mask_targets(source) != mask_targets(rendered):
        raise ValueError("non-dialogue Anahi lab structure changed")

    forbidden = (
        "HORIZONTE", "VINCULO", "DESENCANTO", "BOLSA", "Voce ", "voce ",
        "Nao ", "nao ", "ROTA 103", "recebeu", "apelido", "espaco para",
    )
    for label in TARGETS:
        body = block_pattern(label).search(rendered).group("body")
        for token in forbidden:
            if token in body:
                raise ValueError(f"{label}: Portuguese visible token survived: {token}")

    preserved = (
        "FLAG_SYS_POKEDEX_GET",
        "special SetUnlockedPokedexFlags",
        "special EnableNationalPokedex",
        "FLAG_SYS_NATIONAL_DEX",
        "VAR_DEX_UPGRADE_JOHTO_STARTER_STATE",
        "SPECIES_CYNDAQUIL",
        "SPECIES_TOTODILE",
        "SPECIES_CHIKORITA",
        "ITEM_POKE_BALL",
        "FLAG_SCOTT_CALL_BATTLE_FRONTIER",
        "VAR_BIRCH_LAB_STATE",
    )
    for token in preserved:
        if token not in rendered:
            raise ValueError(f"preserved Anahi-lab gameplay token missing: {token}")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Render the complete visible Anahi laboratory surface in English without changing inherited Emerald event wiring."
    )
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--in-place", action="store_true")
    args = parser.parse_args()
    if args.check and args.in_place:
        parser.error("use either --check or --in-place")

    source = TARGET.read_text(encoding="utf-8")
    rendered = render(source)
    validate_rendered(source, rendered)

    if args.check:
        print(f"Anahi lab English renderer OK: {len(TARGETS)} text blocks validated.")
        return 0
    if args.in_place:
        TARGET.write_text(rendered, encoding="utf-8")
        return 0
    print(rendered, end="" if rendered.endswith("\n") else "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
