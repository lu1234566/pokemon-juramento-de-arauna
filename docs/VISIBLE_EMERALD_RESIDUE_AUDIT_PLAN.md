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

This preparation was recreated directly from current canonical `main` while GitHub Actions quota is exhausted. Use the report to define focused narrative lots; do not rename implementation identifiers. Codespaces remains a last-resort execution environment only if running the report becomes necessary to unblock prioritization.
