import json
import tempfile
import unittest
from pathlib import Path

from arauna_qa.repo_map import RepoMapIndex


class RepoMapIndexTests(unittest.TestCase):
    def make_repo(self):
        temp = tempfile.TemporaryDirectory()
        root = Path(temp.name)
        (root / "data/layouts").mkdir(parents=True)
        (root / "data/maps/Start").mkdir(parents=True)
        (root / "data/maps/House").mkdir(parents=True)
        (root / "data/layouts/layouts.json").write_text(
            json.dumps({
                "layouts": [
                    {"id": "LAYOUT_START", "name": "Start_Layout", "width": 10, "height": 8},
                    {"id": "LAYOUT_HOUSE", "name": "House_Layout", "width": 6, "height": 6},
                ]
            }),
            encoding="utf-8",
        )
        (root / "data/maps/map_groups.json").write_text(
            json.dumps({"group_order": ["gMapGroup_Test"], "gMapGroup_Test": ["Start", "House"]}),
            encoding="utf-8",
        )
        (root / "data/maps/Start/map.json").write_text(
            json.dumps({
                "id": "MAP_START",
                "name": "Start",
                "layout": "LAYOUT_START",
                "connections": [{"map": "MAP_HOUSE", "direction": "up", "offset": 0}],
                "object_events": [{"x": 2, "y": 3}],
                "warp_events": [{"x": 4, "y": 5, "dest_map": "MAP_HOUSE", "dest_warp_id": "0"}],
                "coord_events": [],
                "bg_events": [],
            }),
            encoding="utf-8",
        )
        (root / "data/maps/House/map.json").write_text(
            json.dumps({
                "id": "MAP_HOUSE",
                "name": "House",
                "layout": "LAYOUT_HOUSE",
                "connections": None,
                "object_events": [],
                "warp_events": [{"x": 1, "y": 1, "dest_map": "MAP_START", "dest_warp_id": "0"}],
                "coord_events": [],
                "bg_events": [],
            }),
            encoding="utf-8",
        )
        return temp, root

    def test_runtime_resolution_and_summary(self):
        temp, root = self.make_repo()
        with temp:
            index = RepoMapIndex.from_repo(root)
            self.assertEqual(index.from_runtime(0, 1).id, "MAP_HOUSE")
            summary = index.summarize("MAP_START")
            self.assertEqual(summary["layout"]["width"], 10)
            self.assertEqual(summary["counts"]["warps"], 1)
            self.assertEqual(index.validate(), [])

    def test_detects_bad_warp_and_out_of_bounds_event(self):
        temp, root = self.make_repo()
        with temp:
            path = root / "data/maps/Start/map.json"
            data = json.loads(path.read_text(encoding="utf-8"))
            data["object_events"] = [{"x": 99, "y": 3}]
            data["warp_events"][0]["dest_warp_id"] = "9"
            path.write_text(json.dumps(data), encoding="utf-8")
            issues = RepoMapIndex.from_repo(root).validate()
            codes = {issue.code for issue in issues}
            self.assertIn("EVENT_OUT_OF_BOUNDS", codes)
            self.assertIn("WARP_DEST_INDEX_INVALID", codes)


if __name__ == "__main__":
    unittest.main()
