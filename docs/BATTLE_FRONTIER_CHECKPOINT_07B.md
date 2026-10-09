# Battle Frontier 07B — Battle Dome V1

Quatro salas recebem bancos privados de pedra azulada, madeira escura e bronze. A inscrição nativa passa de BATTLE FRONTIER a ARAUNA CIRCUIT, acompanhando a terminologia dos scripts existentes. Referências: Master Map Design Bible, concept da Liga e checkpoint 07A recuperados antes da edição. A mudança é visual; regras, torneio e progresso permanecem exatos.

Base: `fc408a604b0f2c0b1cc28b3e20a7a9aac6b20596` (07A). GitHub conferido: integrador em `7e9d29dc5fdab047ac663dd2953a83ff9a51c0b8`, main 95 commits atrás. Bundles para 07A, 7e9 e 989/06C2 conservam esse histórico e as correções da engine.

| Mapa | Dimensões | Células | Objetos | Warps |
|---|---:|---:|---:|---:|
| BattleDomeLobby | 23×17 | 391 | 6 | 2 |
| BattleDomeCorridor | 48×7 | 336 | 1 | 2 |
| BattleDomePreBattleRoom | 9×8 | 72 | 1 | 2 |
| BattleDomeBattleRoom | 20×10 | 200 | 15 | 0 |

Total: 999 células e quatro layouts exclusivos. Nenhum layout é adicionado; IDs e ordem dos 754 layouts continuam iguais. Os únicos arquivos anteriores editados são layouts.json e três cabeçalhos de bancos, com bloco append isolado. Grids, bordas, colisão, atributos, máscaras de ambos os planos, scripts, eventos, warps, inscrições/textos de scripts, dados de torneio, treinadores, recompensas, saves e progressão são preservados. As dez células dos footprints de portas mantêm seus pixels, assim como paletas 7 e 9, gráficos de portas e ambos os arquivos de engine.

## Animação e capacidade

246 metatiles recebem arte, mantendo os IDs. Os bancos privados conservam callbacks Building e BattleDome e os 435 atributos nativos. Apenas a paleta antes não referenciada 12 recebe materiais novos. Todas as paletas 0–11 permanecem exatas.

A paleta 8 animada atualiza quatro quadros; apenas os índices 13 e 15 variam. Os 396 quadrantes que usam essa paleta conservam a paleta e as posições de cada índice animado: 792 máscaras verificadas. As novas texturas usam os índices estáveis. Não há novos pixels animados nem interrupção das luzes. Os bancos 4bpp têm no máximo 512 tiles cada, e a alocação estática exclui 432–511 e 992–1023, reservados para animações e portas.

## Verificação

- 23.096 dependências anteriores preservadas por SHA-256, incluindo field_door.c, overworld.c, battle_dome.c, scripts e todos os checkpoints anteriores.
- 854 máscaras de planos secundários e 435 atributos exatos; dez células de portas exatas.
- Seletores visuais originais executados em C: 999 células locais, 20.480 casos de fallback e 53.167 células anteriores de cavernas/Dive. Os sete mapas Tower do 07A retêm seus renders exatos.
- C original das portas: 1.026 roteamentos, 16 casos de desenho/flag Multi e seis casos específicos das três portas Dome, incluindo a combinação de paletas 9/7 da sala pré-batalha.
- C original das luzes e BlendPalette: 865 casos, quatro quadros, 17 coeficientes de fade, três cores alvo, suspensão durante intro e 32 atualizações finais até desligar callback.
- Instalação real, pré-validação, corrupção, alterações locais, bases incorretas, rollback, reaplicação idempotente e reconstrução determinística: resultados em review/frontier_07b/install_test.json.
- Auditoria oficial de mapas e static readiness: logs anexos. A etapa ARM é explicitamente pulada pelo gate estático.

Limites: os testes C usam serviços explícitos do host para VRAM, tarefas, flags e desenho. Não executam o interpretador de scripts/batalha, sprites, partidas, saves ou uma ROM no emulador. ARM e mGBA não estão disponíveis neste ambiente. As prévias são renders RGB555 nativos sem atores, não screenshots do jogo.

## Retomada

Pacote incremental sobre o 07A; cumulativos para GitHub 7e9 e 06C2/989. O instalador verifica toda a base antes de escrever, conserva HEAD, cria backup e faz rollback; um bundle importa o commit e a árvore completa. Nenhum push.

Concluídos 11/47 mapas Frontier. Restam 36. Próximo checkpoint 07C: seis mapas de Battle Palace e Battle Arena. Plano completo em review/frontier_07b/checkpoint_plan.json.
