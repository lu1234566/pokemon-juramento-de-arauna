# Campanha — interiores V2: revisão dos desenhos

Esta revisão substitui a arte do caminhão e dos seis interiores da V1. A base
exata é `d561ab72aeb1c98ac72b0dd6661510effaa7362d`, que já instalou a V1 no
branch `claude/pokemon-juramento-arauna-fhk6ah`. São os mesmos sete mapas,
não sete mapas adicionais no placar geral.

## O que mudou

A V1 usava majoritariamente desenhos de Hoenn recoloridos. A V2 redesenha
paredes, janelas com bandeira, portas, estantes, cestaria, rede de pesca,
mesas/cadeiras, bancada de viveiro e instrumentos meteorológicos. As três
caixas móveis do caminhão recebem também um sprite novo de 16×16, mantendo
o ID de objeto, as animações e os deslocamentos originais.

O atlas foi criado pelo image_gen integrado, com desenhos novos e referências
de madeira, reboco, litoral, cultivo e pesquisa pública. O asset de produção é
`art/campanha_interiores_v2/source_atlas.png`; `source_prompt.txt` registra o
briefing. O construtor faz extração dos módulos, redução por vizinho mais
próximo e codificação nativa. Piso, tecido, cerca, gráfico e cama são módulos
novos definidos em código. Os PNGs integrais e as screenshots são renders dos
arquivos reais, nunca o atlas apresentado como mapa implementado.

As sete salas não têm concept individual na Bible. A orientação regional vem
das Rotas 104 (mata/costa), 117 (campos produtivos) e 119 (mata úmida e ciência).
O atlas concretiza essa orientação sem introduzir uma nova função narrativa.

## Medição de desenho

A auditoria compara classes de cor de cada tile 8×8, mantendo transparência,
e considera os quatro espelhamentos horizontal/vertical. Recoloração e troca
de números da paleta não contam como novidade. Tiles inteiramente transparentes
são excluídos, inclusive o preenchimento final da folha.

A referência é o commit `ad0fd4d17f546ca6fd8d785c8724f9382e6e9382`, anterior ao
bootstrap de Arauna (`Expansion 1.16.2 release`). Seu acervo contém 39.376 tiles
armazenados, 26.933 não transparentes e 16.070 padrões canônicos distintos.
Inclui assets da expansion, portanto não é exatamente o corpus de 18.740 tiles
da auditoria externa citada pelo usuário. A referência e os denominadores
estão explícitos para reprodução; os percentuais de corpora diferentes não
devem ser tratados como medidas idênticas.

| Banco | Tiles V1 não vazios | Coincidência V1 | Tiles V2 não vazios | Coincidência V2 |
| --- | ---: | ---: | ---: | ---: |
| carga | 62 | 85.48% | 33 | 21.21% |
| briney | 437 | 95.65% | 119 | 2.52% |
| flores | 106 | 96.23% | 95 | 1.05% |
| daycare | 108 | 96.30% | 125 | 1.60% |
| abrigo | 432 | 97.22% | 104 | 0.00% |
| clima | 231 | 93.51% | 157 | 5.10% |

O primário exclusivo dos seis interiores tem 13 tiles não vazios; 7,69%
coincidem com algum padrão da referência. O caminhão mantém o primário General,
cuja arte não é usada nas células dessa sala. Os novos secundários não carregam
cópias invisíveis da folha original: há 34–158 tiles incluindo o transparente,
e o restante da folha é apenas preenchimento técnico. Nenhum banco novo passa
de 50% de coincidência entre seus tiles armazenados não vazios.

Também há uma medição ponderada pelas células realmente desenhadas, após
compor as duas camadas do metatile. A última coluna mede as referências não
transparentes da camada superior, usada para arquitetura e objetos nesta V2;
não é uma análise semântica de móveis. Ela evita que apenas um piso novo
mascare objetos antigos. Personagens/OBJ ficam fora desta medição de BG.

| Mapa | Blocos compostos coincidentes V1 | V2 | Referências da camada superior coincidentes V2 |
| --- | ---: | ---: | ---: |
| InsideOfTruck | 75.00% | 40.00% | 0.00% |
| Route104_MrBrineysHouse | 39.35% | 6.02% | 2.35% |
| Route104_PrettyPetalFlowerShop | 40.00% | 0.56% | 2.11% |
| Route117_PokemonDayCare | 43.52% | 0.23% | 0.38% |
| Route119_House | 35.00% | 0.00% | 0.00% |
| Route119_WeatherInstitute_1F | 67.88% | 27.31% | 2.08% |
| Route119_WeatherInstitute_2F | 59.77% | 27.84% | 2.50% |

Coincidência exata de padrões simples pode ocorrer entre desenhos independentes:
pisos lisos, faixas e o fundo preto entram nessa conta. A auditoria detecta
reuso exato, não autoria, qualidade estética ou identidade brasileira.
Ela também não detecta uma cópia redesenhada com pequenas diferenças. A
inspeção visual e a coerência com a Bible continuam necessárias.

## Limite de escopo: a geometria permanece

Este lote corrige o problema da arte reaproveitada. As plantas, dimensões e
coordenadas das salas continuam iguais. Não é uma reformulação da geografia
da campanha. A regra futura deixa de ser “colisão idêntica”: a Bible já permite
migrar coordenadas quando scripts, warps, progressão e alcance forem validados.
O próximo bloco de composição deve priorizar a sequência inicial indicada pela
Bible, começando por Vila Amanhecer, Rota 101 e Vila da Passagem.

Os 177 bancos, 229 plantas iguais e demais números globais do diagnóstico do
usuário não foram recalculados neste lote. Não há correção das 55 conexões nem
novos interiores além destes sete mapas.

## Dados e limites nativos

- Sete layouts V2 acrescentados; registros V1 e demais layouts intactos.
- Nos sete `map.json`, somente o layout muda. Grades e bordas são cópias exatas.
- 946 células mantêm IDs, colisão, elevação e comportamento. NPCs, warps,
  triggers, scripts, música e clima não mudam.
- Sete bancos gráficos compactos: seis secundários e um primário exclusivo.
  PNGs indexados com até 16 cores, tiles estáticos abaixo dos slots 992–1023,
  referências somente às paletas BG 0–12. Nenhum callback novo de animação.
- IDs 4/5 do PC e os seis IDs da porta do caminhão mantidos. Primários usados
  por outros mapas e todos os bancos V1 permanecem byte a byte intactos.
- Metatiles não utilizados dos bancos novos ficam transparentes. O inventário
  dos scripts dos sete mapas não pede outros IDs; os estados do PC e caminhão
  usados pelo motor são explicitamente incluídos.
- Fundos externos aos cômodos continuam preto opaco, com comparação pixel a
  pixel contra a V1. Não viram piso e não dependem do índice transparente.

## Verificação

Build inglês e os três gates oficiais aprovados. Readiness estática aprovada:
189/189 protagonista, 95/95 capacidade de paletas e demais verificações oficiais.
Auditoria de mapas: oito verificações aprovadas; permanecem as três notas já
existentes de warps que exigem Surf em Ever Grande/Lilycove. Resíduo: zero
candidatos críticos, PT ou nomes antigos.

O validador independente confere 15.118 arquivos protegidos intactos, todas as
células/bordas, os atributos, os limites de tile/paleta e o roundtrip 4bpp.
Uma segunda execução do construtor reproduziu os mesmos hashes dos 267
arquivos verificados (inclui também bancos V1 protegidos).

mGBA 0.10.2: 18 execuções, nove entradas em cada ROM. Seis interiores em pontos
centrais, caminhão com os dois protagonistas, e uma entrada adicional junto ao
PC do Day Care com interação pelo botão A. A sequência original do caminhão
mostra movimento/porta fechada, parada/porta aberta e saída para a casa correta
em Vila Amanhecer. O PC executa seu script de inicialização. Todas as 12
comparações de grade/cache entre V1 e V2 foram idênticas, incluindo saída e PC.
Não houve opcode ilegal nem alteração das ROMs em disco.

Para os interiores, o harness apenas redireciona temporariamente a entrada em
RAM e restaura a função antes da captura. No caminhão, entrada, callback,
porta e destino permanecem originais. O nome/gênero/opções são inicializados
após o boot; o menu de criação do personagem não é percorrido novamente.
Não foram repetidas as batalhas do Instituto nem os serviços de compra e
criação com uma equipe completa. Sua preservação é sustentada pela identidade
dos scripts, eventos, IDs e atributos. Não se apresenta isso como teste de
campanha completa.

| Região | V1 | V2 |
| --- | ---: | ---: |
| EWRAM | 249.708 B | 249.708 B |
| IWRAM | 30.428 B | 30.428 B |
| ROM ligada | 17.139.700 B | 17.187.396 B |

## Reprodução e entrega

```sh
python3 tools/arauna_maps/build_campanha_interiores_v2.py
python3 tools/arauna_maps/validate_campanha_interiores_v2.py --base /caminho/base-d561ab72ae
python3 tools/arauna_maps/audit_campanha_tile_shapes_v2.py --base /caminho/base-d561ab72ae --original /caminho/original-ad0fd4d17f
bash scripts/build_arauna.sh en -j6
bash scripts/check_arauna_static.sh
python3 tools/arauna/audit_map_data.py
python3 scripts/audit_visible_residue.py
```

O ZIP inclui patch Git binário incremental, arquivos alterados, atlas de
produção, relatório, auditorias reproduzíveis, sete renders integrais, duas
pranchas de comparação no emulador e uma prancha do caminhão/PC. O certificado
confere aplicação em base limpa e identidade de todos os arquivos instalados.
Não contém ROM, saves, estados, ELF, harness ou workflows de GitHub Actions.

## Verificação na instalação

- Aplicado sem conflito sobre `d561ab72ae`; `make MODERN=1` ok.
- `check_arauna_static.sh` 189/189, `check_overworld_palette_capacity.py`
  95/95, `audit_visible_residue.py` 0 candidatos, `audit_map_data.py` com as
  oito verificações aprovadas.
- `validate_campanha_interiores_v2.py` e `audit_campanha_tile_shapes_v2.py`
  aprovados em worktrees limpas (base `d561ab72ae` e original `ad0fd4d17f`).
- Medição independente da arte, comparando os índices de cada tile 8×8, com
  espelhamentos, contra todos os `tiles.png` do original: entre 0% e 9% de
  desenhos iguais aos de Hoenn por banco (na V1 eram 85–96%).
- Regressões: comportamento de metatile de todos os mapas igual à V1;
  animações gerais intactas; variantes de troca de layout atualizadas; bordas
  119/118 sem piora.
- Emulador: caminhão (porta fechada e aberta), os seis interiores
  fotografados depois de sair e entrar pela porta ou pela escada, e o PC do
  Day Care, que liga e abre o menu de PCs.
- Os layouts e bancos da V1 continuam no repositório, mas nenhum mapa os
  usa mais.
