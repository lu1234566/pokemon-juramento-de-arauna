# Aplicação do plano com arte preservada — 14/10/2026

Continuação de QA, correções adicionais e hash mais recente:
[STORY_GIFT_RUNTIME_QA_20261014.md](STORY_GIFT_RUNTIME_QA_20261014.md).
As evidências e o hash abaixo pertencem à execução anterior.

Base auditada: bcd1fec0025580406d6a6913fcf3e4e0a7824a59. As correções de código, textos e dados estão em três PRs encadeados; o quarto finaliza os únicos PNGs autorizados e guarda as evidências fora dos assets compilados.

## Validação local concluída

Foram executadas 130 assertions dirigidas no mGBA: dados/cap/repelente/relearner (54), LEVEL/cancelamentos (14), Old Rod/Flash/Eon (30), Great Ball da Mata/Serra (14), museu/porto/persistência/opções (18). Os testes foram repetidos após o primeiro reinício do ambiente, com sucesso.

A compilação canônica e os gates estáticos passaram sem warnings de compilador/assembler. Foram comparados 2.260 blocos de texto no endereço ELF da ROM, usando o preproc/charmap do próprio build. A preservação conferiu 20.104 recursos.

ROM testada: SHA-256 3d322afaffc408fc9c135ffba948780784c29768ca8aa27701f0bc9fa195fcad. GCC ARM 13.2.1 e mGBA 0.10.2. EWRAM: 247.164 B (94,29%); IWRAM: 29.156 B (88,98%); ROM sem padding: 31.572.732 B (94,09%).

## Resultado por subsistema

- Recompensas únicas: guardas antes de consumir estado, retry sem repetir batalha na Mata, flags corretas na Serra, Old Rod/Flash/Eon. Carta de Bento possui confirmação distinta e mantém o NPC até entregar TM; sua cena inteira não foi jogada.
- Persistência: museu e porto escrevem hide flags e migram estados antigos. Fuga real dirigida, reentrada e save/carregamento de jogo foram executados.
- LEVEL: rotina nativa de Rare Candy sem consumir item; um Pokémon e um nível por vez; golpes, evolução, repetição, ovos, cap/100/acima do cap e cancelamentos verificados. Oito insígnias mantêm 49; Elite completa libera 58; Hall abre 100.
- Textos: 40 fontes curadas sincronizadas; estados narrativos específicos preservando labels/condições; escape residual e quebra de Salustio corrigidos. MR. BENTO segue a política inglesa atual. O adaptador faz check ou escrita transacional idempotente.
- Dados: Iaraú conserva 20 movimentos, incluindo Uproar 70 confirmado no relearner real; 386 learnsets respeitam o limite. Cinco evoluções modernas preservadas no CSV/gerador; evolution.h intacto. Rock Smash de Trinca-Ferro substituído por Muiraquitã/Granito; Trinca-Ferro permanece na terra.
- QoL: WARD consome o repelente comprado, suprimindo somente expiração. AUTO RUN começa ON; as três opções sobrevivem ao save/carregamento de jogo.
- Arte: somente frames 3/5 de phase2/phase3, linhas 28–31, derivados da outra caminhada da própria folha. Sem alterar cabeça/tronco, demais frames, paleta, transparência, dimensões ou outros recursos. Dez exceções obsoletas e quatro de CIRO removidas após o reparo.
- Ferramentas: atlas compartilhado da Liga seguido no renderer sem copiar recursos; três workflows de escrita legados arquivados; dois .pyc desversionados; gates de source/consumer, progressão, arte congelada e U17 entram na build.

## Recuperação final e evidências

O segundo reinício interrompeu o envio das imagens de QA. O workflow isolado do quarto PR recria o mesmo retoque, recompila, exige o SHA-256 exato da ROM local já testada, repete loops sul/norte de CIRO F2/F3 com os dois gêneros e exporta GIFs/capturas/receipts em review/plan_art_preserved_20261014. Ele não escreve na main e somente publica o resultado na própria branch após os checks passarem.

release_metadata.json, art_freeze_receipt.json e os logs desse workflow identificam o resultado publicado. Os 130 testes locais anteriores não devem ser confundidos com uma campanha natural, nem com uma nova execução de todos os cenários no workflow final.

## Limites

Flash foi testado com uma pocket de TM/HM cheia injetada: existem menos TMs/HMs únicos que os 64 slots, então não se alega que esse inventário surja naturalmente. Os saves usados são fixtures. Bolas e itens-chave usam adição nativa.

Continuam pendentes: bicicleta exclusiva de CIRO (bloqueada pelo escopo), campanha natural completa, audição contextual, matrizes Frontier/Tent/Link, gifts legados não reproduzidos, aceite autoral atual de V2/Libras e evidências externas de autoria/permissão. HORIZON na Serra foi mantido como decisão editorial. Nenhuma licença foi presumida; layouts, portraits, outros Pokémon/NPCs, abertura, ícones e áudio ficaram congelados.
