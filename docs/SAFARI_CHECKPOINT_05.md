# Pokémon Juramento de Arauna — checkpoint 05, Safari V1

**Produção e verificações de host concluídas sobre `5d0b14e46e98f099ef4807af71d5e9be60f88d66`.** O checkpoint inclui os seis setores externos do Safari, a casa de descanso e a recepção na Rota 121. Fecha a entrega artística deste ciclo de cavernas e fundo do mar para integração. A rodada de manutenção posterior foi reservada ao usuário.

## Recuperação e base cumulativa

Antes de editar, foram recuperados a Master Map Design Bible, os 82 concepts, o ZIP do Dive 04 e seu último relatório. Os 83 assets de referência correspondem byte a byte aos arquivos integrados. O ZIP anterior tem SHA-256 `27d371f23ddfcdb102e799723e79266628d00e019ba133b30c308187c9c3599a`.

A branch de integração do GitHub contém `5d0b14e46e`, **86 commits à frente de `main`**, que permanece em `979fb6c1b6731561f3c993efd6045a9bbf096c54`. A comparação foi feita contra o bundle anterior, não somente contra main. A base mantém o Dive instalado, com duas correções do integrador: os 12 `border.bin` submersos agora usam rocha, e o topo de Altering é desenhado no ID realmente escrito pelo script, `0x09F`. Essas correções e a névoa leve permanecem intactas.

O relatório da integração anterior documenta build ARM, fotos em mGBA dos 12 mapas, travessias e revisão da névoa. São evidências do integrador sobre o Dive; não são testes desta entrega do Safari. O validador histórico do Dive usa o contrato anterior a essas correções e pode recusá-las. Esta etapa não altera esse validador; seu contrato parte da base corrigida `5d0b14e46e`.

## Etapa concluída: Safari e dependências visuais

| Mapa nativo | Dimensão | Células | Papel visual |
| --- | --- | ---: | --- |
| SafariZone_Northwest | 40×40 | 1.600 | Platôs e lago |
| SafariZone_North | 40×40 | 1.600 | Encosta e comedouros |
| SafariZone_Northeast | 40×40 | 1.600 | Mata da expansão |
| SafariZone_Southwest | 40×40 | 1.600 | Margem e pouso |
| SafariZone_South | 40×40 | 1.600 | Entrada e trilha principal |
| SafariZone_Southeast | 40×40 | 1.600 | Lagos e capinzal |
| SafariZone_RestHouse | 10×9 | 90 | Pouso de madeira |
| Route121_SafariZoneEntrance | 18×14 | 252 | Recepção da Rota 121 |

São **9.942 células**, **8 warps**, **14 conexões direcionadas**, **39 objetos**, **5 itens visíveis e 4 ocultos**. As coordenadas, flags, níveis, encontros e taxas originais foram preservados. A entrada externa do edifício na própria Rota 121 continua igual à base; a arte da recepção interna é parte desta entrega.

As referências e a interpretação artística estão em `SAFARI_05_DIRECAO_VISUAL.md`. Não há novo nome de lugar, texto, quest ou lore. A geometria herdada permite variar a composição entre lago, encosta, trilha e capinzal sem deslocar gatilhos ou criar bloqueios.

Foram criados três pares de bancos privados: Mata, Pouso e Recepção. O primeiro é compartilhado apenas pelos seis setores externos. Os metatiles mantêm os **mesmos IDs e os 1.680 atributos completos originais**. Os gráficos estáticos foram remanejados dentro dos bancos novos, com exclusão dos slots de animação. Nenhum alias novo de câmera nem hook de motor foi necessário. Os bancos originais de General/Lilycove, Building/GenericBuilding e recepção Arauna permanecem byte-idênticos.

No registro dos 744 layouts, apenas os dois campos de banco dos oito alvos mudam; os outros 736 layouts são iguais. As três declarações de tilesets recebem blocos aditivos. Esses quatro arquivos são os únicos arquivos preexistentes alterados. Nenhum `map.bin`, `border.bin`, JSON de mapa, script, texto, código C de jogo ou sprite foi modificado.

## Mecânicas preservadas

- Entrada: caixa de Pokéblocks, espaço de armazenamento e taxa de 500 continuam nos mesmos scripts; há 30 Safari Balls e 500 passos por sessão.
- Encerramento: saída voluntária, desistência, tempo esgotado e bolas esgotadas mantêm os comandos e retorno à recepção em `(2,5)`.
- A chegada ao Sul conserva o warp em `(32,33)`, o passo do jogador e os deslocamentos do atendente. O percurso entre o balcão e a entrada permanece igual.
- Comedouros: mesmos comportamentos e casas; dez entradas na estrutura nativa, duração de 100 passos e consulta por mapa e distância preservadas.
- Acro Bike, Mach Bike, degraus, trilhos, rampas, Surf, pesca e Rock Smash conservam a grade, os atributos e o código originais.
- As flags dos trabalhadores e da expansão pós-jogo permanecem iguais, assim como os textos e encontros de todos os setores.
- Braille, Regis, lendários, entradas temporárias de Terra/Marine, Dive, submarino, Altering, Mirage e a névoa são protegidos pelo contrato cumulativo desta base.

## Etapa concluída: verificação

`review/safari_05/functional_contract.json` protege **18.010 arquivos de jogo e 183 dependências**, incluindo todas as grades anteriores usadas pela câmera, arte e referências. `validation.json` registra:

- 9.942 células de câmera conferidas com os seletores C reais de bordas e cavernas; 40.960 casos de IDs/limites retornam o ID nativo.
- 53.167 células dos seletores anteriores de cavernas e Dive permanecem iguais.
- As quatro funções C reais de cópia de conexões conferem as 14 direções, com **4.080 células de cache**. Há zero divergências de pixels/atributos e **32.640 comparações de células/fases**, em oito fases de animação.
- 18 casos executam funções reais do Safari: sessão de 500 passos, duração de 100 passos dos comedouros, ativação, capacidade, mapa/distância, desistência, saída e ramos de bolas esgotadas após a batalha.
- 1.792 casos executam os predicados reais de terreno para capim, rampa, trilhos e comedouro; 3.423 comparações conferem esses predicados nos IDs usados. Os atributos completos também são iguais, incluindo água e camadas.
- As 20 metatiles com animação visível continuam animadas. Uma referência dinâmica nativa sem mudança visível é preservada e registrada separadamente. Os destinos de animação não recebem novos tiles estáticos.
- Capacidade de tiles/metatiles, índices PNG 4bpp, roundtrip dos nibbles GBA, RGB555, CRLF de paletas, opacidade da arte nova e callbacks originais conferidos.
- A arte de campo/trilha só ocupa casas livres; as copas só ocupam casas bloqueadas. As silhuetas, máscaras, espelhamentos e camadas herdadas dos demais IDs foram conferidas independentemente do remanejamento dos gráficos. As duas casas de salto `0xD6` mantêm sua borda, e a água rasa distingue-se dos lagos de Surf.
- Auditoria oficial de mapas **8/8**, variantes de layout **9/9**, gates oficiais **95/95** e protagonista **189/189** aprovados. A composição inglesa oficial também foi conferida; a etapa de compilação ARM foi explicitamente omitida pelo script estático. O log acompanha a entrega.

As fixtures C substituem os serviços de flag/script/callback/warp, sem executar o interpretador de scripts nem a engine completa de batalha. Os arquivos completos desses sistemas estão protegidos por SHA-256. Nenhuma sessão de ROM foi executada neste ambiente.

## Etapa concluída: pacote e instalação

O ZIP inclui payload com hashes, instalador protegido, patch binário, bundle Git, relatório, prévias e evidências. O instalador exige a base indicada ou o checkpoint fornecido; verifica tudo antes da primeira escrita, cria backup, reverte falhas e reaplica sem novas escritas. Preserva HEAD e não publica no GitHub. Passaram **24/24 testes de instalação isolada**, incluindo corrupção, alterações locais, main atrasado, rollback após falha na terceira escrita, reaplicação sem backup novo, validador C instalado e rebuild determinístico. `INSTALL_TEST.json` registra os casos.

Use o pacote apenas sobre `5d0b14e46e` ou seu checkpoint. Não reaplique os ZIPs anteriores sobre esta etapa e não use main como base cumulativa.

## Pendência do integrador e próxima responsabilidade

**Build ARM e revisão em mGBA do Safari permanecem pendentes.** O compilador ARM, pkg-config e mGBA não estão disponíveis aqui. Conferir os oito acessos/retornos, passagem pelas 14 conexões, contador de passos, 30 bolas, desistência e esgotamento de bolas, comedouros após 100 passos, Acro/Mach Bike, Surf/pesca, Rock Smash, nove itens e os bloqueios antes/depois da expansão. Conferir portas, NPCs e efeitos de capim sobre as paletas novas.

A produção e as verificações de host desta etapa estão concluídas; a integração externa não é presumida. Após a instalação, a rodada de manutenção fica com o usuário, conforme solicitado.

## Verificação na instalação

- O instalador foi aplicado sobre `5d0b14e46e`. A árvore resultante é
  idêntica à do bundle `7b2b31533c`. `validate_safari_05.py` aprovou e
  regenerou um `validation.json` igual ao entregue.
- Build `en` ok (ROM em 57,8%). Gates aprovados: 189/189, 95/95, 0
  candidatos de resíduo, as oito verificações de mapas e
  `variantes_troca_layout.py --verificar` 9/9. Nenhum símbolo de harness
  na ROM.
- A varredura dos metatiles colocados por script não mudou: 255
  verificados, e as dez diferenças conhecidas são só de camada ou da Mirage
  Tower.
- Legibilidade: nenhuma parede com desenho de piso ou de capim de encontro
  nos seis setores. A recepção mantém as mesmas 6/7 casas ambíguas do
  Emerald.
- Emulador:
  - Fotos nos oito mapas.
  - A pé, funcionam a recepção pela Rota 121 e a casa de descanso, ida e
    volta.
  - 13 das 14 passagens entre setores chegam com VRAM e paletas iguais ao
    carregamento direto. Southwest→Northwest não tem casa atravessável
    nesse sentido; o sentido inverso passa.
  - A animação da porta da casa de descanso é idêntica à da base, inclusive
    o reflexo claro à esquerda.
  - Os reflexos de nuvem nos lagos vêm do clima `WEATHER_SUNNY_CLOUDS`,
    igual à base.
- O banco antigo `gTileset_AraunaRotaSafariV1` ficou sem uso. O
  `AraunaRotaBaseV1` continua usado por 20 interiores de rota.
