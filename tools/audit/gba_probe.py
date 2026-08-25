#!/usr/bin/env python3
"""Read and write a running mGBA's memory, addressed by source symbol.

mGBA 0.10's SDL frontend has no Lua, but `mgba -g` exposes a GDB remote stub
on port 2345, and the linked ELF carries every symbol the decompilation
defines. Together that is enough to ask the running game what it is doing --
which main callback is active, which map the player is on -- instead of
pressing buttons blind and hoping the timing lands.

    from gba_probe import Probe
    with Probe() as p:
        p.run(0.5)
        print(p.callback2_name(), p.location())
"""
from __future__ import annotations

import json
import pathlib
import socket
import struct
import subprocess
import time

ROOT = pathlib.Path(__file__).resolve().parents[2]
ELF = ROOT / "pokemon-juramento-de-arauna-en_modern.elf"
CACHE = ROOT / "build" / "arauna-en" / "symbols.json"

# Offsets into struct SaveBlock1 / SaveBlock2, from include/global.h.
SB1_POS = 0x00          # struct Coords16 pos
SB1_LOCATION = 0x04     # struct WarpData location {s8 mapGroup, mapNum; s16 x,y,warpId}
SB1_PARTY_COUNT = 0x234
SB2_NAME = 0x00         # u8 playerName[PLAYER_NAME_LENGTH + 1]
SB1_FLAGS = 0x1270      # u8 flags[NUM_FLAG_BYTES]
# Emerald keeps the "seen" bits in three places and cross-checks them, so
# writing only SaveBlock2's copy leaves GetNationalPokedexCount at zero and the
# start menu silently refuses to open the Pokedex.
SB1_SEEN1 = 0x988
SB1_SEEN2 = 0x3B24
SB1_VARS = 0x139C       # u16 vars[VARS_COUNT], indexed from VARS_START 0x4000
VAR_NATIONAL_DEX = 0x4046
VARS_START = 0x4000
SB2_POKEDEX = 0x18      # struct Pokedex
DEX_MODE = SB2_POKEDEX + 0x01
DEX_NATIONAL_MAGIC = SB2_POKEDEX + 0x02   # must be 0xDA for National mode
DEX_OWNED = SB2_POKEDEX + 0x10
DEX_SEEN = SB2_POKEDEX + 0x44
DEX_FLAG_BYTES = 0x34
FLAG_SYS_POKEDEX_GET = 0x861              # SYSTEM_FLAGS + 0x1
FLAG_SYS_NATIONAL_DEX = 0x896             # SYSTEM_FLAGS + 0x36

# struct Task {TaskFunc func; bool8 isActive; u8 prev, next, priority; s16 data[16];}
TASK_SIZE = 40
TASK_IS_ACTIVE = 4
NUM_TASKS = 16


def load_symbols(elf: pathlib.Path = ELF) -> dict[str, int]:
    if CACHE.is_file() and CACHE.stat().st_mtime >= elf.stat().st_mtime:
        return {k: int(v) for k, v in json.loads(CACHE.read_text()).items()}
    out = subprocess.run(["arm-none-eabi-nm", str(elf)], capture_output=True, text=True)
    if out.returncode:
        raise SystemExit(f"nm failed on {elf}: {out.stderr.strip()}")
    table: dict[str, int] = {}
    for line in out.stdout.splitlines():
        parts = line.split()
        if len(parts) == 3:
            table[parts[2]] = int(parts[0], 16)
    CACHE.parent.mkdir(parents=True, exist_ok=True)
    CACHE.write_text(json.dumps(table))
    return table


class Probe:
    """A GDB remote client scoped to what a game audit needs."""

    def __init__(self, host: str = "127.0.0.1", port: int = 2345, timeout: float = 10.0):
        self.sym = load_symbols()
        self.by_addr = {v: k for k, v in self.sym.items()}
        self.sock = socket.create_connection((host, port), timeout=timeout)
        self._halted = True
        self._packet("?")

    # -- plumbing ---------------------------------------------------------
    def _packet(self, command: str) -> str:
        checksum = sum(command.encode()) & 0xFF
        self.sock.sendall(b"$" + command.encode() + b"#" + b"%02x" % checksum)
        buf = b""
        while True:
            chunk = self.sock.recv(65536)
            if not chunk:
                raise ConnectionError("mGBA closed the GDB connection")
            buf += chunk
            if buf.count(b"#") and len(buf.rsplit(b"#", 1)[-1]) >= 2:
                break
        return buf.split(b"$", 1)[1].rsplit(b"#", 1)[0].decode()

    def cont(self) -> None:
        """Resume the game. Input is only consumed while it is running."""
        if not self._halted:
            return
        self.sock.sendall(b"$c#63")
        self._halted = False

    def halt(self) -> None:
        """Stop again so memory reads see a stable frame."""
        if self._halted:
            return
        self.sock.sendall(b"\x03")
        time.sleep(0.15)
        self.sock.setblocking(False)
        try:
            self.sock.recv(65536)
        except BlockingIOError:
            pass
        finally:
            self.sock.setblocking(True)
        self._halted = True

    def run(self, seconds: float) -> None:
        self.cont()
        time.sleep(seconds)
        self.halt()

    # The stub answers a bounded packet, so long reads are split.
    CHUNK = 128

    def read(self, addr: int, size: int) -> bytes:
        out = bytearray()
        while size:
            take = min(size, self.CHUNK)
            reply = self._packet("m%x,%x" % (addr, take))
            if reply.startswith("E") or len(reply) != take * 2:
                raise IOError(f"bad read of {take}B at {addr:#x}: {reply!r}")
            out += bytes.fromhex(reply)
            addr += take
            size -= take
        return bytes(out)

    def write(self, addr: int, data: bytes) -> None:
        self._packet("M%x,%x:%s" % (addr, len(data), data.hex()))

    def u8(self, addr: int) -> int: return self.read(addr, 1)[0]
    def u16(self, addr: int) -> int: return struct.unpack("<H", self.read(addr, 2))[0]
    def u32(self, addr: int) -> int: return struct.unpack("<I", self.read(addr, 4))[0]

    # -- game state -------------------------------------------------------
    def callback2_name(self) -> str:
        """The active MainCB2, resolved to its symbol -- the state signal."""
        addr = self.u32(self.sym["gMain"] + 4)
        return self.by_addr.get(addr & ~1, hex(addr))

    def _save_block(self, which: str) -> int | None:
        ptr = self.u32(self.sym[which])
        return ptr if 0x02000000 <= ptr < 0x02040000 else None

    def location(self) -> tuple[int, int, int, int] | None:
        """(mapGroup, mapNum, x, y), or None before the save block exists."""
        sb1 = self._save_block("gSaveBlock1Ptr")
        if sb1 is None:
            return None
        x, y = struct.unpack("<hh", self.read(sb1 + SB1_POS, 4))
        group, num = struct.unpack("<bb", self.read(sb1 + SB1_LOCATION, 2))
        return group, num, x, y

    def party_count(self) -> int | None:
        sb1 = self._save_block("gSaveBlock1Ptr")
        return None if sb1 is None else self.u8(sb1 + SB1_PARTY_COUNT)

    def player_name(self) -> str | None:
        sb2 = self._save_block("gSaveBlock2Ptr")
        if sb2 is None:
            return None
        return decode(self.read(sb2 + SB2_NAME, 8))

    def active_tasks(self) -> list[str]:
        """Names of the running tasks.

        The whole opening -- Anahi's speech, the gender choice, the naming
        screen -- runs as tasks under CB2_MainMenu, so the main callback never
        changes and cannot be used to follow it. The task list can.
        """
        base = self.sym["gTasks"]
        blob = self.read(base, TASK_SIZE * NUM_TASKS)
        out = []
        for i in range(NUM_TASKS):
            entry = blob[i * TASK_SIZE:(i + 1) * TASK_SIZE]
            if not entry[TASK_IS_ACTIVE]:
                continue
            func = struct.unpack("<I", entry[:4])[0]
            out.append(self.by_addr.get(func & ~1, hex(func)))
        return out

    def warp(self, map_group: int, map_num: int, x: int = 5, y: int = 5) -> None:
        """Move the player to any map by writing the destination and reloading.

        CB2_LoadMap builds the field from gSaveBlock1Ptr->location, so setting
        that and handing the main callback back to it is a warp -- no Fly, no
        badge, no walking. struct WarpData is
        {s8 mapGroup, mapNum, warpId; s16 x, y} and warpId -1 means "use the
        coordinates rather than a warp pad".
        """
        sb1 = self._save_block("gSaveBlock1Ptr")
        if sb1 is None:
            raise RuntimeError("warp needs a running save; boot into the field first")
        self.write(sb1 + SB1_POS, struct.pack("<hh", x, y))
        self.write(sb1 + SB1_LOCATION,
                   struct.pack("<bbbxhh", map_group, map_num, -1, x, y))
        self.write(self.sym["gMain"] + 0x438, b"\x00")          # struct Main.state
        self.write(self.sym["gMain"] + 4,
                   struct.pack("<I", self.sym["CB2_LoadMap"] | 1))

    def set_flag(self, flag: int) -> None:
        sb1 = self._save_block("gSaveBlock1Ptr")
        addr = sb1 + SB1_FLAGS + flag // 8
        self.write(addr, bytes([self.u8(addr) | (1 << (flag % 8))]))

    def set_var(self, var: int, value: int) -> None:
        sb1 = self._save_block("gSaveBlock1Ptr")
        self.write(sb1 + SB1_VARS + (var - VARS_START) * 2, struct.pack("<H", value))

    def unlock_pokedex(self, upto: int = 386) -> None:
        """Give the National Dex with every entry seen and caught.

        Entry bits are indexed by National Dex number minus one, the same way
        GetSetPokedexFlag indexes them, so this fills 1..upto.
        """
        sb2 = self._save_block("gSaveBlock2Ptr")
        if sb2 is None:
            raise RuntimeError("no save block yet")
        self.set_flag(FLAG_SYS_POKEDEX_GET)
        self.set_flag(FLAG_SYS_NATIONAL_DEX)
        self.write(sb2 + DEX_MODE, b"\x01")            # DEX_MODE_NATIONAL
        self.write(sb2 + DEX_NATIONAL_MAGIC, b"\xDA")
        # IsNationalPokedexEnabled wants all three: the magic byte, the flag,
        # and this var. Without it the dex silently falls back to Hoenn order
        # and shows national #252 as local #001.
        self.set_var(VAR_NATIONAL_DEX, 0x302)
        bits = bytearray(DEX_FLAG_BYTES)
        for dex in range(1, upto + 1):
            bits[(dex - 1) // 8] |= 1 << ((dex - 1) % 8)
        self.write(sb2 + DEX_OWNED, bytes(bits))
        self.write(sb2 + DEX_SEEN, bytes(bits))
        sb1 = self._save_block("gSaveBlock1Ptr")
        self.write(sb1 + SB1_SEEN1, bytes(bits))
        self.write(sb1 + SB1_SEEN2, bytes(bits))

    # struct PokedexView: pokedexList[NATIONAL_DEX_COUNT + 1] of 4 bytes,
    # then pokemonListCount, then selectedPokemon.
    DEX_VIEW_SELECTED = (386 + 1) * 4 + 2

    def dex_selected(self) -> int:
        """The National Dex number the open list is pointing at.

        Read only. Writing this field moves the cursor and the text but not the
        sprite -- the list loads that lazily as it scrolls -- so an injected
        jump shows the previous entry's artwork. Move the cursor with the D-pad
        instead; play.Session.dex_goto does that.
        """
        view = self.u32(self.sym["sPokedexView"])
        if not 0x02000000 <= view < 0x02040000:
            raise RuntimeError("the Pokedex is not open")
        return self.u16(view + self.DEX_VIEW_SELECTED) + 1

    def summary(self) -> str:
        loc = self.location()
        where = "map %d.%d at (%d,%d)" % loc if loc else "no save block"
        tasks = ", ".join(self.active_tasks()) or "-"
        return f"{self.callback2_name():<26} {where:<26} [{tasks}]"

    def close(self) -> None:
        try:
            self.sock.close()
        except OSError:
            pass

    def __enter__(self): return self
    def __exit__(self, *exc): self.close()


_CHARMAP: dict[int, str] = {}


def decode(raw: bytes) -> str:
    """Game charmap bytes to text, for reading names out of memory."""
    if not _CHARMAP:
        import re
        for line in (ROOT / "charmap.txt").read_text(encoding="utf-8").splitlines():
            line = line.split("@")[0].strip()
            m = re.match(r"^'(\\?.)'\s*=\s*([0-9A-Fa-f]{2})$", line)
            if m:
                char = m.group(1)
                _CHARMAP[int(m.group(2), 16)] = "'" if char == "\\'" else char
    out = []
    for byte in raw:
        if byte == 0xFF:
            break
        out.append(_CHARMAP.get(byte, "?"))
    return "".join(out)


if __name__ == "__main__":
    with Probe() as probe:
        for _ in range(6):
            print(probe.summary())
            probe.run(1.0)
