# Mata do Meio city visible-surface cleanup

The city already uses Mata do Meio and Lidia on its main sign, but several NPC blocks remain inconsistent: untouched English dialogue, a resident accidentally speaking as Lidia, an unrelated sensor/Archive monologue assigned to the rainwater NPC, and inherited DEVON SCOPE prompts around the invisible Kecleon.

## Prepared cleanup

Nine existing string blocks are rewritten without changing their callers:

- local resident recollection about the large Pokémon flying toward Route 131;
- resident blocked from the gym, then ready to challenge Lidia after the obstruction clears;
- tree/rainwater and treehouse-life NPCs restored to their environmental roles;
- trade-evolution NPC localized;
- invisible-obstruction prompts use the player-facing `LENTE HORIZONTE` identity.

The existing city/gym signs and Ciro/Horizonte story NPC remain untouched.

## Safety boundary

Only `.string` blocks change. `ITEM_DEVON_SCOPE`, `FLAG_KECLEON_FLED_FORTREE`, Kecleon species/object/movement, gym-access event, heal/map IDs, route IDs, saves and progression remain unchanged.

This is preparation-only while GitHub Actions quota is exhausted. Activate after the Horizonte key-item identity lot from the newest canonical main; Codespaces remains last resort.
