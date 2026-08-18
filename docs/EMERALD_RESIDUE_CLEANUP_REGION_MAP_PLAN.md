# Arauna region-map visible-name cleanup

The region-map data still exposes original Emerald city and landmark names even where map scripts and story dialogue already use Arauna identities. This pass makes the map UI agree with the canonical story surface without changing map-section IDs or coordinates.

## Canonical replacements

The deterministic tool targets 26 existing `MAPSEC_*` entries. The actual stored names stay within the engine's 16-character map-name limit, using compact forms where necessary: Vila Amanhecer, Vila da Passagem, Porto das Redes, Sertao de Dentro, Campo das Cinzas, Vale do Silencio, Casa da Fogueira, Pampa da Espera, Porto do Sal, Encruzilhada, Serra do Uivo, Mata do Meio, Baia das Luzes, Missoes do Ceu, Aguas de M'Boi, Estr. Juramento, Gruta das Vozes, Serra da Cinza, Galerias Serra, Ruinas da Queda, Memorial Nomes, Arquivo Central, Cavernas M'Boi and Torre Juramento.

## Safety boundary

The tool changes only each selected JSON `name` value. `MAPSEC_*` IDs, x/y positions, dimensions, map connections, warps, fly destinations and save/progression state are preserved byte-for-byte outside those names.

## Integration sequencing

This branch was recreated directly from the newest green `main` after the Anahi opening-speech lot. The deterministic generator is wired into the shared residue pipeline. Merge is allowed only after generated JSON, a final user-authored validation commit, the cleanup check and the full custom Emerald ROM build all pass on the exact final head.

Final validation trigger: the generated region-map JSON is now present on the branch; this commit forces deterministic re-check plus a complete custom Emerald ROM build on the exact final user-authored head before merge.
