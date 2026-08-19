# Pampa da Espera Gym — Elias story core in English

Status: English-only narrative migration.

This slice restores the central Elias/Val story surface inside the inherited Petalburg Gym while deliberately leaving the seven room-trainer conversations for a separate low-risk layer.

## Early visit and Val tutorial

The first visit no longer exposes late M'BOI material too early.

- ELIAS is surprised but glad that the player already travels with a POKéMON;
- VAL asks for help because he wants to travel but does not want to begin alone;
- ELIAS lends the inherited Zigzagoon and POKé BALL;
- the player is asked to accompany VAL without doing the task for him;
- after the unchanged catching tutorial, VAL returns proud that he acted despite being afraid;
- ELIAS sends the player toward the GYM in SERRA DO UIVO and promises a future battle.

All internal Wally/Norman identifiers remain untouched.

## Progression toward the Elias battle

The badge-state dialogue uses Arauna geography instead of visible Rustboro/Dewford residue:

- SERRA DO UIVO;
- PORTO DAS REDES.

ELIAS recognizes the player's growth without yet treating badge count as the whole story.

## Elias confrontation

The GYM battle becomes the first concrete family admission rather than another repeated exposition block.

Before battle, ELIAS states that he approved part of the M'BOI project and spent years calling fear `prudence`. He still fulfills the GYM LEADER role first and tells the player to ask him again after the battle.

After defeat, he admits that being the player's father cannot remain a shield against disclosure.

## Compass Badge

The existing fifth-badge slot is surfaced as the canonical `COMPASS BADGE`:

- badge receipt text is English;
- the inherited DEFENSE / SURF effect explanation remains intact;
- TM42 remains FACADE with the original mechanical meaning.

No badge flag, TM ID or progression is changed.

## Post-battle and rematch

ELIAS holds two feelings at once: disappointment as a LEADER and pride as a father.

Later/rematch dialogue advances the arc:

- parenthood never granted him the right to choose which truths the player could bear;
- silence is no longer described as protection;
- he explicitly names his approval of part of M'BOI without pretending guilt disappears through confession.

## Gym guide and statues

The GYM guide explains the seven-room structure in compact English. Statues identify `PAMPA DA ESPERA POKéMON GYM` and preserve the certified-trainer list.

## Technical contract

`scripts/render_pampa_elias_gym_core_en.py` owns 34 story/core text blocks. `scripts/render_pampa_elias_gym_core_en_checked.py` adjusts six width-only lines found during manual review. Final visible segments are at most 32 characters.

`data/maps/PetalburgCity_Gym/scripts.inc` joins the transactional backup/restore stack and the checked renderer has a dedicated CI validation gate.

Preserved mechanics include `TRAINER_NORMAN_1`, all gym-state variables, `FLAG_BADGE05_GET`, `FLAG_DEFEATED_PETALBURG_GYM`, TM42, VAL tutorial/rival flags, `InitBirchState`, the inherited Wally-house transition, doors, room trainers, rematch state, warps, saves, geometry and art.

English-only. PR #58 untouched.
