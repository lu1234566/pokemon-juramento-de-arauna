# Integração do checkpoint 07B (Battle Dome)

O autor montou o 07B (`868226c157`) sobre o 07A dele (`fc408a604b`). Esta
branch já tinha, por cima dele, a correção das portas da Battle Tower
(`52e6f87e1b`). Os dois mexem em arquivos diferentes, então o 07B entrou por
merge sem conflitos, preservando o commit do autor.

Conferência:

- **Pacote.** Os 89 arquivos do manifesto batem com o checkout.
- **Layouts.** São 754, com IDs e ordem iguais. Quatro layouts do Dome
  trocam só os bancos.
- **Build e gates.** A ROM compila e todos os gates passam. A varredura de
  mapas não acusou nada.
- **mGBA, 4 mapas.** Corredor, sala pré-batalha e arena foram fotografados
  sem os scripts de entrada, para mostrar o cenário parado.

## Portas

O autor manteve nativos os pixels das dez células das portas, para
preservar as animações. Diferente da Torre, aqui a parede nova não deixa
emenda. A verga vermelha das portas do corredor e a moldura das portas do
saguão ficam como detalhe da porta sobre a pedra e o bronze. Por isso
nada foi alterado.
