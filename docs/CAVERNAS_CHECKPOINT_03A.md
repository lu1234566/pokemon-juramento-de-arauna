# Checkpoint 03A — Terra Cave + Marine Cave

Implementação visual concluída sobre `bcd93e980e55a0f5a649baa7d6b8d154b464be23`.
Este checkpoint contém quatro mapas. Build ARM e emulação desta etapa estão
pendentes; as capturas históricas do checkpoint 02 não são testes do 03A.

## Resultado

| Mapa | Dimensões | Arte |
| --- | --- | --- |
| TerraCave_Entrance | 20×20 | Galeria de basalto, cinza, faces escuras e depósitos ocres. |
| TerraCave_End | 27×30 | Núcleo quente, rocha vitrificada, patamares e margem incandescente. |
| MarineCave_Entrance | 20×20 | Galeria úmida, pedra fria, sedimento claro e água de mergulho. |
| MarineCave_End | 27×30 | Câmara costeira, faixas minerais, patamares e margem clara. |

O suplemento está em `docs/CAVERNAS_CHECKPOINT_03A_DESIGN.md`. A arte própria
parte do atlas `art/cavernas_03a/minerais_atlas.png`, criado com a ferramenta
integrada de geração de imagens. O prompt completo está em `geracao.txt`.
O atlas é material de produção, não mapa jogável. As peças foram reduzidas e
indexadas para 4bpp e RGB555 por um builder determinístico.

Dois bancos secundários privados usam a animação Cave já existente. O primário
General permanece intacto. Os aliases entram no seletor gráfico que já atende
as Grutas V2. Não foi alterado código do motor, nem acrescentado harness.
Os quatro registros de layout só recebem o novo banco secundário.

## Preservação comprovada

- 17.753 arquivos preexistentes de dados, código, constantes e gráficos
  idênticos byte a byte. Todas as grades nativas e todos os scripts do jogo
  estão incluídos nesse contrato.
- 740 registros de layout alheios intactos; ordem e IDs dos 744 preservados.
- 2.420 células com atributo completo idêntico entre ID nativo e alias:
  comportamento e tipo de camada; a grade conserva colisão e elevação.
- Cinco warps, dois objetos e dois gatilhos das cavernas preservados.
- As oito entradas temporárias das Rotas 114, 115, 116 e 118, suas condições,
  colocação/limpeza de metatiles e retorno dinâmico à superfície permanecem
  intactos. A aparência dessas rotas e a Rota 103 V1.2 não mudam.
- `setdivewarp MAP_UNDERWATER_MARINE_CAVE, 9, 6`, os scripts submersos e os
  retornos das Rotas 105, 125, 127 e 129 permanecem intactos.
- Os encontros herdados das duas salas finais conservam posições, movimento,
  nível 70, flags, captura, vitória, fuga/teleporte, remoção e fim do clima.
  Esta etapa não migra esses encontros para novas cenas narrativas.

## Validação própria

- Seletor C real: 2.420 células novas e 7.276 verificações de fallback.
- 9.583 células dos 14 mapas anteriores do seletor conservam a saída exata.
- 32 combinações mapa/quadro: água e lava usam gráficos reais de animação.
  A lava estática sob o encontro permanece estática e o bolsão vivo anima.
  Patamares andáveis sobre lava continuam desenhados como terra.
- Índices 4bpp, quantização/roundtrip RGB555, paletas CRLF, opacidade do
  piso, limites de metatiles, tiles e paletas aprovados. Nenhum tile novo usa
  432–511, 928–931 ou 992–1023. Não é uma execução de gbagfx ou build de ROM.
- Auditoria oficial: oito verificações aprovadas em 528 mapas.
- Prontidão estática oficial: aprovada, inclusive 189/189 do protagonista
  e 95/95 de capacidade de paletas. Gerados 528 mapas e 551 músicas com as
  ferramentas do projeto. A compilação ARM foi explicitamente omitida pelo
  script oficial de prontidão estática.
- Builder reaplicável sem mudar bytes. O instalador realiza pré-verificação
  completa, confere dependências do jogo, guarda backup e reverte uma falha
  parcial. Os resultados dos testes de instalação acompanham o pacote.

Evidências: `review/cavernas_03a/validation.json`, `functional_contract.json`,
`map_audit.log`, `static_readiness.log`, `cumulative_audit.json` e `renders.json`.
Há quatro mapas integrais antes/depois e doze pares de recortes 240×160.
Os PNGs são renders nativos sem sprites/névoa, não capturas de emulador.

## Base e pacotes cumulativos

`main` permanece em `979fb6c1b6731561f3c993efd6045a9bbf096c54`, 82 commits
atrás da base escolhida. A branch de trabalho do GitHub estava em `bcd93e980e`.
Não restaurar o checkpoint 71 ou os pacotes antigos sobre esta base.

- Bible PDF e 82 concepts: todos os 83 arquivos conferidos por hash contra
  o pacote recuperado.
- Checkpoints 01/02: 29 dos 30 arquivos coincidem; o relatório instalado
  ganhou a verificação de ROM/emulador feita pelo integrador. Nenhuma fonte
  funcional diverge da entrega correspondente.
- Sul/Pampa V1.1 + Uivo: todos os 1.144 hashes do payload foram conferidos.
  1.136 coincidem com a base; oito diferenças são as cinco correções de
  instalação documentadas e os três bancos corrigidos pela Rota 103 V1.2.

## Reproduzir

Depois de instalar o checkpoint, com Git, Python/Pillow e compilador C do host:

```sh
git worktree add --detach ../arauna-base-03a bcd93e980e55a0f5a649baa7d6b8d154b464be23
python3 tools/arauna_maps/build_cavernas_03a.py --base ../arauna-base-03a
python3 tools/arauna_maps/validate_cavernas_03a.py --base ../arauna-base-03a
python3 tools/arauna_maps/render_cavernas_03a.py --base ../arauna-base-03a
python3 tools/arauna_maps/prepare_route103_host_checks.py
python3 tools/arauna/audit_map_data.py
bash scripts/check_arauna_static.sh
```

O gate de largura de texto requer os objetos históricos de `c210195e` em
clones parciais. Falta de objeto Git não certifica defeito nos textos.
Não regenerar `functional_inventory.json` do checkpoint 01 sobre esta etapa.
O contrato novo é separado e congelado em `functional_contract.json`.

## Integração em ROM ainda pendente

O ambiente desta entrega não contém `arm-none-eabi-gcc` nem mGBA.
O integrador deve compilar a composição inglesa, conferir carregamento dos
dois bancos, lava/água animada, névoa, sprites dos encontros, entrada/retorno
das oito posições de Terra, Dive/emersão de Marine e todos os resultados de
batalha. Não distribuir ROM, ELF, saves, estados ou harness no checkpoint.

## Próximo checkpoint

03B: Sealed Chamber (duas salas), Ancient Tomb e Island Cave. Depois,
03C: Altering e Artisan Cave (três mapas), seguido dos 12 Dive e do Safari.
Essas etapas não foram implementadas pelo 03A. Nenhum push foi realizado.

## Verificação na instalação

- O instalador foi aplicado sobre `bcd93e980e`. A árvore resultante é
  idêntica à do bundle `378ce72228`. `validate_cavernas_03a.py` aprovou e
  regenerou um `validation.json` igual ao entregue.
- Build `en` ok (ROM em 56,8%). Gates aprovados: 189/189, 95/95, 0
  candidatos de resíduo, as oito verificações de mapas e
  `variantes_troca_layout.py --verificar` 9/9. Nenhum símbolo de harness
  na ROM.
- Grades visuais: os índices 406, 407, 408 e 412 de `gMapLayouts` são
  exatamente os quatro layouts, e cada um é usado por um só mapa.
- Legibilidade na visão de câmera:
  - Nas salas finais havia 48 paredes com o mesmo desenho de um piso
    andável e 111/144 pisos com desenho de parede. Agora são 0.
  - Nas entradas, que já eram 0, continuam 0.
- Emulador:
  - Fotos nos quatro mapas, com e sem a névoa original das salas finais
    (`WEATHER_FOG_HORIZONTAL`, herdada do Emerald).
  - A lava e a água animam entre quadros, e só nessas regiões. Os
    lendários aparecem nas posições de sempre.
  - Os warps entrada→fim funcionam a pé nas duas cavernas: chegada em (5,4)
    na Terra Cave e em (20,4) na Marine Cave.
- Observação de design: a névoa das salas finais cobre boa parte da arte
  nova. Trocar ou suavizar o clima é uma decisão separada; esta etapa não
  muda clima nem scripts.
