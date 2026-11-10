# Plugin Vendas

Um ajudante de vendas para o Claude (Cowork e Claude Code). Ele cuida do dia a dia do vendedor: prepara reuniões, resume e faz o follow-up, pesquisa empresas, cuida dos negócios, revisa o funil e escreve a previsão de vendas.

Funciona com as ferramentas que o seu time já usa (CRM, e-mail, agenda, chat e gravador de reuniões). Se nada estiver conectado, funciona com planilhas e textos que você enviar.

## Instalação

```bash
claude plugin marketplace add jaquelineamaro93-hue/skills-IA
```
```bash
claude plugin install vendas@skills-ia
```

## Como funciona, em 4 frases

- **Você pede em português normal.** "Me prepara para a reunião com a Acme" já chama a skill certa. Ou chame pelo nome, por exemplo `/vendas:resumir-reuniao`.
- **Ele só muda algo quando você manda.** Atualizar o CRM, enviar e-mail, postar no chat e marcar reunião só acontecem se você pedir. O que ele sugerir sozinho aparece antes, com a prova do porquê.
- **E-mail de cliente não dá ordem para ele.** E-mails, gravações e mensagens são lidos como informação. Se um e-mail "pedir" alguma ação, ele mostra para você antes.
- **Sem ferramenta conectada também funciona.** Envie a exportação do funil, a transcrição ou a lista de clientes, e ele trabalha com isso.

## As 36 skills

### Seu dia

| Skill | O que faz |
|---|---|
| `primeiros-passos` | Mostra o que está conectado, aprende como você escreve e já monta um painel inicial |
| `resumo-do-dia` | Resumo da manhã: reuniões de hoje, negócios fechando, e-mails esperando, ações principais |
| `preparar-reuniao` | Uma página antes da reunião: quem vai, histórico, o que foi dito antes, perguntas para fazer |
| `resumir-reuniao` | Da gravação ou anotação, sai o e-mail de follow-up, o resumo para o time e o que atualizar no CRM |
| `limpar-caixa-de-entrada` | Separa os e-mails de clientes por prioridade e escreve as respostas |
| `marcar-reuniao` | Acha horário, escreve o convite, marca na agenda e registra no CRM |
| `registrar-no-crm` | Registra uma ligação, reunião ou e-mail no cliente e negócio certos |
| `fechar-o-dia` | Fecha o dia: reuniões processadas, CRM em dia, compromissos anotados, 3 prioridades de amanhã |
| `resumo-da-semana` | O que fechou, andou e atrasou na semana, e o que vem na segunda |

### Clientes e prospecção

| Skill | O que faz |
|---|---|
| `pesquisar-empresa` | Pesquisa uma empresa ou pessoa: o que fazem, notícias, prioridades e se combinam com seu cliente ideal |
| `tudo-sobre-um-cliente` | Um resumo de tudo sobre um cliente: CRM, e-mails, documentos, gravações e chat do time |
| `quem-decide-a-compra` | Mapa das pessoas do negócio: quem decide, quem influencia, quem falta e por onde entrar |
| `escrever-mensagem-de-prospeccao` | E-mail personalizado ou sequência de contatos, e inclusão numa cadência se você pedir |
| `escolher-melhores-leads` | Dá nota a um lead ou ordena uma lista pelo encaixe com o cliente ideal |
| `enviar-lead-para-vendedor` | Decide quem fica com um lead sem dono e escreve o recado de passagem |
| `priorizar-clientes` | Separa sua carteira em grupos A, B e C para mostrar onde focar |
| `plano-para-um-cliente` | Cria ou atualiza o plano estratégico de um cliente |
| `vender-mais-para-clientes` | Acha onde dá para vender mais para quem já é cliente, com evidência |

### Negócios

| Skill | O que faz |
|---|---|
| `revisar-negocio` | Análise funda de um negócio: nota de saúde, riscos, o que falta e próximos passos |
| `o-que-falta-para-avancar` | O que precisa acontecer para o negócio avançar e fechar, com quem e quando |
| `sinais-do-negocio` | Alertas da carteira: negócios parados, datas escorregando, troca de pessoas, concorrente |
| `e-se-a-venda-atrasar` | Simula o efeito na meta se um negócio atrasar, diminuir ou for perdido |
| `plano-para-fechar-venda` | Caso de negócio e plano de ação conjunto até a assinatura |
| `responder-objecao` | Como responder uma objeção, com provas do seu próprio histórico |
| `comparar-concorrentes` | Como ganhar de um concorrente num negócio, e cartões de batalha para o time |
| `criar-material-de-venda` | Apresentação, one-pager ou material para o cliente, sem número inventado |
| `atualizar-negocio-no-crm` | Muda etapa, data, próximo passo, valor ou categoria, mostrando o antes e depois |

### Funil e previsão

| Skill | O que faz |
|---|---|
| `revisar-funil` | Saúde do funil por etapa: cobertura, negócios envelhecendo, conversão e riscos |
| `arrumar-crm` | Revisa o CRM atrás de campos vazios, datas vencidas e etapas erradas |
| `previsao-de-vendas` | O texto da previsão para a reunião de forecast ou o 1:1 com o gestor |
| `funil-do-time` | Visão do gestor: funil por vendedor e etapa, riscos e onde treinar |
| `preparar-conversa-com-vendedor` | Prepara o gestor para o 1:1 com um vendedor |
| `por-que-ganhamos-ou-perdemos` | Padrões nos negócios fechados: onde perdemos, objeções, o que faz ganhar |

### Clientes atuais

| Skill | O que faz |
|---|---|
| `saude-do-cliente` | Saúde do cliente e preparação da reunião trimestral (QBR) |
| `o-que-os-clientes-dizem` | Citações literais dos clientes sobre um assunto, tiradas de gravações e e-mails |
| `renovacoes-chegando` | Renovações que estão chegando, com prazo, risco e chance de aumentar |

## Exemplos

**Depois de uma reunião:** digite `/vendas:resumir-reuniao` e cole suas anotações ou a transcrição. Você recebe o resumo, o rascunho do e-mail de follow-up, o resumo para o time e as atualizações sugeridas no CRM. Nada é gravado nem enviado sem você mandar.

**Reunião de previsão:** "Escreve minha previsão deste trimestre." A skill `previsao-de-vendas` lê seus negócios abertos (ou a exportação do funil) e escreve o que vai fechar, o que pode fechar, o que mudou e onde está o risco.

**Antes de falar com uma empresa nova:** "Pesquisa a Acme antes da minha call amanhã." A skill `pesquisar-empresa` traz o que a empresa faz, notícias recentes, prioridades prováveis, se ela combina com seu cliente ideal e se ela já está no seu CRM.

## Funciona com arquivos, melhor com as suas ferramentas

| O que você quer | Sem nada conectado | Com ferramentas conectadas |
|---|---|---|
| Resumir reunião e fazer follow-up | Cole anotações ou transcrição | Gravador de reuniões, e-mail, CRM, chat |
| Revisar funil e previsão | Envie a exportação do funil | CRM |
| Pesquisar empresas | Busca na web e o que você contar | Enriquecimento de dados, CRM |
| Preparar reuniões | Descreva a reunião | Agenda, CRM, e-mail, gravador |
| Escrever prospecção | Busca na web e o que você contar | E-mail, CRM, ferramenta de cadência |
| Atualizar o CRM | Recebe um checklist para aplicar à mão | CRM |
| Marcar reuniões | Recebe o convite pronto para enviar | Agenda, CRM |

Sem nada conectado, a skill diz claramente o que usou e o que não conseguiu ver.

## Ferramentas que conectam

| Tipo | Exemplos | O que libera |
|---|---|---|
| **CRM** | HubSpot, Close, Salesforce | Negócios, clientes, contatos, atualizações |
| **E-mail e agenda** | Gmail, Google Agenda, Calendly, Microsoft 365 | Conversas, rascunhos, reuniões, agendamento |
| **Gravador de reuniões** | Gong, Fireflies, Zoom, Otter.ai | Transcrições e histórico de reuniões |
| **Enriquecimento de dados** | Clay, ZoomInfo, Apollo, Lusha, Crunchbase | Dados de empresas e contatos |
| **Chat** | Slack, Microsoft Teams | Contexto do time e resumos nos canais |

Salesforce e Microsoft 365 (Outlook, Teams, SharePoint) estão incluídos, mas o administrador da empresa precisa liberar cada um no Claude antes de as pessoas entrarem; no Salesforce, isso inclui configurar o app da empresa. A lista completa está em [CONNECTORS.md](CONNECTORS.md).

## Para administradores

As permissões de cada conector controlam o que pode rodar: cada ferramenta pode ser permitir, perguntar ou bloquear, e as skills nunca passam disso. Se uma ferramenta de escrita estiver bloqueada, a skill continua funcionando e entrega um checklist para a pessoa aplicar à mão.

Para execuções agendadas (o resumo da manhã, os alertas semanais), deixe as ferramentas de enviar, postar e gravar em **perguntar**, para nada sair ou mudar sem uma pessoa aprovar.

## Origem e licença

Obra derivada do plugin de vendas de código aberto da Anthropic (Apache 2.0), traduzida e adaptada para o português por Jaqueline Amaro. Veja [LICENSE](LICENSE) e [NOTICE](NOTICE).
