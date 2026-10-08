# Pokémon Juramento de Arauna — checkpoint 06A, Trainer Hill V1

**Arte e verificações de host concluídas sobre `d665dc34ddea776c06c85981653a9f62aa1e19d6`. Build ARM e revisão em emulador pendentes.** Sete mapas, com quatro andares gerados nas quatro modalidades originais. Entrega isolada e cumulativa para integração.

## Base recuperada e congelada

Antes da edição foram recuperados a Master Map Design Bible, os concepts e os checkpoints. A sequência integrada confirmada no GitHub é `802d01c341` (03C + 03B V1.1), `5d0b14e46e` (Dive), `a08835a98f6` (Safari) e `d665dc34dd` (manutenção de Petalburg/Oldale). O main consultado, `979fb6c1b6731561f3c993efd6045a9bbf096c54`, estava 88 commits atrás da base; não serve como base cumulativa.

A manutenção feita depois do Safari já estava na branch integradora ao iniciar este checkpoint. Foram preservados integralmente a borda de Petalburg e o código da animação da porta de Oldale. Também permanecem as 12 bordas Dive corrigidas, a boca/topo de Altering e a névoa leve integrada. Este checkpoint não remove bancos antigos nem executa a manutenção geral reservada ao usuário.

Referência visual: Bible, p. 16, e `05_Rota_111_Semiarido_Deserto_Serra.png`, presentes em `docs/referencias/bible_concepts_recuperados`. Não há prancha específica de Trainer Hill. A adaptação visual foi registrada em `TRAINER_HILL_06A_DIRECAO_VISUAL.md`; não confunde o equipamento de desafios com a Torre do Ruído da narrativa.

## Sete mapas concluídos

| Mapa | Dimensões | Células estáticas | Warps | Tratamento V1 |
|---|---:|---:|---:|---|
| TrainerHill_Entrance | 19×17 | 323 | 3 | Recepção de pedra clara, madeira e tecido oliva |
| TrainerHill_1F | 16×21 | 336 | 2 | Arenito claro e barreiras de pedra |
| TrainerHill_2F | 16×21 | 336 | 2 | Materiais dos desafios, conforme a modalidade |
| TrainerHill_3F | 16×21 | 336 | 2 | Piso ocre, madeira e pedra |
| TrainerHill_4F | 16×21 | 336 | 2 | Piso de ardósia e barreiras claras |
| TrainerHill_Roof | 25×16 | 400 | 2 | Cobertura escura, fachada de pedra e terraço claro |
| TrainerHill_Elevator | 5×7 | 35 | 2 | Cabine com piso de pedra e painéis de madeira |
| **Total** | | **2.102** | **15** | |

Os materiais pertencem aos metatiles; a disposição pode mudar entre Normal, Variety, Unique e Expert, como no jogo original. As prévias dos andares mostram os mapas efetivamente gerados, incluindo as 16 combinações, e não apenas o blockdata estático que o motor sobrescreve.

## Contrato funcional preservado

- Os sete `map.bin` e `border.bin`, dimensões, colisão e elevação são idênticos à base. Os 15 warps, sete objetos estáticos, textos, gatilhos, scripts, acesso pela Rota 111, movimentos do elevador e retornos permanecem originais.
- As 16 entradas de metatiles e colisão de `graphics/trainer_hill`, as 32 posições de treinadores e todos os dados dos desafios permanecem idênticos. A geração continua copiando as cinco primeiras linhas e gerando as 16×16 células inferiores.
- Os IDs dos quatro andares não mudam: `src/trainer_hill.c` os usa para identificar andar e estado. Flags de pós-jogo, modos, cronômetro, recordes, perdas, equipes, batalhas e prêmios não foram editados.
- As três tabelas globais de tilesets recebem apenas declarações aditivas. Seis layouts existentes trocam somente o par de bancos visuais. Um layout privado de elevador é acrescentado no final da tabela, sem deslocar nenhum ID anterior.
- O elevador antigo é compartilhado com Battle Tower. `LAYOUT_BATTLE_ELEVATOR` e a Battle Tower ficam intactos; somente `TrainerHill_Elevator/map.json` passa a apontar para o novo layout privado. Suas outras propriedades continuam idênticas.
- Os quatro bancos privados preservam **1.011 atributos completos de 16 bits**, incluindo comportamento, terreno e camadas. Mantêm os callbacks originais (`InitTilesetAnim_Building` nos primários e `NULL` nos secundários), os tiles reservados às animações e as paletas 7/9 das portas.
- As portas de elevador `0x32C`/`0x383` ficam visualmente nativas neste V1, inclusive seus pixels fechados e frames animados. Escadas, porta do balcão e pictogramas dos puzzles continuam com os IDs e a função original. Não foi introduzido hook de câmera ou lógica de gameplay.

O congelamento protege **18.105 arquivos de jogo e 183 dependências** por SHA-256. O contrato inclui os checkpoints cumulativos, fontes C, scripts, encontros, itens, bancos anteriores e correções já integradas.

## Verificações concluídas

- Seletor visual real compilado no host: **2.102 células estáticas**, **5.376 células dos 16 andares gerados**, **35.840 casos de fallback/limites** e **53.167 células das cavernas/Dive anteriores**.
- Geração real de Trainer Hill: **5.376 palavras** exatamente iguais às entradas originais, com **11.984 células de guarda** intactas; oito classificações de layout e 20 casos de ciclo do desafio.
- Os casos de ciclo cobrem início com dados de desafio validados/inválidos, retomada e saturação do cronômetro, estado do dono, prêmio incompleto, primeiro prêmio, repetição, bolsa cheia, recorde melhor/pior, derrota e estados especiais.
- Arte: 2.328 células de piso novo são transitáveis; 798 células de barreiras novas são bloqueadas. As 414 máscaras de camada arquitetônica foram preservadas. Contagens, referências, conversão 4bpp, paletas RGB555 e espaços de animação foram conferidos.
- O elevador da Battle Tower permanece igual em layout, dados, pixels e atributos nas suas 35 células.
- Auditoria oficial dos mapas: **8/8** grupos de falhas sem ocorrências. Variantes de layout anteriores: **9/9**, nenhuma divergência de comportamento. A composição inglesa oficial passou, assim como **95/95** gates de assets e **189/189** verificações do protagonista. A compilação ARM foi explicitamente omitida pelo script estático; o log acompanha o checkpoint.
- Instalador real exercitado em checkout isolado: corrupção, edições desconhecidas, base main atrasada, colisão em arquivo novo, rollback de falha na terceira escrita, instalação integral, idempotência, HEAD preservado, contratos, validador instalado e rebuild determinístico. Passaram **25/25** casos. Os resultados constam de `review/trainer_hill_06a/install_test.json` e do `INSTALL_TEST.json` na raiz do pacote.

As funções C são os corpos de produção, compilados com o compilador do host. Heap, despacho de scripts, bolsa, flags/save e VBlank são serviços explícitos de teste. Esta evidência não substitui uma sessão completa do interpretador de eventos, do motor de batalha ou do emulador.

## Entrega e reprodução

O ZIP contém payload com hashes, instalador protegido, patch binário e bundle Git com pré-requisito na base. Verifica tudo antes de escrever, cria backup, reverte falhas e reaplica sem novas escritas. Preserva HEAD e não publica no GitHub. Aplicar uma única alternativa indicada em `LEIA_ME.md`.

```sh
python3 tools/arauna_maps/build_trainer_hill_06a.py --base /checkout-limpo-d665dc34dd
python3 tools/arauna_maps/validate_trainer_hill_06a.py --base /checkout-limpo-d665dc34dd
python3 tools/arauna_maps/render_trainer_hill_06a.py --base /checkout-limpo-d665dc34dd
```

Prévias `TrainerHill_06A_Sete_Mapas.png`, `TrainerHill_06A_Dezesseis_Desafios.png` e `TrainerHill_06A_Cameras.png`: renderer nativo RGB555, sem atores; não são capturas de emulador. O concept gerado é apenas direção artística, não screenshot de ROM.

## Pendência de integração

O compilador ARM e mGBA não estão disponíveis neste ambiente. O integrador ainda precisa compilar e conferir no jogo: entrada pela Rota 111, portas fechadas/animadas, balcão antes/depois de iniciar, escadas, 16 desafios com os treinadores, cronômetro durante batalha/retomada, derrota, recorde e prêmio (incluindo bolsa cheia), cobertura, ida/volta de elevador e um retorno à Battle Tower. Conferir TV e demais animações com as novas paletas.

Após integrar este checkpoint, restam **92 mapas** deste inventário: Navel Rock (21), Bases Secretas (24) e Battle Frontier (47). Próxima etapa proposta: **06B, Navel Rock**, congelando a nova base e a dependência do cais antes da edição.
