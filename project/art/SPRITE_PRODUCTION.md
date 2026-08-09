# Produção gráfica — Pokémon Juramento de Arauna

## Estado do pacote recebido

- Pokédex estruturada: 386/386 registros.
- Artes de referência encontradas: 314/386 (`#001`–`#314`).
- Artes de referência ainda ausentes: 72/386 (`#315`–`#386`).
- As imagens recebidas são referências de design em 512×512 ou 1024×1024; não são sprites prontos para GBA.
- Cada referência ainda precisa de frontal, traseira, ícone, paleta shiny e perfil de animação compatíveis com o motor.

O inventário completo está em `project/art/arauna_sprite_manifest.csv`.

## Formato técnico adotado

| Recurso | Formato de trabalho | Limite |
| --- | --- | --- |
| Frontal animada | PNG indexado, 64×128, dois quadros de 64×64 | 15 cores visíveis + transparência |
| Traseira | PNG indexado, 64×64 | mesma paleta da frontal |
| Ícone | PNG indexado, 32×64, dois quadros de 32×32 | paleta compatível com ícones do motor |
| Shiny | troca de paleta, sem mudar a silhueta | 15 cores visíveis + transparência |
| Animação | quadros frontais + `frontAnimId`/`backAnimId` | movimentos já suportados pelo motor |

## Lote-piloto aprovado e integrado

| Dex | Pokémon | Frontal | Traseira | Ícone | Shiny | Animação proposta |
| --- | --- | --- | --- | --- | --- | --- |
| #001 | Caramelo | aprovada | aprovada | aprovado | aprovada | `ANIM_V_JUMPS_SMALL` / `BACK_ANIM_CONCAVE_ARC_SMALL` |
| #004 | Querô | aprovada | aprovada | aprovado | aprovada | `ANIM_V_JUMPS_BIG` / `BACK_ANIM_CONCAVE_ARC_SMALL` |
| #007 | Pimpau | aprovada | aprovada | aprovado | aprovada | `ANIM_H_PIVOT` / `BACK_ANIM_H_SLIDE` |

O lote foi aprovado em 17 de julho de 2026. Caramelo ocupa a casca de Torchic,
Querô ocupa Mudkip e Pimpau ocupa Treecko, preservando os IDs internos já usados
pelos scripts. Os gráficos foram aplicados às variantes normal e GBA; o projeto
usa o modo GBA para manter a linguagem visual de Pokémon Emerald.

## Próxima ordem de produção

1. Validar o lote integrado em batalha, menu e Pokédex quando o toolchain estiver disponível.
2. Produzir as evoluções `#002`, `#003`, `#005`, `#006`, `#008` e `#009` com a mesma linguagem visual.
3. Processar os demais `#010`–`#314` em lotes pequenos para aprovação.
4. Aguardar ou produzir referências definitivas para `#315`–`#386` antes de criar seus pacotes GBA.
