# Campanha normal: CIRO, despedida, Pampa, Mata e chegada a Dalva

Base: PR #237, commit `2ea87d27799a4ce8ee206be1f6805cb39e450585`.
A única alteração de gameplay desta rodada é o gatilho da despedida da mãe.
Toda a arte instalada de CIRO permanece exatamente igual; nenhum gráfico,
portrait, paleta, tabela gráfica, layout, tileset ou áudio foi alterado.

## Falha reproduzida e corrigida

Na ROM anterior (`49b2898fd2677b01dafdf6dce0d9cc049ed9d413f56b172d68c2f74cd59fbac7`),
a saída do laboratório reposicionado permite seguir pelo leste, atravessar
Route101 e Vila da Passagem e entrar na Rota 102 sem passar pelos gatilhos
antigos da mãe. O jogador tem a dex e cinco Poké Balls, mas não recebeu os
Running Shoes, não habilitou B dash e mantém o estado 3 da vila. A reprodução
está em `campaign_shoes_bypass_receipt.json`; é evidência histórica da ROM
anterior, não um resultado da build corrigida.

`LittlerootTown/scripts.inc` agora agenda a despedida ao sair do laboratório
nos estados previstos. A mãe aparece à esquerda da saída e usa o diálogo,
a entrega, o fanfare e a conclusão já existentes. O estado temporário é limpo
antes da cena. Os gatilhos antigos continuam válidos e o estado 4 impede
repetição. Não há flags novas, campos novos de save ou mudanças de colisão.

O teste normal recebeu os sapatos, fez SAVE pelo menu, abriu CONTINUE em
outro processo, reentrou e saiu do laboratório sem repetir a cena e seguiu
para a Rota 102 com B dash e estado 4 persistidos.

## Percurso repetível, sem injeção de progresso

Os testes novos usam somente joypad, leituras e importação/exportação do
savedata nativo. Não chamam funções injetadas do jogo, não alteram RAM/ROM,
não teleportam o jogador e não forçam resultados de batalha.

| Teste | Percurso e verificações |
|---|---|
| `test_campaign_to_dex.py` | Save do inicial → clínica → CIRO da Rota 103 → vitória → retorno a ANAHI → dex, cinco Poké Balls e SAVE normal |
| `test_campaign_shoes.py` | Saída do laboratório → despedida → Running Shoes/B dash → SAVE/CONTINUE separado → reentrada sem repetição → Rota 102 |
| `test_campaign_pampa.py` | Rota 102 → Pampa → Elias/Val → tutorial de captura → equipe e Poké Balls preservadas → SAVE/CONTINUE → Rota 104 → Mata da Espera → resgate, Great Ball e novo SAVE/CONTINUE |

As origens são geradas pelos testes anteriores desde NEW GAME: relógio,
encontro com CIRO na casa, escolha do inicial, resgate de ANAHI e SAVE no
laboratório. Os checkpoints novos retomam esses saves reais. O controlador
escolhe caminhos e ações a partir do estado observado; não depende de repetir
uma sequência fixa de tempos para todas as batalhas. Usa LEVEL e REST do menu
ARAUNA instalado, respeitando o limite de nível. Isso verifica progressão e
UI; não certifica o balanceamento sem essas facilidades.

Uma jornada exploratória adicional perdeu a primeira tentativa contra CIRO,
retornou normalmente à clínica com o evento pendente, usou LEVEL e venceu
na segunda tentativa. Os receipts de whiteout e da primeira vitória dessa
jornada identificam a ROM anterior. Em outra continuação real, uma criatura
Grass foi capturada normalmente na Mata; a equipe foi preparada pela UI e
atravessou a saída norte e a ponte até o ginásio de Dalva. O tutorial de Val
também preservou essa equipe de origem, sem criar cópias.

### Ginásio de Dalva: derrota e recuperação verificadas

A continuação exploratória venceu a dupla da ponte da Rota 104 e os
treinadores do ginásio pelo controle normal. Preguicinha e Preguicim foram
capturados; LEVEL elevou a equipe até o limite 15. A loja vendeu Poké Balls
pelo fluxo normal, e LINEAGE ensinou Will-O-Wisp e Reversal. Três tentativas
contra Dalva terminaram em derrota. A recuperação levou à última clínica
registrada, restaurou a equipe e manteve insígnia, TM e avanço da cidade
pendentes. Isso não certifica o balanceamento nem prova impossibilidade de
vitória: o controlador ainda usa uma estratégia de batalha limitada.

`campaign_dalva_reversal_prepared_cold_receipt.json` verifica o checkpoint
antes da terceira tentativa. `campaign_dalva_third_result_cold_receipt.json`
verifica a recuperação após ela. Ambos usam CONTINUE em outro processo,
comparando posição, flags, variáveis e SHA-256 de todos os bytes dos três
Pokémon ativos, além das leituras de espécie, nível, HP, golpes e PP.
O mesmo teste de todos os bytes foi adicionado ao tutorial de Val.

Os journals de inputs usam runs `[keys, count, release, repeats]` para guardar
ações e esperas sem repetir milhares de linhas iguais. A compactação preserva
exatamente as ações; o controlador continua guiado pelo estado observado.
Um pacote separado preserva esses dois saves para retomar a jornada. Eles
não integram o repositório nem o artefato público de CI.

## Build e regressão

| Medida | Resultado |
|---|---|
| ROM SHA-256 | `0cc8a741b0c5af840c45e21d362eccd7577dcead6c52d2af876f15ceb48e4d23` |
| ROM com padding | 33.554.432 bytes |
| ROM utilizada | 31.573.148 bytes (94,10%) |
| EWRAM | 247.164 bytes (94,29%) |
| IWRAM | 29.156 bytes (88,98%) |

A build canônica passou seus gates, incluindo 2.260 textos vinculados e
20.104 recursos de arte, sem warnings de compilador/assembler. Os testes
dirigidos anteriores também passaram na ROM nova: nove gifts, oito caminhos
de gifts de história com retry/entrega direta, duas guardas de elegibilidade,
Bento, três Tents, 24 checkpoints de Frontier, Uivo, 11 verificações de sinal
e roteamento de áudio, abertura e inicial normal. Não são jornadas completas
dessas facilities nem audição integral. Os receipts atualizados identificam
a ROM efetivamente executada.

O workflow repete a build e a suíte completa, agora incluindo a campanha
até o resgate na Mata. ROM, saves, savestates e o helper compilado não são
versionados nem distribuídos no artefato de QA.

```bash
bash scripts/build_arauna.sh -j8 all
bash scripts/test_arauna_remaining_runtime.sh
```

## Limites

O teste automático cobre a abertura até a Mata da Espera, no save masculino
gerado pelo harness. Não certifica todos os iniciais, a variante feminina,
toda a campanha, todas as opções de diálogo ou o balanceamento completo.
As insígnias posteriores, os ramos finais, Link/Wireless real, desafios
completos da Frontier, rollback durante gravação e revisão humana de Libras
continuam pendentes. A bicicleta exclusiva de CIRO permanece pendente,
sem mudanças de arte nesta rodada.
