# Checkpoint 03A — suplemento de design

Base: `bcd93e980e55a0f5a649baa7d6b8d154b464be23`. O main permanece
`979fb6c1b6731561f3c993efd6045a9bbf096c54`, 82 commits atrás desta base.
As referências foram recuperadas antes da edição: Bible de 55 páginas,
82 concepts únicos e contrato funcional do checkpoint 01. Os checkpoints
01/02 estão instalados nesta base; não reaplicar overlays cumulativos antigos.

## Escopo e referências

| Mapa técnico | Dimensões | Direção visual |
| --- | --- | --- |
| TerraCave_Entrance | 20×20 | Basalto, cinza e veios ocres; a galeria leva da saída temporária ao núcleo. |
| TerraCave_End | 27×30 | Patamares de rocha vitrificada; fissuras e margem incandescente concentram a leitura no bolsão quente. |
| MarineCave_Entrance | 20×20 | Pedra fria, sedimento claro, linha de maré; o lago de mergulho é legível. |
| MarineCave_End | 27×30 | Câmara úmida, faixas minerais e margem clara; o núcleo de água contrasta com o caminho. |

A Bible, páginas 26–29, fornece a linguagem de pedra antiga, bolsões quentes,
marcas de maré e convergência natural ao núcleo. Os concepts de Trilha de Brasa,
Gruta da Maré e Gruta da Origem orientam materiais e densidade. Não há pranchas
dedicadas de Terra/Marine entre as referências recuperadas; este suplemento
registra a interpretação nova. Não adiciona nomes canônicos, símbolos, objetos
sagrados, cenas ou encontros.

## Composição nativa

Arte mineral própria, com piso de contraste baixo e falésias de contraste maior.
Massas bloqueadas recebem topos e faces de rocha em função da vizinhança;
veios e depósitos mudam por zona, em vez de repetir o mesmo chão marrom.
Margens quentes/frias indicam o núcleo e o retorno. Escadas, boca da caverna,
saída e zona de mergulho continuam legíveis em 240×160.

São usados dois bancos secundários exclusivos, um por sistema. O primário
General e suas animações são preservados. A câmera usa aliases contextuais,
com o atributo completo do ID funcional correspondente. O seletor existente
conserva seu fallback quando um script muda o ID nativo. Os quatro registros
de layout só mudam de banco secundário; IDs, ordem, dimensões e grades ficam
intactos. Não se apresenta esta passagem de materiais e composição como
migração de geometria ou implementação dos novos arcos narrativos da Bible.

## Contrato protegido

- Todos os scripts, eventos, objetos, flags, variáveis, encontros e warps.
- Terra: oito localizações temporárias nas Rotas 114, 115, 116 e 118,
  colocação/limpeza da entrada, warp dinâmico, escape e retorno correspondente.
- Marine: acesso submerso e retorno em `Underwater_MarineCave`, incluindo
  `setdivewarp` e configuração de retorno à superfície.
- Encontros existentes das duas salas finais: posição, movimento, nível 70,
  batalha, captura, vitória, fuga/teleporte, remoção e fim do clima anormal.
- Safari, Dive, puzzles do 03B e Artisan/Altering do 03C ficam como dependências
  preservadas. A Rota 103 V1.2 e seus aliases também são protegidos.

Os identificadores herdados GROUDON/KYOGRE são mantidos no código. Este
checkpoint visual não resolve divergências narrativas anteriores relativas
a esses encontros; segue a instrução explícita de preservá-los.

## Entrega e verificação

Contrato congelado desta base, builder determinístico, validação de dados e
seletor C real, quatro renders integrais e três pares de recortes 240×160 por
mapa. PNGs são renders de dados nativos sem sprites ou névoa, não capturas
de emulador. Compilação ARM/emulação são declaradas separadamente.

Sequência posterior: 03B (Sealed Chamber, Ancient Tomb, Island Cave),
03C (Altering e Artisan), 04A–C (12 Dive), 05 (Safari), 06 (integração em ROM).
