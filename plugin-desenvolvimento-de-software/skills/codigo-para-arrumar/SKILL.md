---
name: codigo-para-arrumar
description: Encontra, organiza e prioriza o que precisa ser arrumado no código e no sistema (dívida técnica). Use quando a pessoa disser "dívida técnica", "o que a gente devia refatorar", "saúde do código", "tech debt", ou perguntar sobre qualidade do código, prioridades de refatoração ou o que está acumulado de manutenção.
---

# Código para arrumar (dívida técnica)

Encontra, organiza e prioriza com método o que precisa ser arrumado.

## Tipos

| Tipo | Exemplos | Risco |
|------|----------|-------|
| **No código** | Lógica duplicada, abstrações ruins, números mágicos | Erros, desenvolvimento lento |
| **Na arquitetura** | Sistema único que devia ser dividido, banco de dados errado | Limite para crescer |
| **Nos testes** | Pouca cobertura, testes instáveis, faltam testes de integração | Erros chegam em produção |
| **Nas dependências** | Bibliotecas desatualizadas ou abandonadas | Falhas de segurança |
| **Na documentação** | Faltam roteiros, READMEs velhos, conhecimento só na cabeça das pessoas | Novos no time sofrem |
| **Na infraestrutura** | Publicação manual, sem monitoramento, sem infraestrutura como código | Incidentes, demora para recuperar |

## Como priorizar

Dê nota de 1 a 5 a cada item em:
- **Impacto:** quanto isso atrasa o time?
- **Risco:** o que acontece se não arrumar?
- **Esforço:** quão difícil é arrumar? (quanto menor o esforço, maior a prioridade)

Prioridade = (Impacto + Risco) x (6 - Esforço)

## Entrega

Uma lista em ordem de prioridade, com o esforço estimado, o motivo de negócio de cada item e um plano em fases que dá para fazer junto com o desenvolvimento de novas funções.
