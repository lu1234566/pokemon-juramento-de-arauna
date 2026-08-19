# Aguas de M'Boi — English restoration

Status: English-only migration slice.

This slice restores the complete visible Aguas de M'Boi crisis, ordinary city life, Kiri dialogue and Torre do Juramento handoff in the official English build.

## Crisis

The city experiences the M'Boi containment collapse as a memory event rather than a generic legendary battle:

- residents recall places and lives they never experienced;
- family members briefly lose familiar names;
- IARA-MAE and ANHANGUERA are described as ancient currents rather than mapped directly onto internal legendary species;
- the GUARDIAN OF THE TOWER forces the two currents apart without choosing for either side;
- LUZIA admits that forcing memory back can become another obligation;
- OTACILIO admits that ending pain without consent is another form of power.

SEU BENTO and AMALIA guide the player toward TORRE DO JURAMENTO while preserving the original event flow.

## Torre do Juramento

AMALIA opens the unchanged Sky Pillar route after the M'Boi collapse. The visible text uses `GUARDIAN OF THE TOWER`; `RAYQUAZA` remains an internal species/event implementation detail.

## Everyday city

Eight ordinary city blocks preserve Aguas de M'Boi as a crater community with water, stairs, bridges and a distinctive night sky. Post-crisis residents keep small habits such as checking names and writing them down before sleep.

The existing Waterfall handoff is surfaced with the Arauna `SPRING BADGE` wording while item/HM behavior remains unchanged.

## Kiri

Six Kiri blocks remain light and personal: her name, the wish her parents placed in it, Berries and favorite seasons. This keeps the city from becoming only a crisis set piece.

## Technical contract

The checked English wrapper composes the existing crisis and daily renderers:

- 38 crisis city blocks;
- 4 Torre do Juramento blocks;
- 8 daily city blocks;
- 6 Kiri blocks.

All visible segments are at most 32 characters. `SootopolisCity`, `SkyPillar_Outside` and `berries.inc` are backed up and restored transactionally by the English build.

Legendary species IDs, weather/event progression, objects, movements, HM behavior, gym progression, Berry distribution, warps, saves, geometry and art are untouched.
