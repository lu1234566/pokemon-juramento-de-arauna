# Campaign: Nara, fourth badge and Strength — 2026-10-16

Continues #242 from the private `badge03_route111_north_ready_20261015`
checkpoint. The ROM is the successful #242 CI build (run 38826273485), SHA256
`a2dfe2d861d84eaf0df31b31b6c42f2a668b1afa7a4f3467e82df355f2b69942`.
No game source, balance, trainer parties, graphics, maps, layouts, palettes or
audio changed. This revision contains QA drivers, documentation and evidence.

## Observed results

| Stage | Native campaign result |
| --- | --- |
| Preparation | Six party members reached the three-badge cap of 29 through LEVEL; two Ipetim evolved; REMEMBER/LINEAGE taught Giga Drain, Magical Leaf, Extrasensory and later Reflect |
| Northern routes | Fiery Path, routes 111/113/114 and Fallarbor traversed by normal movement and battles |
| Meteorite scene | Native scene completed; Meteor Falls state 1 and Route112 cable-car blockade removed |
| Volcano | Cable car ridden; grunts, Tabitha and leader 602 defeated; event completed and exactly one meteorite collected |
| Gym | Four trainer encounters won (202, 204, 201, 203); elevator maze traversed in both directions |
| Nara | First attempt lost; second attempt won, trainer 268, outcome 1, with five conscious party members |
| Victory | Fourth badge, defeated-gym, Overheat and match-call flags set; exactly one Overheat TM; Petalburg gym state 6 |
| Revisit | Separate-process CONTINUE and conversation produced no new battle, duplicate TM or gym-state increment |
| Rival | Exiting normally gave one pair of Go-Goggles; Lavaridge state became 2 |
| Strength | Ordinary party menu offered action 22; boulder 3 moved from (17,15) to (16,15); vacated tile walked through; nobody learned Strength or spent PP, and the Strength HM was not owned |
| Desert | Go-Goggles gate traversed normally; final native checkpoint at Route111 (12,60), six healthy level-29 Pokémon and four badges |
| Storage | All three occupied box records retained their original identities and complete 80-byte hashes |

Chorume defeated the first four opponents and damaged Boitatá before fainting.
Morcego used Confuse Ray and Extrasensory to finish Boitatá. The winning battle
consumed three Super Potions. Rock Tomb and Bulk Up were taught to Caramelão
through their owned TMs, and the TMs were consumed normally; these moves were
not used in the winning battle. Four Energy Roots and one X Speed were also
purchased, but were not used. The trace records the actual move and item
choices, rather than attributing the victory to unexecuted preparations.

The complete final journal contains 31 trainer encounters: 30 wins and the
retained first Nara loss. The winning continuation follows that normal
whiteout, shopping and return to the gym; it does not reload a preferred
battle outcome. The journey journal starts from `fourth_cap29_prepared_20261016`,
whose own preparation journal links to the third-badge source. An earlier
unfinished navigation run was restarted from that normally saved preparation
checkpoint. No uninterrupted first-attempt claim is made.

## QA driver corrections

The controller now reads Disable, Torment and Taunt restrictions before
selecting a move. An observed Torment loop (trainer 78) and a Disable loop
(trainer 143) were recovered in the same live battles after correcting the
driver; their failed selections remain in the journal. Timeout recovery
retains the pending battle record. Magnitude's variable native damage is
scored at its expected base power of 71, and physical scoring accounts for
burn. Map-local NPC IDs are resolved from the map's object order. Navigation
replans when an approaching trainer occupies the planned standing tile and
recognizes the Lavaridge basement elevator behavior.

Preparation helpers teach an owned TM through the actual compatibility and
move-forgetting screens and purchase an exact quantity through the clerk's
normal menu. Campaign helpers retain source checkpoints, fourth-badge story
state, owned items, cable-car statistics and lossless gzip input/battle
journals. They never call game functions or write game RAM/ROM.

## Validation and limits

`test_campaign_badge04.py` passed against the real private victory SAVE,
including a separate-process CONTINUE of its revisit. `test_campaign_strength.py`
passed against the real approach SAVE, including the offered menu action,
unchanged moves/PP, physical push, passage and a separate-process CONTINUE.
Cold checks also passed for preparation, both control-loop recoveries,
meteorite scene, cable-car approach/arrival, volcano victory/clearing, gym
entry/midpoint, second-attempt preparation, Go-Goggles and the final desert
checkpoint. These tests require privately generated saves and are distinct
from fixture-based CI; fixtures are not campaign evidence.

Art freeze passed for 20,104 assets. The graphics/layout/audio diff against
protected Ciro reference `46d50777a45f8fbf1f7f600516a47873ec4fc804` is empty.
Public evidence includes selected receipts, screenshots and hashed compressed
journals. No ROM, native SAVE, emulator state or compiled helper is committed.
The fifth badge and later campaign remain pending; this is a fourth-badge
checkpoint, not a claim that the whole game has been completed.
