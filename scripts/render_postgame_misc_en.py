#!/usr/bin/env python3
from __future__ import annotations
import argparse,re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
MAX=32; CTRL=re.compile(r"\\[npl]"); PH=re.compile(r"\{[^}]+\}")
T:dict[str,dict[str,tuple[str,...]]]={}
def add(p,l,*x): T.setdefault(p,{})[l]=x

PAMPA="data/maps/PetalburgCity_House2/scripts.inc"
add(PAMPA,"PetalburgCity_House2_Text_NormanBecameGymLeader",
    "ELIAS: Some guilt does not vanish\\n","when we stay silent.\\p",
    "I approved part of the M'BOI project\\n","and called my fear prudence for years.$")
add(PAMPA,"PetalburgCity_House2_Text_BattledNormanOnce",
    "ELIAS: Being your father never gave\\n","me the right to decide which truths\\n","you could bear.\\p",
    "It took me too long to understand.$")

CENTER="data/maps/FortreeCity_PokemonCenter_1F/scripts.inc"
add(CENTER,"FortreeCity_PokemonCenter_1F_Text_GoToSafariZone",
    "Building a POKéDEX?\\p",
    "Visit the SAFARI ZONE. You may find\\n","POKéMON you have not seen elsewhere.$")
add(CENTER,"FortreeCity_PokemonCenter_1F_Text_RecordCornerIsNeat",
    "Have you used the RECORD CORNER?\\p",
    "It mixes records from different\\n","TRAINERS. Strange, but interesting.$")
add(CENTER,"FortreeCity_PokemonCenter_1F_Text_DoYouKnowAboutPokenav",
    "You have a POKéNAV too!\\p",
    "MATCH CALL lets you contact TRAINERS\\n","you registered before.\\p",
    "It also shows who is ready for a\\n","rematch. HORIZON built the system.$")

FOSSIL="data/maps/Route114_FossilManiacsTunnel/scripts.inc"
add(FOSSIL,"Route114_FossilManiacsTunnel_Text_LookInDesertForFossils",
    "I'm a FOSSIL researcher.\\p",
    "I love FOSSILS, but these are mine.\\p",
    "If you want to find your own, search\\n","the desert.\\p",
    "Stone and sand hide things for a\\n","very long time.$")
add(FOSSIL,"Route114_FossilManiacsTunnel_Text_DevonCorpRevivingFossils",
    "You found a FOSSIL? Beautiful.\\p",
    "HORIZON researchers can revive some\\n","POKéMON from FOSSILS.\\p",
    "I prefer leaving mine as I found them.$")
add(FOSSIL,"Route114_FossilManiacsTunnel_Text_FossilsAreWonderful",
    "FOSSILS are wonderful.\\p","I could stare at them all day.$")
add(FOSSIL,"Route114_FossilManiacsTunnel_Text_NotSafeThatWay",
    "That way isn't safe.\\p",
    "The wall collapsed while I dug and\\n","revealed a huge cave below.\\p",
    "I left it alone. I found no FOSSILS\\n","down there.$")

SHIP="data/maps/SSTidalCorridor/scripts.inc"
add(SHIP,"SSTidalCorridor_Text_ScottBattleFrontierInvite",
    "SEU BENTO: {PLAYER}{KUN}, good to see\\n","you here.\\p",
    "Congratulations on the LEAGUE.\\p",
    "I want to see how you handle the\\n","CIRCUITO DE BATALHA.\\p",
    "I spoke with the crew. On your next\\n","trip, this ferry can take you there.\\p",
    "I'll be waiting.$")
add(SHIP,"SSTidal_Text_FastCurrentsHopeYouEnjoyVoyage",
    "This ferry crosses strong currents\\n","without losing course.\\p",
    "Enjoy the voyage and explore aboard.$")
add(SHIP,"SSTidal_Text_HopeYouEnjoyVoyage","We hope you enjoy the voyage.$")
add(SHIP,"SSTidal_Text_MadeLandInSlateport",
    "We have arrived at PORTO DO SAL.\\p","Thank you for sailing with us.$")
add(SHIP,"SSTidal_Text_MadeLandInLilycove",
    "We have arrived at BAIA DAS LUZES.\\p","Thank you for sailing with us.$")
add(SHIP,"SSTidalCorridor_Text_CanRestInCabin2",
    "We still have some distance to go.\\p",
    "If you want to rest, use Cabin 2.$")
add(SHIP,"SSTidalCorridor_Text_WeveArrived","We have arrived!$")
add(SHIP,"SSTidalCorridor_Text_VisitOtherCabins",
    "Visit the other cabins.\\p",
    "Some bored TRAINERS may want a\\n","battle.$")
add(SHIP,"SSTidalCorridor_Text_EnjoyYourCruise","Enjoy the voyage!$")
add(SHIP,"SSTidalCorridor_Text_HorizonSpreadsBeyondPorthole",
    "The horizon stretches beyond the\\n","porthole.$")
add(SHIP,"SSTidalCorridor_Text_BrineyWelcomeAboard",
    "CAPTAIN: Welcome aboard, {PLAYER}{KUN}!\\p",
    "They gave me command of this ferry.\\p",
    "I had left the sea, but a ship like\\n","this wakes any sailor's soul.$")
for i in range(1,5): add(SHIP,f"SSTidalCorridor_Text_Cabin{i}",f"Cabin {i}$")

SCOTT="data/maps/BattleFrontier_ScottsHouse/scripts.inc"
add(SCOTT,"BattleFrontier_ScottsHouse_Text_WelcomeToBattleFrontier",
    "SEU BENTO: So you came.\\p",
    "This place may not look enormous,\\n","but the challenge is serious.\\p",
    "{PLAYER}{KUN}, welcome to the\\n","CIRCUITO DE BATALHA.\\p",
    "It took years to gather the people\\n","who keep this place running.$")
add(SCOTT,"BattleFrontier_ScottsHouse_Text_HowMuchEffortItTookToMakeReal",
    "I started by traveling alone, looking\\n","for TRAINERS who held under pressure.\\p",
    "It was a long road. This place grew\\n","from it.$")
add(SCOTT,"BattleFrontier_ScottsHouse_Text_HaveThisAsMementoOfOurPathsCrossing",
    "The past brought all of us here.\\p",
    "I won't decorate that truth.\\p",
    "Fight with everything you learned.\\p",
    "{PLAYER}{KUN}, take this as a mark of\\n","where our paths crossed.$")
add(SCOTT,"BattleFrontier_ScottsHouse_Text_ObtainedXBattlePoints",
    "{PLAYER} received {STR_VAR_1}\\n","Battle Point(s).$")
add(SCOTT,"BattleFrontier_ScottsHouse_Text_ExplainBattlePoints",
    "SEU BENTO: Your Battle Points are\\n","stored on the CIRCUIT PASS.\\p",
    "Better results earn more points.\\p",
    "Exchange them for items when you\\n","think it is worth it.$")
add(SCOTT,"BattleFrontier_ScottsHouse_Text_ExpectingGreatThings",
    "I want to see how far you can go!$")
add(SCOTT,"BattleFrontier_ScottsHouse_Text_WhyIGoSeekingTrainers",
    "SEU BENTO: Every TRAINER carries a\\n","different story.\\p",
    "But excuses don't change a battle's\\n","result.\\p",
    "I look for people willing to be\\n","tested, and I bring them here.$")
add(SCOTT,"BattleFrontier_ScottsHouse_Text_HaveYouMetFrontierBrain",
    "SEU BENTO: Met a CIRCUIT MASTER yet?\\p",
    "Earned any SYMBOLS?\\p",
    "I chose each MASTER because they do\\n","not make things easy.$")
add(SCOTT,"BattleFrontier_ScottsHouse_Text_MayFindWildMonsInFrontier",
    "SEU BENTO: Still filling the POKéDEX?\\p",
    "Explore the CIRCUITO carefully.\\p",
    "Wild POKéMON appear where you least\\n","expect them.$")
add(SCOTT,"BattleFrontier_ScottsHouse_Text_YouveCollectedAllSilverSymbols",
    "SEU BENTO: Let me see that PASS...\\p",
    "Every SILVER SYMBOL.\\p",
    "That is no small achievement. You\\n","earned this reward.$")
add(SCOTT,"BattleFrontier_ScottsHouse_Text_YouveCollectedAllGoldSymbols",
    "SEU BENTO: All GOLD SYMBOLS.\\p",
    "Very few TRAINERS get this far.\\p",
    "{PLAYER}, take this. You'll value it.$")
add(SCOTT,"BattleFrontier_ScottsHouse_Text_SoGladIBroughtYouHere",
    "I knew you would cause trouble when\\n","we first met.\\p",
    "I'm glad I brought you to this circuit.$")
add(SCOTT,"BattleFrontier_ScottsHouse_Text_BerryPocketStuffed",
    "The BERRY pocket in your BAG is full.$")
add(SCOTT,"BattleFrontier_ScottsHouse_Text_Beat50TrainersInARow",
    "SEU BENTO: Fifty straight wins in\\n","BATTLE TOWER?\\p","Not bad. Take this.$")
add(SCOTT,"BattleFrontier_ScottsHouse_Text_Beat100TrainersInARow",
    "SEU BENTO: One hundred straight wins\\n","in BATTLE TOWER?\\p",
    "Now you're raising the stakes. Take\\n","this.$")
add(SCOTT,"BattleFrontier_ScottsHouse_Text_ExpectingToHearEvenGreaterThings",
    "Now I expect even bigger news from\\n","you.$")
add(SCOTT,"BattleFrontier_ScottsHouse_Text_ComeBackForThisLater",
    "Your BAG is full. Come back when you\\n","have room.$")

P={
 PAMPA:("PetalburgCity_House2_EventScript_Woman",),
 CENTER:("HEAL_LOCATION_FORTREE_CITY",),
 FOSSIL:("FLAG_SYS_GAME_CLEAR","FLAG_RECEIVED_REVIVED_FOSSIL_MON","ITEM_ROOT_FOSSIL"),
 SHIP:("VAR_SS_TIDAL_STATE","FLAG_MET_SCOTT_ON_SS_TIDAL","FLAG_DEFEATED_SS_TIDAL_TRAINERS"),
 SCOTT:("FLAG_SCOTT_GIVES_BATTLE_POINTS","FLAG_COLLECTED_ALL_SILVER_SYMBOLS","FLAG_COLLECTED_ALL_GOLD_SYMBOLS","DECOR_GOLD_SHIELD"),
}
def pat(l): return re.compile(rf"(?ms)^{re.escape(l)}:\n(?P<body>.*?)(?=^[A-Za-z0-9_]+(?:::|:)(?:\n|$)|\Z)")
def widths():
    for p,d in T.items():
        for l,lines in d.items():
            for line in lines:
                clean=PH.sub("PLAYER",line.replace("$",""))
                for s in CTRL.split(clean):
                    if len(s.strip())>MAX: raise ValueError(f"{p}: {l}: {len(s.strip())}: {s.strip()!r}")
def mask(text,labels):
    out=text
    for l in labels:
        m=pat(l).search(out)
        if not m: raise ValueError(f"missing {l}")
        a,b=m.span("body"); out=out[:a]+'\t.string "<ARAUNA_EN>"\n\n'+out[b:]
    return out
def render(p,src):
    out=src; labels=tuple(T[p])
    for l,lines in T[p].items():
        ms=list(pat(l).finditer(out))
        if len(ms)!=1: raise ValueError(f"{p}: {l}: expected 1 got {len(ms)}")
        body="".join(f'\t.string "{x}"\n' for x in lines)+"\n"; a,b=ms[0].span("body"); out=out[:a]+body+out[b:]
    if mask(src,labels)!=mask(out,labels): raise ValueError(f"{p}: non-dialogue structure changed")
    for token in P[p]:
        if token not in out: raise ValueError(f"{p}: missing {token}")
    return out
def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--check",action="store_true"); ap.add_argument("--in-place",action="store_true"); a=ap.parse_args()
    if a.check and a.in_place: ap.error("choose --check or --in-place")
    widths(); total=sum(map(len,T.values())); changed=0
    for rel in T:
        p=ROOT/rel; src=p.read_text(encoding="utf-8"); out=render(rel,src)
        if out!=src:
            changed+=1
            if a.in_place:p.write_text(out,encoding="utf-8")
    print(f"Postgame/misc English renderer OK: {total} blocks across {len(T)} files; {changed} changed.")
    return 0
if __name__=="__main__": raise SystemExit(main())
