# Porto das Redes V1 — revisão pelo concept da Casa da Maré

O exterior de Porto das Redes foi reconstruído em 32×26 metatiles. A Casa da Maré ocupa um tablado sobre a água, com redes, postes de amarração e passarelas. Três casas menores de madeira e telha, o Center e pequenas áreas de vegetação formam o núcleo junto à praia. A arquitetura maior deriva dos painéis da casa já aprovada em Amanhecer, adaptados ao edifício comunitário.

## Referência e escopo visual

Foi usada a prancha dedicada **Casa da Maré / Porto das Redes**, particularmente seu exterior. A implantação da vila segue a Master Map Design Bible, página 6, e a referência regional **Arco Costeiro 105–109**. O conjunto enviado não contém uma vista geral dedicada da cidade. A legenda interna da prancha traz nomes/localização divergentes do título; nesta etapa, ela orienta a arquitetura e os materiais. Personagens, textos e progressão existentes foram preservados.

O comparativo está em `review/redes_v1_concept_comparison.png`. A implementação é uma adaptação na grade real do GBA: casa de madeira, redes, tablado, água em volta e núcleo pesqueiro. Não é uma reprodução pixel a pixel da ilustração. O warp do ginásio ocupa a Casa da Maré; seu interior é a próxima etapa da sequência.

`redes_v1_after.png` mostra o terreno. `redes_v1_boat_present.png` acrescenta uma prévia estática do sprite original do barco na coordenada do evento. Não é uma captura de emulador e não representa todos os estados/sprites do mapa. Há seis viewports de 240×160, dois recortes de conexão no mesmo tamanho, mapa de eventos e comparação com o estado anterior.

As rotas vizinhas conservam o terreno anterior, inclusive seus problemas visuais preexistentes. Esta entrega refaz a cidade e mantém os corredores das viagens; não apresenta uma reconstrução completa das Rotas 104–109.

## Migração

| Elemento | Posição final |
|---|---|
| Hall — warp 0 | (7,7) |
| Center — warp 1 | (3,14); Fly em (3,15) |
| Casa da Maré / Ginásio — warp 2 | (24,19) |
| Casa 1 — warp 3 | (14,16) |
| Casa 2 — warp 4 | (6,23) |
| Barco | (24,8), elevação aquática |
| Barqueiro | (24,9) |
| Pescador | (13,21), passeio horizontal livre |
| Moradora | (9,17), passeio horizontal livre |
| Menino da frase | (6,8) |
| Rota 106 | Conexão norte −48; retorno +48 |
| Rota 107 | Conexão leste, offset 0 |

A cidade cresce 12 colunas para oeste e seis linhas para sul. Sua origem global passa de (60,180) para (48,180); o barco continua em (72,188), e a borda leste continua em x=80. Por isso os longos movimentos marítimos mantêm seus caminhos e destinos globais.

As colocações locais do barqueiro em Route104/Route109 foram deslocadas de (12,8) para (24,8). O embarque passa a aceitar conversa a oeste, leste ou sul, os três lados acessíveis do novo cais. O barco ocupa o lado norte. As duas chegadas deixam o jogador em (23,10) e o barqueiro em (24,9), sem sobreposição.

Foram mantidos os 5 warps, 5 objetos e 5 eventos de placa. Não existem gatilhos por coordenada no exterior. Pesca, vara, frase da moda, itens, flags, retornos de interiores e textos permanecem preservados.

## Assets nativos

Foi criado o banco isolado `AraunaRedes`, selecionado por DewfordTown, Route106 e Route107. Os 379 metatiles nativos de Dewford são preservados, assim como seus pixels usados e suas animações. O banco final tem 489/512 metatiles e acrescenta 133 tiles de hardware. As posições da bandeira nativa e a faixa reservada às portas não são ocupadas pelos novos gráficos.

As paletas 6 e 11, não usadas pelas peças nativas de Dewford, atendem às construções e à madeira. As demais paletas não mudam. A porta 0x380 reutiliza a animação já aprovada de Amanhecer V8, na paleta 6. Imagens indexadas, metatiles, atributos, colisões e registros C fazem parte da entrega; não há mudança no motor de eventos ou no código da porta.

## Verificação

- 295 células terrestres conectadas; portas e seus acessos, placas, Fly e áreas de movimento dos NPCs livres.
- Fachadas e módulos de vegetação íntegros; limites externos fechados onde não há conexão.
- Cinco variantes marítimas verificadas no sistema de coordenadas das sete áreas conectadas: duas partidas, chegada da Rota 104 normal, chegada com a ligação do pai e chegada da Rota 109.
- Três abordagens para embarcar e os trajetos de desembarque validados.
- Quatro cópias nativas de conexão executadas com as funções C reais do motor: 839 células e buffers preservados.
- Registro C, callback de Dewford e consulta da porta executados no compilador local com macros controladas para os assets.
- Conversão `mapjson` de cinco mapas; renderer inglês compatível com 117 blocos, dez mapas e dois menus.
- Banco original e dados das rotas preservados; reprodução determinística das fontes e imagens; teste do ZIP após extração.

Os recibos JSON e logs ficam em `review/redes_v1_*`. As verificações são de arquivos, terreno, coordenadas e trechos nativos executáveis no ambiente. O build completo da ROM e a execução no emulador permanecem pendentes: faltam o compilador ARM e a cadeia completa de conversão gráfica. A temporização e a apresentação das viagens ainda precisam dessa conferência no jogo.

## Aplicação

Pré-requisito gráfico: Amanhecer V8 com sua porta animada registrada. O patch de revisão parte do commit `9987ae434c91b3c4d37c34d80b6aa80117a046d0`, após Vila da Passagem V1, seguindo a cadeia já entregue. Não houve merge, push ou GitHub Actions.

```sh
python3 tools/apply_redes_v1.py --target /caminho/do/projeto --check
python3 tools/apply_redes_v1.py --target /caminho/do/projeto
```

São 31 arquivos do jogo: sete arquivos de mapas/scripts, dois JSON compartilhados, três registros de tilesets e 19 arquivos do novo banco. O aplicador guarda os arquivos anteriores, altera apenas os registros de layouts/Fly envolvidos, acrescenta os registros do banco e preserva declarações externas compatíveis. Confere dependências e recusa conflitos antes de escrever. Paletas com LF ou CRLF são aceitas sem mudar suas cores.

Não copie todo o ZIP sobre o projeto. As fontes adicionais são dependências e snapshots para reprodução. Os builders reconstroem a pasta de revisão a partir do snapshot; o aplicador é a entrada adequada para integrar a mudança.

```sh
python3 tools/check_redes_v1_package.py --archive /caminho/do/pacote.zip
```

A próxima etapa é o **interior da Casa da Maré**, conforme a sequência da Bible, página 50.
