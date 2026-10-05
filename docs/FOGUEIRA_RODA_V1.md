# Casa da Fogueira — roda de escuta V1

Cena opcional de apoio na Casa da Fogueira de Encruzilhada Central. A referência
é a página 42 da Design Bible e o concept
`04_Casa_da_Fogueira_Encruzilhada_Central.png`. Esta casa é composta por
`Arauna_CasaFogueira_Entrada`, `Arauna_CasaFogueira_Memorial` e
`Arauna_CasaFogueira_Salao`; não confundir com a cidade Casa da Fogueira que
ocupa PacifidlogTown.

O salão reúne seis moradores. O jogador pode ouvir a roda, ler uma carta aberta
no memorial e decidir compartilhá-la. Ouvir e ler funcionam em qualquer ordem.
Cada ação aceita registra um bit persistente; recusar mantém o estado anterior.
Entrada, fogueira e moradores reconhecem a carta depois de compartilhada.
Todos os eventos terminam liberando o controle; não há disparo automático.

A carta é uma vinheta nova, anônima, de apoio ao tema de memória e consentimento,
não uma fala transcrita da Bíblia nem uma revelação sobre a família do jogador.
A autorização para ler em voz alta está no texto da carta. Os diálogos do jogo
estão em inglês conforme a política atual do repositório.

A paleta 06 do banco exclusivo AraunaFogueira foi revista: madeira escura,
reflexos de âmbar e mobiliário quente. Tiles, metatiles, colisões e posições dos
cinco warps não mudaram. O primeiro NPC mantém seu ID local e se aproxima do
círculo; o segundo mantém todos os dados. Quatro novos NPCs estacionários ocupam
células livres. Os sprites usados são os existentes no projeto.

## Estados

| Ação aceita | Flag persistente | Bit |
| --- | --- | --- |
| Ouvir a roda | FLAG_ARAUNA_FOGUEIRA_LISTENED | 0x040 |
| Ler a carta | FLAG_ARAUNA_FOGUEIRA_MEMORIAL_READ | 0x041 |
| Compartilhar a carta após ouvir e ler | FLAG_ARAUNA_FOGUEIRA_SHARED | 0x042 |

São três slots antes não usados. FLAGS_COUNT e a estrutura de save permanecem
iguais. As novas flags não são requisitos de badges, itens ou eventos do arco
principal. Não há remoção de progresso ao revisitar os ambientes.

## Validação

`python3 tools/arauna_maps/validate_fogueira_roda_v1.py` usa o preproc e as macros
reais de eventos para montar somente dados de script com GNU as no host. Testa
224 combinações de evento, estado inicial e resposta, duas ordens de visita,
repetição, finais sem lock e acessibilidade com os NPCs bloqueando suas células.
As caixas de texto padrão são modeladas como retornando a resposta fornecida;
isso não executa o engine ARM. As 80 linhas cabem em até 182 pixels usando as
larguras reais da fonte normal, dentro do limite de 208 pixels.

`python3 tools/arauna_maps/check_interiors_native_encoding_v1.py` verifica os
37 bancos da entrega anterior de 86 interiores: índices em 4bpp, paletas RGB555
e roundtrip LZ10. É uma conversão independente para verificação de formato,
não uma execução do gbagfx nem uma compilação da ROM.

O compilador ARM e o emulador não estão disponíveis neste ambiente. O gbagfx
não compilou por falta dos headers de libpng. Permanecem pendentes: compilação
da ROM, interação visual/timing e persistência em save/load real.

## Instalação e reprodução

Extrair o ZIP e executar `python3 instalar_fogueira_roda_v1.py --target CAMINHO
--check`, seguido pelo mesmo comando sem `--check`. É necessário ter os três
interiores de Encruzilhada integrados na revisão correspondente à base do
pacote. O instalador recusa diferenças nos arquivos que precisa substituir,
verifica dependências, une apenas o bloco próprio de flags, cria backup e
permite reaplicar sem mudanças. Não requer alterar todo o cabeçalho de flags.

O PNG de comparação é uma composição das tiles e dos sprites reais, sem
captura de emulador. O renderer permite reproduzi-lo com `--concept CAMINHO
--output CAMINHO`. Os builders antigos dos interiores podem regenerar scripts
ou paletas da base; reaplicar este pacote depois dessa regeneração.

## Trabalho ainda necessário na Bíblia

Esta cena não conclui S09–S13. Noite de História, defesa comunitária,
manifestação de Arauá e retorno pós-Torre precisam de implementação própria,
com os respectivos gatilhos de progressão e estados. O grafo principal atual
preserva a ordem de Emerald; as divergências de badges e nomes entre a Bíblia
e o cânone do repositório não foram resolvidas por esta cena.

## Instalação no repositório

- A base do pacote bate com o repositório. O instalador compara bytes e as
  paletas do `arauna_fogueira` estavam com LF no checkout, enquanto o
  `.gitattributes` define `*.pal` com CRLF. As 16 paletas foram regravadas com
  CRLF antes da instalação, sem mudar o conteúdo para o git.
- Flags 0x040–0x042 estavam livres (`FLAG_UNUSED_*`, sem outro alias).
- Emulador, partida real pelas três salas: ouvir → ler → compartilhar e
  recusar → ler → ouvir → compartilhar. Toda pergunta aparece, recusar não
  grava a flag, todos os eventos devolvem o controle e as falas de retorno
  (fogueira, banco, moradores, recepção, livro de visitas) aparecem depois de
  compartilhar.
