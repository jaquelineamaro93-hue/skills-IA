# Conectores

## Como as skills falam das ferramentas

Nos arquivos, `~~tipo` é um apelido para qualquer ferramenta daquele tipo que você conectar. Por exemplo, `~~source control` pode ser GitHub, GitLab ou outro repositório de código com servidor MCP.

O plugin não depende de uma marca: as skills falam do tipo de ferramenta (repositório de código, CI/CD, monitoramento etc.). O `.mcp.json` já traz alguns servidores configurados, mas qualquer servidor do mesmo tipo funciona.

## Conectores deste plugin

| Tipo | Apelido | Já incluídos | Outras opções |
|------|---------|--------------|---------------|
| Chat | `~~chat` | Slack | Microsoft Teams |
| Repositório de código | `~~source control` | GitHub | GitLab, Bitbucket |
| Gestão de tarefas | `~~project tracker` | Linear, Asana, Atlassian (Jira/Confluence) | Shortcut, ClickUp |
| Base de conhecimento | `~~knowledge base` | Notion | Confluence, Guru, Coda |
| Monitoramento | `~~monitoring` | Datadog | New Relic, Grafana, Splunk |
| Gestão de incidentes | `~~incident management` | PagerDuty | Opsgenie, Incident.io, FireHydrant |
| CI/CD | `~~CI/CD` | — | CircleCI, GitHub Actions, Jenkins, BuildKite |
