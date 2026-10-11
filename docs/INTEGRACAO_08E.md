# Integração do checkpoint 08E (concursos)

O bundle `76d76ddfe5` entrou por fast-forward sobre `e740b80190`. Nenhuma
correção foi necessária.

Conferência:

- **Pacote.** O ZIP tem o SHA-256 do relatório. Os três bundles passam em
  `git bundle verify` e apontam para o mesmo commit. Os 255 arquivos do ZIP
  batem com `SHA256_FILES.json`, e os 246 do manifesto batem com o commit e
  com o checkout.
- **Layouts.** São 754, com IDs e ordem iguais. Os seis palcos trocam só os
  bancos. Saem de General + Contest para seis pares exclusivos: Festival,
  Cool, Beauty, Cute, Smart e Tough. Os primários mantêm a animação de
  General e os secundários não têm callback, como o Contest original.
- **Código.** Nenhum código C usa `gTileset_Contest`. As trocas de metatile
  `METATILE_Contest_*` ficam só no lobby, que não mudou de banco.
- **Build e gates.** A ROM compila e todos os gates passam.
  `validate_contests_08e.py` e `check_visual_protection_08.py` passam,
  incluindo os hashes das sete correções anteriores.
- **Tiles animados.** Nos seis primários, os slots animados de General são
  iguais aos nativos.
  - Em cada palco, os 33 metatiles do mapa foram redesenhados.
  - Nenhum deles aponta para slot animado nem desenha tile ausente.
  - Os atributos dos dois bancos são os nativos.

## mGBA: concursos reais

Todos os scripts ficaram ligados. Joguei um concurso completo em cada uma
das cinco categorias, os quatro ranks em sequência e as recompensas.

| Verificação | Resultado |
|---|---|
| Inscrição | O balcão oferece ENTER/INFO/EXIT, os quatro ranks e as cinco categorias. O Pokémon escolhido entra e o jogador chega ao palco da categoria em (7,5) |
| Cool, Beauty, Cute e Smart, Normal | Cada categoria abre o seu palco. O MC apresenta os quatro participantes. Seguem os cinco apelos, com plateia e aplausos, e os resultados. Na derrota: "Congratulations! Please do compete again!" e volta ao lobby em (14,4) |
| Tough, Normal | "A's Quati won!", com a fita Tough |
| Quatro ranks | No Cool, Normal, Super, Hyper e Master foram vencidos em sequência, duas vezes. A fita Cool sobe de 1 a 4 (lida na RAM). Com a fita já ganha, o balcão pergunta "Would you like to enter it in this CONTEST anyway?" |
| Pintura | Depois do primeiro Master, o artista entra no lobby e mostra o quadro. Aceito o museu, entrega a fita Artist |
| Luxury Ball | O segundo Master, com a fita já ganha, dá a Luxury Ball. A bolsa passa de 0 para 1 |
| Salvar e carregar | Salvo no lobby, reiniciado e retomado no mesmo ponto, com as fitas. O segundo Master foi jogado depois do reinício |
| Link | Sem sessão Link no emulador. A sala aberta direto mostra o palco comunitário, com degraus de pedra. Os figurantes ficam genéricos sem os dados da sessão |

O save de teste foi montado só no harness local, que não vai para o
repositório. Ele tem jogo zerado, dois Pokémon de nível 100 que só conhecem
golpes Cool e as oito insígnias. Nas derrotas, o Pokémon repetia o mesmo
apelo. Para as vitórias, o primeiro Pokémon tinha as condições no máximo e
quatro golpes Cool (Dragon Dance, Dragon Claw, Focus Energy e Cross Chop),
e um passo local trocava de golpe a cada rodada. A flag do curador do museu
foi ligada, como depois de ele levar o jogador ao 2F. Sem ela, o artista não
aparece.

## Para o próximo pacote

O próximo pacote, o 08F (BattleColosseum_2P, BattleColosseum_4P,
RecordCorner, TradeCenter e UnionRoom), deve partir deste commit e manter
protegidas as sete correções listadas no relatório do 08E.
