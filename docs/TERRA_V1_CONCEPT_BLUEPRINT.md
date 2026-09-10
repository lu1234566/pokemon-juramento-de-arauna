# Casa da Terra V1 — blueprint antes da construção

Referência visual: prancha `Casa da Terra — Bento`, do pacote Casas da História. Referência textual: Master Map Design Bible, página 33. A imagem mostra uma ponte central de madeira entre dois espelhos d'água, bordas de pedra, vegetação alta e uma plataforma com elementos de memória comunitária. Essa composição é a prioridade visual desta etapa.

## Implantação

- Pátio coberto/jardim interno de 24×24 metatiles. Entrada ao sul e quatro colunas de passarela no eixo central.
- Dois espelhos d'água ornamentais, com vegetação e rochas. Circulação de pedra pelas margens e ponte de madeira no meio.
- Plataforma de encontro em madeira e pedra, acima da água, com bancos laterais; líder diante do eixo do mural.
- Pequeno patamar ao norte com mural comunitário, alcançável por escada. As escadas ligam pisos distintos de verdade: chegada/ponte 3, plataforma 5, mural 7, degraus de transição 0.
- Marcas em tijolos junto à chegada e planta cadastral na margem direita traduzem os objetos descritos na Bible. São elementos visuais nesta entrega.
- Árvores em módulos nativos inteiros delimitam as laterais e o fundo, mantendo a sensação de recinto verde da prancha.
- Banco secundário isolado `AraunaTerra`: vegetação e água nativas copiadas do General, com índices gráficos e paletas remapeados; módulos de pedra, tijolo e madeira na grade real do GBA. Primary Building e o banco antigo permanecem intactos.

## Contrato funcional

O código recebido não possui Baixios do Barro nem um mapa específico da Casa da Terra. A primeira insígnia está em `RustboroCity_Gym`, com Dalva. Esta etapa adapta a arquitetura do concept a esse slot; mantém Dalva, Josh, Tommy, Marc, guia, as duas saídas e as duas certificações. Preserva também a arte e o registro da Dalva já integrados. Não cria um segundo líder ou uma nova insígnia.

O retorno continua no warp 0 de RustboroCity, sem deslocar o gatilho externo da perseguição que começa após a primeira insígnia. Textos, flags, TM, Match Call e revanche permanecem byte-idênticos. As posições e elevações dos eventos podem mudar.

Os espelhos d'água são decoração bloqueada, sem Surf ou pesca. O jogador alcança todos os personagens pela circulação a pé antes da primeira insígnia.

A sequência narrativa da Bible — Bento, três confrontos de lore, proteção do mural, cura antes do chefe e Chancela da Terra — não existe no slot recebido. O cenário materializa a referência; esta entrega não afirma implementar essas cenas nem troca a progressão de Dalva.

## Verificação

Auditar saídas, alcance de todos os eventos, campos de visão e aproximações de três treinadores, transições 3↔0↔5↔0↔7, acessos ao mural e integridade dos módulos. Comparar pixels nativos após cópia e espelhamento, compilar eventos com mapjson e verificar compatibilidade da tradução. O pacote deve reproduzir mapa, renders e quatro ou mais recortes 240×160 a partir das fontes. Build completo e emulador permanecem pendentes.
