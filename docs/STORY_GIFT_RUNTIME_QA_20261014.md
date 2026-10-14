# Presentes de história e abertura normal — continuação de 14/10/2026

Base: `34fd4847a2f5f5ce064a2e13f70fb731d83874b3`, PR #236.
Esta execução preserva integralmente a arte instalada de CIRO. Não muda
sprites, paletas, mapas, layouts, tilesets, portraits, música ou cries.

## Oito caminhos reproduzidos e corrigidos

Na ROM anterior, SHA-256
`5366a77cd57659ace19d3c3b1d7a0437fdfd6f7239a923c1118e5f455a4028b7`,
todos os casos abaixo avançaram a flag de recebimento/ocultação apesar de
`giveitem` falhar. Os receipts `*_story_lost_receipt.json` registram a reprodução
anterior; não são testes da ROM nova.

| Caminho | Consequência anterior | Correção |
|---|---|---|
| ROOT FOSSIL, Mirage Tower | Torre desabava sem entregar o fóssil | Falha mantém ambos os fósseis e a torre |
| CLAW FOSSIL, Mirage Tower | Torre desabava sem entregar o fóssil | Mesma guarda antes de escolher e desabar |
| ROOT FOSSIL, Desert Underpass | Objeto desaparecia sem o item | Ocultação só depois da entrega |
| CLAW FOSSIL, Desert Underpass | Objeto desaparecia sem o item | Ocultação só depois da entrega |
| METEORITE | Máquina passava a vazia sem o item | Flag permanece pendente |
| HM SURF | Cena automática concluía sem a HM | Sai da fase automática; pai de VAL permite retry |
| HM DIVE | Cena concluía, carta omitiria HM e acesso avançava | BENTO retorna uma vez; conversa normal permite retry |
| HM WATERFALL | WALLACE marcava entrega sem a HM | Estado preservado até entrega |

Surf usa o estado existente 5 para encerrar a cena automática, mantendo a flag
da HM desmarcada. A conversa normal prioriza a entrega pendente somente nesse
estado. Dive também encerra a movimentação uma vez, no estado existente 2;
suas flags de recebimento, carta e acesso só avançam após sucesso. Não se
mantém um `OnFrame` repetindo a cena enquanto a mochila permanece cheia.
Nenhum campo, flag nova ou formato de save foi introduzido.

Os oito casos passaram por: falha, SAVE/CONTINUE pendente, segunda falha pelo
NPC/objeto normal, liberação de espaço, entrega, novo SAVE/CONTINUE e ausência
de entrega duplicada. As quatro variantes de fóssil verificam que o objeto
não reaparece após o recebimento; as escolhas da torre executam também o
desabamento e a cena de Route111. Outros oito cenários verificam a entrega
direta com mochila vazia. Duas verificações adicionais impedem Surf/Dive antes
do estado de história previsto.

São testes dirigidos de scripts compilados no mGBA. O setup usa fixtures para
selecionar a cena e preencher a pocket. Para as HMs, a pocket cheia é uma
injeção artificial de capacidade: há menos TMs/HMs únicos que seus 64 slots.
Itens comuns e itens-chave são preenchidos por adição nativa. A liberação de
espaço pelo harness não certifica que todo item-chave seja descartável na UI.
O harness também preserva coordenadas de 16 bits nos mapas largos; a função
de setup `SetWarpDestination` recebe argumentos de 8 bits.

## Abertura ampliada sem alteração da RAM/ROM

Depois do save normal do relógio, o replay passa pela casa de CIRO, conclui o
primeiro encontro, atravessa a ligação com Route101, escolhe o inicial,
vence a primeira batalha e conclui o retorno ao laboratório de ANAHI.
O SAVE é feito pelo menu normal. CONTINUE em outro processo preserva uma
criatura, a flag de resgate e os estados 3 do encontro, rota e laboratório.

`test_natural_start.py` cria a origem desde NEW GAME. O novo
`test_natural_campaign.py` usa exclusivamente joypad e leituras de memória,
além de exportar/importar savedata nativo. Não chama funções injetadas do jogo,
não muda posição/flags/equipe nem força resultado de batalha. O replay de
1.042 ações está em `natural_campaign_replay.json`; as ações incluem esperas
e confirmações de diálogo. Esse percurso não certifica a campanha inteira.

## Regressão e arte preservada

A build canônica e seus gates passaram, incluindo 2.260 textos vinculados à
ROM e 20.104 recursos artísticos. Zero warnings de compilador/assembler; o
gate de imagens local emite um aviso de depreciação do Pillow já existente.
O diff de gráficos, áudio, layouts, tilesets e tabelas gráficas contra #236
permanece vazio. Os PNGs de CIRO F2/F3 continuam com SHA-256:

- F2: `7cb01cd8d660347720489c0babe56109f72aaecc07fd11981d8a8d596d529851`
- F3: `2096be190c806aa00112ce11326d4fc0990c0fadd3a2c8495f63435be7669b74`

Também passaram os testes anteriores: nove gifts, Bento, prêmios das três
Tents, 24 checkpoints de save Frontier, Uivo capturado, início normal e as
11 amostras de sinal/roteamento de áudio. Seus receipts foram atualizados
para a ROM desta execução. Isso não equivale a desafios completos da Frontier
nem audição integral das faixas.

| Medida | Resultado |
|---|---|
| ROM SHA-256 | `49b2898fd2677b01dafdf6dce0d9cc049ed9d413f56b172d68c2f74cd59fbac7` |
| ROM com padding | 33.554.432 bytes |
| ROM utilizada | 31.573.020 bytes (94,09%) |
| EWRAM | 247.164 bytes (94,29%) |
| IWRAM | 29.156 bytes (88,98%) |

`ROM_SHA256.txt` e o guia de publicação identificam esta ROM. O workflow
existente repete build e toda a suíte, incluindo os novos casos e replay.
Ele usa permissões de leitura; ROM, saves, savestates e a biblioteca compilada
do harness não são versionados nem distribuídos no artefato de QA.

```bash
bash scripts/build_arauna.sh -j8 all
bash scripts/test_arauna_remaining_runtime.sh
```

## Pendências mantidas

A campanha natural inteira, os desafios completos das facilities, rollback
durante gravação, sessões reais Link/Wireless e audição integral continuam
pendentes. Entre os gifts ainda a reproduzir estão HM FLY, HM STRENGTH,
DEVON SCOPE, DEVON GOODS, LETTER da Devon, MAGMA EMBLEM e GO-GOGGLES.
A bicicleta exclusiva de CIRO continua pendente, sem qualquer mudança de arte.
Os limites autorais/de Libras e os demais ramos narrativos descritos no relatório
anterior permanecem fora da certificação desta rodada.
