# Templates de WhatsApp Aprovados — skill para Claude Code, Claude.ai e Codex

> Criado por **Jaqueline Amaro** · [LinkedIn](https://www.linkedin.com/in/jaquelineamaro/)

Templates **UTILITY** da WhatsApp Business Platform (Meta) feitos para serem **aprovados na primeira submissão**:
confirmação de pedido, envio, agendamento, pagamento, boleto, resultado de exame, acesso a plataforma e mais.

## O que vem no pacote
| | |
|---|---|
| `SKILL.md` | O processo: contexto → teste Utility vs. Marketing → template → payload JSON → checklist de aprovação |
| `references/approved-templates.md` | Templates validados por vertical: e-commerce, saúde, logística, financeiro, imobiliário, educação, delivery |
| `references/rejection-patterns.md` | Motivos de rejeição, palavras proibidas e exemplos reprovados com a correção |
| `references/copywriting-rules.md` | Variáveis, limites de caracteres, botões, tom de voz e estrutura |

### Diferenciais
- **Filtro Utility vs. Marketing:** avisa antes de escrever se o pedido vai ser reclassificado (e cobrado) como Marketing.
- **Sample values realistas** em toda variável, o detalhe que mais derruba aprovação.
- **Payload JSON pronto para a API** da Meta (Cloud API / BSP), com nome no padrão `util_[tipo]_[acao]_v1`.
- **Checklist de aprovação** rodado em todo template antes da entrega, e diagnóstico de templates rejeitados.

## Antes de começar: checklist
- [ ] **Claude** (claude.ai, Claude Code ou Cowork) — ou **Codex**.
- [ ] Conta na **WhatsApp Business Platform** (direto na Meta ou via BSP) para submeter os templates.
- [ ] O evento que dispara a mensagem, os dados que mudam por cliente e o nome do negócio.

## Instalação
- **Claude.ai / Cowork:** compacte a pasta `templates-whatsapp-aprovados/` em .zip e envie em Configurações → Capacidades → Skills.
- **Claude Code:** copie a pasta para `~/.claude/skills/templates-whatsapp-aprovados/` (ou `.claude/skills/` do projeto).
- **Codex:** copie a pasta para `~/.codex/skills/templates-whatsapp-aprovados/`.

Depois é só pedir: *"Cria um template de confirmação de consulta com botões confirmar e remarcar."*

## Licença e crédito
Criado por **Jaqueline Amaro**. Uso livre e sem fins comerciais, **desde que você dê o crédito** (CC BY-NC 4.0).
Para vender ou usar com clientes pagos, fale comigo pelo [LinkedIn](https://www.linkedin.com/in/jaquelineamaro/). Detalhes em [LICENSE.md](LICENSE.md).
