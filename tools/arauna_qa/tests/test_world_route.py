import unittest
from pathlib import Path

from arauna_qa.repo_map import LayoutDefinition, MapDefinition, RepoMapIndex
from arauna_qa.world_route import WorldRouter


def map_def(map_id, name, layout_id, connections=(), warps=()):
    return MapDefinition(
        map_id,
        name,
        layout_id,
        name,
        None,
        None,
        tuple(connections),
        (),
        tuple(warps),
        (),
        (),
    )


def make_index():
    layouts = {
        "LAYOUT_A": LayoutDefinition("LAYOUT_A", "A_Layout", 10, 8, None, None, None),
        "LAYOUT_B": LayoutDefinition("LAYOUT_B", "B_Layout", 6, 6, None, None, None),
        "LAYOUT_C": LayoutDefinition("LAYOUT_C", "C_Layout", 4, 4, None, None, None),
    }
    a = map_def(
        "MAP_A",
        "A",
        "LAYOUT_A",
        connections=({"map": "MAP_B", "direction": "up", "offset": 2},),
    )
    b = map_def(
        "MAP_B",
        "B",
        "LAYOUT_B",
        warps=(
            {"x": 3, "y": 4, "dest_map": "MAP_C", "dest_warp_id": "0"},
            {"x": 1, "y": 1, "dest_map": "MAP_DYNAMIC", "dest_warp_id": "WARP_ID_DYNAMIC"},
        ),
    )
    c = map_def("MAP_C", "C", "LAYOUT_C")
    maps = {item.id: item for item in (a, b, c)}
    by_name = {item.name: item for item in (a, b, c)}
    return RepoMapIndex(Path("."), layouts, maps, by_name, {})


class WorldRouterTests(unittest.TestCase):
    def test_plans_connection_then_warp(self):
        router = WorldRouter(make_index())
        route = router.plan("MAP_A", "MAP_C")
        self.assertIsNotNone(route)
        self.assertEqual(route.map_sequence, ("MAP_A", "MAP_B", "MAP_C"))
        self.assertEqual([step.kind for step in route.transitions], ["connection", "warp"])

    def test_connection_has_deterministic_boundary_approach(self):
        router = WorldRouter(make_index())
        transition = router.transitions_from("MAP_A")[0]
        self.assertEqual(transition.direction, "UP")
        self.assertEqual(transition.source_y, 0)
        # offset 2 + destination width 6 overlaps source x=2..7 -> midpoint 4
        self.assertEqual(transition.source_x, 4)

    def test_dynamic_warp_is_not_added_to_graph(self):
        router = WorldRouter(make_index())
        transitions = router.transitions_from("MAP_B")
        self.assertEqual(len(transitions), 1)
        self.assertEqual(transitions[0].destination_map, "MAP_C")

    def test_unreachable_target_returns_none(self):
        index = make_index()
        index.maps_by_id["MAP_C"] = map_def("MAP_C", "C", "LAYOUT_C")
        router = WorldRouter(index)
        self.assertIsNone(router.plan("MAP_C", "MAP_A"))


if __name__ == "__main__":
    unittest.main()
