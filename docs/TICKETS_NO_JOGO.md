# Arauá e o segundo Lati sem Mystery Gift

O Aurora Ticket (Birth Island, onde está #386 Arauá) e o Eon Ticket (Ilha do
Sul, onde está o Lati que não ficou vagando) só chegavam por Mystery Gift.
Agora os dois vêm dentro do jogo, depois do Hall da Fama. O efeito é o mesmo
dos scripts de presente: o item e a flag do navio
(`FLAG_ENABLE_SHIP_BIRTH_ISLAND`, `FLAG_ENABLE_SHIP_SOUTHERN_ISLAND`). O porto
da Baía das Luzes, que é uma das correções protegidas, não mudou.

## Onde cada um vem

- **Eon Ticket: a mãe.** Na cena em casa depois do Hall da Fama, o pai entrega
  o S.S. Ticket e a TV mostra o Lati voando. Ao fim da conversa, a mãe acha
  outro bilhete no mesmo envelope. Ele tem o desenho de um POKéMON "como o da
  TV, só que de outra cor", ou seja, o par do que está vagando, e diz ILHA DO
  SUL. Um save que já passou da cena recebe o bilhete ao falar com ela.
- **Aurora Ticket: ANAHI, no sensor de Vínculo.** Depois da contagem dos
  lendários (`docs/LENDARIOS_NO_MUNDO.md`), ANAHI nota uma agulha que não aponta
  para rota nenhuma. Ela aponta para o mar, além da Baía das Luzes, para uma
  ilha sem nome na carta. ANAHI entrega o bilhete. A cena não se repete depois
  de entregue, nem depois da batalha com Arauá.

Se a bolsa estiver cheia, o jogo mostra o aviso de sempre e não marca nada, e
a entrega fica para a próxima conversa.

O Mystic Ticket (Navel Rock) e o Old Sea Map (Faraway Island) continuam só por
evento. As espécies dessas ilhas, Oxalá, Saciamigo e Carcará, já aparecem
selvagens em outros lugares.

## Testes no mGBA

Com scripts ligados, numa ROM de harness destes fontes:

| Verificação | Resultado |
|---|---|
| Descer do quarto depois do Hall da Fama | o pai entrega o S.S. Ticket, a TV mostra o Lati, a mãe entrega o EON TICKET; flag do navio marcada |
| Save que já tinha visto a cena, falando com a mãe | ela entrega o EON TICKET |
| Sensor de Vínculo depois do Hall da Fama | após a contagem, ANAHI entrega o AURORA TICKET; flag do navio marcada |
| Porto da Baía das Luzes com o Aurora Ticket | "Is it you who brought that odd ticket?", o barco sai e chega à Birth Island |

A viagem até a Ilha do Sul com o Eon Ticket e o encontro com o Lati já tinham
sido percorridos na integração do 08D (`docs/INTEGRACAO_08D.md`), que usava
os mesmos item e flag.

## Aviso ao autor

| Arquivo | SHA-256 |
|---|---|
| `data/maps/LittlerootTown_ProfessorBirchsLab/scripts.inc` | `c8d3074d3301e07e081dce838afa74cf4eda903ad547808b766ab06a2ba9a8e4` |
| `data/scripts/players_house.inc` | `03a2b255655a902d4a2b2ecb680a673c4e7cc1dddda1b3a0a47cc7cd7e9fde82` |
