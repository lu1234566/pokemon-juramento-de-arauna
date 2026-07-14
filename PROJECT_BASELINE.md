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

## Remote foundation

- Repository: `lu1234566/pokemon-juramento-de-arauna`
- Visibility: private during initial development
- Stable branch: `main`
- Foundation branch: `agent/bootstrap-project`
- Foundation pull request: `#1` (merged)
- First remote foundation commit: `c862d5903fd768bdd09dcb70d6e276a62a5dc263`
- Merge commit on `main`: `f0f2f1dc12932de23c449fda4d6e727059994212`

The repository was imported with upstream history intact. The project branches were then created directly from the fixed 1.16.2 baseline.

CI confirmation is tracked in issue `#4` and in a focused follow-up pull request. The workflow also supports manual runs so the pinned baseline can be revalidated independently of a source change.

## Baseline CI validation

The first complete run passed on 13 July 2026:

- Workflow run: [Project CI #2](https://github.com/lu1234566/pokemon-juramento-de-arauna/actions/runs/29299307256)
- Run ID: `29299307256`
- Validated commit: `2a93195efc0a088477dcc0d7e3a0fe97f2cd8aef`
- Total duration: 44 minutes and 17 seconds
- `repository-safety`: passed
- Emerald build and engine tests: passed
- Uploaded artifacts: none

This is the accepted clean baseline for project development. Any future engine upgrade must produce an equivalent successful run before it is integrated.
