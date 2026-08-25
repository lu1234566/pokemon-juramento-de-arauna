import unittest
from dataclasses import replace
from collections import deque

from arauna_qa.navigation import MoveResult
from arauna_qa.repo_map import CollisionGrid, MapDefinition
from arauna_qa.state import AraunaState
from arauna_qa.world_nav import WorldNavigator
from arauna_qa.world_route import MapTransition, WorldRoute


def st(x=0,y=1,num=0,**kw):
    s=AraunaState(frame=1,map_group=0,map_num=num,map_layout_id=1,region_map_section_id=1,
        map_type=1,weather=0,music=1,player_valid=True,player_x=x,player_y=y,
        player_x_internal=x+7,player_y_internal=y+7,facing=1,movement_direction=1,
        elevation=3,metatile_behavior=0,avatar_flags=1,running_state=0,tile_transition_state=0,
        field_controls_locked=False,script_enabled=False,script_mode=0,script_ptr=0,
        in_battle=False,held_keys=0,new_keys=0,callback1=0,callback2=0)
    return replace(s,**kw)


def md(mid,name,num,warps=(),connections=()):
    return MapDefinition(mid,name,"L"+name,name,0,num,tuple(connections),(),tuple(warps),(),())


class Index:
    def __init__(self,connection=False):
        self.a=md("MAP_A","A",0,connections=({"map":"MAP_B","direction":"right","offset":0},)) if connection else md("MAP_A","A",0,warps=({"x":2,"y":1,"dest_map":"MAP_B","dest_warp_id":"0"},))
        self.b=md("MAP_B","B",1); self.maps_by_id={"MAP_A":self.a,"MAP_B":self.b}
    def require(self,k): return self.maps_by_id[k]
    def from_runtime(self,g,n): return self.a if (g,n)==(0,0) else self.b if (g,n)==(0,1) else None
    def load_collision_grid(self,m): return CollisionGrid(4,3,tuple(3<<12 for _ in range(12)))


class World:
    def __init__(self,mode): self.x=0;self.y=1;self.num=0;self.frame=1;self.mode=mode
    def snapshot(self): return st(self.x,self.y,self.num,frame=self.frame)
    def move(self,d):
        dx,dy={"UP":(0,-1),"DOWN":(0,1),"LEFT":(-1,0),"RIGHT":(1,0)}[d]; self.frame+=1
        if self.mode=="connection" and d=="RIGHT" and self.x==3: self.num=1;self.x=0;return
        self.x+=dx;self.y+=dy
        if self.mode=="warp" and (self.x,self.y)==(2,1): self.num=1;self.x=0;self.y=1


class Nav:
    def __init__(self,w): self.w=w;self.reader=self
    def snapshot(self): return self.w.snapshot()
    @staticmethod
    def plan_path(grid,start,target,blocked_tiles=()):
        dirs={"UP":(0,-1),"DOWN":(0,1),"LEFT":(-1,0),"RIGHT":(1,0)}; blocked=set(blocked_tiles)
        q=deque([start]);prev={start:None};used={}
        while q:
            cur=q.popleft()
            if cur==target: break
            for d,(dx,dy) in dirs.items():
                nxt=(cur[0]+dx,cur[1]+dy)
                if nxt in prev or nxt in blocked or not grid.is_passable(*nxt): continue
                prev[nxt]=cur;used[nxt]=d;q.append(nxt)
        if target not in prev:return None
        out=[];cur=target
        while cur!=start: out.append(used[cur]);cur=prev[cur]
        return list(reversed(out))
    def step(self,direction,press_frames=2):
        before=self.snapshot();self.w.move(direction);after=self.snapshot()
        changed=(before.map_group,before.map_num)!=(after.map_group,after.map_num)
        moved=changed or (before.player_x,before.player_y)!=(after.player_x,after.player_y)
        return MoveResult(direction,before,after,moved,changed,not moved,1)


class Router:
    def __init__(self,mode):self.mode=mode
    def plan(self,start,target):
        if start!="MAP_A" or target!="MAP_B":return None
        t=MapTransition("warp","MAP_A","MAP_B",2,1) if self.mode=="warp" else MapTransition("connection","MAP_A","MAP_B",3,1,"RIGHT")
        return WorldRoute("MAP_A","MAP_B",(t,))


class WorldNavigationTests(unittest.TestCase):
    def test_warp_is_executed_and_verified(self):
        i=Index();w=World("warp");r=WorldNavigator(Nav(w),i,Router("warp")).route_to("MAP_B")
        self.assertTrue(r.reached);self.assertEqual(r.final_state.map_num,1)
    def test_connection_is_executed_and_verified(self):
        i=Index(True);w=World("connection");r=WorldNavigator(Nav(w),i,Router("connection")).route_to("MAP_B")
        self.assertTrue(r.reached);self.assertEqual(r.final_state.map_num,1)

if __name__=="__main__":unittest.main()
