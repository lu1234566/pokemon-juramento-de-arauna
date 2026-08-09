# Arauna difficulty model

Arauna uses [Pokémon Emerald Imperium](https://www.pokecommunity.com/threads/new-release-pokemon-emerald-imperium.534582/)
as a structural reference for strategic battles: progression targets, stronger AI, manually reviewed bosses,
clear aces and meaningful team roles. It does not copy Imperium's teams or its full difficulty restrictions.

## Intended experience

The default campaign should require adaptation without requiring competitive knowledge or repeated grinding.
A player who catches several local species, reads move descriptions and changes a weak matchup should be able
to win. A player who relies on a single overlevelled starter should feel resistance, but should never become
unable to progress.

## Three trainer layers

| Layer | Team construction | AI | Items |
|---|---|---|---|
| Route trainer | One simple idea, limited coverage | Basic decisions | Usually none |
| Mini-boss/rival | Two complementary roles | Switching and visible matchup awareness | One or two telegraphed items |
| Major boss | A clear strategy, counterplay available nearby, ace last | Strong but non-omniscient | Ace item, then broader items late-game |

## What Arauna adopts now

- soft level targets tied to the existing eight-badge campaign and the League;
- dedicated non-omniscient AI tiers for ordinary trainers, mini-bosses, single bosses and double bosses;
- stronger AI on the eight first Gym battles, Elite Four and Champion;
- a visible held-item ace in the last slot of every principal boss;
- automated validation and a reviewable difficulty report.

The detailed source study and the resulting adaptation decisions are recorded in
`docs/arauna/EMERALD_IMPERIUM_1_3_1_REFERENCE.md`.

## Complexity ramp

Imperium's strongest lesson is that level, party size, held items, EVs and AI should not spike together.
Arauna therefore introduces them in separate layers:

| Campaign point | Party target | Held items | Training data | Strategic expectation |
|---|---:|---:|---|---|
| Badge 1 | 4 | 1 ace item | No EVs | Read the boss theme and switch once |
| Badge 2 | 4 | 1-2 | No EVs | Use status or a secondary counter |
| Badges 3-4 | 5 | 2 | Partial specialization | Answer coverage and one speed-control tool |
| Badges 5-6 | 5 | 2-3 | Partial specialization | Break a coherent field or tempo plan |
| Badges 7-8 | 6 | 4-6 | Strong, not universally perfect | Manage roles across a full team |
| League | 6 | 6 | Fully reviewed spreads | Demonstrate the campaign's learned systems |

These are design targets for the final Arauna teams. The current inherited Emerald parties remain a temporary
runtime scaffold until boss identities and biome ordering are locked.

## Encounter fairness

Difficulty is validated against what the player can catch, not only against theoretical type charts.
Core campaign land tables must provide at least eight distinct choices, and every badge window must expose
at least three direct type answers through land encounters alone. The final team review will narrow that to
at least two *practical* answers after moves, stats, evolution levels and boss coverage are considered.

Story-reserved, legendary, mythical and sensitivity-review entries are forbidden from random wild tables.
This is enforced by `tools/arauna/audit_arauna_encounters.py`.

## What remains deliberately disabled

- no forced Set battle style;
- no ban on Bag use during trainer battles;
- no hard experience cap;
- no perfect EV spreads in the early campaign;
- no AI access to unseen moves, items, abilities or the player's complete party;
- no final redesign of boss species until story order and biome encounters are stable.

## Next balance pass

Once the new story sequence fixes each boss's identity, each major team will be rebuilt from Arauna species.
Every boss will expose at least two viable answers in the preceding biome, avoid unavoidable opening KOs,
and use one central strategy rather than six unrelated competitive sets. Optional bosses may later approach
Imperium's Normal difficulty; the mandatory campaign will remain the more accessible baseline.
