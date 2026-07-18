# English-first runtime

The first playable build of **Pokémon Juramento de Arauna** targets English.

- Brazilian proper names remain unchanged as part of the region's identity.
- The introduction, opening, map lab, Mist Route, First Link Ruin, and First Link Chamber use the English story packs.
- All 386 species have English category, habitat, and Pokédex text in docs/arauna/source/pokedex.en.json.
- The original Portuguese export remains in pokedex.json for the later Brazilian Portuguese localization.
- tools/arauna/integrate_full_arauna_dex.py requires the English localization when rebuilding the species header.
- tools/arauna/validate_english_runtime.py rejects missing entries, Portuguese fallback prose, obsolete placeholder messages, and incorrectly selected language wrappers.
- docs/arauna/source/story_roles.json separates Census registration from capture and locks the explicitly revered entities out of normal capture data.
- docs/arauna/ARAUNA_BATTLE_PROFILES.csv is the reviewable source for abilities, gender, breeding, catch rates, experience and growth curves.
- src/data/pokemon/arauna_teachables.json overlays the reused engine slots with type- and role-aware TM/HM compatibility.
- src/data/pokemon/egg_moves/arauna.h gives each of the 354 breedable species a family-aware set of six to ten inherited moves; the 32 protected slots remain unable to breed.
- tools/arauna/build_arauna_battle_profiles.py regenerates all three datasets and rewires the committed species table without touching art.
- tools/arauna/audit_arauna_trainers.py prevents legendary, mythical, story-reserved and sensitivity-review slots from appearing in ordinary trainer parties; its last migration is recorded in docs/arauna/ARAUNA_TRAINER_AUDIT.md.
- docs/arauna/ARAUNA_CRY_AUDIT.csv records the 386 unique Emerald-slot cries still used as placeholders and reserves stable `.aif` paths for a later dedicated audio pass.

Regenerate battle data from the repository root with:

```sh
python3 tools/arauna/build_arauna_battle_profiles.py
python3 tools/arauna/audit_arauna_trainers.py
python3 tools/arauna/audit_arauna_cries.py
python3 tools/arauna/validate_packed_arauna_dex.py
```

The English build does not delete the Portuguese work. It keeps that material out of the active ROM while the English version is stabilized.
