# Visible Emerald residue audit

This preparation adds a source-level audit that looks only inside player-facing string literals. It deliberately ignores implementation labels such as `MAP_LITTLEROOT_TOWN`, `TRAINER_WALLY_*`, object IDs and event names, because those are allowed to remain as the Emerald structural skeleton.

## What it reports

The audit scans map dialogue, global text, script text, `src/strings.c` and `src/battle_message.c` for visible legacy identities such as May/Brendan/Birch/Steven/Wally/Archie/Maxie/Scott, Team Aqua/Team Magma/Devon, Hoenn and the inherited Hoenn place names that already have Arauna replacements.

Pokémon species names are intentionally outside this audit. The technical cleanup must not silently redesign or rename species/fakemon content.

## Use

- `python3 tools/audit_visible_emerald_residue.py` prints every current hit without failing;
- `python3 tools/audit_visible_emerald_residue.py --json` emits machine-readable findings;
- `python3 tools/audit_visible_emerald_residue.py --fail-on-hit` becomes the final zero-residue gate once the remaining intentional findings are resolved or explicitly allowlisted.

## Integration plan

Keep this as preparation until GitHub Actions capacity is restored. After the active cleanup queue is green, rebase it onto the newest `main`, run the report, use its output to define the final focused narrative lots, then merge the audit infrastructure with a full ROM CI gate.
