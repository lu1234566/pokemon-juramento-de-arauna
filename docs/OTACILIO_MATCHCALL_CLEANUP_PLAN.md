# Otacílio Match Call cleanup

The inherited Mr. Stone contact still exposes one of the clearest remaining Emerald identities in the PokéNav: MR. STONE / DEVON PRES plus eleven vanilla calls about Devon, Steven, Rustboro, Petalburg and Norman.

## Canonical reinterpretation

The same structural contact becomes Dr. Otacílio Meira, director of the Consórcio Horizonte. Its eleven existing call slots are preserved, but the visible dialogue now follows the established Arauna arc: Serra do Uivo, Seu Bento, Porto das Redes, Porto do Sal, Galerias da Serra, Elias, M'Boi and the Arquivo Vivo.

The PokéNav card changes only its visible values:

- `MR. STONE` -> `OTACILIO`
- `DEVON PRES` -> `DIRETOR`

## Safety boundary

Internal Mr. Stone symbols, call indexes, availability conditions, flags and progression remain unchanged. No trainer data, maps, items, route order, save structures or event wiring are modified.

## Activation

After the current GitHub Actions infrastructure failure clears, recreate/copy this deterministic tool onto a fresh `narrative/emerald-residue-run-*` branch from the newest green `main`, wire it into the shared cleanup workflow, generate and verify `data/text/match_call.inc` plus `src/strings.c`, add a final user-authored validation commit and require a successful full custom Emerald ROM build before merge.
