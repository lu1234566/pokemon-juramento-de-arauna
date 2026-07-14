# Greybox — Vila das Araucárias

## Estado

Este é o primeiro layout independente de Arauna. Ele substitui apenas o terreno
temporário do `AraunaMapLab`; scripts, NPCs, flags e batalha continuam separados
e preservados.

O greybox usa os tilesets vanilla `General` e `Petalburg` como placeholders.
Nenhum edifício ou elemento visual desta fase é arte final.

## Intenção espacial

| Zona | Função nesta fase | Direção futura |
| --- | --- | --- |
| Norte | duas construções de referência | casas da família e da pesquisadora |
| Centro | clareira e cruzamento principal | praça sob uma araucária ancestral |
| Leste | área livre de encontro | acesso à primeira rota e ponto de Nilo |
| Sudoeste | construção técnica maior | centro comunitário/laboratório |
| Sul | continuação do eixo principal | saída narrativa bloqueada no prólogo |

## Pontos preservados

| Elemento | Coordenada | Papel |
| --- | --- | --- |
| Entrada do jogador | (10, 13) | chegada segura no eixo central |
| Pesquisadora | (12, 13) | parceiro técnico e retorno |
| Nilo | (16, 10) | batalha de validação |
| Kit de campo | (14, 17) | item persistente de uso único |

Todos esses pontos usam blocos transitáveis no greybox.

## Regras de edição

- O layout `LAYOUT_ARAUNA_MAP_LAB` pode ser editado sem afetar Hoenn.
- O tamanho inicial permanece 20 × 20 para preservar o fluxo já testado.
- Antes de mover um evento, atualize também a tabela de pontos preservados.
- Não crie interiores definitivos até a circulação externa ser aprovada.
- Não substitua os tilesets enquanto os sprites e a direção visual não estiverem definidos.

## Próxima iteração

1. validar o novo layout no Porymap e no mGBA;
2. ajustar circulação e escala;
3. definir a silhueta da araucária central;
4. criar um tileset autoral provisório;
5. promover o laboratório técnico à primeira versão da Vila das Araucárias.
