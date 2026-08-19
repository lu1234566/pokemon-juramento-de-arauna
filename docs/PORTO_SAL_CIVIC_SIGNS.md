# Identidade civica de Porto do Sal

## Objetivo

Substituir as placas publicas vanilla de Slateport por uma superficie coerente de PORTO DO SAL, sem alterar eventos, destinos, flags ou mapas.

## Placas curadas

Onze blocos:

1. Tenda de Batalha;
2. Estaleiro — procura por marinheiro veterano;
3. Estaleiro — barco perto da conclusao;
4. Estaleiro — barco concluido;
5. Clube de Fas de POKéMON;
6. Museu Oceanografico;
7. placa principal de Porto do Sal;
8. Mercado de Porto do Sal;
9. Cais — barco em construcao;
10. Cais — servico ativo;
11. Casa do Avaliador de Nomes.

## Identidade urbana

A placa principal deixa de funcionar como resumo de roteiro sobre ARQUIVO VIVO, DESENCANTO e LEMBRANTES. Ela passa a apresentar a cidade como lugar:

- mercado;
- estaleiro;
- pesquisa;
- mareas e atividade portuaria.

O conflito central continua aparecendo onde pertence: personagens, eventos e instituicoes envolvidas diretamente nele.

## Nomes visiveis removidos deste conjunto

- `SLATEPORT`;
- `LILYCOVE`;
- `S.S. TIDAL`;
- `STERN'S SHIPYARD`;
- `OCEANIC MUSEUM`;
- `NAME RATER'S HOUSE`.

O destino costeiro visivel usado na placa do barco e `BAIA DAS LUZES`, ja estabelecido no canon atual.

## Barco

A superficie usa `BARCO DE LINHA`, consistente com:

- Museu de Porto do Sal;
- Estaleiro de Porto do Sal;
- infraestrutura de ferry herdada.

Nenhum nome proprio novo foi inventado para o navio.

## Seguranca

`scripts/render_porto_sal_civic_signs.py` valida:

- 11 labels exatos;
- marcadores da superficie anterior;
- segmentos de no maximo 32 caracteres;
- estrutura nao textual mascarada;
- ausencia dos principais nomes vanilla nos blocos renderizados.

`SlateportCity/scripts.inc` ja pertence ao backup transacional do build por causa das camadas anteriores de Porto do Sal, portanto nenhum arquivo adicional precisou entrar no conjunto de backup.

## Preservado

- scripts das placas;
- estados de ferry;
- destinos;
- Battle Tent;
- Name Rater;
- mercado;
- objetos e coordenadas;
- flags/vars;
- saves e progressao.

Sem arte, sem Codespaces e PR #58 intocado.
