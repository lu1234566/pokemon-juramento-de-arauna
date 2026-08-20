#!/usr/bin/env python3
from __future__ import annotations
import argparse
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MAX = 32
CTRL = re.compile(r"\\[npl]")
PH = re.compile(r"\{[^}]+\}")
TARGETS: dict[str, dict[str, tuple[str, ...]]] = {}


def add(path: str, label: str, *lines: str) -> None:
    TARGETS.setdefault(path, {})[label] = lines


R110 = "data/maps/Route110/scripts.inc"
add(R110, "Route110_Text_WeCantTalkAboutAquaActivities",
    "HORIZON AGENT: Field work is\\n", "restricted right now.$")
add(R110, "Route110_Text_KickUpARuckus",
    "HORIZON AGENT: PORTO DO SAL\\n", "made central command nervous.$")
add(R110, "Route110_Text_MyFirstJobInAqua",
    "HORIZON AGENT: First field job.\\p", "I hope the sensors stay quiet.$")
add(R110, "Route110_Text_AquaActionsBringSmiles",
    "HORIZON AGENT: We are told the\\n", "network exists to help people.$")
for who in ("May", "Brendan"):
    add(R110, f"Route110_Text_{who}LetsBattle",
        "CIRO: You keep treating every\\n", "scar like an answer.\\p",
        "I want to know what exists\\n", "after it. Battle me.$")
    add(R110, f"Route110_Text_{who}Defeated",
        "CIRO: Don't mistake speed for\\n", "forgetting.\\p",
        "I remember enough to refuse a\\n", "life ruled by what I lost.$")
    add(R110, f"Route110_Text_{who}TakeThis",
        "CIRO: HORIZON didn't ask me to\\n", "forget anything.\\p",
        "It showed me a future that is\\n", "not governed by the past.$")
    add(R110, f"Route110_Text_{who}ExplainItemfinder",
        "CIRO: This ITEMFINDER reacts to\\n", "hidden objects nearby.\\p",
        "Use it well. I won't mark every\\n", "answer for you.$")
add(R110, "Route110_Text_WhichShouldIChoose",
    "Which way?\\p", "Fast road to ENCRUZILHADA\\n",
    "CENTRAL, or the low road for\\n", "POKéMON?$")
add(R110, "Route110_Text_RatedForNumberOfCollisions",
    "This is CYCLING ROAD.\\p",
    "Ride south from ENCRUZILHADA\\n", "CENTRAL on a MACH BIKE to be\\n",
    "rated for time and collisions.$")
add(R110, "Route110_Text_SlateportCitySign",
    "SOUTH: PORTO DO SAL\\p",
    "The road carries traces of the\\n", "DISENCHANTMENT.$")
add(R110, "Route110_Text_AquaWasHere",
    "“HORIZON WAS HERE!”\\p",
    "Someone painted over it with:\\p", "“REMEMBRANCERS REMEMBER.”$")
add(R110, "Route110_Text_MauvilleCitySign",
    "NORTH: ENCRUZILHADA CENTRAL\\p",
    "Power lines and roads meet there.$")
add(R110, "Route110_Text_ImagineSeeingYouHere",
    "ANAHI: I helped build the first\\n", "BOND sensors.\\p",
    "Silence about their misuse would\\n", "make the mistake partly mine.$")
add(R110, "Route110_Text_HeardYouInstallMatchCall",
    "ANAHI: Your POKéNAV has MATCH CALL.\\p",
    "Register me too.\\p",
    "I want you to be able to question\\n", "my field notes from anywhere.$")
add(R110, "Route110_Text_RegisteredBirchInPokenav",
    "Registered PROF. ANAHI in\\n", "the POKéNAV.$")
add(R110, "Route110_Text_KeepAnEyeOutForRival",
    "ANAHI: I once thought measuring\\n", "meant understanding.\\p",
    "Now I know those are different\\n", "things. Keep watching CIRO.$")

CITY = "data/maps/MauvilleCity/scripts.inc"
add(CITY, "MauvilleCity_Text_UncleHesTooPeppy",
    "UNCLE: VAL has more energy since\\n", "he began traveling with POKéMON.\\p",
    "I still worry he pushes himself.$")
add(CITY, "MauvilleCity_Text_WallyWantToChallengeGym",
    "VAL: I thought I had to become\\n", "someone else to keep traveling.\\p",
    "I only needed to find my own pace.$")
add(CITY, "MauvilleCity_Text_UncleYourePushingIt",
    "UNCLE: VAL, you have grown a lot.\\p",
    "But a GYM challenge is a big step.\\p", "You do not have to prove anything.$")
add(CITY, "MauvilleCity_Text_WallyWeCanBeatAnyone",
    "VAL: I know. I still want to try.\\p",
    "Fear can come with me this time.$")
add(CITY, "MauvilleCity_Text_WallyWillYouBattleMe",
    "VAL: {PLAYER}, battle me?\\p",
    "I need to know what my own pace\\n", "feels like under pressure.$")
add(CITY, "MauvilleCity_Text_WallyMyUncleWontKnowImStrong",
    "VAL: I am still afraid.\\p",
    "Courage isn't forgetting fear.\\p", "It is walking while remembering.$")
add(CITY, "MauvilleCity_Text_UncleCanYouBattleWally",
    "UNCLE: If VAL asks again, please\\n", "give him an honest battle.$")
add(CITY, "MauvilleCity_Text_WallyPleaseBattleMe",
    "VAL: Please. One honest battle.\\p", "I am ready to try again.$")
add(CITY, "MauvilleCity_Text_WallyHereICome",
    "VAL: I am scared. I am going anyway.$")
add(CITY, "MauvilleCity_Text_WallyDefeat",
    "VAL: I lost... and I am still here.$")
add(CITY, "MauvilleCity_Text_WallyIllGoBackToVerdanturf",
    "VAL: I'll return to VALE DO SILENCIO\\n", "and train at my own pace.$")
add(CITY, "MauvilleCity_Text_ThankYouNotEnoughToBattle",
    "VAL: Thank you, {PLAYER}.\\p",
    "A real TRAINER listens to the\\n", "POKéMON beside them too.$")
add(CITY, "MauvilleCity_Text_UncleNoNeedToBeDown",
    "UNCLE: VAL, losing did not erase\\n", "the progress you made.\\p",
    "Come on. Everyone is waiting.$")
add(CITY, "MauvilleCity_Text_UncleVisitUsSometime",
    "UNCLE: You helped VAL before.\\p",
    "Visit us in VALE DO SILENCIO\\n", "sometime. He would like that.$")
add(CITY, "MauvilleCity_Text_WallyPokenavCall",
    "VAL: I still get afraid.\\p",
    "Now I know fear can travel with me\\n", "without choosing my direction.$")
add(CITY, "MauvilleCity_Text_RegisteredWally",
    "Registered VAL in the POKéNAV.$")
add(CITY, "MauvilleCity_Text_ScottYouDidntHoldBack",
    "SEU BENTO: I watched that battle.\\p",
    "You respected VAL enough not to\\n", "pretend the test was easier.\\p",
    "Kindness and honesty can coexist.$")
add(CITY, "MauvilleCity_Text_WattsonNeedFavorTakeKey",
    "OLIVIA: Energy moves this city.\\p",
    "That does not make every source\\n", "acceptable. Take this BASEMENT KEY.$")
add(CITY, "MauvilleCity_Text_WattsonWontBeChallenge",
    "OLIVIA: Shut down the generator in\\n", "the underground sector.\\p",
    "I will not keep a dangerous system\\n", "alive for convenience.$")
add(CITY, "MauvilleCity_Text_WattsonThanksTakeTM",
    "OLIVIA: The generator is secure.\\p",
    "Thank you. Take THUNDERBOLT.$")
add(CITY, "MauvilleCity_Text_WattsonYoungTakeCharge",
    "OLIVIA: A network is useful only if\\n", "someone accepts responsibility.$")
add(CITY, "MauvilleCity_Text_CitySign",
    "ENCRUZILHADA CENTRAL\\p",
    "The city prospered with HORIZON.\\p",
    "CIRO now wears the uniform of\\n", "those promising a new future.$")
add(CITY, "MauvilleCity_Text_GymSign",
    "ENCRUZILHADA CENTRAL GYM\\n", "LEADER: OLIVIA\\p",
    "Every network leaves a trace.$")
add(CITY, "MauvilleCity_Text_AllSortsOfPeopleComeThrough",
    "Roads run north, south, east and\\n", "west from ENCRUZILHADA CENTRAL.\\p",
    "Everyone passes through eventually.$")

GYM = "data/maps/MauvilleCity_Gym/scripts.inc"
add(GYM, "MauvilleCity_Gym_Text_GymGuideAdvice",
    "ENCRUZILHADA CENTRAL's leader is\\n", "OLIVIA.\\p",
    "She uses ELECTRIC POKéMON.\\p",
    "GROUND moves help, and the floor\\n", "switches change the barriers.$")
add(GYM, "MauvilleCity_Gym_Text_GymGuidePostVictory",
    "You opened every circuit.\\p", "The BEACON BADGE is yours.$")
add(GYM, "MauvilleCity_Gym_Text_ShawnPostBattle",
    "OLIVIA taught me that a circuit is\\n", "only safe when someone owns the risk.$")
add(GYM, "MauvilleCity_Gym_Text_BenPostBattle",
    "OLIVIA uses switches to make us\\n", "trace the whole circuit.$")
add(GYM, "MauvilleCity_Gym_Text_VivianPostBattle",
    "ENCRUZILHADA CENTRAL grew around\\n", "power, roads and HORIZON contracts.$")
add(GYM, "MauvilleCity_Gym_Text_AngeloPostBattle",
    "OLIVIA says bright systems can still\\n", "hide dangerous wiring.$")
add(GYM, "MauvilleCity_Gym_Text_WattsonIntro",
    "OLIVIA: Energy moves a city.\\p",
    "That does not mean every source of\\n", "energy should be accepted.\\p",
    "Show me how you read a network.$")
add(GYM, "MauvilleCity_Gym_Text_WattsonDefeat",
    "OLIVIA: You found the weak point\\n", "without breaking the whole system.$")
add(GYM, "MauvilleCity_Gym_Text_ReceivedDynamoBadge",
    "{PLAYER} received the\\n", "BEACON BADGE from OLIVIA.$")
add(GYM, "MauvilleCity_Gym_Text_ExplainDynamoBadgeTakeThis",
    "The BEACON BADGE lets you use\\n", "ROCK SMASH outside battle.\\p",
    "It also raises your POKéMON's\\n", "SPEED a little. Take this TM.$")
add(GYM, "MauvilleCity_Gym_Text_RegisteredWattson",
    "Registered GYM LEADER OLIVIA\\n", "in the POKéNAV.$")
add(GYM, "MauvilleCity_Gym_Text_WattsonPostBattle",
    "OLIVIA: Every network leaves a\\n", "trace. Learn which traces matter.$")
add(GYM, "MauvilleCity_Gym_Text_WattsonGoForthAndEndeavor",
    "OLIVIA: Keep asking who benefits\\n", "from the systems you power.$")
add(GYM, "MauvilleCity_Gym_Text_GymStatue",
    "ENCRUZILHADA CENTRAL POKéMON GYM$")
add(GYM, "MauvilleCity_Gym_Text_GymStatueCertified",
    "ENCRUZILHADA CENTRAL POKéMON GYM\\p",
    "OLIVIA'S CERTIFIED TRAINERS:\\n", "{PLAYER}$")
add(GYM, "MauvilleCity_Gym_Text_WattsonPreRematch",
    "OLIVIA: Networks change under load.\\p", "Let's test ours again.$")
add(GYM, "MauvilleCity_Gym_Text_WattsonRematchDefeat",
    "OLIVIA: Good. You traced the change.$")
add(GYM, "MauvilleCity_Gym_Text_WattsonPostRematch",
    "OLIVIA: A stable system is never an\\n", "excuse to stop checking it.$")
add(GYM, "MauvilleCity_Gym_Text_WattsonRematchNeedTwoMons",
    "OLIVIA: Bring at least two POKéMON\\n", "for a rematch.$")

PRESERVED = {
    R110: ("VAR_CYCLING_CHALLENGE_STATE", "TRAINER_MAY_ROUTE_110_TREECKO", "TRAINER_BRENDAN_ROUTE_110_TREECKO", "ITEM_ITEMFINDER"),
    CITY: ("FLAG_VISITED_MAUVILLE_CITY", "TRAINER_WALLY_MAUVILLE", "VAR_SCOTT_STATE", "ITEM_BASEMENT_KEY", "VAR_NEW_MAUVILLE_STATE"),
    GYM: ("TRAINER_WATTSON_1", "FLAG_BADGE03_GET", "ITEM_TM_SHOCK_WAVE", "VAR_MAUVILLE_GYM_STATE"),
}


def pattern(label: str) -> re.Pattern[str]:
    return re.compile(rf"(?ms)^{re.escape(label)}:\n(?P<body>.*?)(?=^[A-Za-z0-9_]+(?:::|:)(?:\n|$)|\Z)")


def validate_widths() -> None:
    for rel, blocks in TARGETS.items():
        for label, lines in blocks.items():
            for line in lines:
                cleaned = PH.sub("PLAYER", line.replace("$", ""))
                for part in CTRL.split(cleaned):
                    if len(part.strip()) > MAX:
                        raise ValueError(f"{rel}: {label}: line exceeds {MAX}: {part.strip()!r}")


def masked(text: str, labels: tuple[str, ...]) -> str:
    result = text
    for label in labels:
        match = pattern(label).search(result)
        if not match:
            raise ValueError(f"missing block: {label}")
        a, b = match.span("body")
        result = result[:a] + '\t.string "<ARAUNA_EN>"\n\n' + result[b:]
    return result


def render(rel: str, source: str) -> str:
    result = source
    labels = tuple(TARGETS[rel])
    for label, lines in TARGETS[rel].items():
        found = list(pattern(label).finditer(result))
        if len(found) != 1:
            raise ValueError(f"{rel}: {label}: expected 1 block, found {len(found)}")
        body = "".join(f'\t.string "{line}"\n' for line in lines) + "\n"
        a, b = found[0].span("body")
        result = result[:a] + body + result[b:]
    if masked(source, labels) != masked(result, labels):
        raise ValueError(f"{rel}: non-dialogue structure changed")
    for token in PRESERVED[rel]:
        if token not in result:
            raise ValueError(f"{rel}: missing preserved token {token}")
    return result


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
        output = render(rel, source)
        if output != source:
            changed += 1
            if args.in_place:
                path.write_text(output, encoding="utf-8")
    mode = "check" if args.check else "render" if args.in_place else "dry render"
    print(f"Route110/Encruzilhada {mode} OK: {total} blocks across {len(TARGETS)} files; {changed} changed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
