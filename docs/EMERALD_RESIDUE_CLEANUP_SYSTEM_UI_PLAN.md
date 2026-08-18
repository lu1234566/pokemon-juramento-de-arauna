# Arauna system/UI identity cleanup plan

A small set of shared player-facing strings can still reintroduce Emerald identities even after map dialogue is rewritten. This pass targets only globally safe identity labels in `src/strings.c`.

## Replacements

- both gender-dependent `{RIVAL}` backing strings (`MAY` and `BRENDAN`) become `CIRO`, so inherited dynamic rival references cannot display an Emerald protagonist name;
- `HOENN DEX` becomes `ARAUNA DEX`;
- `HOENN region's POKéDEX` becomes `ARAUNA region's POKéDEX`;
- the regional diploma/Dex label `HOENN` becomes `ARAUNA`.

## Deliberately deferred placeholders

The generic `{AQUA}`, `{MAGMA}`, `{ARCHIE}` and `{MAXIE}` backing values are not changed in this pass until every remaining placeholder context is audited for line length and prefix composition. Map/story text already receives dedicated faction cleanup; a global replacement must not create malformed strings such as duplicated organization prefixes.

## Safety boundary

Only five exact string constants are targeted. Internal `isHoenn` state, regional Dex enums, game-version logic, map IDs, species data, save structures and progression remain untouched.

## Integration sequencing

The shared residue runner stages `src/strings.c`, applies this tool, verifies the exact replacements, and requires a fresh full custom Emerald ROM CI on a final user-authored head before merge.

## Final validation trigger

The generated source commit was reviewed for scope: it changes exactly the five intended player-facing constants. This user-authored documentation commit intentionally follows the generator so both the deterministic cleanup gate and the full custom Emerald ROM CI execute on a non-bot final head before merge.
