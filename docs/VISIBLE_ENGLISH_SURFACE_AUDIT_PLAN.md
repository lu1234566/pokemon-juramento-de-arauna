# Visible English surface audit

The Arauna semantic rewrite deliberately focused on the principal story surface, so secondary NPCs and inherited utility dialogue can still appear in English. Identity-token cleanup alone cannot detect that class of residue.

## Heuristic

`tools/audit_visible_english_surface.py` scans player-facing `.string` blocks in `data/maps` and `data/text`. It ignores symbols explicitly named `Unused` and reports a block only when at least two distinct high-signal English words are present. This avoids treating proper names, Pokémon vocabulary and implementation labels as translation failures.

The audit is report-only. It must not automatically translate text because meaning, speaker role and Arauna context matter more than literal word replacement.

## Intended workflow

1. Run the report against current canonical `main`.
2. Rank findings by story visibility and concentration of English markers.
3. Convert them in focused location/character lots using exact-label deterministic generators.
4. Preserve all Emerald event wiring and gameplay data.
5. Re-run the report until only deliberately retained/system-neutral English remains, documenting any allowlist instead of hiding it.

This preparation was recreated while GitHub Actions quota is exhausted. Codespaces remains a last-resort execution environment if the report itself becomes necessary to unblock prioritization.
