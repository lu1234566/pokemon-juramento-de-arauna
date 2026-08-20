#!/usr/bin/env python3
from __future__ import annotations
import argparse,re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
MAX=32; CTRL=re.compile(r"\\[npl]"); PH=re.compile(r"\{[^}]+\}")
T:dict[str,dict[str,tuple[str,...]]]={}
def add(p,l,*x): T.setdefault(p,{})[l]=x

MC="data/maps/MossdeepCity/scripts.inc"
add(MC,"MossdeepCity_Text_WantKingsRockStevenGaveMe",
    "A traveler named SEU BENTO gave me\\n","this strange rock. Want it?$")
add(MC,"MossdeepCity_Text_YouCanKeepIt",
    "You can keep it.\\p","SEU BENTO said objects matter when\\n","someone remembers their story.$")
add(MC,"MossdeepCity_Text_StevensHouseOverThere",
    "SEU BENTO keeps notebooks in the\\n","house over there when he visits.$")
add(MC,"MossdeepCity_Text_WailmerWatching",
    "Wild WAILMER gather near\\n","MISSOES DO CEU.\\p","People here watch them between\\n","communication launches.$")
add(MC,"MossdeepCity_Text_SpaceCenterReceivedLetter",
    "MISSOES DO CEU received a warning\\n","about the regional network.\\p","Everyone is watching the center.$")
add(MC,"MossdeepCity_Text_SpaceCenterLaunchingRockets",
    "MISSOES DO CEU is transmitting\\n","again. The center is secure.$")
add(MC,"MossdeepCity_Text_MossdeepTargetedByMagma",
    "The REMEMBRANCERS are gathering at\\n","MISSOES DO CEU.\\p","They say HORIZON will use the network\\n","to expand the LIVING ARCHIVE.$")
add(MC,"MossdeepCity_Text_GymSign",
    "MISSOES DO CEU GYM\\n","LEADERS: CECILIA & CAETANO\\p","Every star has witnesses.$")
add(MC,"MossdeepCity_Text_CitySign",
    "MISSOES DO CEU\\p","HORIZON wants the regional network\\n","to expand the LIVING ARCHIVE.$")
add(MC,"MossdeepCity_Text_SpaceCenterSign",
    "MISSOES DO CEU\\n","REGIONAL COMMUNICATION CENTER$")
add(MC,"MossdeepCity_Text_ScottSomethingWrongWithTown",
    "SEU BENTO: The warning letter is\\n","not rumor.\\p","The REMEMBRANCERS came because the\\n","network can copy more than voices.\\p","Watch what everyone chooses to keep.$")
add(MC,"MossdeepCity_Text_SootopolisNewGymLeader",
    "The GYM at AGUAS DE M'BOI is led\\n","by DONA CELINA now.\\p","People say she teaches when to hold\\n","on and when to let water pass.$")

MG="data/maps/MossdeepCity_Gym/scripts.inc"
add(MG,"MossdeepCity_Gym_Text_GymGuideAdvice",
    "CECILIA and CAETANO lead this GYM.\\p",
    "They use PSYCHIC POKéMON and battle\\n","together. Bring at least two.$")
add(MG,"MossdeepCity_Gym_Text_GymGuidePostVictory",
    "Two leaders, one victory.\\p","The PRISM BADGE is yours.$")
add(MG,"MossdeepCity_Gym_Text_TateAndLizaIntro",
    "CECILIA: From above, cities look\\n","small.\\p","CAETANO: The lives inside them\\n","never are.\\p","CECILIA: We battle as witnesses.$")
add(MG,"MossdeepCity_Gym_Text_TateAndLizaDefeat",
    "CAETANO: Two views were not enough.\\p","CECILIA: Yours changed the pattern.$")
add(MG,"MossdeepCity_Gym_Text_ReceivedMindBadge",
    "{PLAYER} received the PRISM BADGE\\n","from CECILIA and CAETANO.$")
add(MG,"MossdeepCity_Gym_Text_ExplainMindBadgeTakeThis",
    "The PRISM BADGE raises SP. ATK and\\n","SP. DEF.\\p","It also lets you use DIVE outside\\n","battle. Take this TM.$")
add(MG,"MossdeepCity_Gym_Text_ExplainCalmMind",
    "This TM contains CALM MIND.\\p","It raises SP. ATK and SP. DEF by\\n","steadying the user's focus.$")
add(MG,"MossdeepCity_Gym_Text_RegisteredTateAndLiza",
    "Registered CECILIA & CAETANO\\n","in the POKéNAV.$")
add(MG,"MossdeepCity_Gym_Text_TateAndLizaPostBattle",
    "CECILIA: A record needs context.\\p","CAETANO: A witness needs humility.$")
add(MG,"MossdeepCity_Gym_Text_TateAndLizaNeedTwoMons",
    "CECILIA: This is a DOUBLE BATTLE.\\p","Bring at least two POKéMON.$")
add(MG,"MossdeepCity_Gym_Text_GymStatue","MISSOES DO CEU POKéMON GYM$")
add(MG,"MossdeepCity_Gym_Text_GymStatueCertified",
    "MISSOES DO CEU POKéMON GYM\\p","CECILIA & CAETANO CERTIFIED:\\n","{PLAYER}$")
add(MG,"MossdeepCity_Gym_Text_TateAndLizaPreRematch",
    "CAETANO: Same sky, new positions.\\p","CECILIA: Show us what changed.$")
add(MG,"MossdeepCity_Gym_Text_TateAndLizaRematchDefeat",
    "CECILIA: The pattern changed again.$")
add(MG,"MossdeepCity_Gym_Text_TateAndLizaPostRematch",
    "CAETANO: No observation is final.\\p","CECILIA: Keep looking.$")
add(MG,"MossdeepCity_Gym_Text_TateAndLizaRematchNeedTwoMons",
    "CECILIA: Bring at least two POKéMON\\n","for our rematch.$")

SG="data/maps/SootopolisCity_Gym_1F/scripts.inc"
add(SG,"SootopolisCity_Gym_1F_Text_GymGuideAdvice",
    "AGUAS DE M'BOI's leader is\\n","DONA CELINA.\\p","She uses WATER POKéMON.\\p","Cross each ice floor without\\n","stepping on a tile twice.$")
add(SG,"SootopolisCity_Gym_1F_Text_GymGuidePostVictory",
    "You defeated DONA CELINA.\\p","Check your TRAINER CARD. If all\\n","eight BADGES are there, the final\\n","road is open.$")
add(SG,"SootopolisCity_Gym_1F_Text_JuanIntro",
    "DONA CELINA: Living means learning\\n","what to keep and what to release.\\p","Choosing that for someone else is\\n","not ours to do. Show me your choice.$")
add(SG,"SootopolisCity_Gym_1F_Text_JuanDefeat",
    "DONA CELINA: You knew when to hold\\n","and when to let the current pass.$")
add(SG,"SootopolisCity_Gym_1F_Text_ReceivedRainBadge",
    "{PLAYER} received the SPRING BADGE\\n","from DONA CELINA.$")
add(SG,"SootopolisCity_Gym_1F_Text_ExplainRainBadgeTakeThis",
    "The SPRING BADGE makes all POKéMON\\n","obey you.\\p","It also lets you use WATERFALL\\n","outside battle. Take this TM.$")
add(SG,"SootopolisCity_Gym_1F_Text_RegisteredJuan",
    "Registered GYM LEADER DONA CELINA\\n","in the POKéNAV.$")
add(SG,"SootopolisCity_Gym_1F_Text_JuanPostBattle",
    "DONA CELINA: Memory needs movement\\n","as much as it needs a shore.$")
add(SG,"SootopolisCity_Gym_1F_Text_GoGetFortreeBadge",
    "One required BADGE is still missing.\\p","Return to MATA DO MEIO and challenge\\n","LIDIA before the final road.$")
add(SG,"SootopolisCity_Gym_1F_Text_GymStatue","AGUAS DE M'BOI POKéMON GYM$")
add(SG,"SootopolisCity_Gym_1F_Text_GymStatueCertified",
    "AGUAS DE M'BOI POKéMON GYM\\p","DONA CELINA CERTIFIED:\\n","{PLAYER}$")
add(SG,"SootopolisCity_Gym_1F_Text_JuanPreRematch",
    "DONA CELINA: Water returns, but not\\n","as the same water. Ready?$")
add(SG,"SootopolisCity_Gym_1F_Text_JuanRematchDefeat",
    "DONA CELINA: The current changed.$")
add(SG,"SootopolisCity_Gym_1F_Text_JuanPostRematch",
    "DONA CELINA: Keep what helps you\\n","remember. Release what only binds.$")
add(SG,"SootopolisCity_Gym_1F_Text_JuanRematchNeedTwoMons",
    "DONA CELINA: Bring at least two\\n","POKéMON for a rematch.$")

P={MC:("VAR_MOSSDEEP_CITY_STATE","FLAG_VISITED_MOSSDEEP_CITY","VAR_SCOTT_STATE"),MG:("TRAINER_TATE_AND_LIZA_1","FLAG_BADGE07_GET","ITEM_TM_CALM_MIND"),SG:("TRAINER_JUAN_1","FLAG_BADGE08_GET","ITEM_TM_WATER_PULSE","VAR_ICE_STEP_COUNT")}
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
    print(f"Prism/Spring English renderer OK: {total} blocks across {len(T)} files; {changed} changed.")
    return 0
if __name__=="__main__": raise SystemExit(main())
