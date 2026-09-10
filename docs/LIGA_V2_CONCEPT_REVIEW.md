# Chegada à Liga V2 — revisão pelos concepts

O exterior da Liga foi reconstruído a partir dos concepts enviados em 6 de setembro de 2026. Esta entrega implementa o prédio de pedra e vidro azul, o brasão dourado, a escadaria em patamares, a ponte de madeira e as quedas laterais. O arquivo real passa de 40×80 para 44×64 metatiles.

## Fidelidade e adaptações

| Referência visual | Implementação no jogo |
| --- | --- |
| Fachada monumental de pedra, painéis azuis e emblema | Fachada completa de 13×10 metatiles, com cores de pedra, vidro e dourado |
| Portal no centro do conjunto | Warp nativo e três quadros novos de animação da porta |
| Escadaria cerimonial em níveis | Dois lances de quatro tiles de largura, patamar intermediário e pátio superior |
| Ponte de madeira na aproximação | Passarela elevada entre a saída da caverna e a primeira escadaria |
| Água ladeando o complexo | Quedas em três corredores laterais; espelhos d'água no pátio |
| Mata nas encostas | Grupos de árvores nas cristas e na aproximação; abrigo inferior na mata |

A ilustração foi adaptada à projeção e à escala do GBA: o desenho usa pixels e paletas nativas, com degraus de terreno compatíveis com o motor. O volume ilustrado e a iluminação atmosférica do concept não são reproduzidos literalmente. O render mostra terreno estático; jogador, neblina e água animada dependem da execução do jogo. Os interiores do Caminho das Quatro Vozes continuam sendo uma etapa própria.

Referências incluídas em `review/liga_v2_concepts`: Liga exterior, Caminho das Quatro Vozes, Estrada do Juramento e as páginas pertinentes da Design Bible. O plano anterior à edição está em `docs/LIGA_V2_CONCEPT_BLUEPRINT.md`.

## Progressão preservada

O acesso continua sendo Rota 128 → Waterfall → abrigo → entrada inferior da caverna. O setor alto é alcançado pela saída da caverna → ponte → escadarias → Liga. Nenhuma cachoeira lateral permite evitar essa travessia.

| Sistema | V1 | V2 |
| --- | --- | --- |
| Warp 0: Liga | 27, 5 | 22, 13 |
| Warp 1: Centro Pokémon | 7, 47 | 8, 40 |
| Warp 2: caverna inferior | 25, 39 | 32, 36 |
| Warp 3: caverna superior | 5, 22 | 7, 30 |
| Fly/respawn: abrigo | 7, 48 | 8, 41 |
| Fly/respawn: Liga | 27, 6 | 22, 14 |
| Gatilhos de visita | x=6…16, y=57 | x=16…26, y=47 |
| Conexão oeste com Rota 128 | offset 40 | offset 24 |
| Retorno da Rota 128 | offset -40 | offset -24 |

Os índices e destinos dos quatro warps, onze gatilhos, cinco placas e dois pontos de Fly foram conservados. Os scripts externos e os três interiores envolvidos permanecem byte-idênticos. O marco da Liga e suas verificações de insígnias continuam nos scripts existentes. A costura compartilhada com a Rota 128 mantém os metatiles originais na nova posição.

## Verificação

- Validador: PASS. Portas, retornos, placas, Fly, costura da rota, módulos inteiros, elevações e acessibilidade conferidos. 144 células terrestres alcançáveis no setor inferior e 285 no superior.
- Progressão: Waterfall obrigatório, linha de visita inevitável na chegada e setores exteriores separados mesmo com Surf e Waterfall habilitados no modelo de alcance.
- Motor: 6.086 movimentos adjacentes conferidos em funções C extraídas do código para elevação, desembarque de Surf e as quatro combinações de insígnia/direção de Waterfall. Serviços de estado controlados no host; não é execução da ROM.
- Eventos: o `mapjson` nativo gerou os arquivos de eventos e conexões de EverGrandeCity e Route128. Saídas em `review/liga_v2_compile/`.
- Gráficos: 210 tiles estáticos novos; 326 de 512 metatiles secundários; duas paletas de 16 cores quantizadas para GBA. Slots nativos, animação das flores e área reservada à porta preservados. O tileset geral não foi alterado.
- Revisão visual: comparativo com os concepts, comparativo com o PNG original da V1 e quatro recortes de terreno em 240×160. A imagem anterior usa suas cores originais.
- Pacote em pasta limpa: hashes conferidos, 61 arquivos de jogo/assets/imagens reproduzidos sem diferenças, validador e teste C aprovados. O `mapjson` foi recompilado e suas saídas reproduzidas. O instalador também foi aplicado à base recebida com alterações de controle em registros não relacionados; essas alterações foram preservadas e uma segunda aplicação não encontrou nada a atualizar. Evidência em `review/liga_v2_package_check.json` e `.txt`.

Logs em `review/liga_v2_validation.txt` e dados em `review/liga_v2_validation.json`. O build completo da ROM e o teste em emulador continuam pendentes: faltam compilador ARM, `pkg-config` e `png.h` no ambiente. Não foi usada GitHub Actions.

## Instalação e reprodução

O aplicador atualiza onze arquivos do jogo. Mescla somente o registro de EverGrande em layouts, os dois registros próprios de Fly e a conexão correspondente na Rota 128. Valida a base antes da escrita e conserva backup. Aceita a base recebida ou a Liga V1; interrompe se encontrar edições divergentes nos arquivos protegidos.

```sh
python3 tools/apply_liga_concept_v2.py --target /caminho/do/projeto --check
python3 tools/apply_liga_concept_v2.py --target /caminho/do/projeto
```

As outras fontes do ZIP são dependências de reprodução e referências. Use o aplicador para integrar ao projeto cumulativo.

Reproduzir dentro do ZIP extraído, com Python, Pillow e compilador C/C++ do host:

```sh
python3 tools/build_liga_concept_v2.py
python3 tools/validate_liga_concept_v2.py
python3 tools/probe_liga_concept_engine.py
python3 tools/build_liga_concept_review.py
make -C tools/mapjson
```

O pacote inclui os mapas anteriores e o tileset anterior exigidos pelo construtor, além dos assets finais. `review/liga_v2_manifest.json` registra os hashes dos arquivos. O patch binário é relativo à Liga V1, commit `6a1f4ac`; a branch local de revisão é `feature/arauna-liga-concept-v2-review`, commit `926f201`. Não houve merge nem publicação.
