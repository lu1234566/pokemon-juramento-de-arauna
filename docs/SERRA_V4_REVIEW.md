# Serra do Uivo V4 — revisão nativa

Cidade reconstruída a partir da concept art fornecida, após Vila Amanhecer V9. O pacote contém **27 arquivos de integração**, construtores, snapshots, validadores e renders reais do `map.bin`.

## Resultado

Três patamares com alturas físicas 3/5/7, escadas necessárias, cascatas integradas ao relevo, mirante, trilho discreto e onze fachadas completas de pedra/madeira/ardósia. Banco local de **122 metatiles e 184 tiles 8×8**, abaixo dos 496 espaços estáticos da secundária. Os 16 espaços de animação de porta ficam livres.

2060/2400 células diferem da referência Emerald; 2223/2400 diferem da Serra V3 anterior. Contagem de células é apenas uma medida de auditoria: o comparativo com a concept é a referência de julgamento visual.

## Eventos e progressão

As identidades e a ordem dos 12 warps, 16 objetos, 21 gatilhos e 10 placas permanecem. Coordenadas e elevações foram migradas. Os destinos internos, mapas e IDs de save são os mesmos. Não foram criadas flags, recompensas, treinadores nem interiores nesta entrega.

| Warp externo | Destino / índice interno | Nova posição |
|---|---|---|
| 0 | `MAP_RUSTBORO_CITY_GYM` / 0 | 9, 33 |
| 1 | `MAP_RUSTBORO_CITY_FLAT1_1F` / 0 | 15, 48 |
| 2 | `MAP_RUSTBORO_CITY_MART` / 0 | 26, 49 |
| 3 | `MAP_RUSTBORO_CITY_POKEMON_CENTER_1F` / 0 | 28, 32 |
| 4 | `MAP_RUSTBORO_CITY_POKEMON_SCHOOL` / 0 | 29, 40 |
| 5 | `MAP_RUSTBORO_CITY_DEVON_CORP_1F` / 0 | 9, 17 |
| 6 | `MAP_RUSTBORO_CITY_DEVON_CORP_1F` / 1 | 10, 17 |
| 7 | `MAP_RUSTBORO_CITY_HOUSE1` / 0 | 28, 18 |
| 8 | `MAP_RUSTBORO_CITY_CUTTERS_HOUSE` / 0 | 9, 40 |
| 9 | `MAP_RUSTBORO_CITY_HOUSE2` / 0 | 17, 38 |
| 10 | `MAP_RUSTBORO_CITY_FLAT2_1F` / 0 | 8, 50 |
| 11 | `MAP_RUSTBORO_CITY_HOUSE3` / 0 | 33, 51 |

As portas são metatiles reais com comportamento `MB_NON_ANIMATED_DOOR` (0x60). A função nativa de chegada foi executada e retorna sul. O ponto `HEAL_LOCATION_RUSTBORO_CITY` passou de (16,39) para **(28,33)**, em frente ao Centro.

O `scripts.inc` difere em somente três literais de coordenada: as duas portas do cientista e a comparação do X da saída. Todos os comandos de história, flags, itens, textos PT/EN e movimentos permanecem. A fuga mantém (13,21)→(20,12), o empregado termina em (20,14), e as oito variantes de Ciro terminam adjacentes aos gatilhos da saída sul. Os cinco gatilhos do roubo cobrem o acesso obrigatório do bairro do ginásio ao patamar alto.

O interior Casa da Terra e a implementação de Dalva não foram alterados. A **Casa do Uivo é a próxima etapa** da sequência, com sua própria referência e inventário narrativo.

## Evidência e limites

- Validador estrutural: PASS; 841 células alcançáveis, 35 módulos inteiros, 16 percursos de cena, faixas autônomas dos NPCs e retornos dos interiores.
- Cortes de acesso: sem as duas escadas, os respectivos bairros deixam de se conectar; sem os gatilhos, não é possível atravessar os pontos narrativos obrigatórios.
- Funções reais do Emerald em fixture C: PASS em **140 passos** de cenas/escadas e quatro direções iniciais de porta. `IsElevationMismatchAt`, `ObjectEventUpdateElevation` e `GetAdjustedInitialDirection` foram compiladas a partir das fontes do projeto. O ambiente de mapa/objetos é controlado.
- `mapjson` nativo: PASS; 11 arquivos de eventos, conexões, headers e registros gerados.
- Doze recortes de **240×160**, renderizados diretamente dos metatiles; os PNGs não são capturas de emulador.
- ROM completa e emulador não executados: o ambiente não dispõe de `arm-none-eabi-gcc` ou `mgba`.

## Aplicação

Base da cadeia local: `7a89128eecb346a0daa07d60dc2ddb51e4b665e5` (Amanhecer V9). O instalador também aceita o par exato mapa/eventos da Serra V3 cumulativa inventariada. Não aceita uma mistura das duas bases nem sobrescreve conflitos.

Extraia o ZIP numa pasta separada e execute, nela:

```sh
python3 tools/apply_serra_v4.py --target /caminho/do/seu/projeto --check
python3 tools/apply_serra_v4.py --target /caminho/do/seu/projeto
```

Todos os conflitos são conferidos antes da primeira escrita. O instalador guarda backup dos arquivos alterados, preserva entradas alheias em layouts/heal e acrescenta somente o novo registro de tileset. **Não copie o ZIP inteiro sobre o projeto**: as demais pastas contêm fontes de comparação e dependências de auditoria.

## Reprodução

Na pasta extraída, com Python/Pillow, DejaVu Sans, `cc`, `g++` e `make`:

```sh
python3 tools/build_serra_v4.py
python3 tools/validate_serra_v4.py
python3 tools/probe_serra_v4_native.py
python3 tools/build_serra_v4_review.py
```

Execute os builders na pasta de revisão. Eles restauram os arquivos de registro a partir do snapshot para permitir reprodução exata; use o instalador para integrar em um projeto com outras mudanças.

`serra_v4_source/sha256.json` identifica o snapshot funcional e o par V3. `serra_v4_manifest.json` identifica todos os arquivos do ZIP. `serra_v4_package_check.json` registra a extração limpa, a reprodução dos mapas/PNGs e os testes de recusa/idempotência do instalador.
