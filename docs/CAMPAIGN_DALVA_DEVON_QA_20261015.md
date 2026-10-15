# Campaign journey: Dalva to Devon — 2026-10-15

Continuation of PR #238's actual campaign save, not a newly manufactured
progression fixture. Source checkpoint: `campaign_dalva_third_result.sav`,
Pampa at `(26,17)`, three level-15 Pokémon and no badge.

The source and linked ROM are unchanged from
`d49ae3a9dbb07e6112e1472b52199c3d9948c8c4`:
`0cc8a741b0c5af840c45e21d362eccd7577dcead6c52d2af876f15ceb48e4d23`.
The canonical build and 2,260 linked text comparisons passed. The initial
checkpoint passed a separate-process CONTINUE before the journey resumed.

## Actual journey

| Milestone | Observed result |
| --- | --- |
| Route 116 preparation | Four trainers defeated; money increased from 748 to 1,628; eight Poké Balls purchased normally |
| Mata captures | Two Preguicim and one additional Preguicinha caught; six Pokémon in the party, five balls remaining |
| ARAUNA preparation | The three new Pokémon raised to the current level-15 cap; REST used; two Preguicinha taught Destiny Bond through LINEAGE and the normal move-forgetting screen |
| Fourth campaign attempt at Dalva | Actual `B_OUTCOME_WON = 1`; `FLAG_BADGE01_GET = true`; `FLAG_RECEIVED_TM_ROCK_TOMB = true`; one Rock Tomb TM; city state 1, Pampa gym state 3 |
| Cold validation of victory | Separate process loaded the normal victory SAVE; all party bytes, recorded story state and control availability matched |
| Theft scene | Walking through `(18,23)` triggered the chase; city state 2, Route 116 state 1, tunnel state 2; goods-stolen flag set |
| Devon employee's request | Normal coordinate event at `(29,10)` advanced city state to 3 |
| Tunnel rescue | Peeko rescued and goods recovered through the normal battle/event; city state 4, tunnel state 3, recovered flag set, stolen flag cleared, one Devon Goods item |
| Devon president | Normal return event and escort completed; letter and PokéNav received; city state 6, Devon 3F state 1, returned-goods flag set |
| Devon exit | Mandatory PokéNav/Match Call tutorial completed normally; city state 7; controls unlocked; normal SAVE and separate-process CONTINUE passed |

The final ordinary campaign Pokémon survived Dalva at 40/40 HP; the other
five had fainted. REST was used after recording the victory. No trainer
roster, move, level cap, item price or battle outcome was edited.

The Devon Goods item remains in the bag after visiting the president because
its later delivery is a separate campaign objective.

## Driver corrections

`campaign_controller.py` now considers attack/defense stages when estimating
damage and accepts explicit move/party policies that still use joypad input.
It records move choices and enemy HP. Capture preparation is bounded to four
turns so drain-move encounters cannot indefinitely postpone throwing a ball.
If only status moves have PP, the fallback selects an available move slot.

`campaign_preparation.py` handles LINEAGE through the actual menus, including
checking the offered moves and selecting the move to forget. `dalva_policy.py`
records the strategy used during this session. It is a manual QA aid, not a
guarantee of victory across RNG states. Two supplementary fresh-process
autoplay attempts did not certify another win; the victory claimed here is
the actual main-session result and its successfully reloaded native SAVE.

The mandatory Devon tutorial needs two explicit menu choices: POKENAV in the
forced Start menu, then MATCH CALL inside PokéNav. After calling Mr Stone,
ordinary B input exits the call and menus. Blind A input was a driver error,
not evidence of a game softlock. `test_campaign_devon_exit.py` tests this
continuation from the private, normally generated Devon save.

## Evidence and scope

Selected receipts and native screenshots are in
`review/remaining_runtime_20261014/campaign_*20261015*`. Saves remain private;
no ROM or save file is committed or uploaded as a public CI artifact.
The archived receipts reference lossless JSON/gzip sidecars for input runs
and full battle traces, retaining SHA-256 digests, row counts and compact
battle summaries. Every sidecar was decompressed and compared with its
original content. The cold-checkpoint validator checks their integrity.
The native CI evidence artifact includes these `.json.gz` sidecars as well.

All progression in this journey came from movement, dialogue, battles,
ordinary menu actions, SAVE and CONTINUE. No injected game functions, warps,
RAM/ROM writes or forced battle results were used. Importing an existing
native save for CONTINUE is distinct from constructing a fixture.

Input journals are segment evidence, not one uninterrupted replay recording:
the driver was reloaded after an encounter-handling error, and the Devon exit
uses a new process. The Route 116 funds receipt preserves the earlier input
segment; the capture/recovery receipts identify the next segment. Native
checkpoints and party hashes preserve the actual game continuity across them.

The art freeze comparison against
`46d50777a45f8fbf1f7f600516a47873ec4fc804` passed for `graphics/`,
`data/tilesets/`, `data/layouts/` and `sound/`. Ciro's installed art, palettes
and portraits remain byte-identical. This PR changes QA helpers and evidence
only. The second badge and subsequent campaign are not certified here.
