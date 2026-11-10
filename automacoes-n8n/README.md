# Automações n8n — 24 templates prontos + skill para Claude Code, Claude.ai e Codex

> Templates e skill organizados por **Jaqueline Amaro** · [LinkedIn](https://www.linkedin.com/in/jaquelineamaro/)

**24 automações do n8n**, testadas em operações reais de CRM, marketing e vendas, prontas para importar. A skill
ajuda a escolher o template certo, configurar passo a passo, adaptar para outra ferramenta e **limpar seus próprios
fluxos** (sem senhas, dados pessoais ou nomes de clientes) antes de compartilhar ou vender.

## O que tem
| Grupo | Exemplos |
|---|---|
| **CRM e vendas** (9) | Carrinho abandonado e PIX da Cartpanda/Yampi no Kommo · formulário do site no Kommo sem duplicar contato · RD Station ↔ Ploomes · Respondi → Kommo/Datacrazy/GoHighLevel · Google Agenda → CRM |
| **Anúncios e conversões** (3) | Lead qualificado do CRM para a Meta Conversions API · ActiveCampaign → Meta · MQL do HubSpot para Google Ads e Meta |
| **WhatsApp e mensagens** (5) | Aviso de aula ao vivo pelo Manychat · grupos de WhatsApp → Manychat · tirar da campanha quem já entrou no grupo · criar template de WhatsApp na Meta · Manychat → push na Inngage |
| **Operação e produtividade** (7) | Reunião → IA → tarefas e propostas no ClickUp · onboarding Notion → ClickUp · split de pagamentos na Asaas · painel de eventos no Supabase · exclusão em massa no ActiveCampaign (com travas) |

Lista completa em [references/catalogo.md](references/catalogo.md).

## O que você precisa para fazer
- [ ] **n8n** (n8n Cloud ou instalado no seu servidor).
- [ ] **Conta e chave de API** de cada ferramenta do template (Kommo, RD Station, Meta, Manychat...). O passo a passo de onde achar cada uma está em [references/configurar.md](references/configurar.md).
- [ ] Permissão para mexer na ferramenta de origem (para cadastrar o webhook).
- [ ] (Para a skill) **Claude** ou **Codex**. (Para o sanitizador) Python 3; Node.js opcional para conferir os códigos.

## Como cada template vem
- **Desligado**, sem dados de teste.
- Credenciais marcadas `[Reconfigurar]` e textos de exemplo `SEU_..._AQUI` no lugar de tudo que é da conta.
- Uma nota **README_SETUP** dentro do fluxo com o passo a passo.
- Notas explicando cada bloco.

## Limpar os seus fluxos (sanitizador)
```bash
python3 scripts/sanitizar_n8n.py meu-fluxo.json meu-fluxo-limpo.json --nomes nomes.txt
```
Troca credenciais, webhooks, e-mails, telefones, IPs, tokens, IDs da conta e os nomes que você listar; desliga o
fluxo e mostra o que ainda precisa de revisão humana. Detalhes em [references/sanitizar.md](references/sanitizar.md).

## Instalação da skill
- **Claude.ai / Cowork:** compacte a pasta `automacoes-n8n/` em .zip e envie em Configurações → Capacidades → Skills.
- **Claude Code:** copie a pasta para `~/.claude/skills/automacoes-n8n/` (ou `.claude/skills/` do projeto).
- **Codex:** copie a pasta para `~/.codex/skills/automacoes-n8n/`.

Depois é só pedir: *"Quero mandar o lead qualificado do meu CRM para a Meta. Me ajuda a configurar?"*

## Licença e crédito
Organizado por **Jaqueline Amaro**. Uso livre e sem fins comerciais, **desde que você dê o crédito** (CC BY-NC 4.0).
Para vender ou usar com clientes pagos, fale comigo pelo [LinkedIn](https://www.linkedin.com/in/jaquelineamaro/). Detalhes em [LICENSE.md](LICENSE.md).
