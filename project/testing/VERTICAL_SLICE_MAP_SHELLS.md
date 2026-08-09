# Roteiro de teste — shells do vertical slice

Este roteiro valida navegação, colisões, independência dos seis mapas e o reset
visual da Vila das Araucárias para os tilesets originais `General + Petalburg`.
Escolha dos iniciais, encontros e história final ainda não fazem parte desta etapa.

## Preparação

1. Compile a build portuguesa a partir do commit da tarefa.
2. Inicie um save compatível e use o acesso técnico próximo ao centro de
   Littleroot para entrar em `AraunaMapLab`.
3. Mantenha Porymap aberto no grupo `gMapGroup_AraunaPrototype` para conferir os
   mapas e layouts.

## Percurso

| Origem | Ponto provisório | Destino | Retorno esperado |
|---|---|---|---|
| Vila | caminho abaixo da casa noroeste | Casa do Protagonista | porta inferior retorna à vila |
| Vila | soleira sul do centro de pesquisa | Centro de Pesquisa | porta inferior retorna à soleira |
| Vila | estrada aberta na borda leste | Rota da Neblina | saída sul retorna à estrada |
| Rota da Neblina | saída norte | Ruína do Primeiro Elo | entrada sul retorna à rota |
| Ruína do Primeiro Elo | escada superior | Câmara do Primeiro Elo | saída inferior retorna à ruína |

## Verificações manuais

- [ ] Os seis mapas aparecem no grupo de Arauna no Porymap.
- [ ] Cada mapa aponta para um layout com nome e arquivos próprios.
- [ ] A vila usa `gTileset_General` + `gTileset_Petalburg`, sem depender do tileset autoral.
- [ ] Casa e centro não preservam NPCs ou eventos dos mapas usados como base.
- [ ] Rota, ruína e câmara não preservam itens, treinadores ou scripts de Hoenn.
- [ ] Toda entrada coloca o jogador em uma célula transitável.
- [ ] Toda saída possui caminho de volta.
- [ ] Casa e centro usam portas animadas originais do Emerald.
- [ ] A estrada leste aciona a transição somente na borda do mapa.
- [ ] O acesso técnico de Littleroot continua entrando na vila.
- [ ] A pesquisadora, Nilo e o item técnico da vila continuam funcionando.
- [ ] O percurso completo pode ser feito sem menu de debug.
- [ ] Salvar e recarregar em cada mapa não prende o jogador.
- [ ] O mesmo percurso funciona na build inglesa.

## Independência dos layouts

No Porymap, faça uma alteração visual temporária em um único mapa, confirme que
nenhum outro layout muda e descarte a alteração. Os arquivos esperados são:

- `data/layouts/AraunaMapLab/`;
- `data/layouts/AraunaPlayerHouse/`;
- `data/layouts/AraunaResearchCenter/`;
- `data/layouts/AraunaMistRoute/`;
- `data/layouts/AraunaFirstLinkRuin/`;
- `data/layouts/AraunaFirstLinkChamber/`.

Registre qualquer warp sem retorno, célula sólida ou alteração compartilhada na
issue M3.2.
