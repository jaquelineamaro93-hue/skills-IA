---
name: planejamento-estrategico
description: "Guides a team leader through a complete strategic plan for their area (CRM, CX, growth, marketing, product, sales, operations), step by step, and turns it into a working spreadsheet: Strategy House (mission, vision, goals, enablers, foundation) connected to the company mission; end-to-end customer journey with channels, pains, opportunities and moments of truth; project context canvas (data, systems, stakeholders, out of scope, deliverables); lifecycle phases with INPUT vs OUTPUT metrics; objective tree (central objective → input and output pillars → groups with objectives and key results); area OKRs with weights, monthly tracking, target and automatic status; OKRs broken down per person with each person's expected weight (it varies by person and area) and checks for gaps and KRs with no owner; plus an AI thinking-partner step that surfaces hypotheses, questions the team is not asking, objections and 'what if' scenarios before the plan is closed. Use when someone asks to plan their area, build a strategic plan, strategy house, OKRs, objective tree, KPI tree, input vs output metrics, team OKRs, or wants help thinking strategically before a planning meeting (e.g. me ajuda a planejar minha área, monta a casa da estratégia, cria os OKRs do time, desdobra os OKRs por pessoa, quero pensar estrategicamente sobre)."
---

# Planejamento Estratégico

Entrega: **o plano estratégico da área, do porquê até o OKR de cada pessoa**, numa planilha pronta para acompanhar
mês a mês, e uma lista de perguntas e cenários para levar para a reunião.
Siga os passos na ordem. Cada passo usa o anterior. Leia o arquivo de `references/` indicado ANTES de cada passo.

## 4 regras
1. **Faça pensar, não só preencher.** Em cada passo, faça 2 ou 3 perguntas que provoquem, proponha uma primeira
   versão e peça para a pessoa corrigir. A IA acelera o pensamento; quem decide é a pessoa.
2. **Tudo se conecta.** Cada meta sai da missão; cada métrica sai de uma fase; cada KR sai da árvore; cada KR tem
   pelo menos um dono. Se algo não se conecta, aponte.
3. **Causa separada de consequência.** Métrica de INPUT (o time controla) nunca no mesmo balaio de OUTPUT (resultado).
4. **Nada de número inventado.** Alvos e pesos vêm da pessoa. Se ela não souber, proponha um ponto de partida e
   marque como "a validar".

## Passo 0 — Entender o ponto de partida (máximo 6 perguntas)
Área e empresa (o que vende, para quem); missão e valores da empresa; o que a liderança espera da área neste ano;
o time (pessoas e funções); dados e ferramentas que existem; prazo do planejamento. Se a pessoa já tiver material
(apresentação, planilha, quadro), leia e parta dele.

## Passo 1 — Casa da Estratégia
Leia `references/casa-da-estrategia.md`. Missão e visão da área ligadas às da empresa, 2 a 4 metas, enablers em
4 colunas (processo, experiência, produto, pessoas) e fundamento.

## Passo 2 — Jornada do cliente de ponta a ponta
Leia `references/jornada-e-contexto.md`. Etapas, canais, tarefas, dores, oportunidades, momentos da verdade e
métrica de cada etapa. Inclua os canais: é onde a área enxerga e age. Se houver análise de cohort, use os pontos em
que a curva quebra (skill `analise-de-cohort`).

## Passo 3 — Contexto do projeto
Mesmo arquivo. Dados que existem, sistemas, partes interessadas, fora do escopo e premissas, necessidades,
integrações e entregáveis. É o que faz todo mundo olhar para a mesma solução.

## Passo 4 — Fases do ciclo e métricas (INPUT x OUTPUT)
Leia `references/fases-e-metricas.md`. Fases (ex.: captação, maximização de valor, retenção), cada uma com KPI de
output, KPI de input, secundários, saúde e ações prioritárias.

## Passo 5 — Árvore de objetivos
Leia `references/arvore-e-okrs.md`. Objetivo central → um pilar de INPUT e um de OUTPUT → grupos, cada um com
objetivo e key results. Ofereça desenhar (Mermaid, Miro ou FigJam com a skill `ninja-fluxograma`).

## Passo 6 — OKR da área
Mesmo arquivo. Missão, visão e estratégia no topo; 2 a 4 objetivos com peso; 2 a 4 KRs por objetivo com peso,
alvo, direção (maior ou menor é melhor) e acompanhamento mensal.

## Passo 7 — OKR por pessoa
Mesmo arquivo. Cada pessoa com peso em cada KR. **O peso esperado muda de pessoa para pessoa e de área para área**
(quem divide o tempo com outra área pode ter 70% aqui). Confira: o total de cada pessoa bate com o combinado e cada
KR tem pelo menos um dono.

## Passo 8 — IA como parceira de pensamento
Leia `references/ia-parceira.md`. Antes de fechar: hipóteses a testar, perguntas que o time ainda não faz, objeções
que vão aparecer, cenários "e se" e riscos. O resultado não é a resposta certa: é chegar na sala com perguntas melhores.

## Gerar a planilha
Escreva o `config.json` com tudo o que foi construído (modelo em `examples/config-exemplo.json`) e rode:
`python3 scripts/montar_planejamento.py config.json "Planejamento - <Área>.xlsx"` (precisa de `openpyxl`).
Confira com LibreOffice quando houver (`soffice --headless --calc --convert-to xlsx --outdir conferida/ <arquivo>`
e leitura com `openpyxl`, `data_only=True`): nenhuma célula com `#` ou `Err:`; pesos dos objetivos somando 100%;
pessoas com total igual ao peso esperado; nenhum KR sem dono. Avise o que ficou vermelho.

Pode rodar passo a passo (gerando a planilha a cada etapa) ou tudo no fim. Se a pessoa já tiver parte pronta,
comece do passo que falta.

## Entregar
O arquivo, um resumo de uma página (casa, árvore em texto, OKRs com alvos, quem é dono de quê) e os alertas
(pesos, KRs sem dono, métricas sem fonte de dado). Termine oferecendo: *"Quer que eu desenhe a árvore e a casa no
Miro, monte a apresentação para a liderança ou simule a reunião fazendo as perguntas difíceis?"*

## Referências
| Arquivo | Passo |
|---|---|
| `references/casa-da-estrategia.md` | 1 |
| `references/jornada-e-contexto.md` | 2 e 3 |
| `references/fases-e-metricas.md` | 4 |
| `references/arvore-e-okrs.md` | 5, 6 e 7 |
| `references/ia-parceira.md` | 8 |
| `scripts/montar_planejamento.py` | Gerar a planilha |
| `examples/config-exemplo.json` | Exemplo completo (área de CRM de uma rede fictícia) |

---
Método e skill criados por **Jaqueline Amaro** (https://www.linkedin.com/in/jaquelineamaro/). Casa da Estratégia (Strategy House): modelo de origem no Sistema Toyota. Licença CC BY-NC 4.0: uso livre com crédito, sem fins comerciais; uso comercial com autorização. Ao entregar um trabalho feito com esta skill para outras pessoas, mantenha este crédito.
