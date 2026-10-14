"""Native mGBA QA. Fixture writes are setup, never evidence of progression."""
import ctypes as C
import hashlib
import json
import os
import re
import subprocess
from pathlib import Path
from PIL import Image

Q = Path(__file__).resolve().parent
R = Q.parents[1]
BUILD = Path(os.environ.get("ARAUNA_QA_BUILD_DIR", R))
ROM = BUILD / "pokemon-juramento-de-arauna-en_modern.gba"
SYMS = {}
ADDRESSES = {}
symbol_file = BUILD / "arauna-en.symbols.txt"
symbol_text = symbol_file.read_text() if symbol_file.exists() else subprocess.check_output(["arm-none-eabi-nm", "-n", str(BUILD / "pokemon-juramento-de-arauna-en_modern.elf")], text=True)
for line in symbol_text.splitlines():
    fields = line.split()
    if len(fields) == 3:
        SYMS[fields[2]] = int(fields[0], 16)
        ADDRESSES.setdefault(fields[2], []).append(int(fields[0], 16))
DEFS = dict(re.findall(r"^#define[ \t]+(\w+)[ \t]+([^\n]+)", "\n".join(p.read_text() for p in (R / "include/constants").glob("*.h")), re.M))
tmhm = (R / "include/constants/tms_hms.h").read_text()
tm_names = re.findall(r"F\((\w+)\)", tmhm.split("#define FOREACH_HM")[0])
hm_names = re.findall(r"F\((\w+)\)", tmhm.split("#define FOREACH_HM")[1].split("#define")[0])
for i, name in enumerate(tm_names):
    DEFS["ITEM_TM_" + name] = "ITEM_TM01 + " + str(i)
for i, name in enumerate(hm_names):
    DEFS["ITEM_HM_" + name] = "ITEM_HM01 + " + str(i)

def constant(name):
    expression = DEFS[name].split("//")[0].strip()
    expression = re.sub(r"\b[A-Za-z_]\w*\b", lambda m: str(constant(m[0])) if m[0] in DEFS else m[0], expression)
    if not re.fullmatch(r"[0-9a-fA-FxX()+* /|&~<>-]+", expression):
        raise ValueError((name, expression))
    return int(eval(expression, {"__builtins__": {}}))

LIB = C.CDLL(str(Q / "mgba_helper.so"))
LIB.boot.argtypes = [C.c_char_p]
LIB.invokex.argtypes = [C.c_uint32, C.POINTER(C.c_uint32), C.POINTER(C.c_uint32)]
LIB.rd.argtypes = [C.c_uint32, C.c_int]
LIB.rd.restype = C.c_uint32
LIB.wr.argtypes = [C.c_uint32, C.c_uint32, C.c_int]
LIB.pc.restype = C.c_uint32
for method in ("pixels", "exportsave", "importsave", "statewrite", "stateread"):
    getattr(LIB, method).argtypes = [C.c_char_p]

def call(name, *args):
    result = C.c_uint32()
    values = (C.c_uint32 * 8)(*(list(args) + [0] * 8)[:8])
    if not LIB.invokex(SYMS[name], values, C.byref(result)):
        raise RuntimeError((name, hex(LIB.pc())))
    return result.value

def read(address, size=4):
    return LIB.rd(SYMS.get(address, address), size)

def write(address, value, size=4):
    LIB.wr(SYMS.get(address, address), value, size)

def frames(keys=0, count=1):
    LIB.frames(keys, count)

def press(keys, count=2, release=20):
    frames(keys, count)
    frames(0, release)

def snapshot(name):
    raw = Q / (name + ".rgba")
    LIB.pixels(str(raw).encode())
    image = Image.frombytes("RGBA", (240, 160), raw.read_bytes())
    raw.unlink()
    image.save(Q / (name + ".png"))

def boot():
    assert LIB.boot(str(ROM).encode())
    frames(0, 750)

def fixture(map_name="LittlerootTown", x=10, y=8):
    call("NewGameInitData")
    call("ScriptContext_Stop")
    warp(map_name, x, y)

def warp(map_name, x, y):
    groups = json.loads((R / "data/maps/map_groups.json").read_text())
    for gi, group in enumerate(groups["group_order"]):
        if map_name in groups[group]:
            mi = groups[group].index(map_name)
            break
    else:
        raise ValueError(map_name)
    call("SetWarpDestination", gi, mi, 255, x, y)
    # SetWarpDestination takes signed 8-bit arguments, although WarpData
    # stores 16-bit coordinates. Preserve wide-map coordinates in the fixture.
    if x > 127 or y > 127:
        write(SYMS["sWarpDestination"] + 4, x, 2)
        write(SYMS["sWarpDestination"] + 6, y, 2)
    call("WarpIntoMap")
    call("SetMainCallback2", SYMS["CB2_LoadMap"] | 1)
    frames(0, 160)

def quantity(item):
    return call("CountTotalItemQuantityInBag", constant(item))

def flag(name):
    return call("FlagGet", constant(name))

def run_script(name, limit=2500, keys=1):
    call("ScriptContext_SetupScript", SYMS[name])
    frames(0, 15)
    for i in range(limit):
        frames(keys if i % 2 == 0 else 0, 2)
        if not call("ArePlayerFieldControlsLocked"):
            return i * 2 + 15
    snapshot("blocked_" + name)
    raise RuntimeError(("script timeout", name, hex(read("sGlobalScriptContext" + ""))))

def save(path):
    assert call("TrySavingData", 0) == 1
    assert LIB.exportsave(str(path).encode())

def restore(path):
    LIB.shutdownx()
    assert LIB.boot(str(ROM).encode())
    assert LIB.importsave(str(path).encode())
    frames(0, 750)
    for _ in range(12):
        press(1, release=120)
        if read(SYMS["gMain"] + 4) == SYMS["CB2_Overworld"] | 1:
            frames(0, 60)
            return
    snapshot("continue_failed")
    raise RuntimeError(("CONTINUE did not reach overworld", hex(read(SYMS["gMain"] + 4))))

def metadata():
    return {"rom_sha256": hashlib.sha256(ROM.read_bytes()).hexdigest(), "emulator": "mGBA 0.10.2", "fixture_setup": True}
