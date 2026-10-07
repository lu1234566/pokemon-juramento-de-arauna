# Rota 103 V1.2 — checkpoint 02

Base: `7d40f7345ab2d84b4d8710edee30cf128c346166`. A recuperação da Bible,
concepts e inventário está no checkpoint 01. Esta é a primeira etapa de
implementação de Cavernas Lendárias + Fundo do Mar V1.

## Mudança concluída

As 111 células bloqueadas que pareciam chão andável passam a ter moitas
densas: 68 nas ilhotas/grama e 43 na família de piso terroso e bordas. A
vegetação reutiliza os desenhos já instalados em Sul/Pampa V1.1, conservando o
piso de cada célula. Grama de encontro, água e bases de árvores não mudam.

Foram alteradas somente as quatro entradas da camada superior de cinco
metatiles, em três bancos secundários privados. Não foram criados tiles,
metatiles, paletas ou layouts. A grade e os IDs nativos permanecem intactos.
Os dois aliases de Oldale e o alias de Route110 recebem a mesma vegetação;
assim, a aparência não volta ao desenho anterior quando vista da borda.

## Validação própria

- Exatamente 111 células da Rota 103 mudaram em RGB555; zero alterações
  visuais fora desse conjunto no mapa.
- 17.755 arquivos existentes de dados, motor, constantes e gráficos
  permaneceram idênticos byte a byte. Inclui scripts, eventos, flags,
  warps, encontros, grades, atributos, animações e código de save/migração.
- Todas as 134 direções de conexão foram verificadas com o seletor C e as
  funções reais de cópia das conexões compilados no host.
- 324.096 comparações de células em oito quadros de animação. Os 40 sentidos
  com aliases do Uivo continuam exatos em RGB555. Só 21 células de cache
  mudam: duas vistas de Oldale e 19 de Route110; zero mudanças alheias.
- Auditoria oficial de mapas: oito verificações aprovadas em 528 mapas.
- Prontidão estática oficial aprovada, incluindo 189/189 verificações do
  protagonista e 95/95 de capacidade de paletas de objetos. Fontes dos 528
  mapas e 551 músicas geradas pelas ferramentas e configurações do projeto.
- Conversão idempotente e recusa de edição local desconhecida antes de
  qualquer escrita: aprovadas.

Os PNGs são renders dos dados nativos, com quatro recortes antes/depois de
240×160 e dois mapas integrais. Não são capturas do mGBA. Build ARM e teste
em emulador desta correção permanecem pendentes: o ambiente de retomada não
tem o compilador ARM nem mGBA. Os resultados de emulação da entrega anterior
foram recuperados como evidência histórica, não reaproveitados como teste V1.2.

## Reprodução

Em um checkout com o checkpoint 02 aplicado:

```sh
git worktree add --detach ../arauna-resume-base 7d40f7345ab2d84b4d8710edee30cf128c346166
python3 tools/arauna_maps/build_route103_v12.py --base ../arauna-resume-base
python3 tools/arauna_maps/validate_route103_v12.py --base ../arauna-resume-base
python3 tools/arauna_maps/render_route103_v12.py --base ../arauna-resume-base
python3 tools/arauna_maps/prepare_route103_host_checks.py
python3 tools/arauna/audit_map_data.py
bash scripts/check_arauna_static.sh
```

Requer Git, Python, Pillow e compiladores C/C++ do host. O gate de largura de
texto consulta o commit original do Emerald: um clone parcial precisa ter
esses objetos históricos disponíveis. Não confundir falta de objeto Git com
defeito nos textos. O inventário não deve ser regenerado sobre uma etapa
posterior para substituir silenciosamente o contrato de base.

## Próximo trabalho delimitado

O redesenho das cavernas, Dive e Safari ainda não começou. Não está anunciado
como concluído. O inventário congelado cobre todos os 31 mapas.

| Checkpoint seguinte | Unidade de entrega |
| --- | --- |
| 03A | Terra Cave e Marine Cave: quatro mapas, entradas e encontros preservados |
| 03B | Sealed Chamber, Ancient Tomb e Island Cave: quatro mapas e puzzles |
| 03C | Altering Cave e Artisan Cave: três mapas |
| 04A | Dive de Route124, Route126 e Sootopolis: três mapas |
| 04B | Dive de Route127, Route128 e Seafloor Cavern: três mapas |
| 04C | Os seis Dive restantes: seis mapas e entradas temporárias |
| 05 | Safari: seis setores e Rest House |
| 06 | Build, emulador, revisão do pacote integral e checkpoint final |

Nenhuma remoção de banco antigo foi feita. Isso não é necessário para esta
correção e precisa de auditoria de dependências própria. Nada foi enviado ao
GitHub. O checkpoint portátil contém os commits locais e patch binário, sem
ROM, ELF, save ou estado de emulador.

## Verificação na instalação

- O instalador foi aplicado sobre `7d40f7345a`. A árvore resultante é
  idêntica à do bundle do checkpoint 02 (`ce7900f5c4`).
  `validate_route103_v12.py` aprovou numa worktree limpa.
- Build `en` ok (ROM em 56,7%). Gates aprovados: 189/189, 95/95, 0
  candidatos de resíduo, as oito verificações de mapas e
  `variantes_troca_layout.py --verificar` 9/9. Nenhum símbolo de harness
  na ROM.
- Render próprio em RGB555: a Rota 103 muda exatamente as 111 células.
  Oldale e a Rota 110 ficam idênticas; nos bancos delas mudam só os
  aliases da faixa de borda.
- Legibilidade da Rota 103: nenhuma célula bloqueada tem o mesmo desenho
  de um chão andável (antes eram 111), e nenhuma se parece com o capim de
  encontro. Os vãos de terra entre as árvores da faixa leste são
  andáveis, como na geometria original.
- Emulador:
  - As travessias a pé Oldale↔103, 103↔110, 110↔Mauville/Slateport e
    102→Oldale chegam com VRAM e paletas iguais ao carregamento direto.
  - Fotos de antes e depois da faixa leste e das ilhotas do rio.
