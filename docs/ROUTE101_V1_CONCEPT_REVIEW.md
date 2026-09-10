# Rota 101 V1 — Sul de Arauna

A Rota 101 foi reconstruída em 40×28 metatiles seguindo o concept do Sul de Arauna e a função individual definida na página 12 da Design Bible: trilha estreita, clareira, solo ocre avermelhado, capim úmido e cercas curtas. O mapa anterior era uma rota de 20×20 com as faixas de relevo e a circulação herdadas do Emerald.

## Resultado visual

| Direção da referência | Implementação |
| --- | --- |
| Caminho em curva, entre campos e mata leve | Trilha que sai da clareira ao sul, contorna campos a leste e retorna para noroeste |
| Pequena clareira na primeira rota | Área de Anahí e da bolsa, com três saídas controladas durante o resgate |
| Capim úmido e pequenos grupos de árvores | Cinco manchas acessíveis de habitat, bosques internos e campo lateral no sudeste |
| Cercas e solo próximos da vila | Peças do banco de Amanhecer V8, com a mesma paleta de madeira e terra |

O concept recebido reúne as rotas 101–103. A Bible atribui as propriedades rurais à 102 e a água/horizonte à 103; nesta etapa, a fidelidade está nos elementos da 101, sem antecipar esses locais. O mapa não recebeu edifícios, rio ou ponte. A textura foi traduzida para metatiles nativos; a imagem do concept não foi usada como chão pintado.

Comece por `review/route101_v1_concept_comparison.png` e `review/route101_v1_after.png`. O pacote inclui comparação com a rota anterior, camada de eventos, seis recortes individuais de 240×160 e duas vistas de conexão no mesmo tamanho. São renders de terreno, sem sprites de atores sobrepostos, e não capturas de emulador.

## Eventos e progressão

| Dependência | Valor final |
| --- | --- |
| Entradas do resgate | (10, 27) e (11, 27) |
| Posição inicial da perseguição | Anahí em (5, 24), perseguidor em (5, 25) |
| Final da perseguição | Anahí em (9, 22), perseguidor em (10, 22) |
| Bolsa | (12, 24) |
| Jogador após escolher o inicial | (11, 22), ao lado de Anahí após sua aproximação |
| Bloqueios durante o resgate | 2 ao sul, 4 no desvio oeste, 1 na passagem norte |
| Warp narrativo | Interior do laboratório, (6, 5), preservado |
| Conexão norte | x=8..11, offset 0 |
| Conexão sul | x=10/11, offset 0 |

Os 8 objetos, 9 gatilhos e 1 placa mantêm suas identidades. Não há portas/warps estáticos no exterior. Os trajetos de perseguição continuam nativos; mudaram três posicionamentos absolutos e a direção para a qual o jogador olha ao chegar à cena. Flags, variáveis de progressão, diálogos, escolha do inicial, cura e distinção entre protagonistas foram preservados.

O validador confirma que os dois pontos de entrada iniciam o resgate, que as sete barreiras impedem sair ou alcançar capim enquanto a cena aguarda a bolsa e que a bolsa permanece acessível. Os trajetos simultâneos não dividem células nem atravessam uns aos outros. Esse ensaio opera por passos sobre o mapa real, sem simular cada quadro do motor.

## Encontros e mapas vizinhos

São 88 células de capim com comportamento nativo de encontro. A tabela original permanece byte-idêntica: 12 slots terrestres, níveis 2–3 e taxa interna 20. Identificadores de espécies e o mapeamento dos dois Pokémon visíveis não foram alterados; os nomes de slots do Emerald continuam sendo identificadores internos do projeto.

O banco de Amanhecer recebeu quatro metatiles derivados de capim, arbusto e samambaias nativos, nas posições 0x30F–0x312 anteriormente reservadas. Nenhum tile gráfico novo foi necessário. Não mudaram as paletas, os pixels, as portas ou os metatiles usados por Amanhecer.

Vila da Passagem passa a carregar esse mesmo banco para enxergar a Rota 101 antes da transição. A comparação de todos os metatiles usados por Amanhecer, Oldale, Route102 e Route103, incluindo bordas, confirmou aparência idêntica. Seus mapas, eventos e scripts foram preservados. A saída roteirizada de Ciro mantém livres as colunas 9, 10 e 11 da rota, e os gatilhos de encontro com ele continuam cobrindo a chegada à cidade.

## Verificação

- 432 células caminháveis, todas conectadas; objetos, áreas de movimento, placa, gatilhos e duas conexões acessíveis.
- Duas variantes de chegada do jogador, perseguição, bloqueios de saída, acesso à bolsa e aproximação após a escolha do inicial aprovados.
- Eventos e encontros preservados; o renderizador de diálogos em inglês utilizado pelo build conserva as novas coordenadas.
- Funções C nativas `FillNorthConnection`, `FillSouthConnection` e `FillConnection` executadas no computador anfitrião: quatro transições, 812 células copiadas e limites de memória íntegros. Apenas memória e cópia de bytes foram adaptadas ao ensaio.
- Conversão dos eventos por `mapjson` e reprodução do pacote registradas nos relatórios incluídos.
- Extração limpa aprovada: sete arquivos de jogo, quinze imagens e nove arquivos nativos de eventos/cabeçalhos/conexões reproduzidos sem diferenças. O instalador aceitou paletas com CRLF sem mudar cores, preservou alterações independentes de layout e metatiles, tornou-se idempotente e recusou um conflito real antes de escrever.

O build completo da ROM e o teste em emulador continuam pendentes por falta da cadeia ARM e das dependências completas de conversão gráfica. Os renders e ensaios aqui descritos não substituem esse teste.

## Instalação

Esta revisão depende da **Vila Amanhecer V8** já aplicada. O aplicador verifica a base, os vizinhos, as paletas e possíveis conflitos antes da escrita. Ele atualiza sete arquivos, mesclando apenas dois registros de layout e os quatro metatiles reservados nos arquivos compartilhados. Mantém backup e não altera o restante do banco.

```sh
python3 tools/apply_route101_v1.py --target /caminho/do/projeto --check
python3 tools/apply_route101_v1.py --target /caminho/do/projeto
```

Não copie todo o ZIP sobre outro projeto: as demais fontes são dependências de reprodução e snapshots. Execute os construtores somente na pasta de revisão; use o aplicador para integrar ao projeto.

```sh
python3 tools/build_route101_v1.py
python3 tools/validate_route101_v1.py
python3 tools/probe_route101_v1_connections.py
python3 tools/build_route101_v1_review.py
make -C tools/mapjson
python3 tools/package_route101_v1.py
python3 tools/check_route101_v1_package.py
```

Reprodução: Python 3, Pillow, compiladores C/C++ e make. As legendas usam DejaVu Sans quando disponível. Dados completos: `review/route101_v1_validation.json`, `route101_v1_scene_paths.json`, `route101_v1_connection_probe.json`, `route101_v1_integration.json` e `route101_v1_package_check.json`.

O patch parte do commit local `359076f`, que contém Amanhecer V8 sobre a revisão da Liga. Esta etapa foi registrada no commit local `88d122a`, branch `feature/arauna-route101-v1-concept-review`. Sem merge, push ou GitHub Actions. A próxima etapa da ordem canônica é Vila da Passagem.
