# Casa da Terra V1

O interior foi reconstruído em **24×24 metatiles** seguindo a prancha enviada: uma passarela central atravessa dois espelhos d’água, chega a uma plataforma em T com bancos e relevo comunitário, e continua por escadas até o mural do fundo. Galerias de pedra acompanham a água; árvores inteiras delimitam as laterais. A entrada ocupa uma pequena área de barro ao sul.

## Referência e alcance

Referências: prancha **Casa da Terra — Bento**, no pacote de Casas da História, e página 33 da Master Map Design Bible. A comparação integral está em `review/terra_v1_concept_comparison.png`.

| Elemento da referência | Implementação no mapa |
| --- | --- |
| Ponte central e dois espelhos d’água | Passarela de madeira, corrimãos, água azul profunda, pedras e pequenas plantas |
| Plataforma em T e bancos laterais | Tablado elevado com dois bancos completos e relevo central |
| Escada ao fundo | Segundo lance de degraus, com passagem pelos dois lados do relevo |
| Vegetação envolvendo o recinto | Árvores nativas completas nas bordas e arbustos na chegada |
| Tijolos, mapa comunitário, mural-certidão | Pilha de tijolos a oeste, planta cadastral a leste e mural na parede norte |

A grade do GBA, o enquadramento jogável e os cinco personagens exigem uma adaptação das proporções da ilustração. A água é ornamental e bloqueada: o percurso não depende de Surf ou pesca antes da primeira insígnia. Tijolos, mapa e mural são elementos visuais nesta versão.

O código recebido não contém Baixios do Barro ou as cenas de Bento descritas na Bible. A arquitetura foi implantada em `RustboroCity_Gym`, o slot existente da primeira insígnia, preservando **Dalva**. As três disputas de lore, proteção do mural, cura anterior ao chefe e Chancela da Terra não foram implementadas. O pacote não troca o líder, textos, itens ou flags para simular essas cenas.

## Mudanças e eventos

São **26 arquivos do jogo**: três arquivos de mapa/eventos, um registro de layout, três registros de tileset e 19 arquivos do banco secundário `AraunaTerra`. O antigo corredor de 11×20 foi substituído pelo pátio de 24×24. O banco possui **54 metatiles e 138 tiles gráficos de 8×8**, abaixo da área reservada às animações de porta. A paleta azul é local; bancos e paletas existentes permanecem intactos.

As peças de vegetação e água copiadas do General conservam índices, quadrantes e espelhamentos, com remapeamento das paletas para o banco local. Pedra, madeira, corrimãos, bancos, mural, relevo e objetos da memória comunitária usam módulos indexados próprios. O banco primário continua sendo Building.

| Evento | Posição local | Elevação | Comportamento preservado |
| --- | --- | --- | --- |
| Dalva | (11,8) | 5 | Primeira insígnia, TM, revanche e Match Call |
| Josh | (11,16) | 3 | Olha ao sul; alcance 2 |
| Tommy | (9,9) | 5 | Olha a oeste; alcance 3 |
| Guia | (8,21) | 3 | Orientação antes/depois da vitória |
| Marc | (4,13) | 3 | Olha ao sul; alcance 3 |
| Saídas 0 e 1 | (11,23), (12,23) | 3 | Retornam ao warp 0 de RustboroCity |
| Certificações | (9,21), (14,21) | 3 | Mesmos dois textos, leitura de frente |

Os três pisos têm elevações **3, 5 e 7**; os dez tiles de degraus usam a transição nativa **0**. O jogador precisa passar pelas escadas para chegar aos patamares. O mural permanece alcançável pelos dois lados do relevo central.

O `scripts.inc` do ginásio e o script exterior permanecem byte-idênticos. A arte de Dalva — sprite de campo, paleta e retrato de batalha — e os quatro arquivos de registro de personagens permanecem byte-idênticos. Nenhum ID, flag, texto ou recompensa foi alterado.

## Integração com os exteriores existentes

A base local de revisão **b43fa45**, após Casa da Maré V1, ainda tem o exterior anterior de RustboroCity; o workspace cumulativo tem um redesenho exterior anterior a esta entrega. Os dois usam o mesmo warp lógico 0, em posições distintas:

| Exterior auditado | Porta de retorno | Resultado |
| --- | --- | --- |
| Base de revisão b43fa45 | (27,19) | Porta nativa, chegada livre em (27,20) e saída lateral |
| Workspace cumulativo | (16,27) | Porta nativa, chegada livre em (16,28) e continuação |

O interior retorna pelo ID do warp, sem coordenada externa absoluta. O aplicador reconhece os dados de eventos, terreno, borda e layout dessas duas versões e não modifica nenhum deles. Uma terceira versão divergente é recusada antes da escrita. A auditoria cobre a porta e a chegada das duas versões; não equivale a rever todo o exterior ou executar a perseguição em emulador.

## Verificação

- As 154 células caminháveis formam um componente conectado; as 149 livres continuam conectadas com os cinco NPCs presentes.
- As duas saídas, duas certificações, o mural e os cinco NPCs têm acesso compatível com posição, direção e elevação.
- Os três campos de visão estão livres. As oito aproximações possíveis preservam o acesso ao líder e às saídas.
- As funções C reais de alcance, percurso e elevação passaram em oito aproximações positivas, seis casos negativos de alcance e seis percursos de escada. As regras nativas também alcançaram as mesmas 149 células livres e rejeitaram saltos diretos entre níveis.
- O teste C usa callbacks de colisão e macros gráficas controlados; não executa o engine inteiro.
- O conversor nativo `mapjson` gerou os três arquivos `.inc`. A verificação de tradução passou nos 153 blocos de texto de 15 arquivos.
- Seis recortes de **240×160** cobrem o mapa inteiro. As imagens usam os metatiles e frames existentes do projeto; são prévias estáticas, sem protagonista, e não capturas de emulador.
- O teste do ZIP reconstrói os arquivos do jogo, reproduz todas as imagens, executa o teste C e recompila os eventos após extração. Confere aplicação restrita, preservação de registros alheios, idempotência e paletas CRLF; também verifica a recusa de alterações desconhecidas no exterior, em Dalva ou no banco local antes de escrever.

Build completo da ROM e execução em emulador permanecem pendentes. Não houve push, merge ou GitHub Actions.

## Aplicação e reprodução

Use o aplicador, que altera somente os 26 arquivos do jogo e guarda os anteriores. As demais fontes no ZIP são dependências de auditoria; não copie o pacote inteiro por cima do projeto.

```bash
python3 tools/apply_terra_v1.py --target /caminho/do/projeto --check
python3 tools/apply_terra_v1.py --target /caminho/do/projeto
```

O patch `review/terra_v1_from_review_base.patch` corresponde somente ao incremento sobre b43fa45. O recibo `review/terra_v1_integration.json` identifica o commit local e os arquivos exatos.

```bash
python3 tools/build_terra_v1.py
python3 tools/validate_terra_v1.py
python3 tools/probe_terra_v1_native.py
python3 tools/build_terra_v1_review.py
python3 tools/check_terra_v1_package.py --archive /caminho/do/pacote.zip
```

Reprodução requer Python 3, Pillow, DejaVu Sans, `cc`, `g++` e `make`. Não é necessário executar os construtores de etapas anteriores.

Próxima etapa da sequência da Bible: **Primeira Câmara**.
