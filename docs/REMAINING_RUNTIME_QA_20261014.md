# Continuação da QA com a arte de CIRO preservada

Rodada posterior, hash atual e gifts adicionais:
[STORY_GIFT_RUNTIME_QA_20261014.md](STORY_GIFT_RUNTIME_QA_20261014.md).
Os resultados e hash deste relatório pertencem à rodada do PR #236.

Base desta continuação: `46d50777a45f8fbf1f7f600516a47873ec4fc804`, do PR #235.
Base original da auditoria: `bcd1fec0025580406d6a6913fcf3e4e0a7824a59`.

## Defeitos reproduzidos e corrigidos

### Snapshot misto de PC e equipe na Frontier

Uma criatura com personalidade `0x12345678` e LEFTOVERS foi gravada no PC
por SAVE normal. A retirada foi feita pelas funções nativas de armazenamento.
Depois, a rotina de gravação da facility preservou a equipe original, mas
`SAVE_LINK` não atualizou os setores do PC. CONTINUE encontrou a mesma criatura
e o mesmo item tanto na equipe quanto no PC.

`SaveGameFrontier` agora usa `SAVE_NORMAL`: grava um snapshot completo e rotativo
de equipe, mochila e PC. A rotina continua gravando a equipe original e
restaurando a equipe temporária/alugada em RAM. O formato dos saves não muda.
Isso acrescenta os setores do PC à gravação das facilities; o custo é uma
gravação completa, em vez da atualização parcial anterior.

A reprodução anterior está em `frontier_duplicate_receipt.json`, SHA-256
`3d322afaffc408fc9c135ffba948780784c29768ca8aa27701f0bc9fa195fcad`.
Após a correção, 24 combinações de entrada/status passaram em Tower, Factory,
Palace, Arena, Dome e nas três Tents, usando as rotinas compiladas de gravação.
São checkpoints dirigidos, não vitórias nas oito facilities nem sessões Link.

### Nove presentes legados

| Presente | Falha anterior com a pocket cheia | Resultado corrigido |
|---|---|---|
| GOOD ROD | Flag avançava sem a vara | Retry e recebimento único |
| SUPER ROD | Flag avançava sem a vara | Retry e recebimento único |
| WAILMER PAIL | Flag avançava sem o regador | Retry e recebimento único |
| SOOT SACK | Estado avançava sem o saco | Estado permanece pendente |
| COIN CASE | Flag avançava e HARBOR MAIL era consumido | Mail consumido somente após entrega |
| POWDER JAR | Flag avançava sem o pote | Retry e recebimento único |
| HM CUT | Flag avançava sem a HM | Retry e recebimento único |
| HM ROCK SMASH | Flags avançavam sem a HM | Flags preservadas até entrega |
| BASEMENT KEY | Flag avançava sem a chave | Retry e recebimento único |

Cada interação inteira foi executada na ROM antes da correção. As guardas
agora verificam `VAR_RESULT` antes de consumir estado; COIN CASE também só
remove o mail após entregar o item. A mensagem de bolsa cheia já existente é
reutilizada. Não há textos, sprites ou recursos artísticos novos no jogo.

Na versão final, os nove casos passaram por falha de capacidade, SAVE/CONTINUE
pendente, liberação de uma vaga, entrega, novo SAVE/CONTINUE e interação sem
duplicação. O setup libera uma vaga por função nativa; isso não afirma que
todos os itens-chave possam ser descartados pelo jogador. As pockets de TM/HM
dos testes CUT, ROCK SMASH e Bento são sintéticas: há menos TMs/HMs únicos do
que os 64 slots. Esta condição não é apresentada como inventário natural.

## Outras lacunas fechadas nesta execução

- **Bento:** cena completa da carta, bolsa cheia, manutenção do NPC, retry,
  registro de contato e ocultação após CONTINUE; uma TM, carta consumida uma vez.
- **Tents:** nas três rotinas nativas, prêmio pendente com bolsa cheia,
  recebimento posterior e persistência antes/depois de CONTINUE.
- **Uivo capturado:** entrada por fixture no estado 4; MASTER BALL selecionada
  pela mochila normal, resultado de captura real, continuação até estado 8,
  compromisso 1, uma SOOTHE BELL e equipe com duas criaturas após CONTINUE.
  Não se escreveu o resultado da batalha nem os estados seguintes do arco.
- **Início normal:** abertura, NEW GAME, escolha de nome, caminhão, vila,
  casa, relógio, SAVE pelo menu e CONTINUE em outro processo. Somente joypad
  e leituras de memória; não houve edição da RAM/ROM do jogo nesse percurso.
  `natural_inputs.json` guarda o replay e `natural_cold_receipt.json` o retorno.
- **Áudio:** 11 capturas PCM do engine: seis mapas, quatro cries e uma fanfarra.
  Foram conferidos roteamento musical, sinal não silencioso, ausência de
  saturação nos trechos, término dos cries/fanfarra e manutenção da música.
  Cada música foi amostrada por aproximadamente seis segundos; estes checks
  não certificam a audição de cada faixa inteira nem aprovação musical/artística.

## Arte e build final

Nenhum pixel de CIRO foi alterado nesta continuação. Os dois PNGs permanecem
byte a byte iguais ao PR #235, inclusive paleta e transparência. O gate contra
a auditoria conferiu 20.104 recursos; o diff contra #235 é vazio em gráficos,
áudio, tilesets, layouts e wiring gráfico do rival. A bicicleta continua
pendente por exigir asset exclusivo fora do escopo, sem retocar o protagonista.

Build canônica local: GCC ARM 13.2.1; mGBA 0.10.2. Zero warnings de
compilador/assembler. Gates estáticos e equivalência de 2.260 textos da ROM
passaram. O build não reescreveu fontes rastreadas inesperadamente.

| Medida | Resultado |
|---|---|
| ROM SHA-256 | `5366a77cd57659ace19d3c3b1d7a0437fdfd6f7239a923c1118e5f455a4028b7` |
| ROM com padding | 33.554.432 bytes |
| ROM utilizada | 31.572.828 bytes (94,09%) |
| EWRAM | 247.164 bytes (94,29%) |
| IWRAM | 29.156 bytes (88,98%) |

`ROM_SHA256.txt` e a tabela do guia de publicação foram atualizados. Os receipts
registram o hash da ROM em que cada cenário realmente rodou; os de reprodução
anterior são históricos, não testes da ROM final. As 130 assertions do lote
anterior também permanecem históricas e não são somadas como novos testes.

## Reprodução

Instalar GCC/binutils ARM, newlib, libpng, libmgba-dev, Pillow e NumPy; obter o
histórico Git necessário aos gates. Então:

```bash
bash scripts/build_arauna.sh -j8 all
bash scripts/test_arauna_remaining_runtime.sh
```

O workflow `Arauna remaining runtime QA` repete build e testes com permissões
somente de leitura. Suas capturas, receipts, logs e WAVs são evidências externas
ao jogo. ROM, save, savestate e biblioteca compilada do harness não são
versionados nem incluídos no artefato desse workflow. Ele não escreve na main.

## Cobertura ainda pendente

Campanha natural inteira, balanceamento e todos os finais/estados da Torre e
Fogueira na ROM atual ainda não foram percorridos. O teste de Uivo acima fecha
o ramo capturado, sem revalidar todos os ramos possíveis. Batalhas completas das
facilities, rollback por interrupção no meio da gravação e sessões reais de
Link/Wireless também não são certificados pelos checkpoints dirigidos.

A varredura encontrou outros presentes legados com entrega/estado ainda sem
guarda; os nove casos desta continuação não constituem aprovação de todos os
gifts. Persistem aprovação autoral atual de V2, revisão qualificada de Libras,
auditoria auditiva integral e evidências externas de autoria/permissão.
