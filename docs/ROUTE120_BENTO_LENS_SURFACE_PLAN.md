# Route 120 Seu Bento / Horizonte lens surface

The mandatory Route 120 bridge scene already displays Seu Bento instead of Steven, but six distinct moments reuse the same unrelated monologue, while the Kecleon prompts and route sign still expose `DEVON SCOPE`, English text and `FORTREE CITY`.

## Prepared reinterpretation

Seu Bento now notices the invisible obstruction, asks whether the player is ready, reveals it with a Horizonte lens, reacts to the encounter, gives the lens to the player and leaves toward Mata do Meio. The three Kecleon interaction strings are localized and the route sign uses Mata do Meio.

The visible bag identity for the same device is prepared separately as `LENTE HORIZ.` because the engine's item-name limit is 14 characters. Dialogue may spell `LENTE HORIZONTE` in full.

## Safety boundary

Only existing `.string` blocks in `data/maps/Route120/scripts.inc` are targeted. `ITEM_DEVON_SCOPE`, `FLAG_RECEIVED_DEVON_SCOPE`, Kecleon species/battle setup, object IDs, bridge metatiles, weather, route IDs, movements, item grant and progression remain unchanged.

This is preparation-only while GitHub Actions quota is exhausted. Activate from the newest canonical main after the Horizonte key-item identity lot; Codespaces remains last resort.
