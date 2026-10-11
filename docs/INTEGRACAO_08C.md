# Integração do checkpoint 08C (SS Tidal)

O bundle `5c8f309fd1` entrou por fast-forward sobre `54c82e4430`. A arte do
navio não precisou de correção. O teste da viagem no mGBA revelou quatro
falas trocadas por engano numa reescrita antiga do enredo, corrigidas nos
scripts.

Conferência:

- **Pacote.** O ZIP tem o SHA-256 do relatório. Os três bundles passam em
  `git bundle verify` e apontam para o mesmo commit. Os 76 arquivos do ZIP
  batem com `SHA256_FILES.json`, e os 66 do manifesto batem com o commit e
  com o checkout.
- **Layouts.** São 754, com IDs e ordem iguais. Os três mapas trocam só os
  bancos, para o par exclusivo `arauna_sstidal08c`. Dos dois bancos, só a
  paleta 12 é nova, e os atributos são os nativos.
- **Build e gates.** A ROM compila e todos os gates passam.
  `validate_sstidal_08c.py` e `check_visual_protection_08.py` passam sobre
  o pacote.
- **Tiles animados.** Os slots animados de General são iguais aos nativos.
  Nenhum dos 130 metatiles usados aponta para slots animados ou desenha
  tile ausente.
- **Portas.** `GetDoorGraphics` procura a animação só pelo ID do metatile,
  sem olhar o banco.
  - As quatro portas do corredor (`0x22B`) usam a animação
    `abandoned_ship`.
  - As quatro das cabines (`0x297`) usam `abandoned_ship_room`.
  - Os metatiles das portas e das vergas, a paleta 7 e os slots 1016–1023
    são os nativos.
  - Renderizados na parede nova, os quadros de abertura combinam com a porta
    fechada.

## mGBA: viagens reais

Todos os scripts ficaram ligados. Fiz as sete verificações que o relatório
pede.

| Verificação | Resultado |
|---|---|
| Embarque nos dois portos | Os atendentes pedem o ticket e mostram os destinos. Na primeira viagem, MR. BENTO aparece no corredor com o convite para o Battle Circuit |
| Porto do Sal → Baía das Luzes | Partida, cama da cabine 2, "We have reached BAIA DAS LUZES", desembarque no porto certo |
| Baía das Luzes → Porto do Sal | Partida, cama (metade da viagem), 205 passos, "We have reached PORTO DO SAL", desembarque no porto certo |
| Battle Circuit | Depois do convite, Porto do Sal oferece BATTLE CIRCUIT e o navio chega ao Circuito |
| Portas e escotilhas | Entrada e saída das cabines e do porão pelas portas animadas. A escotilha mostra o navio cruzando as Rotas 134/133 |
| Batalhas | As oito batalhas do navio vencidas, inclusive a dupla de JAIR. Falando de novo, os treinadores só falam; HILARIO também depois de sair e voltar à cabine |
| TM e Leftovers | TM49 (Snatch) e Leftovers coletados uma vez. Depois do desembarque, a flag que esconde o doador está ligada |
| Salvar e carregar | Salvo a bordo (o save mostra "FERRY"), reiniciado e retomado na mesma etapa da viagem, que segue até o desembarque. Na volta, o menu do Pokémon abre normal |

O save de teste foi montado só no harness local, que não vai para o
repositório. Ele tem jogo zerado, dois Pokémon de nível 100, as oito
insígnias, Repel e estilo de batalha SET. Para as batalhas, a escotilha, o
TM e as Leftovers, o jogo começou dentro do navio, com a variável da
viagem ajustada. As viagens, o embarque, o save e o desembarque foram
jogados desde o porto.

## Correção: falas trocadas por "May"

O commit `5e1c6b7015` trocou o enredo de Emerald pelo de Arauna. Toda fala
cujo rótulo começa com `Text_May`, da rival May, virou fala de CIRO. Quatro
desses rótulos usam "May" como verbo e não são da rival:

| Rótulo | Quem fala | Fala restaurada |
|---|---|---|
| `SlateportCity_Harbor_Text_MayISeeYourTicket` | atendente do porto | "Hello, are you here for the ferry? May I see your TICKET?" |
| `LilycoveCity_Harbor_Text_MayISeeYourTicket` | atendente do porto | a mesma |
| `FallarborTown_CozmosHouse_Text_MayIHaveMeteorite` | PROF. SALUSTIO, antes da pergunta SIM/NÃO | "Please, may I have that METEORITE? …" |
| `Route116_Text_MayISeeThoseGlasses` | homem que perdeu os óculos | "Those glasses! May I see them for a second?" |

Com a troca, o atendente falava de "DISENCHANTMENT" e logo depois dizia que
o jogador mostrou o ticket. A pergunta da troca do METEORITE vinha depois de
uma frase sobre memória. As falas restauradas usam os nomes atuais do jogo.
No mGBA, os dois atendentes já pedem o ticket.

### Observação, sem correção

`SlateportCity_Text_MaybeThisTrainer` também caiu na regra do "May". Mas
a fala antes dela na mesma cena, `YouDroveTeamAquaAway`, foi trocada por
outra regra e virou fala de HORIZON. Restaurar só uma deixaria BENTO
dizendo uma fala de HORIZON. A cena precisa de uma decisão de enredo e
ficou como está.

## Aviso ao autor

Quatro arquivos que o contrato do 08C congela mudaram. Os hashes agora são:

| Arquivo | SHA-256 |
|---|---|
| `data/maps/SlateportCity_Harbor/scripts.inc` | `fc256e12cb37712c2a2b3e026d442e6baa55ed6560909e7cadecda83c19167ea` |
| `data/maps/LilycoveCity_Harbor/scripts.inc` | `46ab224e74a02b311a9a38b0eb8f940b169e9e5d83844283ccda00be39ebd18c` |
| `data/maps/FallarborTown_CozmosHouse/scripts.inc` | `798dc439a26a33d0845646eab56d599d7712e34414c712304d834ae4eb89f4a6` |
| `data/maps/Route116/scripts.inc` | `cd955b92f802f347645b82cc1bc54aa1715d35097009f7504ec98079c46a62c5` |

`validate_sstidal_08c.py` agora para no arquivo de Fallarbor. Antes da
correção, o validador passava inteiro. O próximo pacote deve partir deste
commit e proteger esses quatro arquivos, junto de `party_menu.c`,
`field_player_avatar.c` e `scrcmd.c`.
