# Integração do checkpoint 07A (Battle Tower)

O bundle `fc408a604b` entrou por fast-forward sobre `7e9d29dc5f`. Os 97
arquivos do manifesto batem com o checkout. Seis layouts da Torre trocam só
os bancos, mantendo IDs, grades e bordas; nenhum layout é acrescentado e os
saves não precisam de migração.

Conferência:

- **Validador do autor.** `validate_frontier_07a.py --base 7e9d29dc5f`
  passou antes das correções abaixo.
- **Build e gates.** A ROM compila e todos os gates passam. A varredura de
  mapas não acusou nada.
- **mGBA, 7 mapas.** O corredor, o elevador, as salas de batalha e a sala de
  parceiros têm scripts de entrada: o atendente leva o jogador adiante. Por
  isso foram fotografados também sem esses scripts, para mostrar o cenário
  parado.
- **Animação no jogo.** Do elevador ao corredor, a porta abre e fecha na
  chegada e o jogador segue até a porta aberta da sala de batalha.

## Portas integradas à parede nova

O pacote manteve nativos os metatiles acima das portas para preservar as
animações: `0x206` sobre a porta de elevador, `0x2A5`/`0x2A6` sobre a porta
dupla Multi e `0x207`, a porta aberta do corredor. A parede nativa tinha uma
faixa branca no alto e a nova é cinza-esverdeada. Por isso sobrava um
retângulo branco acima de cada porta: quatro no saguão, uma no corredor, três
no corredor Multi e uma na sala de parceiros.

`tools/arauna_maps/corrige_portas_frontier_07a.py` aplica a correção e pode
ser rodada de novo sem efeito:

- **Metatiles.** Nas linhas 0–5 desses metatiles entra a parede lisa nova
  (`0x209`), na camada de baixo. Nas linhas 6–7 fica só o que a porta nativa
  desenha diferente da parede nativa: a linha escura da moldura, num tile
  novo da camada de cima, nas paletas nativas 7 e 9. São dois tiles novos no
  secundário da Torre; os demais metatiles não mudam.
- **Animações.** A porta de elevador e a porta dupla ganham animações
  próprias: o desenho parado novo com as folhas da porta copiadas da
  animação nativa. Na faixa de cima, a linha da moldura usa a cor mais
  próxima da paleta 12. O `field_door.c` usa essas animações quando o
  primário é `gTileset_AraunaFrontier07ATowerBase`; nos outros mapas, a
  Battle Tower de Dewford e as portas externas continuam com as originais.

Depois dessas correções, `validate_frontier_07a.py` acusa as mudanças pelo
hash congelado. As alterações são intencionais e estão descritas aqui.
