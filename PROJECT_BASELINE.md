# Project baseline

## Engine

- Upstream: <https://github.com/rh-hideout/pokeemerald-expansion>
- Release tag: `expansion/1.16.2`
- Commit: `ad0fd4d17f546ca6fd8d785c8724f9382e6e9382`
- Baseline date: 13 July 2026
- Target game: Pokémon Emerald / Game Boy Advance

## Repository policy

The upstream history is intentionally preserved. In a developer checkout:

```bash
git remote add upstream https://github.com/rh-hideout/pokeemerald-expansion.git
git fetch upstream --tags
```

Engine upgrades must be performed in an isolated branch, one released version at a time. The upgrade is accepted only after the Emerald build, automated tests and the project regression checklist pass.

## First local build observation

The source was checked out exactly at the tag above. The initial build command reached dependency discovery and correctly reported that the disposable workspace lacked `arm-none-eabi-gcc`, `pkg-config` and `libpng` headers. The filesystem did not permit system package installation, so the clean baseline build is delegated to GitHub Actions and must pass before engine modifications are merged.
