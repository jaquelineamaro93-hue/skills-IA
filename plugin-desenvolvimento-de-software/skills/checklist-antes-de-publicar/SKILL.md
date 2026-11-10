---
name: checklist-antes-de-publicar
description: Checklist para conferir tudo antes de colocar uma versão do sistema no ar (deploy). Use quando for publicar uma versão, subir uma mudança com migração de banco de dados ou feature flags, conferir testes e aprovações antes de produção, ou deixar combinado antes quando voltar atrás (rollback).
argument-hint: "[serviço ou nome da versão]"
---

# Checklist antes de publicar

> Se aparecer um apelido de ferramenta que você não conhece, ou quiser ver o que está conectado, veja [CONNECTORS.md](../../CONNECTORS.md).

Gera um checklist para conferir se está tudo pronto antes de colocar no ar.

## Como usar

```
/desenvolvimento-de-software:checklist-antes-de-publicar $ARGUMENTS
```

## Entrega

```markdown
## Checklist de publicação: [serviço/versão]
**Data:** [data] | **Quem publica:** [nome]

### Antes
- [ ] Todos os testes passando no CI
- [ ] Código revisado e aprovado
- [ ] Nenhum erro crítico conhecido na versão
- [ ] Migrações de banco testadas (se houver)
- [ ] Feature flags configuradas (se houver)
- [ ] Plano para voltar atrás escrito
- [ ] Time de plantão avisado

### Durante
- [ ] Publicar em homologação e conferir
- [ ] Rodar os testes rápidos (smoke tests)
- [ ] Publicar em produção (aos poucos, se der)
- [ ] Acompanhar erros e lentidão por 15 minutos
- [ ] Conferir os fluxos principais dos usuários

### Depois
- [ ] Confirmar que as métricas estão normais
- [ ] Atualizar as notas da versão / changelog
- [ ] Avisar os interessados
- [ ] Fechar as tarefas ligadas

### Quando voltar atrás
- Taxa de erro acima de [X]%
- Tempo de resposta (P50) acima de [X] ms
- [Fluxo crítico] falhando
```

## Personalização

Conte como é a sua publicação e eu ajusto o checklist:
- "Usamos feature flags" → entra a conferência das flags
- "Tem migração de banco" → entram as checagens de migração
- "Muda a API de um jeito que quebra quem usa" → entra avisar quem consome a API

## Se houver ferramentas conectadas

Se **~~source control** (repositório de código) estiver conectado:
- Puxe a diferença da versão e a lista de mudanças
- Confira se todos os PRs foram aprovados e juntados

Se **~~CI/CD** estiver conectado:
- Veja sozinho o resultado do build e dos testes
- Confira se o pipeline está verde antes de publicar

Se **~~monitoring** (monitoramento) estiver conectado:
- Preencha os limites de "voltar atrás" pelos números atuais
- Deixe pronto o acompanhamento das métricas depois da publicação

## Dicas

1. **Use antes de toda publicação,** até as de rotina. Checklist evita o "esqueci de...".
2. **Personalize uma vez e reaproveite.** Conte como é o seu processo e eu sigo ele.
3. **Combine antes quando voltar atrás.** Decida isso antes de publicar, não no meio do problema.
