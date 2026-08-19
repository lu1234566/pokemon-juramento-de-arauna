# Route 102 + Pampa da Espera — English opening continuation

Status: English-only narrative migration.

This slice continues the early-game path from VILA DA PASSAGEM through Route 102 into PAMPA DA ESPERA without changing the inherited Emerald tutorial, city or Scott-event graph.

## Route 102 — 7 blocks

The route remains a basic catching/travel tutorial while using Arauna characters and place names:

- the inherited Wally tutorial text visibly belongs to VAL;
- VAL asks the player to watch because he is still nervous about catching a POKéMON alone;
- after succeeding, he recognizes that being afraid did not prevent him from acting;
- the return line explicitly points back to ELIAS;
- ordinary route NPCs remain light tutorial flavor;
- signs point east to VILA DA PASSAGEM and west to PAMPA DA ESPERA.

The tutorial battle itself is untouched and still runs from the Petalburg/Pampa script using the original Wally mechanics.

## Pampa da Espera exterior — 12 blocks

### Val and family

`PetalburgCity_Text_WhereIsWally` previously contained a VAL monologue even though the event belongs to his mother. It now correctly displays a mother/caregiver line explaining that VAL went to speak with ELIAS and still feels nervous in crowds.

The former Wally-house sign is now simply `VAL'S HOUSE`.

### City and Gym surface

- local guide teaches the normal GYM-sign convention;
- the visible gym is PAMPA DA ESPERA GYM, led by ELIAS;
- the inherited party/storage explanation remains practical and mechanical;
- the city sign frames PAMPA DA ESPERA around departures and returns while keeping ELIAS's silence around M'BOI visible but restrained.

### Seu Bento introduction

The three inherited Scott encounter texts now visibly belong to SEU BENTO from his first appearance:

- he notices the player as a very new trainer;
- he refuses to judge them too early;
- he explains that he travels observing how TRAINERS treat their BONDS and says they will meet again.

All Scott internal variables, objects and movement remain unchanged.

## Technical contract

`scripts/render_route102_pampa_en.py` owns 19 blocks:

- 7 in `data/maps/Route102/scripts.inc`;
- 12 in `data/maps/PetalburgCity/scripts.inc`.

`scripts/render_route102_pampa_en_checked.py` fixes one width-only 33-character gym-sign line. Final visible segments are at most 32 characters.

Both source maps join the transactional build backup/restore stack and the checked renderer has a dedicated CI gate.

Preserved mechanics include Route 102 trainer IDs/Match Calls, `SavePlayerParty`, `LoadWallyZigzagoon`, `StartWallyTutorialBattle`, `LoadPlayerParty`, Petalburg/Pampa city and gym state variables, Scott state/encounter variables, all movement, warps, saves, geometry and art.

English-only. PR #58 untouched.
