# Integração do checkpoint 07F (Battle Pyramid)

O bundle `fd298f4467` entrou por fast-forward sobre `9a3f9464ea`. Nenhuma
correção foi necessária.

Conferência:

- **Pacote.** O ZIP bate com o SHA-256 do relatório e os 84 arquivos do
  manifesto batem com o checkout.
- **Layouts.** São 754, com IDs e ordem iguais. Saguão, andar e topo trocam
  só os bancos. Os 16 módulos (`LAYOUT_BATTLE_PYRAMID_SQUARE01`–`16`)
  mantêm as referências do editor; no jogo, são desenhados com o banco do
  andar.
- **Build e gates.** A ROM compila e todos os gates passam.
- **Tiles.** Nos layouts do Frontier e nos 16 módulos desenhados com o banco
  do andar, nenhum metatile perdeu tiles animados nem desenha tile ausente.
- **Código.** A paleta do andar continua vindo de `gBattlePyramidFloor_Pal`
  para o slot 6, que é o que a arte nova do andar usa.
- **mGBA.** Fotografados o saguão, o topo e um andar gerado pelo motor. O
  andar aparece escuro, com o círculo de luz nativo e a paleta do primeiro
  andar. O topo e o andar foram fotografados assim que o mapa carrega: os
  toques de A e START da inicialização abriam o resumo de Pokémon nesses
  mapas.
