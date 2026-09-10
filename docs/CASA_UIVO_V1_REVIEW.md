# Casa do Uivo V1 — revisão e integração

Esta entrega implementa o refúgio externo, a sala principal e a sala das memórias, com entrada pela Serra V4, seis extremidades de warp recíprocas, dois NPCs e onze textos ambientais. O desenho segue a composição da concept art fornecida: fachada alta entre rochas, cascata lateral, pátio com duas tochas, interiores em madeira e janela azul no memorial da mãe do Eremita.

**Escopo concluído: mapas, assets, acesso e visita ambiental.** O capítulo U03–U11, a batalha de acalmar, o Selo do Uivo e animações/legendas/replay em Libras não estão implementados. Consulte `CASA_UIVO_V1_BLUEPRINT.md` para o contrato narrativo e as diferenças de escala em relação à referência.

## Arquivos de jogo

São 63 arquivos declarados em `review/casa_uivo_v1_manifest.json`: três novos mapas/layouts; dois bancos gráficos; extensão compatível do banco da Serra; entrada e placa da trilha; registros de mapas, layouts e tilesets; texto inglês. Os nomes internos novos são `Arauna_CasaUivo_Refugio`, `Arauna_CasaUivo_Sala` e `Arauna_CasaUivo_Memorias`, anexados ao grupo narrativo existente. Os IDs anteriores não são renumerados.

Os demais arquivos do ZIP são ferramentas, dependências de reprodução, snapshots e evidências. **Não copiar o ZIP inteiro sobre o jogo.** A base aceita é a revisão da Serra V4 (`6efd240`). O instalador verifica dependências antes de escrever e preserva alterações cumulativas em layouts e pontos de cura de outras cidades.

```bash
python3 tools/apply_casa_uivo_v1.py --target /caminho/do/jogo --check
python3 tools/apply_casa_uivo_v1.py --target /caminho/do/jogo
```

O segundo comando cria um backup recuperável dos arquivos substituídos. Uma nova execução sem mudanças não escreve novamente. Se houver divergência nos dados da Serra, nos quartos novos, nos registros ou nas dependências protegidas, o instalador interrompe antes de alterar qualquer arquivo. O acesso funciona nos dois sentidos e não abre caminho que evite as cenas existentes.

## Reprodução

Requisitos locais: Python 3, Pillow, compilador C, compilador C++ e make. Os arquivos dependentes estão no ZIP.

```bash
python3 tools/build_casa_uivo_v1.py
python3 tools/validate_casa_uivo_v1.py
python3 tools/probe_casa_uivo_v1_native.py
python3 tools/build_casa_uivo_v1_review.py
python3 tools/package_casa_uivo_v1.py
python3 tools/check_casa_uivo_v1_package.py
```

O builder é determinístico. A extensão da Serra preserva todos os metatiles, gráficos e paletas anteriores; a mudança de mapa limita-se a 13 células da passagem. Os novos bancos consomem 342/496 tiles de hardware no refúgio e 170/496 nos interiores; o banco da Serra fica em 211/496. Não usam os slots reservados às animações de portas. Os PNGs são indexados em 4bpp, e os metatiles/atributos são dados nativos de 16 bits.

## Verificação executada

- Validação de tamanho, colisão, elevação, portas, saídas, retorno, objetos e aproximação a todas as interações, incluindo a janela da sala das memórias.
- Checagem dos módulos completos do refúgio e dos edifícios existentes da Serra; 20 células livres para a futura cena de sinalização.
- Preservação dos 12 warps, 16 objetos, 21 gatilhos e 16 percursos de cena anteriores da Serra. Scripts de progressão preservados; apenas a nova placa é acrescentada ao script da cidade. Dalva, flags, engine, vizinhos e interiores existentes permanecem protegidos.
- Execução de 11 funções reais do Emerald em fixtures C locais: alcance nos quatro mapas, seis acessos de chegada e oito combinações de direção inicial. Esses testes usam funções extraídas da engine com dependências controladas.
- Compilação nativa via `mapjson`: quatro mapas e os registros compartilhados, total de 20 saídas geradas. A política English-only existente passa; os novos textos são gravados diretamente em inglês e não mudam a ordem de renderizadores.
- Renders do `map.bin`, camadas de eventos, comparação com a concept e sete recortes de 240 × 160. A prévia da sala usa os frames nativos parados dos NPCs registrados.
- Pacote extraído em pasta limpa, reprodução determinística, verificação de hashes, integração idempotente, preservação de alterações alheias e recusa de cinco conflitos antes de escrever.

As imagens são renders reproduzíveis dos arquivos nativos, não screenshots de emulador. As provas C e `mapjson` não equivalem a compilar ou jogar a ROM completa. Não há toolchain ARM nem emulador disponíveis no ambiente; permanecem necessários o build final da ROM e o teste visual/runtime real. Cachoeira e tochas são estáticas, e os NPCs usam sprites genéricos até receberem arte própria.

Nenhum push, merge, GitHub Actions ou alteração no PR legado foi executado.

## Evidências

- `review/casa_uivo_v1_after.png`: conjunto final.
- `review/casa_uivo_v1_concept_comparison.png`: cada ambiente ao lado da referência.
- `review/casa_uivo_v1_viewports.png`: telas de revisão.
- `review/casa_uivo_v1_validation.json`, `native_probe.json`, `mapjson.json` e `package_check.json` (com o prefixo `casa_uivo_v1_`): resultados reproduzíveis.
- `review/casa_uivo_v1_source/sha256.json`: inventário dos dados preservados.

Próximo item da sequência de mapas do Design Bible: Pampa da Espera. A implementação narrativa completa do Uivo continua explicitamente pendente conforme o blueprint.
