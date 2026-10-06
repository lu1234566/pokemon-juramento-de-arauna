# Início de Arauna — Composição V1

Base de instalação: `42cff21717d138690118555fb23b0fc13bcb571b`, branch de referência `claude/pokemon-juramento-arauna-fhk6ah`.
Direção: Arauna Master Map Design Bible, bloco A. Esta entrega redesenha três exteriores; os PNGs de revisão são renders dos arquivos reais e capturas da ROM compilada.

## Composição implementada

| Mapa | Dimensão | Resultado |
| --- | --- | --- |
| Vila Amanhecer / Littleroot | 30×26 | Rua de terra sinuosa, casas de silhuetas distintas, clareira com ipê, cercas e araucárias. Laboratório deslocado de (12,21) para (20,22). |
| Rota 101 | 40×28 | Trilha curva, campos de capim, marcos vegetais e bifurcação para a Primeira Câmara. A área do resgate mantém colisão, elevação e comportamento da base. |
| Vila da Passagem / Oldale | 30×26 | Entroncamento em Y/T, ocupação ao longo dos braços e novos pontos de entrada das quatro construções. |

As dimensões e os pontos de travessia ficaram iguais aos da base para manter as conexões. As coordenadas das duas casas de Amanhecer preservam o desembarque do caminhão e as cenas dos tênis. Não é uma reconstrução completa de todos os espaços de cena.

## Migração funcional

| Porta da Passagem | Antes | Depois |
| --- | --- | --- |
| Casa/pousada 1 | (6,7) | (8,9) |
| Casa 2 | (22,21) | (22,20) |
| Centro | (3,18) | (7,19) |
| Venda | (25,6) | (20,8) |

IDs e destinos dos warps permanecem iguais. O ponto de cura passa a (7,20). A apresentação da loja foi transladada em (-5,+2), incluindo as posições do empregado e seus quatro percursos. As placas e os NPCs reposicionados conservam scripts, flags e conteúdo. O registro de posicionamento do Pokémon decorativo da Rota 101 acompanha sua mudança para (13,11).

Saves que ainda guardam o ID antigo destes três layouts recebem uma migração única no Continue: recarrega os eventos pelo cabeçalho atual e conserva a posição quando ela continua livre. Se virou obstáculo, escolhe o piso livre mais próximo. A animação normal de saída de porta pode avançar o jogador uma célula. Saves dos outros mapas e caches já atualizados seguem o caminho anterior. Nenhum campo do formato de save foi acrescentado ou movido.

O capim novo responde ao Cut e vira o campo do mesmo banco. O seletor original continua valendo para os demais tilesets.

## Arte e bancos

Atlas novo: `art/inicio_geometria_v1/source_atlas.png`, produzido pela ferramenta interna de geração de imagens. O prompt completo está em `source_prompt.txt`. O construtor recorta os módulos, reduz às medidas nativas, quantiza nas paletas existentes e monta os metatiles. Os pisos têm padrões próprios desenhados pelo código, com menos ruído visual.

Dois bancos exclusivos atendem os cinco mapas contíguos. Eles preservam os desenhos necessários das Rotas 102/103 e das faixas de vizinhos, além dos IDs do General referenciados pelo motor. Tiles estáticos duplicados são compactados sem alterar índices funcionais, cores ou flips. Os slots 432–511 e 992–1023 ficam reservados às animações. Os metatiles novos usam somente paletas 0–12 e pisos opacos.

| Medida de formas reaproveitadas | Resultado |
| --- | ---: |
| Tiles novos, excluindo compatibilidade | 1.38% |
| Banco primário, incluindo compatibilidade | 46.84% |
| Banco secundário, incluindo compatibilidade | 6.08% |

O detector compara classes de cor, transparência e espelhamentos exatos contra o histórico anterior ao projeto (`ad0fd4d17f...`, 39.376 tiles armazenados). Superfícies simples podem coincidir por acaso. Não mede qualidade artística nem identidade cultural. Os percentuais não usam a mesma população menor da auditoria externa de Emerald vanilla.

## Validação

- ARM build aprovado; ROM utiliza 17.232.692 bytes dos 32 MiB disponíveis.
- Gates oficiais aprovados: 189/189, 95/95; auditoria de resíduos sem candidatos.
- As oito verificações da auditoria de dados de mapas passaram.
- 15267 arquivos protegidos permanecem idênticos à base.
- Todas as portas e placas têm aproximação acessível. O corte de alcance do resgate mantém a bolsa acessível e impede a fuga antes do inicial.
- As 2.760 células das Rotas 102/103 mantêm grade, comportamentos e render RGB idênticos. As faixas recebidas de vizinhos sem mudança conservam o render anterior.
- Migração de saves: 1124 posições antigas de piso livre verificadas no código C real; 101 precisam de deslocamento. Caches atuais e outros layouts não são migrados.
- Cut: 1.024 IDs de outros bancos conferidos contra o seletor anterior; capim próprio vira campo próprio.
- Decodificação independente dos tiles LZ10/4bpp e das 32 paletas RGB555 diretamente da ROM: bytes iguais às fontes.
- Construtor idempotente sobre os arquivos nativos de dados.

No mGBA 0.10.2, 11 cenários passaram: travessias Amanhecer→101→Passagem e ida/volta 102/103; entradas e saídas pelas quatro portas da Passagem e pelo laboratório; bloqueio norte; tênis; apresentação da loja e poção; resgate com escolha do inicial e retorno ao laboratório; caminhão masculino/feminino; retomada com cache antigo em cada um dos três mapas. Nenhum opcode ilegal foi registrado.

As fotos exteriores vêm de entrada natural por portas/conexões depois da inicialização temporária, evitando o artefato conhecido de captura. O processo de captura altera apenas a memória do emulador. A ROM em disco manteve o SHA-256 `a82200133bc90f07fd428e21979132b7dc5d005b8a8e792652eeb88ed9348f0a`. Código temporário, ROM, ELF, saves e estados não integram a entrega.

## Reprodução

Aplicar o patch na base indicada, em checkout limpo, sem restaurar checkpoints completos. Há uma cópia dos arquivos alterados e um manifesto SHA-256 no ZIP.

```bash
git apply --check Arauna_Inicio_Composicao_V1.patch
git apply --index Arauna_Inicio_Composicao_V1.patch
python3 tools/arauna_maps/validate_inicio_geometria_v1.py --base /caminho/do/checkout-base
bash scripts/build_arauna.sh en -j6
bash scripts/check_arauna_static.sh
python3 tools/arauna/audit_map_data.py
python3 tools/arauna_maps/verify_inicio_rom_v1.py --rom pokemon-juramento-de-arauna-en_modern.gba --elf pokemon-juramento-de-arauna-en_modern.elf
```

Para reconstruir os PNGs completos: `render_native_map.py LittlerootTown amanhecer.png`, e os equivalentes `Route101` e `OldaleTown`.

Os sete registros da Campanha Interiores V1 seguem sem mapas ativos. Permanecem como entradas históricas dos validadores V1/V2; esta rodada não remove nem renumera layouts. As demais áreas e as conexões fora deste grupo continuam no panorama anterior.

## Verificação na instalação

- Aplicado sem conflito sobre `42cff21717`; `make MODERN=1` ok.
- `check_arauna_static.sh` 189/189, `check_overworld_palette_capacity.py`
  95/95, `audit_visible_residue.py` 0 candidatos, `audit_map_data.py` com as
  oito verificações aprovadas, inclusive warps alcançáveis a partir do ponto
  de cura.
- `validate_inicio_geometria_v1.py` aprovado em worktrees limpas.
- Bordas, render RGB com `render_native_map.py` e `bancos_nativos.py` do
  repositório: nenhuma das 12 faixas entre Amanhecer, Rota 101, Passagem,
  Rotas 102/103, Petalburg e Rota 110 mudou. Rota 103 ↔ Rota 110 já
  diferia antes (251 e 126 células).
- Ajuste na instalação: em `CB2_ContinueSavedGame`, o "continue game warp"
  do jogo volta a ter prioridade sobre a migração dos três layouts antigos.
  Assim a flag continua sendo consumida como antes. A migração em si não
  mudou.
- Emulador: os três mapas, a Rota 102 com os bancos novos e a porta do
  Centro da Passagem, entrando e saindo para (7,20).

### Pendência de arte

Em 85 células, o fundo de módulos desenhados na camada de baixo ficou com
um cinza (RGB 106,123,115) no lugar da grama: o ipê e as laterais de
algumas casas (29 em Amanhecer, 12 na Rota 101, 44 na Passagem). As portas
do Centro e da venda usam o vidro azul do Emerald, que destoa da fachada
rústica.

## Atualização — correção de arte V2

Os fundos cinzas externos e as portas de vidro da Passagem registrados na revisão da V1 foram corrigidos sobre a base instalada `01bf15e5ac`. A lógica de save, incluindo a prioridade do continue warp, permanece idêntica a essa base. Detalhes e validação atual estão em `docs/INICIO_ARTE_V2.md`. Os registros originais desta página ficam preservados como histórico.
