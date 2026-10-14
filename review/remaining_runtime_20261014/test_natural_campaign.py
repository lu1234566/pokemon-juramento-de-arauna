"""Continue the unmodified normal opening save to the starter and lab.

Only joypad input and memory reads, plus exporting/importing native savedata.
No injected calls, position changes, flags, party edits or forced outcomes.
Run test_natural_start.py first to create the clock save from NEW GAME.
"""
import argparse
import subprocess
import sys
from runtime import *

parser = argparse.ArgumentParser()
parser.add_argument("--cold", action="store_true")
args = parser.parse_args()

def var(name):
    return read(read("gSaveBlock1Ptr") + 0x139C + 2 * (constant(name) - constant("VARS_START")), 2)

def saved_flag(name):
    flag_id = constant(name)
    return bool(read(read("gSaveBlock1Ptr") + 0x1270 + flag_id // 8, 1) & (1 << (flag_id % 8)))

def verify():
    sb1 = read("gSaveBlock1Ptr")
    assert (read(sb1 + 4, 1), read(sb1 + 5, 1)) == (1, 4)
    assert var("VAR_LITTLEROOT_RIVAL_STATE") == 3
    assert var("VAR_ROUTE101_STATE") == 3
    assert var("VAR_BIRCH_LAB_STATE") == 3
    assert read("gPlayerPartyCount", 1) == 1
    assert saved_flag("FLAG_RESCUED_BIRCH")
    assert saved_flag("FLAG_SYS_POKEMON_GET")
    assert not read("sLockFieldControls", 1)
    return {"ciro_first_meeting": 3, "route101_state": 3, "lab_state": 3, "party_count": 1, "rescued_anahi": True}

boot()
restore(Q / ("natural_starter_complete.sav" if args.cold else "natural_clock_complete.sav"))
if not args.cold:
    before_save = read("gSaveCounter")
    replay = json.loads((Q / "natural_campaign_replay.json").read_text())
    for keys, count, release in replay["inputs"]:
        press(keys, count, release)
    result = verify()
    assert read("gBattleOutcome", 1) == constant("B_OUTCOME_WON")
    assert read("gSaveCounter") > before_save, "SAVE must be performed by the recorded menu inputs"
    assert LIB.exportsave(str(Q / "natural_starter_complete.sav").encode())
    snapshot("natural_starter_saved")
    result |= {"first_battle_outcome": "won", "normal_save_menu": True, "joypad_actions": len(replay["inputs"])}
else:
    result = verify() | {"new_process": True, "cold_continue": True}
    snapshot("natural_starter_cold_continue")
receipt = metadata() | {"fixture_setup": False, "game_ram_or_rom_writes": False, "scope": "clock save through first CIRO meeting, starter selection, first battle victory, ANAHI lab and normal SAVE/CONTINUE; not whole campaign"} | result
(Q / ("natural_campaign_cold_receipt.json" if args.cold else "natural_campaign_receipt.json")).write_text(json.dumps(receipt, indent=2) + "\n")
if not args.cold:
    subprocess.run([sys.executable, str(Path(__file__)), "--cold"], check=True)
print("Natural starter campaign", "cold CONTINUE" if args.cold else "joypad replay", "PASS", flush=True)
