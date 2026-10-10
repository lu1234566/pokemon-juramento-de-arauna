# Integração do checkpoint 08B2 (DesertUnderpass e ScorchedSlab)

O bundle `646a270fdf` entrou por fast-forward sobre `0434665c07`. A arte
não precisou de correção. O teste do ScorchedSlab no mGBA revelou dois
defeitos antigos na função "sem escravos de HM", corrigidos em
`src/field_player_avatar.c` e `src/scrcmd.c`.

Conferência:

- **Pacote.** Os três bundles passam em `git bundle verify` e apontam para
  o mesmo commit. Os 104 arquivos do ZIP batem com `SHA256_FILES.json`. Os
  94 do manifesto batem com o commit e com o checkout.
- **Layouts.** São 754, com IDs e ordem iguais. Só `DesertUnderpass` e
  `ScorchedSlab` trocam os bancos, para pares novos exclusivos de cada mapa.
- **Build e gates.** A ROM compila e todos os gates passam.
  `validate_desert_08b2.py` e `check_visual_protection_08.py` passam sobre
  o pacote.
- **Tiles animados.** Nos dois pares, os slots animados de General e Cave
  são iguais aos nativos. Nos 10 metatiles de água do ScorchedSlab, a
  camada de baixo (a água animada) não mudou. A camada de cima ganhou
  margens novas e, onde estava vazia, o tile 943, que é transparente. Nenhum
  metatile usado desenha tile ausente.

## mGBA: percurso real

Todos os scripts ficaram ligados.

- **Underpass, entrada.** Com o jogo zerado e o Root Fossil escolhido, o
  túnel da Rota 114 leva ao Underpass.
- **Underpass, fóssil.** Ao fim da galeria, "Obtained the CLAW FOSSIL!" e o
  fóssil some.
- **Underpass, volta.** Na saída e na volta ("PASSAGEM SECA"), o fóssil não
  reaparece. Um encontro selvagem (Zabumba, nv. 38) abre com o fundo de
  batalha do deserto.
- **ScorchedSlab, entrada.** Da margem da Rota 120, a pergunta de Surf leva
  pela água até a porta da caverna. O jogador chega surfando e desembarca
  no patamar.
- **ScorchedSlab, TM.** "found one TM11 SUNNY DAY!" e o item some.
- **ScorchedSlab, volta.** O jogador surfa de volta, sai pela porta e
  entra de novo. O TM não reaparece.

O save de teste foi montado só no harness local, que não vai para o
repositório. Ele tem um Pokémon de nível 100 que só conhece Cross Chop, as
oito insígnias e Repel. A flag que esconde o fóssil foi limpa na RAM. No
jogo normal, quem a limpa é o desabamento da Mirage Tower.

## Correção: Surf e Secret Power na função "sem escravos de HM"

O commit `001189d29b` faz qualquer Pokémon usar os golpes de HM quando o
jogador tem a insígnia. A função tinha duas falhas.

- **Surf não funcionava.** A água só oferece Surf se `PartyHasMonWithSurf()`
  for verdadeira. Essa checagem roda em C antes do script e exigia um
  Pokémon que conhecesse o golpe. Sem ele, apertar A na água não fazia nada
  e o menu também não oferecia Surf. Agora qualquer Pokémon que não seja
  ovo serve, como em `checkpartymove`. As duas chamadas já checam a
  insígnia antes.
- **Secret Power não era HM.** O substituto de `checkpartymove` valia para
  qualquer golpe. Com isso, qualquer Pokémon abria base secreta sem o TM43.
  O commit original prometia só os oito HMs, e agora o substituto vale só
  para eles. Base secreta voltou a pedir um Pokémon que saiba Secret Power.

Conferido no mGBA, com um Pokémon que não conhece Surf:

| Lugar | Ação | Resultado |
|---|---|---|
| Rota 120, de frente para a água | Apertar A | "Would you like to SURF?"; o jogador surfa |
| Mesmo lugar | Abrir o menu do Pokémon | SURF e FLY oferecidos; SURF funciona |
| Rota 111, entrada de base secreta | Apertar A | "There's a small indent in the wall.", como no original |

## Aviso ao autor

Dois arquivos que o contrato do 08B2 congela mudaram. Os hashes agora são:

| Arquivo | SHA-256 |
|---|---|
| `src/field_player_avatar.c` | `81ebe4b5761f8992cb459cf37978262358231734a1c56f8b3447346f770db95f` |
| `src/scrcmd.c` | `98cd4b72474c3cc7dfd5dc6cf54a4a96f807733017761a2be58d62b0dcd063a9` |

`validate_desert_08b2.py` agora para em `src/field_player_avatar.c`. Antes
da correção, o validador passava inteiro. O próximo pacote deve partir deste
commit e proteger os dois arquivos, junto de `src/party_menu.c`, sem
regenerar os contratos históricos.
