# Horizonte key-item visible identities

Two inherited key items still expose the DEVON brand directly in the bag even when surrounding dialogue has already been rewritten for Arauna:

- `ITEM_DEVON_GOODS` -> visible `CARGA HORIZ.`
- `ITEM_DEVON_SCOPE` -> visible `LENTE HORIZ.`

The abbreviations are deliberate because Emerald defines `ITEM_NAME_LENGTH` as 14. The descriptions spell out Consórcio Horizonte in Portuguese.

## Safety boundary

Only the `.name` values for the two existing item records and their two description string blocks are targeted. `ITEM_DEVON_GOODS`, `ITEM_DEVON_SCOPE`, item IDs, pockets, importance, use functions, icons, flags, save representation and all event references remain untouched.

This branch is preparation-only while no repository checkout/Actions runner is available. Activate later from the newest canonical main through the deterministic generator; Codespaces remains last resort.
