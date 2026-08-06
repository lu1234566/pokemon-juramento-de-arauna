# Handoff — Pokémon: Juramento de Arauna

Written at the end of a long working session so the next one starts where this
one stopped. Everything below was verified against the repository, not
remembered.

Branch: `claude/project-error-scan-x96c5e` (PR #58). All work is committed and
pushed. **No build has been triggered** — the owner asked that the next build
already contain everything, to save Actions minutes.

---

## 1. What the project is

A ROM hack of Pokémon Emerald on pokeemerald-expansion: a Brazil-inspired
region called Arauna, darker and folkloric in tone, with 386 original fakemon.
English-first release.

Build: `make ARAUNA_LANGUAGE=ENGLISH -j$(nproc)` → `pokeemerald-en.gba`.

CI is `.github/workflows/build.yml`, two jobs:
- `repository-safety` — 35 checks, mirrored by `scripts/run_repository_safety.sh`
- `build-and-test` — builds the ROM

The ROM artifact (`pokeemerald-en-gba`) uploads **only on `workflow_dispatch`**,
per ADR-014. A pull_request run builds but never publishes, so a green PR run
gives the owner nothing to download.

---

## 2. Constraints that are easy to violate

These cost real time to discover. Treat them as hard rules.

**Var space is full.** `VARS_END = 0x40FF`. Adding a var grows SaveBlock1 and
breaks the save format. The Bond axes are packed 5 bits each into one var
(`VAR_ARAUNA_BOND_AXES`).

**Flags live in two headers.** `include/constants/flags.h` *and*
`include/config/arauna.h` both define `FLAG_ARAUNA_*`, and both compile.
Claiming a slot in one without checking the other silently gives two names to
one bit. `scripts/validate_flag_slot_collisions.py` now guards this — it exists
because five story flags landed on top of the Porto aliases at 0x4B–0x4F.

**Charmap.** `charmap.txt` maps characters to bytes. It has no em dash (use
`--`). `ã`/`õ`/`Ã`/`Õ` now have real glyphs at 0xF4/0xF5/0xF1/0xF2 — before this
session they were aliased onto plain `a`/`o` and the tilde was silently dropped
at assembly. `scripts/validate_script_charmap.py` checks every `.string` in
`data/` is encodable.

**The English text pack allows only `é` as non-ASCII**
(`tools/arauna/validate_english_runtime.py`). Use `...` not `…`.

**`scripts/check_localization.py` only scans `data/text/arauna/{en,pt_br}`** —
32-char visible lines, `$` termination, placeholder parity. Map scripts are not
covered by it, but `validate_script_charmap.py` does cover them.

**Renaming characters: touch only `.string` lines.** A global
`FLANNERY→BRÁS` once corrupted `TRAINER_FLANNERY_1` and
`FLAG_ENABLE_FLANNERY_MATCH_CALL`.

**`graphics/arauna/` is gitignored**, so the editable art pack never reaches a
CI checkout. Any check that reads it must skip when absent, not fail.

**Portuguese builds are blocked at the Makefile** (`$(error ...)`). The PT-BR
text pack is ~58% complete (142 of 245 labels); that is a known gap, not a break.

**`POKEDEX_PLUS_HGSS = FALSE`.** The vanilla Pokédex is what runs.
`src/pokedex_plus_hgss.c` carries an identical-looking copy of many things and
editing it changes nothing on screen.

**The upstream battle test suite cannot pass** and is marked
`continue-on-error`. It asserts on vanilla species names and data that Arauna
replaced. 2535 pass, 1896 fail, and none of the failures indicate a defect.

---

## 3. Story and progression state

Prologue, after this session's changes:

```
casa      night: talk to Dona Zila and Prof. Anahi → dawn
          (door is gated on FLAG_ARAUNA_PROLOGUE_NIGHT_COMPLETE)
vila      objective board says "go to the Research Center"
lab       three balls → story → prompt → givemon
          → AraunaPlayerHouse_EventScript_CompleteChoice
casa      return to Dona Zila → founding story (P08) → notebook → promise
rota      Mist Route → warp MAP_ROUTE104, 255, 16, 3
rustboro  Dona Celina at (18,55), on the entrance corridor
          → her trial gives FLAG_BADGE01_GET
          → Bento's gym
a pé      Rustboro → Route 115 → Route 114 (Serra do Uivo) → Fallarbor
```

`VAR_ARAUNA_STORY_STAGE` has per-value meaning, read by the village objective
board: 0 home, 1 Research Center, 2 Ciro, 3 Mist Route open, 6/7/8 later.
**`AraunaPlayerHouse_EventScript_Opening` sets it to 1 on the first step into
the house** — do not gate anything on `== 0` expecting it to mean "before the
night".

**Level cap** is `sLevelCapFlagMap` in `src/caps.c`, keyed on badge flags:
badge 1 → 15, badge 2 → 19, and so on. `FLAG_BADGE01_GET` is set by *both*
Celina's trial and the vanilla Rustboro gym. Celina must be met first or the
gym is a wall — which is why she stands on the entrance corridor.

Deliberately deferred, by the owner's own commit `0d3d4a4`: the First Link ruin
and chamber have no entrance. Not a regression.

Porto das Redes keeps its harbour, witnesses and Consortium agent, and is meant
to rejoin the route later, in its proper Emerald position.

---

## 4. Tools built this session

All wired into CI and the safety runner. Each exists because the defect it
catches actually shipped.

| tool | catches |
|---|---|
| `scripts/validate_inc_syntax.py` | detached/missing assembler directives (`.<tab>string`) |
| `scripts/validate_png_integrity.py` | PNG chunk CRC damage that aborts gbagfx |
| `scripts/validate_flag_slot_collisions.py` | two names on one flag/var slot |
| `scripts/validate_script_charmap.py` | `.string` content the charmap cannot encode |
| `scripts/validate_event_placement.py` | scripted coordinates inside walls |
| `scripts/validate_edge_transitions.py` | map-edge openings wider than their trigger |
| `scripts/validate_canonical_story.py` | founding stories, Bond system, payoffs |
| `tools/arauna/check_sprite_health.py` | solid canvas, stacked copies, undersized backs |
| `tools/arauna/repack_graphics_from_art_pack.py` | rebuilds the graphics header from the art pack |
| `tools/arauna/fix_sprite_transparency.py` | flood-fills a baked-in background to index 0 |
| `tools/arauna/add_tilde_glyphs.py` | keeps ã/õ glyphs from reverting to umlauts |
| `tools/arauna/set_dex_region_label.py` | keeps the Pokédex counter reading ARAUNA |

---

## 5. Graphics pipeline — the important part

`src/data/graphics/arauna_fakemon_graphics.h` holds, per species NNN:
`gAraunaFrontPic_NNN` (LZ77, 64x128 = two 64x64 frames), `gAraunaBackPic_NNN`
(LZ77, 64x64), `gAraunaPalette_NNN` and `gAraunaShinyPalette_NNN` (16 u16,
RGB555), `gAraunaIcon_NNN` (uncompressed, 32x64).

**Front, back and icon of one species share a single palette**, index order
included. The engine loads one palette for all three. This is the constraint
every conversion attempt has broken so far.

RGB555 to RGB: `(c & 31) * 8`, `((c >> 5) & 31) * 8`, `((c >> 10) & 31) * 8`.
Index 0 is transparent and never drawn.

### Back sprite status — the one open item

The shipped back sprites are wrong: for 175 of 386 species the art is a
**front-facing view**, so the player's Pokémon stares at the player in battle.
That is a content problem in the art pack, not a code defect — the committed
header faithfully matches the pack.

The owner is regenerating them. Three attempts so far:

1. **1254x1254 RGBA concept art** (9 species, and a 386 set on Drive at 55 MB).
   Art is good: genuine rear views, IoU against the front 0.35–0.50. Wrong
   format.
2. **160x144 RGB** from a screen converter — lost transparency, background
   baked to near-black. Rejected.
3. **64x64 RGBA**, transparency correct — but a Game Boy monochrome green
   palette replaced every colour. Rejected.
4. **64x64 4bpp indexed with PLTE and tRNS** — format finally correct, but
   remapped against the wrong palette: blues became browns, and yellow/cyan
   fringing appeared on edges.

**What is still needed:** each `NNN_nome_back.png` remapped against
`gAraunaPalette_NNN` — the same species, matched by file number. No global
palette, no shared palette, no new palette.

Curation threshold: mean colour error per species on a 0–441 scale. The
approved batch of 9 scored 12–20. Only 009 Petropico exceeded it at 36, because
its current palette has no room for the new art's greens; front and back share
a palette, so fixing that species means redoing both.

Note on transport: 386 sprites at 64x64 4bpp is **under 1 MB** and fits in chat.
Drive is unreachable from this environment — `drive.google.com` returns 403
through the proxy, and the Drive connector cannot list a folder by parent.

---

## 6. Still open

1. **Back sprites** — blocked on the palette pairing above.
2. **Rustboro has no identity of its own** — outside Celina and Bento it is
   still stock Emerald. No Arauna NPCs, signs or dialogue.
3. **Porto das Redes** is not on the route; it should rejoin after Rustboro.
4. **The house feels cramped** — reported in play, never diagnosed. Needs the
   owner to say what specifically bothers them.
5. Dead text left in place on purpose: a handful of labels orphaned by the
   teleport removal and the starter move. A few hundred bytes; not worth the
   churn in localisation files.

---

## 7. How to work here

Run `bash scripts/run_repository_safety.sh` before every commit. It is the same
35 checks CI runs, and it is fast.

When a validator fails after an intentional change, read what it was protecting
before editing it. Several encode design decisions rather than trivia — two of
them explicitly forbade a `givemon` at the Research Center, which was correct
until the owner asked for exactly that.

Verify a new check by reintroducing the defect and confirming the check names
it. Every tool listed above was verified that way.

Do not trigger builds without being asked. The owner is paying for Actions
minutes and wants each build to carry a complete batch of fixes.
