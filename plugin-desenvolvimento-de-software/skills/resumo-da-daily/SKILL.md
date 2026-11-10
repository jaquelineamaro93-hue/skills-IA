---
name: resumo-da-daily
description: Monta o seu resumo para a reunião diária do time (daily/standup) a partir do que você fez. Use para se preparar para a daily, resumir os commits, PRs e tarefas de ontem, organizar em ontem / hoje / travas, ou transformar anotações soltas num resumo para compartilhar.
argument-hint: "[ontem | hoje | travas]"
---

# Resumo da daily

> Se aparecer um apelido de ferramenta que você não conhece, ou quiser ver o que está conectado, veja [CONNECTORS.md](../../CONNECTORS.md).

Monta o resumo para a daily juntando o que você fez nas ferramentas.

## Como funciona

```
SEMPRE FUNCIONA
  ✓ Me conte o que você fez e eu organizo
  ✓ No formato da daily (ontem / hoje / travas)
  ✓ Curto e focado em ação

MELHOR COM AS SUAS FERRAMENTAS
  + Repositório de código: commits e PRs recentes
  + Gestão de tarefas: tarefas que mudaram de situação
  + Chat: conversas e decisões importantes
  + CI/CD: situação dos builds e publicações
```

## O que preciso de você

**Opção A: deixa que eu busco.** Com as ferramentas conectadas, é só chamar `/desenvolvimento-de-software:resumo-da-daily` que eu junto tudo.

**Opção B: me conta o que fez.** "Trabalhei na migração do login, revisei 3 PRs, travei no limite de uso da API."

## Entrega

```markdown
## Daily - [data]

### Ontem
- [item feito, com o número da tarefa se houver]
- [item feito]

### Hoje
- [item planejado, com o número da tarefa]
- [item planejado]

### Travas
- [trava, com contexto e quem pode ajudar]
```

## Se houver ferramentas conectadas

Se **~~source control** (repositório de código) estiver conectado:
- Puxe commits e PRs recentes (abertos, revisados, juntados)
- Resuma as mudanças de código por alto

Se **~~project tracker** (gestão de tarefas) estiver conectado:
- Puxe as tarefas que foram para "em andamento" ou "feito"
- Mostre os próximos itens da sprint

Se **~~chat** estiver conectado:
- Procure conversas e decisões importantes
- Aponte conversas esperando a sua resposta

## Dicas

1. **Rode toda manhã.** Vira hábito e você nunca corre atrás das anotações.
2. **Acrescente contexto.** Depois que eu gerar, complete com detalhes sobre travas e prioridades.
3. **Escolha o formato.** Peça no formato do Slack, do e-mail ou da ferramenta de daily do time.
