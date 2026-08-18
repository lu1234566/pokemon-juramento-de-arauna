# Emerald residue cleanup — lot 7

This lot removes the remaining high-visibility Emerald identities shown on battle-intro/name plates while preserving every trainer ID, party, AI flag, item, script and progression condition.

## Player-facing replacements

- May / Brendan rival battle entries -> Ciro;
- Roxanne -> Dalva;
- Brawly -> Ademar;
- Wattson -> Olivia;
- Flannery -> Nara;
- Norman -> Elias;
- Winona -> Lidia;
- Tate & Liza -> Cecilia & Caetano;
- Juan -> Celina;
- Steven battle-facing name -> Bento;
- Team Aqua / Team Magma battle classes are surfaced as Horizonte / Lembrante-facing identities;
- relevant late-game battle classes are localized to Arauna-facing names.

## Revalidation against current main

Before this lot was revalidated, both source files touched by the original isolated patch were compared with the current `main`:

- `src/data/trainers.h` has the same blob SHA on current `main` as on the original patch base (`b4c1b05752331a50a08c9b1a40621683e9f01931`);
- `src/data/text/trainer_class_names.h` has the same blob SHA on current `main` as on the original patch base (`63cc356b236f5ceea1a0f4a454f8de7e8150da4f`).

Those two source blobs were checked again after the battle-message cleanup reached `main`; they are still unchanged. This user-authored documentation update intentionally requests a fresh pull-request full ROM CI run on the final battle-name head before merge.

## Safety boundary

This lot changes only visible trainer names and trainer-class labels. It does not change trainer IDs, species, levels, moves, held items, battle scripts, flags, maps, saves or progression.