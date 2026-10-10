# Integração do checkpoint 08A (revisão de ambientação)

O bundle `6b974ba33e` entrou por fast-forward sobre `a594b3e1e6`. O
checkpoint traz um relatório, um inventário, renders, um contrato de
proteção e um roteiro de aceitação. Nenhum arquivo do jogo mudou, e nenhuma
correção foi necessária.

Conferência:

- **Pacote.** O bundle passa em `git bundle verify` e o commit só acrescenta
  arquivos. Os 42 arquivos do manifesto batem com o commit e com a pasta
  `source` do ZIP.
- **Auditoria reproduzida.** `audit_brazil_08.py` reescreve inventário,
  renders, montagens e roteiro byte a byte iguais aos do pacote. O
  resultado é 528 mapas: 477 com banco Arauna, 16 módulos da Pyramid, 8
  inativos e 27 nativos.
- **Os 27 nativos.** Nenhum deles aparece em `arauna_border_visuals.c`,
  `arauna_cave_visuals.c` ou nas tabelas de `src/data/arauna_*`, então
  nenhum é trocado em tempo de execução.
- **Mapa regional.** Desde o Emerald original, só os nomes em
  `region_map_sections.json` mudaram. Os gráficos do PokéNav e do Pokédex
  continuam os de Hoenn.
- **Proteção.** `check_visual_protection_08.py` passa nos oito arquivos.
- **Build e gates.** A ROM compila e é byte a byte igual à de `a594b3e1e6`.
  Todos os gates passam, e não há símbolo do harness na ROM.
- **`main`.** `main` está em `979fb6c1b6`, 114 commits atrás desta branch.

## Aceitação do Frontier

O relatório diz que o ambiente do autor não tinha mGBA, compilador ARM nem
ROM. Este ambiente tem os três: as integrações 07A–07I compilaram a ROM e
fotografaram os mapas no mGBA 0.10.2.

Essas fotos não são a aceitação que o roteiro pede. Algumas salas foram
fotografadas com os scripts de entrada desligados, e nenhuma batalha real
foi jogada. As 47 linhas de `aceitacao_frontier_47_mapas.csv` continuam
pendentes.
