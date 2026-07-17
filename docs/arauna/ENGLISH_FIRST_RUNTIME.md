# English-first runtime

The first playable build of **Pokémon Juramento de Arauna** targets English.

- Brazilian proper names remain unchanged as part of the region's identity.
- The introduction, opening, map lab, Mist Route, First Link Ruin, and First Link Chamber use the English story packs.
- All 386 species have English category, habitat, and Pokédex text in docs/arauna/source/pokedex.en.json.
- The original Portuguese export remains in pokedex.json for the later Brazilian Portuguese localization.
- tools/arauna/integrate_full_arauna_dex.py requires the English localization when rebuilding the species header.
- tools/arauna/validate_english_runtime.py rejects missing entries, Portuguese fallback prose, obsolete placeholder messages, and incorrectly selected language wrappers.

The English build does not delete the Portuguese work. It keeps that material out of the active ROM while the English version is stabilized.

## Arauna Dex runtime contract

- The regional Dex is the Arauna Dex and maps directly to native slots 001-386.
- The Research Center unlocks the regional Dex without enabling Emerald's unstable National Dex screen.
- Story-only Testimonies, guardians, legendary species, and mythicals stay out of ordinary wild and trainer tables until they receive scripted encounters.
- Battle and catching tutorials use a common temporary Arauna species instead of Pomba-Gira.
- A clean save is recommended when testing changes to Dex numbering and unlock flags.

## Pre-build check in Codespaces

Run the two standard-library checks before compiling. For this Dex migration, use a clean build:

```sh
python3 tools/arauna/validate_english_runtime.py
python3 tools/arauna/validate_packed_arauna_dex.py
make clean
make ARAUNA_LANGUAGE=ENGLISH -j2
```

The playable output is `pokeemerald-en.gba`. The English-first CI intentionally does not build the Portuguese ROM yet.
