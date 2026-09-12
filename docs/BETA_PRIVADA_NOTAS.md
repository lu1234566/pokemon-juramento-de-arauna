# Beta privada — o que testar e o que ainda não está pronto

Este documento acompanha a build de beta privada. Ele existe para separar o que
já deve funcionar do que sabidamente ainda não existe, para que o tempo de teste
vá para onde rende.

## O que esta build cobre

**Abertura e primeiros passos.** A professora Anahí abre o jogo no lugar do
Birch, na fala de apresentação da região e no overworld. O prólogo roda inteiro:
caminhão, chegada à vila, a mãe, a casa.

**Elenco.** Trinta e sete personagens nomeados estão desenhados na escala do
overworld — vinte e um pixels de corpo, que é a medida dos NPCs da vanilla. Antes
desta rodada quase todos estavam a vinte e oito, um terço mais altos que qualquer
pessoa com quem dividiam a tela.

**Mapas.** Dez mapas nativos do Arauna, mais as cidades adaptadas às concept
arts: Vila Amanhecer, Vila da Passagem, Pampa da Espera e seus interiores, Serra
do Uivo, Porto das Redes, Liga, e agora Porto do Sal, Encruzilhada com a Casa da
Fogueira, e Vale do Silêncio.

**Criaturas no overworld.** Quarenta e cinco delas, espalhadas por vinte e cinco
mapas.

## O que testar primeiro

1. **Andar por aí, sem pressa.** O travamento mais sério que apareceu nesta
   fase disparava só de uma criatura entrar no alcance de spawn — sem ação
   nenhuma. Está corrigido, mas é o tipo de falha que só a caminhada acha.
2. **As três cidades novas.** Porto do Sal, Encruzilhada e Vale do Silêncio.
   Entrar e sair de todos os prédios, conferir se as passagens levam onde
   deveriam.
3. **A Casa da Fogueira.** Entrada, memorial e salão. São interiores recém
   chegados e nunca jogados.
4. **Chegar de barco em Porto do Sal.** O ponto de desembarque estava fora do
   mapa e foi movido para o cais; vale confirmar que o jogador aparece em pé no
   lugar certo.
5. **Os personagens de perto.** Se algum parecer fora de escala em relação aos
   NPCs comuns ao lado, é defeito.

## O que sabidamente falta

Nada disto é regressão: são frentes que ainda não foram feitas.

- **Interiores das cidades.** Os sete antigos da Encruzilhada, os do Porto do Sal
  e os do Vale do Silêncio. Os pacotes de mapa declaram essas frentes como
  pendentes.
- **Cenas S09 a S13** da Encruzilhada.
- ~~**Idioma misto.**~~ Resolvido. A ROM é inteiramente em inglês: 834 falas
  em 115 arquivos foram traduzidas, o vocabulário do mundo foi unificado
  (`docs/GLOSSARIO_EN.md`) e um portão lê as 37.265 falas visíveis e falha
  se qualquer palavra em português voltar. Nomes próprios — lugares, pessoas
  e criaturas — continuam como são; é a única coisa que a ROM ainda escreve
  em português, por escolha.
- **Três sprites fora de escala, e 23 com o passo pela metade.** Medido e
  escrito em `docs/SPRITES_OVERWORLD.md`. Em resumo: a mãe (25px), a
  recepcionista de link (27px, em dez mapas) e o Dusclops (26px) começam a
  cabeça seis pixels acima do resto do elenco e invadem o tile de cima — é o
  sprite sobreposto da screenshot 5. E em 23 folhas uma das poses de caminhada
  é cópia da pose parada, então o personagem anda mancando. O QC já recusa
  isso em folhas novas.
- **Arcos narrativos.** A visita à Casa do Uivo está implementada, mas o arco
  U03–U11, a batalha, o Selo e as Libras continuam pendentes. A Primeira Câmara
  tem portão e altar funcionando, mas não o Sistema de Vínculos completo.

## Peculiaridades que são da vanilla, não do Arauna

Vale registrar para não virarem relatório de bug:

- A maioria dos NPCs do jogo fica parada olhando para baixo. Isso é o Emerald
  original: 64% dos NPCs da vanilla são estáticos, contra 63% aqui.
- Warps em coordenadas fora do mapa existem na vanilla em nove lugares — Battle
  Frontier, loja de Lilycove, Meteor Falls e o porto de Slateport. São tratados
  por script e ficaram intocados.

## Como isto foi verificado

A build passa por: compilação limpa sem `-Woverflow`, os oito gates do Arauna, o
`scripts/check_arauna_static.sh`, auditoria de limites e identificadores em 528
mapas, validação de todos os pontos de cura, e uma varredura em emulador que
caminha pelos mapas procurando assinatura de travamento.

O que a verificação **não** cobre, e por isso a beta existe: progressão de
história, batalhas, diálogos em sequência, e qualquer coisa que dependa de
flags acumuladas ao longo de uma partida real.
