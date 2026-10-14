"""Compiled story scenes: capacity failure, cold CONTINUE and normal NPC retry.

Fixtures select a scene and fill its pocket. Progress after entry is made by
the engine scripts; tests never write the result flags or gift quantities.
"""
import argparse
from runtime import *

CASES = {
    "mirage_root": ("MirageTower_4F", "RootFossil", "ITEM_ROOT_FOSSIL", "FLAG_CHOSE_ROOT_FOSSIL"),
    "mirage_claw": ("MirageTower_4F", "ClawFossil", "ITEM_CLAW_FOSSIL", "FLAG_CHOSE_CLAW_FOSSIL"),
    "underpass_root": ("DesertUnderpass", "Fossil", "ITEM_ROOT_FOSSIL", "FLAG_HIDE_DESERT_UNDERPASS_FOSSIL"),
    "underpass_claw": ("DesertUnderpass", "Fossil", "ITEM_CLAW_FOSSIL", "FLAG_HIDE_DESERT_UNDERPASS_FOSSIL"),
    "meteorite": ("MtChimney", "MeteoriteMachine", "ITEM_METEORITE", "FLAG_RECEIVED_METEORITE"),
    "surf": ("PetalburgCity_WallysHouse", "WallysDad", "ITEM_HM_SURF", "FLAG_RECEIVED_HM_SURF"),
    "dive": ("MossdeepCity_StevensHouse", "Steven", "ITEM_HM_DIVE", "FLAG_RECEIVED_HM_DIVE"),
    "waterfall": ("SootopolisCity", "Wallace", "ITEM_HM_WATERFALL", "FLAG_RECEIVED_HM_WATERFALL"),
}
parser = argparse.ArgumentParser()
parser.add_argument("case", choices=CASES)
parser.add_argument("--expect", choices=("lost", "retry"), required=True)
parser.add_argument("--direct", action="store_true", help="ordinary first delivery with an empty bag")
parser.add_argument("--ineligible", action="store_true", help="NPC before its story scene; Surf/Dive only")
args = parser.parse_args()
map_name, npc, item, received = CASES[args.case]
script = map_name + "_EventScript_" + npc
boot()
fixture()
events = json.loads((R / "data/maps" / map_name / "map.json").read_text())
objects = events["object_events"]
event = next((e for e in objects if e["script"] == script), None)
if event:
    local = event.get("local_id", objects.index(event) + 1)
    if isinstance(local, str):
        local = SYMS[local] if local in SYMS else constant(local)
    if event["flag"] not in ("0", 0):
        call("FlagClear", constant(event["flag"]))
    x, y = event["x"], event["y"] + 1
else:
    local = 0
    event = next(e for e in events["bg_events"] if e.get("script") == script)
    x, y = event["x"], event["y"] + 1
if args.case.startswith("underpass_"):
    call("FlagSet", constant("FLAG_CHOSE_CLAW_FOSSIL" if args.case.endswith("root") else "FLAG_CHOSE_ROOT_FOSSIL"))
if args.case == "meteorite":
    call("FlagSet", constant("FLAG_DEFEATED_EVIL_TEAM_MT_CHIMNEY"))
if args.case == "waterfall":
    call("FlagSet", constant("FLAG_SOOTOPOLIS_ARCHIE_MAXIE_LEAVE"))
if args.case == "surf":
    x, y = 2, 4
if args.case == "dive":
    x, y = 3, 7
warp(map_name, x, y)
sb2 = read("gSaveBlock2Ptr")
write(sb2 + 0x14, (read(sb2 + 0x14, 2) & ~7) | 2, 2)
call("ClearBag")
target = constant(item)
pocket = call("GetItemPocket", target)
synthetic = pocket == call("GetItemPocket", constant("ITEM_TM01"))
slots = read(SYMS["gBagPockets"] + (pocket - 1) * 8)
capacity = read(SYMS["gBagPockets"] + (pocket - 1) * 8 + 4, 1)
if args.direct or args.ineligible:
    pass
elif synthetic:
    # There are fewer unique TMs than slots: explicit capacity fault injection.
    key = read(sb2 + 0xAC) & 0xffff
    for i in range(capacity):
        write(slots + i * 4, constant("ITEM_TM06"), 2)
        write(slots + i * 4 + 2, 99 ^ key, 2)
else:
    for item_id in range(1, constant("ITEMS_COUNT")):
        if item_id != target and call("GetItemPocket", item_id) == pocket:
            call("AddBagItem", item_id, 1)
assert bool(call("CheckBagHasSpace", target, 1)) == bool(args.direct or args.ineligible)

def select_npc():
    if local:
        sb1 = read("gSaveBlock1Ptr")
        idx = call("GetObjectEventIdByLocalIdAndMap", local, read(sb1 + 5, 1), read(sb1 + 4, 1))
        if idx >= 16:
            snapshot(args.case + "_object_missing")
        assert idx < 16, (args.case, local, read(sb1, 2), read(sb1 + 2, 2), read(sb1 + 4, 1), read(sb1 + 5, 1), flag(received))
        write("gSelectedObjectEvent", idx, 1)
        write("gSpecialVar_LastTalked", local, 2)

def interact(label=script):
    select_npc()
    run_script(label, limit=6000)
    frames(0, 120)
    if args.case.startswith("mirage_") and flag(received):
        # Tower collapse warps into a second automatic Route111 scene.
        for _ in range(6000):
            press(1, release=2)
            if not call("ArePlayerFieldControlsLocked") and read(SYMS["gMain"] + 4) == SYMS["CB2_Overworld"] | 1:
                frames(0, 120)
                if not call("ArePlayerFieldControlsLocked"):
                    break
    assert not call("ArePlayerFieldControlsLocked"), "autorun scene must allow freeing pocket space"

if args.ineligible:
    assert args.case in ("surf", "dive")
    interact()
    assert quantity(item) == 0
    assert not flag(received)
    (Q / (args.case + "_story_ineligible_receipt.json")).write_text(json.dumps(metadata() | {"case": args.case, "scenario": "ineligible", "no_early_gift": True}, indent=2) + "\n")
    print(args.case, "ineligible confirmed", flush=True)
    raise SystemExit(0)

if args.case == "surf":
    call("VarSet", constant("VAR_PETALBURG_CITY_STATE"), 4)
    interact(map_name + "_EventScript_GiveHMSurf")
elif args.case == "dive":
    call("VarSet", constant("VAR_STEVENS_HOUSE_STATE"), 1)
    interact(map_name + "_EventScript_StevenGivesDive")
else:
    interact()
if args.direct:
    assert quantity(item) == 1
    assert flag(received)
    save(Q / (args.case + "_story_direct.sav"))
    restore(Q / (args.case + "_story_direct.sav"))
    assert quantity(item) == 1
    assert flag(received)
    if not args.case.startswith(("mirage_", "underpass_")):
        interact()
        assert quantity(item) == 1
    snapshot(args.case + "_direct_claimed")
    (Q / (args.case + "_story_direct_receipt.json")).write_text(json.dumps(metadata() | {"case": args.case, "scenario": "direct", "first_delivery_and_continue": True}, indent=2) + "\n")
    print(args.case, "direct confirmed", flush=True)
    raise SystemExit(0)
assert quantity(item) == 0
failed_flag = flag(received)
assert failed_flag == (args.expect == "lost")
if args.case.startswith("mirage_") and args.expect == "retry":
    assert not flag("FLAG_HIDE_MIRAGE_TOWER_ROOT_FOSSIL")
    assert not flag("FLAG_HIDE_MIRAGE_TOWER_CLAW_FOSSIL")
snapshot(args.case + "_" + args.expect + "_full")
if args.expect == "retry":
    if args.case == "surf":
        assert call("VarGet", constant("VAR_PETALBURG_CITY_STATE")) == 5
    if args.case == "dive":
        assert call("VarGet", constant("VAR_STEVENS_HOUSE_STATE")) == 2
        assert not flag("FLAG_OMIT_DIVE_FROM_STEVEN_LETTER")
        assert not flag("FLAG_HIDE_SEAFLOOR_CAVERN_ENTRANCE_AQUA_GRUNT")
    save(Q / (args.case + "_story_pending.sav"))
    restore(Q / (args.case + "_story_pending.sav"))
    assert not flag(received)
    assert quantity(item) == 0
    frames(0, 120)
    assert not call("ArePlayerFieldControlsLocked")
    # A second failed interaction after CONTINUE must remain pending too.
    interact()
    assert not flag(received)
    assert quantity(item) == 0
    # Test retry through the ordinary NPC/object script after cold CONTINUE.
    if synthetic:
        call("ClearBag")
    else:
        slots = read(SYMS["gBagPockets"] + (pocket - 1) * 8)
        assert call("RemoveBagItem", read(slots, 2), 1)
    interact()
    assert quantity(item) == 1
    assert flag(received)
    if args.case == "dive":
        assert flag("FLAG_OMIT_DIVE_FROM_STEVEN_LETTER")
        assert flag("FLAG_HIDE_SEAFLOOR_CAVERN_ENTRANCE_AQUA_GRUNT")
    save(Q / (args.case + "_story_claimed.sav"))
    restore(Q / (args.case + "_story_claimed.sav"))
    assert quantity(item) == 1
    assert flag(received)
    if args.case.startswith(("mirage_", "underpass_")):
        warp(map_name, x, y)
        sb1 = read("gSaveBlock1Ptr")
        assert call("GetObjectEventIdByLocalIdAndMap", local, read(sb1 + 5, 1), read(sb1 + 4, 1)) >= 16
    else:
        interact()
        assert quantity(item) == 1
    snapshot(args.case + "_retry_claimed")
receipt = metadata() | {"case": args.case, "expect": args.expect, "full_bag_received_flag": bool(failed_flag), "synthetic_tm_pocket": synthetic, "retry_and_continue": args.expect == "retry", "script": script}
(Q / (args.case + "_story_" + args.expect + "_receipt.json")).write_text(json.dumps(receipt, indent=2) + "\n")
print(args.case, args.expect, "confirmed", flush=True)
