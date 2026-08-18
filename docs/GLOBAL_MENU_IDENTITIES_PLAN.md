# Global Arauna menu identity cleanup

Several global `src/strings.c` constants remain player-facing even though the region map itself already uses Arauna names. They surface in Briney destination choices, the S.S. Tidal destination menu, the wall-mounted region-map title and the PokéNav map description.

## Prepared exact replacements

- PETALBURG -> PAMPA DA ESPERA
- SLATEPORT -> PORTO DO SAL
- DEWFORD -> PORTO DAS REDES
- LILYCOVE CITY -> BAIA DAS LUZES
- SLATEPORT CITY -> PORTO DO SAL
- `Check the map of the HOENN region.` -> `Veja o mapa de ARAUNA.`
- map title `HOENN` -> `ARAUNA`

The backing `gText_*` symbol names remain unchanged to avoid touching implementation wiring.

## Safety

No menu indexes, travel destinations, map IDs, ferry state, route connections, flags, saves, trainer data or progression are changed. The strings continue pointing at the same functional Emerald destinations; only their player-visible Arauna identities change.

## Activation

This preparation was recreated from current canonical `main` while GitHub Actions quota is exhausted. Activate later through the deterministic residue runner and reserve Codespaces for last-resort execution/build validation.
