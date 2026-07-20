#!/usr/bin/env python3
"""Static checks for the third hands-on playtest feedback batch.

This validator intentionally covers only non-Pokemon work:
- the two visible east-exit tiles in Vila Amanhecer;
- removal of the direct Vila -> Route 109 story teleport;
- physical handoff through Mist Route and Route 110;
- Zila's Notebook as a usable Key Item and progress reader.
"""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def load_json(path: str) -> dict:
    with (ROOT / path).open(encoding="utf-8") as handle:
        return json.load(handle)


def main() -> None:
    village = load_json("data/maps/AraunaMapLab/map.json")
    route = load_json("data/maps/AraunaMistRoute/map.json")
    village_scripts = read("data/maps/AraunaMapLab/scripts.inc")
    route_scripts = read("data/maps/AraunaMistRoute/scripts.inc")
    house_scripts = read("data/maps/AraunaPlayerHouse/scripts.inc")
    item_header = read("include/item.h")
    item_use_header = read("include/item_use.h")
    overrides = read("src/arauna_item_overrides.c")
    notebook = read("src/arauna_notebook.c")
    config = read("config.mk")

    east_exit_tiles = {
        (event["x"], event["y"])
        for event in village["coord_events"]
        if event["script"] == "AraunaMapLab_EventScript_EnterMistRoute"
    }
    assert east_exit_tiles == {(18, 11), (19, 11)}, east_exit_tiles

    hidden_route_warps = [
        event for event in village["warp_events"]
        if event["dest_map"] == "MAP_ARAUNA_MIST_ROUTE"
    ]
    assert not hidden_route_warps, hidden_route_warps

    assert "warp MAP_ROUTE109" not in village_scripts
    assert "AraunaMapLab_EventScript_OfferPortoTravel" not in village_scripts
    assert "warp MAP_ARAUNA_MIST_ROUTE, 255, 10, 17" in village_scripts

    assert route["warp_events"] == []
    assert "warp MAP_ROUTE110" in route_scripts
    assert "FLAG_ARAUNA_PORTO_ARRIVED" in route_scripts
    assert "AraunaMistRoute_Text_CoastRoad" in route_scripts

    assert "giveitem ITEM_FAME_CHECKER" in house_scripts
    assert "ItemUseOutOfBattle_AraunaNotebook" in item_use_header
    assert "ITEM_FAME_CHECKER" in overrides
    assert "Zila's Notebook" in overrides
    assert "GetAraunaNotebookPage" in notebook
    assert "FLAG_ARAUNA_TESTIMONY_IARA_MAE" in notebook
    assert "build/%/src/item.o: CPPFLAGS += -DITEM_C_IMPLEMENTATION" in config

    for accessor in (
        "CopyItemName",
        "CopyItemNameHandlePlural",
        "GetItemName",
        "GetItemDescription",
        "GetItemFieldFunc",
    ):
        assert f"#define {accessor} Arauna" in item_header

    print(
        "Playtest feedback validation passed: visible east exit, no direct "
        "Porto teleport, coast-road handoff, and usable Zila notebook."
    )


if __name__ == "__main__":
    main()
