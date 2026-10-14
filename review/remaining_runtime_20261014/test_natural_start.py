"""NEW GAME to clock and normal SAVE/CONTINUE, using only joypad inputs."""
import argparse
import subprocess
import sys
from runtime import *

parser = argparse.ArgumentParser()
parser.add_argument("--cold", action="store_true")
args = parser.parse_args()
save_path = Q / "natural_clock_complete.sav"

def clock_flag():
    flag_id = constant("FLAG_SET_WALL_CLOCK")
    return bool(read(read("gSaveBlock1Ptr") + 0x1270 + flag_id // 8, 1) & (1 << (flag_id % 8)))

def intro_state():
    return read(read("gSaveBlock1Ptr") + 0x139C + 2 * (constant("VAR_LITTLEROOT_INTRO_STATE") - constant("VARS_START")), 2)

if args.cold:
    boot()
    restore(save_path)
    assert clock_flag()
    assert intro_state() == 6
    assert not read("sLockFieldControls", 1)
    snapshot("natural_clock_cold_continue")
    (Q / "natural_cold_receipt.json").write_text(json.dumps(metadata() | {"fixture_setup": False, "new_process": True, "clock_flag": True, "intro_state": 6, "controls_unlocked": True, "game_ram_or_rom_writes": False}, indent=2) + "\n")
    print("Natural starting save, separate-process CONTINUE: PASS", flush=True)
    raise SystemExit(0)

inputs = []
boot()

def act(keys, count=2, release=100):
    press(keys, count, release)
    inputs.append([keys, count, release])

def finish_dialogue():
    for _ in range(400):
        if not read("sLockFieldControls", 1):
            return
        act(1, 2, 6)
    snapshot("natural_dialogue_timeout")
    raise RuntimeError("Dialogue failed to release normal controls")

for _ in range(98):
    act(1)
for _ in range(12):
    act(1, 30, 10)
for _ in range(6):
    act(2, 2, 35)
act(16, 90, 100)
snapshot("natural_boot_village")
for _ in range(20):
    act(1)
for _ in range(45):
    act(1, 15, 15)
finish_dialogue()
act(128, 18, 30)
finish_dialogue()
act(64, 120, 120)
finish_dialogue()
sb1 = read("gSaveBlock1Ptr")
assert (read(sb1 + 4, 1), read(sb1 + 5, 1)) == (1, 1)
snapshot("natural_upstairs")
act(32, 32, 16)
act(64, 2, 6)
act(1, 2, 90)
for _ in range(10):
    act(1, 5, 50)
act(64, 2, 12)  # Confirm YES in the clock's default-NO menu.
act(1, 2, 120)
finish_dialogue()
assert clock_flag()
assert intro_state() == 6
snapshot("natural_clock_finished")
act(8, 2, 45)
assert read("sStartMenuCursorPos", 1) == 0
for _ in range(3):
    act(128, 2, 8)
act(1, 2, 90)
for _ in range(200):
    if read("gSaveCounter") > 0 and read(SYMS["gMain"] + 4) == SYMS["CB2_Overworld"] | 1 and not read("sLockFieldControls", 1):
        break
    act(1, 2, 20)
else:
    snapshot("natural_save_timeout")
    raise RuntimeError("Normal SAVE menu did not complete")
assert LIB.exportsave(str(save_path).encode())
snapshot("natural_saved_clock")
(Q / "natural_inputs.json").write_text(json.dumps(metadata() | {"fixture_setup": False, "game_ram_or_rom_writes": False, "inputs": inputs, "scope": "normal opening, NEW GAME, name selection, truck, village, house, clock and normal SAVE; not whole campaign"}, indent=2) + "\n")
subprocess.run([sys.executable, str(Path(__file__)), "--cold"], check=True)
print("Natural opening to clock and SAVE: PASS", flush=True)
