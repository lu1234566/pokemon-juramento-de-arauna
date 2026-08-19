# Val's House — English family surface

Status: English-only migration.

This slice converts the eight authored Portuguese text blocks in the inherited Wally-house map while preserving the entire HM SURF and VAL progression flow.

## Family arc — 8 blocks

VAL's parents now provide a consistent English through-line:

- they thank the player for treating VAL patiently during the early catching/travel stage;
- they worry when he goes several days without sending news;
- after the ELIAS GYM victory, VAL's father gives the unchanged HM SURF as thanks for helping VAL when he was still afraid to travel alone;
- SURF's visible explanation remains mechanical and concise;
- later dialogue describes VAL traveling because he wants to rather than because he needs to prove himself;
- after the inherited Victory Road encounter, his father recognizes that VAL returned more certain while remaining himself;
- his mother describes both pride and understandable worry as VAL chooses his own path.

The house does not turn VAL's family into exposition devices; it keeps the focus on his independence and the player's early patience with him.

## Technical contract

`scripts/render_val_house_en.py` owns all 8 visible text blocks in `data/maps/PetalburgCity_WallysHouse/scripts.inc`.

`scripts/render_val_house_en_checked.py` changes four width-only lines found during manual review. Final visible segments are at most 32 characters.

The house map joins the transactional backup/restore stack and receives a dedicated CI gate.

Preserved: `ITEM_HM_SURF`, `FLAG_RECEIVED_HM_SURF`, `VAR_PETALBURG_CITY_STATE`, `FLAG_DEFEATED_WALLY_VICTORY_ROAD`, `FLAG_THANKED_FOR_PLAYING_WITH_WALLY`, all object facing/warp state, saves, geometry and art.

English-only. PR #58 untouched.
