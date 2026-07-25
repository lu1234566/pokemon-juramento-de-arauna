# Priority-10 NPC pack v3 integration

## Source selection

**v3 is canonical.** The v2 archive was used only for comparison. The only art revision between the two packages is the Compliance Agent, whose v3 design reads as a corporate environmental auditor rather than a conventional villain-team member.

## Integrated overworld characters

- Dona Zila;
- Professor Anahi;
- Ciro, prologue clothing;
- Ciro, Consortium clothing;
- Dona Celina;
- Compliance Agent;
- dockworker;
- memorial fisher;
- Serra child.

The deaf hermit is intentionally excluded: its v3 portrait was rejected in ADR-024 visual review and is pending regeneration.

All nine use dedicated object-event graphics IDs and are assigned by narrative script, not by globally replacing Emerald NPC classes.

## Integrated trainer portraits

Six unused Frontier Brain portrait slots in the Arauna campaign are repurposed without changing the global trainer-picture table: Anabel stores Anahi, Tucker stores prologue Ciro, Noland stores Consortium Ciro, Greta stores Dona Celina, Lucy stores the Compliance Agent, and Spenser stores the deaf hermit (regenerated portrait, approved after the ADR-024 revision). Current story battles use Tucker, Lucy, Greta and Spenser. Anahi and Consortium Ciro remain installed for later story battles. The deaf hermit's overworld sprite stays on the reused vanilla gentleman, since a single static render cannot supply a directional 16x32 walk sheet.

## Overworld palette adaptation

Emerald normally keeps only four shared NPC palettes and one swappable special-NPC palette available. Multiple competing special palettes cannot coexist on one map. To keep Porto and the Serra stable, the pack's overworld pixel geometry is retained while each sheet is remapped to the closest shared Emerald NPC palette. Trainer portraits preserve their supplied indexed palettes because battle portraits load independently.

- `agente_conformidade` → shared Emerald NPC palette 4
- `ciro_consorcio` → shared Emerald NPC palette 4
- `ciro_prologo` → shared Emerald NPC palette 4
- `crianca_serra` → shared Emerald NPC palette 1
- `dona_celina` → shared Emerald NPC palette 1
- `dona_zila` → shared Emerald NPC palette 1
- `eremita_surdo` → shared Emerald NPC palette 1
- `pescador_memorial` → shared Emerald NPC palette 4
- `professora_anahi` → shared Emerald NPC palette 4
- `trabalhador_cais` → shared Emerald NPC palette 4

The original v3 palette files remain the art-direction reference for a later engine-wide palette expansion, but this implementation prioritizes correct simultaneous rendering on original GBA constraints.

## Libras safety gate

The normal child and hermit overworlds are installed. **No improvised LOOK / WAIT / SAFE animation** is implemented. Lexical sign animations remain blocked until video reference, handshape/orientation/movement verification and review by a fluent Libras user or specialist are available.

## Validation

`scripts/validate_priority10_npcs.py` checks PNG format, dimensions and transparency, map-to-character wiring, dedicated object IDs, repurposed campaign portrait slots, current story-battle portraits, the v3 Agent gender, and the Libras animation block.
