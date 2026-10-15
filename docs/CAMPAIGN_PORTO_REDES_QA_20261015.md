# Campaign journey: letter, second badge and Flash — 2026-10-15

Continues the actual `porto_redes_arrival_20261015` checkpoint from PR #239.
The matching CI build and symbol listing were recovered instead of rebuilding
an unchanged game. ROM SHA-256 is still
`0cc8a741b0c5af840c45e21d362eccd7577dcead6c52d2af876f15ceb48e4d23`.
The source checkpoint passed separate-process CONTINUE before play resumed.

## Results from normal play

| Stage | Observed result |
| --- | --- |
| Porto das Redes clinic | Normal nurse interaction registered the local return point |
| Gruta das Vozes | HM Flash received; both lower floors traversed through their actual ladders; Bento's room reached through the north-side route |
| Bento | Letter consumed once; Steel Wing TM received; PokéNav contact registered; NPC departed |
| Storage | Two duplicate Preguicim deposited through ARAUNA > STORAGE; their identities and complete 80-byte box records survived SAVE/CONTINUE |
| Captures | Two level-7 Morcim caught with ordinary balls; the party returned to six members |
| Preparation | ARAUNA LEVEL used to reach the current level-19 cap; Caramelão, Preguicão and two Morcego evolved normally; Leech Seed and Synthesis selected through REMEMBER |
| Ademar | First attempt in this journey won: trainer 266, `B_OUTCOME_WON = 1`; second badge and one Bulk Up TM received; Pampa gym state advanced from 3 to 4 |
| Leader revisit | Victory SAVE loaded in a new process; no new battle, duplicate TM or repeated gym-state increment; gym lights remained on |
| Flash | Offered in the party context menu after the badge; native cave light level changed from 7 to 1 and the used-Flash flag was set; no party member learned Flash or lost PP |
| Persistence | Actual victory, letter, Flash and the two deposited Pokémon validated through native SAVE/CONTINUE in separate processes |

Two Pokémon remained conscious after the leader battle: Preguicão at 22/55 HP
and Caramelão at 32/57 HP. The leader AI sent its remaining team in an order
different from the source roster order. The archived battle trace records the
actual choices and HP. The strategy helper is a manual QA aid, not a promise
of identical outcomes across RNG states.

## QA driver changes

- Walking now idles and retries an apparently blocked edge before caching it.
  A cave step rejected during movement timing was later traversed with normal
  input; it was not a reason to edit the map's collision data.
- LEVEL now waits for the party-selection screen after reaching the requested
  level, so move-learning and evolution prompts finish before menu exit.
  The previous level-only stop could loop between move-learning questions.
- The move-menu helper now supports REMEMBER as well as LINEAGE, selecting
  only moves offered by the game and using the real forgetting screen.
- The cold-checkpoint validator can verify cave light level and retained box
  records in addition to party, story flags, variables, inventory and journals.

`test_campaign_bento.py` replays the actual pre-delivery save, revisits the room
and checks the one-time reward. `test_campaign_badge02.py` loads the actual
victory and revisits the leader. `test_campaign_flash.py` uses the native party
menu without teaching Flash and checks unchanged moves/PP. All three passed,
including their separate-process CONTINUE checks. These tests require the
private campaign saves and are separate from the fixture-based CI scenarios.

## Evidence and limits

Receipts, screenshots and lossless JSON/gzip input/battle journals use the
`campaign_*20261015*` names under `review/remaining_runtime_20261014/`.
Archive sidecars retain SHA-256 digests and counts. Native saves remain private.
No ROM or save file is added to the repository or native evidence artifact.

The main journey used movement, dialogue, battles, ordinary menu choices,
SAVE and CONTINUE. No injected game calls, teleports, game RAM/ROM writes,
artificial story flags or forced outcomes were used. Driver functions were
updated without resetting the live emulator or its input journal.

No gameplay source, trainers, balance, maps, layouts, tilesets, graphics,
palettes, portraits or audio changed. Ciro's installed art remains identical
to the protected art reference. The third badge and later campaign are not
certified by this PR.
