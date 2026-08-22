# Arauna region-map canonical labels

This pass aligns the compact region-map / Fly / POKeNAV-facing labels with the currently approved Arauna surface without changing Emerald map-section identifiers, coordinates, dimensions, warps or progression.

## Corrected visible labels

Three stale labels are canonicalized during the official English build:

| Internal map section | Stale source label | Build-time Arauna label |
|---|---|---|
| `MAPSEC_LAVARIDGE_TOWN` | `SERTAO DE DENTRO` | `CASA DA CINZA` |
| `MAPSEC_SAFARI_ZONE` | `SAFARI ZONE` | `ARAUNA PRESERVE` |
| `MAPSEC_BATTLE_FRONTIER` | `BATTLE FRONTIER` | `BATTLE CIRCUIT` |

`CASA DA CINZA` matches the approved Lavaridge/Nara story surface.

`BATTLE CIRCUIT` matches the approved postgame arrival, reception, services, lounge and Circuit Pass terminology.

`ARAUNA PRESERVE` is intentionally the compact map label. The Route 121 sign may continue to display the fuller **ARAUNA WILDLIFE PRESERVE** identity; the map-section storage contract is limited to `MAP_NAME_LENGTH = 16` characters.

## Validation contract

`tools/cleanup_region_map_names.py` now owns and validates **28** Arauna map-section labels. Every owned label must:

- resolve to exactly one existing `MAPSEC_*` entry;
- remain at or below `MAP_NAME_LENGTH = 16`;
- equal the approved canonical value after the cleanup pass.

The tool preserves internal map-section IDs and all non-name JSON fields.

## Transactional build integration

The canonicalization runs before the reviewed English dialogue renderers in `scripts/build_arauna.sh`.

`src/data/region_map/region_map_sections.json` joins the existing transactional overlay list. The build wrapper therefore:

1. backs up the JSON;
2. runs `python3 tools/cleanup_region_map_names.py`;
3. compiles using the canonical labels;
4. restores the original working-tree JSON on normal exit, failure or interruption.

This avoids a large generated-data diff while ensuring the official ROM receives the correct player-facing map labels.

## Deliberately unchanged

- `MAPSEC_*` identifiers;
- region-map coordinates and sizes;
- map layouts and connections;
- Fly destinations and unlock rules;
- warps and event progression;
- the full Route 121 preserve sign copy;
- Battle Circuit facility internal `FRONTIER_*` identifiers.

No GitHub Actions or Codespaces are required for this surface pass.
