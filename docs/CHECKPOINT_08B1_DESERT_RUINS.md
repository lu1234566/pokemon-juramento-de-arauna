# 08B1 — DesertRuins V1

Um mapa concluído: DesertRuins, duas câmaras no mesmo layout de 17 × 33.
A arte usa arenito estratificado e placas de lajedo desgastado, com piso mais
claro que as paredes. A leitura em 240 × 160 distingue o espaço de circulação,
os seis afloramentos da câmara superior e a inscrição da passagem selada.
Não foram acrescentados objetos, textos ou elementos de história.

## Base recuperada e histórico

Base: `393cdf63e4cef254d5890882df572f4011c69bf4`, último commit da branch
`claude/pokemon-juramento-arauna-fhk6ah` conferido no GitHub em 10/10/2026.
Ela já integra a revisão 08A (`6b974ba33e`) sobre `a594b3e1e6`. Entre a594 e
393 só há documentação e materiais de revisão; nenhum arquivo funcional do
jogo mudou. O checkpoint usa a base mais recente para conservar essa revisão.

O ZIP 08A recuperado tem SHA-256
`1319502d41bb6e9fc889eaa9166c0657e7f79ac67375f182109b2d47cd9a6541`.
Foram lidos a Master Map Design Bible recuperada, o conceito da Rota 111,
o relatório 08A e a integração 08A. O semiarido/deserto da Rota 111 orientou
os materiais; a Bible pede coerência entre geografia e puzzle e leitura
clara da colisão.

`main` permanece em `979fb6c1b6`, 115 commits atrás da base 393. O incremento
não deve ser aplicado diretamente em main. O pacote inclui um bundle desde
393 e outro cumulativo desde a594, incorporando o histórico 08A e sua revisão
de integração. Não houve push.

## Preservação

| Elemento | Resultado |
|---|---|
| Layouts | Os 754 IDs, dimensões e ordem permanecem; só DesertRuins muda de bancos |
| Grade e borda | map.bin e border.bin byte a byte iguais |
| Mapas e scripts | Todos os map.json, scripts, eventos, conexões e warps preservados |
| Braille | Mensagem e fonte intactas; 90 pixels de pontos conservados em posição e cor RGB555 |
| Passagem | IDs 0x229, 0x235 e os seis IDs abertos 0x22A–0x22C / 0x232–0x234 preservados |
| Puzzle | Rock Smash continua aceito em (5,23), (6,23) e (7,23), somente antes da conclusão |
| Encontro | SPECIES_REGIROCK nível 40, flags e ramos de captura, vitória e fuga intactos |
| Centro e Palace | As correções de metatiles já integradas ficam protegidas |
| Portas e overworld | field_door.c, overworld.c e os seletores de mapas intactos |

O contrato congela os 24.108 arquivos anteriores que não são os quatro
registros gráficos aditivos. O Centro 07H conserva o metatiles.bin com hash
`aa2ce0422b3b25572bf3afcb9b521a75f2259f2d6be0268b522f83d0321b3e4b`.
O manifesto 07H histórico não foi regenerado nem usado para restaurar esse
arquivo. A água do Palace 07C também permanece igual.

O novo par de bancos é exclusivo do mapa, com 48 IDs redesenhados e 116
slots gráficos estáticos. Os atributos dos 926 metatiles, as máscaras de
camada e os callbacks nativos são mantidos. Os slots usados pelo DMA de
General e Cave ficam reservados. Os outros 878 metatiles do par permanecem
visualmente idênticos; nenhum banco compartilhado foi alterado.

## Verificação concluída

- Contrato completo, 754 layouts e quatro registros aditivos: PASS.
- Gráficos 4bpp, limites de VRAM, paletas e 96 máscaras de camada: PASS.
- Função C original de Regirock: 3.366 combinações de mapa, posição e flag.
- Escritor C original de fieldmap: comparação das 561 células depois de abrir;
  exatamente seis mudam, preservando a elevação, com centro livre e lados bloqueados.
- Acesso às três posições de Rock Smash e estados aberto/fechado: PASS.
- Varredura dos 528 mapas: oito gates PASS; três avisos de Surf já existentes.
- Gates de paletas de atores, espécies especiais, facções e assets de personagens:
  PASS. A proteção 08A também passa nos oito arquivos.

Os JSON e logs em `review/desert_08b1` registram os resultados. A instalação
tem pré-verificação integral de hashes, backup, rollback em caso de erro e
reaplicação sem novas escritas. Os testes de transporte e instalação seguem
nos arquivos INSTALL_TEST.json e CUMULATIVE_TEST.json do pacote.

## Limites e aceitação em ROM

Este ambiente não possui compilador ARM nem mGBA. Os PNGs são renders dos
assets nativos, sem atores, não capturas de emulador. Compilação da nova ROM,
entrada e retorno pela Rota 111, leitura do Braille, execução real de Rock
Smash e batalha/captura/fuga continuam pendentes no ambiente de integração.
O encontro e suas condições foram preservados por hashes, não simulados em batalha.

A aceitação das 47 salas do Frontier com save carregado e batalhas reais
continua pendente. O roteiro 08A foi preservado, sem marcar sessões como jogadas.

## Reprodução e próxima etapa

Com Python 3, Pillow, compilador C do host e cabeçalhos gerados por mapjson:

```sh
python3 tools/arauna_maps/validate_desert_08b1.py
python3 tools/arauna_maps/desert_08b1.py render
python3 tools/arauna/audit_map_data.py
python3 tools/arauna_maps/check_visual_protection_08.py
```

O inventário atualizado tem 478 mapas com banco Arauna, 16 módulos da Pyramid,
8 inativos e 26 ainda nativos. O inventário 08A histórico permanece intacto.
Próximo pacote: **08B2 — DesertUnderpass e ScorchedSlab**, dois mapas, partindo
do commit 08B1 registrado no manifesto. Depois: **08B3 — MirageTower 1F–4F**.
