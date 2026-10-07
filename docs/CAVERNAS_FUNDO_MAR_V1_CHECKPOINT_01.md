# Cavernas Lendárias + Fundo do Mar V1 — checkpoint 01

Recuperação e inventário concluídos em 07/10/2026. Este checkpoint não altera
o jogo. A correção da Rota 103 pertence ao checkpoint 02.

## Base recuperada

- `main`: `979fb6c1b6731561f3c993efd6045a9bbf096c54`, de 11/09/2026.
- Base de trabalho: `7d40f7345ab2d84b4d8710edee30cf128c346166`, branch
  `claude/pokemon-juramento-arauna-fhk6ah`, com 81 commits posteriores ao main.
- Inclui Sul/Pampa V1, Sul/Pampa V1.1 + Uivo Norte V1, Grutas V2 e os
  interiores de rota anteriores. Não restaurar o overlay 71 por cima desta base.

Foram recuperados a Bible de 55 páginas e 82 concepts PNG únicos. Os ZIPs
passaram em CRC, os PNGs abriram e o PDF avulso coincide byte a byte com o PDF
do pacote da Bible. As 96 ocorrências de PNG nos pacotes selecionados incluem
duplicatas; não são 96 concepts diferentes. A prancha de superfície separada,
já contida no pacote de rotas/cavernas, não precisou de nova extração.

Foram conferidos todos os hashes de 938 arquivos do Sul V1 e 1.144 do Uivo V1.
O conteúdo dos dois ZIPs está íntegro. Na branch atual, nove arquivos do Sul
mudaram na etapa posterior; cinco arquivos do Uivo diferem da entrega original:
dois `border.bin`, o registro de layouts, o relatório e a validação de ROM.
Essas diferenças são documentadas na seção “Verificação na instalação” do
relatório instalado: bordas externas de árvores e variante sem Mirage Tower.

O checkpoint 71 foi recuperado para comparação e arquivo. Dos seus 5.349
arquivos de payload, 2.719 coincidem, 1.600 não estão no checkout atual e 1.030
diferem. Isso não certifica perda de trabalho: `docs/INTEGRACAO_42_MAPAS.md`
documenta sua integração seletiva sobre a branch com alterações posteriores de
idioma, progressão e motor. Os arquivos e validadores antigos não devem ser
copiados cegamente, nem os 71 testes antigos usados como aprovação desta base.

## Escopo técnico congelado

| Frente | Mapas técnicos |
| --- | ---: |
| Sete sistemas de cavernas | 11 |
| Dive | 12 |
| Safari, incluindo Rest House | 7 |
| Rota 103 V1.2 | 1 |
| Total | 31 |

O contrato registra 39 warps, 68 objetos, dois gatilhos por coordenada, 76
eventos de fundo e 29 conexões, além das flags, variáveis, comandos funcionais,
metatiles produzidos por scripts e dependências transitivas.

As cavernas são Terra Cave, Marine Cave, Sealed Chamber, Ancient Tomb,
Island Cave, Altering Cave e Artisan Cave. Sete sistemas não significam sete
arquivos: entradas, salas finais e pisos são mapas próprios. Os 12 Dive usam o
prefixo `Underwater_`. Os dois interiores submersos do Navio Perdido já têm
layouts Arauna e ficam como dependências protegidas fora desse lote.

`DesertRuins` também fica protegido fora do redesenho: o puzzle de Sealed
Chamber abre as câmaras relacionadas. As regras do Safari, bicicletas, pontos
de descanso, retorno, conexões Dive/emerge e entradas temporárias das cavernas
fazem parte do contrato. Battle Frontier, bases secretas e Navel Rock seguem
fora do escopo de arte.

## Autoridade e próximas etapas

Roteiro canônico: nomes e função narrativa. Scripts, eventos, flags, warps e
progressão atuais: autoridade funcional. Bible: geografia e identidade.
Concepts: composição e paleta; rótulos antigos não renomeiam slots.

As sete cavernas adicionais, Safari e fundo do mar não têm pranchas dedicadas
entre os 82 concepts recuperados. Precisam de um suplemento de design antes
da implementação. A ausência de referência dedicada não autoriza substituir
os puzzles ou inventar encontros. Os layouts antigos não são autoridade
artística, mas uma alteração de geometria exige migração conjunta do contrato.

1. Checkpoint 02: corrigir as 111 células da Rota 103 e seus aliases de borda.
2. Checkpoint 03: suplemento e implementação das sete cavernas, com
   preservação dos puzzles, entradas temporárias e condições de encontros.
3. Checkpoint 04: os 12 Dive, alinhamento com a superfície, emersão e bordas.
4. Checkpoint 05: os sete mapas do Safari e validação do fluxo de retorno.
5. Checkpoint 06: build da ROM e revisão em emulador do pacote completo.

Cada etapa deve ser reproduzível e entregue separadamente. Não chamar renders
de dados nativos de captura do emulador. Não distribuir ROM, ELF, save, estado
ou harness de depuração. Nenhuma alteração desta retomada foi enviada ao GitHub.

## Evidências

- `review/cavernas_fundo_mar_v1/recovery_audit.json`
- `review/cavernas_fundo_mar_v1/concept_provenance.json`
- `review/cavernas_fundo_mar_v1/functional_inventory.json`
- `tools/arauna_maps/inventory_cavernas_fundo_mar_v1.py`
