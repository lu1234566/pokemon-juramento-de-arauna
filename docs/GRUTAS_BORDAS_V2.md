# Grutas V2 e bordas prioritárias — entrega incremental

Base obrigatória: `73312e48f3542a78377024913fcaf44da5e771c0`, branch `claude/pokemon-juramento-arauna-fhk6ah`.

## Conteúdo

Victory Road 1F, B1F e B2F; Seafloor Cavern Entrance e Room1–Room9; ajuste do piso da casa da Lanette; os cinco pares de borda pedidos, nos dois sentidos. Os ajustes V1.1 dos demais Interiores de Rota já pertencem à base instalada e foram preservados.

Na Victory Road, a folha de faixa ocre fornece o penhasco com topo, face vertical e base. Há faces de uma e duas células de altura, bandas ocres e contornos laterais; as massas de rocha fechadas usam uma superfície superior. O Seafloor usa a folha de basalto, com faces escuras e topo claro. As margens recebem uma transição de piso seco, piso molhado e espuma sobre a água animada. O desenho das correntezas continua indicando a direção original.

Na casa da Lanette, todas as células livres de colisão usam o mesmo piso de madeira, exceto a saída marcada. Os objetos bloqueados continuam visíveis e com os mesmos atributos. A mudança não libera paredes nem reposiciona móveis ou eventos.

## Como funciona

As grades `map.bin` e `border.bin`, eventos, encontros, scripts e conexões permanecem byte a byte iguais à base. A ordem dos 737 layouts não muda. Não há migração nova de save: os IDs armazenados continuam nativos da V1. A conversão de saves anterior das Grutas V1 permanece intacta.

Os penhascos, margens e o piso da Lanette usam aliases apenas na câmera. Cada alias tem o mesmo atributo completo da célula nativa; a grade visual fica em `review/grutas_bordas_v2/visual_grids`. Se um script muda o ID da célula, a câmera volta ao ID nativo, preservando os quebra-cabeças. A camada inferior dos aliases é opaca e os objetos estão na camada superior.

Nas bordas, oito mapas recebem pares de bancos próprios. Dez retângulos, delimitados pelas funções Fill* do motor, usam o mecanismo de `src/arauna_border_visuals.c`. A cor do vizinho é importada exatamente, sem quantização adicional. Os bancos são compactados e as paletas são empacotadas sem alterar o desenho próprio dos mapas. Os IDs usados no mapa, nos scripts e no cache dos vizinhos ficam reservados antes da criação de aliases.

A câmera consulta o tipo de camada do alias visual. As rotinas de colisão e comportamento continuam consultando o ID nativo. Isso permite desenhar um vizinho de outro banco sem usar um tipo de camada errado. As travessias recarregam os bancos e paletas pelo mecanismo já existente.

A alocação estática exclui 432–511 e 992–1023 e os intervalos específicos dos callbacks de flores. A água usa os slots reservados para sua animação original; nenhuma arte estática nova ocupa esses intervalos. Só as paletas 0–12 são referenciadas. Os novos PNGs são indexados de 4 bits e as paletas físicas do pacote usam CRLF.

A cor de fundo de índice zero e as paletas fixas das animações de porta foram preservadas. O tratamento especial de Cut do banco Início também reconhece o primário privado da Rota 103. Os IDs produzidos por scripts e por Cut estão incluídos na verificação visual.

## Resultado das bordas

Comparação RGBA exata, sintetizando os gráficos reais da água na VRAM. “Antes” usa a base 73312e48f3. “Depois” usa o seletor C real compilado no host. O total desta tabela não é diretamente comparável ao antigo limiar de diferença RGB maior que 48.

| Direção | Células da faixa | Diferentes antes | Diferentes depois |
|---|---:|---:|---:|
| MauvilleCity → Route110 | 280 | 278 | 0 |
| Route110 → MauvilleCity | 343 | 325 | 0 |
| Route110 → SlateportCity | 329 | 329 | 0 |
| Route110 → Route103 | 154 | 126 | 0 |
| Route126 → Route124 | 560 | 554 | 0 |
| SlateportCity → Route110 | 280 | 280 | 0 |
| EverGrandeCity → Route128 | 280 | 268 | 0 |
| Route128 → EverGrandeCity | 376 | 231 | 0 |
| Route124 → Route126 | 560 | 544 | 0 |
| Route103 → Route110 | 288 | 258 | 0 |

Nas dez direções, 3.193 células que diferiam passam a coincidir com o vizinho. Nenhuma das outras 124 direções mudou. Isso resolve estes cinco pares; não resolve todas as bordas do jogo.

`borders_static_audit.json` mantém a auditoria histórica por PNG estático e limiar 48, explicitamente sem sintetizar a VRAM. Para aceitar esta entrega, use `validation.json`, que compara os oito quadros da animação e não confunde os placeholders estáticos com a água em execução.

## Verificações

- Build ARM moderno em inglês: aprovado; ROM ocupa 17.679.524 bytes antes do preenchimento a 32 MiB.
- Gates: 189/189 de protagonista; 95/95 de paletas e layouts; auditoria de resíduos com zero candidatos.
- Auditoria de mapas: as oito verificações passam.
- 2.471 arquivos de mapas, grades, scripts e código de animação conferidos sem alteração; ordem dos layouts preservada.
- Seletor da câmera e funções Fill* reais compilados: 40.512 células de 134 conexões conferidas; 27.600 comparações adicionais dos oito quadros nas faixas prioritárias.
- 56.687 verificações de fallback de escopo e de células alteradas por script; 5.812 células com alias nas grutas e na Lanette, com atributos preservados e camada inferior opaca.
- Construtores reproduzem 346 arquivos byte a byte.
- ROM compilada: 20 bancos nativos, 14 grades visuais, 10 tabelas de aliases e 32 quadros de animação conferidos contra os arquivos-fonte.
- mGBA 0.10.2: 61 capturas/casos únicos; os 13 mapas e Lanette carregados; travessia da escada 1F→B1F; água alterando bytes na VRAM; dez travessias de borda aprovadas, incluindo os pares marítimos com Surf. Nenhum opcode ilegal registrado.
- Validador da borda 119/118 continua passando; as novas direções têm validador separado para incluir animações.

SHA-256 da ROM verificada: `b8460e9e2d299ef75a18eda08597335f3fd9e8357eecb956ff7e9a35d41d1231`. A ROM não é distribuída. Não há harness nos símbolos da ROM final.

## Capturas e limites

As cinco pranchas em `review/grutas_bordas_v2/boards` mostram os 14 mapas, comparações V1/V2 e os dez sentidos de borda. Os PNGs de 240×160 estão em `mgba`. As pranchas só ampliam os pixels sem suavização. As comparações usam a mesma posição inicial; as posições dos testes de travessia e dos detalhes visuais podem ser diferentes e estão registradas em `emulator.json`.

As capturas carregam o mapa pelo fluxo nativo, com um hook temporário apenas na memória do mGBA. O hook é removido antes das verificações; a ROM em disco não é modificada. Para enxergar a arte das cavernas, a revisão usa iluminação completa por Flash. Nenhum hook, ROM, ELF, save ou estado de emulador acompanha o ZIP.

Não foi concluída uma campanha completa nem todos os quebra-cabeças. Não foi importado um save histórico real nesta rodada; a compatibilidade da V2 se apoia na preservação das grades, IDs, layout order e atributos, além do fallback para alterações de script. As paredes mantêm a geometria de colisão da V1, portanto a altura visual é obtida dentro das células bloqueadas existentes.

## Reproduzir

Dependências: Python 3, Pillow, compilador C do host; toolchain ARM/newlib/libpng para o build normal do projeto; mGBA para a inspeção manual.

Crie uma cópia limpa da base, separada da árvore já instalada:

```sh
git worktree add --detach ../arauna-base-73312 73312e48f3542a78377024913fcaf44da5e771c0
python3 tools/arauna_maps/build_grutas_v2.py --base ../arauna-base-73312
python3 tools/arauna_maps/build_border_priority_v2.py --base ../arauna-base-73312
python3 tools/arauna_maps/validate_grutas_bordas_v2.py --base ../arauna-base-73312
python3 tools/arauna_maps/validate_border_visuals_119_118.py --base ../arauna-base-73312
bash scripts/check_arauna_static.sh
python3 tools/arauna/audit_map_data.py
bash scripts/build_arauna.sh en -j4
python3 tools/arauna_maps/validate_rom_visuals_v2.py --rom pokemon-juramento-de-arauna-en_modern.gba --elf pokemon-juramento-de-arauna-en_modern.elf
```

Render estático de um mapa com aliases:

```sh
python3 tools/arauna_maps/render_visuals_v2.py VictoryRoad_1F /tmp/victory-v2.png
```

Para revisar no mGBA, compile sua ROM, carregue-a e visite as posições registradas em `emulator.json`. Os scripts de captura privados não são parte do patch. Os registros de validação e os construtores permitem conferir os dados do jogo sem depender dessas capturas.

## Verificação na instalação

- Aplicado sem conflito sobre `73312e48f3`; `make MODERN=1` ok; 189/189,
  95/95, 0 candidatos de resíduo e as oito verificações de mapas aprovadas.
- `validate_grutas_bordas_v2.py` e `validate_border_visuals_119_118.py`
  aprovados em worktree limpa.
- Índices de `sCaveVisualGrids` conferidos: são 0-based em `gMapLayouts`,
  que o jogo acessa como `gMapLayouts[id - 1]`.
- Os oito mapas que trocaram de banco (Slateport, Mauville, Ever Grande e
  Rotas 103, 110, 124, 126 e 128) têm render próprio, atributos e callbacks
  de animação idênticos aos anteriores, inclusive nos IDs usados por
  scripts.
- Emulador:
  - As oito travessias a pé testáveis (110↔Mauville, 110↔Slateport,
    110↔103, 124↔126) chegam com VRAM e paletas iguais ao carregamento
    direto. Ever Grande ↔ Rota 128 é só por mar.
  - Fotos antes/depois das faixas de borda e das grutas V1/V2.
