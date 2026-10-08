# Arauna — Checkpoint 03C + 03B V1.1

Base obrigatória: `4410ced6384b1d71dfa562d4bb5a2486ebc01e22`.

Entrega conjunta: os três mapas de Altering/Artisan Cave e a V1.1 visual das quatro salas do 03B. Nenhum arquivo de gameplay, evento, encontro, script, warp, flag ou texto foi modificado. Os IDs nativos e os atributos completos das peças de porta, saída e inscrição foram preservados; a V1.1 modifica sua arte, como solicitado.

## Recuperação e comparação com o GitHub

A Bible, os 82 concepts e o checkpoint 03B foram recuperados antes da geração dos assets. Os 83 arquivos de referência conferem por SHA-256. A branch do GitHub `claude/pokemon-juramento-arauna-fhk6ah` aponta para a base indicada, 84 commits à frente de `main` (`979fb6c1b6`).

Dos 125 arquivos do pacote 03B anterior, 121 coincidem com a instalação. As quatro diferenças são o relatório ampliado pelo integrador e três grades visuais que restauram nove células de saída ao ID nativo. Essa instalação corrigida é a base deste pacote. O integrador registra build e mGBA do 03B: passagem pelas portas abertas e retorno pelas saídas. Essa validação histórica não é atribuída ao novo 03C/V1.1.

As auditorias cumulativas de Sul/Pampa, Uivo, Rota 103 V1.2 e 03A/03B foram mantidas. O contrato funcional do 03B anterior continua íntegro na base. Nenhum overlay antigo foi reaplicado sobre o GitHub instalado.

## Etapa concluída: 03C

| Mapa | Dimensão | Células redesenhadas | Warps | Objetos / itens ocultos |
|---|---:|---:|---:|---:|
| AlteringCave | 32×24 | 768 | 1 | 0 / 0 |
| ArtisanCave_B1F | 46×54 | 2.484 | 2 | 1 / 4 |
| ArtisanCave_1F | 21×22 | 462 | 2 | 1 / 0 |

Altering recebeu rocha fria em cinza violeta e piso mineral claro. Artisan recebeu estratos de pedra cinza, veios ocres e depósitos discretos de pigmento. Os dois pisos compartilham a mesma identidade e preservam a ligação por escadas. Faces de rocha, massas escuras, patamares andáveis, escadas e saídas têm desenho próprio. O atlas mineral nativo do 03A foi reutilizado e convertido determinísticamente; o suplemento de direção está em `CAVERNAS_03C_03B_V11_DESIGN.md`.

As 3.714 palavras nativas de mapa, bordas, dimensões e posições permanecem idênticas. A ligação de Altering com Rota 103, as ligações de Artisan com Battle Frontier, os itens e os quatro itens ocultos não mudaram. Não houve expansão do Battle Frontier.

As nove tabelas de Altering preservam espécies, níveis e taxas. A função real de seleção foi executada em host: variantes 0–8, valores fora do limite retornando à tabela 0 e seleção independente dos dois mapas de Artisan. O script de Mystery Gift e `VAR_ALTERING_CAVE_WILD_SET` permanecem intactos.

## Etapa concluída: 03B V1.1

Saídas, portas e inscrições usam a pedra do novo cenário: arcos minerais, placas escuras com traços claros e saídas com abertura iluminada. A geometria dos traços de inscrição foi extraída das peças instaladas e comparada com os tiles novos; a fonte e as 22 mensagens Braille não mudaram. Não foram acrescentados símbolos ornamentais ou novas condições de puzzle.

Cada banco da V1.1 preserva **todos os atributos de metatile**, não apenas os dos blocos usados pelos scripts. Os IDs `0x229`, `0x22A–0x22C`, `0x232–0x237` e `0x207` continuam os mesmos. As saídas usam `0x258–0x25A` em Ancient/Island e `0x2E5–0x2E7` na sala interna de Sealed Chamber. Os 14 IDs de landmark de cada banco recebem a arte nova; as demais entradas de metatile e paletas continuam iguais às instaladas.

As nove casas corrigidas pelo integrador permanecem nativas: `(9–11,20)` na Sealed Chamber interna e `(7–9,12)` em Ancient Tomb e Island Cave. Também foram restauradas visualmente seis casas das **saídas externas**, `(7–9,30)` em Ancient/Island, que ainda recebiam um alias de parede. A mudança nesses seis pontos é somente no desenho: palavras de mapa, atributos, colisões, elevação e warps permanecem intactos. As grades históricas do 03B foram preservadas; quatro cópias novas são usadas pela V1.1, com somente essas seis diferenças de ID de desenho.

A comparação com a base instalada registra 93 células com pixels alterados no 03B: 34 na sala externa, 13 na interna e 23 em cada caverna dos golens. As portas foram renderizadas e verificadas nos estados fechado e aberto. Dig, Flash, Wailord primeiro/Relicanth por último, flags, as 36 casas da volta de Regice e os resultados dos encontros lendários permanecem iguais.

## Verificação concluída

- **17.833 arquivos de jogo preexistentes** e **23 dependências de arte/grades** conferidos por SHA-256. Os bancos antigos, a fonte e os scripts permanecem intactos.
- 744 layouts: somente os sete campos `secondary_tileset` desta entrega mudaram; 737 layouts alheios permanecem iguais.
- Seletor C de produção: **5.802 células**, **17.434 casos de fallback e limites** e **14.091 células de casos já instalados**. Nos casos do 03B, as seis novas saídas são explicitamente permitidas; os demais IDs de desenho coincidem com a instalação.
- **53 testes dos puzzles**, executando corpos reais das funções de `braille_puzzles.c` e do escritor de `fieldmap.c`, com stubs de áudio/tarefas/acesso à equipe. O interpretador de scripts não foi emulado; suas ramificações são protegidas por comparação integral dos arquivos.
- **19 testes** executando a função real `GetCurrentMapWildMonHeaderId` sobre a ordem das tabelas do JSON instalado.
- 36 verificações das peças de portas fechadas/abertas, 29 verificações de warps/peças de saída e oito comparações dos traços de inscrição.
- Cinco bancos privados de **432 tiles gráficos**, dentro da capacidade de 512. Metatiles, serialização 4bpp, cores RGB555, paletas 0–12, opacidade e slots de animação conferidos. Não houve mudança no código do motor.
- Auditoria oficial de mapas: **8/8** checks em 528 mapas. Gates estáticos oficiais aprovados, incluindo **189/189** checks do protagonista.
- Prévia reproduzível: sete mapas integrais, 21 pares antes/depois em 240×160, três pares de porta e três comparações de saída. A coluna “antes” do 03B usa a grade corrigida da base. São renders de host com tiles e seletor C reais, sem sprites, não screenshots de emulador.

## Instalação e limite

O pacote contém instalador com preflight completo, proteção contra base/alterações locais desconhecidas, backup, rollback e reaplicação idempotente, além de patch binário, bundle Git, código reprodutível e prévias. **21/21 testes do instalador passaram**, incluindo alterações locais em scripts/Braille/encontros/grades corrigidas, corrupção do payload, rejeição do main atrasado, rollback após falha na terceira escrita, instalação integral e reaplicação sem novas escritas. O resultado acompanha a entrega em `INSTALL_TEST.json`. A instalação não faz commit nem push e aplica conjuntamente 03C + 03B V1.1.

**Compilação ARM de ROM e validação em mGBA deste pacote ficam pendentes para o integrador:** essas ferramentas não estão disponíveis neste ambiente. Confirmar em câmera as escadas de Artisan, as saídas internas e externas do 03B, os estados das três portas, as inscrições e o acesso a Altering pela Rota 103. As checks de host não substituem esse teste runtime.

Produção, contratos, verificações de host e pacote estão concluídos. A instalação externa não é presumida. As próximas etapas são os **12 mapas Dive** e o **Safari**, em checkpoints próprios, sobre a base resultante da integração.

## Verificação na instalação

- O instalador foi aplicado sobre `4410ced638`. A árvore resultante é
  idêntica à do bundle `eaee97a921`. `validate_cavernas_03c.py` aprovou e
  regenerou um `validation.json` igual ao entregue.
- Build `en` ok (ROM em 57,2%). Gates aprovados: 189/189, 95/95, 0
  candidatos de resíduo, as oito verificações de mapas e
  `variantes_troca_layout.py --verificar` 9/9. Nenhum símbolo de harness
  na ROM.
- Legibilidade na visão de câmera:
  - Altering e Artisan tinham no Emerald 353, 657 e 223 paredes com o mesmo
    desenho de um piso andável. Agora são 0.
  - As 14 fronteiras de elevação bloqueante da Artisan B1F têm desenhos
    diferentes dos dois lados.
  - As quatro salas do 03B continuam com 0.
- Emulador:
  - Fotos nos três mapas novos.
  - Portas do 03B fechadas e abertas com as flags dos puzzles; inscrições.
  - Testes a pé:
    - saídas internas e externas;
    - escadas 1F↔B1F da Artisan;
    - saída da Artisan para a Battle Frontier;
    - saída da Altering para a Rota 103.

### Bugs antigos achados na instalação e corrigidos

Uma varredura comparou, mapa a mapa, o atributo de cada metatile colocado
por script com o do tileset original do Emerald (255 casos). Ela achou:

- **Altering Cave inacessível no pós-jogo.** Com `FLAG_SYS_GAME_CLEAR`, a
  Rota 103 coloca a boca da caverna em (45,5–6). Desde os bancos privados
  da Rota 103 (V2, Sul e Uivo), o `0x0A7` (`General_CaveEntrance_Bottom`)
  tinha comportamento `MB_NORMAL` em vez de `MB_NON_ANIMATED_DOOR`, e não
  se entrava na caverna. O atributo foi restaurado no banco
  `arauna_border_route103_uivo_v1`, onde nenhuma casa da grade usa esse ID.
  No mGBA, o jogador agora entra na caverna a pé.
- **Quadrado preto no Space Center de Mossdeep (1º andar).** Enquanto
  `VAR_MOSSDEEP_CITY_STATE` ≤ 2, o script punha `Facility_DataPad` (0x3E4),
  que não existe no banco das Missões do Céu (205 metatiles), e desenhava
  um quadrado preto. Esta versão do mapa não tem o evento de leitura da
  nota. O script agora põe o canto do console que já está ali (0x216).

Pendências registradas sem mudança:

- A boca da Altering na Rota 103 é um retângulo preto liso; falta arte de
  caverna no banco da rota.
- As peças 0x3F0–0x3F2 da Mirage Tower temporária da Rota 111 são terreno
  comum no desenho atual, com 363 casas. A base da torre aparece como chão
  durante esse estado.
- Os livros e as caixas da mudança em Littleroot e o topo da caverna
  vermelha da Rota 114 diferem só no tipo de camada, sem efeito de jogo.
