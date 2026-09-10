# Pampa da Espera V1 — direção e contrato

A referência de produção é o Master Map Design Bible, página 5: campos do Sul, ocupação baixa e horizontal, telha cerâmica, alvenaria clara, cercados, galpão cívico e praça do fundador. O pacote de cidades não contém uma vista externa dedicada de Pampa. A prancha `Casa_do_Pampa_Nabor.png` mostra um recinto aquático que diverge da própria legenda rural. Conforme a regra de autoridade da página 1, a descrição da Bíblia orienta o exterior. A comparação entregue explicita essa diferença; não afirma reproduzir uma concept externa ausente.

A cidade usa 38 × 30 metatiles. Mantém-se a altura de 30 para preservar as faixas das Rotas 102/104. O galpão ocupa o alto central; casa de Val e Centro ficam a leste; mercado e duas casas compõem a faixa inferior. A praça tem monumento e banco. O sino e o bebedouro identificam o setor cívico/rural. Há somente três árvores altas; arbustos baixos e cercados delimitam os acessos. Dois pequenos lagos mantêm as recompensas de Surf e a fala do menino sobre seu reflexo.

## Progressão

Elias é o responsável implementado no jogo. O nome Nabor da prancha antiga e a nova sequência de chancela da Bíblia não substituem a implementação atual. Este lote adapta o exterior de Pampa; seus interiores, a batalha de Elias, suas flags e recompensas permanecem como recebidos.

- Ginásio: porta (15,8), preservando os dois warps literais do script interno. Chegada do jogador (15,9), Val/pai em (15,10).
- Tutorial: cidade oito células mais larga; acrescentam-se oito passos para a direita às duas rotinas. Jogador e Val continuam terminando na Rota 102 em (5,5) e (6,5).
- Retorno com o pai: novo percurso acompanha a rua, passa pelo corredor em (21,10) e chega à casa em (26,7). Quatro blocos de movimento e duas constantes de coordenada são as únicas alterações no script da cidade.
- Guia do Ginásio e Seu Bento: oito gatilhos e quatro variantes de cada cena preservados. Os cercados não permitem evitar as cenas a pé. A saída de Bento atravessa os tiles reais da Rota 104.
- Max Revive, Ether e Rare Candy oculto mantêm os mesmos scripts/itens/flags e exigem Surf. A água usa `MB_POND_WATER`, elevação 1, com margens e ilhas na elevação 3.
- As sete colunas de ambas as bordas usam apenas o banco primário. As faixas recíprocas das rotas também usam esse banco, evitando troca visual de tiles no cache de conexão.

As portas customizadas são estáticas, com comportamento nativo de porta não animada. Os comandos de abrir/fechar da cena retornam sem criar animação nessas portas; sua espera não fica presa. Essa condição foi executada com as funções reais da engine em fixtures C locais.
