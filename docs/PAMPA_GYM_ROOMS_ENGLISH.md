# Pampa da Espera Gym — room trainers in English

Status: English-only surface migration.

This slice completes the seven inherited Petalburg Gym challenge rooms after the Elias/Val story core was restored separately.

## Seven trainer rooms — 28 blocks

Each of the seven existing trainers keeps the same trainer ID, party, room, door-unlock callback and post-badge state. Only visible dialogue changes.

The rooms now read as different battle habits rather than generic filler:

- SPEED — controlling early momentum;
- ACCURACY — acting when every hit matters;
- CONFUSION — maintaining a BOND when commands become uncertain;
- DEFENSE — using durability to take calculated risks;
- RECOVERY — keeping a plan when an opponent refuses to stay worn down;
- POWER — direct pressure;
- CRITICAL — keeping composure through critical-hit variance.

Trainer dialogue also stops treating the player as merely `the LEADER's kid`: ELIAS is acknowledged, but the player's choices are framed as their own.

## Doors and room labels — 10 blocks

All door prompts are compact English. Two misleading vanilla visible labels are corrected without changing room logic:

- internal `STRENGTH ROOM` -> visible `POWER ROOM`;
- internal `ONE-HIT KO ROOM` -> visible `CRITICAL ROOM`.

The Emerald source itself notes that these room names were mechanically misleading; the internal door functions, map geometry and trainer assignments remain untouched.

The final door identifies `GYM LEADER'S ROOM` and states that ELIAS waits beyond it.

## Technical contract

`scripts/render_pampa_gym_rooms_en.py` owns 38 blocks: 28 trainer blocks plus 10 door/room prompts.

`scripts/render_pampa_gym_rooms_en_checked.py` contains only:

- five width corrections found in manual review;
- explicit literal source anchors for unusually short inherited defeat lines that do not contain a normal room/trainer marker.

The renderer runs after the Elias story-core renderer and the two target sets are disjoint.

Preserved: `TRAINER_RANDALL`, `TRAINER_PARKER`, `TRAINER_GEORGE`, `TRAINER_BERKE`, `TRAINER_MARY`, `TRAINER_ALEXIA`, `TRAINER_JODY`, all parties, battle callbacks, post-badge branches, `PetalburgGymSlideOpenRoomDoors`, `PetalburgGymUnlockRoomDoors`, room metatiles, flags, variables, warps, saves, geometry and art.

English-only. PR #58 untouched.
