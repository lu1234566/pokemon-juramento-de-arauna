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
    "ELIAS: Some guilt stays.\\n","Silence does not erase it.\\p",
    "I approved part of M'BOI.\\n","For years, I called it prudence.$")
add(PAMPA,"PetalburgCity_House2_Text_BattledNormanOnce",
    "ELIAS: Being your father\\n","gave me no right to hide truth.\\p",
    "It took me too long to learn.$")

CENTER="data/maps/FortreeCity_PokemonCenter_1F/scripts.inc"
add(CENTER,"FortreeCity_PokemonCenter_1F_Text_GoToSafariZone",
    "Building a POKéDEX?\\p",
    "Visit the SAFARI ZONE.\\n","You may find rare POKéMON.$")
add(CENTER,"FortreeCity_PokemonCenter_1F_Text_RecordCornerIsNeat",
    "Used the RECORD CORNER?\\p",
    "It mixes TRAINER records.\\n","Strange, but interesting.$")
add(CENTER,"FortreeCity_PokemonCenter_1F_Text_DoYouKnowAboutPokenav",
    "You have a POKéNAV too!\\p",
    "MATCH CALL contacts TRAINERS\\n","you registered before.\\p",
    "It also marks rematches.\\n","HORIZON built that system.$")

FOSSIL="data/maps/Route114_FossilManiacsTunnel/scripts.inc"
add(FOSSIL,"Route114_FossilManiacsTunnel_Text_LookInDesertForFossils",
    "I'm a FOSSIL researcher.\\p",
    "I love FOSSILS. These are mine.\\p",
    "Search the desert for your own.\\p",
    "Stone and sand hide old things.$")
add(FOSSIL,"Route114_FossilManiacsTunnel_Text_DevonCorpRevivingFossils",
    "Found a FOSSIL? Beautiful.\\p",
    "HORIZON can revive some\\n","POKéMON from FOSSILS.\\p",
    "I leave mine as I found them.$")
add(FOSSIL,"Route114_FossilManiacsTunnel_Text_FossilsAreWonderful",
    "FOSSILS are wonderful.\\p","I could stare all day.$")
add(FOSSIL,"Route114_FossilManiacsTunnel_Text_NotSafeThatWay",
    "That way isn't safe.\\p",
    "The wall collapsed as I dug.\\n","A huge cave opened below.\\p",
    "I left it alone.\\n","There were no FOSSILS there.$")

SHIP="data/maps/SSTidalCorridor/scripts.inc"
add(SHIP,"SSTidalCorridor_Text_ScottBattleFrontierInvite",
    "{PLAYER}{KUN}! SEU BENTO here.\\p",
    "Congrats on the LEAGUE.\\p",
    "I want to see you handle\\n","CIRCUITO DE BATALHA.\\p",
    "I spoke with the crew.\\n","This ferry can take you there.\\p",
    "I'll be waiting.$")
add(SHIP,"SSTidal_Text_FastCurrentsHopeYouEnjoyVoyage",
    "This ferry crosses hard seas\\n","without losing its course.\\p",
    "Enjoy the voyage aboard.$")
add(SHIP,"SSTidal_Text_HopeYouEnjoyVoyage","We hope you enjoy the voyage.$")
add(SHIP,"SSTidal_Text_MadeLandInSlateport",
    "We arrived at PORTO DO SAL.\\p","Thanks for sailing with us.$")
add(SHIP,"SSTidal_Text_MadeLandInLilycove",
    "We arrived at BAIA DAS LUZES.\\p","Thanks for sailing with us.$")
add(SHIP,"SSTidalCorridor_Text_CanRestInCabin2",
    "We still have some way to go.\\p",
    "Rest in Cabin 2 if you want.$")
add(SHIP,"SSTidalCorridor_Text_WeveArrived","We have arrived!$")
add(SHIP,"SSTidalCorridor_Text_VisitOtherCabins",
    "Visit the other cabins.\\p",
    "Some TRAINERS may want\\n","a battle.$")
add(SHIP,"SSTidalCorridor_Text_EnjoyYourCruise","Enjoy the voyage!$")
add(SHIP,"SSTidalCorridor_Text_HorizonSpreadsBeyondPorthole",
    "The horizon lies beyond\\n","the porthole.$")
add(SHIP,"SSTidalCorridor_Text_BrineyWelcomeAboard",
    "CAPTAIN: Welcome, {PLAYER}{KUN}!\\p",
    "They gave me this ferry.\\p",
    "I had left the sea.\\n","A ship can wake an old sailor.$")
for i in range(1,5): add(SHIP,f"SSTidalCorridor_Text_Cabin{i}",f"Cabin {i}$")

SCOTT="data/maps/BattleFrontier_ScottsHouse/scripts.inc"
add(SCOTT,"BattleFrontier_ScottsHouse_Text_WelcomeToBattleFrontier",
    "SEU BENTO: So you came.\\p",
    "This place is not huge,\\n","but its challenge is serious.\\p",
    "{PLAYER}{KUN}, welcome to\\n","CIRCUITO DE BATALHA.\\p",
    "It took years to gather\\n","the people who run it.$")
add(SCOTT,"BattleFrontier_ScottsHouse_Text_HowMuchEffortItTookToMakeReal",
    "I traveled alone at first,\\n","seeking steady TRAINERS.\\p",
    "It was a long road.\\n","This place grew from it.$")
add(SCOTT,"BattleFrontier_ScottsHouse_Text_HaveThisAsMementoOfOurPathsCrossing",
    "The past brought us here.\\p",
    "I won't decorate that truth.\\p",
    "Fight with what you learned.\\p",
    "{PLAYER}{KUN}, take this mark\\n","of where our paths crossed.$")
add(SCOTT,"BattleFrontier_ScottsHouse_Text_ObtainedXBattlePoints",
    "{PLAYER} received {STR_VAR_1}\\n","Battle Point(s).$")
add(SCOTT,"BattleFrontier_ScottsHouse_Text_ExplainBattlePoints",
    "SEU BENTO: Your Battle Points\\n","are stored on the CIRCUIT PASS.\\p",
    "Better results earn more.\\p",
    "Trade them for useful items\\n","when you think it is worth it.$")
add(SCOTT,"BattleFrontier_ScottsHouse_Text_ExpectingGreatThings",
    "I want to see how far you go!$")
add(SCOTT,"BattleFrontier_ScottsHouse_Text_WhyIGoSeekingTrainers",
    "SEU BENTO: Every TRAINER\\n","carries a different story.\\p",
    "Excuses do not change\\n","a battle's result.\\p",
    "I seek people willing\\n","to be tested here.$")
add(SCOTT,"BattleFrontier_ScottsHouse_Text_HaveYouMetFrontierBrain",
    "SEU BENTO: Met a CIRCUIT\\n","MASTER yet?\\p",
    "Earned any SYMBOLS?\\p",
    "I chose each MASTER\\n","because they do not go easy.$")
add(SCOTT,"BattleFrontier_ScottsHouse_Text_MayFindWildMonsInFrontier",
    "SEU BENTO: Filling the POKéDEX?\\p",
    "Explore the CIRCUITO.\\p",
    "Wild POKéMON may appear\\n","where you least expect them.$")
add(SCOTT,"BattleFrontier_ScottsHouse_Text_YouveCollectedAllSilverSymbols",
    "SEU BENTO: Let me see that PASS.\\p",
    "Every SILVER SYMBOL.\\p",
    "That is no small feat.\\n","You earned this reward.$")
add(SCOTT,"BattleFrontier_ScottsHouse_Text_YouveCollectedAllGoldSymbols",
    "SEU BENTO: All GOLD SYMBOLS.\\p",
    "Few TRAINERS get this far.\\p",
    "{PLAYER}, take this.\\n","You'll value it.$")
add(SCOTT,"BattleFrontier_ScottsHouse_Text_SoGladIBroughtYouHere",
    "I knew you'd cause trouble\\n","when we first met.\\p",
    "I'm glad I brought you here.$")
add(SCOTT,"BattleFrontier_ScottsHouse_Text_BerryPocketStuffed",
    "Your BERRY pocket is full.$")
add(SCOTT,"BattleFrontier_ScottsHouse_Text_Beat50TrainersInARow",
    "SEU BENTO: Fifty straight wins\\n","in BATTLE TOWER?\\p","Not bad. Take this.$")
add(SCOTT,"BattleFrontier_ScottsHouse_Text_Beat100TrainersInARow",
    "SEU BENTO: One hundred wins\\n","in BATTLE TOWER?\\p",
    "Now you're raising the stakes.\\n","Take this.$")
add(SCOTT,"BattleFrontier_ScottsHouse_Text_ExpectingToHearEvenGreaterThings",
    "I expect even bigger news\\n","from you.$")
add(SCOTT,"BattleFrontier_ScottsHouse_Text_ComeBackForThisLater",
    "Your BAG is full.\\n","Come back with room.$")

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
