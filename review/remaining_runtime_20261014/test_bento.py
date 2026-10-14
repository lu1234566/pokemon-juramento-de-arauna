"""Run the entire compiled letter/reward scene, with a full TM fixture."""
from runtime import *

boot()
fixture()
call("FlagClear", constant("FLAG_HIDE_GRANITE_CAVE_STEVEN"))
warp("GraniteCave_StevensRoom", 7, 9)
call("AddBagItem", constant("ITEM_LETTER"), 1)
sb2 = read("gSaveBlock2Ptr")
write(sb2 + 0x14, (read(sb2 + 0x14, 2) & ~7) | 2, 2)
# Only 58 distinct TM/HMs exist for 64 slots: synthetic capacity fixture.
slots = read(SYMS["gBagPockets"] + (call("GetItemPocket", constant("ITEM_TM_STEEL_WING")) - 1) * 8)
key = read(sb2 + 0xAC) & 0xffff
for i in range(64):
    write(slots + i * 4, constant("ITEM_TM06"), 2)
    write(slots + i * 4 + 2, 99 ^ key, 2)
assert not call("CheckBagHasSpace", constant("ITEM_TM_STEEL_WING"), 1)
sb1 = read("gSaveBlock1Ptr")
gi, mi = read(sb1 + 4, 1), read(sb1 + 5, 1)
idx = call("GetObjectEventIdByLocalIdAndMap", 1, mi, gi)
assert idx < 16
write("gSelectedObjectEvent", idx, 1)
write("gSpecialVar_LastTalked", 1, 2)
run_script("GraniteCave_StevensRoom_EventScript_Steven")
assert flag("FLAG_DELIVERED_STEVEN_LETTER")
assert not flag("FLAG_HIDE_GRANITE_CAVE_STEVEN")
assert not flag("FLAG_REGISTERED_STEVEN_POKENAV")
assert quantity("ITEM_TM_STEEL_WING") == 0
assert quantity("ITEM_LETTER") == 0
snapshot("bento_bag_full_retry_available")
save(Q / "bento_pending.sav")
restore(Q / "bento_pending.sav")
assert flag("FLAG_DELIVERED_STEVEN_LETTER")
assert not flag("FLAG_HIDE_GRANITE_CAVE_STEVEN")
assert quantity("ITEM_TM_STEEL_WING") == 0
call("ClearBag")
sb1 = read("gSaveBlock1Ptr")
idx = call("GetObjectEventIdByLocalIdAndMap", 1, read(sb1 + 5, 1), read(sb1 + 4, 1))
assert idx < 16
write("gSelectedObjectEvent", idx, 1)
write("gSpecialVar_LastTalked", 1, 2)
run_script("GraniteCave_StevensRoom_EventScript_Steven")
assert quantity("ITEM_TM_STEEL_WING") == 1
assert flag("FLAG_HIDE_GRANITE_CAVE_STEVEN")
assert flag("FLAG_REGISTERED_STEVEN_POKENAV")
save(Q / "bento_claimed.sav")
restore(Q / "bento_claimed.sav")
assert quantity("ITEM_TM_STEEL_WING") == 1
assert flag("FLAG_HIDE_GRANITE_CAVE_STEVEN")
assert flag("FLAG_REGISTERED_STEVEN_POKENAV")
sb1 = read("gSaveBlock1Ptr")
assert call("GetObjectEventIdByLocalIdAndMap", 1, read(sb1 + 5, 1), read(sb1 + 4, 1)) == 16
snapshot("bento_claimed_continue")
(Q / "bento_receipt.json").write_text(json.dumps(metadata() | {"scene": "full compiled script", "tm_capacity": "synthetic duplicate slots, not naturally obtainable", "letter_consumed_once": True, "reward_retry_after_continue": True, "npc_persistently_hidden": True, "one_tm_after_continue": True}, indent=2) + "\n")
print("Bento scene, full bag, retry and CONTINUE: PASS", flush=True)
