# Arauna system/UI identity cleanup plan

A small set of shared player-facing strings can still reintroduce Emerald identities even after map dialogue is rewritten. This prepared pass targets only globally safe identity labels in `src/strings.c`.

## Prepared replacements

- both gender-dependent `{RIVAL}` backing strings (`MAY` and `BRENDAN`) become `CIRO`, so inherited dynamic rival references cannot display an Emerald protagonist name;
- `HOENN DEX` becomes `ARAUNA DEX`;
- `HOENN region's POKéDEX` becomes `ARAUNA region's POKéDEX`;
- the regional diploma/Dex label `HOENN` becomes `ARAUNA`.

## Deliberately deferred placeholders

The generic `{AQUA}`, `{MAGMA}`, `{ARCHIE}` and `{MAXIE}` backing values are not changed in this preparation pass until every remaining placeholder context is audited for line length and prefix composition. Map/story text already receives dedicated faction cleanup; a global replacement must not create malformed strings such as duplicated organization prefixes.

## Safety boundary

Only five exact string constants are targeted. Internal `isHoenn` state, regional Dex enums, game-version logic, map IDs, species data, save structures and progression remain untouched.

## Integration sequencing

After the current narrative cleanup lots settle on green `main`, rebase/reset this preparation branch, wire the tool into the shared residue runner (which already stages `src/strings.c`), apply/check it, and require a full ROM CI before merge.
