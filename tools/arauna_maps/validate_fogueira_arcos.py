#!/usr/bin/env python3
"""Validate the current listening circle, scene visibility and Noise Tower.

The source interpreter evaluates the repository's event commands, failing on
unknown commands. Message boxes, battles, item capacity and warps are modeled
inputs; this is NOT ARM execution, animation QA or a qualified Libras review.
"""
from __future__ import annotations
import argparse
import collections
import itertools
import json
import re
import struct
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
FOGUEIRA = ['Arauna_CasaFogueira_'+n for n in ('Entrada','Memorial','Salao')]
TOWER = ['Arauna_TorreRuido_'+n for n in ('Recepcao','Essencia','Contratos','Barragem','Sifao')]
WHEEL_FLAGS = ['FLAG_ARAUNA_FOGUEIRA_'+s for s in ('LISTENED','MEMORIAL_READ','SHARED')]
STATE='VAR_ARAUNA_FOGUEIRA_STATE'
TS='VAR_ARAUNA_TOWER_STATE'

class Scripts:
    def __init__(self):
        self.code=[];self.labels={};self.texts={}
        files=[ROOT/'data/maps'/n/'scripts.inc' for n in FOGUEIRA+TOWER+['Arauna_CasaUivo_Sala']]
        files.append(ROOT/'data/scripts/arauna_noise_tower.inc')
        files.append(ROOT/'data/maps/LittlerootTown_ProfessorBirchsLab/scripts.inc')
        for p in files:
            current=None
            source=p.read_text()
            if p.parent.name=='LittlerootTown_ProfessorBirchsLab':
                source=source[source.index('LittlerootTown_ProfessorBirchsLab_EventScript_TryGiveAuroraTicket::'):]
                source=source[:source.index('@ The twenty legends')]
            for lineno,line in enumerate(source.splitlines(),1):
                line=line.split('@',1)[0].strip()
                if not line:continue
                m=re.fullmatch(r'(\w+)::?',line)
                if m:
                    current=m[1];assert current not in self.labels,(p,current)
                    self.labels[current]=len(self.code);continue
                if line.startswith('.string '):
                    self.texts[current]=self.texts.get(current,'')+line[len('.string '):];continue
                if line.startswith('.') or line.startswith('map_script'):continue
                op,_,tail=line.partition(' ')
                self.code.append((op,[s.strip() for s in tail.split(',')],str(p.relative_to(ROOT)),lineno))
        self.labels['Common_EventScript_NopReturn']=len(self.code)
        self.code.append(('return',[], 'shared return modeled explicitly',0))

class VM:
    def __init__(self,scripts,variables=None,flags=(),defeated=(),items=(),bag_full=False):
        self.s=scripts;self.vars=dict(variables or {});self.flags=set(flags)
        self.defeated=set(defeated);self.items=list(items);self.bag_full=bag_full
    def val(self,s):
        if s in ('TRUE','YES'):return 1
        if s in ('FALSE','NO'):return 0
        try:return int(s,0)
        except ValueError:return self.vars.get(s,0) if s.startswith('VAR_') else s
    def run(self,label,answers=(),choices=(),battles=()):
        pc=self.s.labels[label];stack=[];locked=False;answers=iter(answers)
        choices=iter(choices);battles=iter(battles);seen=[];switch=0
        def jump(dest):
            assert dest in self.s.labels,('undefined label',dest,label)
            return self.s.labels[dest]
        for _ in range(1500):
            op,a,path,line=self.s.code[pc];pc+=1;seen.append(op)
            if op=='end':
                assert not locked,(label,'ended locked',path,line)
                return {'outcome':'end','commands':seen}
            if op=='return':
                if not stack:
                    assert not locked,(label,'returned locked');return {'outcome':'return','commands':seen}
                pc=stack.pop()
            elif op in ('lock','lockall'):locked=True
            elif op in ('release','releaseall'):locked=False
            elif op=='setflag':self.flags.add(a[0])
            elif op=='clearflag':self.flags.discard(a[0])
            elif op=='setvar':self.vars[a[0]]=self.val(a[1])
            elif op=='goto':pc=jump(a[0])
            elif op=='call':stack.append(pc);pc=jump(a[0])
            elif op.startswith(('goto_if_','call_if_')):
                cond=op.split('_if_')[1]
                if cond in ('set','unset'):
                    yes=(a[0] in self.flags)==(cond=='set');dest=a[1]
                elif cond=='defeated':yes=a[0] in self.defeated;dest=a[1]
                else:
                    x,y=self.val(a[0]),self.val(a[1]);dest=a[2]
                    if cond=='eq':yes=x==y
                    elif cond=='ne':yes=x!=y
                    elif cond=='lt':yes=x<y
                    elif cond=='le':yes=x<=y
                    elif cond=='gt':yes=x>y
                    elif cond=='ge':yes=x>=y
                    else:raise AssertionError(('unknown conditional',op,path,line))
                if yes:
                    if op.startswith('call'):stack.append(pc)
                    pc=jump(dest)
            elif op=='switch':switch=self.val(a[0])
            elif op=='case':
                if switch==self.val(a[0]):pc=jump(a[1])
            elif op=='msgbox':
                assert a[0] in self.s.texts or a[0]=='gText_TooBadBagIsFull',('missing text',a[0])
                if a[1]=='MSGBOX_YESNO':self.vars['VAR_RESULT']=next(answers)
            elif op=='multichoice':self.vars['VAR_RESULT']=next(choices)
            elif op=='trainerbattle_no_intro':
                outcome=next(battles)
                if outcome=='loss':return {'outcome':'whiteout','commands':seen}
                assert outcome=='win';self.defeated.add(a[0])
            elif op=='giveitem':
                self.vars['VAR_RESULT']=int(not self.bag_full)
                if not self.bag_full:self.items.append(a[0])
            elif op=='checkitem':self.vars['VAR_RESULT']=int(a[0] in self.items)
            elif op=='warp':self.last_warp=a
            elif op in ('faceplayer','closemessage','playse','fadescreen','fadescreenspeed','playmoncry','waitmoncry','applymovement','waitmovement','waitmessage','addobject','removeobject','waitstate','delay','setobjectxyperm','setobjectmovementtype','message'):
                pass # Explicitly visual/timing operations, outside this model.
            else:raise AssertionError(('unmodeled command',op,path,line,label))
        raise AssertionError(('script did not terminate',label))

def wheel(s):
    count=0;L,M,S=WHEEL_FLAGS
    labels=[e['script'] for n in FOGUEIRA for e in (json.loads((ROOT/'data/maps'/n/'map.json').read_text())['object_events']+json.loads((ROOT/'data/maps'/n/'map.json').read_text())['bg_events']) if e['script'].startswith('Arauna_CasaFogueira_')]
    for phase,badge,bits,answer in itertools.product(range(5),(False,True),itertools.product((0,1),repeat=3),(0,1)):
        flags={f for f,b in zip(WHEEL_FLAGS,bits) if b}
        if badge:flags.add('FLAG_BADGE07_GET')
        for label in labels:
            v=VM(s,{STATE:phase},flags);before=set(v.flags)
            v.run(label,answers=[1,answer] if label.endswith('_Voices') else [answer])
            expected=set(before)
            if label.endswith('_Letters') and M not in before and answer:expected.add(M)
            if label.endswith('_Voices') and answer:
                if S not in before:
                    if L not in before:expected.add(L)
                    elif M in before:expected.add(S)
            assert v.flags==expected,(phase,badge,bits,label,answer,v.flags,expected)
            assert v.vars.get(STATE)==phase and not v.items and not v.defeated
            count+=1
    for order in [('Voices','Letters','Voices'),('Letters','Voices','Voices')]:
        v=VM(s,{STATE:4},['FLAG_BADGE07_GET'])
        for event in order:
            n=FOGUEIRA[2] if event=='Voices' else FOGUEIRA[1]
            v.run(n+'_EventScript_'+event,[1,1] if event=='Voices' else [1])
        assert set(WHEEL_FLAGS)<=v.flags
    return count

def fogueira(s):
    voice=FOGUEIRA[2]+'_EventScript_Voices';tests=0
    v=VM(s,{STATE:0});v.run(voice,[0]);assert v.flags==set() and v.vars[STATE]==0
    tests+=1
    for lose_at in (None,0,1,2):
        v=VM(s,{STATE:0},['FLAG_BADGE07_GET'])
        outcomes=['win']*3
        if lose_at is not None:outcomes[lose_at]='loss'
        r=v.run(voice,[0,1],[2],outcomes)
        if lose_at is not None:
            assert r['outcome']=='whiteout' and v.vars[STATE]==1
            assert len(v.defeated)==lose_at
            v.run('Fogueira_Salao_OnTransition');assert 'FLAG_ARAUNA_FOGUEIRA_HIDE_HORIZON' not in v.flags
            v.run(voice,[0,1],battles=['win']*(3-lose_at))
        assert v.vars[STATE]==3
        tests+=1
    for hall,tower,badge,full in itertools.product((0,1),repeat=4):
        flags={f for f,b in [('FLAG_SYS_GAME_CLEAR',hall),('FLAG_ARAUNA_TOWER_COMPLETE',tower),('FLAG_BADGE08_GET',badge)] if b}
        v=VM(s,{STATE:3},flags,bag_full=bool(full));v.run(voice,[0])
        eligible=bool(hall and tower)
        assert v.vars[STATE]==(4 if eligible and not full else 3)
        assert v.items==(['ITEM_SACRED_ASH'] if eligible and not full else [])
        if eligible:
            assert 'FLAG_ARAUNA_ARAUA_AWAKENED' in v.flags
            v.bag_full=False;v.run(voice,[0]);assert v.vars[STATE]==4
            v.run(voice,[0]);assert v.items==['ITEM_SACRED_ASH']
        tests+=1
    for state in range(5):
        v=VM(s,{STATE:state},['FLAG_ARAUNA_FOGUEIRA_HIDE_HORIZON']);v.run('Fogueira_Salao_OnTransition')
        assert ('FLAG_ARAUNA_FOGUEIRA_HIDE_HORIZON' in v.flags)==(state!=1)
        tests+=1
    # Old saves already received the ash at state 4. The new ending can still
    # awaken Arauá after the Tower, without giving the old reward again.
    for hall,tower in itertools.product((0,1),repeat=2):
        flags={f for f,b in [('FLAG_SYS_GAME_CLEAR',hall),('FLAG_ARAUNA_TOWER_COMPLETE',tower)] if b}
        v=VM(s,{STATE:4},flags);v.run(voice,[0]);assert v.vars[STATE]==4 and not v.items
        assert ('FLAG_ARAUNA_ARAUA_AWAKENED' in v.flags)==bool(hall and tower)
        tests+=1
    return tests

def tower(s):
    journeys=0
    for workers,zila,custody,lots,items in itertools.product((1,2),(1,2),(1,2,3),itertools.permutations((1,2,3)),itertools.permutations(('RECORDING','DRAWING','SCHOOL','DAM_REPORT'))):
        v=VM(s,flags=['FLAG_SYS_GAME_CLEAR'])
        v.run('NoiseTower_Lobby',[1] if workers==1 else [0,1]);assert v.vars[TS]==1
        for i in lots:v.run('NoiseTower_Lot'+str(i),[1])
        assert v.vars[TS]==2
        v.run('NoiseTower_Lot'+str(lots[0]));assert v.vars[TS]==2
        v.run('NoiseTower_Zila',[1] if zila==1 else [0,1]);assert v.vars[TS]==3
        v.run('NoiseTower_Ciro',[1]);assert v.vars[TS]==4
        for i in items:v.run('NoiseTower_Item'+i)
        assert v.vars[TS]==5
        v.run('NoiseTower_Agent');assert v.vars[TS]==6
        if journeys==0:
            r=v.run('NoiseTower_Meira',battles=['loss']);assert r['outcome']=='whiteout' and v.vars[TS]==6
        v.run('NoiseTower_Meira',[0]*(custody-1)+[1],battles=['win']);assert v.vars[TS]==9
        assert v.vars['VAR_ARAUNA_TOWER_WORKERS']==workers
        assert v.vars['VAR_ARAUNA_TOWER_ZILA']==zila
        assert v.vars['VAR_ARAUNA_TOWER_CUSTODY']==custody
        assert 'FLAG_ARAUNA_TOWER_COMPLETE' in v.flags
        before=(v.vars.copy(),v.flags.copy(),v.defeated.copy());v.run('NoiseTower_Meira');assert before==(v.vars,v.flags,v.defeated)
        journeys+=1
    v=VM(s);v.run('NoiseTower_Travel');assert not v.vars and not v.flags and not hasattr(v,'last_warp')
    v=VM(s,flags=['FLAG_SYS_GAME_CLEAR']);v.run('NoiseTower_Travel',[1]);assert v.last_warp==['MAP_ARAUNA_TORRE_RUIDO_RECEPCAO','0']
    v=VM(s,{TS:6},['FLAG_SYS_GAME_CLEAR']);v.run('NoiseTower_Meira',[0,0,0],battles=['win']);assert v.vars[TS]==8 and 'FLAG_ARAUNA_TOWER_COMPLETE' not in v.flags
    v.run('NoiseTower_Meira',[1]);assert v.vars[TS]==9 and len(v.defeated)==1
    for phase,label in [(0,'NoiseTower_Meira'),(1,'NoiseTower_Zila'),(2,'NoiseTower_Ciro'),(3,'NoiseTower_ItemRECORDING'),(4,'NoiseTower_Agent')]:
        v=VM(s,{TS:phase},['FLAG_SYS_GAME_CLEAR']);v.run(label);assert v.vars[TS]==phase and 'FLAG_ARAUNA_TOWER_COMPLETE' not in v.flags
    return journeys

def uivo(s):
    tests=0
    for choice,caught in itertools.product((1,2,3),(False,True)):
        flags=['FLAG_ARAUNA_UIVO_PUP_CAUGHT'] if caught else []
        v=VM(s,{'VAR_ARAUNA_UIVO_STATE':6},flags)
        v.run('CasaUivo_EventScript_Hermit',[1]+[0]*(choice-1)+[1])
        assert v.vars['VAR_ARAUNA_UIVO_STATE']==8 and v.vars['VAR_ARAUNA_UIVO_ACCESS']==choice
        assert v.items==['ITEM_SOOTHE_BELL']
        before=(v.vars.copy(),v.flags.copy(),list(v.items));v.run('CasaUivo_EventScript_Hermit',[1])
        # VAR_RESULT is a scratch answer, not persistent story progress.
        old={k:x for k,x in before[0].items() if k!='VAR_RESULT'}
        assert old=={k:x for k,x in v.vars.items() if k!='VAR_RESULT'} and before[1:]==(v.flags,v.items)
        tests+=1
    v=VM(s,{'VAR_ARAUNA_UIVO_STATE':6});v.run('CasaUivo_EventScript_Hermit',[1,0,0,0]);assert v.vars['VAR_ARAUNA_UIVO_STATE']==6 and not v.items
    return tests+1

def ticket(s):
    label='LittlerootTown_ProfessorBirchsLab_EventScript_TryGiveAuroraTicket'
    count=0
    for tower,awake,ship,battled,full in itertools.product((0,1),repeat=5):
        flags={f for f,b in [('FLAG_ARAUNA_TOWER_COMPLETE',tower),('FLAG_ARAUNA_ARAUA_AWAKENED',awake),('FLAG_ENABLE_SHIP_BIRTH_ISLAND',ship),('FLAG_BATTLED_DEOXYS',battled)] if b}
        v=VM(s,flags=flags,bag_full=bool(full));v.run(label)
        eligible=bool(tower and awake and not ship and not battled and not full)
        assert v.items==(['ITEM_AURORA_TICKET'] if eligible else [])
        if eligible:
            assert 'FLAG_RECEIVED_AURORA_TICKET' in v.flags
            v.run(label);assert v.items==['ITEM_AURORA_TICKET']
        count+=1
    v=VM(s,flags=['FLAG_ARAUNA_TOWER_COMPLETE','FLAG_ARAUNA_ARAUA_AWAKENED'],items=['ITEM_AURORA_TICKET'])
    v.run(label);assert v.items==['ITEM_AURORA_TICKET'] and 'FLAG_ENABLE_SHIP_BIRTH_ISLAND' in v.flags
    return count+1

def geometry(s):
    layouts={l['id']:l for l in json.loads((ROOT/'data/layouts/layouts.json').read_text())['layouts']}
    reports=[]
    maps={n:json.loads((ROOT/'data/maps'/n/'map.json').read_text()) for n in FOGUEIRA+TOWER}
    by_id={m['id']:m for m in maps.values()}
    by_id.update({m['id']:m for m in (json.loads(p.read_text()) for p in (ROOT/'data/maps').glob('*/map.json'))})
    for name,m in maps.items():
        l=layouts[m['layout']];w,h=l['width'],l['height'];b=(ROOT/l['blockdata_filepath']).read_bytes();assert len(b)==w*h*2,(name,len(b),w,h)
        cells=struct.unpack('<'+'H'*(w*h),b);blocked={(i%w,i//w) for i,c in enumerate(cells) if c&0xc00}
        assert len(m['object_events'])<16 and not m['coord_events']
        phases=range(5) if name.endswith('Salao') else (0,1) if name==FOGUEIRA[0] else (0,)
        for phase in phases:
            v=VM(s,{STATE:phase})
            if name.endswith('Salao'):
                assert 'map_script MAP_SCRIPT_ON_TRANSITION, Fogueira_Salao_OnTransition' in (ROOT/'data/maps'/name/'scripts.inc').read_text()
                v.run('Fogueira_Salao_OnTransition')
            elif name==FOGUEIRA[0]:
                if phase:v.flags.add('FLAG_SYS_GAME_CLEAR')
                v.run('Fogueira_Entrada_OnTransition')
                assert ('FLAG_ARAUNA_TOWER_HIDE_CIRO' in v.flags)==(phase==0)
            elif name in TOWER:
                assert 'map_script MAP_SCRIPT_ON_FRAME_TABLE, NoiseTower_OnFrame' in (ROOT/'data/maps'/name/'scripts.inc').read_text()
            objects={(o['x'],o['y']) for o in m['object_events'] if o['flag']=='0' or o['flag'] not in v.flags}
            visible=[o for o in m['object_events'] if o['flag']=='0' or o['flag'] not in v.flags]
            assert len(objects)==len(visible),(name,'overlapping visible objects')
            assert not objects&blocked,(name,'object on collision',objects&blocked)
            start=(m['warp_events'][0]['x'],m['warp_events'][0]['y']);seen={start};q=collections.deque(seen)
            def neighbors(x,y):return ((x+1,y),(x-1,y),(x,y+1),(x,y-1))
            while q:
                for p in neighbors(*q.popleft()):
                    x,y=p
                    if 0<=x<w and 0<=y<h and p not in seen|objects|blocked:seen.add(p);q.append(p)
            for index,e in enumerate(m['warp_events']):
                assert (e['x'],e['y']) in seen,(name,'unreachable warp',e)
                target=by_id[e['dest_map']]['warp_events'][int(e['dest_warp_id'])]
                # The two lobby exits intentionally arrive through the Fogueira
                # transport; its original city exit is the return destination.
                transport=name==TOWER[0] and e['dest_map']==maps[FOGUEIRA[0]]['id']
                assert transport or (target['dest_map']==m['id'] and int(target['dest_warp_id'])==index),(name,'return warp',e)
            for e in m['object_events']+m['bg_events']:
                if e.get('flag','0') in v.flags:continue
                assert seen.intersection(neighbors(e['x'],e['y'])),(name,'unreachable interaction',e['script'])
                assert e['script'] in s.labels,(name,'undefined event',e['script'])
            reports.append({'map':name,'phase':phase,'reachable_floor':len(seen),'visible_objects':len(objects)})
    # Existing ids stay fixed: the five maps are appended to the last group.
    groups=json.loads((ROOT/'data/maps/map_groups.json').read_text());last=groups['group_order'][-1]
    assert groups[last][-5:]==TOWER and len(groups[last])<=256
    return reports

def text_width(s):
    widths=[int(n) for n in re.findall(r'\d+',re.search(r'gFontNormalLatinGlyphWidths\[\] = \{(.*?)\};',(ROOT/'src/fonts.c').read_text(),re.S)[1])]
    cmap={c:int(n,16) for c,n in re.findall(r"^'(.)'\s*=\s*([0-9A-F]{2})\s*$",(ROOT/'charmap.txt').read_text(),re.M)}
    cmap["'"]=cmap['’'];count=0;maximum=0
    for label,text in s.texts.items():
        strings=re.findall(r'"(.*?)"',text)
        for string in strings:
            for line in re.split(r'\\[nlp]|\$',string):
                if not line:continue
                # The engine allows player names up to seven characters. W is
                # a conservative widest normal glyph, not an assumed short name.
                line=line.replace('{PLAYER}','W'*7)
                assert '{' not in line,(label,'unmodeled text control',line)
                width=sum(widths[cmap[c]] for c in line);assert width<=208,(label,line,width)
                count+=1;maximum=max(maximum,width)
    return {'lines':count,'maximum_pixels':maximum,'available_pixels':208}

def main():
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path);a=p.parse_args()
    s=Scripts();report={'status':'PASS','scope':'event source model and map geometry; no ARM execution or rendering','wheel_scenarios':wheel(s),'fogueira_scenarios':fogueira(s),'tower_journeys':tower(s),'uivo_scenarios':uivo(s),'ticket_scenarios':ticket(s),'maps':geometry(s),'text':text_width(s),'pending':['ROM build and emulator acceptance','qualified Libras translation and deaf signing review']}
    if a.output:a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))
if __name__=='__main__':main()
