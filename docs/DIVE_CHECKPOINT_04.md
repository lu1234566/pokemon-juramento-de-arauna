# Arauna — checkpoint 04, Dive V1

Base obrigatória: `802d01c3417a9384f8de54050c469e0c5de29399`.

Entrega concluída em produção: **12 mapas submersos**, a boca de Altering na Rota 103, a base da Mirage Tower e uma névoa mais leve nas salas finais de Terra/Marine. Scripts, eventos, warps, condições de Dive/emersão, palavras de mapa, colisões, elevação, encontros e itens permanecem iguais à instalação. As modificações de código se limitam a dois hooks de desenho, auditados contra o arquivo anterior completo.

## Recuperação e base instalada

A Bible e os concepts foram recuperados antes de editar; os 83 assets conferem com o ZIP anterior. A branch do GitHub `claude/pokemon-juramento-arauna-fhk6ah` aponta para a base pedida, 85 commits à frente de `main` (`979fb6c1b6`). Dos 185 arquivos de payload do 03C/V1.1, 184 coincidem integralmente com a instalação; a única diferença é o relatório ampliado pelo integrador. As correções extras da base — atributo de porta de Altering e console do Space Center — foram mantidas.

O integrador já registra build e mGBA do 03C/V1.1. Essa verificação histórica não é atribuída ao novo Dive. As grades corrigidas, os bancos anteriores e os pacotes cumulativos não foram reaplicados sobre a instalação. O contrato desta etapa inclui **17.906 arquivos de jogo** e **110 dependências** de arte, grades e referências.

**Divergência de inventário:** a Rota 107 não tem mapa Underwater, conexão Dive ou warp de mergulho nesta base. Os 12 slots reais incluem a Rota 134, M’Boi e Seafloor Cavern. A entrega usa esses 12 mapas existentes, sem criar uma ligação nova na Rota 107 ou retirar um acesso instalado para manter a contagem. A Rota 107 permanece preservada.

## Etapa concluída: 12 Dive

| Slot técnico | Dimensão | Células | Ambientação | Itens ocultos |
|---|---:|---:|---|---:|
| Underwater_Route105 | 40×80 | 3.200 | Sedimento costeiro e recife | 0 |
| Underwater_Route124 | 80×80 | 6.400 | Arquipélago, algas e pilares | 7 |
| Underwater_Route125 | 80×40 | 3.200 | Mar frio | 0 |
| Underwater_Route126 | 80×80 | 6.400 | Vestígios submersos de M’Boi | 8 |
| Underwater_Route127 | 80×80 | 6.400 | Canais oceânicos | 4 |
| Underwater_Route128 | 120×40 | 4.800 | Transição para a caverna de fundo | 2 |
| Underwater_Route129 | 80×40 | 3.200 | Oceano aberto e plataformas | 0 |
| Underwater_Route134 | 18×10 | 180 | Entrada do arquivo submerso | 0 |
| Underwater_SealedChamber | 22×48 | 1.056 | Corredor ancestral e inscrição | 0 |
| Underwater_MarineCave | 20×10 | 200 | Acesso à Marine, pedra fria | 0 |
| Underwater_SootopolisCity | 20×10 | 200 | Acesso a M’Boi | 0 |
| Underwater_SeafloorCavern | 14×9 | 126 | Submarino do Consórcio | 0 |

As **35.362 células** têm pixels novos e atributos completos equivalentes aos nativos. Foram usados seis bancos secundários privados, cada um com 512 tiles dentro da capacidade. Os 236 atributos originais de cada banco permanecem iguais. Algas animadas conservam os slots e o callback de Underwater. Os mapas de Navio Perdido, interiores de cavernas, Safari e Battle Frontier não foram redesenhados nesta etapa.

O complemento `DIVE_04_DIRECAO_VISUAL.md` documenta a adaptação da Bible e a distinção entre as seis famílias. As superfícies atuais continuam sendo a referência geométrica dos pontos de Dive; não foram criados pontos aleatórios para justificar a decoração.

## Retornos, entradas e itens preservados

- **16 warps** e **13 conexões**, incluindo sete conexões de emersão e seis conexões laterais submersas, continuam iguais.
- Os oito acessos temporários à Marine a partir de Underwater nas Rotas 105/125/127/129 mantêm condições e retorno dinâmico. A Rota 107 não participa dessa lógica instalada.
- Marine: `Underwater_MarineCave` mantém o retorno para `MAP_MARINE_CAVE_ENTRANCE, 10, 17`; a entrada da Marine conserva o Dive de volta para o acesso submerso.
- Sealed: o ponto `(12,44)` mantém o retorno para `MAP_SEALED_CHAMBER_OUTER_ROOM, 10,19`; os demais pontos preservam o retorno à Rota 134 em `(60,31)`. A inscrição continua em `(12,43)`.
- M’Boi: retorno fixo para `MAP_SOOTOPOLIS_CITY, 23,43`, sem mudar a entrada da cidade.
- Seafloor: retorno para `MAP_SEAFLOOR_CAVERN_ENTRANCE, 10,17`. As quatro posições de interação com o submarino, a flag de desaparecimento e as 12 substituições de metatile permanecem iguais.
- **21 itens ocultos:** mesmos itens, coordenadas, elevações e flags. JSON de encontros, espécies, níveis e taxas permanecem iguais. Scripts dos lendários, puzzles e progressão anterior estão no contrato imutável.

`review/dive_04/endpoints.json` lista os comandos fixos e as condições instaladas. O interpretador de scripts não foi emulado; seus bytes completos estão protegidos. O teste em host executa as funções reais de comportamento e despacho do Dive com uma fixture explícita para o callback de script.

## Etapa concluída: Altering e Mirage Tower

Altering: os IDs nativos `0x0A6` e `0x0A7`, escritos em `(45,5–6)` após `FLAG_SYS_GAME_CLEAR`, receberam arco de pedra e soleira. A posição do warp e todos os atributos permanecem iguais, incluindo `MB_NON_ANIMATED_DOOR` restaurado na base. A grade da Rota 103 V1.2 e suas colisões continuam intactas.

Mirage: os IDs `0x3F0–0x3F2` são usados por **363 células** do mapa, incluindo a base. Alterar sua arte globalmente desenharia pedaços de torre em terreno comum. A solução usa aliases somente em `(18–20,56)`, nos dois layouts da Rota 111. O seletor exige também o ID nativo esperado. Os IDs e atributos originais permanecem iguais, e o restante do terreno mantém seus pixels. A correção funciona na torre presente e no estado temporário antes da queda. Quando o script repõe areia, o seletor deixa de desenhar a base. Não houve alteração nas flags, layouts de estado, deslocamento do jogador ou código de desintegração.

## Resposta e mudança da névoa

A instalação do 03A confirmou em mGBA que `WEATHER_FOG_HORIZONTAL` herdada do Emerald encobria boa parte da arte nova. A solução desta etapa é **névoa leve, somente em TerraCave_End e MarineCave_End**. O alvo de mistura passa de `(12,8,3)` para `(4,16,3)`: a contribuição da névoa cai e o cenário conserva a intensidade de fundo. O último número é o atraso de transição, preservado.

Weather ID, textura e rolagem da névoa, sprites, ciclo de início/fim e scripts que retiram o clima após os encontros permanecem iguais. Outros mapas conservam `(12,8,3)` e o ramo de Underwater permanece `(4,16,0)`. A implementação real de `FogHorizontal_Main` passou por **1.056 casos de host** cobrindo os 528 mapas.

`Nevoa_Terra_Marine_Estudo.png` é um estudo dos coeficientes sobre assets nativos. Não reproduz a composição completa de sprites/paletas da ROM e não é captura de emulador. A legibilidade final precisa de confirmação em mGBA.

## Verificação concluída

- 17.906 arquivos de jogo e 110 dependências conferidos por SHA-256; todos os mapas, scripts, eventos, textos, flags, itens, encontros e bancos anteriores fora dos assets explicitamente corrigidos permaneceram iguais.
- 744 layouts: apenas os 12 campos `secondary_tileset` desta entrega mudaram; 732 layouts alheios permaneceram iguais.
- Código C real de câmera: **35.362 células novas**, **70.772 casos de fallback/limites** e **17.805 células dos 25 casos já instalados**, sem regressão.
- Código C real de Dive: **1.536 casos** de comportamento/despacho e **35.362 comparações** entre atributos de ID nativo e ID de desenho. O callback de script é uma fixture; os scripts originais são protegidos integralmente.
- **53 testes dos puzzles** usando as funções reais instaladas e o escritor nativo de metatiles; condições de Braille/Regis e encontros anteriores preservados.
- 12 células do estado “submarino ausente” verificadas no seletor real, com arte nativa opaca para os IDs de substituição.
- IDs e atributos de Altering; três aliases de Mirage nos dois layouts; fallback após a reposição de areia; pixels do terreno e gráficos usados anteriormente conferidos. As **5.600 células** do layout sem torre permanecem visualmente iguais à base.
- Serialização 4bpp, RGB555, paletas CRLF, capacidade, opacidade e slots de animação conferidos. A arte mantém algas animadas.
- Auditoria oficial de mapas: **8/8**; variantes de troca de layout: **9/9**; gates estáticos oficiais aprovados, incluindo **189/189** checks do protagonista.
- Prévia reproduzível com 24 mapas antes/depois, câmeras nativas, quatro estados de exteriores, estado do submarino e estudo da névoa. Sem sprites de personagens; renders de host, não emulador.

## Pacote, instalação e pendência

O pacote inclui instalador com preflight completo, backup, rollback, reaplicação idempotente, patch binário e bundle Git. **24/24 testes de instalação isolada passaram**, incluindo corrupção do payload, alterações locais em scripts/itens/encontros/grades/atributos, rejeição do main atrasado, rollback após falha na terceira escrita e reaplicação sem novas escritas. O checkout instalado também passou pelo validador real e pelo rebuild idempotente. `INSTALL_TEST.json` acompanha o resultado. O instalador não altera HEAD, não faz commit/push e recusa o main atrasado. A aplicação combina o Dive, as duas correções externas e a névoa; não reaplicar pacotes antigos depois dele.

**Pendência para o integrador: build ARM de ROM e testes em mGBA.** A toolchain ARM e mGBA não estão disponíveis neste ambiente. Conferir ida/volta pelos sete pares superfície/Dive, os oito acessos temporários à Marine, `(12,44)` de Sealed, os 21 itens, o submarino nos dois estados, Altering antes/depois do pós-jogo, Mirage presente/ausente/em queda e névoa com os lendários antes/depois do encontro. Confirmar as seis conexões laterais em câmera.

Código, arte, contratos e verificações de host concluídos. A instalação externa não é presumida. **Próxima etapa: Safari**, sobre a base resultante da integração, fechando este ciclo de cavernas/fundo do mar.

## Verificação na instalação

- O instalador foi aplicado sobre `802d01c341`. A árvore resultante é
  idêntica à do bundle `6e6139e5fd`.
- Build `en` ok (ROM em 57,7%). Gates aprovados: 189/189, 95/95, 0
  candidatos de resíduo, as oito verificações de mapas e
  `variantes_troca_layout.py --verificar` 9/9. Nenhum símbolo de harness
  na ROM.
- Legibilidade na visão de câmera: 0 paredes com desenho de piso nos 12
  mapas. Na Rota 127 eram 2.508.
- Emulador:
  - Fotos nos 12 mapas submersos.
  - A travessia 127↔128 chega com VRAM e paletas iguais ao carregamento
    direto.
  - As fronteiras 124↔126 e 126↔127 não têm casa atravessável e ficam fora
    da câmera a partir das casas andáveis.
  - A boca da Altering com `FLAG_SYS_GAME_CLEAR` deixa entrar a pé.
  - Mirage Tower nos três estados, com o harness ajustando
    `VAR_MIRAGE_TOWER_STATE`: presente, ausente (2) e temporário (1).
  - Névoa leve nas duas salas finais, comparada com as fotos do 03A.

### Correções na instalação

- **Topo da boca da Altering.** O arco foi desenhado no `0x0A6`, mas o
  script da Rota 103 põe `General_CaveEntrance_Top` (`0x09F`) em (45,5).
  Essa casa continuava preta. A definição do `0x0A6` foi copiada para o
  `0x09F` no banco `arauna_border_route103_uivo_v1`. Os dois IDs têm o
  atributo 0 e nenhuma casa da grade usa nenhum deles.
- **Borda dos 12 mapas submersos.** O `border.bin` usava o `0x213`, que nos
  bancos novos desenha piso claro. Nos mapas pequenos (Marine Cave, M'Boi,
  Rota 134, Seafloor) aparecia uma faixa clara fora do mapa. A borda agora
  usa a rocha lisa que preenche as rotas de cada banco: `0x2FE` em Mare,
  `0x2FC` em Arquipélago e `0x2F3` em Arquivo, Horizonte, Oceano e Costa.
- **Efeito no validador do autor.** `validate_dive_04.py` recusa as duas
  correções: a lista de IDs permitidos da Altering tem `0x0A6` em vez de
  `0x09F`, e os `border.bin` estão no contrato protegido. Uma cópia local que
  permite só essas duas mudanças aprova todo o resto.
