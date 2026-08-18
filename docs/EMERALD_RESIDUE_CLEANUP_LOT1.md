# Emerald residue cleanup — lot 1

This lot removes the most visible vanilla Emerald gym-sign residue while preserving the existing event graph and progression.

## Replaced visible identities

- Rustboro / Roxanne -> Serra do Uivo / Dalva
- Dewford / Brawly -> Porto das Redes / Ademar
- Mauville / Wattson -> Encruzilhada Central / Olivia
- Lavaridge / Flannery -> Casa da Cinza / Nara
- Petalburg / Norman -> Pampa da Espera / Elias
- Fortree / Winona -> Mata do Meio / Lidia
- Mossdeep / Tate & Liza -> Missoes do Ceu / Cecilia e Caetano
- Sootopolis / Juan -> M'Boi / Dona Celina

## Safety boundary

Only the labeled `*_Text_GymSign` string blocks are rewritten by `tools/cleanup_emerald_residue_signs.py`.

This lot deliberately does **not** change:

- map coordinates or object positions;
- warps or connections;
- flags or variables;
- badge order;
- trainer teams;
- triggers or movement scripts;
- route progression.

Secondary NPC dialogue, old company terminology and other English/Hoenn residue are intentionally left for later cleanup lots so each change remains reviewable and regression-safe.
