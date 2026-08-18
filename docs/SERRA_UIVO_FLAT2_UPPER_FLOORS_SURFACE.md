# Serra do Uivo residential upper-floor cleanup

The inherited 2F/3F apartment dialogue still exposed DEVON/CORPORATION/PRESIDENT family lore even though the surrounding district is already Serra do Uivo and Consórcio Horizonte.

This micro-lot localizes only five player-facing string fragments across the two tiny residential scripts. The 2F child still grants the same Premier Ball through the same event, flag and item path. The 3F NPCs are reinterpreted as residents discussing Horizonte field work and local mineral collecting rather than an inherited president/son relationship.

Internal Rustboro/Devon/President label names remain unchanged as implementation skeleton. No executable script command, item ID, flag, object, map, warp, save data or progression logic changes.

The source-level validator rejects visible DEVON/CORPORATION/PRESIDENT tokens in these two files and checks every string segment against the 32-character width boundary. GitHub Actions is intentionally not used while the monthly quota is exhausted.
