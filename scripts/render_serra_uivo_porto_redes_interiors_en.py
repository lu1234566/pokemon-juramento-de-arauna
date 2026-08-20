#!/usr/bin/env python3
from __future__ import annotations
import argparse
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MAX_VISIBLE_WIDTH = 32
CONTROL_RE = re.compile(r"\\[npl]")
PLACEHOLDER_RE = re.compile(r"\{[^}]+\}")
TARGETS: dict[str, dict[str, tuple[str, ...]]] = {}


def add(path: str, label: str, *lines: str) -> None:
    TARGETS.setdefault(path, {})[label] = lines


D1 = "data/maps/RustboroCity_DevonCorp_1F/scripts.inc"
add(D1, "RustboroCity_DevonCorp_1F_Text_WelcomeToDevonCorp",
    "Welcome to the HORIZON\\n", "CONSORTIUM field center.\\p",
    "This floor is open to visitors.$")
add(D1, "RustboroCity_DevonCorp_1F_Text_StaffGotRobbed",
    "A central HORIZON agent took a\\n", "sealed RESEARCH CASE.\\p",
    "The local team never approved it.$")
add(D1, "RustboroCity_DevonCorp_1F_Text_ThoseShoesAreOurProduct",
    "Those RUNNING SHOES use a sole\\n", "developed by this field center.\\p",
    "Not every HORIZON project is a\\n", "BOND experiment.$")
add(D1, "RustboroCity_DevonCorp_1F_Text_RobberWasntVeryBright",
    "The stolen case is useful only\\n", "with the matching lab equipment.\\p",
    "That makes the recall stranger.$")
add(D1, "RustboroCity_DevonCorp_1F_Text_SoundsLikeStolenGoodsRecovered",
    "The RESEARCH CASE was recovered.\\p", "Its seals are still intact.$")
add(D1, "RustboroCity_DevonCorp_1F_Text_OnlyAuthorizedPeopleEnter",
    "Sorry. The upper floors require\\n", "authorization.$")
add(D1, "RustboroCity_DevonCorp_1F_Text_HowCouldWeGetRobbed",
    "A valid central credential opened\\n", "our own security doors.\\p",
    "That is what worries me.$")
add(D1, "RustboroCity_DevonCorp_1F_Text_YoureAlwaysWelcomeHere",
    "You helped recover our records.\\p", "You're welcome on the upper floor.$")
add(D1, "RustboroCity_DevonCorp_1F_Text_RocksMetalDisplay",
    "A display traces HORIZON's past.\\p",
    "It began with stone, metal and\\n", "road engineering in Arauna.\\p",
    "Later came BOND measurement.$")
add(D1, "RustboroCity_DevonCorp_1F_Text_ProductDisplay",
    "Prototype POKé BALLS and POKéNAV\\n", "parts fill the case.\\p",
    "A newer panel lists BOND sensors\\n", "as restricted research.$")

D2 = "data/maps/RustboroCity_DevonCorp_2F/scripts.inc"
add(D2, "RustboroCity_DevonCorp_2F_Text_DeviceForTalkingToPokemon",
    "We're testing ways to interpret\\n", "POKéMON signals.\\p",
    "A signal is not consent, though.$")
add(D2, "RustboroCity_DevonCorp_2F_Text_DevelopingNewBalls",
    "I'm developing new POKé BALLS.\\p", "Progress is slow, but honest.$")
add(D2, "RustboroCity_DevonCorp_2F_Text_WeFinallyMadeNewBalls",
    "The REPEAT BALL and TIMER BALL\\n", "are ready.\\p",
    "They came from this field center,\\n", "not the LIVING ARCHIVE program.$")
add(D2, "RustboroCity_DevonCorp_2F_Text_IMadePokenav",
    "I helped build the POKéNAV.\\p",
    "Navigation and field notes were\\n", "the original purpose.$")
add(D2, "RustboroCity_DevonCorp_2F_Text_WowThatsAPokenav",
    "That's one of our POKéNAV units.\\p",
    "It maps routes, stores contacts\\n", "and records field observations.$")
add(D2, "RustboroCity_DevonCorp_2F_Text_DeviceToVisualizePokemonDreams",
    "I'm testing a dream-imaging rig.\\p",
    "We stop the moment a POKéMON shows\\n", "distress.$")
add(D2, "RustboroCity_DevonCorp_2F_Text_DevelopDeviceToResurrectFossils",
    "My FOSSIL REGENERATOR can revive\\n", "ancient POKéMON from fossils.$")
add(D2, "RustboroCity_DevonCorp_2F_Text_WantToBringFossilBackToLife",
    "Is that a POKéMON fossil?\\p",
    "I can revive one fossil at a time.\\p", "Would you like me to try?$")
add(D2, "RustboroCity_DevonCorp_2F_Text_OhIsThatSo",
    "No problem. The machine will stay\\n", "ready if you change your mind.$")
add(D2, "RustboroCity_DevonCorp_2F_Text_TwoFossilsPickOne",
    "You have two fossils.\\p",
    "The machine handles only one at\\n", "a time. Choose one to revive.$")
add(D2, "RustboroCity_DevonCorp_2F_Text_HandedFossilToResearcher",
    "{PLAYER} handed the {STR_VAR_1}\\n", "to the HORIZON RESEARCHER.$")
add(D2, "RustboroCity_DevonCorp_2F_Text_FossilRegeneratorTakesTime",
    "The FOSSIL REGENERATOR needs\\n", "time to finish.\\p",
    "Take a short walk and return.$")
add(D2, "RustboroCity_DevonCorp_2F_Text_FossilizedMonBroughtBackToLife",
    "The revival is complete!\\p",
    "The fossil became {STR_VAR_2} again.$")
add(D2, "RustboroCity_DevonCorp_2F_Text_ReceivedMonFromResearcher",
    "{PLAYER} received {STR_VAR_2} from\\n", "the HORIZON RESEARCHER.$")
add(D2, "RustboroCity_DevonCorp_2F_Text_DevelopNewPokenavFeature",
    "I'm working on a new POKéNAV\\n", "feature for field teams.$")
add(D2, "RustboroCity_DevonCorp_2F_Text_WhatToWorkOnNext",
    "I choose my next project carefully.\\p",
    "Being possible is not the same as\\n", "being worth doing.$")

CUT = "data/maps/RustboroCity_CuttersHouse/scripts.inc"
add(CUT, "RustboroCity_CuttersHouse_Text_YouCanPutThisHMToGoodUse",
    "You look ready for rough trails.\\p", "Take this HM. It contains CUT.$")
add(CUT, "RustboroCity_CuttersHouse_Text_ExplainCut",
    "CUT can clear thin trees outside\\n", "battle.\\p",
    "You need the RIFT BADGE to use it\\n", "that way. HMs can be reused.$")
add(CUT, "RustboroCity_CuttersHouse_Text_DadHelpedClearLandOfTrees",
    "My father cleared old road lines\\n", "when SERRA DO UIVO expanded.\\p",
    "He always marked what he removed.$")

SCHOOL = "data/maps/RustboroCity_PokemonSchool/scripts.inc"
add(SCHOOL, "RustboroCity_PokemonSchool_Text_ScottMetAlreadyCut",
    "SEU BENTO: We met in\\n", "PAMPA DA ESPERA.\\p",
    "I watch how TRAINERS treat the\\n", "BONDS they depend on.\\p",
    "Someone in town can teach CUT.$")
add(SCHOOL, "RustboroCity_PokemonSchool_Text_StudentTalentLevelUnknown",
    "SEU BENTO: A classroom shows\\n", "practice, not a person's limit.\\p",
    "I'll keep watching.$")
add(SCHOOL, "RustboroCity_PokemonSchool_Text_ScottStoneBadge",
    "SEU BENTO: That's a RIFT BADGE.\\p",
    "A BADGE tells me you won once.\\p",
    "How you act afterward tells me\\n", "more.$")
add(SCHOOL, "RustboroCity_PokemonSchool_Text_ScottMetAlreadyStoneBadge",
    "SEU BENTO: We met in\\n", "PAMPA DA ESPERA.\\p",
    "And you already carry DALVA's\\n", "RIFT BADGE.\\p",
    "Good. Now show what you learned.$")

GRANITE = "data/maps/GraniteCave_StevensRoom/scripts.inc"
add(GRANITE, "GraniteCave_StevensRoom_Text_ImStevenLetterForMe",
    "SEU BENTO: A LETTER for me?\\p",
    "I write down names when they fade\\n", "from ordinary conversation.\\p",
    "A record should leave a trail, not\\n", "replace the people who remember.$")
add(GRANITE, "GraniteCave_StevensRoom_Text_ThankYouTakeThis",
    "SEU BENTO: Thank you.\\p",
    "This copy stays outside HORIZON.\\p", "Take this TM for the trouble.$")
add(GRANITE, "GraniteCave_StevensRoom_Text_CouldBecomeChampionLetsRegister",
    "SEU BENTO: You pay attention.\\p",
    "That matters more than speed.\\p", "Register my POKéNAV contact.$")
add(GRANITE, "GraniteCave_StevensRoom_Text_RegisteredSteven",
    "SEU BENTO was registered in\\n", "the POKéNAV.$")
add(GRANITE, "GraniteCave_StevensRoom_Text_IveGotToHurryAlong",
    "SEU BENTO: I have more notebooks\\n", "to compare. We'll meet again.$")
add(GRANITE, "GraniteCave_StevensRoom_Text_OhBagIsFull",
    "SEU BENTO: Your BAG is full.\\p", "Make room, then come back.$")

HOUSE2 = "data/maps/DewfordTown_House2/scripts.inc"
add(HOUSE2, "DewfordTown_House2_Text_BrawlySoCool",
    "ADEMAR listens before he speaks.\\p",
    "People here trust that more than\\n", "a loud promise.$")

PRESERVED = {
    D1: ("FLAG_RETURNED_DEVON_GOODS", "FLAG_DEVON_GOODS_STOLEN", "FLAG_RECOVERED_DEVON_GOODS"),
    D2: ("VAR_FOSSIL_RESURRECTION_STATE", "ITEM_ROOT_FOSSIL", "ITEM_CLAW_FOSSIL", "FLAG_RECEIVED_REVIVED_FOSSIL_MON"),
    CUT: ("ITEM_HM_CUT", "FLAG_RECEIVED_HM_CUT"),
    SCHOOL: ("FLAG_BADGE01_GET", "VAR_SCOTT_STATE", "ITEM_QUICK_CLAW"),
    GRANITE: ("ITEM_LETTER", "FLAG_DELIVERED_STEVEN_LETTER", "ITEM_TM_STEEL_WING", "FLAG_REGISTERED_STEVEN_POKENAV"),
    HOUSE2: ("ITEM_SILK_SCARF", "FLAG_RECEIVED_SILK_SCARF"),
}


def block_pattern(label: str) -> re.Pattern[str]:
    return re.compile(rf"(?ms)^{re.escape(label)}:\n(?P<body>.*?)(?=^[A-Za-z0-9_]+(?:::|:)(?:\n|$)|\Z)")


def validate_widths() -> None:
    for path, blocks in TARGETS.items():
        for label, lines in blocks.items():
            for line in lines:
                cleaned = PLACEHOLDER_RE.sub("PLAYER", line.replace("$", ""))
                for part in CONTROL_RE.split(cleaned):
                    segment = part.strip()
                    if len(segment) > MAX_VISIBLE_WIDTH:
                        raise ValueError(f"{path}: {label}: {len(segment)} chars: {segment!r}")


def mask_target_bodies(text: str, labels: tuple[str, ...]) -> str:
    masked = text
    for label in labels:
        match = block_pattern(label).search(masked)
        if not match:
            raise ValueError(f"missing target block while masking: {label}")
        start, end = match.span("body")
        masked = masked[:start] + '\t.string "<ARAUNA_EN>"\n\n' + masked[end:]
    return masked


def render_one(rel: str, source: str) -> str:
    rendered = source
    labels = tuple(TARGETS[rel])
    for label, lines in TARGETS[rel].items():
        matches = list(block_pattern(label).finditer(rendered))
        if len(matches) != 1:
            raise ValueError(f"{rel}: {label}: expected one block, found {len(matches)}")
        body = "".join(f'\t.string "{line}"\n' for line in lines) + "\n"
        start, end = matches[0].span("body")
        rendered = rendered[:start] + body + rendered[end:]
    if mask_target_bodies(source, labels) != mask_target_bodies(rendered, labels):
        raise ValueError(f"{rel}: non-dialogue structure changed")
    for token in PRESERVED[rel]:
        if token not in rendered:
            raise ValueError(f"{rel}: preserved gameplay token missing: {token}")
    return rendered


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--in-place", action="store_true")
    args = parser.parse_args()
    if args.check and args.in_place:
        parser.error("choose --check or --in-place")
    validate_widths()
    total = sum(len(v) for v in TARGETS.values())
    changed = 0
    for rel in TARGETS:
        path = ROOT / rel
        source = path.read_text(encoding="utf-8")
        rendered = render_one(rel, source)
        if rendered != source:
            changed += 1
            if args.in_place:
                path.write_text(rendered, encoding="utf-8")
    if args.check:
        print(f"Serra/Porto interior renderer OK: {total} blocks across {len(TARGETS)} files.")
    elif args.in_place:
        print(f"Rendered {total} blocks across {changed} interior files.")
    else:
        print(f"Dry render OK: {total} blocks across {len(TARGETS)} files.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
