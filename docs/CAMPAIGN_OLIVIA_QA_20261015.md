# Campaign: Olivia, third badge and Rock Smash — 2026-10-15

Continues the private M'Boi gym checkpoint from #241, using its exact CI ROM:
`a2dfe2d861d84eaf0df31b31b6c42f2a668b1afa7a4f3467e82df355f2b69942`.
No gameplay source, balance, trainer party, map, layout, graphic, palette or
audio changed. This PR contains campaign evidence and QA driver improvements.

## Observed campaign results

| Stage | Result |
| --- | --- |
| Preparation | REMEMBER and LINEAGE used through their real menus; team stayed within the level-24 cap |
| Gym | Three trainer encounters won; floor switches and the final passage traversed using normal movement |
| Storage | One duplicate Morcego deposited; all three complete box records survived subsequent CONTINUE checks |
| Capture | Lixão caught on Route110 after weakening it normally; native capture checkpoint passed CONTINUE |
| Training | Lixão learned Mud Shot and Rock Slide through LINEAGE, reached level 24 and evolved into Chorume; Magnitude was retained through the real forgetting screen |
| Olivia | Sixth attempt won, trainer 267, outcome 1; five party members remained conscious; one Super Potion used |
| Rewards | Third badge, defeated-gym, Shock Wave and match-call flags set; exactly one Shock Wave TM; Pampa gym state 5 and museum state 3 |
| Revisit | Loading the victory in a separate process and talking to Olivia caused no new battle, duplicate TM or repeated gym-state increment; exit remained reachable |
| Rock Smash | Party menu offered the badge-granted action on Route111; rock 15 disappeared and the passage was walked through; nobody learned the move or lost PP |
| Persistence | Victory, revisit, Rock Smash replay and the north-side checkpoint passed native SAVE/CONTINUE in separate processes |

Chorume defeated Ouríço and Cabofio with Mud Shot and Vagalume with Rock
Slide. Ipetim handled Arraia and established Destiny Bond before Tupã's
finishing attack. The winning trace records actual move selections, health,
item use and the victory outcome. Status cures were purchased normally during
preparation; the winning battle did not consume them.

Five losses and an unsuccessful capture attempt remain in the private
archive. Native SAVE/CONTINUE retries are identified in the checkpoint chain;
this is not presented as one uninterrupted first attempt. The winning journey
resumes `olivia_attempt4_ready_20261015`, visits the shop, returns to the gym,
wins, revisits Olivia and continues to Route111. Its final checkpoint is
`badge03_route111_north_ready_20261015`, at `(18,99)`, with six healthy level-24
Pokémon, three badges, one Shock Wave TM and used-Rock-Smash statistic 1.

## QA changes and validation

The joypad driver evaluates a living enemy after one side of a double battle
faints and cycles the actual target cursor to that enemy. Optional switches
are handled through the battle script's Yes/No box, including the announced
incoming species. Optional policies can select owned battle items and ordinary
party switches. The preparation helper handles SWITCH's second cursor, empty
move slots and a selected move-forgetting slot during LEVEL. Receipts now
retain third-badge state, Rock Smash statistics and complete occupied box
record hashes; the cold validator checks those values.

`test_campaign_badge03.py` and `test_campaign_rock_smash.py` both passed using
private, naturally generated saves. They are separate from fixture-based CI
and require those saves. Capture, training, victory and final-route cold
checks also passed. The existing Tuim four-form/all-slot heap regression
passed again on the unchanged ROM. Art freeze passed for 20,104 assets; the
graphics/layout/audio diff against the protected Ciro reference is empty.

Public receipts retain lossless gzip input/battle journals with hashes and
counts. No ROM, native save, emulator state or compiled helper is committed.
The journey uses joypad input, reads, normal menus, SAVE and CONTINUE; no
injected game calls, RAM/ROM writes, teleports, artificial flags or forced
outcomes. The fourth badge and later campaign remain pending.
