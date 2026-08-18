# Consórcio Horizonte HQ surface cleanup

The inherited Devon Corp building is structurally useful as the Serra do Uivo technical center, but its visible text still exposes one of the largest remaining Emerald leaks: DEVON, MR. STONE, STEVEN, DEWFORD, SLATEPORT and the malformed `CONSORCIO HORIZONTEORATION` replacement.

## Canonical reinterpretation

The building becomes a Consórcio Horizonte technical center. The inherited president slot is explicitly Dr. Otacílio Meira, consistent with the project canon that the Consórcio is led by Otacílio. The player still performs the same structural delivery sequence, but the visible destinations are Porto do Sal and Porto das Redes, and the inherited Steven letter contact is Seu Bento.

The research floor is rewritten around field equipment, PokéNav networking, Vínculo sensors, memory research and the existing fossil-regenerator feature. Fossil species, item grants and machine state are not changed.

## Prepared scope

A deterministic exact-label tool rewrites 40 player-facing blocks across the inherited 1F, 2F and 3F scripts. It rejects visible DEVON / HORIZONTEORATION / MR. STONE / STEVEN / SLATEPORT / DEWFORD / MAGMA / AQUA / CAPT. STERN tokens inside the targeted blocks.

## Safety boundary

Internal Devon/Mr. Stone symbol names, flags and map IDs remain untouched. The parcel delivery, PokéNav award, Letter, Exp. Share, fossil choices, fossil species, item IDs, party/PC transfer logic, coordinates, movements, warps, route order and badge progression are unchanged.

## Activation

Activate from the newest green `main` after the current Actions infrastructure failure clears. Wire `cleanup_horizonte_hq_surface.py` into the shared residue runner, generate the map scripts, run `--check`, add a user-authored validation commit and require a successful full custom Emerald ROM build before merge.
