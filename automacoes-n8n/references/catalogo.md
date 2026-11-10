# Catálogo dos 24 templates

Todos vêm **desligados**, com credenciais marcadas `[Reconfigurar]`, textos de exemplo `SEU_..._AQUI` e uma nota
**README_SETUP** dentro do fluxo com o passo a passo.

## CRM e vendas (`templates/crm-e-vendas/`)
| Arquivo | O que faz | Ferramentas |
|---|---|---|
| `cartpanda-para-kommo.json` | Pedido criado, PIX gerado, pagamento aprovado, carrinho abandonado e rastreio viram contato e negócio no Kommo, com UTMs, entrega, produto e link do carrinho. Tem esteira para descobrir os IDs do Kommo | Cartpanda, Kommo |
| `yampi-para-kommo-e-manychat.json` | Eventos de checkout da Yampi sincronizam o lead no Kommo e enviam dados para o Manychat | Yampi, Kommo, Manychat |
| `formulario-wordpress-para-kommo-sem-duplicar.json` | Cada envio do formulário do site vira lead no Kommo sem duplicar contato (busca pelos últimos 8 dígitos do telefone) e grava backup em planilha | WordPress/Elementor, Kommo, Google Sheets |
| `formulario-e-compra-para-kommo-brevo-manychat.json` | Formulário do site → Kommo → Brevo (e-mail) → Manychat (WhatsApp), e compras → Kommo | WordPress, Hotmart, Kommo, Brevo, Manychat, Google Sheets |
| `formulario-respondi-para-kommo-datacrazy-ghl.json` | Respostas de formulário são registradas, viram lead no Kommo e seguem para Datacrazy ou GoHighLevel conforme a rota | Respondi, Kommo, Datacrazy, GoHighLevel, Google Sheets |
| `rd-station-para-ploomes.json` | Conversões do RD Station viram contato e negócio no Ploomes com origem, campanha e responsável | RD Station, Ploomes, Google Sheets, Slack |
| `ploomes-para-rd-station-e-blip.json` | Mudança de etapa no Ploomes atualiza o RD Station e dispara templates de WhatsApp pelo Blip | Ploomes, RD Station, Blip, Google Sheets, Slack |
| `omie-para-brevo-esqueleto.json` | **Esqueleto** para sincronizar contatos do Omie com o Brevo (a lógica precisa ser montada) | Omie, Brevo |
| `google-agenda-para-crm-ghl.json` | Evento novo na agenda envia os participantes externos, um a um, para um webhook do CRM | Google Agenda, GoHighLevel/LeadConnector |

## Anúncios e conversões (`templates/anuncios-e-conversoes/`)
| Arquivo | O que faz | Ferramentas |
|---|---|---|
| `crm-para-meta-capi.json` | Evento do CRM (ex.: lead qualificado) vai para a Meta Conversions API com dados em hash, com e sem fbclid, e bloco de teste | Qualquer CRM com webhook, Meta |
| `activecampaign-para-meta-capi.json` | Evento do ActiveCampaign vai para a Meta Conversions API | ActiveCampaign, Meta |
| `mql-hubspot-para-google-ads-e-meta.json` | Lead que vira MQL no HubSpot vai como conversão offline para o Google Ads e para a Meta | HubSpot, Google Ads, Meta |

## WhatsApp e mensagens (`templates/whatsapp-e-mensagens/`)
| Arquivo | O que faz | Ferramentas |
|---|---|---|
| `manychat-para-inngage-push.json` | Lead do Manychat vira assinante de push na Inngage | Manychat, Inngage |
| `crm-para-manychat-aviso-de-aula-ao-vivo.json` | Contato que entra numa automação do CRM vira assinante no Manychat com tag que dispara o aviso de aula ao vivo (Brasil e Portugal) | CRM/e-mail marketing, Manychat |
| `grupos-whatsapp-sendflow-para-manychat.json` | Quem entra num grupo de WhatsApp vira assinante no Manychat, marcado com o grupo de origem | Sendflow, Manychat |
| `remover-lead-da-campanha-ao-entrar-no-grupo.json` | Quem entrou no grupo sai da fila de convites (evita mensagem repetida e bloqueio do número) | Ferramenta de grupos |
| `criar-template-whatsapp-na-meta.json` | Cria um template de mensagem na WhatsApp Business API e registra numa planilha | Meta (WhatsApp Business), Google Sheets |

## Operação e produtividade (`templates/operacao-e-produtividade/`)
| Arquivo | O que faz | Ferramentas |
|---|---|---|
| `reuniao-ia-para-tarefas-e-propostas-clickup.json` | Transcrição de reunião vira lista de tarefas ou proposta com IA, gravada no banco e publicada no ClickUp | OpenAI, Supabase, ClickUp |
| `onboarding-de-cliente-notion-para-clickup.json` | Etapas de onboarding no Notion viram tarefas e documentos no ClickUp | Notion, ClickUp |
| `dashboard-de-eventos-supabase.json` | Coleta diária de métricas de eventos de uma API de chat e grava no Supabase para um painel | API de chat, Supabase |
| `split-de-pagamentos-asaas.json` | Cobranças e assinaturas com divisão de pagamento entre carteiras, com registro em planilha | Asaas, Google Sheets |
| `avisos-de-status-das-ferramentas.json` | Recebe aviso de status (fora do ar, instável) e repassa para um canal interno | Status page (ex.: Instatus) |
| `pesquisa-web-para-google-sheets.json` | Respostas de uma pesquisa na web vão para uma planilha | Formulário web, Google Sheets |
| `CUIDADO-exclusao-em-massa-activecampaign.json` | **Apaga contatos para sempre** a partir de uma lista na planilha, em lotes, marcando o que foi feito | ActiveCampaign, Google Sheets |

## Como escolher
- **"Quero o lead no CRM sem duplicar"** → `formulario-wordpress-para-kommo-sem-duplicar` (a lógica de telefone serve para qualquer CRM).
- **"Quero que os anúncios aprendam com quem virou cliente"** → um dos três de `anuncios-e-conversoes`.
- **"Carrinho abandonado e PIX no CRM"** → `cartpanda-para-kommo` ou `yampi-para-kommo-e-manychat`.
- **"WhatsApp disparado por automação"** → `crm-para-manychat-aviso-de-aula-ao-vivo` ou `ploomes-para-rd-station-e-blip`.
