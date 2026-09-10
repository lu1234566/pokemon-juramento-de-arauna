# Casa da Maré — interior V1

O interior foi reconstruído em **22×16 metatiles**, com madeira de tons quentes, redes completas, fotografias, janelas voltadas ao mar, bancada de reparo, estantes, mesa coletiva e bancos. A entrada desemboca num salão compacto; a oficina fica à esquerda e a área de reunião ocupa o fundo. O antigo labirinto estreito de 18×28 foi substituído por ambientes conectados.

## Referência e alcance

A base visual são os painéis **Interior principal** e **Sala de história** da prancha enviada `Casa da Maré / Porto das Redes`, reproduzidos lado a lado em `review/mare_v1_concept_comparison.png`. A composição adapta materiais, mobiliário e usos à grade do GBA e aos oito NPCs existentes. Não é uma cópia pixel a pixel da ilustração.

O exterior de Porto das Redes V1 já encaminha a Casa da Maré para `DewfordTown_Gym`. Esta entrega continua esse vínculo e preserva **Ademar e a segunda insígnia**. A Bible descreve também Celina e cenas M05–M14; esses eventos não existem neste slot do código recebido. A arquitetura está implementada; essas cenas narrativas não estão implementadas por este pacote.

## Mudanças no jogo

São **26 arquivos do jogo**: três arquivos de mapa/eventos, um registro de layout, três registros de tileset e 19 arquivos do banco secundário `AraunaMare`. O banco usa 47 metatiles e 122 tiles gráficos estáticos de 8×8; fica abaixo do limite de 512 metatiles e da área de VRAM reservada às animações de porta. Os pixels copiados dos móveis nativos foram comparados com suas fontes, incluindo os espelhamentos horizontal e vertical.

As paletas dos bancos existentes permanecem intactas. Os móveis combinam peças completas do `GenericBuilding` com módulos locais de madeira, rede, bancada e objetos marítimos em pixels indexados. A mesma porta exterior e o tablado de Porto das Redes continuam em uso.

| Elemento | Posição local | Comportamento preservado |
| --- | --- | --- |
| Ademar | (12,4) | Insígnia, TM, revanche e Match Call |
| Takao | (4,12) | Olha ao norte, alcance 3 |
| Jocelyn | (18,4) | Olha ao sul, alcance 3 |
| Laura | (16,13) | Olha ao norte, alcance 2 |
| Guia | (8,13) | Orientação antes/depois da vitória |
| Cristian | (3,6) | Olha a leste, alcance 3 |
| Lilith | (17,9) | Olha ao sul, alcance 3 |
| Brenden | (5,9) | Olha a leste, alcance 2 |
| Saídas 0 e 1 | (10,15), (11,15) | Retornam ao warp 2 do tablado |
| Certificações | (11,2), (12,2), (9,12), (12,12) | Mesmos dois textos, quatro acessos |

Todas as posições usam a elevação 3 do piso. Os quatro acessos às certificações foram distribuídos entre a parede do fundo e a chegada; cada um pode ser lido de frente. O `scripts.inc` do ginásio permanece **byte-idêntico**. Nenhum personagem, diálogo, flag, item ou ID de treinador foi substituído.

## Iluminação

O desafio de iluminação continua ativo. Antes das vitórias, o raio é de 24 pixels; após seis treinadores, chega a 72 pixels; derrotar Ademar ilumina o ambiente todo. As imagens gerais mostram esse último estado para permitir revisão dos materiais e móveis.

`review/mare_v1_lighting.png` mostra as três condições com máscaras calculadas pelas funções reais de `src/field_screen_effect.c`, compiladas no ambiente local. São prévias estáticas, sem protagonista, no ponto caminhável (7,10). Não são capturas de emulador. Os frames e paletas dos NPCs usados nos outros PNGs vêm dos arquivos existentes do projeto; o sprite de Ademar conserva a textura da arte recebida.

## Verificação concluída

- 184 células de piso formam um único componente conectado; as interações e saídas continuam acessíveis com os oito NPCs presentes.
- Dois warps e quatro certificações têm posição, direção e elevação compatíveis.
- Os seis campos de visão completos estão livres. As 16 aproximações possíveis mantêm acesso às saídas e a Ademar.
- Os 64 conjuntos de treinadores derrotados foram executados no interpretador restrito dos comandos reais de iluminação, antes/depois do líder: 128 estados. Repetir uma interação não dispara iluminação extra.
- As funções C nativas de alcance e percurso passaram em 16 casos positivos e 12 negativos, com callbacks de colisão controlados. O registro do tileset foi compilado com macros gráficas controladas. Esses testes não substituem a execução do engine inteiro.
- O conversor nativo `mapjson` gerou os três arquivos de eventos/layout/cabeçalho. O verificador de tradução continua compatível com os 117 blocos de texto em dez mapas e dois menus.
- O ZIP é reproduzível após extração: construtor, validador, render, máscaras e conversor nativo. O aplicador preserva registros externos, é idempotente, aceita paletas CRLF e rejeita bancos divergentes antes de escrever.

Build completo da ROM e execução em emulador permanecem pendentes. Não houve push, merge ou uso de GitHub Actions.

## Integração e reprodução

Base local de revisão: **dc5f1c2**, após Porto das Redes V1. O pacote é um incremento para essa sequência. O patch `review/mare_v1_from_review_base.patch` contém somente os arquivos do jogo desta etapa. Para outra base, use primeiro a checagem do aplicador; ele deve detectar as dependências divergentes.

```bash
python3 tools/apply_mare_v1.py --target /caminho/do/projeto --check
python3 tools/apply_mare_v1.py --target /caminho/do/projeto
```

O aplicador altera somente os 26 arquivos listados por `GAME_FILES` e guarda a versão anterior. As outras fontes do ZIP servem à auditoria. Não copie o ZIP inteiro sobre o repositório.

```bash
python3 tools/build_mare_v1.py
python3 tools/validate_mare_v1.py
python3 tools/probe_mare_v1_native.py
python3 tools/build_mare_v1_review.py
python3 tools/check_mare_v1_package.py --archive /caminho/do/pacote.zip
```

Reprodução requer Python 3, Pillow, fonte DejaVu Sans, `cc`, `g++` e `make`. Os construtores antigos não precisam ser executados novamente.

Próxima etapa da sequência da Bible: **Casa da Terra**.
