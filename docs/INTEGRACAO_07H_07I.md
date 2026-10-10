# Integração dos checkpoints 07H (serviços) e 07I (exteriores)

Os bundles `725f8fe44f` (07H) e `0103bc9731` (07I) entraram por
fast-forward sobre `531352ce37`. Com eles, os 47 mapas do Battle Frontier
estão trocados. Uma correção foi necessária, nas portas do Cable Club.

Conferência:

- **Pacotes.** Os 173 arquivos do manifesto do 07H batem com `725f8fe44f`,
  e os 132 do 07I com `0103bc9731`. Depois do 07I e da correção abaixo,
  cinco arquivos do manifesto do 07H mudaram: `layouts.json`, os três
  headers de tilesets e o `metatiles.bin` do Centro.
- **Layouts.** São 754, com IDs e ordem iguais. Oito layouts trocam só os
  bancos:
  - 07H: `POKEMON_CENTER_1F`, `POKEMON_CENTER_2F`, `MART`, `RANKING_HALL`
    e `EXCHANGE_SERVICE_CORNER`;
  - 07I: `OUTSIDE_WEST`, `OUTSIDE_EAST` e `RECEPTION_GATE`.

  Os três layouts compartilhados (`POKEMON_CENTER_1F`, `POKEMON_CENTER_2F`
  e `MART`) só são usados pelos mapas do Frontier.
- **Build e gates.** A ROM compila e todos os gates passam.
- **Tiles.** Nos oito layouts, nenhum metatile perdeu tiles animados nem
  desenha tile ausente.
- **Conexão Oeste–Leste.** Os dois lados têm primários diferentes, e
  `AraunaConnectionNeedsFullReload` recarrega primário, paletas e animações
  na travessia. No mGBA, a travessia em y=48 não tem costura.
- **Portas.** As 18 portas animadas dos exteriores usam a animação nativa, e
  a animação bate com a fachada nova. No mGBA, a porta da Torre (Leste
  16,14) e a de uma casa (Leste 10,28) abrem sem bloco destoante.
- **Escadas rolantes.** Os quadros que `fldeff_escalator.c` troca são
  nativos e seguem o desenho parado.

## Correção: portas do Cable Club (2º andar)

O metatile `0x25C`, acima das portas `0x264`, ficou nativo. A parede ao
lado (`0x20B`) ganhou uma faixa marrom no alto, e sobravam duas faixas
claras sobre as portas. No original, as linhas 0–6 de `0x25C` são iguais às
de `0x20B`.

`tools/arauna_maps/corrige_porta_cable_club_07h.py` copia os quadrantes de
cima de `0x20B` para `0x25C` nas duas camadas. Os de baixo continuam com a
moldura nativa. A faixa agora segue contínua sobre as portas, no render e no
mGBA. O script confere o original antes de escrever, e rodá-lo de novo não
muda nada.

O `metatiles.bin` de `arauna_frontier07h_clinic` está no manifesto do 07H,
então o hash dele difere do manifesto. Pacotes seguintes devem partir deste
commit e tratar o arquivo como protegido, como foi feito com a água do
Palace no 07C.

A animação da porta do Cable Club não mudou. Ela só toca em jogo por cabo e,
no original, já não batia com o desenho parado.

## mGBA

Fotografados, a partir da entrada:

- os cinco interiores de serviço;
- o portão de recepção;
- 13 pontos do Oeste e 13 do Leste;
- a travessia da fronteira;
- as duas portas abrindo;
- o 2º andar do Centro Pokémon diante das portas do Cable Club.
