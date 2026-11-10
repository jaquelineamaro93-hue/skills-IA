# Conectores

## Como as skills falam das ferramentas

O plugin não depende de uma marca. As skills falam do tipo de ferramenta ("o CRM", "o e-mail", "a agenda", "as gravações"), então qualquer conector daquele tipo funciona. O arquivo `.mcp.json` já traz alguns servidores configurados, mas qualquer servidor do mesmo tipo serve.

Toda skill também funciona sem nada conectado: envie uma exportação ou cole anotações, e ela trabalha com isso.

## Conectores deste plugin

| Tipo | Apelido | Já incluídos | Outras opções |
|------|---------|--------------|---------------|
| CRM | `~~CRM` | HubSpot, Salesforce\*, Close, Monday | Pipedrive, Attio, Zoho CRM, Copper |
| E-mail | `~~email` | Gmail, Microsoft 365 (Outlook)\* |  |
| Agenda | `~~calendar` | Google Agenda, Calendly, Microsoft 365 (Outlook)\* |  |
| Chat | `~~chat` | Slack, Microsoft 365 (Teams)\* |  |
| Documentos e base de conhecimento | `~~knowledge base` | Google Drive, Notion, Atlassian (Confluence), Microsoft 365 (SharePoint)\* | Box, Dropbox, Guru |
| Gravador de reuniões | `~~conversation intelligence` | Gong, Fireflies, Zoom, Otter.ai | Granola, Fathom, Chorus |
| Enriquecimento de dados | `~~data enrichment` | Clay, ZoomInfo, Apollo, Lusha, Crunchbase | Clearbit |
| Cadência de vendas | `~~sales engagement` | Outreach, Apollo | Salesloft |
| Inteligência competitiva | `~~competitive intelligence` | Similarweb | Crayon, Klue |
| Gestão de projetos | `~~project tracker` | Atlassian (Jira) | Linear, Asana |

## Salesforce e Microsoft 365

**Salesforce e Microsoft 365 (marcados com \* acima) estão incluídos, e os dois precisam ser configurados pela empresa: um administrador libera o conector no Claude antes de as pessoas entrarem. No Salesforce, isso inclui configurar o app da empresa.**

Depois de conectados, as skills usam esses conectores como qualquer outra ferramenta do mesmo tipo.

Google Agenda, Gmail e Google Drive estão no `.mcp.json` sem endereço. Conecte pelas configurações de conectores do Claude.

## Permissões

O que cada conector pode fazer é definido no próprio conector: permitir, perguntar ou bloquear, ferramenta por ferramenta. As skills nunca passam disso. Veja no README as configurações recomendadas para execuções agendadas.
