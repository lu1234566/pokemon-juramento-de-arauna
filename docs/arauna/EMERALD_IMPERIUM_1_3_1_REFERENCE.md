# Emerald Imperium 1.3.1 balance reference

This is a design study for Pokémon Juramento de Arauna. It records structural lessons from the
Emerald Imperium 1.3.1 ROM and its public battle, encounter, change and changelog documents.
Arauna does not copy trainer teams, maps, dialogue, sprites or proprietary ROM data.

## Material reviewed

- the 1.3.1 game ROM, used only to verify the build identity and GBA header;
- the compact and sequential Boss Battles workbooks;
- the 1.3 Encounter Tracker workbook;
- the 77-page routes, gifts and eggs guide;
- the 1.3.1 stats, types, abilities and moves workbook;
- changelogs from versions 1.1, 1.2, 1.3 and 1.3.1.

The two Boss Battles files are complementary rather than duplicates. The compact workbook is easier
to parse by trainer category; the larger workbook places fights in suggested campaign order and includes
damage-calculator fields, IVs, EVs and speed values.

## What the numbers show

### Progression

Imperium uses 19 explicit caps:

`15, 20, 25, 30, 32, 34, 44, 47, 56, 59, 64, 68, 71, 74, 76, 80, 82, 84, 85`.

They are not simply badge caps. Rival fights, villain gauntlets, the Trick House, Victory Road and the
Champion also advance the curve. This supports a campaign with many more mandatory battle checks than
base Emerald.

The compact workbook contains 134 machine-detectable boss or mini-boss team blocks. Some sheets include
paired trainers or reward columns, so this count is a structural sample rather than a claim about the exact
number of unique NPCs.

### Team and resource ramp

- Roxanne uses four Pokémon at levels 14-15.
- Brawly uses five Pokémon at levels 23-25.
- Wattson uses five Pokémon at level 34.
- major mid- and late-game teams usually reach six members;
- nearly every documented boss Pokémon holds an item;
- the version 1.1 changelog explicitly removed EVs from Pokémon before Wattson;
- documented teams from Wattson onward commonly use complete 510-EV spreads;
- late teams use coordinated weather, terrain, speed control, switching, resist berries and role compression.

The useful lesson is the order in which complexity appears. A larger early team can still be readable when
its moves are simple. Full items, optimized EVs and advanced switching should not all arrive at the same time.

### Encounter availability

The tracker contains 104 named encounter locations and lists 730 species/form labels. A median location has
16 populated encounter entries across all methods. Core land tables use the 12 standard GBA slots, commonly
with broad species variety; Route 101, for example, exposes 12 different land species.

The encounter documents also deliberately move rewards and species when a boss answer would otherwise be
available too early or too late. This means boss difficulty is partly an ecology problem: a counter is fair
only if the player can obtain it before the fight.

### Species and mechanics

The change workbook includes 1,192 comparable species/form rows:

- 236 have changed base stats;
- 43 have changed typing;
- 525 have changed ability sets;
- the median base-stat-total change among stat edits is +10;
- the median total movement across the six stats is 25 points;
- 125 moves and 30 abilities have documented changes;
- three moves and 16 abilities are marked as new.

This is selective rebalance rather than a universal stat increase. Arauna should preserve the same principle:
give each Fakemon a role, then change only the numbers or tools needed to make that role work.

### Fairness and maintenance

The changelogs repeatedly fix AI information leaks, bad damage assumptions, switch logic, unavailable rewards,
DexNav level-cap exploits and emulator crashes. They also add nurses before long gauntlets and delay automatic
level-cap tools until move learning is safe. The project treats quality-of-life and reliable information as part
of difficulty design.

## Arauna decisions derived from the reference

| Imperium pattern | Arauna adaptation |
|---|---|
| 19 hard progression checks | Nine soft targets until Arauna has additional mandatory story milestones |
| Four to five Pokémon immediately | Four readable members at Badge 1; full teams arrive gradually |
| Near-universal boss held items | One telegraphed ace item early, broader item use later |
| Full EVs from Wattson onward | No early EVs, partial specialization mid-game, full optimization at the League |
| Forced restrictions in Normal mode | Bag and Shift remain available in the default Arauna campaign |
| Very broad encounter catalogue | Eight or more distinct land choices in core areas, within the 386-species Census |
| Many specialized optional fights | Mandatory bosses teach mechanics; optional rematches may approach Imperium intensity |
| Highly capable custom AI | Strong visible-information AI without knowledge of unseen player data |

## Non-copying rule

Imperium teams are test cases, not templates. Arauna bosses will use Arauna species, Brazilian-biome ecology,
their own roles and story identities. A team may borrow a general concept such as rain control or a resist-berry
ace, but it must have new members, sequencing and counterplay.

