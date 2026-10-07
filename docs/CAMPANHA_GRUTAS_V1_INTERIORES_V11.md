# Campanha Grutas V1 + Interiores de Rota V1.1

Entrega incremental sobre `4439f996326bbe457d8a9eacbf2ae4341befa88b`, da branch `claude/pokemon-juramento-arauna-fhk6ah`. Os treze mapas recebem bancos nativos derivados das duas folhas de conceito já entregues. A geometria e os dados de jogo continuam os da base.

| Área | Mapas | Referência usada |
| --- | --- | --- |
| Victory Road | 1F, B1F e B2F | Folha com faixa ocre |
| Seafloor Cavern | Entrance e Room1–Room9 | Folha de basalto escuro |

Os nomes antigos dos arquivos de referência eram invertidos em relação ao pedido: `Atlas de sprites da Gruta Abissal.png` contém a faixa ocre e foi usado na Victory Road; `Tileset pixel art da Passagem da Serra.png` contém basalto e foi usado no Seafloor. As cópias exatas estão em `art/campanha_grutas_v1` com nomes que indicam o destino.

## Bancos e integração

São cinco bancos privados: dois primários, dois secundários de rocha e um secundário para as correntezas das salas 6 e 7 do Seafloor. Cada banco contém `tiles.png` indexado em 4bpp, treze paletas JASC-PAL com CRLF, `metatiles.bin` e `metatile_attributes.bin`.

O construtor cobre todos os IDs usados nas grades, bordas e comandos `setmetatile` desses mapas. Também conserva os IDs nomeados do banco original para alterações de tiles em tempo de execução. Quando o mesmo ID representava chão livre e rocha bloqueada, somente as ocorrências bloqueadas receberam aliases com atributos idênticos. Os bits de colisão e elevação não mudaram.

Os metatiles têm piso opaco na camada inferior e objetos na superior. As paredes têm desenho e contraste diferentes do chão. Os atributos originais, incluindo comportamento e tipo de camada, foram preservados. Nenhum índice de layout foi inserido, removido ou renumerado: os 737 registros continuam na mesma ordem.

As referências usam apenas paletas 0–12. Os slots gráficos 432–511 e 992–1023 não são referenciados. A água ocupa 424–427 e a cascata 428–431. Cada família tem oito quadros de água e oito de cascata, atualizados por callbacks próprios; os callbacks anteriores ficam intactos.

## Interiores V1.1

- **Trick House, desafios 2, 4, 6 e 7:** trilhos mais espessos, contorno escuro e travessas claras. Como os oito desafios compartilham o banco, os demais também recebem o novo desenho quando usam esses IDs. Colisão, interruptores, setas, buracos, gelo e scripts permanecem iguais.
- **Casa da Lanette:** o piso básico passa a ser madeira uniforme, inclusive embaixo dos módulos de mobiliário. A planta e os móveis permanecem iguais.
- **Túnel do Fossil Maniac:** pela contagem bruta de células com colisão livre, foram revisadas 14 ocorrências, e não apenas as 11 da avaliação visual anterior. Dez ocorrências do ID misto `0x279` passam ao piso `0x303`, com o mesmo atributo; quatro ocorrências `0x22c/0x22d` recebem desenho de piso. As paredes bloqueadas continuam rocha.
- **Entrada do Safari:** as sete coordenadas citadas já usam piso ladrilhado opaco na base `4439f99632`. A revisão confirmou isso e conservou a arte. Coordenadas: (0,3), (12,3), (12,6), (12,9), (17,9), (12,10), (12,11). O PC foi ligado e o menu aberto no mGBA.

## Cache de saves antigos

O Emerald restaura uma pequena grade de metatiles ao continuar um save. Ela poderia reintroduzir IDs antigos nos mapas desta entrega. `AraunaGrutas_NormalizeSavedBlock` converte esse cache somente nos cinco bancos novos e no túnel revisado. Conserva os bits altos, é idempotente e não muda os mapas externos. O formato do save, a posição do jogador e as flags não foram modificados; a prioridade do continue game warp permanece igual à base.

O validador compila e executa o próprio C gerado em um teste independente: **458.752 valores** distribuídos em sete casos de banco, com conferência do resultado esperado, preservação dos bits e idempotência. Também compara a conversão das grades antigas com as atuais nos 14 mapas envolvidos. **Não foi importado um save histórico de um jogador real.**

## Verificação concluída

| Verificação | Resultado |
| --- | --- |
| Build ARM oficial em inglês, MODERN=1 | PASS |
| Gates oficiais | PASS; 189/189 protagonista e 95/95 capacidade de paletas |
| Auditoria de dados de mapas | 8/8 verificações aprovadas |
| Resíduos visíveis | 0 candidatos |
| Validador desta entrega | 14.457 células; 13 mapas novos e 25 interiores da V1 |
| Dados protegidos | 15.560 arquivos idênticos à base |
| Colisão, elevação, comportamento e camada | Idênticos à base em todas as células verificadas |
| IDs de scripts e opacidade da camada inferior | PASS |
| Codificação nativa comparada com a ROM | 5 bancos novos, 15 bancos de interiores e 32 quadros de animação |
| Regeneração dos dois construtores | 138 arquivos nativos e de integração idênticos byte a byte |
| mGBA 0.10.2 | 20 mapas fotografados, com mapa e posição conferidos |
| Interações no mGBA | 6 casos aprovados, sem opcode ilegal |

Os seis casos de interação são ida e volta entre Victory Road 1F e B1F, ida e volta entre Seafloor Room1 e Entrance, barreiras dos desafios 2 e 7, PC do Safari e uso de Surf na Room6. A animação de água alterou **214 bytes de VRAM** durante o teste. Esses casos não equivalem a concluir todos os puzzles ou jogar toda a campanha.

As capturas são o framebuffer nativo de 240×160 do mGBA, sem retoque. As pranchas apenas ampliam por vizinho mais próximo e acrescentam títulos. O carregamento inicial usou um gancho temporário somente na memória do emulador, restaurado antes das verificações. Para tornar os pisos subterrâneos legíveis na revisão, a iluminação inicial usou `flashLevel=0`; a rotina padrão de escuridão foi temporariamente contornada e restaurada em memória. Nenhuma dessas alterações está na ROM em disco ou no patch. A neblina original da Room9 foi mantida.

A ROM local foi produzida pelo GCC ARM 13.2.1, com 17.440.236 bytes ocupados antes do preenchimento para 32 MiB. SHA-256 da ROM preenchida: `045b082d9dfc69ebb267f23d60b4055f6cbda108eae0c46df7c6ba7459f8bfaf`. **A ROM, ELF, saves, estados de emulador e o harness de captura não fazem parte do pacote.**

Os comprovantes completos ficam em `review/campanha_grutas_v1`: recibos JSON, logs, vinte renders estáticos, capturas nativas e seis pranchas. A prancha de antes/depois da V1.1 é explicitamente um render estático, não uma captura do emulador.

## Reproduzir

Use Python 3.12 e Pillow 12.3.0 para reproduzir os assets byte a byte. São necessários Git e GCC de host para o validador; o build segue os requisitos normais do projeto.

```bash
# Em uma cópia limpa da base, depois de aplicar o pacote:
python3 tools/arauna_maps/build_interiores_rota_v1.py
python3 tools/arauna_maps/build_campanha_grutas_v1.py

# BASE_DIR deve ser outra cópia limpa, no commit exato 4439f99632.
python3 tools/arauna_maps/validate_campanha_grutas_v1.py --base BASE_DIR
bash scripts/build_arauna.sh en -j6
python3 tools/arauna/audit_map_data.py
python3 scripts/audit_rendered_visible_residue_en.py
bash scripts/check_arauna_static.sh
python3 tools/arauna_maps/verify_campanha_grutas_rom_v1.py \
  --rom pokemon-juramento-de-arauna-en_modern.gba \
  --elf pokemon-juramento-de-arauna-en_modern.elf
python3 tools/arauna_maps/verify_interiores_rota_rom_v1.py \
  --rom pokemon-juramento-de-arauna-en_modern.gba \
  --elf pokemon-juramento-de-arauna-en_modern.elf \
  --output review/campanha_grutas_v1/rom_interiores_encoding.json
python3 tools/arauna_maps/render_campanha_grutas_review_v1.py --base BASE_DIR
```

O lote não implementa as bordas prioritárias, Dive, SS Tidal nem o redesenho das rotas iniciais. Os exteriores e suas conexões permanecem iguais à base. A revisão de puzzles completa e o teste com save histórico continuam como verificações adicionais possíveis.

## Verificação na instalação

- Aplicado sem conflito sobre `4439f99632`; `make MODERN=1` ok; 189/189,
  95/95, 0 candidatos de resíduo e as oito verificações de mapas aprovadas.
- `validate_campanha_grutas_v1.py` aprovado em worktree limpa.
- Código revisado. As animações de água e cascata usam os tiles 424–431 do
  primário de cada caverna, fora dos slots reservados.
  `AraunaGrutas_NormalizeSavedBlock` só troca IDs antigos listados, nos
  seis bancos, preservando colisão e elevação.
- Nos 23 layouts afetados, inclusive os interiores da V1.1 em que só o banco
  mudou, colisão, elevação e comportamento são idênticos à base (12.561
  células).
- Legibilidade (paredes quase iguais a algum chão):
  - Victory Road 1F: de 694 para 180 células.
  - Seafloor Room 9: de 445 para 11.
  - Túnel do Fossil Maniac: de 146 para 0.
  - Desafios da Trick House: continuam em 0.
  - Casa da Lanette: subiu de 0 para 3.
- Emulador: as 13 grutas e os interiores revisados carregam; Victory Road B1F
  e B2F continuam escuras sem Flash, como no original.
- Placar de conteúdo: 353 mapas com arte Arauna e 175 iguais ao original.

### Pendência de arte

Na Victory Road, as paredes ficaram como tufos azulados repetidos sobre a
areia, sem a faixa ocre nem o volume de penhasco da folha de conceito. A
água tem bordas retas, sem margem. O Seafloor está mais próximo do
conceito, mas também sem altura nas paredes.
