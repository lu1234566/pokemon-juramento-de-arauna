# Campanha — caminhão e interiores de rota V1

## Entrega

Primeiro lote da prioridade de campanha: sete mapas em seis bancos secundários
exclusivos. Base de instalação: `258195026b8e5d1a43bfb81fdf1480c02000c4b2`, branch
`claude/pokemon-juramento-arauna-fhk6ah`. Essa base já incorpora as bordas V2
119/118 e as variantes Arauna dos scripts que trocam layouts.

| Mapa técnico | Dimensões | Trabalho visual |
| --- | --- | --- |
| InsideOfTruck | 5×5 | Painel de carga reforçado, piso de metal e materiais menos saturados |
| Route104_MrBrineysHouse | 12×9 | Tábuas, madeira costeira e carta de navegação na parede |
| Route104_PrettyPetalFlowerShop | 15×9 | Piso de tábuas e materiais de viveiro; plantas e balcão preservados |
| Route117_PokemonDayCare | 12×9 | Madeira quente; balcão, PC, cadeiras e área cercada preservados |
| Route119_House | 10×9 | Madeira de abrigo úmido e pequeno painel/cartografia de mata |
| Route119_WeatherInstitute_1F | 20×13 | Piso técnico verde, sombras contínuas e painéis de medição |
| Route119_WeatherInstitute_2F | 20×11 | Mesmo sistema de materiais, séries de medição e estações de trabalho |

Os conceitos da Bible definem materiais de região, mas não desenhos individuais
para essas sete salas. Esta V1 segue a mata/costa da Rota 104, os campos
cultivados da 117 e a floresta chuvosa/instituto técnico da 119. Não representa
uma transcrição de um concept individual inexistente. A arte nativa foi criada
com módulos indexados, pelo mesmo método dos construtores de interiores já
adotados no repositório; não é uma imagem ilustrativa colocada sobre o mapa.

## Preservação da lógica

Sete layouts novos são acrescentados ao fim do registro. Os layouts antigos
continuam intactos. Cada novo `map.bin` e `border.bin` é uma cópia exata do
original. Nos sete `map.json`, somente `layout` mudou.

Eventos, NPCs, warps, triggers, música, encontros, clima, scripts, colisão,
elevação e comportamento permanecem iguais. Os atributos dos metatiles são
copiados byte a byte; os IDs não são renumerados. A abertura do caminhão conserva
os seis IDs usados pelo motor para fechar e abrir a porta, as caixas móveis e
a saída dinâmica definida pelo gênero do protagonista.

Não há alteração em primários compartilhados nem em código do motor. Os
bancos secundários originais continuam intactos, e os outros mapas mantêm seus
bancos. Nenhum dos sete mapas tem conexões de borda; este lote não amplia o
escopo da correção V2.

## Assets e limites GBA

- Seis folhas PNG indexadas, com no máximo 16 índices e 512 tiles cada.
- 66 tiles estáticos novos no total, alocados em slots livres. O intervalo
  reservado às portas não é sobrescrito. Os bancos originais não têm callback
  de animação secundária; os novos também usam `NULL`.
- Paleta 12 estava livre em todos os bancos de origem e recebe os módulos
  novos. Toda referência permanece entre as paletas 0 e 12.
- As paletas secundárias de arquitetura são ajustadas por banco. No Instituto,
  a paleta do piso/sombras também muda para evitar faixas de cores diferentes
  sob paredes e móveis. Paletas de OBJ são um espaço separado e permanecem
  intactas.
- Os módulos de piso usam índices opacos; não introduzem o defeito das frestas
  pretas associado ao índice 0 na camada inferior.

## Verificação

- Build inglês: aprovado com os três gates oficiais de inglês, cobertura
  narrativa e largura de texto.
- Readiness estática: aprovada; protagonista 189/189, capacidade de paletas
  95/95 e demais verificações oficiais aprovadas.
- Auditoria de mapas: oito verificações aprovadas. As três notas existentes
  de warps que exigem Surf em Ever Grande/Lilycove permanecem.
- Auditoria de resíduo: zero candidatos críticos, PT ou nomes antigos.
- Validador deste lote: 946 células, grades/bordas e atributos idênticos;
  8.053 arquivos protegidos intactos; roundtrip 4bpp aprovado para seis bancos.
  867 células mudam de aparência.
- Reprodução: os 139 arquivos de assets/layouts/mapas/registros produzidos pelo
  construtor tiveram os mesmos SHA-256 em uma segunda execução.
- Regressão das bordas 119/118: 609 células alvo continuam exatas, zero pioras
  e 7.200 células próprias preservadas.
- Regressão da Mata da Espera: 501 células acessíveis antes do Cut e 660 depois,
  atributos e IDs interativos preservados.

### Emulador

mGBA 0.10.2 com a ROM final limpa e a ROM da base: oito entradas em cada versão,
16 execuções. Seis interiores foram carregados em pontos centrais caminháveis,
com NPCs e dispositivos nativos. O caminhão foi testado com protagonista
masculino e feminino, verificando o gênero em RAM e executando sua sequência
original: movimento com porta fechada, parada com porta aberta e saída para
Vila Amanhecer. A saída masculina chega à área da casa esquerda; a feminina,
à casa direita, como na base.

Dez comparações de grade/cache em RAM foram idênticas entre base e entrega:
oito entradas e duas saídas do caminhão. Não houve opcode ilegal. As imagens
de antes/depois usam a mesma posição e o mesmo número de frames.

O teste chama `CB2_NewGame` após a inicialização e configura nome/gênero/opções
como uma nova partida. Não refaz o menu de criação do personagem. Para os seis
interiores, a entrada é temporariamente direcionada em memória, com a função
original restaurada antes das capturas. No caminhão não há substituição de
entrada, callback de sequência, porta ou destino. A ROM em disco não é alterada.

Não foram jogadas novamente as batalhas do Instituto nem testados os serviços
do Day Care e da floricultura com uma equipe completa; sua preservação está
sustentada pela identidade dos scripts, eventos, IDs e atributos. O teste no
emulador cobre carregamento/render e a sequência completa do caminhão.

### Memória do build

| Região | Base | Entrega |
| --- | ---: | ---: |
| EWRAM | 249.708 bytes | 249.708 bytes |
| IWRAM | 30.428 bytes | 30.428 bytes |
| ROM ligada | 17.082.492 bytes | 17.139.700 bytes |

A ROM cresce 57.208 bytes; o consumo de RAM permanece igual. A imagem de ROM
preenchida até 32 MiB serve apenas à verificação local e não está no ZIP.

## Reprodução e continuidade

O README do ZIP contém base, commit local, aplicação do patch e manifesto.
Assets já gerados estão incluídos; não é necessário recriá-los para compilar.
O construtor requer Python/Pillow. O validador recebe uma worktree da base
exata e compara os arquivos que devem permanecer intactos.

```sh
python3 tools/arauna_maps/build_campanha_interiores_v1.py
python3 tools/arauna_maps/validate_campanha_interiores_v1.py --base /caminho/para/base-258195026b
bash scripts/build_arauna.sh en -j6
bash scripts/check_arauna_static.sh
python3 tools/arauna/audit_map_data.py
python3 scripts/audit_visible_residue.py
```

O próximo lote continua pelos interiores de rota ainda pendentes; Victory
Road e Seafloor Cavern vêm em seguida. As 55 conexões/6.015 células e o placar
308/528 são referências do levantamento enviado pelo usuário, não uma nova
auditoria global desta rodada. Esta entrega adapta sete mapas e não afirma
ter concluído os outros 213 daquele levantamento.

## Evidências e entrega

`review/campanha_interiores_v1/` contém dados de construção, validação,
reprodução, build/gates, auditoria de mapas, resíduo, regressão de bordas e
16 execuções do emulador. A entrega inclui patch Git binário incremental,
arquivos alterados, manifesto, relatório, duas pranchas dos sete mapas e uma
prancha de abertura/saída do caminhão. Não inclui ROM, saves, estados, ELF,
harness de entrada ou workflows de GitHub Actions.

## Verificação na instalação

- Aplicado sem conflito sobre `258195026b`; `make MODERN=1` ok.
- `check_arauna_static.sh` 189/189, `check_overworld_palette_capacity.py`
  95/95, `audit_visible_residue.py` 0 candidatos, `audit_map_data.py` com as
  oito verificações aprovadas.
- `validate_campanha_interiores_v1.py` aprovado contra uma worktree limpa da
  base. Rodado numa segunda worktree limpa com o patch: na cópia de trabalho
  do repositório, 885 paletas estão gravadas com LF, embora o
  `.gitattributes` peça CRLF. Para o Git o conteúdo é o mesmo, mas a
  comparação byte a byte do validador acusa diferença.
- Regressões: variantes de troca de layout atualizadas, bordas 119/118 sem
  piora, animações gerais e comportamento de metatile de todos os mapas sem
  diferença em relação à base; paletas 13–15 sem uso.
- Emulador: os seis interiores fotografados depois de sair e entrar pela
  porta (ou pela escada, no 2F do Instituto). Na entrada direta, o harness de
  teste executa a sequência do caminhão em qualquer mapa, e ela troca os
  metatiles em (4, 1–3). Caminhão: viagem e abertura da porta.
