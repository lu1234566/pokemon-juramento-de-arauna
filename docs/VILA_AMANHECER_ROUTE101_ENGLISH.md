# Vila Amanhecer + Route 101 — English opening restoration

Status: English-only migration slice.

This slice restores the first outdoor minutes of Pokemon Juramento de Arauna in English without changing the inherited Littleroot/Route 101 event graph.

## Vila Amanhecer — 17 blocks

The opening town now surfaces:

- MOM welcoming the player to VILA AMANHECER;
- the player's home and CIRO'S HOUSE;
- PROFESSOR ANAHI's FIELD LAB;
- Running Shoes handoff and controls;
- local warnings about entering the woods without a POKéMON;
- ordinary PC/storage guidance;
- ANAHI's field-research reputation;
- the postgame records invitation back to the lab.

ELIAS remains present in the family context, but the scene does not invent new father events or change any progression.

## Route 101 — 7 blocks

The unchanged Birch-rescue sequence now displays ANAHI throughout:

- ANAHI calls for help;
- the bag/POKé BALL prompt remains the trigger for the original starter selection;
- leaving the rescue area is still prevented by the same scripts;
- after rescue, ANAHI thanks the player and notices how quickly the chosen POKéMON accepted them;
- tutorial NPCs explain POKéMON CENTER and tall-grass basics without legacy OLDALE naming;
- the route sign points toward ENCRUZILHADA CENTRAL.

The rescue dialogue intentionally avoids dumping the later BOND/LIVING ARCHIVE exposition during the player's first encounter with ANAHI.

## Technical contract

`scripts/render_vila_amanhecer_route101_en.py` changes 24 text blocks total:

- 17 in `data/maps/LittlerootTown/scripts.inc`;
- 7 in `data/maps/Route101/scripts.inc`.

The renderer validates exact source markers, visible width (maximum 32 characters), structural masking and key Route 101 gameplay tokens.

The build adds both map sources to its transactional backup/restore stack and applies the renderer before later narrative overlays.

The following remain untouched: `FLAG_RESCUED_BIRCH`, `VAR_ROUTE101_STATE`, `ChooseStarter`, party healing, player-gender handling, route blocking, starter flags, warps, map geometry, saves and art.

English-only. PR #58 untouched.
