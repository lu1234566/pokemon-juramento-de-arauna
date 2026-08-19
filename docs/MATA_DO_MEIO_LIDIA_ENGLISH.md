# Mata do Meio and Lidia — English narrative surface

Status: English-only narrative continuation.

This slice closes the main visible surface of Fortree's replacement as MATA DO MEIO and rewrites Lidia's gym around inherited routes, observation and memory without changing Emerald gameplay wiring.

## Mata do Meio

The city is presented as a canopy community whose bridges and habits depend on routes learned across generations. Residents notice that familiar POKéMON paths and responses are beginning to fail. One resident explicitly recalls CIRO watching a longtime partner freeze when called and then staring at his HORIZON device.

The city and gym signs use `MATA DO MEIO` as the canonical proper name. The local scope interaction is surfaced generically as a `FIELD SCOPE`; the internal `ITEM_DEVON_SCOPE` check remains untouched.

## Lidia

LIDIA treats inherited paths, songs, fear and trust as forms of memory that should be observed before anyone decides what they mean. Her challenge emphasizes adaptation without erasure.

Her post-battle thesis is concise:

> A path is not a command. Memory should guide, not own us.

This directly supports Arauna's broader consent theme without turning the gym into a faction lecture.

## Gym surface

The guide, six gym trainers, statues, leader dialogue, rematch dialogue and PokéNav registration now consistently name LIDIA / MATA DO MEIO instead of Winona / Fortree.

The sixth Arauna badge is surfaced in English as `PLUME BADGE`, translating the existing canonical `INSÍGNIA PLUMA` rather than restoring Emerald's old visible badge name.

## Preserved

The renderer requires the following internal mechanics to remain present:

- `TRAINER_WINONA_1` and the existing trainer party;
- rotating-gate puzzle specials;
- Kecleon and `ITEM_DEVON_SCOPE` interaction;
- `FLAG_DEFEATED_FORTREE_GYM`;
- `FLAG_BADGE06_GET`;
- `ITEM_TM_AERIAL_ACE` and its received flag;
- Winona Match Call internals;
- `FLAG_SCOTT_CALL_FORTREE_GYM`, which continues into the visible Seu Bento call.

No map geometry, collision, warp, save layout, trainer party, item behavior or flag progression is changed.
