# Integração do checkpoint 07C (Battle Palace e Battle Arena)

O bundle `638d523c08` entrou por fast-forward sobre `9f0a056e90`.

Conferência:

- **Pacote.** Os 168 arquivos do manifesto batem com o checkout.
- **Layouts.** São 754, com IDs e ordem iguais. Seis layouts trocam só os
  bancos.
- **Build e gates.** A ROM compila e todos os gates passam.
- **Varreduras.** A de mapas não acusou nada, e a de portas mostra as portas
  do Palace iguais às nativas.
- **mGBA, 6 mapas.** A água do pátio do Palace anima com o primário privado
  (callback `InitTilesetAnim_General`). O corredor do Palace foi fotografado
  sem sprites, porque, com os scripts de entrada desligados, os objetos
  ficam sem gráfico.

## Água na sala de batalha do Palace

No original, o metatile `0x226` é água com a margem de pedra à esquerda,
quase igual ao `0x190`. O banco 07C o redesenhou como bloco de parede, e a
sala de batalha ficou com um bloco cinza dentro da água em (2,4) e (2,5), as
únicas células que o usam. O comportamento de água estava certo; o defeito
era só visual.

`tools/arauna_maps/corrige_agua_palace_07c.py` copia para `0x226` os
gráficos do `0x190` novo e mantém os atributos. Pode ser rodada de novo sem
efeito.

## Observação

Nos canteiros do corredor do Palace, as moitas entre as flores ficaram em
verde bem escuro. No jogo, elas aparecem como folhagem densa e não como
falha, então ficaram como o autor desenhou.
