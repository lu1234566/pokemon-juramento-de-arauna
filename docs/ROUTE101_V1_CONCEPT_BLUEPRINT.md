# Rota 101 V1 — blueprint pelos concepts

Referências: concept conjunto `Rotas 101–103 — Sul de Arauna` e página 12 da Master Map Design Bible. No conjunto, a 101 representa a trilha estreita, a 102 as pequenas propriedades e a 103 a água e o horizonte. A 101 usa a mata leve, o capim úmido, o solo ocre avermelhado e as cercas curtas.

- Dimensões propostas: 40×28 metatiles, conforme a Bible.
- Fluxo: saída de Vila Amanhecer → pequena clareira do resgate → trilha em curva para leste entre moitas de capim → retorno para noroeste → Vila da Passagem.
- Silhueta: clareira baixa, meandros na trilha, pequenos bosques no interior e dois bolsões laterais de capim. As árvores formam grupos completos, sem corredor reto contínuo.
- Landmarks: clareira de Anahí, cerca curta na borda do campo, placa junto à trilha e capim onde os Pokémon locais podem ser vistos.
- Conexões: norte em x=8..11, sul em x=10/11, ambas com offset 0. Conservar o acesso aos gatilhos e ao rival no sul de Vila da Passagem.
- Cena: deslocar o palco do resgate para a clareira ao sul e manter a perseguição nativa. A entrada inicia a cena; durante o resgate, duas células bloqueiam a volta para a vila, quatro guardam o pequeno desvio oeste e uma guarda a passagem norte. A bolsa permanece acessível.
- Estados: preservar as flags, VAR_ROUTE101_STATE, ChooseStarter, cura, distinção dos protagonistas e warp para o interior do laboratório. Migrar somente posições e o olhar do jogador para a nova posição da perseguição.
- Encontros: preservar espécies internas, níveis, taxas e mapeamento dos dois Pokémon visíveis. O capim deve usar o comportamento nativo de encontro e ser alcançável depois do resgate.
- Tileset: reutilizar o banco exclusivo de Amanhecer. Acrescentar quatro clones de metatiles nativos de capim, arbusto e samambaias em índices reservados, sem alterar os pixels, paletas ou metatiles usados pela vila.
- Transição norte: Vila da Passagem também deve carregar esse banco para exibir a rota antes da troca de mapa. Uma comparação exaustiva já confirmou que o banco conserva todos os metatiles usados por Oldale, Route102 e Route103.
- Evidência: mapa real, comparativo com o concept, recortes 240×160, vista das duas conexões, simulação da perseguição e das barreiras, conversão nativa de eventos e pacote reproduzível. A ROM e o emulador continuam pendentes neste ambiente.

Inventário recebido: 8 objetos, 9 gatilhos, 1 placa, nenhuma porta/warp no exterior e 12 slots de encontros terrestres com níveis 2–3.
