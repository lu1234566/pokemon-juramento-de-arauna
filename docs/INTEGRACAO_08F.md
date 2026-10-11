# Integração do checkpoint 08F (salas de conexão)

O bundle `90f3f478c8` entrou por fast-forward sobre `f0f08e4ed2`. Nenhuma
correção foi necessária.

Conferência:

- **Pacote.** O ZIP tem o SHA-256 do relatório. Os três bundles passam em
  `git bundle verify` e apontam para o mesmo commit. Os 186 arquivos do ZIP
  batem com `SHA256_FILES.json`. Os 177 do manifesto batem com o checkout e
  com `source/`. As 104 paletas `.pal` diferem do blob do Git só no fim de
  linha: o `.gitattributes` grava `.pal` com CRLF no checkout, e o manifesto
  usa o arquivo do checkout.
- **Layouts.** São 754, com IDs e ordem iguais. Os cinco layouts trocam só
  os bancos. Saem de Building + CableClub (as duas arenas, RecordCorner e
  TradeCenter) e Building + UnionRoom para quatro pares exclusivos: League
  (as duas arenas), Records, Trade e Union. Os primários mantêm a animação
  de Building e os secundários não têm callback. A compressão é a original:
  CableClub sem compressão, UnionRoom comprimido.
- **Código.** Nenhum código C usa os bancos antigos. As trocas de metatile
  do `cable_club.inc` ficam nos balcões dos Centros e em Mossdeep. Na Union
  Room, o código só liga e desliga a colisão dos avatares.
- **Build e gates.** A ROM compila e todos os gates passam.
  `validate_connections_08f.py` e `check_visual_protection_08.py` passam,
  incluindo os hashes das sete correções anteriores.
- **Tiles animados.** Nos quatro primários, a TV de Building (slots 496–499)
  é igual à nativa.
  - Todos os metatiles usados foram redesenhados: 59 em cada arena, 60 no
    RecordCorner, 75 no TradeCenter e 37 na UnionRoom.
  - Nenhum deles aponta para a TV nem desenha tile ausente.
  - Os atributos são os nativos.

## mGBA: sessões reais por cabo

Todos os scripts ficaram ligados. A interface Python do mGBA não traz o modo
multiplayer, então montei um cabo local: dois ou quatro emuladores no mesmo
processo, avançando juntos por ciclos, com o protocolo multiplayer do GBA
(SIOCNT, SIOMULTI e a interrupção serial) feito como no lockstep do mGBA. Os
jogos montaram o link sozinhos.

| Sala | Verificado |
|---|---|
| Balcão do Centro | O atendente do Cable Club oferece TRADE CENTER, COLOSSEUM e RECORD CORNER. Segue o save, "2P LINK" ou "4P LINK", "Start link with N players" e "Please enter". Com escolhas diferentes, o jogo recusa: "The link partners appear to have made different selections" |
| TradeCenter | Os dois sentam e abrem o menu de troca. "Is this trade okay?" mostra os golpes de cada lado. Seguem a animação pelo cabo, "Take good care of Quati!" e o save. Na memória, os Pokémon trocaram de lado. Recarregado o save do jogador 1, o Pokémon recebido continua na equipe. "Cancel trade?" volta à sala |
| BattleColosseum_2P | Os dois ocupam os lugares e a batalha corre inteira nos dois jogos. Tem troca forçada do Pokémon desmaiado, tela Win/Loss e save. A arena volta depois |
| BattleColosseum_4P | Quatro jogos ligados. Cada um escolhe a metade da equipe no seu lugar. A batalha multi, 2 contra 2, vai até o Win/Loss e volta à arena |
| RecordCorner | Os dois ocupam os lugares: "Mixing records…" e "Record mixing completed" |
| Saída | Em todas as salas, a porta pergunta "The link will be terminated if you leave the room. Is that okay?". Segue "Terminating link… You will be escorted out of the room", e todos voltam ao Centro. A porta usa o atributo nativo de seta para o sul |
| UnionRoom | Precisa do Wireless Adapter, que o mGBA não emula. Sem ele, o atendente diz "Unfortunately, your Wireless Adapter is not connected properly." Entrar direto dá "Communication error", como no original. A sala aberta sem scripts mostra a arte nova |

O cabo e os saves de teste ficaram só no harness local, que não vai para o
repositório. Cada jogo começa no 2F do Centro de Lilycove, com Pokédex, a
flag de Mauville (libera o RECORD CORNER) e dois Pokémon de nível 100. O segundo
jogador tem golpes diferentes no primeiro Pokémon, para a troca aparecer na
memória.

## Para o próximo passo

A fila de mapas em bancos Hoenn terminou. O próximo passo, a aceitação final
do ciclo de mapas, deve partir deste commit e manter protegidas as sete
correções listadas no relatório do 08F. A Union Room ainda precisa de uma
sessão sem fio real, em hardware ou num emulador com Wireless Adapter.
