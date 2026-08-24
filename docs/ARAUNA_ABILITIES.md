# Arauna abilities

The 386 creatures draw on 46 abilities. None of them is a new battle effect:
each claims one Gen 3 slot whose behaviour already carries it, and that slot's
visible name and description are rewritten. The player reads Arauna's identity
while the mechanics stay code that shipped in 2005.

That was a deliberate trade. A genuinely new ability means new branches in the
battle engine, and those break in ways only a late-game playthrough finds --
the wrong thing to introduce during a pre-launch pass. The pairing lives in
`data/text/arauna/ability_map.json`, one line per ability, so any of these can
be re-judged and re-applied without touching code.

## Where the pairing is exact

Twenty-two abilities are the Gen 3 ability under a Portuguese name, so the
effect is the one a player would expect: Torrente/Torrent, Espessura/Overgrow,
Chama/Blaze, Enxame/Swarm, Vista Aguçada/Keen Eye, Olho Composto/Compound Eye,
Intimidação/Intimidate, Levitação/Levitate, Estática/Static, Corpo
Flamejante/Flame Body, Determinação/Guts, Sincronia/Synchronize,
Corredor/Run Away, Muda/Shed Skin, Escama Dracônica/Marvel Scale, Nuvem de
Areia/Sand Stream, Corpo Metálico/Clear Body, Coragem/Inner Focus, Véu
Vegetal/Chlorophyll, Corpo Rochoso/Rock Head, Encanto/Cute Charm, Corpo
Fedido/Stench.

## Where a judgement was made

Gen 3 has no equivalent for these, so each took the closest compatible effect.
These are the ones worth re-reading:

| Arauna | Shown as | Effect borrowed | Why |
| --- | --- | --- | --- |
| Vento Veloz | Swift Wind | Swift Swim | speed that arrives with weather |
| Ritmo | Rhythm | Speed Boost | momentum that builds over turns |
| Placidez | Placid | Own Tempo | a calm that resists confusion |
| Colheita | Harvest | Pickup | gathering between battles |
| Faro | Scent | Illuminate | a nose that draws encounters in |
| Faro Fiel | Faithful | Vital Spirit | a watchful dog does not sleep |
| Alerta | Alert | Insomnia | same reading, different creature |
| Cara de Mau | Grim Face | Battle Armor | a face that refuses a clean hit |
| Ponto Cego | Blind Spot | Shield Dust | the added effect never lands |
| Poeira | Dust Cloud | Sand Veil | cover raised from the ground |
| Alma Antiga | Old Soul | Pressure | age that wears an opponent down |
| Véu Mágico | Magic Veil | Natural Cure | protection that mends on leaving |
| Presságio | Omen | Serene Grace | a hint of what is about to happen |
| Ponto Fraco | Weak Spot | Hustle | swinging for the weak point, wildly |
| Escavador | Digger | Arena Trap | digging that cuts off escape |
| Brincalhão | Playful | Truant | play that skips a turn |
| Travessura | Mischief | Sticky Hold | nothing is taken from it |
| Corpo Seco | Dry Body | Immunity | dryness that resists poison |
| Rasgo Rápido | Quick Tear | Hyper Cutter | claws that stay sharp |
| Garra Dura | Hard Claw | Shell Armor | hardness that blunts a critical |
| Fura-mão | Piercer | Rough Skin | it hurts to touch |
| Motor Elétrico | Motor Drive | Volt Absorb | electricity feeds it |
| Fuga | Escape | Limber | never held still |

`Fuga` and `Corredor` both read as fleeing; `Corredor` took Run Away, so `Fuga`
took Limber, on the argument that what stops a runner is paralysis. If that
reads wrong, swapping the two is a one-line change in the map.

Base stats come from the project's own `pokedex.json` and are copied across
unchanged. Evolutions are untouched.
