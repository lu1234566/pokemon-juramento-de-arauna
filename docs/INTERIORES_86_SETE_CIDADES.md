# Interiores — 86 mapas em sete cidades (V1)

Instalação do `Pokemon_Juramento_de_Arauna_Interiores_7_Cidades_86_Mapas_V1`,
que chegou dentro da Retomada Consolidada de 05/10/2026. Quatro subpacotes:
Serra do Uivo (16, Rustboro), Porto do Sal (14, Slateport), Encruzilhada
Central (8, Mauville) e Quatro Cidades (48: Campo/Fallarbor, Casa da
Cinza/Lavaridge, Mata do Meio/Fortree, Baía das Luzes/Lilycove). Cada
subpacote tem o seu documento (`SERRA_`, `PORTO_`, `ENCRUZ_`,
`QUATRO_INTERIORS_V1.md`).

## O que muda

Só o visual: 37 tilesets secundários novos e um layout próprio por mapa. Nos
86 `map.json` o único campo alterado é `layout`. Tamanho, colisão, elevação e
comportamento de metatile são idênticos aos layouts antigos, tile a tile.

## Conferência

- Os 369 metatiles que código ou scripts referenciam pelo nome, nas famílias
  dos tilesets substituídos (Centro Pokémon, loja, ginásio elétrico, museu,
  concursos, fábrica, tenda), mantêm o comportamento nos tilesets novos. O
  desenho foi comparado lado a lado: os feixes e interruptores do ginásio de
  Encruzilhada, a escada rolante e as barreiras do Cable Club, os laptops da
  loteria e o elevador da loja continuam reconhecíveis. A porta do Cable Club
  virou um bloco liso em vários Centros (a animação de abertura continua).
- Emulador: 22 mapas cobrindo todas as famílias de tileset carregam e
  renderizam sem tile corrompido e sem travamento.

## Correções na instalação

- Três `map.json` partiam de uma base anterior ao lote 06 e trariam de volta
  `OBJ_EVENT_GFX_SCOTT`: `FallarborTown_BattleTentLobby`,
  `LilycoveCity_CoveLilyMotel_2F` e `RustboroCity_PokemonSchool`. Entrou só o
  layout novo; o objeto continua `OBJ_EVENT_GFX_STEVEN`.
- `InSlateportBattleTent()` (`src/battle_tent.c`) reconhecia a Tenda de
  Slateport pelo layout do corredor e da sala de batalha. Com os layouts
  novos, a tela de resumo deixaria de tratar os Pokémon de aluguel como
  emprestados. Agora a função compara o mapa atual.
