# Porto do Sal — mapa V5

## Objetivo

O V3 foi certificado no Arauna Map Studio com `PASS / SIM · VERIFICADO / 0E · 0A / confiança full`.
O V4 introduziu Mercado das Marés e Cais dos Engenheiros, mas a revisão visual mostrou duas costuras a melhorar.

O V5 mantém a metodologia de patches reais de Emerald e faz somente duas correções visuais:

- desloca a ala costeira do mercado dois tiles para oeste, aproximando-a do fluxo do mercado principal;
- estende o mesmo patch portuário do Cais dos Engenheiros para oeste, em direção ao estaleiro.

O pátio de sal do V4 é preservado.

## Segurança

- entrada determinística: Porto do Sal V3 certificado;
- V3 raw SHA-1: `664c661e163661cc3d5f7c4ae4cd552c2297e16c`;
- V5 raw SHA-1: `b6821b5fa6106917761c5e473725e720d10fb893`;
- 42 células diferentes do V3;
- apenas 22 células diferem do V4 revisado visualmente;
- todos os destinos permanecem `collision 0 / elevation 3`;
- bits físicos `0xFC00` preservados bit a bit;
- nenhuma célula nas caixas de movimento de NPCs, warps + cushion, BG events ou coord events é permitida pelo builder;
- nenhum `map.json`, script, texto, flag, var, save, conexão, interior, tileset ou paleta alterado;
- sem shuffle, aleatoriedade ou geometria sintética;
- nenhum GitHub Actions ou Codespaces usado.

## Arquivos

- `data/layouts/SlateportCity/map.bin`
- `tools/build_porto_sal_map_v5.py`
- `docs/PORTO_SAL_MAP_V5.md`

## Gate

Antes do merge:

1. revisar visualmente Mercado das Marés e Cais dos Engenheiros no Arauna Map Studio;
2. confirmar linguagem GBA/Emerald;
3. executar `Validar` com Workspace conectado e exigir `SIM · VERIFICADO / 0E · 0A`.
