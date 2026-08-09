# Teste de cura e whiteout

## Validação automática

```sh
python3 scripts/validate_safe_recovery.py
```

O script confere a nova heal location, a coordenada de retorno, a colisão do
mapa, o registro após o inicial, a cura repetível e os textos bilíngues.

## Teste manual no mGBA

1. Escolha o inicial, saia do Centro e salve o jogo.
2. Volte e fale com a Dra. Maia após sofrer dano; a equipe deve ser curada.
3. Perca para um selvagem da Rota da Neblina.
4. Confirme o retorno à frente do Centro de Pesquisa com a equipe restaurada.
5. Confirme que inicial, Pokédex, kit, capturas e estágio da história persistem.
6. Repita o whiteout contra Nilo e contra o agente técnico.
7. Salve, recarregue e repita uma cura para validar o checkpoint persistente.

O teste deve ser repetido em português e inglês. Nenhuma aprovação de sprite é
necessária porque esta etapa não altera recursos gráficos.
