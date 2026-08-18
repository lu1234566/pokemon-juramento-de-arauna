# Serra do Uivo apartment Horizonte surface fix

A small apartment NPC still displayed the malformed automated replacement `CONSORCIO HORIZONTEORATION's workers live in this building.`

This lot changes only that player-facing string to a short Portuguese line identifying the residents as Consórcio Horizonte workers. The inherited Rustboro/Devon label names remain untouched as implementation skeleton, and the Skitty interaction is unchanged.

No map data, object IDs, flags, warps, progression or items change. The deterministic helper rejects the malformed `HORIZONTEORATION` token and verifies the exact replacement block.

GitHub Actions is intentionally not used while the monthly quota is exhausted; this micro-lot is small enough for complete source/diff inspection under the temporary no-Actions policy.
