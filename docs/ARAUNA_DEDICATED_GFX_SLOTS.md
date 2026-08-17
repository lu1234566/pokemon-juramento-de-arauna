# Arauna dedicated overworld graphics slots

Three object-event graphics IDs explicitly marked unused by vanilla Pokémon Emerald are reclaimed for Arauna story characters without increasing `NUM_OBJ_EVENT_GFX`.

| Arauna constant | ID | Vanilla storage reclaimed | Runtime palette |
| --- | ---: | --- | --- |
| `OBJ_EVENT_GFX_DONA_ZILA` | 76 | `OBJ_EVENT_GFX_UNUSED_NATU_DOLL` | `NPC_3` |
| `OBJ_EVENT_GFX_CIRO_CONSORCIO` | 77 | `OBJ_EVENT_GFX_UNUSED_MAGNEMITE_DOLL` | `NPC_4` |
| `OBJ_EVENT_GFX_CIRO_FINAL` | 78 | `OBJ_EVENT_GFX_UNUSED_SQUIRTLE_DOLL` | `NPC_4` |

The inherited unused symbols remain the numeric storage at indices 76-78, while their graphics-info records are converted to standard 16x32 walking NPCs with nine overworld frames.

This reserves stable story-character IDs while keeping Emerald's one-byte object graphics ID format and the original `NUM_OBJ_EVENT_GFX` limit unchanged.
