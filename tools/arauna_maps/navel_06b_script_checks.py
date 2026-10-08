"""Restricted control-flow runner for unchanged encounter/harbor event sources."""
import re
from navel_06b_common import ROOT

class Runner:
    def __init__(self):
        paths=[ROOT/'data/maps'/n/'scripts.inc' for n in ('NavelRock_Top','NavelRock_Bottom','NavelRock_Harbor','LilycoveCity_Harbor')]+[ROOT/'data/event_scripts.s']
        self.labels={};self.lines=[]
        for p in paths:
            for line in p.read_text().splitlines():
                line=line.split('@')[0].strip();m=re.fullmatch(r'(\w+):{1,2}',line)
                if m:self.labels[m[1]]=len(self.lines)
                elif line:self.lines.append(line)
        self.flags=set();self.vars={};self.removed=[];self.moves=[];self.warps=[];self.mon=None;self.specials=[]
    def value(self,x):
        if x.startswith('VAR_'):return self.vars.get(x,0)
        try:return int(x,0)
        except ValueError:return x
    def run(self,label,outcome='B_OUTCOME_CAUGHT',answer='YES'):
        pc=self.labels[label];stack=[]
        skip_calls={'Common_EventScript_FerryDepartIsland','LilycoveCity_Harbor_EventScript_BoardFerry','LilycoveCity_Harbor_EventScript_BoardFerryWithSailor'}
        ignored={'lock','lockall','release','releaseall','faceplayer','waitse','delay','playse','playmoncry','waitmoncry','doweather','waitmovement','waitstate','closemessage','hideobjectat','fadescreenswapbuffers','bufferspeciesname'}
        for _ in range(1000):
            line=self.lines[pc];pc+=1;parts=line.split(None,1);op=parts[0];args=[x.strip() for x in parts[1].split(',')] if len(parts)>1 else []
            if op=='end':return
            if op=='return':
                if not stack:return
                pc=stack.pop();continue
            if op in ('call','goto') or op.startswith(('call_if_','goto_if_')):
                selected=True;dest=args[-1]
                if '_if_' in op:
                    condition=op.split('_if_')[1]
                    if condition in ('set','unset'):selected=(args[0] in self.flags)==(condition=='set')
                    elif condition in ('eq','ne'):selected=(self.value(args[0])==self.value(args[1]))==(condition=='eq')
                    else:raise AssertionError(line)
                if selected:
                    if dest in skip_calls:assert op.startswith('call');continue
                    if op.startswith('call'):stack.append(pc)
                    pc=self.labels[dest]
                continue
            if op=='setflag':self.flags.add(args[0])
            elif op=='clearflag':self.flags.discard(args[0])
            elif op=='setvar':self.vars[args[0]]=self.value(args[1])
            elif op=='specialvar':assert args[1]=='GetBattleOutcome';self.vars[args[0]]=outcome
            elif op=='removeobject':self.removed.append(self.value(args[0]))
            elif op=='seteventmon':self.mon=(args[0],int(args[1]))
            elif op=='applymovement':self.moves.append(tuple(args))
            elif op=='warp':self.warps.append(tuple(args))
            elif op=='setweather':self.vars['weather']=args[0]
            elif op=='special':self.specials.append(args[0])
            elif op=='msgbox':
                if args[-1]=='MSGBOX_YESNO':self.vars['VAR_RESULT']=answer
            elif op not in ignored:raise AssertionError('Unsupported opcode in tested fragment: '+line)
        raise AssertionError('Event fragment exceeded instruction guard')

def checks():
    count=0
    for map_name,species,local in (('NavelRock_Top','HO_OH','HoOh'),('NavelRock_Bottom','LUGIA','Lugia')):
        for caught in (0,1):
            for defeated in (0,1):
                for hidden in (0,1):
                    r=Runner();hide='FLAG_HIDE_'+species
                    if caught:r.flags.add('FLAG_CAUGHT_'+species)
                    if defeated:r.flags.add('FLAG_DEFEATED_'+species)
                    if hidden:r.flags.add(hide)
                    r.run(map_name+'_OnTransition');assert (hide in r.flags)==bool(caught or (defeated and hidden))
                    if species=='HO_OH':assert r.vars['VAR_TEMP_1']==int(bool(caught or defeated))
                    count+=1
        for outcome in ('B_OUTCOME_WON','B_OUTCOME_RAN','B_OUTCOME_PLAYER_TELEPORTED','B_OUTCOME_CAUGHT'):
            r=Runner();r.vars['VAR_LAST_TALKED']='LOCALID_NAVEL_ROCK_'+species.replace('_','')
            r.run(map_name+'_EventScript_'+local,outcome);assert r.mon==('SPECIES_'+species,70)
            assert ('FLAG_CAUGHT_'+species in r.flags)==(outcome=='B_OUTCOME_CAUGHT')
            assert ('FLAG_DEFEATED_'+species in r.flags)==(outcome=='B_OUTCOME_WON')
            assert 'FLAG_SYS_CTRL_OBJ_DELETE' not in r.flags and 'BattleSetup_StartLegendaryBattle' in r.specials
            if species=='HO_OH':assert 'SpawnCameraObject' in r.specials and 'RemoveCameraObject' in r.specials and r.vars['weather']=='WEATHER_NONE'
            else:assert r.specials.count('ShakeCamera')==2
            count+=1
        for delete in (0,1):
            for outcome in ('B_OUTCOME_WON','B_OUTCOME_CAUGHT'):
                r=Runner()
                if delete:r.flags.add('FLAG_SYS_CTRL_OBJ_DELETE')
                r.run(map_name+'_OnResume',outcome);assert len(r.removed)==int(bool(delete and outcome=='B_OUTCOME_CAUGHT'));count+=1
    for answer in ('YES','NO'):
        r=Runner();r.run('NavelRock_Harbor_EventScript_Sailor',answer=answer)
        assert r.warps==([('MAP_LILYCOVE_CITY_HARBOR','8','11')] if answer=='YES' else []);count+=1
    for label in ('LilycoveCity_Harbor_EventScript_GoToNavelRock','LilycoveCity_Harbor_EventScript_GoToNavelRockFirstTime'):
        r=Runner();r.run(label);assert r.warps==[('MAP_NAVEL_ROCK_HARBOR','8','4')];count+=1
    return {'status':'PASS','event_fragment_cases':count,'encounter_slots':['SPECIES_HO_OH','SPECIES_LUGIA'],'level':70,'ferry_arrival':[8,4],'ferry_return':[8,11],'scope':'Restricted runner of control-flow/flag commands in original event sources. Battle outcome, message answer, camera/movement services and ferry animation calls are fixtures. Not the full ROM script interpreter, battle or camera engine.'}
