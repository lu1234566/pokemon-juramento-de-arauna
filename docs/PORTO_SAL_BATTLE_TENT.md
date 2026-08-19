# TENDA DE BATALHA de Porto do Sal

## Objetivo

Fechar a superficie jogavel da Tenda de Batalha de Porto do Sal em PT-BR sem alterar a implementacao interna de Battle Tent / Battle Factory herdada de Emerald.

A modalidade visivel passa a ser apresentada como **DESAFIO DE TROCA**.

## Cobertura

O renderer `scripts/render_porto_sal_battle_tent.py` cobre 35 blocos `.string` e 10 strings de menu/UI.

### Superficie exclusiva da Tenda

Em `data/text/battle_tent.inc`:

- recepcao;
- entrada no DESAFIO DE TROCA;
- explicacao completa da modalidade;
- save antes do desafio;
- devolucao da equipe e dos alugados;
- tres vitorias e premio;
- BOLSA cheia;
- retomada de desafio salvo;
- desclassificacao por sair sem salvar;
- regras basicas;
- parceiro de troca;
- limite de trocas;
- observacoes de troca;
- regras dos POKéMON alugados.

Em `data/maps/SlateportCity_BattleTentLobby/scripts.inc`:

- NPC da TM41 TORMENT;
- explicacao da TM41;
- visitante sobre POKéMON INSETO;
- visitante sobre poder batalhar sem equipe forte propria;
- visitante sobre variedade de alugueis.

### Interface compartilhada de aluguel/troca

A Tenda reutiliza mensagens internas da Battle Factory. Foram localizados somente os blocos que a Tenda realmente chama:

- guarda temporaria da equipe;
- escolha de alugados;
- restauracao;
- segunda e terceira batalha;
- salvar/pausar;
- desistir;
- trocar POKéMON;
- confirmacao da troca;
- encaminhamento para a sala;
- salvamento de dados.

Os dois cabecalhos do quadro de regras compartilhado tambem foram localizados.

### Premio compartilhado

A Tenda usa `BattleFrontier_BattleTowerLobby_Text_ReceivedPrize` ao entregar o premio. Apenas esse bloco da Tower foi incluido neste lote.

### Menus

Em `src/strings.c`, a camada localiza os textos globais usados pelos menus da Tenda:

- CHALLENGE -> DESAFIO;
- EXIT -> SAIR;
- BASIC RULES -> REGRAS BASICAS;
- SWAP: PARTNER -> TROCA: RIVAL;
- SWAP: NUMBER -> TROCA: NUMERO;
- SWAP: NOTES -> TROCA: NOTAS;
- BATTLE POKéMON -> POKéMON DA TENDA;
- GO ON -> CONTINUAR;
- REST -> PAUSAR;
- RETIRE -> DESISTIR.

Essas strings sao globais por design; a mudanca melhora outras interfaces que reutilizam os mesmos comandos sem alterar IDs de menu.

## Regras visiveis

A Tenda informa ao jogador que:

- sao usados tres POKéMON alugados;
- os alugados entram no Nivel 30;
- as batalhas sao individuais;
- apos uma vitoria e possivel trocar um alugado por um POKéMON do treinador derrotado;
- a terceira batalha encerra a sequencia e nao oferece nova troca;
- tres vitorias seguidas geram premio;
- pausa exige save.

## Preservado

Continuam intactos:

- `VAR_FRONTIER_FACILITY`;
- `FRONTIER_FACILITY_FACTORY`;
- `VAR_FRONTIER_BATTLE_MODE`;
- `FRONTIER_MODE_SINGLES`;
- `FRONTIER_LVL_TENT`;
- `FRONTIER_DATA_CHALLENGE_STATUS`;
- `FRONTIER_DATA_BATTLE_NUM`;
- `slateporttent_*`;
- `factory_*`;
- aluguel e troca de POKéMON;
- geracao de oponentes;
- premios;
- TM41;
- saves;
- warps;
- movimentos;
- objetos;
- flags;
- vars;
- formato de save.

O BattleRoom nao recebe alteracao: introducao do oponente, batalha, vitoria/derrota e retorno usam a mesma logica original.

## Seguranca

O renderer exige:

- cada label alvo exatamente uma vez;
- cada declaracao C alvo exatamente uma vez;
- no maximo duas linhas por pagina de texto;
- no maximo 32 caracteres por segmento visivel;
- identidade estrutural dos arquivos ASM depois de mascarar `.string`;
- aplicacao apenas em build transacional.

Os arquivos-base nao sao commitados com os textos renderizados.

## CI e auditoria

`build.yml` executa:

```sh
python3 scripts/render_porto_sal_battle_tent.py --check
```

O `audit_visible_residue_rendered.py` aplica a mesma camada antes de classificar residuos, inclusive nos textos compartilhados e em `src/strings.c`.
