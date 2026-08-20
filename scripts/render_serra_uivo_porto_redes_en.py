#!/usr/bin/env python3
from __future__ import annotations
import argparse, re
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
MAX=32
CTRL=re.compile(r"\\[npl]")
PH=re.compile(r"\{[^}]+\}")
T: dict[str,dict[str,tuple[str,...]]]={}
def A(path,label,*lines): T.setdefault(path,{})[label]=lines

RC="data/maps/RustboroCity/scripts.inc"
A(RC,"RustboroCity_Text_WeShortenItToDevon","HORIZON keeps a technical\\n","center in SERRA DO UIVO.\\p","Many families depend on it.\\p","Not everyone trusts what the\\n","center is measuring.$")
A(RC,"RustboroCity_Text_OutOfTheWay","HORIZON AGENT: Move.\\p","This RESEARCH CASE is being\\n","recalled by central command.$")
A(RC,"RustboroCity_Text_WaitDontTakeMyGoods","EMPLOYEE: Wait!\\p","That recall was never approved\\n","by this center!$")
A(RC,"RustboroCity_Text_HelpMeIWasRobbed","EMPLOYEE: It's you!\\p","A HORIZON agent took our\\n","RESEARCH CASE under a recall.\\p","Nobody here authorized it.\\p","Please recover those records.$")
A(RC,"RustboroCity_Text_ShadyCharacterTookOffTowardsTunnel","The agent ran toward\\n","GALERIAS DA SERRA.$")
A(RC,"RustboroCity_Text_YouGotItThankYou","EMPLOYEE: You recovered it!\\p","The seals are intact. Good.\\p","Take this GREAT BALL too.$")
A(RC,"RustboroCity_Text_PleaseComeWithMe","Please come with me.\\p","Our director needs to see\\n","what you brought back.$")
A(RC,"RustboroCity_Text_TunnelNearingCompletion","GALERIAS DA SERRA\\p","WORK HALTED.\\p","BOND readings remain unstable.$")
A(RC,"RustboroCity_Text_DevonCorpSign","HORIZON CONSORTIUM\\p","SERRA DO UIVO FIELD CENTER.$")
A(RC,"RustboroCity_Text_GymSign","SERRA DO UIVO GYM\\n","LEADER: DALVA\\p","The mountain remembers.$")
A(RC,"RustboroCity_Text_DevonCorpBranchOfficeSign","HORIZON CONSORTIUM\\p","AUTHORIZED PERSONNEL ONLY.$")
A(RC,"RustboroCity_Text_CitySign","SERRA DO UIVO\\p","HORIZON brought jobs and roads.\\p","It also brought machines that\\n","measure BONDS.$")
A(RC,"RustboroCity_Text_HaveYouChallengedGym","Have you challenged DALVA?\\p","Her GYM tests patience and\\n","ROCK POKéMON.$")
A(RC,"RustboroCity_Text_HeyThatsRustborosGymBadge","That's the RIFT BADGE!\\p","DALVA does not give that mark\\n","to unchanged challengers.$")
A(RC,"RustboroCity_Text_YoureNewAroundHere","You're new to SERRA DO UIVO.\\p","HORIZON changed this town fast.$")
A(RC,"RustboroCity_Text_GymLeaderIsntEasyWithFire","DALVA trains ROCK POKéMON.\\p","My FIRE team learned patience.$")
for who,reg,no in (("May","RegisteredMay","MayOhHaventRaisedPokemonEnough"),("Brendan","RegisteredBrendan","BrendanNoConfidenceInPokemon")):
    A(RC,f"RustboroCity_Text_{who}HiLetsRegister","CIRO: Your POKéNAV takes\\n","contacts now, right?\\p","Register mine. I want data from\\n","the same roads you see.$")
    A(RC,f"RustboroCity_Text_{reg}","CIRO was registered in\\n","the POKéNAV.$")
    A(RC,f"RustboroCity_Text_{who}PassedBrineyWantToBattle","CIRO: HORIZON says BOND loss\\n","can be measured.\\p","Can instinct beat a model?\\p","Battle me?$" )
    A(RC,f"RustboroCity_Text_{no}","CIRO: Then not now.\\p","A forced result teaches nothing.$")
    A(RC,f"RustboroCity_Text_{who}WantToBattle","CIRO: One clean battle.\\p","Let's see what the sensors miss.$")
    intro="MayImNotGoingToLose" if who=="May" else "BrendanIWontGoEasy"
    A(RC,f"RustboroCity_Text_{intro}","CIRO: If the model is right,\\n","this should be predictable.\\p","Prove it isn't.$")
    A(RC,f"RustboroCity_Text_{who}Defeat","CIRO: That result doesn't fit.\\p","Either the sensor missed\\n","something, or I did.$")
    A(RC,f"RustboroCity_Text_{who}MrBrineyHint","CIRO: The veteran sailor can\\n","take you to PORTO DAS REDES.\\p","I have my own route.$")

RG="data/maps/RustboroCity_Gym/scripts.inc"
A(RG,"RustboroCity_Gym_Text_GymGuideAdvice","SERRA DO UIVO's leader is DALVA.\\p","She uses ROCK POKéMON.\\p","WATER and GRASS can help.\\p","Defeat her for your first BADGE.$")
A(RG,"RustboroCity_Gym_Text_GymGuidePostVictory","Your RIFT BADGE is now shown\\n","on the TRAINER CARD.$")
A(RG,"RustboroCity_Gym_Text_RoxanneIntro","DALVA: Stone keeps pressure\\n","inside every crack.\\p","A mark proves what happened.\\p","Show me what you leave behind.$")
A(RG,"RustboroCity_Gym_Text_RoxanneDefeat","DALVA: You changed the mark's\\n","direction. Good.$")
A(RG,"RustboroCity_Gym_Text_ReceivedStoneBadge","{PLAYER} received the\\n","RIFT BADGE from DALVA.$")
A(RG,"RustboroCity_Gym_Text_StoneBadgeInfoTakeThis","The RIFT BADGE raises ATTACK.\\p","It also lets you use CUT\\n","outside battle.\\p","Take this TM as well.$")
A(RG,"RustboroCity_Gym_Text_RoxannePostBattle","DALVA: A crack can become a path\\n","if you learn to read it.$")
A(RG,"RustboroCity_Gym_Text_GymStatue","SERRA DO UIVO POKéMON GYM$")
A(RG,"RustboroCity_Gym_Text_GymStatueCertified","SERRA DO UIVO POKéMON GYM\\p","DALVA'S CERTIFIED TRAINERS:\\n","{PLAYER}$")
A(RG,"RustboroCity_Gym_Text_RegisteredRoxanne","Registered GYM LEADER DALVA\\n","in the POKéNAV.$")
for suf,msg in {
"RoxannePreRematch":("DALVA: Old stone changes too.\\p","Neither of us is the same. Go.$"),
"RoxanneRematchDefeat":("DALVA: Another mark worth\\n","remembering.$"),
"RoxannePostRematch":("DALVA: Return when your road\\n","changes you again.$"),
"RoxanneRematchNeedTwoMons":("DALVA: Bring at least two\\n","POKéMON for a rematch.$")}.items(): A(RG,"RustboroCity_Gym_Text_"+suf,*msg)

D3="data/maps/RustboroCity_DevonCorp_3F/scripts.inc"
A(D3,"RustboroCity_DevonCorp_3F_Text_MrStoneIHaveFavor","DIRECTOR: I run this HORIZON\\n","field center.\\p","The agent used a central recall\\n","we did not approve.\\p","Take the RESEARCH CASE to the\\n","PORTO DO SAL SHIPYARD.\\p","Take this LETTER to SEU BENTO\\n","in GRUTA DAS VOZES too.$")
A(D3,"RustboroCity_DevonCorp_3F_Text_MrStoneWantYouToHaveThis","DIRECTOR: Take this POKéNAV.\\p","It is not payment for silence.\\p","Use it to check our claims.$")
A(D3,"RustboroCity_DevonCorp_3F_Text_MrStoneExplainPokenavRestUp","DIRECTOR: It maps Arauna and\\n","stores contacts and field notes.\\p","PORTO DAS REDES and PORTO DO SAL\\n","are marked. Rest before leaving.$")
A(D3,"RustboroCity_DevonCorp_3F_Text_MrStoneGoWithCautionAndCare","DIRECTOR: Travel carefully,\\n","{PLAYER}. Keep your own notes.$")
A(D3,"RustboroCity_DevonCorp_3F_Text_CountingOnYou","DIRECTOR: Keep both deliveries\\n","intact.$")
A(D3,"RustboroCity_DevonCorp_3F_Text_ThankYouForDeliveringLetter","DIRECTOR: SEU BENTO got the\\n","LETTER? Good.\\p","An independent copy now exists.\\p","Take this EXP. SHARE.$")
A(D3,"RustboroCity_DevonCorp_3F_Text_ThisIs3rdFloorWaitHere","EMPLOYEE: Third floor.\\p","Please take the RESEARCH CASE\\n","to PORTO DO SAL.\\p","After that recall, I trust you\\n","more than another courier.$")
A(D3,"RustboroCity_DevonCorp_3F_Text_WordWithPresidentComeWithMe","Our director wants to speak\\n","with you. Please come with me.$")
A(D3,"RustboroCity_DevonCorp_3F_Text_VisitCaptSternShipyard","At the PORTO DO SAL SHIPYARD,\\n","ask for the chief engineer.$")

R104="data/maps/Route104/scripts.inc"
for who in ("May","Brendan"):
    pre="WeShouldRegister" if who=="May" else "WeShouldRegister"
    A(R104,f"Route104_Text_{who}{pre}","CIRO: Register my POKéNAV.\\p","I want data from the same roads.$")
    A(R104,f"Route104_Text_Registered{who}","CIRO was registered in\\n","the POKéNAV.$")
    A(R104,f"Route104_Text_{who}HowsYourPokedex","CIRO: How much is recorded?\\p","A story matters if tested.$")
    battle="MinesDecentLetsBattle" if who=="May" else "DoingGreatLetsBattle"
    A(R104,f"Route104_Text_{who}{battle}","CIRO: My readings are clean.\\p","One more result. Battle?$")
    decline="HaventRaisedPokemon" if who=="May" else "NoConfidence"
    A(R104,f"Route104_Text_{who}{decline}","CIRO: Then later.\\p","A forced result teaches nothing.$")
    A(R104,f"Route104_Text_{who}LetsBattle","CIRO: Ready for another test?$")
    A(R104,f"Route104_Text_{who}Intro","CIRO: Same road, same setup.\\p","Begin.$")
    A(R104,f"Route104_Text_{who}Defeat","CIRO: That variance is too large\\n","to ignore.$")
    A(R104,f"Route104_Text_{who}PostBattle","CIRO: I need better assumptions,\\n","not a prettier conclusion.$")
A(R104,"Route104_Text_DadPokenavCall","ELIAS: {PLAYER}? Register this\\n","number.\\p","You need not report every step.\\p","Just know you can call.$")
A(R104,"Route104_Text_RegisteredDadInPokenav","Registered ELIAS in the POKéNAV.$")
A(R104,"Route104_Text_MrBrineysCottage","VETERAN SAILOR'S COTTAGE$")
A(R104,"Route104_Text_RouteSignPetalburg","SOUTH: PAMPA DA ESPERA$")
A(R104,"Route104_Text_RouteSignRustboro","NORTH: SERRA DO UIVO$")

R116="data/maps/Route116/scripts.inc"
A(R116,"Route116_Text_ScoundrelMadeOffWithPeeko","SAILOR: A HORIZON agent took\\n","my WINGULL into the galleries!\\p","Please help me get her back.$")
A(R116,"Route116_Text_DiggingTunnelWhenGoonOrderedMeOut","A HORIZON agent drove me out\\n","of GALERIAS DA SERRA.\\p","The POKéMON react to loud gear.\\p","If he starts it, they'll panic.$")
A(R116,"Route116_Text_GoonHightailedItOutOfTunnel","The agent ran out.\\p","I can work in the galleries.$")
A(R116,"Route116_Text_RouteSignRustboro","WEST: SERRA DO UIVO$")
A(R116,"Route116_Text_RusturfTunnelSign","GALERIAS DA SERRA$")

RT="data/maps/RusturfTunnel/scripts.inc"
A(RT,"RusturfTunnel_Text_ComeAndGetSome","HORIZON AGENT: Still coming?\\p","Then take the case yourself.$")
A(RT,"RusturfTunnel_Text_GruntIntro","HORIZON AGENT: This recall was\\n","supposed to be simple.\\p","Take the case. Clear the route.\\p","You are making both harder.$")
A(RT,"RusturfTunnel_Text_GruntDefeat","HORIZON AGENT: Central will not\\n","like this report.$")
A(RT,"RusturfTunnel_Text_GruntTakePackage","HORIZON AGENT: Fine.\\p","The field center keeps its case.\\p","I followed a central order.\\p","Ask why HORIZON fights itself.$")
A(RT,"RusturfTunnel_Text_ThankYouLetsGoHomePeeko","SAILOR: You saved my WINGULL.\\p","Thank you, {PLAYER}.\\p","Find me at my coastal cottage\\n","when you need the sea route.$")
A(RT,"RusturfTunnel_Text_ToGetToVerdanturf","The far side leads toward\\n","VALE DO SILENCIO.\\p","For now, take the coastal route.$")

DT="data/maps/DewfordTown/scripts.inc"
A(DT,"DewfordTown_Text_TinyIslandCommunity","PORTO DAS REDES is small.\\p","News moves fast between boats.$")
A(DT,"DewfordTown_Text_TownSign","PORTO DAS REDES\\p","Fishers remember a community\\n","official records erased.$")
A(DT,"DewfordTown_Text_GymSign","PORTO DAS REDES GYM\\n","LEADER: ADEMAR\\p","The sea returns stories.$")
A(DT,"DewfordTown_Text_HallSign","PORTO DAS REDES HALL\\p","CATCHES, WEATHER, STORIES, NEWS.$")
A(DT,"Route104_Text_LandedInDewfordDeliverLetter","SAILOR: PORTO DAS REDES!\\p","Take the LETTER to SEU BENTO\\n","in GRUTA DAS VOZES.$")
A(DT,"DewfordTown_Text_SetSailBackToPetalburg","SAILOR: LETTER delivered?\\p","Or sail back to PAMPA DA ESPERA?$")
A(DT,"DewfordTown_Text_PetalburgWereSettingSail2","SAILOR: PAMPA DA ESPERA it is!\\p","We're casting off.$")
A(DT,"DewfordTown_Text_GoDeliverIllBeWaiting","SAILOR: Deliver the LETTER.\\p","I'll wait here.$")
A(DT,"DewfordTown_Text_BrineyLandedInDewford","SAILOR: PORTO DAS REDES.\\p","Tell me when you need the sea.$")
A(DT,"DewfordTown_Text_WhereAreWeBound","SAILOR: The boat is ready.\\p","Where are we bound?$")
A(DT,"DewfordTown_Text_PetalburgWereSettingSail","SAILOR: PAMPA DA ESPERA?\\p","Then we cast off.$")
A(DT,"DewfordTown_Text_SlateportWereSettingSail","SAILOR: PORTO DO SAL?\\p","Then we cast off.$")
A(DT,"DewfordTown_Text_JustTellMeWhenYouNeedToSetSail","SAILOR: Tell me when you need\\n","the sea route again.$")

DG="data/maps/DewfordTown_Gym/scripts.inc"
A(DG,"DewfordTown_Gym_Text_GymGuideAdvice","PORTO DAS REDES GYM is led by\\n","ADEMAR.\\p","He uses FIGHTING POKéMON.\\p","Each victory adds more light.$")
A(DG,"DewfordTown_Gym_Text_GymGuidePostVictory","The room is bright now.\\p","The TIDE BADGE suits that path.$")
A(DG,"DewfordTown_Gym_Text_BrawlyIntro","ADEMAR: The sea returns things\\n","when it chooses.\\p","No one owns the water's memory.\\p","Show me how you keep balance.$")
A(DG,"DewfordTown_Gym_Text_BrawlyDefeat","ADEMAR: You moved with the wave\\n","instead of fighting it.$")
A(DG,"DewfordTown_Gym_Text_ReceivedKnuckleBadge","{PLAYER} received the\\n","TIDE BADGE from ADEMAR.$")
A(DG,"DewfordTown_Gym_Text_KnuckleBadgeInfoTakeThis","The TIDE BADGE makes POKéMON\\n","up to Lv. 30 obey you.\\p","It also lets you use FLASH\\n","outside battle. Take this TM.$")
A(DG,"DewfordTown_Gym_Text_RegisteredBrawly","Registered GYM LEADER ADEMAR\\n","in the POKéNAV.$")
A(DG,"DewfordTown_Gym_Text_BrawlyPostBattle","ADEMAR: Calm water can hide\\n","a strong current. Listen.$")
A(DG,"DewfordTown_Gym_Text_GymStatue","PORTO DAS REDES POKéMON GYM$")
A(DG,"DewfordTown_Gym_Text_GymStatueCertified","PORTO DAS REDES POKéMON GYM\\p","ADEMAR'S CERTIFIED TRAINERS:\\n","{PLAYER}$")
for suf,msg in {
"BrawlyPreRematch":("ADEMAR: Tides return, but never\\n","as the same water. Ready?$"),
"BrawlyRematchDefeat":("ADEMAR: You found the current\\n","again.$"),
"BrawlyPostRematch":("ADEMAR: Return when the sea\\n","teaches you something new.$"),
"BrawlyRematchNeedTwoMons":("ADEMAR: Bring at least two\\n","POKéMON for a rematch.$")}.items(): A(DG,"DewfordTown_Gym_Text_"+suf,*msg)

PRES={RC:("VAR_RUSTBORO_CITY_STATE","FLAG_DEVON_GOODS_STOLEN","FLAG_RECOVERED_DEVON_GOODS"),RG:("TRAINER_ROXANNE_1","FLAG_BADGE01_GET","ITEM_TM_ROCK_TOMB"),D3:("VAR_DEVON_CORP_3F_STATE","ITEM_LETTER","FLAG_RECEIVED_POKENAV"),R104:("VAR_BOARD_BRINEY_BOAT_STATE","FLAG_DEFEATED_RIVAL_ROUTE_104"),R116:("FLAG_RECOVERED_DEVON_GOODS","ITEM_REPEAT_BALL"),RT:("VAR_RUSTURF_TUNNEL_STATE","TRAINER_GRUNT_RUSTURF_TUNNEL","ITEM_DEVON_GOODS"),DT:("FLAG_VISITED_DEWFORD_TOWN","ITEM_OLD_ROD","FLAG_DELIVERED_STEVEN_LETTER"),DG:("TRAINER_BRAWLY_1","FLAG_BADGE02_GET","ITEM_TM_BULK_UP")}

def pat(label): return re.compile(rf"(?ms)^{re.escape(label)}:\n(?P<body>.*?)(?=^[A-Za-z0-9_]+(?:::|:)(?:\n|$)|\Z)")
def validate_widths():
    for path,d in T.items():
        for label,lines in d.items():
            for line in lines:
                clean=PH.sub("PLAYER",line.replace("$",""))
                for seg in CTRL.split(clean):
                    if len(seg.strip())>MAX: raise ValueError(f"{path}: {label}: {len(seg.strip())}: {seg.strip()!r}")
def mask(text):
    r=re.compile(r"(?ms)^(?P<label>[A-Za-z0-9_]+):\n(?P<body>(?:\t\.string .*?\n)+)")
    return r.sub(lambda m:f"{m.group('label')}:\n\t.string \"<TEXT>\"\n",text)
def render(path,src):
    out=src
    for label,lines in T[path].items():
        m=list(pat(label).finditer(out))
        if len(m)!=1: raise ValueError(f"{path}: {label}: expected 1 block, got {len(m)}")
        body="".join(f'\t.string "{x}"\n' for x in lines)+"\n"
        a,b=m[0].span("body"); out=out[:a]+body+out[b:]
    if mask(src)!=mask(out): raise ValueError(f"{path}: non-dialogue structure changed")
    for token in PRES[path]:
        if token not in out: raise ValueError(f"{path}: missing preserved token {token}")
    return out

def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--check",action="store_true"); ap.add_argument("--in-place",action="store_true"); a=ap.parse_args()
    if a.check and a.in_place: ap.error("choose --check or --in-place")
    validate_widths(); blocks=sum(map(len,T.values())); changed=0
    for rel in T:
        p=ROOT/rel; src=p.read_text(encoding="utf-8"); out=render(rel,src)
        if out!=src:
            changed+=1
            if a.in_place: p.write_text(out,encoding="utf-8")
    if a.check: print(f"Serra/Porto English renderer OK: {blocks} blocks across {len(T)} files.")
    elif a.in_place: print(f"Rendered {blocks} blocks across {changed} files.")
    else: print(f"Dry render OK: {blocks} blocks across {len(T)} files.")
    return 0
if __name__=="__main__": raise SystemExit(main())
