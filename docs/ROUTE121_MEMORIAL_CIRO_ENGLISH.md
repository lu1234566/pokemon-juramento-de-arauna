# Route 121 — Ciro and the road to the Memorial

Status: English-only narrative continuation.

This slice turns the short Route 121 Mt. Pyre transition into Arauna's approach to the MEMORIAL DOS NOMES without changing the existing three-grunt movement event.

## Ciro

Ciro does not receive a new object or event on this route. Instead, a civilian describes seeing him pass through after Mata do Meio and Route 120.

He asks whether the names connected to M'BOI are people or merely records, then continues toward the memorial alone. This is intentionally quieter than a direct confrontation: his confidence in HORIZON is beginning to fracture before he has language for what replaces it.

## HORIZON movement

The unchanged three-Aqua-object sequence now surfaces as a HORIZON field team moving toward the memorial to secure the RECORD-MATRIX.

`VAR_ROUTE121_STATE`, all three local object IDs and the existing exit movements remain unchanged.

## Route surface

- `MT. PYRE` is replaced by the visible `MEMORIAL DOS NOMES` destination;
- the old pier sign becomes `MEMORIAL DOS NOMES PIER`;
- the old `SAFARI ZONE` sign is surfaced as `ARAUNA WILDLIFE PRESERVE` while the underlying map/facility wiring remains untouched.

## Technical contract

Four text blocks are anchor-checked and rendered through a matcher that safely handles the legacy physical backslash-newline source format. All new visible segments are at most 32 characters.

No trainer IDs, map geometry, object placement, movements, route state, warps, saves or art are changed.
