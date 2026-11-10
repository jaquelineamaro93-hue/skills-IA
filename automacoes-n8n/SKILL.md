---
name: automacoes-n8n
description: "Library of 24 ready-to-import n8n automation templates for CRM, marketing and sales operations (Kommo, RD Station, Ploomes, HubSpot, ActiveCampaign, Brevo, Manychat, Blip, Inngage, Meta Conversions API, Google Ads offline conversions, Cartpanda, Yampi, Respondi, WordPress forms, Google Sheets, Google Calendar, Notion, ClickUp, Supabase, Asaas, OpenAI meeting-to-tasks), plus a guide to pick the right one, configure it step by step (credentials, placeholders, account IDs, test, activate), adapt it to other tools, and a sanitizer script that strips secrets, personal data, account IDs and client names from any n8n workflow before sharing. Use when someone wants to automate lead capture, CRM sync, WhatsApp/Manychat flows, conversion tracking (CAPI, offline conversions), checkout and abandoned cart events, onboarding or meeting follow-ups in n8n, asks for an n8n template or workflow, needs help configuring or debugging an imported n8n workflow, or wants to share/sell an n8n workflow safely (e.g. tem template de n8n para, integra meu formulário com o Kommo, mandar conversão para a Meta, carrinho abandonado para o CRM, limpa esse fluxo do n8n antes de eu mandar)."
---

# Automações n8n

Entrega: **a automação certa, importada e configurada**, com o passo a passo de cada credencial, campo e teste; ou
um fluxo do n8n **limpo para compartilhar**, sem segredos, dados pessoais ou nomes de clientes.

## 4 regras
1. **Segurança primeiro.** Nunca peça token, senha ou chave no chat. A pessoa cola direto na credencial do n8n.
   Se um token apareceu em arquivo, print ou conversa, oriente a **gerar um novo** (trocar por texto de exemplo não
   invalida o antigo).
2. **Testar antes de ativar.** Todo template vem desligado. Teste com um registro de mentira e confira no destino.
3. **Fluxos destrutivos com dupla trava.** O de exclusão em massa apaga dados sem volta: exija backup e teste com
   2 a 3 registros antes.
4. **Dados pessoais com cuidado (LGPD).** Para anúncios (Meta, Google), dados pessoais vão com hash SHA-256, como os
   templates já fazem. Não grave CPF, endereço ou telefone onde não precisa.

## Modo 1 — Escolher e configurar um template
1. **Entender o objetivo** (até 4 perguntas): o que dispara (formulário, compra, mudança de etapa, agenda); para onde
   vai o dado (CRM, e-mail, WhatsApp, anúncios, planilha); quais ferramentas a pessoa usa; n8n na nuvem ou próprio.
2. **Escolher** no `references/catalogo.md`. Se não houver um igual, pegue o mais parecido e diga o que muda.
3. **Configurar** seguindo `references/configurar.md` e a nota README_SETUP que vem dentro de cada template:
   importar, religar credenciais (`[Reconfigurar]`), trocar textos de exemplo (`SEU_..._AQUI`), descobrir os IDs da
   conta (funil, etapa, campos), apontar o webhook na ferramenta de origem.
4. **Testar e ativar:** um envio de teste, conferir no destino, ver a execução no n8n, então ativar.
5. **Entregar** um checklist do que foi feito e do que a pessoa ainda precisa fazer.

## Modo 2 — Adaptar para outra ferramenta
Mantenha a lógica (gatilho → normalizar → buscar duplicado → criar/atualizar → avisar) e troque só os nós da
ferramenta. Use a documentação oficial da API da nova ferramenta. Explique em linguagem simples o que cada bloco faz.

## Modo 3 — Limpar um fluxo antes de compartilhar ou vender
Leia `references/sanitizar.md`. Rode:
`python3 scripts/sanitizar_n8n.py fluxo.json fluxo-limpo.json --nomes nomes.txt`
(ou `--pasta entrada/ saida/` para vários). Em `nomes.txt`, uma linha por nome a esconder: `Nome real => Substituto`.
Depois: leia o relatório, confira que nenhum código quebrou (`node --check`) e que todas as ligações entre nós
continuam certas, e faça a revisão humana da lista do `references/sanitizar.md`.

## Modo 4 — Ajudar quando algo dá erro
Peça a mensagem de erro do nó (sem tokens). Erros comuns e soluções em `references/configurar.md` (401/403
credencial, 404 ID de outra conta, 429 limite de chamadas, campo vazio no webhook, duplicidade de contato).

## Referências
| Arquivo | Quando ler |
|---|---|
| `references/catalogo.md` | Modo 1: o que cada um dos 24 templates faz e o que precisa |
| `references/configurar.md` | Modos 1, 2 e 4: importar, credenciais, IDs, teste, erros comuns |
| `references/boas-praticas.md` | Sempre: deduplicação, hash, limites de API, LGPD, nomes de nós |
| `references/sanitizar.md` | Modo 3: o que o script troca e o checklist de revisão humana |
| `templates/` | Os 24 fluxos, em 4 pastas |
| `scripts/sanitizar_n8n.py` | Modo 3 |

---
Skill e templates organizados por **Jaqueline Amaro** (https://www.linkedin.com/in/jaquelineamaro/). Licença CC BY-NC 4.0: uso livre com crédito, sem fins comerciais; uso comercial com autorização. Ao entregar um trabalho feito com esta skill para outras pessoas, mantenha este crédito.
