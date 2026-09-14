# Clima e ambientação por bioma

A progressão, ordem de rotas, conexões, scripts, eventos, warps, dimensões e
geometria física de Pokémon Emerald permanecem intactas. Em `map.json`, apenas
o campo `weather` é alterado.

> **Este arquivo foi reescrito.** A tabela anterior descrevia as identidades do
> *Emerald* — "metrópole costeira sob chuva oceânica", "cidade-jardim úmida" —
> escolhidas antes de as cidades virarem lugares do Arauna. Três delas deixaram
> de bater com o nome que a cidade tem hoje, e uma quarta tinha saído do lugar
> numa integração de mapa posterior. A tabela abaixo é derivada da identidade
> **Arauna**, que é a que está na tela.

## Clima não afeta batalha

Vale registrar, porque muda o que está em jogo ao mexer aqui: neste código o
clima do overworld **não** alimenta `gBattleWeather`. `BattleStartClearSetData`
zera a variável e nada a preenche a partir do mapa, então chuva na Mata do Meio
não dá bônus a golpe de Água nem tempestade de areia causa dano por turno. A
única ponte é `GetBattleEnvironment...`, que escolhe o **fundo** de batalha
arenoso quando o clima salvo é `WEATHER_SANDSTORM`. Nenhum mapa desta tabela
usa areia, então nem esse fundo muda.

Ou seja: clima aqui é ambientação, não regra. O que **é** regra e ficou de fora
está na seção "O que não foi tocado".

## As dezesseis cidades

| Cidade | Nome no Arauna | Identidade | Clima |
|---|---|---|---|
| LittlerootTown | VILA AMANHECER | aldeia-jardim clara e compacta | `WEATHER_SUNNY_CLOUDS` |
| OldaleTown | VILA DA PASSAGEM | entroncamento rural aberto | `WEATHER_SUNNY` |
| PetalburgCity | PAMPA DA ESPERA | planície aberta de capim alto | `WEATHER_SUNNY_CLOUDS` |
| RustboroCity | SERRA DO UIVO | serra pétrea, densa e sombreada | `WEATHER_SHADE` |
| DewfordTown | PORTO DAS REDES | vila de pesca, brisa marítima | `WEATHER_SUNNY_CLOUDS` |
| SlateportCity | PORTO DO SAL | porto salineiro, luz dura | `WEATHER_SUNNY` |
| MauvilleCity | ENCRUZILHADA | cruzamento urbano seco | `WEATHER_SUNNY_CLOUDS` |
| VerdanturfTown | VALE DO SILÊNCIO | vale de névoa baixa | `WEATHER_FOG_HORIZONTAL` |
| FallarborTown | CAMPO DAS CINZAS | povoado sob queda de cinza | `WEATHER_VOLCANIC_ASH` |
| LavaridgeTown | CASA DA CINZA | termas ao pé da SERRA DA CINZA | `WEATHER_VOLCANIC_ASH` |
| FortreeCity | MATA DO MEIO | mata chuvosa sobre passarelas | `WEATHER_RAIN` |
| LilycoveCity | BAÍA DAS LUZES | baía tropical, marina e praça | `WEATHER_SUNNY_CLOUDS` |
| MossdeepCity | MISSÕES DO CÉU | ilha técnica, céu limpo | `WEATHER_SUNNY` |
| SootopolisCity | ÁGUAS DE M'BOI | cratera d'água, vertical e tempestuosa | `WEATHER_RAIN_THUNDERSTORM` |
| PacifidlogTown | CASA DA FOGUEIRA | aldeia de passarelas sobre a água | `WEATHER_SUNNY` |
| EverGrandeCity | ESTR. JURAMENTO | santuário de altitude envolto em névoa | `WEATHER_FOG_HORIZONTAL` |

### As quatro que mudaram, e por quê

**PAMPA DA ESPERA** estava em `WEATHER_NONE`, que não é escolha nenhuma — a
integração do Pampa V1 substituiu o `map.json` e levou o clima junto. A tabela
antiga pedia `RAIN`, escolhido quando o lugar ainda era "cidade-jardim úmida".
Uma pampa é planície aberta de capim; o que passa por cima dela é nuvem.

**CASA DA CINZA** estava em `WEATHER_DROUGHT`. O nome é literal e ela fica ao
pé da SERRA DA CINZA, ao lado do CAMPO DAS CINZAS. `DROUGHT` é o estouro de luz
do deserto: lavava a cor das termas e não dizia nada sobre cinza. Agora cai
cinza, como nos vizinhos.

**BAÍA DAS LUZES** estava em `WEATHER_DOWNPOUR`. A arte V2 entregue é baía
tropical com palmeiras, fachadas coloniais, fonte e marina. Temporal permanente
escondia exatamente as luzes que dão nome ao lugar.

**CASA DA FOGUEIRA** estava em `WEATHER_RAIN`. Uma fogueira que não apaga
debaixo de chuva perpétua se contradiz sozinha.

## As rotas: o bioma começa antes da cidade

As trinta e oito rotas estavam **todas** em `WEATHER_SUNNY`. O efeito era que
cada cidade tinha um bioma e a região não tinha nenhum: bastava sair da mata
chuvosa para o céu abrir de uma vez.

A regra aplicada: **uma rota herda o clima do lugar em que ela desemboca,
quando esse lugar afirma um bioma** — chuva, cinza, névoa, encoberto — e não
apenas sol. Assim a chuva aparece antes da mata, e a cinza antes do cinzal.

| Rota | Herda de | Clima |
|---|---|---|
| Rota 101 | VILA AMANHECER | `WEATHER_SUNNY_CLOUDS` |
| Rota 112 | SERRA DA CINZA / CASA DA CINZA | `WEATHER_VOLCANIC_ASH` |
| Rota 115 | SERRA DO UIVO | `WEATHER_SHADE` |
| Rota 116 | SERRA DO UIVO / GALERIAS SERRA | `WEATHER_SHADE` |
| Rota 117 | VALE DO SILÊNCIO | `WEATHER_FOG_HORIZONTAL` |
| Rota 121 | BAÍA DAS LUZES | `WEATHER_SUNNY_CLOUDS` |

E dois lugares nomeados que não tinham clima nenhum:

| Mapa | Nome no Arauna | Clima |
|---|---|---|
| MtPyre_Exterior | MEMORIAL NOMES | `WEATHER_SHADE` |
| SafariZone (6 mapas) | ARAUNA PRESERVE | `WEATHER_SUNNY_CLOUDS` |

## Quatro mapas que **não** foram tocados, de propósito

Cada um destes já tem máquina de clima própria, e mexer no padrão do `map.json`
seria inútil ou danoso. Conferido antes de aplicar, não depois.

- **Rota 113** — onze `coord_event` já trocam para cinza ao entrar no cinzal.
  O padrão ensolarado *é* a aproximação; um padrão chapado apagaria o gradiente.
- **Rota 119** — doze `coord_event` acionam `WEATHER_ROUTE119_CYCLE`, o ciclo de
  chuva da mata. Trocar o padrão só tiraria o ciclo.
- **Rota 120** — um script `OnTransition` define o clima pela posição Y do
  jogador: sol em cima, chuva no meio, nublado embaixo. Ele roda sempre e
  sobrescreve o `map.json`, então mexer ali não teria efeito nenhum. Junto com
  a 119, isso já dá à MATA DO MEIO o corredor chuvoso que ela precisa.
- **Passo Cortado (JaggedPass)** — a cinza dele é acionada por
  `VAR_JAGGED_PASS_ASH_WEATHER`, ou seja, é uma batida de história. Pôr o padrão
  em cinza adiantaria o evento.

## O que não foi tocado

- times, níveis, golpes, IVs, IA, encontros, flags, progressão, layout de save,
  geometria de mapa e warps;
- `music` e `battle_scene` — ver abaixo;
- qualquer mapa com `coord_event` de clima ou `setweather` em script.

## Pendente, e é decisão de elenco: a trilha

Quatro lugares distintos do Arauna dividem tema com outro lugar:

| Lugar | Tema | Divide com |
|---|---|---|
| ENCRUZILHADA | `MUS_RUSTBORO` | SERRA DO UIVO |
| MISSÕES DO CÉU | `MUS_RUSTBORO` | SERRA DO UIVO |
| CASA DA CINZA | `MUS_OLDALE` | VILA DA PASSAGEM |
| CASA DA FOGUEIRA | `MUS_LILYCOVE` | BAÍA DAS LUZES |

**Isto não é resíduo de placeholder: é a própria escolha do Emerald.** Não
existe `MUS_MAUVILLE`, `MUS_MOSSDEEP`, `MUS_LAVARIDGE` nem `MUS_PACIFIDLOG` no
jogo — essas cidades sempre reaproveitaram tema de outra. Trocá-las é redesenhar
a trilha, não corrigir um defeito, e o projeto já tem faixas `MUS_ARAUNA_*`
próprias sendo feitas. Por isso ficou de fora: é escolha de quem está compondo.

Se a decisão for desempatar com o que já existe na ROM, há 77 temas de lugar
não usados por mapa nenhum, incluindo `MUS_DESERT`, `MUS_ROUTE101`,
`MUS_RG_CELADON`, `MUS_RG_FUCHSIA`, `MUS_RG_VERMILLION`, `MUS_RG_CINNABAR` e
`MUS_RG_SEVII_123/45/67`.
