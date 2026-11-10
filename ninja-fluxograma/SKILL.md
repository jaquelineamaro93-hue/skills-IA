---
name: ninja-fluxograma
description: "Turns any company's sales process into a visual flowchart board (Miro, FigJam, Mermaid or draw.io) and, when asked, into a ready-to-configure AI SDR agent. Reads the process from wherever it lives: sales documents (playbook, deck, scripts, call transcripts), CRM pipeline exports or connectors (stages, fields, loss reasons), or an existing chatbot/AI agent exported as JSON or read from its API. Maps stages, questions, decisions, data captured, hand-offs and outcomes, draws them with consistent shapes, flags gaps and bottlenecks, and can do the reverse: turn the approved flowchart into stage-by-stage agent instructions, agent prompt, fields and test conversations. Use when someone asks to map, draw, diagram or document a sales/qualification/pre-sales process, CRM pipeline, WhatsApp bot or AI agent flow (e.g. desenha o processo de vendas no Miro, transforma o funil do CRM em fluxograma, mapeia o fluxo do meu agente, cria um agente SDR a partir desse fluxo, audita meu bot)."
---

# Ninja Fluxograma

Entrega: **o processo comercial do cliente desenhado num quadro** (Miro, FigJam, Mermaid ou draw.io), com cada etapa,
pergunta, decisão, dado capturado, transbordo e resultado. Opcional: o **agente SDR de IA** gerado a partir do fluxo.
Siga as fases na ordem. Leia o arquivo de `references/` indicado em cada fase ANTES de executá-la.

## 6 regras (valem para tudo)
1. **Nunca invente regra de negócio.** Critério de corte, preço, prazo, integração: se não está na fonte nem foi
   dito pela pessoa, pergunte. Ponto em aberto vira nota "Confirmar" no quadro e na lista final.
2. **Padrão antes de customização.** Compare sempre com o funil padrão (Recepção → Triagem → Qualificação → Agenda
   opcional → Qualificado / Desqualificado). Diferença vira observação, não erro.
3. **1 ação = 1 forma.** Cada mensagem, campo, decisão ou transição é uma forma própria no quadro e uma linha
   própria no texto. Nada escondido.
4. **Toda transição avisa o lead.** Mudar de etapa, transferir para humano ou encerrar exige mensagem antes.
5. **Desqualificado tem porta aberta.** Se o lead corrigir a informação, o fluxo volta para a etapa certa.
6. **Dado do cliente é confidencial.** Acesso só leitura, token nunca escrito em arquivo nem no quadro, nenhum
   dado pessoal de lead real no entregável. Exemplos são fictícios.

## Fase 0 — Entender o pedido
| Sinal | Modo | Fases |
|---|---|---|
| "desenha", "mapeia", "fluxograma", "joga no Miro" | **Mapear** | 1, 2, 3, 5 |
| "cria um agente", "transforma em agente SDR" | **Mapear + Agente** | 1 a 6 |
| "não tenho nada documentado" | **Briefing** | Questionário de `references/briefing.md` |
| Agente ou bot já existe, "revisa", "por que ele erra" | **Auditoria** | 1, 2, 3 e `references/checklist-qa.md` |

## Fase 1 — Coletar o processo
Leia `references/fontes-de-dados.md`. Descubra de onde vem o processo e leia tudo:
documentos, export ou conector do CRM, export/API do agente ou bot, ou a descrição da própria pessoa.
Pergunte qual é o destino do quadro (Miro, FigJam, Mermaid, draw.io) se ainda não foi dito.

## Fase 2 — Sintetizar
Leia `references/etapas.md`. Mostre um resumo curto:
- **Antes do SDR** (como o lead chega) e **depois** (para onde vai o qualificado).
- **Etapas** encontradas, na ordem, com tipo: linear ou reativa.
- **Critérios de corte**, **motivos de perda** e **sub-tipos de resultado**.
- **Transbordos**: lead muito quente, pedido de humano, suporte.
- **Dados capturados** em cada etapa.
- **Lacunas e gargalos**: etapa sem saída, decisão sem critério, laço sem limite, motivo de perda sem pergunta
  que o origine, campo do CRM nunca preenchido.

**[PARE AQUI]** se houver lacuna que muda o desenho. No máximo 5 perguntas, de uma vez. O resto vira nota "Confirmar".

## Fase 3 — Desenhar o quadro
Leia `references/destinos.md` e use as convenções de forma e cor. Ordem de preferência:
1. **Miro** conectado no Claude → crie o quadro direto (frames por etapa, formas, conectores, notas).
2. **FigJam** conectado → gere o diagrama lá.
3. Sem conector → **Mermaid** (renderize se possível) e/ou **draw.io XML** para importar no Miro, Lucid ou draw.io.
Sempre entregue também o Mermaid, que serve de fonte da verdade para versões futuras.

## Fase 4 — Escrever as etapas do agente (modo Agente)
Leia `references/formato-das-etapas.md`. Cada etapa do quadro vira um bloco de texto pronto para colar:
cabeçalho → Regras gerais → Passos (`Passo N: "Título"` com Regras / Objetivo / Fallback) → Templates.
Cada forma do quadro vira uma linha do Objetivo, na mesma ordem dos conectores.

## Fase 5 — Campos, prompt e testes
- Tabela de campos (`snake_case`, tipo, etapa, valores aceitos), sempre com `etapa_atual`,
  `motivo_desqualificacao` e `subtipo_resultado`. Se veio do CRM, mostre o campo de origem.
- Modo Agente: prompt pelo `references/prompt-do-agente.md` (persona, missão, comunicação, base de
  conhecimento, objeções, limites, escalonamento).
- Rode `references/checklist-qa.md`. Modo Agente: escreva de 6 a 10 conversas de teste.

## Fase 6 — Entregar
```
# Ninja Fluxograma — [Empresa / Processo]
## Link do quadro (ou imagem + código Mermaid / draw.io)
## Resumo do processo (antes, depois, etapas, cortes, resultados)
## Gargalos e melhorias sugeridas
## Campos (com origem no CRM, quando houver)
## [Modo Agente] Etapas prontas para colar · Prompt do agente · Mapa de ações → plataforma · Conversas de teste
## Confirmar com o responsável
```
Termine oferecendo: *"Quer que eu ajuste o quadro, gere o agente SDR a partir dele ou adapte para a sua plataforma?"*

## Referências
| Arquivo | Quando ler |
|---|---|
| `references/fontes-de-dados.md` | Fase 1 |
| `references/etapas.md` | Fase 2 |
| `references/destinos.md` | Fase 3 |
| `references/formato-das-etapas.md` | Fase 4 |
| `references/prompt-do-agente.md` | Fase 5, modo Agente |
| `references/checklist-qa.md` | Fase 5 e modo Auditoria |
| `references/briefing.md` | Modo Briefing ou quando a fonte não basta |
| `examples/exemplo-completo.md` | Para calibrar o nível de detalhe (empresa fictícia) |
