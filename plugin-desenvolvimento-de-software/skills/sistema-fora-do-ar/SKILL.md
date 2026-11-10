---
name: sistema-fora-do-ar
description: Conduz a resposta a um incidente (sistema fora do ar ou com problema grave) - avaliar a gravidade, comunicar, resolver e escrever a análise depois (postmortem). Use quando a pessoa disser "temos um incidente", "produção caiu", "o sistema está fora do ar", "o serviço de pagamentos está dando erro", trouxer um alerta para avaliar a gravidade, pedir uma atualização no meio do incidente ou quiser escrever a análise sem culpados depois de resolver.
argument-hint: "<descrição do incidente ou alerta>"
---

# Sistema fora do ar

> Se aparecer um apelido de ferramenta que você não conhece, ou quiser ver o que está conectado, veja [CONNECTORS.md](../../CONNECTORS.md).

Cuida de um incidente desde a descoberta até a análise final.

## Como usar

```
/desenvolvimento-de-software:sistema-fora-do-ar $ARGUMENTS
```

## Modos

```
/desenvolvimento-de-software:sistema-fora-do-ar novo [descrição]     # Começar um incidente
/desenvolvimento-de-software:sistema-fora-do-ar atualizar [situação] # Publicar uma atualização
/desenvolvimento-de-software:sistema-fora-do-ar analise              # Gerar a análise final (postmortem)
```

Se o modo não for dito, pergunte em que fase o incidente está.

## Como funciona

```
Fase 1: AVALIAR
  ✓ Dar a gravidade (SEV1 a SEV4)
  ✓ Ver quais sistemas e usuários foram afetados
  ✓ Definir papéis (quem coordena, quem comunica, quem resolve)

Fase 2: COMUNICAR
  ✓ Escrever a atualização interna
  ✓ Escrever o aviso para clientes (se precisar)
  ✓ Abrir a sala de guerra e o ritmo de atualizações

Fase 3: RESOLVER
  ✓ Anotar o que foi feito para conter o problema
  ✓ Montar a linha do tempo
  ✓ Confirmar que resolveu

Fase 4: ANÁLISE FINAL
  ✓ Documento sem culpados
  ✓ Linha do tempo reconstruída
  ✓ Causa raiz (5 porquês)
  ✓ Ações com responsáveis
```

## Gravidade

| Nível | Critério | Tempo de resposta |
|-------|----------|-------------------|
| SEV1 | Serviço fora do ar, todos os usuários afetados | Na hora, todo mundo |
| SEV2 | Função importante com problema, muitos usuários afetados | Em até 15 min |
| SEV3 | Problema numa função menor, alguns usuários afetados | Em até 1 hora |
| SEV4 | Problema visual ou de baixo impacto | Próximo dia útil |

## Como comunicar

Atualizações claras e com fatos, num ritmo regular. Inclua: o que está acontecendo, quem é afetado, o que estamos fazendo e quando vem a próxima atualização.

## Entrega - atualização

```markdown
## Atualização do incidente: [título]
**Gravidade:** SEV[1-4] | **Situação:** Investigando | Causa achada | Monitorando | Resolvido
**Impacto:** [quem/o que foi afetado]
**Última atualização:** [horário]

### Situação atual
[O que sabemos agora]

### O que já foi feito
- [ação 1]
- [ação 2]

### Próximos passos
- [o que vem e quando]

### Linha do tempo
| Horário | Evento |
|---------|--------|
| [HH:MM] | [evento] |
```

## Entrega - análise final (postmortem)

```markdown
## Análise do incidente: [título]
**Data:** [data] | **Duração:** [X horas] | **Gravidade:** SEV[X]
**Autores:** [nomes] | **Situação:** Rascunho

### Resumo
[2 a 3 frases em linguagem simples]

### Impacto
- [usuários afetados]
- [quanto tempo durou]
- [impacto no negócio, se der para medir]

### Linha do tempo
| Horário (UTC) | Evento |
|---------------|--------|
| [HH:MM] | [evento] |

### Causa raiz
[Explicação do que causou o incidente]

### 5 porquês
1. Por que [sintoma]? → [Porque...]
2. Por que [causa 1]? → [Porque...]
3. Por que [causa 2]? → [Porque...]
4. Por que [causa 3]? → [Porque...]
5. Por que [causa 4]? → [Causa raiz]

### O que funcionou
- [coisas que deram certo]

### O que não funcionou
- [coisas que deram errado]

### Ações
| Ação | Responsável | Prioridade | Prazo |
|------|-------------|------------|-------|
| [ação] | [pessoa] | P0/P1/P2 | [data] |

### Aprendizados
[O principal que o time leva disso]
```

## Se houver ferramentas conectadas

Se **~~monitoring** (monitoramento) estiver conectado:
- Puxe os detalhes do alerta e as métricas
- Mostre os gráficos das métricas afetadas

Se **~~incident management** (gestão de incidentes) estiver conectado:
- Crie ou atualize o incidente no PagerDuty/Opsgenie
- Acione quem está de plantão

Se **~~chat** estiver conectado:
- Publique as atualizações no canal do incidente
- Crie o canal da sala de guerra

## Dicas

1. **Comece a escrever na hora.** Não espere ter tudo; atualize conforme descobre.
2. **Atualizações com fatos.** O que sabemos, o que fizemos, o que vem. Sem palpite.
3. **Análise sem culpados.** O foco é nos sistemas e processos, não nas pessoas.
