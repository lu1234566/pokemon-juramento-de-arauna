# Navel Rock 06B — direção visual

Referências recuperadas antes da edição: `docs/referencias/bible_concepts_recuperados/Arauna_Master_Map_Design_Bible.pdf`, páginas 20–22 (arquipélago e oceano profundo) e 29 (Gruta da Maré), e os concepts `13_Rotas_124-126_Arquipelago.png`, `14_Rotas_127-131_Oceano_Profundo.png`, `07_Gruta_da_Mare_Alta.png` e `08_Gruta_da_Mare_Baixa.png`. O pacote recuperado tem SHA-256 `ecf381db95864a61e191a9fcf2525e3f892a1dd934e5aaca7c43344f5e6e19e3`. Não foi encontrada prancha específica de Navel Rock: esta adaptação complementa a Bible, sem introduzir nome, história, quest ou encontro novo.

O local é uma rocha isolada no mar, com um percurso vertical que se divide entre um cume aberto e um santuário profundo. O contraste visual ajuda a reconhecer a direção da viagem, mantendo as plantas e o ritmo originais.

| Trecho | Materiais e cor | Leitura no jogo |
|---|---|---|
| Exterior e porto | Rocha cinza esverdeada, marcas claras de sal, água azul e madeira castanha | Chegada marítima e ligação entre barco, ponte e boca da gruta |
| Entrada, B1F e bifurcação | Pedra neutra, fissuras discretas e bordas elevadas | Corredor longo legível e bifurcação reconhecível |
| Up1–2 | Pedra quente, com areia mineral nas luzes | Início da subida |
| Up3–4 e topo | Tons de calcário dourado, sombras ocres e céu aberto | Cume exposto ao sol; recinto de Ho-Oh |
| Down01–04 | Pedra cinza azulada | Primeira transição para profundidade |
| Down05–08 | Ardósia mais fria | Continuidade da descida |
| Down09–11 e fundo | Rocha azul escura, veios claros e luz fria | Santuário profundo de Lugia |

As fissuras permanecem no piso transitável. Os rodapés bloqueados têm aspecto de borda elevada, e escadas conservam suas silhuetas e contraste. O número, posição e comportamento dos metatiles continuam originais. Nenhum adereço do concept foi colocado como obstáculo novo.

`review/navel_06b/concept/NavelRock_06B_Direcao.png` é um estudo gerado de materiais, acompanhado do prompt exato em `prompt.txt`. Ele não representa a geometria instalada nem uma captura do jogo. A produção usa gráficos nativos indexados, transparência de camada preservada, 4bpp e paletas RGB555.

As montagens `NavelRock_06B_Locais_Chave.png`, `NavelRock_06B_Subida_e_Descida.png` e `NavelRock_06B_Cameras.png` mostram os dados efetivamente escritos. Não incluem sprites, enquadramento dinâmico ou clima do motor. As prévias pequenas são recortes de 240×160; as salas menores recebem margem preta, sem simular a borda do runtime.

Não foi adicionada névoa. Todos os climas e os comandos de clima dos scripts permanecem iguais à base cumulativa, incluindo as alterações já integradas nas cavernas anteriores.
