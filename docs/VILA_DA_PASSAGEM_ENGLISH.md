# Vila da Passagem — English early-game hub

Status: English-only migration and canonical-name correction.

This slice completes the inherited Oldale Town surface as VILA DA PASSAGEM and corrects the inbound Route 101 / Route 103 signs to match the region-map naming contract.

## Canonical name correction

`tools/cleanup_region_map_names.py` is authoritative for visible regional place names:

- `MAPSEC_OLDALE_TOWN` -> `VILA DA PASSAGEM`;
- `MAPSEC_MAUVILLE_CITY` -> `ENCRUZILHADA`.

Earlier English Route 101 / Route 103 overlays incorrectly pointed Oldale traffic toward `ENCRUZILHADA CENTRAL`. Small checked wrappers now correct those outputs to `VILA DA PASSAGEM`, and the previous slice documentation is updated accordingly.

## Vila da Passagem — 10 blocks

The town remains a compact early tutorial hub:

- saving/rest reminder;
- POKéMON MART introduction;
- original free POTION handoff and explanation;
- the footprint researcher still blocks the west exit before the adventure starts and keeps the original light joke;
- both internal rival branches surface the same CIRO return line after Route 103;
- the town sign preserves the authored Arauna hook: a local POKéMON stopped responding to its own name, and residents call the phenomenon DESECHANTMENT.

The DESECHANTMENT reference remains environmental rather than turning the tutorial town into an exposition scene.

## Technical contract

- `scripts/render_vila_da_passagem_en.py`: 10 Oldale text blocks;
- `scripts/render_vila_amanhecer_route101_en_checked.py`: canonical Route 101 destination;
- `scripts/render_route103_ciro_en_checked.py`: canonical Route 103 shortcut/sign destination.

`data/maps/OldaleTown/scripts.inc` joins the transactional backup/restore stack. The two checked inbound wrappers only alter visible destination payloads from the already-validated base renderers.

Preserved: `FLAG_VISITED_OLDALE_TOWN`, `FLAG_RECEIVED_POTION_OLDALE`, `ITEM_POTION`, `FLAG_ADVENTURE_STARTED`, footprints blocking/movements, rival triggers/exits, `VAR_OLDALE_RIVAL_STATE`, inherited Oldale internal IDs/flags, warps, saves, geometry and art.

English-only. PR #58 untouched.
