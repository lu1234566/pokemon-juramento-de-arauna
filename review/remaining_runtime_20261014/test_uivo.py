"""Catch the pup through the actual bag, finish Uivo, and cold CONTINUE."""
from runtime import *

boot()
fixture()
call("ZeroPlayerPartyMons")
call("CreateMon", SYMS["gPlayerParty"], constant("SPECIES_POOCHYENA"), 35, 31, 1, 0x13579, 0, 0)
write("gPlayerPartyCount", 1, 1)
call("AddBagItem", constant("ITEM_MASTER_BALL"), 1)
call("VarSet", constant("VAR_ARAUNA_UIVO_STATE"), 4)
call("FlagSet", constant("FLAG_BADGE02_GET"))
warp("Arauna_CasaUivo_Refugio", 8, 12)
run_script("CasaUivo_Refugio_Howl")
sb1 = read("gSaveBlock1Ptr")
idx = call("GetObjectEventIdByLocalIdAndMap", 1, read(sb1 + 5, 1), read(sb1 + 4, 1))
assert idx < 16
write("gSelectedObjectEvent", idx, 1)
write("gSpecialVar_LastTalked", 1, 2)
call("ScriptContext_SetupScript", SYMS["CasaUivo_EventScript_Pup"])
for i in range(3500):
    frames(1 if i % 2 == 0 else 0, 2)
    if read(SYMS["gBattlerControllerFuncs"]) in [address | 1 for address in ADDRESSES["HandleInputChooseAction"]]:
        break
else:
    snapshot("uivo_no_battle_menu")
    raise RuntimeError("No battle action menu")
snapshot("uivo_battle_menu")
press(16, release=8)
press(1, release=120)
snapshot("uivo_bag_initial")
press(16, release=60)
snapshot("uivo_bag_balls")
press(1, release=30)
press(1, release=90)
for i in range(4000):
    frames(2 if i % 2 == 0 else 0, 2)
    if call("VarGet", constant("VAR_ARAUNA_UIVO_STATE")) == 5 and not read("sLockFieldControls", 1):
        break
else:
    snapshot("uivo_capture_blocked")
    raise RuntimeError("Capture did not return to state 5")
assert flag("FLAG_ARAUNA_UIVO_PUP_CAUGHT")
assert read("gPlayerPartyCount", 1) == 2
assert quantity("ITEM_MASTER_BALL") == 0
snapshot("uivo_pup_caught")
warp("Arauna_CasaUivo_Sala", 8, 6)
sb1 = read("gSaveBlock1Ptr")
idx = call("GetObjectEventIdByLocalIdAndMap", 1, read(sb1 + 5, 1), read(sb1 + 4, 1))
write("gSelectedObjectEvent", idx, 1)
write("gSpecialVar_LastTalked", 1, 2)
run_script("CasaUivo_EventScript_Hermit")
assert call("VarGet", constant("VAR_ARAUNA_UIVO_STATE")) == 8
assert call("VarGet", constant("VAR_ARAUNA_UIVO_ACCESS")) == 1
assert quantity("ITEM_SOOTHE_BELL") == 1
save(Q / "uivo_caught_complete.sav")
restore(Q / "uivo_caught_complete.sav")
assert flag("FLAG_ARAUNA_UIVO_PUP_CAUGHT")
assert read("gPlayerPartyCount", 1) == 2
assert call("VarGet", constant("VAR_ARAUNA_UIVO_STATE")) == 8
assert call("VarGet", constant("VAR_ARAUNA_UIVO_ACCESS")) == 1
assert quantity("ITEM_SOOTHE_BELL") == 1
snapshot("uivo_caught_complete_continue")
(Q / "uivo_capture_receipt.json").write_text(json.dumps(metadata() | {"battle_capture": "Master Ball through actual bag UI", "outcome": "caught", "party_count": 2, "uivo_state_after_continue": 8, "access_after_continue": 1, "soothe_bell_after_continue": 1, "scope": "starting state 4 fixture; no forced battle result or post-start arc progression"}, indent=2) + "\n")
print("Uivo captured ending and cold CONTINUE: PASS", flush=True)
