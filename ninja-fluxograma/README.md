# Ninja Fluxograma — skill para Claude Code, Claude.ai e Codex

> Criado por **Jaqueline Amaro** · [LinkedIn](https://www.linkedin.com/in/jaquelineamaro/)

Transforma **qualquer processo do seu negócio num fluxograma claro no Miro** (ou FigJam, Mermaid, draw.io):
vendas, **lifecycle e jornada do cliente**, atendimento, operação interna ou qualquer fluxo de ponta a ponta.
Ela lê o processo de onde ele estiver (documentos, planilhas, CRM, ferramenta de automação, sistema de chamados ou o
agente que você já usa) e desenha cada etapa, decisão, gatilho, canal, prazo e resultado.

Depois, se você quiser, transforma o fluxo aprovado em:
- um **agente de IA** (de vendas, de suporte, de onboarding), com as instruções de cada etapa prontas para colar;
- uma **régua de lifecycle**, com cada mensagem, gatilho, espera, canal e métrica;
- um **passo a passo (POP)** para o time seguir.

## Serve para
| Tipo de processo | Exemplos |
|---|---|
| Vendas e pré-vendas | funil comercial, qualificação, SDR, agendamento |
| Lifecycle / jornada do cliente | onboarding, ativação, engajamento, retenção, reativação, renovação, upsell |
| Atendimento e suporte | triagem de chamados, escalonamento, pós-atendimento |
| Operação interna | pedido até entrega, aprovação de compra, contratação, onboarding de colaborador |

## O que vem no pacote
| | |
|---|---|
| `SKILL.md` | O fluxo em 6 fases e 6 modos: mapear, agente, lifecycle, POP, briefing e auditoria |
| `references/fontes-de-dados.md` | Como ler documentos, CRM, ferramentas de automação, sistemas de chamados e agentes existentes (só leitura) |
| `references/tipos-de-processo.md` | Modelos de partida para vendas, lifecycle, atendimento e operação, e como montar a régua |
| `references/etapas-sdr.md` | O funil SDR padrão: Recepção, Triagem, Qualificação, Agenda, Qualificado, Desqualificado |
| `references/destinos.md` | Convenções de forma, cor e raias, e como gerar no Miro, FigJam, Mermaid e draw.io |
| `references/formato-das-etapas.md` | Texto de cada etapa do agente: Passo / Regras / Objetivo / Fallback |
| `references/prompt-do-agente.md` | Persona, comunicação, base de conhecimento, objeções, limites, escalonamento |
| `references/checklist-qa.md` | Checklist de qualidade, auditoria e conversas de teste |
| `references/briefing.md` | Questionário para quando nada está documentado |
| `examples/` | Dois exemplos completos com empresas fictícias: vendas e lifecycle |

### Diferenciais
- **Qualquer processo, um padrão só:** raias por participante, uma ação por forma, toda decisão com todas as saídas.
- **Do sistema ao quadro:** etapas do CRM, jornadas da automação e filas de atendimento viram desenho, com os gargalos anotados.
- **Ida e volta:** o mesmo quadro vira agente de IA, régua de lifecycle ou passo a passo.
- **Não inventa regra de negócio:** o que falta vira nota "Confirmar" no quadro.
- **Seguro com dado de cliente:** acesso só leitura, senha nunca salva, nenhum dado pessoal no entregável.

## Antes de começar: checklist
- [ ] **Claude** (claude.ai, Claude Code ou Cowork) — ou **Codex**.
- [ ] (Recomendado) **Conector do Miro** ligado no Claude, para o quadro ser criado direto. Sem ele, a skill entrega Mermaid e draw.io para importar.
- [ ] (Opcional) Conector do **Figma/FigJam**, do seu **CRM** ou da sua **ferramenta de automação**.
- [ ] O material do processo (manual, planilha, prints, exportação) ou 20 minutos para responder o briefing.
- [ ] Autorização do cliente para acessar os dados e sistemas dele.

## Instalação
- **Claude.ai / Cowork:** compacte a pasta `ninja-fluxograma/` em .zip e envie em Configurações → Capacidades → Skills.
- **Claude Code:** copie a pasta para `~/.claude/skills/ninja-fluxograma/` (ou `.claude/skills/` do projeto).
- **Codex:** copie a pasta para `~/.codex/skills/ninja-fluxograma/`.

Depois é só pedir: *"Desenha no Miro o lifecycle de onboarding dos nossos clientes"*, *"Mapeia o processo de
aprovação de compras"* ou *"Pega o funil do CRM e transforma num agente SDR"*.

## Licença e crédito
Criado por **Jaqueline Amaro**. Uso livre e sem fins comerciais, **desde que você dê o crédito** (CC BY-NC 4.0).
Para vender ou usar com clientes pagos, fale comigo pelo [LinkedIn](https://www.linkedin.com/in/jaquelineamaro/). Detalhes em [LICENSE.md](LICENSE.md).
