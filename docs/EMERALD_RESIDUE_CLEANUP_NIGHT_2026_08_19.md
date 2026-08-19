# Emerald residue cleanup — 2026-08-19

## Objetivo

Executar, pela infraestrutura do próprio repositório, todos os limpadores automáticos já versionados para remover resíduos visíveis de Pokémon Emerald que não dependem de arte nova.

## Escopo automatizado

O workflow `.github/workflows/apply-emerald-residue-cleanup.yml` executa em sequência:

1. `cleanup_emerald_residue_signs.py`;
2. `cleanup_match_call_residue.py`;
3. `cleanup_ciro_route_residue.py`;
4. `cleanup_littleroot_house_residue.py`;
5. `cleanup_battle_message_residue.py`;
6. `cleanup_vila_amanhecer_residue.py`;
7. `cleanup_intro_speech_residue.py`;
8. `cleanup_region_map_names.py`;
9. `cleanup_system_ui_identity.py`;
10. `cleanup_route119_surface_residue.py`;
11. `cleanup_val_household_residue.py`;
12. `cleanup_pokedex_rating_residue.py`.

Cada limpador é executado e depois repetido com `--check`, garantindo idempotência do lote.

## Regras deste lote

- preservar identificadores internos, flags, warps, save layout e progressão do Emerald;
- alterar somente superfície visível e documentação quando possível;
- não introduzir sprites, tiles, portraits, fontes ou qualquer outra arte nova;
- não depender de Codespaces;
- validar a branch com GitHub Actions antes do merge;
- não tocar no PR legado #58.

## Aceite

- workflow de cleanup concluído;
- build padrão concluída;
- nenhuma alteração proprietária versionada;
- mudanças geradas revisadas antes do merge;
- qualquer item que exija arte permanece explicitamente fora deste lote.
