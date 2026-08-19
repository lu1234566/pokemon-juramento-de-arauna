# Museu de Porto do Sal — exposicoes cientificas

## Escopo

Esta camada completa a superficie visivel do antigo Oceanic Museum sem alterar nenhuma interacao, objeto ou progressao.

Arquivos de jogo renderizados apenas durante o build:

- `data/maps/SlateportCity_OceanicMuseum_1F/scripts.inc`
- `data/maps/SlateportCity_OceanicMuseum_2F/scripts.inc`

## 1F

Nove paineis/exposicoes foram localizados para PT-BR e mantidos como divulgacao cientifica:

1. experimento de redemoinho;
2. experimento de queda d'agua;
3. solo oceanico e sedimentacao;
4. formacao de areia costeira;
5. por que o mar parece azul;
6. por que o mar e salgado;
7. proporcao aproximada entre mar e terra;
8. fossil de marca de onda;
9. medidor de profundidade por ecos.

A curadoria evita usar cada painel como exposicao de lore. O Museu continua parecendo uma instituicao oceanografica civil de verdade.

## 2F

Dez exposicoes foram curadas:

- duas amostras de agua;
- pressao em profundidade;
- modelo da regiao de Arauna;
- correntes profundas;
- correntes de superficie;
- barco de linha;
- submersivel de pesquisa;
- sonda submersivel nao tripulada;
- navio historico.

Foram removidas referencias visiveis a `LITTLEROOT`, `S.S. TIDAL`, `STERN'S SHIPYARD`, `S.S. ANNE`, `ABANDONED SHIP` e `DEWFORD` dentro deste conjunto.

## Visitantes restantes

Tres falas humanas do 2F tambem foram fechadas:

- lembranca de um navio encalhado na costa;
- aviso para nao correr no Museu;
- desejo de viajar em um submersivel de pesquisa.

## Seguranca

O renderer `scripts/render_porto_sal_museum_science.py`:

- exige labels exatos;
- exige marcadores da superficie anterior;
- limita cada segmento visivel a 32 caracteres;
- mascara somente os blocos `.string` para confirmar que a estrutura executavel nao mudou;
- possui `--check` e `--in-place`.

O build aplica as camadas do Museu na ordem:

1. pessoas/fila;
2. confronto e Pecas Oceanicas;
3. exposicoes cientificas.

Nenhum `scripts.inc` do Museu e commitado ja renderizado.

## Auditoria global

`scripts/audit_visible_residue_rendered.py` compoe as camadas do Museu sobre o auditor existente. Dessa forma o relatorio passa a refletir a superficie que chega a ROM, em vez de contar como residuos textos-fonte que os renderers substituem durante o build.

## Preservado

Continuam intactos:

- ingresso e fluxo de dinheiro;
- TM do agente familiar;
- `ITEM_DEVON_GOODS` interno;
- batalhas do 2F;
- flags e vars;
- movimentos;
- objetos;
- warps;
- saves;
- progressao Emerald.

Sem arte, sem Codespaces e sem alteracao do PR legado #58.
