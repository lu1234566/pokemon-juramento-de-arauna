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
