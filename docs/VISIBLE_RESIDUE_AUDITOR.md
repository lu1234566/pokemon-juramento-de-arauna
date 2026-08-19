# Auditor de residuos visiveis

`scripts/audit_visible_residue.py` inventaria texto ainda herdado do Emerald sem alterar nenhum arquivo do jogo.

## O que ele le

- `data/maps/**/scripts.inc`;
- `data/text/**/*.inc`;
- `data/scripts/**/*.inc`;
- strings localizadas com `_()` em `src/**/*.c` e `src/**/*.h`.

A fonte inglesa legitima da introducao (`data/text/arauna/en/`) e ignorada para evitar falso positivo.

## Classificacao

- **P0**: conflito canonico explicito em texto visivel, como `SCOTT`, `HOENN`, `TEAM AQUA`, `TRICK MASTER`, nomes de cidades do Emerald ou vocabulario do Battle Frontier.
- **P1**: bloco provavelmente em ingles, identificado por vocabulario e baixa presenca de portugues.

O scanner agrupa `.string` por label, portanto procura o texto que o jogador pode ler em vez de confundir nomes internos de flags, vars e scripts com residuos visiveis.

## Uso

```bash
python3 scripts/audit_visible_residue.py
python3 scripts/audit_visible_residue.py --output docs/VISIBLE_RESIDUE_INVENTORY.md
python3 scripts/audit_visible_residue.py --json /tmp/visible-residue.json
```

A geracao do inventario retorna sucesso mesmo quando encontra residuos: neste estagio ele e uma ferramenta de planejamento, nao um gate que exige traducao integral do jogo.

## Sementes manuais confirmadas em 19/08/2026

Buscas no estado atual indicam lotes de alta prioridade em:

1. superficie naval/pos-game (`SSTidalCorridor`, Reception Gate, Match Call e demais textos ligados a Scott/Frontier);
2. conjunto completo da Trick House;
3. superficies de campanha ainda contendo `TEAM AQUA`/`TEAM MAGMA`;
4. strings de sistema com `HOENN`, que precisam ser separadas de constantes internas antes de qualquer troca.

A regra continua sendo: preservar identificadores internos do Emerald e converter apenas a superficie alcançavel pelo jogador.
