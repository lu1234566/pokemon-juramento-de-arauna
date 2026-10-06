# Início de Arauna — Correção de arte V2

Base de instalação: `01bf15e5ac957a21c24d49cd6c78658d07154e38`.
Esta é uma correção incremental do Início Composição V1 já instalado. A Campanha Interiores V2 e os arquivos históricos da V1 permanecem como estavam.

## Resultado

- Ipê e recortes das casas/laboratório agora usam a grama do banco como camada de baixo. O objeto fica na camada de cima, com índice 0 transparente somente nessa camada. O piso permanece opaco.
- Centro e venda da Passagem ganham portas de madeira, com transom, batente e três fases distintas de abertura/fechamento. O seletor usa a arte nova somente quando o primário é `gTileset_AraunaInicioBaseV1` e o ID é `0x061` ou `0x041`.
- Os IDs funcionais das portas, warps, destinos, eventos, scripts, climas, encontros e pontos de cura permanecem iguais à base instalada.

O problema não era um fundo cinza no atlas: ao achatar objeto e piso numa única camada, o construtor escolhia a paleta do objeto também para o chão. Algumas paletas não têm o verde necessário. Agora o piso e a silhueta usam camadas e paletas independentes. A escolha de paleta dos pixels do objeto conserva o critério anterior. A vegetação da faixa de borda mantém sua composição opaca anterior para preservar a interface com outros bancos.

## Dados da revisão

| Mapa | Pixels da cor cinza relatada antes | Depois |
| --- | ---: | ---: |
| Amanhecer | 1265 | 169 |
| Rota 101 | 1320 | 38 |
| Passagem | 1915 | 186 |

A cor medida é RGB (106,123,115). Os pixels restantes são tons presentes nos próprios telhados, paredes e sombras; não se fez uma substituição global dessa cor. `99` metatiles de objetos foram conferidos com a mesma camada de grama opaca do piso.

## Verificações desta correção

- Build ARM aprovado: ROM utiliza 17.233.848 bytes, acréscimo de 1.156 bytes em relação à entrega anterior. EWRAM e IWRAM permanecem em 249.708 e 30.428 bytes.
- Gates oficiais: 189/189 e 95/95; auditoria de resíduos com 0 candidatos. As oito verificações de dados de mapas passaram.
- Os 528 `map.json`, scripts dos mapas e o `layouts.json` permanecem idênticos à base. Nenhum registro de layout foi removido, acrescentado ou renumerado.
- Nas 5.440 células dos cinco mapas, colisão, elevação e atributos de comportamento permanecem iguais à base.
- Rotas 102 e 103 mantêm a grade e o render RGB exatos. As 12 conexões foram comparadas pelo RGB real, seguindo os IDs das grades antes e depois. As 29 células de objetos que mudam na faixa recebida mostram a mesma correção do mapa fonte; nenhuma conexão ganhou células de desenho errado.
- O seletor C real de portas foi compilado e testado: 1.024 IDs fora do banco conservam a seleção anterior; no banco próprio, apenas os dois IDs declarados mudam.
- Tiles LZ10/4bpp, 32 paletas RGB555 e os 768 bytes dos três quadros da porta foram comparados diretamente com a ROM ligada. Conferem com as fontes.
- Construtor idempotente: 7.130 arquivos nativos conferidos.
- Validador funcional anterior reaprovado contra a base da Campanha V2: 1.124 posições de save, alcance dos eventos/warps e Cut. O novo validador também exige que `src/overworld.c` e `src/fldeff_cut.c` sejam idênticos à base instalada.

## Emulador

No mGBA 0.10.2, três percursos passaram sem opcodes ilegais:

1. Centro: saída natural para (7,20), entrada pela porta de madeira, registro dos três quadros em VRAM, nova saída e foto do ipê da Passagem.
2. Venda: saída natural para (20,9), entrada pela porta de madeira, registro dos três quadros em VRAM e nova saída.
3. Laboratório: saída natural para Amanhecer, fotos do laboratório e do ipê, travessia até a Rota 101 e foto do ipê dessa rota.

A inicialização de captura alterou somente a memória do emulador, com os desvios restaurados antes das travessias. As fotos exteriores vêm de portas ou conexões naturais. A ROM em disco manteve SHA-256 `38efbd8e6b493961b3153d953c220b25396a3da1715f2594ec61f059b0000948` durante as capturas. ROM, ELF, saves, estados e o programa de captura não fazem parte da entrega.

## Migração e limites

O ajuste instalado de prioridade do “continue game warp” está preservado byte a byte. Esta rodada não altera a lógica nem o formato de save e não inclui teste com um arquivo de save antigo fornecido por um jogador. A retomada continua coberta pelos testes de rotina já descritos na V1.

Esta correção conserva a composição instalada. Não redesenha a geografia outra vez, não limpa duplicatas e não remove os sete layouts históricos de Interiores V1.

## Reprodução

```bash
git apply --check /caminho/Arauna_Inicio_Arte_V2.patch
git apply --index /caminho/Arauna_Inicio_Arte_V2.patch
python3 tools/arauna_maps/validate_inicio_arte_v2.py --base /caminho/do/checkout-01bf15e5ac
python3 tools/arauna_maps/validate_inicio_geometria_v1.py --base /caminho/do/checkout-42cff21717 --output /caminho/validacao-funcional.json
bash scripts/build_arauna.sh en -j6
bash scripts/check_arauna_static.sh
python3 tools/arauna/audit_map_data.py
python3 tools/arauna_maps/verify_inicio_rom_v1.py --rom pokemon-juramento-de-arauna-en_modern.gba --elf pokemon-juramento-de-arauna-en_modern.elf --output /caminho/codificacao.json
```

As cópias usadas em `--base` precisam permanecer limpas. `build_inicio_geometria_v1.py` reconstrói a arte a partir do atlas já presente na base e desenha a porta no formato nativo editável de 16×32 pixels. O PNG de animação contém três quadros, totalizando 16×96 pixels.

## Verificação na instalação

- Aplicado sem conflito sobre `01bf15e5ac`; `make MODERN=1` ok; 189/189,
  95/95, 0 candidatos de resíduo e as oito verificações de mapas aprovadas.
- `validate_inicio_arte_v2.py` (base `01bf15e5ac`) e
  `validate_inicio_geometria_v1.py` (base `42cff21717`) aprovados em
  worktrees limpas.
- Cor RGB (106,123,115) recontada com o renderizador do repositório: 169,
  38 e 186 pixels, os mesmos números do relatório.
- Bordas: as 12 faixas da região estão idênticas às da base.
- Emulador: ipês sem quadrado cinza em Amanhecer e na Passagem; portas do
  Centro e da venda abrindo e fechando com a arte de madeira ao entrar.
