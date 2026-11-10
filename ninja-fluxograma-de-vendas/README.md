# Ninja Fluxograma de Vendas — skill para Claude Code, Claude.ai e Codex

Transforma o processo comercial de qualquer empresa num **fluxograma visual no Miro** (ou FigJam, Mermaid, draw.io),
a partir de onde o processo estiver: playbook, scripts, CRM ou o agente de IA que o cliente já usa.
E faz o caminho de volta: do fluxograma aprovado, gera o **agente SDR de IA** pronto para configurar.

## O que vem no pacote
| | |
|---|---|
| `SKILL.md` | O fluxo em 6 fases e 4 modos: mapear, mapear + agente, briefing, auditoria |
| `references/fontes-de-dados.md` | Como ler documentos, pipeline do CRM (conector ou export) e agentes/bots existentes (export ou API, só leitura) |
| `references/etapas.md` | O funil SDR padrão: Recepção, Triagem, Qualificação, Agenda, Qualificado, Desqualificado |
| `references/destinos.md` | Convenções de forma e cor e como gerar no Miro, FigJam, Mermaid e draw.io |
| `references/formato-das-etapas.md` | Texto de cada etapa do agente: Passo / Regras / Objetivo / Fallback, etapas lineares e reativas |
| `references/prompt-do-agente.md` | Persona, comunicação, base de conhecimento, objeções, lead score, limites, escalonamento |
| `references/checklist-qa.md` | Checklist de qualidade, auditoria e 10 conversas de teste |
| `references/briefing.md` | Questionário para o cliente preencher quando não há nada documentado |
| `examples/exemplo-completo.md` | Exemplo completo com empresa fictícia |

### Diferenciais
- **Do CRM ao quadro:** etapas, campos e motivos de perda do pipeline viram frames, formas e resultados, com conversão e gargalos anotados.
- **Uma ação, uma forma:** nada escondido. O que está no quadro é exatamente o que o agente vai fazer.
- **Ida e volta:** o mesmo quadro gera as instruções do agente, etapa por etapa, prontas para colar em qualquer plataforma.
- **Não inventa regra de negócio:** o que falta vira nota "Confirmar" no quadro.
- **Seguro com dado de cliente:** acesso só leitura, token nunca salvo, nenhum dado pessoal no entregável.

## Antes de começar: checklist
- [ ] **Claude** (claude.ai, Claude Code ou Cowork) — ou **Codex**.
- [ ] (Recomendado) **Conector do Miro** ligado no Claude, para o quadro ser criado direto. Sem ele, a skill entrega Mermaid e draw.io para importar.
- [ ] (Opcional) Conector do **Figma/FigJam** ou do seu **CRM** (HubSpot, Salesforce, Pipedrive, RD Station, monday...).
- [ ] O material do processo: playbook, scripts, export do pipeline, export do agente atual, ou 20 minutos para responder o briefing.
- [ ] Autorização do cliente para acessar os dados e sistemas dele.

## Instalação
- **Claude.ai / Cowork:** compacte a pasta `ninja-fluxograma-de-vendas/` em .zip e envie em Configurações → Capacidades → Skills.
- **Claude Code:** copie a pasta para `~/.claude/skills/ninja-fluxograma-de-vendas/` (ou `.claude/skills/` do projeto).
- **Codex:** copie a pasta para `~/.codex/skills/ninja-fluxograma-de-vendas/`.

Depois é só pedir: *"Pega o funil do meu CRM e o playbook anexo e desenha o processo no Miro."*
ou *"Transforma esse fluxograma num agente SDR para WhatsApp."*

## Licença
Uso pessoal e comercial no seu trabalho e com seus clientes; revenda e redistribuição proibidas. Veja [LICENSE.md](LICENSE.md).
