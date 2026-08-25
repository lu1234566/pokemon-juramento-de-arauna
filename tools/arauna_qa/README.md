# Arauna QA Harness

This directory is the operational layer for letting an external agent drive and inspect **Pokémon Juramento de Arauna** in mGBA without changing the retail ROM code.

The harness is deliberately opt-in. It uses mGBA's Lua scripting API plus the `.sym` file produced from the exact ROM build. The normal game source, flags, saves, maps and progression are untouched.

## What works

- TCP bridge between mGBA and Python on `127.0.0.1:8765`;
- A/B/Select/Start/D-pad/L/R input, including frame-counted presses;
- arbitrary 8/16/32-bit and range memory reads;
- screenshots, save-state save/load and reset;
- symbol resolution from the matching pokeemerald `.sym` output;
- structured runtime snapshots for map, player coordinates/direction/elevation, metatile behavior, weather/music, script state, field-control lock, battle state, callbacks and keys;
- repository map index resolving `(mapGroup,mapNum)` back to `data/maps/*/map.json`;
- structural validation of map layouts, events, connections and warp destinations;
- `step(DIR)` that verifies movement against runtime state rather than assuming a key press succeeded;
- static collision-grid decoding from `data/layouts/*/map.bin` using Emerald's 10-bit metatile / 2-bit collision / 4-bit elevation layout;
- A* path planning inside the current map;
- `walk_to(x, y)` / `walkto X Y` with runtime confirmation and replanning around dynamic blockers such as NPCs.

Static collision is intentionally only a planning hint. Runtime mGBA state is authoritative. If a tile that looks free in `map.bin` is blocked in the running game, the navigator retries once, records it as a dynamic obstacle, replans and continues. Unexpected movement, scripted displacement and map changes also force a re-evaluation.

The reader follows the current Emerald structures in `include/main.h`, `include/global.fieldmap.h`, `include/fieldmap.h` and `src/script.c`. Logical player coordinates subtract Emerald's `MAP_OFFSET` (7) from internal map-buffer coordinates.

## Requirements

- mGBA 0.10.x or newer with Lua scripting support;
- Python 3.10+;
- a locally built Arauna ROM and its matching `.sym` file.

For the official Arauna English build, build the ROM and symbols in the same wrapper invocation so the overlay composition is identical:

```bash
bash scripts/build_arauna.sh -j2 all syms
```

Never mix a `.sym` file from one build with a different `.gba`.

## Non-destructive live smoke test

Start the smoke listener first:

```bash
python3 tools/arauna_qa/smoke_test.py \
  --sym /path/to/matching/game.sym \
  --screenshot /tmp/arauna-smoke.png
```

Then open the matching ROM in mGBA and load `tools/arauna_qa/bridge.lua` from **Tools -> Scripting...**. The smoke runner checks the TCP handshake, ROM game code, symbol-backed runtime reads and an optional screenshot. It does not press a gameplay button or write game RAM.

A successful run exits with status 0 and prints JSON with `"ok": true`.

## Interactive mode

Start the Python listener from the repository checkout:

```bash
python3 tools/arauna_qa/arauna_qa.py --sym /path/to/matching/game.sym
```

If the controller is executed from outside the checkout, pass `--repo /path/to/pokemon-juramento-de-arauna`.

Open the matching ROM in mGBA, then load:

```text
tools/arauna_qa/bridge.lua
```

### Interactive commands

```text
state
map
step UP
walk RIGHT RIGHT UP
walkto 10 12
info
ping
press A 3
keys LEFT B
release
screenshot /tmp/arauna.png
save /tmp/arauna.ss0
load /tmp/arauna.ss0
reset
quit
```

`walkto X Y` currently plans only inside the current map. Entering a warp or connection that changes `(mapGroup,mapNum)` terminates the command with `reason: "map_changed"`; cross-map route planning is a later layer.

`press KEY [frames]` holds the requested key(s) for the specified number of emulated frames and waits through one release frame before returning. `keys` is a persistent manual hold and should be followed by `release`.

One-shot state/map dumps are also available:

```bash
python3 tools/arauna_qa/arauna_qa.py --sym /path/to/matching/game.sym --once state
python3 tools/arauna_qa/arauna_qa.py --sym /path/to/matching/game.sym --once map
```

## Repository-only map audit

No emulator is required to inspect map/event/warp structure:

```bash
python3 tools/arauna_qa/repo_audit.py --repo .
```

## Run the host-side tests

From `tools/arauna_qa`:

```bash
python3 -m unittest discover -s tests -v
```

The suite covers symbol parsing, runtime-state decoding, GBA input masks, socket protocol round trips, repository-map resolution/auditing, map-bin collision decoding, state-confirmed movement, A* planning, dynamic-blocker replanning and warp termination. These tests do not require mGBA or the ARM toolchain.

## Safety boundaries

The harness intentionally does **not** expose generic game-RAM writes. Normal GBA key state is the only autonomous gameplay mutation; save-state load/reset are explicit commands. This keeps black-box QA useful while avoiding accidental changes to flags, variables, party data or saves.

The TCP listener binds to `127.0.0.1` by default. Do not expose it publicly.

## Next layers

1. live mGBA smoke-test evidence for this PR;
2. runtime collision exploration and map coverage recording;
3. cross-map path planning through connections and warps;
4. loop/softlock detector;
5. NPC/interactable selection and scripted objective execution;
6. battle/party decoder and battle decision layer;
7. deterministic scenario files plus screenshot/state reports;
8. autonomous campaign agent loop.

If source-level instrumentation becomes necessary later, add it as a separate QA-only build. The current bridge does not require such instrumentation.
