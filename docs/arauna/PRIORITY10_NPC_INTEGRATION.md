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
| Memorial fisher | `OBJ_EVENT_GFX_OLD_MAN` / `old_man.png` | Porto memorial |
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

## Libras guardrail

The package documentation requires fluent review and video reference before implementing lexical signs. Specific LOOK / WAIT / SAFE animations are **not implemented** in this change. The Serra sequence keeps its existing non-lexical presentation and written explanation until validated references exist.

## Known architectural limitation

This first integration reuses existing Emerald graphics and trainer-picture IDs to avoid destabilizing the expansion's object tables. Those IDs can also appear in unconverted Hoenn content. Dedicated Arauna IDs remain a later cleanup task after the full map graph and character roster are stable.
