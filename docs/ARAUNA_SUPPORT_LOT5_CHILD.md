# Arauna support characters — lot 5

The Child of the Forest now has a distinct overworld identity in Mata do Meio and directly supports Ciro's narrative turning point.

Implementation:
- reuse `OBJ_EVENT_GFX_UNION_ROOM_NURSE` (ID 227), an optional multiplayer/Union Room visual slot outside the intended single-player campaign;
- replace that slot's 144x32 sheet with the converted Child of the Forest artwork remapped to the existing NPC_3 palette;
- assign the visual only to the existing Fortree/Mata do Meio child event;
- rewrite that child's dialogue so the player's later understanding of Ciro's doubts is grounded in an event he actually witnessed.

The child explains that a long-time companion Pokémon suddenly stopped recognizing them. Ciro witnessed the incident and could no longer answer with his usual confidence in HORIZONTE technology.

No coordinates, flags, warps, triggers, movement, trainer data or route progression are changed.
