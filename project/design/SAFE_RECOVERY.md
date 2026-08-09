# Cura e retorno seguro

O vertical slice precisa continuar dentro de Arauna mesmo quando o jogador
perde uma batalha. Este sistema registra a frente do Centro de Pesquisa como
ponto de recuperação e transforma a Dra. Maia em uma cura repetível.

## Comportamento

- O ponto de retorno é registrado quando o inicial e a Pokédex são recebidos.
- Um whiteout cura a equipe e devolve o jogador à Vila das Araucárias, na
  coordenada passável imediatamente abaixo da porta do Centro de Pesquisa.
- Conversar com a Dra. Maia depois da escolha cura a equipe gratuitamente.
- A cura funciona antes de Nilo, durante a exploração da rota e depois do
  encerramento do vertical slice.
- Estágios da história, escolha de Vínculo, capturas e itens não são reiniciados.

O ponto usa somente dados e scripts. Nenhum NPC, sprite, mapa ou tileset novo é
necessário.
