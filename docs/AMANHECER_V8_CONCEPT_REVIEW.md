# Vila Amanhecer V8 — revisão pelas concept arts

O exterior de Vila Amanhecer foi reconstruído em 30×26 metatiles, com fachadas próprias na resolução do jogo. A referência principal de arquitetura é o par de concepts dedicados da casa do protagonista e do Laboratório Anahí; a Design Bible orienta a função rural, a disposição assimétrica e a circulação da vila.

## Correspondência visual

| Referência recebida | Implementação no mapa real |
| --- | --- |
| Casa com cobertura cerâmica, madeira e janelas azuis | Fachada de 7×6 metatiles, telhado vermelho, base clara, madeira, janelas azuis e caixa de correio |
| Laboratório com cobertura azul-petróleo e emblema circular | Edifício de 8×7 metatiles, cobertura própria, paredes claras, emblema e pequenos vasos externos |
| Jardins e cercas próximos das fachadas | Canteiros, cercas curtas com aberturas e árvores completas junto aos acessos |
| Vila rural com caminho de terra e casas desencontradas | Rua ocre de 2–3 metatiles, casa oeste mais alta, casa leste deslocada e laboratório ao sul em diagonal |

Os volumes, as cores e a relação entre edifício, jardim e acesso vêm dos concepts. Texturas e detalhes foram simplificados para leitura em 240×160 e para o formato nativo de 4 bits por pixel. A vila mantém três edifícios funcionais; ícones genéricos de serviços presentes no concept amplo não substituem os usos definidos pela Design Bible.

Veja `review/amanhecer_v8_concept_comparison.png`, o mapa integral em `review/amanhecer_v8_after.png` e os quatro recortes `review/amanhecer_v8_viewport_*.png`. São renders do terreno e dos assets efetivamente instalados, sem composição de sprites de NPCs; não são capturas de emulador. A camada de eventos aparece separadamente em `review/amanhecer_v8_events.png`.

## Migração funcional

Coordenadas abaixo são metatiles, com origem em zero.

| Elemento | V7 / valor herdado | V8 |
| --- | --- | --- |
| Dimensões da revisão visual anterior | 24×24 | 30×26 |
| Porta da casa oeste | (5, 9) | (6, 10) |
| Porta da casa leste | (17, 13) | (24, 13) |
| Porta do laboratório | (9, 20) | (12, 21) |
| Saída dinâmica do caminhão, variante masculina | (3, 10) | (4, 12) |
| Saída dinâmica do caminhão, variante feminina | (12, 10) | (22, 15) |
| Fly da casa oeste | (5, 9) | (6, 11) |
| Fly da casa leste | (14, 9) | (24, 14) |
| Conexão norte | x=10/11, offset 0 | x=10/11, offset 0 |

Os três índices e destinos de warp, os cinco gatilhos, as quatro placas e os oito objetos mantêm suas identidades. Flags, estados e diálogos foram preservados. Os scripts externos receberam migração de coordenadas e duas correções:

- O guarda agora volta também à linha de origem após empurrar o jogador, evitando deslocamento acumulado em tentativas repetidas de sair da vila.
- A cena do Censo posiciona jogador, Anahí e Ciro em três células distintas nas duas variantes; Anahí não ocupa mais a célula de chegada do jogador.

A chegada do caminhão, a entrada nas casas, os dois destinos de Fly e as cenas dos calçados foram conferidos para ambas as escolhas de personagem. Os arquivos de eventos e scripts dos três interiores e da Rota 101 permanecem byte a byte iguais à fonte preservada.

## Integração gráfica

O tileset `gTileset_AraunaAmanhecer` é uma cópia independente do banco nativo com 308 novos tiles gráficos, 273 metatiles ativos e 386 dos 512 índices secundários alocados. A alocação inclui espaço reservado até os IDs de portas 0x380 e 0x381. Os slots de animação nativa foram preservados.

As duas portas têm três quadros nativos e registros próprios em `src/field_door.c`. O ensaio C compila os registros e executa a função real de busca de porta, com macros de carregamento de assets controladas; ele não equivale a compilar o jogo completo.

A vila e a Rota 101 referenciam o mesmo banco porque o motor desenha parte do mapa vizinho antes da transição. A geometria e os eventos da rota não mudam. A validação compara cada metatile usado pela rota e pelas sete linhas da borda sul de Oldale: a aparência permanece idêntica. As paletas nativas 9 e 10, necessárias a essa borda, foram preservadas. Os assets compartilhados originais de General e Petalburg não foram substituídos.

## Validação concluída

- 3 warps, 5 gatilhos, 4 placas, 8 objetos e 2 destinos de Fly verificados; 286 células alcançáveis.
- Retorno dos interiores, acesso às portas, envelopes de movimento dos NPCs e impossibilidade de contornar os gatilhos iniciais conferidos.
- Duas chegadas do caminhão, três interceptações consecutivas por lado e ambas as variantes das cenas de calçados e do Censo simuladas sobre o terreno real.
- Integridade de fachadas e árvores, formato 4bpp, paletas, orçamento gráfico e registros de portas verificados.
- Conversão nativa de `map.json` em eventos, cabeçalhos e conexões concluída com `mapjson` para Littleroot, InsideOfTruck e Route101.
- Os 32 arquivos de jogo foram reproduzidos byte a byte pelo construtor; o instalador aplicado novamente não propõe alterações.
- Extração limpa do ZIP aprovada: 32 arquivos de jogo, 13 imagens e 9 arquivos nativos de eventos/cabeçalhos/conexões reproduzidos. Aplicação aprovada sobre a V7 e a base original, preservando alterações externas em layouts, Fly e registros C. Uma divergência proposital no mapa foi recusada antes de qualquer escrita.

O build completo da ROM e a execução em emulador continuam pendentes. Este ambiente não possui o compilador ARM necessário nem a cadeia completa de conversão de gráficos. Os resultados apresentados são validação de arquivos, simulação de trajetos, renderização e ensaio C no computador anfitrião.

## Aplicação e reprodução

Extraia o ZIP em uma pasta de revisão. O aplicador aceita a fonte V7 preservada e o projeto-base incluído como referência, verifica conflitos antes da escrita, guarda os arquivos anteriores e mescla somente os registros necessários nos arquivos compartilhados.

```sh
python3 tools/apply_amanhecer_v8.py --target /caminho/do/projeto --check
python3 tools/apply_amanhecer_v8.py --target /caminho/do/projeto
```

O aplicador instala 32 arquivos de jogo: 5 arquivos diretos, 21 novos assets e 6 arquivos compartilhados com alterações delimitadas. As demais fontes do ZIP servem à reprodução e à auditoria; não copie todo o conteúdo sobre outro projeto. O construtor usa o snapshot preservado da V7 e deve ser executado na pasta de revisão, enquanto o aplicador preserva alterações externas compatíveis no projeto de destino.

Reprodução local: Python 3 com Pillow, compilador C, compilador C++ e `make`. As comparações com texto usam DejaVu Sans quando disponível; os metatiles não dependem da fonte.

```sh
python3 tools/build_amanhecer_v8.py
python3 tools/validate_amanhecer_v8.py
python3 tools/probe_amanhecer_v8_registry.py
python3 tools/build_amanhecer_v8_review.py
make -C tools/mapjson
python3 tools/package_amanhecer_v8.py
python3 tools/check_amanhecer_v8_package.py
```

O último comando extrai o ZIP em uma pasta temporária, verifica o manifesto, repete a reprodução e testa o aplicador sobre as duas fontes aceitas. Os relatórios estruturados estão em `review/amanhecer_v8_validation.json`, `review/amanhecer_v8_scene_paths.json`, `review/amanhecer_v8_integration.json` e `review/amanhecer_v8_package_check.json`.

O patch binário parte do commit de revisão da Liga V2, `926f201`, e foi registrado localmente como `359076f`. O branch desta etapa é `feature/arauna-amanhecer-v8-concept-review`. Nenhum merge ou envio remoto foi realizado. Este pacote entrega o exterior de Vila Amanhecer e suas dependências; a revisão conceitual da Rota 101 é a próxima etapa.
