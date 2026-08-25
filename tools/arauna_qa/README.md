# Arauna QA Harness

This directory is the first operational layer for letting an external agent drive and
inspect **Pokémon Juramento de Arauna** in mGBA without changing the retail ROM code.

The harness is deliberately opt-in. It uses mGBA's Lua scripting API plus the `.sym`
file produced from the exact ROM build. The normal game source, flags, saves, maps and
progression are untouched.

## What works in V1

- TCP bridge between mGBA and Python on `127.0.0.1:8765`;
- A/B/Select/Start/D-pad/L/R input, including frame-counted presses;
- arbitrary 8/16/32-bit and range memory reads;
- screenshots;
- save-state save/load;
- emulator reset and basic ROM/frame information;
- symbol resolution from pokeemerald `.sym` output;
- structured snapshots of:
  - map group/number (when the player object exists),
  - player logical and internal coordinates,
  - facing/movement direction and elevation,
  - current metatile behavior,
  - map layout/section/type/weather/music,
  - field-control lock,
  - script status/mode/pointer when local symbols are present,
  - battle state,
  - held/new keys and main callbacks.

The reader follows the current Emerald structures in `include/main.h`,
`include/global.fieldmap.h`, `include/fieldmap.h` and `src/script.c`. The logical player
coordinates subtract Emerald's `MAP_OFFSET` (7) from the internal map-buffer
coordinates.

## Requirements

- mGBA 0.10.x or newer with Lua scripting support;
- Python 3.10+;
- a locally built Arauna ROM and its matching `.sym` file.

Generate symbols for the same build that you open in mGBA:

```bash
make syms
```

If the official Arauna wrapper builds into a different output directory/name, use the
`.sym` produced beside that exact `.elf`/`.gba`. Never mix symbols from another build.

## Start it

1. Start the Python listener:

```bash
python3 tools/arauna_qa/arauna_qa.py --sym /path/to/matching/pokeemerald.sym
```

2. Open the matching ROM in mGBA.
3. In mGBA, open **Tools -> Scripting...** and load:

```text
tools/arauna_qa/bridge.lua
```

The Lua side connects only to localhost by default.

## Interactive commands

```text
state
info
ping
press UP
press A 3
keys LEFT B
release
screenshot /tmp/arauna.png
save /tmp/arauna.ss0
load /tmp/arauna.ss0
reset
quit
```

`press KEY [frames]` holds the requested key(s) for the specified number of emulated
frames and waits through one release frame before returning. `keys` is a persistent
manual hold and should be followed by `release`.

A one-shot state dump is also available:

```bash
python3 tools/arauna_qa/arauna_qa.py \
  --sym /path/to/matching/pokeemerald.sym \
  --once state
```

Then load `bridge.lua` in mGBA. The process prints one JSON snapshot and exits.

## Run the host-side tests

From this directory:

```bash
python3 -m unittest discover -s tests -v
```

These tests do not require mGBA or the ARM toolchain.

## Safety boundaries

V1 intentionally does **not** write game RAM. The only input mutation is the normal
GBA key state; save-state load/reset are explicit commands. This keeps the first
integration useful for black-box QA while avoiding accidental changes to flags,
variables, party data or saves.

The TCP listener binds to `127.0.0.1` by default. Do not expose it publicly.

## Next layers

The next implementation stages can build on this without replacing the bridge:

1. `walk_to(x, y)` plus pathfinding and collision exploration;
2. map/event/warp extraction from the repository and comparison with runtime state;
3. softlock/loop detection from repeated state snapshots;
4. battle/party decoding;
5. deterministic YAML/JSON test scenarios;
6. screenshot + state reports;
7. an agent loop that chooses actions and plays through objectives automatically.

If source-level instrumentation becomes necessary later, add it as a separate
QA-only build. The V1 bridge does not require such instrumentation.
