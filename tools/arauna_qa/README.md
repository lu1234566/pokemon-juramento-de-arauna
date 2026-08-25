# Arauna QA Harness

This directory is the opt-in operational layer for letting an external agent drive and inspect **Pokémon Juramento de Arauna** in mGBA without changing retail game code.

The harness uses mGBA's Lua scripting API plus the `.sym` file produced by the exact ROM build. Normal game source, flags, saves, maps and progression remain untouched; autonomous gameplay is performed with ordinary GBA input.

## Current capabilities

### Emulator bridge and runtime state

- TCP bridge between mGBA and Python on `127.0.0.1:8765`;
- A/B/Select/Start/D-pad/L/R input, including frame-counted presses and no-input frame advances;
- arbitrary 8/16/32-bit and range memory reads;
- screenshots, save-state save/load and reset;
- symbol resolution from the matching pokeemerald `.sym` output;
- structured runtime snapshots for map, player coordinates/direction/elevation, metatile behavior, weather/music, script state, field-control lock, battle state, callbacks and keys.

### Maps, movement and world navigation

- repository map index resolving `(mapGroup,mapNum)` back to `data/maps/*/map.json`;
- structural validation of map layouts, events, connections and warp destinations;
- static collision-grid decoding from `data/layouts/*/map.bin` using Emerald's 10-bit metatile / 2-bit collision / 4-bit elevation layout;
- runtime-confirmed `step(DIR)` and A* `walk_to(x, y)`;
- dynamic-blocker replanning around NPCs and unexpected runtime obstacles;
- static world graph through map connections and warps;
- `route TARGET_MAP` for route inspection;
- `routeto TARGET_MAP` / scenario `goto_map` for verified cross-map execution one transition at a time.

Static collision is only a planning hint. Runtime mGBA state is authoritative. Unexpected movement, scripted displacement, blockers, battle entry or map transitions cause the navigator to re-evaluate instead of assuming a key press succeeded.

### NPC and interactable QA

- live decoding of Emerald `gObjectEvents` slots;
- current object coordinates, local ID, map identity, direction, visibility, movement/trainer metadata and metatile behavior;
- `objects` to inspect live objects;
- `talk OBJECT_INDEX` / `talklocal LOCAL_ID`;
- safe approach to moving NPCs while avoiding known trigger coordinates;
- normal D-pad facing and A-button interaction;
- interaction is considered successful only with observable runtime evidence such as script start, field lock, battle start, map change or selected object event.

### Party and battle inspection

- Gen 3 party decryption using personality/OT ID XOR, all 24 secure substruct orders and checksum validation;
- player and enemy party snapshots;
- live `gBattleMons` decoding including species, HP, level, stats, moves, PP, types, ability, status and stat stages;
- `gBattleMoves` metadata and the ROM's own `gTypeEffectiveness` table;
- conservative move advisor based on power, accuracy, STAB and actual type effectiveness.

The advisor is intentionally not a full reimplementation of Emerald's AI. Status strategy, every move effect, held items and ability interactions are not yet fully scored.

### Verified battle control

- battle prompt detection through `gBattleBufferA`, controller execution flags and real action/move cursors;
- `battleprompt` for inspecting the active player prompt;
- `battlechoose SLOT` for a specific move slot;
- `battleauto` for one recommended decision;
- `playbattle [MAX_TURNS]` for a bounded autonomous single battle;
- no blind A/B confirmation when the battle controller reaches an unknown prompt;
- explicit safe aborts for unsupported double-battle/manual-target states and stalled unknown states.

`playbattle` only submits a move while a verified player action prompt is active. Between decisions it advances emulation with no key held. `MAX_TURNS` caps submitted player decisions; the final allowed move is still given time to finish and end the battle.

## Requirements

- mGBA 0.10.x or newer with Lua scripting support;
- Python 3.10+;
- a locally built Arauna ROM and its matching `.sym` file.

Build ROM and symbols together so they describe the same binary:

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

Useful commands:

```text
state
map
objects
step UP
walk RIGHT RIGHT UP
walkto 10 12
route MAP_ID
routeto MAP_ID
talk 3
talklocal 7
party
enemy
battle
battleprompt
advise
battlechoose 2
battleauto
playbattle 64
scenario tools/arauna_qa/scenarios/current_single_battle_smoke.json
press A 3
keys LEFT B
release
screenshot /tmp/arauna.png
save /tmp/arauna.ss0
load /tmp/arauna.ss0
info
ping
reset
quit
```

`press KEY [frames]` holds the requested key(s) for the specified number of emulated frames and waits through one release frame before returning. `keys` is a persistent manual hold and should be followed by `release`.

One-shot state/map dumps are also available:

```bash
python3 tools/arauna_qa/arauna_qa.py --sym /path/to/matching/game.sym --once state
python3 tools/arauna_qa/arauna_qa.py --sym /path/to/matching/game.sym --once map
```

## Declarative scenarios

A scenario is JSON with an ordered `steps` array. Supported actions are:

- `goto_map`;
- `walk_to`;
- `talk` by `object_index` or `local_id`;
- `play_battle` (alias `playbattle`);
- `press`;
- `wait`;
- `screenshot`;
- `assert`.

Assertions currently support map ID plus `player_x`, `player_y`, `in_battle`, `script_enabled`, `field_controls_locked` and `player_valid`.

Example battle step:

```json
{
  "action": "play_battle",
  "max_turns": 64,
  "max_cycles": 2048,
  "wait_frames": 4,
  "stall_cycles": 100
}
```

Included scenarios:

- `scenarios/current_single_battle_smoke.json` — run after manually entering a supported single battle; captures before/after screenshots and requires the battle to end;
- `scenarios/npc_battle.template.json` — end-to-end template for `goto_map -> talk -> assert battle -> play_battle -> assert battle ended`. Replace its map/local-ID placeholders with a real trainer from the build under test before running.

Scenario execution stops on the first failed step unless that step explicitly sets `"continue_on_failure": true`.

## Repository-only map audit

No emulator is required to inspect map/event/warp structure:

```bash
python3 tools/arauna_qa/repo_audit.py --repo .
```

## Host-side tests

From `tools/arauna_qa`:

```bash
python3 -m unittest discover -s tests -v
```

The suite covers symbol parsing, runtime-state decoding, GBA input masks, socket protocol round trips, repository-map resolution/auditing, map-bin collision decoding, confirmed movement, A* planning, dynamic blockers, cross-map routing, live object decoding, NPC interaction, Gen 3 party decryption, battle state decoding, move advice, verified battle-menu input, bounded battle autoplay and declarative battle scenarios. These tests do not require mGBA or the ARM toolchain.

## Safety boundaries

The harness intentionally does **not** expose generic game-RAM writes. Normal GBA key state is the only autonomous gameplay mutation; save-state load/reset remain explicit commands. This keeps black-box QA useful while avoiding accidental direct changes to flags, variables, party data or saves.

The TCP listener binds to `127.0.0.1` by default. Do not expose it publicly.

## Remaining validation / next layers

1. live mGBA handshake and smoke evidence against the exact Arauna ROM + `.sym` pair;
2. first real end-to-end Arauna trainer scenario;
3. screenshot/state failure bundle with automatic reproduction trace;
4. explicit handling of safe dialogue/Yes-No prompts without blind confirmation;
5. double-battle targeting and switching/items only after their prompt state can be verified as strictly as move selection;
6. campaign-level objective definitions and long-form progression coverage;
7. optional deterministic QA build features (fixed RNG seed / debug-only observability) if black-box state proves insufficient.

If source-level instrumentation becomes necessary later, it should remain a separate QA-only build. The current bridge does not require source modifications to the retail game.
