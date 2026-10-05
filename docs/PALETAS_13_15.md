# Paletas de fundo 13–15 nos tilesets Arauna

O overworld carrega só as paletas de fundo 0–12 dos tilesets
(`NUM_PALS_TOTAL 13` em `include/fieldmap.h`): 0–5 do primário, 6–12 do
secundário. As 13–15 ficam com outras coisas (13 quase preta, 14 moldura de
janela, 15 texto). Os pacotes de interiores da Liga, Porto do Sal, Serra do
Uivo, Encruzilhada, Quatro Cidades e a Vila Amanhecer desenhavam tiles com
as paletas 13–15; no jogo esses tiles saíam pretos ou nas cores da janela de
texto (o oval da câmara de Drake aparecia branco e vermelho; as paredes e
tapetes de casas de Rustboro, pretos e cinza).

## Correção

- `tools/arauna_maps/corrige_paletas_13_15.py` (sem argumentos: simula;
  `--aplicar`: grava) põe as cores de que esses tiles precisam num slot 6–12,
  reaproveitando cores idênticas ou índices que nenhum tile usa naquele slot,
  e reindexa os pixels. Tile que outra paleta também usa é duplicado num slot
  de tile vago. Se não houver espaço, esvazia antes o slot menos usado da
  mesma forma. Aplicado em 38 tilesets secundários.
- As quatro câmaras da Elite usam os mesmos tiles cerimoniais com uma paleta
  por câmara (Sidney 12, Phoebe 13, Glacia 14, Drake 15): não cabem num só
  conjunto de 7 slots. Phoebe, Glacia e Drake ganharam variantes do tileset
  (`gTileset_AraunaLigaVozesPhoebe/Glacia/Drake`) que reaproveitam tiles,
  atributos e animação do `AraunaLigaVozes` e trazem a paleta da câmara no
  slot 12.

## Conferência

- Os 103 layouts afetados renderizam, pixel a pixel, igual ao desenho do autor
  com as paletas 13–15 (comparação dos arquivos antes e depois).
- Varredura de todos os 493 layouts usados por mapas: nenhum tile com paleta
  fora de 0–12, metatile ou tile fora do tileset. As únicas ocorrências são as
  bases secretas do Emerald original, não tocadas.
- Emulador: câmaras da Elite, apartamentos e Devon de Rustboro com as cores
  certas.

Pacotes futuros: rodar a ferramenta sem argumentos depois de instalar; se
listar algo, rodar com `--aplicar`.
