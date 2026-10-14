"""Native Frontier save after PC withdrawal; catches mixed PC/party snapshots."""
import argparse
from runtime import *

parser = argparse.ArgumentParser()
parser.add_argument("--expect", choices=("duplicate", "consistent"), required=True)
parser.add_argument("--entry", default="shared", choices=("shared", "tower", "factory", "palace", "arena", "dome", "verdanturf", "fallarbor", "slateport"))
parser.add_argument("--status", type=int, default=0, choices=(0, 1, 2, 3, 4))
args = parser.parse_args()
boot()
fixture()
call("ZeroPlayerPartyMons")
party = SYMS["gPlayerParty"]
call("CreateMon", party, constant("SPECIES_POOCHYENA"), 40, 31, 1, 0x11223344, 0, 0)
write("gPlayerPartyCount", 1, 1)
temp = call("Alloc", 100)
call("CreateMon", temp, constant("SPECIES_PIKACHU"), 30, 31, 1, 0x12345678, 0, 0)
write("gSpecialVar_0x8006", constant("ITEM_LEFTOVERS"), 2)
call("SetMonData", temp, 12, SYMS["gSpecialVar_0x8006"])
call("SetBoxMonAt", 0, 0, temp)
call("Free", temp)
save(Q / "frontier_before_withdraw.sav")
call("BoxMonAtToMon", 0, 0, party + 100)
call("ZeroBoxMonAt", 0, 0)
write("gPlayerPartyCount", 2, 1)
call("SavePlayerParty")
assert call("GetBoxMonDataAt", 0, 0, 11) == 0
assert call("GetMonData3", party + 100, 0, 0) == 0x12345678
# A facility can replace the active team; its save must preserve originals.
call("ZeroPlayerPartyMons")
call("CreateMon", party, constant("SPECIES_GEODUDE"), 50, 31, 1, 0x87654321, 0, 0)
write("gPlayerPartyCount", 1, 1)
sb1 = read("gSaveBlock1Ptr")
call("SetDynamicWarp", 0, read(sb1 + 4, 1), read(sb1 + 5, 1), 255)
entries = {
    "tower": ("CallBattleTowerFunc", "BATTLE_TOWER_FUNC_SAVE"),
    "factory": ("CallBattleFactoryFunction", "BATTLE_FACTORY_FUNC_SAVE"),
    "palace": ("CallBattlePalaceFunction", "BATTLE_PALACE_FUNC_SAVE"),
    "arena": ("CallBattleArenaFunction", "BATTLE_ARENA_FUNC_SAVE"),
    "dome": ("CallBattleDomeFunction", "BATTLE_DOME_FUNC_SAVE"),
    "verdanturf": ("CallVerdanturfTentFunction", "VERDANTURF_TENT_FUNC_SAVE"),
    "fallarbor": ("CallFallarborTentFunction", "FALLARBOR_TENT_FUNC_SAVE"),
    "slateport": ("CallSlateportTentFunction", "SLATEPORT_TENT_FUNC_SAVE"),
}
if args.entry == "shared":
    call("SaveGameFrontier")
else:
    function, selector = entries[args.entry]
    write("gSpecialVar_0x8004", constant(selector), 2)
    write("gSpecialVar_0x8005", args.status, 2)
    call(function)
assert read("gPlayerPartyCount", 1) == 1
assert call("GetMonData3", party, 11, 0) == constant("SPECIES_GEODUDE")
tag = "frontier_" + args.expect + "_" + args.entry + "_" + str(args.status)
path = Q / (tag + ".sav")
assert LIB.exportsave(str(path).encode())
restore(path)
party_personality = call("GetMonData3", party + 100, 0, 0)
box_species = call("GetBoxMonDataAt", 0, 0, 11)
box_personality = call("GetBoxMonDataAt", 0, 0, 0)
duplicate = box_species != 0 and box_personality == party_personality == 0x12345678
assert read("gPlayerPartyCount", 1) == 2
assert call("GetMonData3", party, 11, 0) == constant("SPECIES_POOCHYENA")
assert call("GetMonData3", party + 100, 11, 0) == constant("SPECIES_PIKACHU")
assert call("GetMonData3", party + 100, 12, 0) == constant("ITEM_LEFTOVERS")
assert duplicate == (args.expect == "duplicate")
if args.expect == "consistent":
    assert box_species == 0
snapshot(tag + "_continue")
receipt = metadata() | {"expected": args.expect, "entry": args.entry, "status_input": args.status, "duplicate": duplicate, "active_rental_restored_in_ram": True, "original_party_after_continue": True, "held_item_after_continue": True, "box_species": box_species, "party_personality": party_personality, "box_personality": box_personality, "scope": "PC withdrawal native functions and facility save; challenge battles not played"}
(Q / (tag + "_receipt.json")).write_text(json.dumps(receipt, indent=2) + "\n")
print("Frontier snapshot", args.expect, args.entry, args.status, "confirmed", flush=True)
