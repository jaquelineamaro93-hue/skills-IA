# Configurar um template no n8n

## 1. Importar
n8n → **Workflows** → **Import from File** (ou cole o JSON na tela). O fluxo entra desligado.
Leia a nota **README_SETUP** dentro do fluxo: ela tem o passo a passo específico daquele template.

## 2. Religar as credenciais
Todo nó com credencial aparece com `[Reconfigurar] <ferramenta>`. Abra o nó → **Credential** → **Create new** e cole
a chave **direto no n8n**. Onde achar a chave:
| Ferramenta | Onde |
|---|---|
| Kommo | Configurações → Integrações → criar integração privada → token de longa duração |
| RD Station | App no RD Station Marketing (OAuth2: Client ID e Secret) |
| Ploomes | Administração → Integração → User-Key |
| HubSpot | Configurações → Integrações → Apps privados → token |
| ActiveCampaign | Configurações → Desenvolvedor → URL e chave da API |
| Brevo | SMTP & API → API Keys |
| Manychat | Configurações → API → chave |
| Meta (CAPI / WhatsApp) | Gerenciador de Negócios → Usuários do sistema → gerar token com as permissões do pixel/WABA |
| Google (Sheets, Agenda, Ads) | OAuth2 pelo próprio n8n; Ads precisa também do developer token |
| Notion | Integrações → Internal Integration Token (e compartilhar a página com a integração) |
| ClickUp | Configurações → Apps → API Token |
| Asaas | Integrações → Chave de API (sandbox e produção são diferentes) |

Alguns templates guardam o token num nó **Edit Fields** (painel de controle). Prefira mover para uma credencial
(Header Auth) quando puder: fica protegido e não aparece em exportações.

## 3. Trocar os textos de exemplo
Procure por `SEU_`, `SUA_`, `_AQUI` e `0 /* SEU_ID_AQUI */` (IDs dentro de códigos). Cada um diz o que colocar:
URL da conta, ID do pixel, ID da planilha, IDs de funil, etapa e campos.

**Descobrir IDs da conta:** vários templates trazem uma **esteira auxiliar** (gatilho manual) que lista funis,
etapas e campos personalizados da sua conta. Rode uma vez e copie os IDs. Sem esteira: use a API da ferramenta
(ex.: `GET /api/v4/leads/pipelines` no Kommo) ou a URL da tela de configuração, que costuma mostrar o ID.

## 4. Apontar o webhook
No nó Webhook, copie a **Production URL** e cadastre na ferramenta de origem (formulário, checkout, CRM).
A **Test URL** só funciona com o fluxo aberto em "Listen for test event".

## 5. Testar
1. "Execute workflow" + um envio de teste na origem (dado de mentira).
2. Confira cada nó na execução (verde = ok) e o resultado no destino.
3. Teste também o caminho de exceção: contato que já existe, campo vazio, telefone com formatos diferentes.
4. Meta CAPI: use o **Test Event Code** e veja o evento chegar em Eventos de teste antes de tirar o código.

## 6. Ativar e acompanhar
Ative o fluxo. Configure um **workflow de erro** (Settings → Error workflow) que avise no Slack ou e-mail quando algo
falhar. Olhe as execuções na primeira semana.

## Erros comuns
| Erro | Causa provável | O que fazer |
|---|---|---|
| 401 / 403 | Credencial errada, vencida ou sem permissão | Gerar nova chave com as permissões certas |
| 404 | ID de funil, campo ou conta de outra conta | Rodar a esteira de IDs e trocar |
| 429 | Limite de chamadas da API | Aumentar o Wait entre lotes, diminuir o lote |
| Campo vazio no destino | Nome do campo no webhook mudou | Ver o payload real na execução e ajustar a expressão |
| Contato duplicado | Busca por e-mail com maiúsculas/espaços, ou telefone em formatos diferentes | Normalizar (minúsculas, só dígitos, últimos 8 dígitos) antes de buscar |
| Nó "não encontrado" em expressão | Nó renomeado sem atualizar `$('Nome do nó')` | Corrigir o nome na expressão |
| Meta: evento sem correspondência | Dados sem hash ou mal normalizados | Minúsculas, sem espaços, telefone com DDI, depois SHA-256 |
