# Story-masked badge trials

This branch adds the first two Gym-style boss battles without presenting them as
conventional Gyms. Both are framed as the final action inside an existing story
mission, and both reuse existing Emerald maps, NPC positions, trainer classes and
battle presentation. There is **no new map**.

## Tide Vigil

After Iaraco's color and Iara-Mae's Testimony are restored, Dona Zila asks the
player to hold course while the tide changes. The mandatory battle takes place
through her existing Slateport NPC. Losing preserves the completed testimony and
returns the player to the battle gate; winning records the trial before the Mare
Badge can be awarded.

The provisional team is Botim at level 16, Sucurim at level 17 and Capivim at
level 19. Names, levels, moves and dialogue remain provisional until the author's
near-complete narrative script is incorporated.

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
