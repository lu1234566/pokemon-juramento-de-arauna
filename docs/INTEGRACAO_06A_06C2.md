# Integração dos checkpoints 06A, 06B, 06C1 e 06C2

Trainer Hill, Navel Rock e as 24 Bases Secretas entraram pelo bundle
cumulativo do pacote 06C2. O fast-forward a partir de `872f56e86f` preserva
o histórico do autor:

| Commit | Conteúdo |
|---|---|
| `29ae94cdc2` | 06A, Trainer Hill (7 mapas) |
| `2449e12b06` | 06B, Navel Rock (21 mapas e o porto) |
| `0098c5c3b5` | 06C1, 16 bases em cavernas |
| `6cfba8c79b` | conciliação com a manutenção `872f56e86f` |
| `989c33c94f` | 06C2, 8 bases em árvores e arbustos |

## Conferência

- **Pacote.** Os 83 arquivos do manifesto batem com o checkout, incluindo as
  paletas em CRLF.
- **Layouts.** São 754. Os 744 anteriores mantêm IDs e ordem; 38 trocam
  apenas os bancos e 10 novos entram no final. Os 26 bancos removidos na
  manutenção continuam fora.
- **Código C.** Fora dos três cabeçalhos de tilesets, que só ganham
  declarações, o pacote não mexe em código. A correção de Oldale e a borda de
  Petalburg continuam iguais.
- **Validador do autor.** `validate_secret_06c2.py --base 6cfba8c79b` passa.
- **Build e gates.** A ROM compila e todos os gates passam. A varredura de
  mapas (IDs, tiles ausentes, bordas) não acusou nada no jogo inteiro, e a de
  `setmetatile` não acusou nada novo.
- **mGBA, 77 fotos dos 53 mapas.** Os andares do Trainer Hill aparecem como o
  motor os gera no modo Normal. As bases foram fotografadas com
  `VAR_INIT_SECRET_BASE` = 1; sem isso, o roteiro de primeira entrada devolve
  o jogador para fora. Oito bases, de todas as famílias de banco, foram
  decoradas pelo próprio jogo: móveis gravados em `secretBases[0]` e
  desenhados por `InitSecretBaseAppearance` ao reentrar.

## Correções na integração

### Portas do elevador do Trainer Hill

A animação de porta de 16×32 redesenha a porta e o metatile de cima, só com
a camada de baixo. Os bancos do pavilhão redesenharam a parede acima das duas
portas de elevador (`0x32C` no saguão e `0x383` na cobertura), mas a animação
nativa continuava pintando a parede de Hoenn. Enquanto a porta abria e
fechava, aparecia um bloco branco no saguão e um verde-água na cobertura.

A correção usa duas animações próprias, geradas por
`tools/arauna_maps/gera_portas_trainer_hill_06a.py`. Cada quadro é o desenho
parado do banco novo, com as folhas da porta copiadas da animação nativa:

- a parede e a moldura saem exatas;
- na faixa em que o friso novo (paleta 12, cheia) encontra a folha da porta,
  o interior da porta usa a cor mais próxima da paleta 12.

O `field_door.c` usa essas animações quando o primário é
`gTileset_AraunaTrainerHill06APavilionBase`, como já fazia com as portas de
madeira do Início. A Battle Tower continua com as originais.

### Saves antigos em Navel Rock

O jogo carrega o layout pelo ID gravado no save. Um save feito numa versão
anterior em Down01–11, Up3/Up4 ou no porto de Navel Rock abriria com o
layout antigo até o jogador sair do mapa. O mesmo vale para o elevador do
Trainer Hill. Nos Down, o layout antigo agora tem a arte de Up1/Up2.

`AraunaMigrateInitialMapSave` virou uma tabela de pares (layout antigo,
layout atual do mapa) e ganhou os 10 pares novos. Como os pares são
conferidos juntos, o porto de Birth Island, que continua com
`LAYOUT_ISLAND_HARBOR`, não é afetado.

Teste:

- **Saves novos.** Seis saves foram criados na ROM anterior ao pacote e
  continuados na nova. Down01, Down05, Down10, Up3 e o porto abrem nos
  layouts novos. Up1, que manteve o ID, fica como está.
- **Pares antigos.** Os oito saves da versão `591aeb2497` continuam migrando
  para os layouts Sul/Pampa, Uivo e Composição.
- **Elevador.** Ali não dá para salvar: o aviso da entrada trava o menu.

## O que continua pendente

O pacote não muda a lógica de jogo, e o autor cobriu os fluxos com testes de
host. Ainda não foram jogados no emulador:

- os 16 desafios do Trainer Hill com cronômetro, derrota, recorde e prêmio;
- o barco para Navel Rock;
- as batalhas e capturas de Ho-Oh e Lugia;
- o record mixing das bases.
