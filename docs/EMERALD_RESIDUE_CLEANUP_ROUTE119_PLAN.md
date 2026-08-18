# Route 119 visible-surface cleanup plan

Route 119 already surfaces Ciro in the rival encounter, but several adjacent player-facing strings still expose Emerald identities. This pass removes those contradictions without changing the rival branches, battle IDs, HM reward, flags or movements.

## Replacements

- Scott's two visible speeches become a generic Arauna `VIAJANTE` role, avoiding an unsupported recurring Emerald identity;
- Fortree references in those speeches become Mata do Meio / Lidia context;
- the two bridge guards refer to HORIZONTE and the Instituto das Aguas;
- the Route 119 destination sign points to Mata do Meio;
- the Weather Institute sign becomes Instituto das Aguas.

## Safety boundary

Only six existing `.string` blocks in `data/maps/Route119/scripts.inc` are targeted. Internal Scott/May/Brendan labels, trainer IDs, music slots, rival selection, HM02/Fly handling, coordinates, warps, flags and route progression remain untouched.

## Integration sequencing

This active branch starts directly from the latest green `main`. The shared cleanup workflow applies and checks the deterministic tool, stages only the existing generated-source directories already used by the residue pipeline, and requires a fresh full custom Emerald ROM build on a final user-authored head before merge.
