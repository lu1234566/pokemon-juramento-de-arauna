# Integração do checkpoint 08B3 (Mirage Tower 1F–4F)

O bundle `062b84e92f` entrou por fast-forward sobre `a862cdee1d`. Nenhuma
correção foi necessária.

Conferência:

- **Pacote.** O ZIP tem o SHA-256 do relatório. Os três bundles passam em
  `git bundle verify` e apontam para o mesmo commit. Os 80 arquivos do ZIP
  batem com `SHA256_FILES.json`, e os 70 do manifesto batem com o commit e
  com o checkout.
- **Layouts.** São 754, com IDs e ordem iguais. Os quatro andares trocam só
  os bancos, para o par exclusivo `arauna_mirage08b3`.
- **Código.** Nenhum código depende dos bancos antigos.
  `SetCrackedFloorHoleMetatile` só usa os IDs `0x22F` e `0x206`, que o par
  mantém.
- **Build e gates.** A ROM compila e todos os gates passam.
  `validate_mirage_08b3.py` e `check_visual_protection_08.py` passam,
  incluindo os hashes de `party_menu.c`, `field_player_avatar.c` e
  `scrcmd.c`.
- **Tiles animados.** Os slots animados de General são iguais aos nativos.
  Os 41 metatiles usados foram redesenhados, entre eles o piso frágil e o
  buraco. Nenhum aponta para slots animados nem desenha tile ausente. Os
  atributos dos dois bancos são os nativos.

## mGBA: percurso real

Todos os scripts ficaram ligados. Fiz as cinco verificações que o
relatório pede.

| Verificação | Resultado |
|---|---|
| Entrada e escadas | Com a torre visível, a Rota 111 leva ao 1F ("TORRE MIRAGEM"). Subida 1F→2F→3F→4F e descida 4F→3F→2F→1F→Rota 111 |
| Piso frágil, 2F | Com a Mach Bike em velocidade máxima, o jogador cruza a coluna de rachaduras e elas viram buraco atrás dele. A pé, cai para o 1F |
| Piso frágil, 3F | Pisar na rachadura derruba o jogador no 2F |
| Rock Smash | As pedras do 3F e do 4F quebram pela pergunta no mundo e pelo menu do Pokémon. O Pokémon não conhece o golpe; vale a terceira insígnia |
| Fósseis | Recusar deixa o fóssil no lugar. Aceitar o Root ou, em outro save, o Claw: "Obtained the … FOSSIL!", o teto desmorona, o jogador cai na Rota 111, a torre se desfaz e o outro fóssil afunda na areia |
| Underpass | Depois do colapso, `FLAG_HIDE_DESERT_UNDERPASS_FOSSIL` está limpa, a flag do fóssil escolhido está ligada e `VAR_MIRAGE_TOWER_STATE` vale 2 (lidos na RAM). A coleta no Underpass foi verificada no 08B2 |
| Encontros | Encontro selvagem no 1F (Granito, nv. 20) |

O save de teste foi montado só no harness local, que não vai para o
repositório. Ele tem um Pokémon de nível 100 que só conhece Cross Chop, as
oito insígnias, Mach Bike registrada no SELECT, Go-Goggles e Repel. A torre
aparece por `FLAG_FORCE_MIRAGE_TOWER_VISIBLE`, como na primeira visita do
jogo normal.

## Para o próximo pacote

O próximo pacote, o 08C, deve partir deste commit. Ele mantém protegidos
`party_menu.c`, `field_player_avatar.c` e `scrcmd.c`.
