# Integração do checkpoint 08B1 (DesertRuins)

O bundle `5e51e3b2ba` entrou por fast-forward sobre `393cdf63e4`. A arte
não precisou de correção. O teste do puzzle do Regirock no mGBA revelou um
defeito antigo no menu do Pokémon, corrigido em `src/party_menu.c`.

Conferência:

- **Pacote.** Os dois bundles passam em `git bundle verify` e apontam para
  o mesmo commit. Os 62 arquivos do manifesto batem com o checkout. Os
  `.pal` só batem depois do checkout, porque o git os guarda com LF e os
  grava com CRLF.
- **Layouts.** São 754, com IDs e ordem iguais. Só `DesertRuins_Layout`
  troca os bancos, para um par novo exclusivo do mapa.
- **Build e gates.** A ROM compila e todos os gates passam.
  `validate_desert_08b1.py` e `check_visual_protection_08.py` passam sobre
  o pacote.
- **Tiles animados.** Nos slots animados de General e Cave, o par novo é
  igual ao nativo: água, borda de areia, borda de terra, cachoeira, flor e
  lava. Nenhum dos 47 metatiles que o mapa usa aponta para esses slots ou
  desenha tile ausente. Isso vale também para os da passagem.

## mGBA: percurso real

Todos os scripts ficaram ligados. Nenhuma sala foi fotografada com script
desligado.

- **Entrada.** A porta da Rota 111 leva à câmara de baixo. A porta só abre
  com `FLAG_REGI_DOORS_OPENED`, como depois da Sealed Chamber num jogo real.
- **Braille.** A inscrição abre a caixa de Braille.
- **Rock Smash.** Em (6,23), Rock Smash aparece no menu do Pokémon e
  dispara o efeito de campo. A parede treme, a passagem abre e a porta
  leva à câmara do Regirock.
- **Batalha.** A batalha (Piraruaçu, nv. 40) foi jogada até o fim nas três
  saídas. Em todas o Regirock some do mapa:
  - vitória;
  - fuga ("flew away");
  - captura com Master Ball, recusando o apelido.

O save de teste foi montado só no harness local, que não vai para o
repositório. Ele tem um Pokémon de nível 100 que não conhece Rock Smash, as
oito insígnias e Master Balls. Nas três batalhas, a flag do puzzle já vinha
ligada.

## Correção: menu do Pokémon com muitas insígnias

O commit `001189d29b` faz qualquer Pokémon oferecer os oito golpes de HM
quando o jogador tem a insígnia correspondente. Todos entravam na lista de
ações, sempre. A lista tem oito posições e a janela cabe nove linhas. A
partir da quinta insígnia com dois Pokémon (sexta com um só), a lista
estourava. A janela saía desenhada com lixo e o menu deixava de responder.
Na prática, nenhum golpe de campo podia ser usado no fim do jogo, o que
incluía o puzzle do Regirock.

Agora o golpe que o Pokémon não conhece só aparece onde funciona. Para
isso, o menu chama a mesma função de preparação usada ao escolher o golpe e
depois devolve os callbacks e as variáveis de script que ela altera. No
Dive, ele lê o tile, porque a função real roda o script de mergulho do
mapa. A lista também nunca passa de oito.

As perguntas no mundo (árvore, pedra, rocha, água, cachoeira, mergulho) já
funcionavam sem o golpe e não mudaram. Com o filtro, o menu só oferece o que
não tem pergunta: Fly, Flash, Cut na grama e os puzzles em Braille.

Conferido no mGBA, com as oito insígnias:

| Lugar | Menu oferece | Resultado |
|---|---|---|
| Ruínas, em (6,23) | ROCK SMASH | Abre a passagem |
| Rota 111 | FLY | Abre o mapa de voo |
| Granite Cave B1F | FLASH | Ilumina a caverna |

## Aviso ao autor

`src/party_menu.c` está entre os arquivos que o contrato do 08B1 congela.
O hash dele agora é:

`e05f9efb61cfd652e56a361ba1e8b826f614abc0e684438a0b031b036679d08f`

Por isso, `validate_desert_08b1.py` para na conferência desse arquivo. Com
o arquivo anterior, o validador passa inteiro. O próximo pacote deve partir
deste commit e incluir `src/party_menu.c` entre os arquivos protegidos, sem
regenerar o contrato histórico do 08B1.
