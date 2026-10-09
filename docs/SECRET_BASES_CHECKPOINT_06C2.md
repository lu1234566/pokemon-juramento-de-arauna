# Arauna — Bases Secretas em árvores e arbustos, 06C2 V1

Oito interiores concluídos: Tree1–4 e Shrub1–4. Junto ao 06C1, fecha as 24 Bases Secretas. Próximo ciclo: Battle Frontier, 47 mapas, em checkpoints por instalação.

## Base recuperada e conciliada

O pacote 06C1 foi recuperado e conferido antes das edições: commit `0098c5c3b54e32b925e4ff839cd0535e772b6778`, ZIP SHA-256 `9a80f3d9660c41d9caaed2ea37410d2b37fd351f3a828a17efd8a07978d6de84`. A Master Map Design Bible e os 82 concepts permanecem em docs/referencias/bible_concepts_recuperados.

O integrador do GitHub avançou para `872f56e86f09d3dff41a9e6c7a8bc5640386fe86`: remove as declarações de 26 bancos antigos sem referências e complementa docs/MANUTENCAO_2026_10.md. Foi conciliado sem conflitos com o 06C1; a base deste incremento é `6cfba8c79b4bc674d9962063f7fdb2d18a238fa4`, com o 06C1 e a manutenção como pais. O novo contrato congela essa base conciliada. Não altera os contratos históricos dos pacotes anteriores.

Main `979fb6c1b6731561f3c993efd6045a9bbf096c54` está 89 commits atrás do integrador. A conciliação preserva a manutenção e os pacotes 06A/06B/06C1. Não houve push nem mensagem ao autor.

## Direção visual

A seção Mata do Meio da Bible orienta mata densa, solo sombreado, madeira e passarelas funcionais. O concept da Rota 104 traz vegetação retomando a trilha. A Bible não possui um capítulo dedicado às Bases Secretas; estes materiais adaptam essas referências sem criar lore nem trocar nomes.

| Família | Mapas | Materiais |
|---|---:|---|
| Tree | 4 | Madeira envelhecida, tábuas largas com juntas alternadas, fibras discretas, folhagem verde fria |
| Shrub | 4 | Terra sombreada, raízes curtas embutidas, folhas esparsas, folhagem verde oliva |

O desenho não acrescenta obstáculos ao espaço decorável. Contornos, moitas, buracos, entrada e computador mantêm suas posições e funções.

## Implementação

Dois bancos secundários privados gTileset_AraunaSecret06C2Tree/Shrub. Cada um retém os 83 gráficos originais, acrescenta 65 gráficos de ambiente e completa 160 tiles. O material ocupa a paleta 12, sem referências no banco original. As 12 paletas anteriores e toda referência a gráficos primários permanecem intactas. Compressão LZ nativa, callback NULL.

Apenas oito campos secondary_tileset de layouts existentes e blocos aditivos em três headers mudam. Os 754 IDs e sua ordem permanecem iguais; não acrescenta layouts. Bancos primários e ponteiros usados pelo menu de decoração ficam intactos. O mesmo piso aparece sob os móveis e estados do PC.

Grids, bordas, map.json, colisão, elevação, scripts, eventos, progressão, treinador, 14 placeholders de decoração por mapa, catálogo, inventário, permissões, saves, link/record mixing e 75 entradas externas são preservados por hashes. Oito saídas continuam MAP_DYNAMIC / WARP_ID_SECRET_BASE. As 16 cavernas do 06C1 têm renders idênticos à base conciliada. Os 26 bancos retirados no GitHub continuam sem declarações.

## Verificação

validation.json: 22.920 dependências congeladas (18.490 de gameplay + 4.430 outras), 1.044 células, 648 atributos, 1.296 máscaras de camadas, 2.752 referências primárias, 24 arquivos de paleta e 166 gráficos originais preservados. Selector C real também confere as 53.167 células anteriores de cavernas/Dive.

Funções C reais e catálogo nativo: 250.560 decisões de posicionamento antes/depois para 120 decorações válidas, 600 escritas de decorações não sprite, 100 casos de PC/entrada/retorno e 128 casos das 16 posições salvas. Os grupos Tree/Shrub usam índices nativos 16–23, conservando sua relação com os IDs de bases externas. O harness usa serviços explícitos de grid, variáveis, saves, objetos, fades, tasks e callbacks; não executa o motor inteiro.

install_test.json registra testes do instalador real em checkout isolado: preflight, corrupção, edição local, base desconhecida, rollback, instalação, reaplicação, hashes e builder determinístico. CUMULATIVE_TEST.json no ZIP verifica duas importações reais independentes: GitHub com manutenção, e 06C1 sem manutenção; compara commits/árvore completa, hashes de checkout com paletas CRLF e patch aplicado.

As três montagens e oito pares de mapas são renders RGB555 nativos sem sprites/clima do motor, não capturas de emulador. Cenas decoradas usam CanPlaceDecoration e ShowDecorationOnMap; não são instaladas em grids nem saves.

Auditoria oficial de mapas 8/8 e static readiness oficial English PASS; os fontes foram restaurados e todos os hashes conferidos após a composição. Compilação ARM, revisão mGBA, sprites e record mixing em link pendentes. A preservação desses dados/código é verificada, sem alegar execução integral. Sem ROM, ELF ou save distribuído.

## Pacotes

- cumulative_06A_06B_06C1_06C2.bundle: histórico completo sobre o GitHub 872 e seu pai d665.
- cumulative_from_06C1_06C2.bundle: manutenção e 06C2 sobre o 06C1 recuperado 0098.
- checkpoint_SecretBases_06C2.bundle, changes.patch e source: somente o incremento 06C2 sobre a base conciliada 6cfba8c79b.

Não aplicar o incremento diretamente sobre main, d665, 872 ou 0098. Use o cumulativo correspondente. Manutenção adicional fica para a rodada do usuário.
