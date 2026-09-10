# Pampa da Espera — interiores V1

Continuação do exterior `55fd170`. Escopo: os sete mapas internos de Pampa, que contêm quinze salas visíveis. A cidade fica com seu primeiro lote espacial completo nesta rodada de adaptação pelas referências.

## Direção de arte e autoridade

O Master Map Design Bible, página 34, descreve a Casa do Pampa com madeira de galpão, sino, arquivo, livro, lenço, depósito e salão cívico. A imagem antiga `Casa_do_Pampa_Nabor.png` apresenta uma arena aquática; esse conflito já foi registrado no exterior. A regra da página 1 da Bíblia orienta usar sua descrição para a direção rural. Não se afirma copiar a geometria dessa arena.

`Centro_Comunitario.png` orienta madeira, balcão, mesa redonda e plantas no Centro. `Casa_de_Ciro.png` orienta apenas os materiais e módulos domésticos. Nenhuma delas é apresentada como uma concept específica da casa de Val. O painel de referência explicita os empréstimos.

Elias é o líder implementado; Dalva mantém seus assets. Nabor, a segunda Chancela e a sequência de três confrontos da legenda antiga não substituem a história atual. Este lote não implementa a nova sequência narrativa da Bíblia.

## Ambientes

| Mapa | Direção e elementos | Contrato funcional |
|---|---|---|
| Ginásio / Casa do Pampa | Recepção com registros; sete pequenas salas de equipamento, arquivo, tecidos e repouso; salão de Elias com estrado e passadeira | Nove salas nas coordenadas da engine; sete treinadores e todas as portas mantidos |
| Casa 1 | Cozinha, mesa de mate, tecido verde e estante | Morador desce de (7,4) para (7,5); mesma área de caminhada 2 × 2 |
| Casa 2 | Livros, cama estreita, mesa de estudo e quadro de campo | Moradora passa de (2,5) para (3,5); mesma área de caminhada 1 × 1 |
| Casa de Val | Cozinha familiar, arquivo, mesa e plantas | Pais, TV, chegada do pai e entrega de Surf preservados |
| Venda | Balcão de madeira e prateleiras de mercadorias | Compra, questionário, estoques e NPCs existentes |
| Centro 1F | Livros, mapa da região, mesa redonda e tapete | Enfermeira, aparelho de cura, PC e escada nas âncoras nativas |
| Centro 2F | Atendimento comunitário, registros e tecido verde | PCs, portas, barreiras e escada preservados |

## Implementação nativa

Sete layouts privados são acrescentados à tabela, sem deslocar os 452 IDs existentes. Quatro bancos secundários exclusivos recebem os gráficos 4bpp. A paleta 12 contém a nova madeira/tecido; os demais slots nativos permanecem intactos. Nenhum layout compartilhado de outras cidades é redesenhado.

Colisão, elevação e atributos de comportamento seguem a referência recebida, com uma exceção declarada: 48 células de mobiliário real nas bordas das sete salas de treino agora bloqueiam movimento. As áreas inteiras do tutorial e do encontro final permanecem fisicamente equivalentes. As duas mudanças de posição de moradores evitam que seus retângulos de movimento atinjam móveis, inclusive conflitos que já existiam na geometria recebida.

As portas deslizantes conservam IDs 0x218–0x21c e 0x220–0x224. O último quadro inferior é uma interação `MB_PETALBURG_GYM_DOOR`, ainda bloqueada por colisão: a travessia ocorre por `warpdoor`. A célula de chegada abaixo de cada porta fica livre. As escadas mantêm todos os quadros nativos; o PC usa os IDs primários 4/5; as barreiras de comunicação mantêm os quatro IDs alterados pelo script.
