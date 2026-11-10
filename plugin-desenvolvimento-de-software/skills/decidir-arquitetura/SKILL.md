---
name: decidir-arquitetura
description: Cria ou avalia um registro de decisão de arquitetura (ADR). Use para escolher entre tecnologias (ex.: Kafka ou SQS), registrar uma decisão de desenho do sistema com prós, contras e consequências, revisar uma proposta de arquitetura ou desenhar um componente novo a partir de requisitos e restrições.
argument-hint: "<decisão ou sistema a desenhar>"
---

# Decidir arquitetura

> Se aparecer um apelido de ferramenta que você não conhece, ou quiser ver o que está conectado, veja [CONNECTORS.md](../../CONNECTORS.md).

Cria um registro de decisão de arquitetura (ADR) ou avalia o desenho de um sistema.

## Como usar

```
/desenvolvimento-de-software:decidir-arquitetura $ARGUMENTS
```

## Modos

**Criar um ADR:** "Usamos Kafka ou SQS para os eventos?"
**Avaliar um desenho:** "Revisa essa proposta de microsserviços"
**Desenhar um sistema:** "Desenha o sistema de notificações do app"

Para o passo a passo de levantar requisitos, escala e prós e contras, veja a skill **desenhar-sistema**.

## Entrega - formato ADR

```markdown
# ADR-[número]: [título]

**Situação:** Proposta | Aceita | Descontinuada | Substituída
**Data:** [data]
**Quem decide:** [quem precisa aprovar]

## Contexto
[Qual é a situação? O que está pesando?]

## Decisão
[Qual mudança estamos propondo?]

## Opções avaliadas

### Opção A: [nome]
| Critério | Avaliação |
|----------|-----------|
| Complexidade | [Baixa/Média/Alta] |
| Custo | [avaliação] |
| Crescimento | [avaliação] |
| O time conhece? | [avaliação] |

**Prós:** [lista]
**Contras:** [lista]

### Opção B: [nome]
[mesmo formato]

## Prós e contras
[Os principais, com o raciocínio claro]

## Consequências
- [O que fica mais fácil]
- [O que fica mais difícil]
- [O que vamos precisar rever]

## Próximas ações
1. [ ] [passo de implementação]
2. [ ] [acompanhamento]
```

## Se houver ferramentas conectadas

Se **~~knowledge base** (base de conhecimento) estiver conectada:
- Procure ADRs e documentos de desenho anteriores
- Ache o contexto técnico que importa

Se **~~project tracker** (gestão de tarefas) estiver conectado:
- Ligue aos épicos e tarefas relacionados
- Crie as tarefas de implementação

## Dicas

1. **Diga as restrições logo no começo.** "Precisamos entregar em 2 semanas" ou "tem que aguentar 10 mil requisições por segundo" muda a resposta.
2. **Dê nome às opções.** Mesmo que já tenha preferência, a análise fica mais justa com alternativas claras.
3. **Inclua os requisitos que não são funções.** Velocidade, custo, conhecimento do time e manutenção importam tanto quanto as funções.
