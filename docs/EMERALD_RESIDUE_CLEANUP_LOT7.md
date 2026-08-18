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

- `src/data/trainers.h` has the same blob SHA on current `main` as on the original patch base;
- `src/data/text/trainer_class_names.h` has the same blob SHA on current `main` as on the original patch base.

Therefore no later story/map cleanup has modified either battle-name source file. A fresh pull-request CI run against current `main` is still required before merge.

## Safety boundary

This lot changes only visible trainer names and trainer-class labels. It does not change trainer IDs, species, levels, moves, held items, battle scripts, flags, maps, saves or progression.
