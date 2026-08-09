# Arauna encounter ecology

This checkpoint gives the existing Emerald map shell an Arauna-specific ecosystem without changing map layouts.

## Availability

- 321 ordinary species are distributed across wild tables and each has at least one encounter.
- 9 members of the three starter families remain outside ordinary wild tables.
- 25 story or sensitivity-review species remain reserved for scripted registration or encounters.
- 27 legendary and 4 mythical species remain outside ordinary wild tables.
- Preto-Velho (#265), Zumbi-Rei (#381), Iemanjã (#382), and Oxumará (#383) have catch rate zero and are registered through story events instead of capture.

## Progression rules

- Existing maps are associated with Brazilian biome roles such as Atlantic Forest, Cerrado, Caatinga, Amazon, Pantanal, Pampas, coast, rivers, caves, and highlands.
- Land, water, fishing, and Rock Smash tables only use compatible habitat profiles.
- Encounters at level 5 or lower are capped at 400 BST.
- Evolved forms never appear below their evolution level.
- Rare slots may contain stronger or less common species, while common slots favor lower-BST species appropriate to the map.
- The three encounter groups are protected from story-only, legendary, mythical, and starter-family species.

The source-of-truth registry is `docs/arauna/ARAUNA_ENCOUNTER_ECOLOGY.csv`. Regenerate the tables with:

```sh
python3 tools/arauna/build_arauna_encounters.py
```

The generation is deterministic: the same Dex, story-role registry, and map template produce the same encounters. This checkpoint does not require a ROM build; trainer teams and exact per-route difficulty will receive a later fine-balance pass.
