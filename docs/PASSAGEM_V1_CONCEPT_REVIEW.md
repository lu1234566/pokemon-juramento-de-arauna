# Vila da Passagem V1 — revisão guiada pelas referências

A vila passa a ocupar um entroncamento rural em Y, com duas casas de telha cerâmica desencontradas, Center e Mart em ramais da estrada, bancos e pequenos bosques. A composição implementada tem 30×26 metatiles. A dimensão proposta de 28×22 foi ajustada para acomodar fachadas inteiras e os trajetos dos eventos.

## Fidelidade e origem das referências

A Master Map Design Bible, página 4, é a referência específica de Oldale: primeira vila de estrada, terra batida e madeira, três braços legíveis, ocupação ao redor do cruzamento e ausência de praça planejada. Nenhum dos seis arquivos enviados contém um PNG dedicado a Vila da Passagem. As imagens de Amanhecer e do Sul de Arauna fornecem a direção visual regional; o comparativo identifica essa distinção.

Foram usados os módulos de casas já aprovados em Amanhecer V8. Center e Mart mantêm a sinalização reconhecível e as portas animadas nativas. A loja continua com teto azul, conforme seu tutorial. Não foram alterados os interiores nem seus diálogos.

Veja `review/passagem_v1_concept_comparison.png`, `review/passagem_v1_after.png`, `review/passagem_v1_before_after.png` e `review/passagem_v1_events.png`. Os seis viewports e as três junções têm recortes individuais de 240×160. Todas as imagens de implementação vêm do terreno real; não são capturas de emulador e não incluem sprites de personagens.

## Migração funcional

| Elemento | Posição final / comportamento |
|---|---|
| Casa 1 / warp 0 | Porta (6,7) |
| Casa 2 / warp 1 | Porta (22,21) |
| Center / warp 2 | Porta (3,18); Fly em (3,19) |
| Mart / warp 3 | Porta (25,6) |
| Funcionário antes do brinde | (24,13), conduz o jogador por qualquer um dos quatro lados |
| Final do tutorial | Funcionário em (24,7); jogador em (24,8) |
| Guarda da saída oeste | (1,11) antes da aventura; volta à origem após cada bloqueio |
| Ciro | (11,25); gatilhos em (8,25), (9,25), (10,25) |
| Rota 101 | Sul, abertura x=8..11, offset 0 |
| Rota 102 | Oeste, abertura y=10/11, offset 0 |
| Rota 103 | Norte, abertura x=18..21, offset +10; retorno com −10 |

Há 4 warps, 4 objetos, 4 gatilhos e 5 eventos de placa. Quatro eventos de placa são as metades dos painéis integrados dos serviços. Somente uma placa avulsa foi colocada. A ocupação em Y não depende de uma coleção de letreiros.

As flags de visita, início da aventura, brinde, mochila cheia e Ciro, bem como os destinos e os textos, foram preservadas. Os movimentos foram adaptados. O funcionário ganhou a quarta abordagem, agora acessível. Ciro mantém as duas mensagens e a saída pela Rota 101. O renderer inglês existente valida dez blocos e preserva o código fora dos diálogos.

## Banco gráfico e conexões

Os mapas usam o banco `AraunaAmanhecer`. Foram reservados 18 metatiles: 0x313..0x325, exceto 0x31E. São cópias das peças nativas de serviços com a grama remapeada para a paleta local; atributos, IDs das portas, imagens e paletas existentes permanecem intactos. Não há novos tiles de hardware nem mudanças no motor. O slot 0x31E foi evitado porque aparece na coluna adicional carregada da Rota 110.

Route102 e Route103 passam a selecionar o banco compatível, que conserva suas peças nativas. Seus terrenos permanecem na versão anterior. O teste compara seus renders, os de Amanhecer/Route101 e as bordas visíveis de Petalburg/Route110. A seleção do banco não redesenha essas rotas.

## Verificação realizada

- 406 células transitáveis conectadas; portas, retorno dos interiores, placas e Fly alcançáveis.
- Fachadas e árvores inteiras; três aberturas externas sem vazamentos de colisão.
- Quatro percursos do tutorial do Mart, três bloqueios oeste repetidos, três aproximações de Ciro e saída da variante de conversa.
- Verificação de trajetos e ocupação de tiles considerando atrasos. Não substitui teste de temporização no emulador.
- Seis cópias de conexão executadas no compilador do ambiente com as funções C reais do motor: 1.209 células, offsets 0/+10/−10, sem extrapolar o buffer.
- Conversão nativa `mapjson` de OldaleTown e das três rotas; renderer inglês; construção determinística.
- Aplicador com conferência prévia, cópia anterior, mescla restrita dos registros compartilhados, reaplicação sem efeito e rejeição de conteúdo conflitante antes de escrever.

Os recibos estão em `review/passagem_v1_validation.json`, `review/passagem_v1_connection_probe.json`, `review/passagem_v1_integration.json` e `review/passagem_v1_package_check.json`. O último recibo documenta a reprodução após extração, hashes, compilação de eventos e casos de instalação.

Build completo da ROM e execução em emulador continuam pendentes. O ambiente não tem o compilador ARM nem a cadeia completa de conversão gráfica. A entrega é um pacote de integração revisável, não uma ROM pronta.

## Aplicação

Pré-requisitos: Vila Amanhecer V8 e Rota 101 V1 aplicadas. A base do patch é o commit local `88d122aa16ef9bdda50fb2e239eea367344c37c0`. Não houve merge, push nem GitHub Actions.

```sh
python3 tools/apply_passagem_v1.py --target /caminho/do/projeto --check
python3 tools/apply_passagem_v1.py --target /caminho/do/projeto
```

O aplicador atualiza nove arquivos: mapa, borda, eventos e scripts de Oldale; conexão de retorno de Route103; registros de layouts e Fly; dois arquivos de metatiles. Os registros não envolvidos e slots não usados são preservados. As paletas JASC aceitam LF ou CRLF sem mudar cores. Alterações em dependências conectadas exigem revisão; o aplicador as recusa antes de escrever.

Não copie o conteúdo inteiro do ZIP sobre outro projeto. As demais fontes são dependências e snapshots para reproduzir a revisão. `build_passagem_v1.py` reconstrói a versão da pasta de revisão e seu banco a partir do snapshot; para integração em trabalho compartilhado, use o aplicador.

```sh
python3 tools/check_passagem_v1_package.py --archive /caminho/do/pacote.zip
```

A sequência de produção da Bible, página 50, indica **Porto das Redes** após Vila da Passagem.
