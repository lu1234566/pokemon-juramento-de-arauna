#!/usr/bin/env python3
from __future__ import annotations
import argparse,re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
MAX=32; CTRL=re.compile(r"\\[npl]"); PH=re.compile(r"\{[^}]+\}")
T:dict[str,dict[str,tuple[str,...]]]={}
def add(p,l,*x): T.setdefault(p,{})[l]=x

R1="data/maps/SeafloorCavern_Room1/scripts.inc"
add(R1,"SeafloorCavern_Room1_Text_Grunt1Intro",
    "You should not have reached the\\n","chambers of M'BOI.\\p",
    "While OTACILIO is below, nobody\\n","gets through.$")
add(R1,"SeafloorCavern_Room1_Text_Grunt1Defeat","Damn... You got past me.$")
add(R1,"SeafloorCavern_Room1_Text_Grunt1PostBattle",
    "OTACILIO believes some memories\\n","only keep hurting people.\\p",
    "I won't pretend I understand it all.$")
add(R1,"SeafloorCavern_Room1_Text_Grunt2Intro",
    "These caves react to things our\\n","sensors cannot read.\\p",
    "Do not come any closer.$")
add(R1,"SeafloorCavern_Room1_Text_Grunt2Defeat","So even that didn't stop you...$")
add(R1,"SeafloorCavern_Room1_Text_Grunt2PostBattle",
    "The deeper we go, the less the\\n","ARCHIVE obeys.\\p",
    "Maybe it was never really a tool.$")

R3="data/maps/SeafloorCavern_Room3/scripts.inc"
add(R3,"SeafloorCavern_Room3_Text_ShellyIntro",
    "MARTA: OTACILIO is near the core.\\p",
    "I won't let you interrupt everything\\n","now.$")
add(R3,"SeafloorCavern_Room3_Text_ShellyDefeat",
    "MARTA: Heh... You're worse than the\\n","reports said.$")
add(R3,"SeafloorCavern_Room3_Text_ShellyPostBattle",
    "MARTA: Don't confuse obedience with\\n","certainty.\\p",
    "I follow OTACILIO because I saw what\\n","memories can do.$")
add(R3,"SeafloorCavern_Room3_Text_Grunt5Intro",
    "MARTA ordered me to guard this route.\\p",
    "If you want through, try your luck.$")
add(R3,"SeafloorCavern_Room3_Text_Grunt5Defeat",
    "I should have stayed with reports...$")
add(R3,"SeafloorCavern_Room3_Text_Grunt5PostBattle",
    "The ARCHIVE became unstable after we\\n","descended into M'BOI.\\p",
    "OTACILIO keeps going anyway.$")

R4="data/maps/SeafloorCavern_Room4/scripts.inc"
add(R4,"SeafloorCavern_Room4_Text_Grunt3Intro",
    "Below here, the ARCHIVE stops\\n","responding properly.\\p",
    "This is no place for curiosity.$")
add(R4,"SeafloorCavern_Room4_Text_Grunt3Defeat","You're really going to continue?$")
add(R4,"SeafloorCavern_Room4_Text_Grunt3PostBattle",
    "Recordings here mix evacuation,\\n","rescue and silence.\\p",
    "Maybe that is why OTACILIO came\\n","personally.$")
add(R4,"SeafloorCavern_Room4_Text_Grunt4Intro",
    "The core is just ahead.\\p",
    "One more step and I stop you.$")
add(R4,"SeafloorCavern_Room4_Text_Grunt4Defeat","I failed to protect the passage.$")
add(R4,"SeafloorCavern_Room4_Text_Grunt4PostBattle",
    "The sensors lost their reading.\\p",
    "If something wakes below, nobody\\n","knows what happens next.$")

CH="data/maps/EverGrandeCity_ChampionsRoom/scripts.inc"
add(CH,"EverGrandeCity_ChampionsRoom_Text_IntroSpeech",
    "AMALIA: The LEAGUE can no longer\\n","call silence order.\\p",
    "If you came this far, show me what\\n","Arauna made of you.$")
add(CH,"EverGrandeCity_ChampionsRoom_Text_Defeat",
    "AMALIA: So this is how Arauna changes\\n","hands...\\p",
    "You won without asking the past to\\n","disappear.$")
add(CH,"EverGrandeCity_ChampionsRoom_Text_PostBattleSpeech",
    "AMALIA: The title is yours now.\\p",
    "A title erases nothing.\\p",
    "It only adds weight to what you\\n","choose to remember.$")
for label in ("MayAdvice","BrendanAdvice"):
    add(CH,f"EverGrandeCity_ChampionsRoom_Text_{label}",
        "CIRO: {PLAYER}! I came to tell you\\n","one thing before the battle...\\p",
        "Use everything you learned.\\p",
        "And don't fight to prove anything\\n","to me.$")
for label in ("MayItsAlreadyOver","BrendanYouveWon"):
    add(CH,f"EverGrandeCity_ChampionsRoom_Text_{label}",
        "CIRO: ...Wait.\\p",
        "It's already over? You beat AMALIA?\\p",
        "Of course you did. I should have\\n","arrived five minutes earlier.$")
add(CH,"EverGrandeCity_ChampionsRoom_Text_BirchArriveRatePokedex",
    "ANAHI: I arrived late too.\\p",
    "Before any speech, let me see your\\n","POKéDEX.$")
add(CH,"EverGrandeCity_ChampionsRoom_Text_BirchCongratulations",
    "ANAHI: Excellent, {PLAYER}.\\p",
    "You went farther than any report can\\n","measure.$")
add(CH,"EverGrandeCity_ChampionsRoom_Text_WallaceComeWithMe",
    "AMALIA: {PLAYER}...\\p",
    "No. I should say this properly.\\p",
    "The LEAGUE's new name is yours.\\p",
    "Come with me.$")
add(CH,"EverGrandeCity_ChampionsRoom_Text_WallaceWaitOutside",
    "AMALIA: Ciro. Anahi. Wait here.\\p",
    "The record belongs to the one who\\n","won. We can talk afterward.$")
for label in ("MayCongratulations","BrendanCongratulations"):
    add(CH,f"EverGrandeCity_ChampionsRoom_Text_{label}",
        "CIRO: I still want to beat you.\\p",
        "But today... congratulations.\\p",
        "You earned this.$")

P={
 R1:("TRAINER_GRUNT_SEAFLOOR_CAVERN_1","TRAINER_GRUNT_SEAFLOOR_CAVERN_2"),
 R3:("TRAINER_SHELLY_SEAFLOOR_CAVERN","TRAINER_GRUNT_SEAFLOOR_CAVERN_5"),
 R4:("TRAINER_GRUNT_SEAFLOOR_CAVERN_3","TRAINER_GRUNT_SEAFLOOR_CAVERN_4"),
 CH:("TRAINER_WALLACE","ProfBirch_EventScript_RatePokedex","MAP_EVER_GRANDE_CITY_HALL_OF_FAME"),
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
    print(f"Climax/finale English renderer OK: {total} blocks across {len(T)} files; {changed} changed.")
    return 0
if __name__=="__main__": raise SystemExit(main())
