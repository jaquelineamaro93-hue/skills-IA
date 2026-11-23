# skills-IA

Skills para Claude Code e Codex, construídas e testadas em projetos reais por **Jaqueline Amaro**.

| Skill | O que faz |
|---|---|
| [`video-com-avatar-ia`](video-com-avatar-ia/) | Reels verticais com o seu avatar de IA falando com a sua própria voz clonada: identidade fiel, 5 ângulos, voz natural sincronizada à boca com autocorreção, cards, CTA e música. |
| [`automacoes-n8n`](automacoes-n8n/) | 24 automações prontas do n8n para CRM, marketing e vendas (Kommo, RD, Ploomes, HubSpot, Meta CAPI, Manychat...), com guia de configuração e um sanitizador que limpa seus fluxos antes de compartilhar. |
| [`analise-de-cohort`](analise-de-cohort/) | Mostra quanto tempo os clientes ficam e quanto valem: retenção, receita, LTV, CAC, LTV/CAC e payback por safra, cortes por canal e plano, insights e testes de conferência. |
| [`analise-de-dados-investigativa`](analise-de-dados-investigativa/) | Análise de dados investigativa: 6 lentes não-convencionais, checagem anti-pareidolia, oportunidades priorizadas, gráficos e relatório com nível de confiança. |
| [`ninja-fluxograma`](ninja-fluxograma/) | Desenha qualquer processo do negócio no Miro (ou FigJam, Mermaid, draw.io): vendas, lifecycle e jornada do cliente, atendimento e operação. Transforma o fluxo em agente de IA, régua de lifecycle ou passo a passo. |
| [`agente-buscador-de-vagas`](agente-buscador-de-vagas/) | Agente que busca vagas todo dia a partir do seu currículo, filtra por cargo, senioridade, modelo, pisos e não repete vagas, dá nota de compatibilidade e acompanha a conversão. Em três mensagens: [jaquelineamaro.com.br/agente-de-vagas](https://www.jaquelineamaro.com.br/agente-de-vagas/). |
| [`segundo-cerebro`](segundo-cerebro/) | Central de conhecimento pessoal ou de negócio: captura o que você aprende, organiza por tema e fonte, consulta antes de decidir e gera um índice para nada se perder. |
| [`health-score-clientes`](health-score-clientes/) | Health score para qualquer negócio recorrente (SaaS, serviço B2B, escola, assinatura, financiamento): entrevista, mapa de sistemas, vetores e pesos, cálculo sem dependências e calibração. Roda como planilha, tarefa agendada ou agente. Versão guiada, sem programar: [jaquelineamaro.com.br/health-score](https://www.jaquelineamaro.com.br/health-score/). |
| [`planilha-de-growth`](planilha-de-growth/) | Monta a planilha central de growth da marca: tarefas, calendário comercial, preço e margem com cupom, concorrentes, influenciadores, criativos, réguas de CRM, eventos e brindes, com fórmulas e alertas. |
| [`planejamento-estrategico`](planejamento-estrategico/) | Planeja a área do porquê até o OKR de cada pessoa: Casa da Estratégia, jornada, contexto, métricas de input e output, árvore de objetivos, OKRs com acompanhamento mensal e IA como parceira de pensamento. |
| [`meta-ads`](meta-ads/) | Especialista em Meta Ads: contexto da marca e ICP, ângulos e ganchos, diagnóstico de campanhas (cortar, manter ou escalar), custo real por lead qualificado cruzando com o CRM, anúncio x página, plano de 90 dias, montagem de campanha, checagem de política do Meta e das regras brasileiras e briefing de criativos. |
| [`templates-whatsapp-aprovados`](templates-whatsapp-aprovados/) | Templates UTILITY do WhatsApp Business (Meta) prontos para aprovação: texto, variáveis, botões, payload JSON e checklist. |

## Plugins (Claude Cowork e Claude Code)
| Plugin | O que faz |
|---|---|
| [`vendas`](plugin-vendas/) | 36 ajudantes para vender: preparar e resumir reuniões, follow-up, pesquisar empresas, cuidar dos negócios, revisar o funil, previsão de vendas e renovações. |
| [`desenvolvimento-de-software`](plugin-desenvolvimento-de-software/) | 10 ajudantes para quem cria sistemas e aplicativos: resumo da daily, revisão de código, arquitetura, correção de erros, sistema fora do ar, testes e documentação. |

Instalação dos plugins no Claude Code:
```bash
claude plugin marketplace add jaquelineamaro93-hue/skills-IA
```
```bash
claude plugin install vendas@skills-ia
```
Os plugins são obras derivadas de código aberto da Anthropic (Apache 2.0), traduzidas e adaptadas para o português; veja `LICENSE` e `NOTICE` de cada um.

Cada pasta de skill é completa: `SKILL.md` (o fluxo), `references/` e, quando precisa, `scripts/` e `examples/`.
O README de cada skill traz o **checklist do que você precisa ter antes de começar** (contas, programas e materiais) e a instalação.

## Sobre a autora
**Jaqueline Amaro** — especialista em CRM, CX e IA. Criadora da
[SOMA Mentoria](https://www.somamentoria.com) e da [Conexão CRM](https://www.conexaocrm.com)
(CRM Academy + Mulheres de CRM).

- LinkedIn: [linkedin.com/in/jaquelineamaro](https://www.linkedin.com/in/jaquelineamaro/)
- Instagram: [@jaquedocrm1112](https://www.instagram.com/jaquedocrm1112/)

## Licença e crédito
As skills deste repositório foram criadas por **Jaqueline Amaro** e são de **uso livre, sem fins comerciais, com crédito**
(CC BY-NC 4.0). Pode consultar, usar e adaptar; só não esqueça de citar quem fez:

> "[nome da skill]" por Jaqueline Amaro — https://github.com/jaquelineamaro93-hue/skills-IA

Quer vender, usar com clientes pagos ou dentro de um serviço pago? Fale comigo pelo LinkedIn para uma licença comercial.
Os plugins `vendas` e `desenvolvimento-de-software` são adaptações de código aberto e seguem a licença Apache 2.0 de cada um.

Dúvidas e novas skills: fale comigo pelo LinkedIn ou Instagram.
