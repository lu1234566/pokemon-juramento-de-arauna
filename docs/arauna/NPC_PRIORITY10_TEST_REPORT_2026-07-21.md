# Priority-10 NPC pack — technical test report

Date: 2026-07-21
Branch: `agent/integrate-priority10-npcs-v3`
Canonical source: `arauna_npc_priority10_v3.zip`

## Asset validation performed

The supplied v3 archive was extracted in a clean temporary directory and validated independently from the repository.

- 10 editorial overworld sheets: 48×128, indexed PNG, 12 non-empty 16×32 cells.
- 10 engine overworld sheets: 144×32, indexed PNG, 9 non-empty 16×32 frames.
- 6 trainer portraits: 64×64 indexed PNG.
- Palette index 0 is transparent in every PNG.
- Every image uses at most 16 palette indices, all in the 0–15 range.
- Every supplied uncompressed `.4bpp` payload was regenerated from the indexed PNG and matched byte-for-byte: 10 overworld sheets and 6 trainer portraits.
- All supplied BGR555 palettes matched their canonical PNG palettes except the v3 Compliance Agent `.pal`, which was stale relative to the revised v3 PNG. A corrected external v3.1 source bundle was generated without changing any artwork, pixel index or frame.

The ROM integration compiles PNG assets through the repository graphics pipeline and does not import the stale standalone `.pal`, so that source-bundle defect does not alter the integrated ROM graphics.

## Repository integration inspected

- All 16 approved PNGs are present in the PR.
- The temporary `.integration/npc_v3` transfer payload is absent from the final diff.
- The dedicated validator is included in the repository safety suite and Project CI.
- Story bindings cover Dona Zila, Professor Anahi, both Ciro outfits, Dona Celina, Compliance Agent, dockworker, memorial fisher, Serra child and deaf hermit.
- The Libras guardrail remains explicit: no lexical LOOK / WAIT / SAFE animation was improvised.

## Build and runtime status

GitHub Actions was retried, but the runner created jobs with zero executable steps and no downloadable logs. The same infrastructure failure affected both the integration workflow and Project CI before repository commands started.

A clean local clone was also attempted, but the execution environment could not resolve `github.com`, so the full private repository could not be downloaded there.

Consequently, the asset payload and static integration checks are verified, while the following remain blocked by execution infrastructure rather than a known code failure:

- full English ROM compilation;
- engine test target;
- mGBA visual/runtime pass through Vila Amanhecer, Porto das Redes and Serra do Uivo.

The PR must remain a draft until those three runtime checks execute successfully.
