# Casa da Maré V1 — interior guiado pela prancha

Referência: `review/mare_v1_concepts/Casa_da_Mare.png`, painéis “Interior principal” e “Sala de história”; Master Map Design Bible, página 42. A proposta usa piso e paredes de madeira, redes penduradas, fotografias, mesa de reparo e um espaço de reunião.

## Implantação antes da construção

- Sala inicialmente dimensionada em 22×18 e refinada para 22×16 após os viewports, mais larga e menos profunda que o labirinto de 18×28 do Emerald. A redução elimina o excesso de piso junto à chegada.
- Entrada ao sul, entre dois painéis de certificação; guia ao lado da chegada.
- Oficina de redes à esquerda, com bancada e materiais; mesa coletiva no centro.
- Área de reunião ao norte, com Ademar, bancos e imagens nas paredes. Divisórias baixas sugerem os ambientes da prancha mantendo a circulação entre eles.
- Estantes, janelas e objetos marítimos nas bordas. A composição deve continuar legível em 240×160.
- Banco secundário próprio, `AraunaMare`, usando peças inteiras dos interiores nativos e elementos de rede em pixels indexados. Nenhum banco global será recolorido.

## Compatibilidade funcional

O exterior entregue de Porto das Redes já vincula a Casa da Maré ao slot `DewfordTown_Gym`. Esta etapa continua essa integração. Mantém Ademar, seis treinadores, guia, dois warps de saída e quatro acessos aos textos de certificação. Os IDs, direções, alcances, flags, batalhas, revanche, insígnia, TM e textos não serão alterados. Só as posições e elevações migram para o piso contínuo.

A iluminação progressiva é mecânica existente: o salão começa com raio de visão de 24 pixels, cresce após as seis vitórias e fica totalmente visível após Ademar. O desenho claro para revisão representa o estado iluminado; o pacote também mostrará o estado inicial. Não será apresentado como uma sala sempre iluminada.

A Bible descreve cenas M05–M14 de Celina; elas não existem neste slot do código recebido. A referência orienta o espaço e os materiais. Esta entrega não criará essas cenas nem afirmará implementá-las. A conciliação narrativa é uma lacuna anterior à reconstrução visual.

## Verificação prevista

Conectividade com todos os NPCs presentes, quatro painéis alcançáveis, saídas compatíveis com o tablado externo, aproximações dos seis treinadores livres, scripts byte-idênticos e compatibilidade do banco com os limites nativos. Conferir os estados de iluminação pelo roteiro e a máscara pelo código C do engine. Gerar mapa real, eventos, comparação e recortes 240×160; compilar o JSON com o conversor nativo. Build da ROM e teste em emulador permanecem pendentes.
