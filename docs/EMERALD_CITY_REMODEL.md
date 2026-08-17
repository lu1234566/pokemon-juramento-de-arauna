# Remodelação das cidades — base Emerald

A progressão, ordem de rotas, conexões, scripts, eventos, warps, dimensões e geometria física de Pokémon Emerald permanecem intactas.

A composição visual foi remixada somente com blocos/metatiles já presentes no próprio mapa vanilla; nenhum gráfico externo foi adicionado.

| Cidade | Identidade | Clima | Composição visual alterada |
|---|---|---|---:|
| LittlerootTown | aldeia-jardim clara, compacta e acolhedora | `WEATHER_SUNNY_CLOUDS` | 107/400 (26.8%) |
| OldaleTown | entroncamento rural aberto e ensolarado | `WEATHER_SUNNY` | 221/400 (55.2%) |
| PetalburgCity | cidade-jardim úmida organizada em bairros | `WEATHER_RAIN` | 502/900 (55.8%) |
| RustboroCity | centro urbano pétreo, denso e sombreado | `WEATHER_SHADE` | 1650/2400 (68.8%) |
| DewfordTown | vila costeira compacta de brisa marítima | `WEATHER_SUNNY_CLOUDS` | 108/400 (27.0%) |
| SlateportCity | porto comercial amplo, luminoso e irregular | `WEATHER_SUNNY` | 1672/2400 (69.7%) |
| MauvilleCity | cruzamento urbano seco e movimentado | `WEATHER_SUNNY_CLOUDS` | 418/800 (52.2%) |
| VerdanturfTown | vila verde de névoa baixa e jardins | `WEATHER_FOG_HORIZONTAL` | 169/400 (42.2%) |
| FallarborTown | povoado de cinzas vulcânicas e terreno áspero | `WEATHER_VOLCANIC_ASH` | 152/400 (38.0%) |
| LavaridgeTown | cidade termal quente, seca e mineral | `WEATHER_DROUGHT` | 140/400 (35.0%) |
| FortreeCity | assentamento florestal chuvoso em plataformas | `WEATHER_RAIN` | 439/800 (54.9%) |
| LilycoveCity | metrópole costeira em terraços sob chuva oceânica | `WEATHER_DOWNPOUR` | 2171/3200 (67.8%) |
| MossdeepCity | ilha tecnológica clara, espaçada e marítima | `WEATHER_SUNNY` | 1681/3200 (52.5%) |
| SootopolisCity | cidade-cratera dramática, vertical e tempestuosa | `WEATHER_RAIN_THUNDERSTORM` | 2330/3600 (64.7%) |
| PacifidlogTown | aldeia flutuante chuvosa de passarelas | `WEATHER_RAIN` | 398/800 (49.8%) |
| EverGrandeCity | santuário de altitude envolto em névoa | `WEATHER_FOG_HORIZONTAL` | 2409/3200 (75.3%) |

## Invariantes verificadas automaticamente

- ordem e conexões de progressão do Emerald preservadas;
- warps, object events, coord events, bg events e scripts preservados;
- colisão e elevação preservadas bit a bit em todas as coordenadas;
- bordas, portas e coordenadas sensíveis preservadas;
- somente blocos existentes no mapa vanilla são reutilizados;
- em `map.json`, somente `weather` é alterado;
- nenhuma cidade pode ficar abaixo de 18% de composição visual alterada.
