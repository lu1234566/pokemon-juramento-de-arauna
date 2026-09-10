# Liga V2 — implementação guiada pelos concepts

Referências recebidas em 06/09/2026: os seis pacotes de concepts e a Master Map Design Bible. A Bíblia prevalece sobre nomes antigos nas imagens. Scripts, flags, progressão e destinos dos warps continuam sendo autoridade funcional.

## Correção solicitada

A V1 não reproduzia os elementos dominantes do concept da Liga. A V2 deve incorporar fachada monumental de pedra, vidro azul, molduras douradas, brasão, escadarias centrais em patamares, ponte de madeira na aproximação e quedas d'água laterais entre paredões arborizados. A imagem fornecida orienta a composição; o resultado entregue continuará sendo render do map.bin real.

## Blueprint antes da implementação

- Função: chegada solene ao Caminho das Quatro Vozes. A referência dos interiores será preservada para a etapa interna; esta revisão altera o exterior.
- Bioma: serra úmida com água, mata nas cristas e costa no acesso inferior.
- Arquitetura: edifício completo com pedra clara, painéis azuis, contrafortes e portal central. Centro Pokémon como abrigo lateral discreto.
- Silhueta: platô central suspenso entre dois corredores de água; as bordas naturais permanecem assimétricas. Fachada e escadaria estabelecem o eixo cerimonial após a caverna.
- Fluxo inferior: Rota 128 → cachoeira funcional → desembarque → trilha da mata/abrigo → entrada inferior da caverna.
- Fluxo superior: saída da caverna → trilha de aproximação → ponte de madeira → escadaria → patamar → segunda escadaria → hall da Liga.
- Landmarks: pedra/azul/dourado da fachada, brasão, cachoeiras laterais e escadaria larga, conforme os três concepts locais.
- Entrada: mar e rocha primeiro; abrigo depois da cachoeira; complexo monumental revelado após a travessia interna.
- Geometria proposta: 44×64; connection da Rota 128 migra de offset 40 para 24, com retorno -24. A costura compartilhada mantém os mesmos metatiles.
- Eventos: quatro warps com mesmos índices/destinos, onze gatilhos de visita na água, cinco placas e dois pontos de Fly. Preservar Waterfall e a ligação obrigatória pela caverna.
- Assets: acrescentar metatiles ao tileset exclusivo de Ever Grande; manter orçamento de 512 tiles secundários e 16 cores por paleta. Preservar slots de animação e formato da porta nativa.

## Critérios visuais

Comparar o render com os concepts, não apenas com Emerald. Conferir fachada de pedra e vidro azul, escadaria com continuidade real, patamares proporcionais, cachoeiras enquadrando a Liga, ponte antes do complexo e mata nas encostas. Não reutilizar a fachada laranja nem apresentar um concept como resultado jogável.
