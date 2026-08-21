# Casa da Cinza + Nara — English story surface

## Scope

This pass completes the mandatory Lavaridge-facing surface as **CASA DA CINZA** after the already-active Serra da Cinza / Mt. Chimney conflict layer.

It owns 59 text blocks:

- 19 in `data/maps/LavaridgeTown/scripts.inc`;
- 39 in `data/maps/LavaridgeTown_Gym_1F/scripts.inc`;
- 1 route-sign block in `data/maps/MtChimney/scripts.inc`.

The Casa da Cinza renderer runs after the existing Mt. Chimney surface renderer, so the downhill route sign finishes as **CASA DA CINZA** rather than the older `SERTAO DE DENTRO` placeholder. It can also render the clean vanilla sign directly.

## Casa da Cinza

The settlement is framed around heat, ash, old losses, hot springs, rest and recovery. Grief is explicitly treated as something that can be carried and observed rather than erased or romanticized.

The inherited hot-spring and Egg interactions keep their mechanics while the visible writing is brought into the Arauna tone.

## Ciro after Badge 04

Both inherited May/Brendan post-Gym slots render the same Ciro dialogue.

Ciro remains HORIZON-aligned. He refuses to live only inside what he lost and still believes BOND measurements may reduce harm, but his position is not written as proof that data can replace consent or context.

The inherited GO-GOGGLES reward and return toward PAMPA DA ESPERA remain mechanically unchanged.

## Nara

Nara inherits the Flannery functional slot without inheriting Flannery's personality.

Her Gym language is about controlled heat, pressure, cooling, evidence and consequence. Ash is not treated as empty residue: it records that something changed and that something was lost.

The visible fourth badge is **ASH BADGE**, translating the established `INSÍGNIA CINZA` concept. Internal `FLAG_BADGE04_GET` and all Emerald badge-order logic remain unchanged.

TM50 remains OVERHEAT. Its visible explanation reinforces the same idea: power has a cost.

## Preserved internals

The renderer checks that these progression surfaces do not change:

- `ITEM_GO_GOGGLES` / `FLAG_RECEIVED_GO_GOGGLES`;
- `VAR_LAVARIDGE_TOWN_STATE`;
- the inherited Wynaut Egg flow;
- hot-spring game statistic;
- `TRAINER_FLANNERY_1` and all eight inherited Gym trainer IDs;
- `FLAG_DEFEATED_LAVARIDGE_GYM`;
- `FLAG_BADGE04_GET`;
- `ITEM_TM_OVERHEAT` / `FLAG_RECEIVED_TM_OVERHEAT`;
- `FLAG_ENABLE_FLANNERY_MATCH_CALL`;
- `FLAG_WHITEOUT_TO_LAVARIDGE`.

No warps, map geometry, trainer teams, movement, triggers, save IDs or progression graph are changed.

## Renderer contract

`scripts/render_casa_da_cinza_nara_en_checked.py`:

- reads one plain UTF-8 JSON bank;
- requires exactly 19 town labels, 39 Gym labels and 1 ridge-sign label;
- replaces only exact labeled text bodies;
- supports historical assembler line continuations;
- is idempotent;
- validates a conservative 32-character visible width;
- requires final `$` termination;
- masks all target bodies and proves non-dialogue structure is byte-stable;
- preserves progression-token counts;
- rejects visible Lavaridge / Flannery / old Portuguese residue inside owned blocks;
- requires both gender-dependent rival slots to render identical Ciro dialogue.

## Validation

Validated locally without GitHub Actions:

- Python compile: PASS;
- conservative text-width validation: PASS;
- synthetic `--check -> --in-place -> --check`: 59/59 PASS;
- historical multiline `.string` continuation: PASS;
- adjacent `.align 2` boundary sentinels on all three target files: PASS;
- Ciro gender-slot equality: PASS;
- NARA / CASA DA CINZA / ASH BADGE identity requirements: PASS.

A full GBA ROM toolchain build is not part of this pass.

PR #58 remains outside scope.
