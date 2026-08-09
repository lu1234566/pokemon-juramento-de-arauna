# Story-masked badge trials

This branch adds the first two Gym-style boss battles without presenting them as
conventional Gyms. Both are framed as the final action inside an existing story
mission, and both reuse existing Emerald maps, NPC positions, trainer classes and
battle presentation. There is **no new map**.

## Tide Vigil

Dona Celina is Porto das Redes' local Storyteller and guardian of the House of
Tide. Before she opens the Vigil, the player must hear the fisher memorial, read
the Consortium discharge permit, recover the dockworkers' unfinished song and
inspect Celina's embroidered net. Those four pieces unlock the field Agent
confrontation, which retains a pre-battle heal after the investigation route.

After the Agent is defeated, Celina completes her husband's verse with the
player. The player returns to Route 109, restores Iaraco through song and receives
Iara-Mae's non-capturable Testimony. Only then does Celina begin the mandatory
Tide Vigil through her reassigned Slateport NPC.

Her provisional three-member party targets levels 14, 15 and 17. The current
species slots remain temporary until the first approved Emerald-style art batch.
Losing preserves the completed investigation and Testimony and returns the player
to the battle gate; winning records the trial before the Mare Badge is awarded.

## Trial of Echoes

After the player uses Libras to calm Lobisomem, the hermit asks for a final
answer through action. The mandatory battle uses the existing Route 114 hermit
NPC. Losing does not repeat the Libras or Lobisomem scenes; winning records the
trial before the Uivo Badge can be awarded.

The provisional team is Morcim at level 23, Argilim at level 24, Cristalim at
level 25 and Granito at level 27. The trial tests observation and adaptation; it
does not portray deafness as an obstacle or turn Lobisomem into a capturable
boss.

## Save and retry contract

- Story resolution happens before each battle gate.
- A loss never sets the trial-complete or badge flags.
- A win sets a dedicated trial flag before granting the badge.
- Re-entering after a loss retries only the battle.
- Re-entering after a win cannot duplicate the battle or badge.
- The first playable runtime remains English-only.
- Global EXP Share and DexNav remain outside this branch.
