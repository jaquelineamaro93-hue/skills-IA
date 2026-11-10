# Plugin Desenvolvimento de Software

Um ajudante para times que **criam e mantêm sistemas e aplicativos** (programadores, tech leads, times de produto e tecnologia), no Claude Cowork e no Claude Code.

Ele ajuda no dia a dia de quem programa: montar o resumo da daily, revisar código, decidir a arquitetura, achar e corrigir erros, agir quando o sistema cai, conferir tudo antes de publicar, planejar testes e escrever documentação.

Funciona sozinho (você cola o código ou descreve o problema) e fica melhor quando você conecta o repositório de código, a ferramenta de tarefas e o monitoramento.

## Instalação

```bash
claude plugin marketplace add jaquelineamaro93-hue/skills-IA
```
```bash
claude plugin install desenvolvimento-de-software@skills-ia
```

## As 10 skills

Você pode pedir em português normal ("revisa esse código", "o sistema caiu") ou chamar pelo nome, por exemplo `/desenvolvimento-de-software:revisar-codigo`.

| Skill | O que faz |
|---|---|
| `resumo-da-daily` | Monta o seu resumo da daily (ontem / hoje / travas) a partir de commits, PRs, tarefas e chat |
| `revisar-codigo` | Revisa código atrás de falhas de segurança, lentidão, erros e estilo |
| `achar-e-corrigir-erro` | Sessão passo a passo para reproduzir, isolar, achar a causa e corrigir um erro |
| `decidir-arquitetura` | Registro de decisão de arquitetura (ADR) com opções, prós e contras |
| `desenhar-sistema` | Desenho de sistemas: componentes, API, modelo de dados, escala |
| `sistema-fora-do-ar` | Resposta a incidente: gravidade, comunicação, resolução e análise final |
| `checklist-antes-de-publicar` | Checklist para conferir tudo antes de colocar uma versão no ar |
| `plano-de-testes` | Estratégia e plano de testes: o que testar e de que jeito |
| `codigo-para-arrumar` | Encontra e prioriza o que precisa ser arrumado no código (dívida técnica) |
| `escrever-documentacao` | README, documentação de API, roteiros de operação e guias para quem chega |

## Exemplos

**Daily:** `/desenvolvimento-de-software:resumo-da-daily`. Com as ferramentas conectadas, ele junta seus commits, PRs e tarefas. Sem elas, conte o que você fez e ele organiza.

**Revisão de código:** `/desenvolvimento-de-software:revisar-codigo https://github.com/org/repo/pull/123`. Mande o link do PR, cole o diff ou aponte os arquivos.

**Erro:** `/desenvolvimento-de-software:achar-e-corrigir-erro Os usuários estão vendo erro 500 na página de pagamento`.

**Arquitetura:** `/desenvolvimento-de-software:decidir-arquitetura Usamos fila de mensagens ou chamadas diretas entre os serviços?`

**Sistema fora do ar:** `/desenvolvimento-de-software:sistema-fora-do-ar O serviço de pagamentos está devolvendo erro 503`.

**Antes de publicar:** `/desenvolvimento-de-software:checklist-antes-de-publicar servico-de-login v2.3.0`.

## Sozinho ou com as suas ferramentas

| O que você quer | Sozinho | Melhor com |
|---|---|---|
| Resumo da daily | Conte o que fez | Repositório de código, gestão de tarefas, chat |
| Revisar código | Cole o diff ou o código | Repositório de código (puxa o PR sozinho) |
| Corrigir erro | Descreva o problema | Monitoramento (logs e métricas) |
| Decidir arquitetura | Descreva o sistema | Base de conhecimento (decisões anteriores) |
| Sistema fora do ar | Descreva o incidente | Monitoramento, gestão de incidentes, chat |
| Checklist antes de publicar | Descreva a publicação | CI/CD, repositório de código |

## Ferramentas que conectam

| Tipo | Exemplos | O que libera |
|---|---|---|
| **Repositório de código** | GitHub, GitLab | Diffs de PR, histórico de commits, branches |
| **Gestão de tarefas** | Linear, Jira, Asana | Situação das tarefas, sprints, responsáveis |
| **Monitoramento** | Datadog, New Relic | Logs, métricas, alertas, painéis |
| **Gestão de incidentes** | PagerDuty, Opsgenie | Plantão, acompanhamento e acionamento |
| **Chat** | Slack, Teams | Conversas do time, canal da daily |
| **Base de conhecimento** | Notion, Confluence | Decisões de arquitetura, roteiros, guias |

A lista completa está em [CONNECTORS.md](CONNECTORS.md).

## Origem e licença

Obra derivada do plugin de engenharia de código aberto da Anthropic (Apache 2.0), traduzida e adaptada para o português por Jaqueline Amaro. Veja [LICENSE](LICENSE) e [NOTICE](NOTICE).
