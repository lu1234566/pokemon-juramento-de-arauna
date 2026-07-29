#!/usr/bin/env python3
"""Static checks for the accepted non-Pokemon playtest feedback batch."""

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
    mist = load_json("data/maps/AraunaMistRoute/map.json")
    coast = load_json("data/maps/Route110/map.json")
    porto = load_json("data/maps/SlateportCity/map.json")

    village_scripts = read("data/maps/AraunaMapLab/scripts.inc")
    mist_scripts = read("data/maps/AraunaMistRoute/scripts.inc")
    house_scripts = read("data/maps/AraunaPlayerHouse/scripts.inc")
    runtime = read("data/scripts/arauna_porto_runtime.inc")
    item_header = read("include/item.h")
    item_use_header = read("include/item_use.h")
    overrides = read("src/arauna_item_overrides.c")
    notebook = read("src/arauna_notebook.c")
    field_tools = read("src/arauna_field_tools.c")
    surf = read("data/scripts/surf.inc")
    build_config = read("config.mk")

    east_exit_tiles = {
        (event["x"], event["y"])
        for event in village["coord_events"]
        if event["script"] == "AraunaMapLab_EventScript_EnterMistRoute"
    }
    # The gate is three rows tall; a trigger on only the middle row let the
    # player walk out along y=10 or y=12 with nothing firing.
    assert east_exit_tiles == {(x, y) for x in (18, 19) for y in (10, 11, 12)}, east_exit_tiles
    assert not [event for event in village["warp_events"] if event["dest_map"] == "MAP_ARAUNA_MIST_ROUTE"]
    assert "warp MAP_ROUTE109" not in village_scripts
    assert "AraunaMapLab_EventScript_OfferPortoTravel" not in village_scripts
    assert "warp MAP_ARAUNA_MIST_ROUTE, 255, 10, 17" in village_scripts

    assert mist["warp_events"] == []
    assert "warp MAP_ROUTE104, 255, 16, 3" in mist_scripts
    assert "FLAG_ARAUNA_PORTO_ARRIVED" not in mist_scripts
    assert "AraunaMistRoute_Text_CoastRoad" in mist_scripts

    assert coast["layout"] == "LAYOUT_ROUTE110"
    assert not coast["show_map_name"]
    assert not coast["allow_cycling"]
    assert any(obj["script"] == "Route110_EventScript_ConsortiumCheckpoint" for obj in coast["object_events"])
    assert porto["layout"] == "LAYOUT_SLATEPORT_CITY"
    assert not porto["show_map_name"]
    assert len(porto["object_events"]) < 15
    assert "FLAG_ARAUNA_PORTO_ARRIVED" in runtime
    assert "AraunaPorto_EventScript_RoadArrival" in runtime

    assert "giveitem ITEM_FAME_CHECKER" in house_scripts
    assert "giveitem ITEM_DEVON_SCOPE" in runtime
    assert "ItemUseOutOfBattle_AraunaNotebook" in item_use_header
    assert "ItemUseOutOfBattle_AraunaBoard" in item_use_header
    assert "ITEM_FAME_CHECKER" in overrides and "Zila's Notebook" in overrides
    assert "ITEM_DEVON_SCOPE" in overrides and "Tide Board" in overrides
    assert "GetAraunaNotebookPage" in notebook
    assert "FLAG_ARAUNA_TESTIMONY_IARA_MAE" in notebook
    assert "FLAG_ARAUNA_BOARD_RECEIVED" in notebook
    assert "AraunaPartyHasMonWithSurf" in field_tools
    assert "EventScript_UseTideBoard" in surf

    assert "build/%/src/item.o: CPPFLAGS += -DITEM_C_IMPLEMENTATION" in build_config
    assert "ARAUNA_FIELD_PLAYER_AVATAR_IMPLEMENTATION" in build_config
    for accessor in (
        "CopyItemName",
        "CopyItemNameHandlePlural",
        "GetItemName",
        "GetItemDescription",
        "GetItemFieldFunc",
    ):
        assert f"#define {accessor} Arauna" in item_header

    print(
        "Playtest feedback validated: visible Vila exit, physical coast travel, "
        "Porto identity, dynamic notebook and HM-free Tide Board."
    )


if __name__ == "__main__":
    main()
