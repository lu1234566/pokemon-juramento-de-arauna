# Barqueiro / coastal transport visible-residue cleanup

The inherited Mr. Briney boat system is useful structurally, but its player-facing surface still exposes MR. BRINEY, PEEKO, Dewford, Slateport, Petalburg, Devon and Capt. Stern throughout one of the earliest mandatory travel sequences.

No canonical Arauna personal-name replacement for this functional slot is established in the current story documents. To avoid inventing lore, the visible speaker is therefore identified by role as `BARQUEIRO`, while all internal Briney/Peeko symbols remain untouched.

## Prepared scope

Twenty-four exact text blocks across the inherited Briney house, Porto das Redes and Route 109 travel scenes are rewritten. Destinations become Pampa da Espera, Porto das Redes and Porto do Sal; the package is identified only as Horizonte material. The companion Pokémon remains the same underlying species/object but loses the Emerald-specific Peeko nickname in player-facing dialogue.

## Safety boundary

All sailing scripts, destination menu indexes, boat movements, backup-location variables, flags, warps, item delivery state, Pokémon species/object IDs and route progression remain unchanged. This is text-only reinterpretation of the existing travel graph.

## Activation

Activate from the newest green `main` after GitHub Actions can execute jobs again. Wire the deterministic tool into the shared cleanup runner, generate/check the three map scripts, add a final user-authored validation commit and require a successful full custom Emerald ROM build before merge.
