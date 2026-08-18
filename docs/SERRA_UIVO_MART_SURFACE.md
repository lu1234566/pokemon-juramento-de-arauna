# Serra do Uivo Mart visible-language cleanup

The inherited Rustboro Mart still had three fully English NPC conversations, including a visible Petalburg Woods reference, even though the shop itself is already structurally correct for Serra do Uivo.

This micro-lot localizes only those three NPC string blocks. The basic and expanded PokéMart inventories, the Devon-derived unlock condition, Timer/Repeat Ball availability, clerk flow, item IDs, flags and all executable script commands remain unchanged.

No new place name is invented for Petalburg Woods; the localized NPC simply refers to the nearby forest generically. The source validator checks the exact localized anchors, rejects the old English/Petalburg Woods text and enforces a 32-character maximum per visible segment.

GitHub Actions is intentionally not used while the monthly quota is exhausted; this text-only micro-lot is fully inspectable from its diff.
