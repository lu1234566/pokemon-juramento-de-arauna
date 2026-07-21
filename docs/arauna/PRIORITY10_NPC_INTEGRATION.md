# Priority-10 NPC pack integration

`arauna_npc_priority10_v3.zip` **v3 is canonical**. The v2 archive was used only for comparison. The v3 Compliance Agent is the approved corporate environmental auditor design.

## Runtime mapping

| Character | Overworld graphics ID / file | Story binding |
|---|---|---|
| Dona Zila | `OBJ_EVENT_GFX_MOM` / `mom.png` | Dona Zila's house |
| Professor Anahi | `OBJ_EVENT_GFX_REPORTER_F` / `reporter_f.png` | prologue house scene |
| Ciro, prologue | `OBJ_EVENT_GFX_CAMPER` / `camper.png` | Vila Amanhecer |
| Ciro, Consortium | `OBJ_EVENT_GFX_DEVON_EMPLOYEE` / `devon_employee.png` | Porto das Redes |
| Dona Celina | `OBJ_EVENT_GFX_OLD_WOMAN` / `old_woman.png` | Porto testimony arc |
| Compliance Agent | `OBJ_EVENT_GFX_SCIENTIST_1` / `scientist_1.png` | Consortium confrontation |
| Dockworker | `OBJ_EVENT_GFX_SAILOR` / `sailor.png` | Porto docks |
| Memorial fisher | `OBJ_EVENT_GFX_WALLACE` / `wallace.png` | Porto memorial |
| Serra child | `OBJ_EVENT_GFX_GIRL_1` / `girl_1.png` | Serra do Uivo Libras introduction |
| Deaf hermit | `OBJ_EVENT_GFX_GENTLEMAN` / `gentleman.png` | Route 114 ascent |

The original sheets were adapted to Emerald's four shared normal-NPC palettes. This preserves the 16-color GBA limit and avoids competing special-palette loads. The guide in Vila Amanhecer now uses `OBJ_EVENT_GFX_MAN_3` so the Compliance Agent art remains character-specific in the current slice.

## Battle portraits

Six approved 64×64 indexed portraits replace reserved trainer-art slots:

- Professor Anahi → Salon Maiden Anabel slot;
- Ciro, prologue → Dome Ace Tucker slot;
- Ciro, Consortium → Factory Head Noland slot;
- Dona Celina → Arena Tycoon Greta slot;
- Compliance Agent → Pike Queen Lucy slot;
- Deaf hermit → Palace Maven Spenser slot.

These files are compiled through the existing trainer-picture table, so no new image decompression path is introduced.

## Validation

The repository validator checks all sixteen PNG files for dimensions, indexed 8-bit encoding, transparent palette index zero, at most sixteen used palette indices, nine overworld frames and the eleven story bindings. It also rejects misspelled or absent map-object movement range fields. The same validator is part of both `scripts/run_repository_safety.sh` and the GitHub Actions repository-safety job.

A local package-level validation was executed on 2026-07-21. It passed ZIP integrity, manifest resolution, all ten indexed overworld sheets, all six indexed trainer portraits, nine distinct non-empty engine frames per NPC, byte-for-byte GBA 4bpp packing, BGR555 palette compatibility, 12-frame-to-9-frame mapping, the targeted v2-to-v3 Compliance Agent revision and the Libras guardrail.

GitHub Actions run `29790755324` was retried after this validation. Both jobs entered the queue but failed before their first workflow step, with no step list or downloadable log. This is an Actions startup/infrastructure blocker, not a compiler result. The PR remains draft until repository safety, the English ROM build and engine tests run in a clean checkout.

## Libras guardrail

The package documentation requires fluent review and video reference before implementing lexical signs. Specific LOOK / WAIT / SAFE animations are **not implemented** in this change. The Serra sequence keeps its existing non-lexical presentation and written explanation until validated references exist.

## Known architectural limitation

The memorial fisher uses the reserved Wallace overworld slot because Emerald's normal Old Man sheet exposes only three source frames. The other overworld characters and six battle portraits still reuse existing IDs, which can also appear in unconverted Hoenn content. Dedicated Arauna IDs remain a later cleanup task after the full map graph and character roster are stable.
