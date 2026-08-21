# Encruzilhada Central — English story surface

## Scope

This pass closes the mandatory Encruzilhada Central arc immediately after Route 110.

It keeps the inherited Mauville event graph intact and replaces only player-facing `.string` blocks in:

- `data/maps/MauvilleCity/scripts.inc`
- `data/maps/MauvilleCity_Gym/scripts.inc`

The reviewed bank contains 62 blocks.

## Val

The inherited Wally scene is surfaced as VAL consistently.

Val does not challenge Olivia to prove that illness, fear, or vulnerability never existed. His arc is about finding his own pace and choosing to move while fear is still present.

The player battle remains mechanically identical. The loss becomes useful evidence for Val rather than a humiliation. His POKéNAV registration remains the inherited Wally state internally.

Seu Bento's inherited Scott appearance focuses on the distinction between care and pity: the player gives Val an honest battle without turning concern into an easy victory.

## Olivia

The inherited Wattson surface becomes OLIVIA.

Her Gym is framed around electrical networks, routing, load, visible consequences, and safe failure. The switch puzzle remains completely unchanged mechanically.

The visible third badge is **BEACON BADGE**, translating the already established `INSÍGNIA FAROL` surface while preserving internal `BADGE03`.

TM34 remains SHOCK WAVE. ROCK SMASH progression remains unchanged.

Olivia's later inherited New Mauville request is reframed as an unsafe old power relay below the city. She asks the player to trace and shut down the fault rather than treating electrical infrastructure as automatically good because it represents progress.

## Encruzilhada Central

The city is presented as Arauna's crossroads: four roads and a shared grid carrying goods, people, news and competing accounts.

Visible civic signs use:

- ENCRUZILHADA CENTRAL
- ENCRUZILHADA CENTRAL GYM
- ENCRUZILHADA CYCLES
- ENCRUZILHADA GAME HALL

## Safety contract

The renderer:

- requires every one of the 62 target labels exactly once;
- replaces only consecutive `.string` lines immediately below those labels;
- accepts the reviewed source or an already-rendered source;
- checks all visible segments at <=32 characters using a conservative 16-character placeholder;
- masks every target and proves all non-target script structure is byte-stable;
- preserves representative progression tokens for Val, Olivia, the Gym, the power-relay sidequest, items, Match Call, badge state and barrier state;
- rejects surviving WALLY, WATTSON, MAUVILLE, RYDEL and Portuguese placeholder residue inside owned blocks.

No trainer teams, movements, warps, map geometry, flags, vars, badge order, item IDs or save structure are changed.

PR #58 remains outside scope.
