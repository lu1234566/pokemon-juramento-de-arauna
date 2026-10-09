# Integração do checkpoint 07D (Battle Factory)

O bundle `2a1838d000` entrou por fast-forward sobre `8d7cafa5d7`. Nenhuma
correção foi necessária.

Conferência:

- **Pacote.** O ZIP bate com o SHA-256 do relatório e os 82 arquivos do
  manifesto batem com o checkout.
- **Layouts.** São 754, com IDs e ordem iguais. Três layouts da Factory
  trocam só os bancos.
- **Build e gates.** A ROM compila e todos os gates passam.
- **Varredura de mapas.** Não acusou nada.
- **Tiles animados.** Nos layouts do Frontier trocados desde o 07A, nenhum
  metatile que usava tiles animados no original (slots 432–511 do
  primário) os perdeu. Esse era o sintoma da água `0x226` do Palace,
  corrigida no 07C.
- **mGBA, 3 mapas.** A sala pré-batalha e a arena foram fotografadas sem os
  scripts de entrada. A Factory não usa portas animadas: as passagens são
  movimentos e fades de script.
