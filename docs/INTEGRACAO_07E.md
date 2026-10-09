# Integração do checkpoint 07E (Battle Pike)

O bundle `a679c20843` entrou por fast-forward sobre `38d7879ae1`. Nenhuma
correção foi necessária.

Conferência:

- **Pacote.** O ZIP bate com o SHA-256 do relatório e os 96 arquivos do
  manifesto batem com o checkout.
- **Layouts.** São 754, com IDs e ordem iguais. Seis layouts do Pike trocam
  só os bancos.
- **Build e gates.** A ROM compila e todos os gates passam.
- **Tiles.** Nos layouts do Frontier trocados desde o 07A, nenhum metatile
  perdeu tiles animados e nenhum desenha tile ausente.
- **Cortina.** Os três quadros que `Task_CloseBattlePikeCurtain` escreve
  (área 3×4 a partir de `0x201`) foram renderizados no banco novo e seguem
  as cortinas abertas.
- **mGBA, 6 mapas.** As salas com script de entrada foram fotografadas sem
  esses scripts. Na sala de Pokémon selvagens, o mato de encontro manteve a
  silhueta e passou de amarelo a cobre.

O container desta sessão foi recriado antes desta integração. O build usa o
`gcc-arm-none-eabi` do Ubuntu e dá o mesmo tamanho de ROM do 07D, conferido
antes de aplicar o pacote.
