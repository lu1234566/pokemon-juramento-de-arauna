"""Whole compiled NPC scenes: full pocket, pending flags and later retry."""
import argparse
from runtime import *

CASES = {
    "good_rod": ("Route118", "GoodRodFisherman", "ITEM_GOOD_ROD", "FLAG_RECEIVED_GOOD_ROD", None),
    "super_rod": ("MossdeepCity_House3", "SuperRodFisherman", "ITEM_SUPER_ROD", "FLAG_RECEIVED_SUPER_ROD", None),
    "pail": ("Route104_PrettyPetalFlowerShop", "WailmerPailGirl", "ITEM_WAILMER_PAIL", "FLAG_RECEIVED_WAILMER_PAIL", None),
    "soot_sack": ("Route113_GlassWorkshop", "GlassWorker", "ITEM_SOOT_SACK", "VAR_GLASS_WORKSHOP_STATE", None),
    "coin_case": ("MauvilleCity_House2", "Woman", "ITEM_COIN_CASE", "FLAG_RECEIVED_COIN_CASE", "ITEM_HARBOR_MAIL"),
    "powder_jar": ("SlateportCity", "BerryPowderClerk", "ITEM_POWDER_JAR", "FLAG_RECEIVED_POWDER_JAR", None),
    "cut": ("RustboroCity_CuttersHouse", "Cutter", "ITEM_HM_CUT", "FLAG_RECEIVED_HM_CUT", None),
    "rock_smash": ("MauvilleCity_House1", "RockSmashDude", "ITEM_HM_ROCK_SMASH", "FLAG_RECEIVED_HM_ROCK_SMASH", None),
    "basement_key": ("MauvilleCity", "Wattson", "ITEM_BASEMENT_KEY", "FLAG_GOT_BASEMENT_KEY_FROM_WATTSON", None),
}
parser = argparse.ArgumentParser()
parser.add_argument("case", choices=CASES)
parser.add_argument("--expect", choices=("lost", "retry"), required=True)
args = parser.parse_args()
map_name, npc, item, state, trade = CASES[args.case]
script = map_name + "_EventScript_" + npc
boot()
fixture()
events = json.loads((R / "data/maps" / map_name / "map.json").read_text())["object_events"]
index, event = next((i, e) for i, e in enumerate(events) if e["script"] == script)
local = event.get("local_id", index + 1)
if isinstance(local, str):
    local = SYMS[local] if local in SYMS else constant(local)
if event.get("flag") not in ("0", 0, None):
    call("FlagClear", constant(event["flag"]))
warp(map_name, event["x"], event["y"] + 1)
sb2 = read("gSaveBlock2Ptr")
write(sb2 + 0x14, (read(sb2 + 0x14, 2) & ~7) | 2, 2)
call("ClearBag")
if trade:
    assert call("AddBagItem", constant(trade), 1)
target = constant(item)
pocket = call("GetItemPocket", target)
synthetic = pocket == call("GetItemPocket", constant("ITEM_TM01"))
if synthetic:
    slots = read(SYMS["gBagPockets"] + (pocket - 1) * 8)
    capacity = read(SYMS["gBagPockets"] + (pocket - 1) * 8 + 4, 1)
    key = read(sb2 + 0xAC) & 0xffff
    for i in range(capacity):
        write(slots + i * 4, constant("ITEM_TM06"), 2)
        write(slots + i * 4 + 2, 99 ^ key, 2)
else:
    for item_id in range(1, constant("ITEMS_COUNT")):
        if item_id != target and call("GetItemPocket", item_id) == pocket:
            call("AddBagItem", item_id, 1)
assert not call("CheckBagHasSpace", target, 1)

def progress():
    return call("VarGet", constant(state)) if state.startswith("VAR_") else flag(state)

def interact():
    sb1 = read("gSaveBlock1Ptr")
    idx = call("GetObjectEventIdByLocalIdAndMap", local, read(sb1 + 5, 1), read(sb1 + 4, 1))
    assert idx < 16
    write("gSelectedObjectEvent", idx, 1)
    write("gSpecialVar_LastTalked", local, 2)
    run_script(script)

initial = progress()
interact()
assert quantity(item) == 0
failed_progress = progress()
trade_after = quantity(trade) if trade else None
if args.expect == "lost":
    assert failed_progress != initial
else:
    assert failed_progress == initial
    if trade:
        assert trade_after == 1
    save(Q / (args.case + "_pending.sav"))
    restore(Q / (args.case + "_pending.sav"))
    assert progress() == initial
    assert quantity(item) == 0
    # Keep the trade resource; free one slot using the native remove routine.
    if synthetic:
        call("ClearBag")
    else:
        slots = read(SYMS["gBagPockets"] + (pocket - 1) * 8)
        filler = read(slots, 2)
        assert call("RemoveBagItem", filler, 1)
    interact()
    assert quantity(item) == 1
    assert progress() != initial
    if trade:
        assert quantity(trade) == 0
    save(Q / (args.case + "_claimed.sav"))
    restore(Q / (args.case + "_claimed.sav"))
    assert quantity(item) == 1
    interact()
    assert quantity(item) == 1
snapshot(args.case + "_" + args.expect)
receipt = metadata() | {"case": args.case, "expect": args.expect, "initial_progress": initial, "full_bag_progress": failed_progress, "trade_after_full_bag": trade_after, "synthetic_tm_pocket": synthetic, "retry_and_continue": args.expect == "retry", "script": script}
(Q / (args.case + "_" + args.expect + "_receipt.json")).write_text(json.dumps(receipt, indent=2) + "\n")
print(args.case, args.expect, "confirmed", flush=True)
