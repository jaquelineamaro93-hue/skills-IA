# Complex Data Analysis — skill para Claude Code, Claude.ai e Codex

Análise de dados que vai além do "o que os dados mostram" e descobre **o que eles estão tentando dizer**.
Você manda a planilha, o export do CRM ou as conversas do WhatsApp; a skill enquadra a pergunta, mapeia a
qualidade dos dados, cruza fontes e entrega oportunidades priorizadas com nível de confiança.

## O que vem no pacote
| | |
|---|---|
| `SKILL.md` | O fluxo completo em 6 fases e 4 modos (rápido, focado, completo, drill-down) |
| `references/lenses.md` | As 6 lentes não-convencionais com técnicas e mini-cases |
| `references/conversation-tips.md` | Métricas e técnicas para conversas (WhatsApp, chatbot, atendimento) |
| `references/examples.md` | Exemplos completos de entrada e saída para calibrar profundidade e tom |

### Diferenciais
- **6 lentes de análise:** sinais fracos, inversão, temporal de 2ª ordem, quali-quanti, proporções vs. absolutos e mapeamento de lacunas.
- **Checagem anti-pareidolia:** nenhum padrão vira insight sem passar por 4 testes; o que não passa é marcado como hipótese.
- **Oportunidades priorizadas:** impacto, esforço, confiança, horizonte e a decisão sugerida para cada uma.
- **Cálculos sempre com código** (Python/pandas) e gráficos que contam a história em 5 segundos.
- **LGPD por padrão:** nomes, CPFs, telefones e e-mails são anonimizados automaticamente.

## Antes de começar: checklist
- [ ] **Claude** (claude.ai com execução de código ativada, Claude Code ou Cowork) — ou **Codex**.
- [ ] Os dados em CSV, XLSX, JSON ou texto (exports de CRM, planilhas de vendas/marketing, conversas).
- [ ] Uma pergunta de negócio, mesmo que vaga ("por que as vendas caíram?", "o que estamos perdendo?").

## Instalação
- **Claude.ai / Cowork:** compacte a pasta `complex-data-analysis/` em .zip e envie em Configurações → Capacidades → Skills.
- **Claude Code:** copie a pasta para `~/.claude/skills/complex-data-analysis/` (ou `.claude/skills/` do projeto).
- **Codex:** copie a pasta para `~/.codex/skills/complex-data-analysis/`.

Depois é só pedir: *"Analisa esse export de leads e me diz o que estamos perdendo."*

## Licença
Uso pessoal e comercial no seu trabalho; revenda e redistribuição proibidas. Veja [LICENSE.md](LICENSE.md).
