# Arauna region-map visible-name cleanup

The region-map data still exposes the original Emerald city and landmark names even where map scripts and story dialogue already use Arauna identities. This pass makes the map UI agree with the canonical story surface without changing map-section IDs or coordinates.

## Canonical replacements prepared

The deterministic tool targets 26 existing `MAPSEC_*` entries, including:

- Littleroot -> Vila Amanhecer;
- Oldale -> Vila da Passagem;
- Dewford -> Porto das Redes;
- Petalburg -> Pampa da Espera;
- Rustboro -> Serra do Uivo;
- Slateport -> Porto do Sal;
- Mauville -> Encruzilhada Central;
- Verdanturf -> Vale do Silencio;
- Fallarbor -> Campo das Cinzas;
- Lavaridge -> Sertao de Dentro;
- Fortree -> Mata do Meio;
- Lilycove -> Baia das Luzes;
- Mossdeep -> Missoes do Ceu;
- Sootopolis -> Aguas de M'Boi;
- Ever Grande / Victory Road -> Estrada do Juramento;
- Granite Cave -> Gruta das Vozes;
- Mt. Chimney -> Serra da Cinza;
- Rusturf Tunnel -> Galerias da Serra;
- Meteor Falls -> Ruinas da Queda;
- Mt. Pyre -> Memorial dos Nomes;
- Aqua Hideout map section -> Arquivo Central;
- Seafloor Cavern -> Cavernas de M'Boi;
- Sky Pillar -> Torre do Juramento.

## Safety boundary

The tool changes only each selected JSON `name` value. `MAPSEC_*` IDs, x/y positions, dimensions, map connections, warps, fly destinations and save/progression state are preserved byte-for-byte outside those names.

## Integration sequencing

This preparation branch intentionally does not alter the shared residue-cleanup workflow yet. It should be rebased onto the latest green `main` after the currently running Vila Amanhecer and battle-message lots, then wired into the cleanup runner and full ROM CI before merge.
