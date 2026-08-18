# Mata do Meio Pokemon Center visible-language cleanup

The inherited Fortree Pokemon Center still contained three fully English NPC conversations and a visible reference praising DEVON, while the surrounding city and story surface already use Mata do Meio and Consórcio Horizonte.

This micro-lot localizes only those three NPC `.string` blocks. The nurse flow, Fortree heal-location ID, Cable Club resume hook, Safari Zone reference, Match Call mechanics and every executable command remain unchanged. The visible corporate reference is rewritten as HORIZONTE without renaming any backing Emerald symbol.

The source validator checks localized anchors, rejects the old English/DEVON fragments and enforces a 32-character maximum per visible segment.

GitHub Actions is intentionally not used while the monthly quota is exhausted; the complete text-only diff is small enough for direct inspection.
