# Emerald residue cleanup — 2026-08-19

## Objetivo

Executar e proteger, pela infraestrutura do próprio repositório, os limpadores de resíduos visíveis do Pokémon Emerald que não dependem de arte nova.

## Escopo automatizado atual

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
12. `cleanup_pokedex_rating_residue.py`;
13. `cleanup_anahi_lab_system_residue.py`.

Cada limpador é executado e depois repetido com `--check`, permitindo verificar idempotência do lote. A CI normal também executa os treze validadores em modo `--check`.

## Regras

- preservar identificadores internos, flags, warps, save layout e progressão do Emerald;
- alterar somente superfície visível e documentação quando possível;
- não introduzir sprites, tiles, portraits, fontes ou qualquer outra arte nova;
- não depender de Codespaces;
- não tocar no PR legado #58;
- não interpretar falha de infraestrutura anterior ao Checkout como falha de código.

## Resultado de 19/08/2026

O lote do laboratório de Anahi foi integrado no PR #125 e fechou a issue #123. O diff do arquivo grande foi auditado e alterou somente os seis blocos de `.string` previstos.

Os runners do GitHub Actions, porém, encerraram os jobs antes do primeiro step (`steps: null`), inclusive após rerun. Assim, build e checks executáveis permanecem pendentes de infraestrutura, não de uma falha observada no repositório.

A proteção da `main` exige `repository-safety` e `build-and-test`; o workflow principal foi alinhado para publicar esses contextos quando os runners voltarem a iniciar jobs.

## Aceite para a próxima execução real

- `repository-safety` concluído;
- builds pt-BR e en concluídas;
- `build-and-test` concluído;
- nenhuma alteração proprietária versionada;
- qualquer item que exija arte permanece fora deste lote.
