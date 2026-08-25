import unittest
from dataclasses import replace

from arauna_qa.exploration import Explorer
from arauna_qa.navigation import Navigator
from arauna_qa.repo_map import CollisionGrid, MapDefinition
from arauna_qa.state import AraunaState


def state(x=0, y=1, group=0, number=0, **changes):
    base = AraunaState(
        frame=1, map_group=group, map_num=number, player_valid=True,
        player_x=x, player_y=y, player_x_internal=x+7, player_y_internal=y+7,
        tile_transition_state=0, field_controls_locked=False, script_enabled=False,
        in_battle=False
    )
    return replace(base, **changes)


def grid(width=4, height=3, blocked=()):
    blocked=set(blocked)
    cells=[]
    for y in range(height):
        for x in range(width):
            c=1 if (x,y) in blocked else 0
            cells.append((c<<10)|(3<<12))
    return CollisionGrid(width,height,tuple(cells))


class World:
    def __init__(self,dynamic=()):
        self.x=0; self.y=1; self.group=0; self.number=0; self.frame=1
        self.dynamic=set(dynamic)
    def snapshot(self):
        return state(self.x,self.y,self.group,self.number,frame=self.frame)
    def move(self,d):
        dx,dy={"UP":(0,-1),"DOWN":(0,1),"LEFT":(-1,0),"RIGHT":(1,0)}[d]
        nxt=(self.x+dx,self.y+dy); self.frame+=1
        if nxt in self.dynamic: return
        self.x,self.y=nxt

class Bridge:
    def __init__(self,w): self.w=w
    def press(self,direction,frames=1): self.w.move(direction)

class Reader:
    def __init__(self,w): self.w=w
    def snapshot(self): return self.w.snapshot()

class Index:
    def __init__(self,g):
        self.g=g
        self.m=MapDefinition(
            "MAP_TEST","Test","LAYOUT_TEST","Test",0,0,(),
            (),({"x":1,"y":1,"dest_map":"MAP_OTHER","dest_warp_id":"0"},),
            ({"x":2,"y":2,"script":"Trigger"},),()
        )
    def from_runtime(self,g,n): return self.m if (g,n)==(0,0) else None
    def load_collision_grid(self,m): return self.g

class ExplorationTests(unittest.TestCase):
    def test_known_triggers_are_excluded(self):
        idx=Index(grid())
        excluded=Explorer.known_trigger_tiles(idx.m)
        self.assertEqual(excluded,{(1,1),(2,2)})

    def test_reachable_tiles_respect_collision_and_exclusion(self):
        g=grid(blocked={(1,0)})
        cells=Explorer.reachable_tiles(g,(0,1),excluded={(1,1)})
        self.assertIn((0,0),cells)
        self.assertNotIn((1,0),cells)
        self.assertNotIn((1,1),cells)

    def test_explore_avoids_triggers_and_records_dynamic_blocker(self):
        g=grid()
        world=World(dynamic={(1,0)})
        idx=Index(g)
        nav=Navigator(Bridge(world),Reader(world),max_polls=2,map_index=idx)
        result=Explorer(nav,idx).explore_current_map(max_targets=6,max_total_moves=30)
        self.assertNotIn((1,1),result.visited_tiles)
        self.assertNotIn((2,2),result.visited_tiles)
        self.assertIn((1,0),result.blocked_tiles)
        self.assertGreater(result.coverage_ratio,0)
        self.assertNotEqual(result.reason,"map_changed")

if __name__=="__main__": unittest.main()
