# Emerald residue cleanup — lot 2

This lot removes high-visibility vanilla identity leaks from the Serra do Uivo / Rustboro story slot without changing event wiring.

## Visible text corrected

- broken `CONSORCIO HORIZONTEORATION` wording is replaced with Arauna-native Consorcio Horizonte text;
- MAY and BRENDAN Match Call registration dialogue is surfaced as CIRO while the underlying Emerald labels remain untouched;
- the registration confirmation now names CIRO;
- Devon-facing exterior signs are rewritten as Consorcio Horizonte / Serra do Uivo signage.

## Safety boundary

Only existing `.string` blocks are replaced. Labels, flags, variables, object events, movement, coordinates, warps, item IDs, trainer data and progression remain unchanged.

The cleanup tool verifies the exact expected lines and rejects legacy identity tokens inside every targeted block.
