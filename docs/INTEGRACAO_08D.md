# Integração do checkpoint 08D (ilhas especiais)

O bundle `c6143a5173` entrou por fast-forward sobre `72b72497ac`. Nenhuma
correção foi necessária.

Conferência:

- **Pacote.** O ZIP tem o SHA-256 do relatório. Os três bundles passam em
  `git bundle verify` e apontam para o mesmo commit. Os 225 arquivos do ZIP
  batem com `SHA256_FILES.json`, e os 215 do manifesto batem com o commit e
  com o checkout.
- **Layouts.** São 754, com IDs e ordem iguais. Seis layouts trocam só os
  bancos, para cinco pares exclusivos: Southern, Birth, IslandHarbor,
  FarawayCoast e FarawayForest. `LAYOUT_ISLAND_HARBOR` só é usado por
  `BirthIsland_Harbor`.
- **Saves antigos.** A migração do 06B (`ISLAND_HARBOR` para o porto de
  Navel Rock) só vale quando o mapa atual usa o layout novo de Navel Rock.
  Um save no porto de Birth Island não é migrado.
- **Build e gates.** A ROM compila e todos os gates passam.
  `validate_islands_08d.py` e `check_visual_protection_08.py` passam,
  incluindo os hashes das sete correções anteriores.
- **Tiles animados.** Nos seis layouts, os slots animados são iguais aos
  nativos: General, a água com vento e a fonte de Rustboro, e a bandeira de
  Dewford.
  - Os metatiles usados que apontam para esses slots têm as palavras
    animadas iguais às nativas: 13 e 1 na Ilha do Sul, 20 e 1 em Faraway,
    48 na Birth e 11 no porto. Só as partes estáticas foram redesenhadas.
  - Nenhum metatile usado desenha tile ausente.
  - Os atributos são os nativos.

## mGBA: percurso real

Todos os scripts ficaram ligados. Fiz as três sessões que o relatório pede.

| Ilha | Verificado |
|---|---|
| Ilha do Sul | O Eon Ticket é aceito na Baía das Luzes ("Oh? That PASS…") e a viagem chega ao cais. No santuário, a câmera sobe e o Lati (Zumbi-Rei) aparece e se aproxima. A derrota termina em "flew away"; em outro save, a captura com Master Ball. Na revisita, o santuário está vazio. O marinheiro leva de volta à Baía das Luzes |
| Birth Island | O Aurora Ticket é aceito e a viagem atravessa o porto. O triângulo passa pelas 11 posições, dentro dos limites de passos, mudando de cor. Com passos demais, volta ao início (nível 0). A pedra se desfaz, Deoxys (Arauá) desce e é capturado, com registro na Pokédex. Ao voltar do porto, nem Deoxys nem o triângulo reaparecem. O marinheiro leva de volta |
| Faraway Island | O Old Sea Map leva à cena com HONORIO. O jogador sobe pela costa de solo quente até a mata. Mew (Carcará) aparece, se esconde e é encurralado no capim: "Myuu…". Foi capturado num save e derrotado em outro; derrotado, não volta na reentrada. CUT aparece no menu na grama alta e, usado, dá "The feeling of being watched faded…". Salvo na ilha, reiniciado e retomado no mesmo ponto. CAPT. HONORIO leva de volta |

O save de teste foi montado só no harness local, que não vai para o
repositório. Ele tem jogo zerado, as flags de navio das ilhas, os tickets
na bolsa, dois Pokémon de nível 100 que não conhecem Cut, as oito insígnias
e Repel. Na perseguição, um passo local lia a posição real de Mew na
memória e andava até ele. Mew se moveu pela própria IA.

## Para o próximo pacote

O próximo pacote deve partir deste commit e manter protegidas as sete
correções listadas no relatório do 08D.
