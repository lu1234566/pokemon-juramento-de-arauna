# Main readiness audit — 2026-08-23

## Scope

This audit closes the non-map implementation/readiness pass requested before moving to broader map and art work.

The audited build remains English-only and preserves the inherited Emerald technical skeleton. The pass is limited to visible/runtime text, UI labels, renderer/build infrastructure, policy gates, and documentation. It does not intentionally change map geometry, warps, trainer teams, progression flags, save format, rematch indices, or internal event identifiers.

Legacy PR #58 is explicitly out of scope and must remain untouched.

## Canonical build contract after this pass

- 66 English-only renderers in locked order: `scripts/english_renderers.txt`.
- 40 final transactional overlay files: `scripts/english_overlay_files_extra.txt`.
- 16/16 canonical visible stages in `scripts/check_arauna_story_coverage.py`.
- 346 final-gap runtime text blocks covered by the completion banks and PokéNav runtime accounting.
- Portuguese build inputs are rejected by `scripts/build_arauna.sh`.
- Static validation uses the official build wrapper through `scripts/check_arauna_static.sh`; the workflow no longer maintains a second partial renderer list.

## Concrete runtime gaps found and closed

### M'Boi → Oath Tower transition

`data/maps/CaveOfOrigin_B1F/scripts.inc` still exposed the original Wallace/Juan/Sootopolis/Groudon/Kyogre/Rayquaza/Cave of Origin/Mt. Pyre/Sky Pillar surface in an obligatory story transition.

The new checked renderer keeps the inherited event graph and internal symbols while replacing only the visible text with the Arauna surface led by AMALIA and the M'BOI / MEMORIAL / OATH TOWER route.

The associated `MULTI_WHERES_RAYQUAZA` menu keeps its internal multichoice ID but receives private Arauna-visible labels.

### Route 119 optional residue

`data/maps/Route119_House/scripts.inc` still named CAVE OF ORIGIN in optional NPC dialogue. The visible block is now aligned with M'BOI without changing the Wingull event or any map state.

### Route 105 PokéNav bridge

`data/maps/Route105/scripts.inc` still displayed DAD / NORMAN and DEVON's MR. STONE in a runtime PokéNav call.

The surface is now ELIAS / OTACILIO while the inherited registration/call path and internal identifiers remain unchanged.

### Abandoned Ship scanner sidequest

`data/maps/AbandonedShip_CaptainsOffice/scripts.inc` still sent the player to CAPT. STERN.

Only the three visible blocks in this office are owned by the readiness renderer. The quest now points to the HARBOR ENGINEER / PORTO DO SAL surface while preserving the scanner item/flag/event flow.

### Region-map landmarks

`src/landmark.c` still exposed several old-world landmark names even after the map-section names had been converted.

Only landmarks with already-established Arauna equivalences were changed. Current replacements include:

- MR. BRINEY'S COTTAGE → SAILOR'S COTTAGE
- SLATEPORT BEACH → PORTO DO SAL BEACH
- NEW MAUVILLE → OLD POWER RELAY
- METEOR FALLS → RUINAS DA QUEDA
- RUSTURF TUNNEL → GALERIAS SERRA
- SAFARI ZONE ENTRANCE → ARAUNA PRESERVE
- MT. PYRE → MEMORIAL NOMES
- SEAFLOOR CAVERN → CAVERNAS M'BOI
- GRANITE CAVE → GRUTA DAS VOZES
- SKY PILLAR → TORRE JURAMENTO
- MAGMA HIDEOUT → REMEMBRANCERS BASE

Generic landmarks without a settled Arauna identity were intentionally left unchanged rather than inventing new canon during a safety audit.

## Validator repairs

### Canonical static entrypoint

`scripts/check_arauna_static.sh` now exercises the same transactional render composition used by `scripts/build_arauna.sh`, then performs the remaining static checks without invoking the ARM compiler.

### CI source of truth

`.github/workflows/build.yml` no longer enumerates a stale subset of renderers. The repository-safety job calls the canonical static entrypoint instead. The separate build job still calls the official English build wrapper.

No GitHub Actions run is required or requested by this audit.

### Visible-residue scanner

The former residue scanners were from the transitional bilingual period and could incorrectly classify English itself as a problem. They are now compatibility wrappers around the English rendered-surface scanner.

`scripts/audit_rendered_visible_residue_en.py` inventories high-confidence stale speakers/identities, Portuguese residue, and legacy-place candidates after the official overlays are applied. Transactional critical identity/PT-BR survivors can fail the readiness pass.

### Localization compatibility

`scripts/check_localization.py` is no longer a bilingual contract gate. It delegates to the current English-only policy so obsolete PT-BR assumptions cannot contradict the official build.

## Documentation repair

`README.md` now describes the actual English-only build, official manifests, static-readiness entrypoint and remaining evidence requirements.

`docs/LOCALIZATION_CURRENT_STATE_2026_08_19.md` is retained as historical documentation and explicitly marked as superseded by the current English-only policy.

## Safety boundaries reviewed

This pass must not rename or remove inherited technical identifiers merely because they contain Emerald names. Examples include internal trainer constants, flags, vars, local IDs, map IDs, rematch slots and event labels. They remain valid implementation details when they are not displayed to the player.

The readiness renderer validates representative gameplay-token counts and masks its owned text blocks/menu/landmark definitions to ensure non-owned structure remains stable.

## Validation evidence and remaining evidence debt

### Source-level evidence completed in this audit

- manifest/policy counts reconciled to 66 renderers and 40 extra overlays;
- coverage accounting reconciled to 16/16 stages and 346 final-gap runtime blocks;
- final readiness sources are included in the transactional overlay set;
- CI duplicate renderer list removed;
- canonical documentation reconciled;
- branch commits use `[skip ci]` and the audit does not intentionally invoke GitHub Actions or Codespaces.

### Not claimed as executed

Two kinds of evidence remain separate from source-level readiness:

1. **Static runner execution** — `bash scripts/check_arauna_static.sh` should be executed from a real checkout capable of running the repository scripts. The current connector-only environment cannot execute the private repository checkout directly.
2. **ARM build and ROM playtest** — `bash scripts/build_arauna.sh -j2 all` plus emulator/device playtest remains required before calling the ROM itself release-tested.

This document deliberately does not claim either result without execution.

## Readiness conclusion

The implementation queue for the audited English-only narrative/visible-identity/build-infrastructure scope is closed at source level once this branch is integrated. Remaining work belongs to execution validation (static runner, ARM build, ROM playtest) and separate map/art/polish scopes, not to reopening the obsolete bilingual infrastructure or renaming Emerald internals.
