---
name: ninja-fluxograma
description: "Turns any business process into a clear visual flowchart board (Miro, FigJam, Mermaid or draw.io): sales and pre-sales, customer lifecycle and CRM journeys (onboarding, activation, retention, win-back, renewal), customer support and service, internal operations (approvals, order to delivery, hiring, onboarding employees) or any end-to-end business flow. Reads the process from wherever it lives: documents and playbooks, spreadsheets, CRM pipelines and marketing automation journeys (connector or export), ticketing or bot/AI agent exports and APIs, or the person's own description. Maps stages, steps, decisions, triggers, channels, timing, data captured, hand-offs and outcomes with consistent shapes, flags gaps and bottlenecks, and can turn the approved flow into deliverables: an AI agent (SDR, support, onboarding) with stage-by-stage instructions and prompt, a lifecycle message plan, or a step-by-step procedure (SOP). Use when someone asks to map, draw, diagram, document or audit a process or journey (e.g. desenha meu processo no Miro, fluxograma do lifecycle, mapeia a jornada do cliente, transforma o funil do CRM em fluxograma, desenha o fluxo de atendimento, fluxograma do processo de aprovação, cria um agente a partir desse fluxo, audita meu bot)."
---

# Ninja Fluxograma

Entrega: **qualquer processo de negócio desenhado num quadro** (Miro, FigJam, Mermaid ou draw.io), com cada etapa,
ação, decisão, gatilho, canal, prazo, dado capturado, passagem de bastão e resultado. Opcional: transformar o fluxo
aprovado em um **agente de IA**, num **plano de lifecycle** ou num **passo a passo (POP)**.
Siga as fases na ordem. Leia o arquivo de `references/` indicado em cada fase ANTES de executá-la.

## 6 regras (valem para tudo)
1. **Nunca invente regra de negócio.** Critério, prazo, preço, responsável, integração: se não está na fonte nem foi
   dito pela pessoa, pergunte. Ponto em aberto vira nota "Confirmar" no quadro e na lista final.
2. **Comece pelo modelo do tipo de processo.** Compare com o modelo de `references/tipos-de-processo.md`.
   Diferença vira observação, não erro.
3. **1 ação = 1 forma.** Cada mensagem, tarefa, campo, decisão ou passagem é uma forma própria no quadro e uma linha
   própria no texto. Nada escondido.
4. **Toda decisão tem todas as saídas.** Cada losango mostra o "sim", o "não" e o "e se não responder / der erro".
   Toda espera tem prazo; todo laço tem limite.
5. **Toda pessoa sabe o que está acontecendo.** Quando o fluxo muda de etapa, passa para outra pessoa ou termina,
   quem está do outro lado (cliente, lead, colaborador) recebe aviso.
6. **Dado do cliente é confidencial.** Acesso só leitura, senha ou token nunca escrito em arquivo nem no quadro,
   nenhum dado pessoal real no entregável. Exemplos são fictícios.

## Fase 0 — Entender o pedido
Descubra **o tipo de processo** e **o que entregar**:

| Tipo de processo | Exemplos |
|---|---|
| **Vendas e pré-vendas** | funil comercial, qualificação, SDR, agendamento |
| **Lifecycle / jornada do cliente** | onboarding, ativação, engajamento, retenção, reativação, renovação, upsell |
| **Atendimento e suporte** | primeiro atendimento, triagem de chamados, escalonamento, pós-atendimento |
| **Operação interna** | pedido até entrega, aprovação de compras, contratação, onboarding de colaborador |
| **Outro processo de negócio** | qualquer fluxo de ponta a ponta que a pessoa descrever |

| Sinal | Modo | Fases |
|---|---|---|
| "desenha", "mapeia", "fluxograma", "joga no Miro" | **Mapear** | 1, 2, 3, 6 |
| "cria um agente", "transforma em agente" | **Mapear + Agente** | 1 a 6 |
| "monta a régua", "plano de lifecycle", "quais mensagens" | **Mapear + Lifecycle** | 1, 2, 3, 5, 6 |
| "passo a passo", "POP", "manual do processo" | **Mapear + POP** | 1, 2, 3, 5, 6 |
| "não tenho nada documentado" | **Briefing** | Questionário de `references/briefing.md` |
| Processo, agente ou régua já existe, "revisa", "onde trava" | **Auditoria** | 1, 2, 3 e `references/checklist-qa.md` |

## Fase 1 — Coletar o processo
Leia `references/fontes-de-dados.md`. Descubra de onde vem o processo e leia tudo: documentos, planilhas,
CRM ou ferramenta de automação (conector ou exportação), sistema de chamados, export/API do agente ou bot,
ou a descrição da própria pessoa. Pergunte o destino do quadro (Miro, FigJam, Mermaid, draw.io) se ainda não foi dito.

## Fase 2 — Sintetizar
Leia `references/tipos-de-processo.md` (e `references/etapas-sdr.md` se for vendas). Mostre um resumo curto:
- **Começo e fim:** o que dispara o processo e qual é o resultado esperado.
- **Quem participa:** cliente, times, sistemas (vira as raias do quadro).
- **Etapas** na ordem, com tipo: linear (passos em sequência) ou reativa (reage ao que acontecer).
- **Decisões e critérios**, **gatilhos e prazos**, **canais** (e-mail, WhatsApp, push, ligação, tarefa interna).
- **Resultados possíveis** (sucesso, perda, cancelamento, escalonamento), com o motivo de cada um.
- **Dados capturados** ou usados em cada etapa.
- **Lacunas e gargalos:** etapa sem saída, decisão sem critério, espera sem prazo, laço sem limite, passagem sem
  responsável, resultado sem medição, etapa onde muita gente para (quando houver números).

**[PARE AQUI]** se houver lacuna que muda o desenho. No máximo 5 perguntas, de uma vez. O resto vira nota "Confirmar".

## Fase 3 — Desenhar o quadro
Leia `references/destinos.md` e use as convenções de forma e cor. Ordem de preferência:
1. **Miro** conectado no Claude → crie o quadro direto (raias por participante, frames por etapa, formas, conectores, notas).
2. **FigJam** conectado → gere o diagrama lá.
3. Sem conector → **Mermaid** (renderize se possível) e/ou **draw.io XML** para importar no Miro, Lucid ou draw.io.
Sempre entregue também o Mermaid, que serve de fonte da verdade para versões futuras.

## Fase 4 — Agente de IA (modo Agente)
Leia `references/formato-das-etapas.md`. Cada etapa do quadro vira um bloco de texto pronto para colar:
cabeçalho → Regras gerais → Passos (`Passo N: "Título"` com Regras / Objetivo / Fallback) → Templates.
Cada forma do quadro vira uma linha do Objetivo, na mesma ordem dos conectores. Monte o prompt pelo
`references/prompt-do-agente.md`. Serve para agente SDR, de suporte, de onboarding ou de reativação.

## Fase 5 — Entregáveis do fluxo
- **Campos:** tabela (`snake_case`, tipo, etapa, valores aceitos, origem no CRM ou sistema). Sempre com
  `etapa_atual` e o motivo de cada resultado.
- **Modo Lifecycle:** a régua pronta, uma linha por mensagem ou ação: etapa, gatilho, espera, canal, público
  (segmento), objetivo, mensagem (rascunho), métrica de sucesso, regra de saída. Detalhes em `references/tipos-de-processo.md`.
- **Modo POP:** o passo a passo numerado por etapa, com responsável, prazo, ferramenta e o que fazer em cada exceção.
- **Modo Agente:** de 6 a 10 conversas de teste.
Rode `references/checklist-qa.md` em todos os modos.

## Fase 6 — Entregar
```
# Ninja Fluxograma — [Empresa / Processo]
## Link do quadro (ou imagem + código Mermaid / draw.io)
## Resumo do processo (começo, fim, participantes, etapas, decisões, resultados)
## Gargalos e melhorias sugeridas
## Campos (com origem, quando houver)
## [Modo Agente] Etapas prontas para colar · Prompt · Mapa de ações → plataforma · Conversas de teste
## [Modo Lifecycle] Régua de mensagens e ações
## [Modo POP] Passo a passo
## Confirmar com o responsável
```
Termine oferecendo: *"Quer que eu ajuste o quadro, transforme em agente de IA, em régua de lifecycle ou em passo a passo?"*

## Referências
| Arquivo | Quando ler |
|---|---|
| `references/fontes-de-dados.md` | Fase 1 |
| `references/tipos-de-processo.md` | Fase 2 e modo Lifecycle |
| `references/etapas-sdr.md` | Fase 2, quando o processo for de vendas |
| `references/destinos.md` | Fase 3 |
| `references/formato-das-etapas.md` | Fase 4 |
| `references/prompt-do-agente.md` | Fase 4 |
| `references/checklist-qa.md` | Fase 5 e modo Auditoria |
| `references/briefing.md` | Modo Briefing ou quando a fonte não basta |
| `examples/exemplo-completo.md` | Exemplo de vendas (empresa fictícia) |
| `examples/exemplo-lifecycle.md` | Exemplo de lifecycle (empresa fictícia) |
