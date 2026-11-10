---
name: planilha-de-growth
description: "Builds a complete growth command-center spreadsheet (.xlsx) for any brand, especially DTC / e-commerce / product launches, with formulas, dropdowns and alerts already in place: tasks by workstream, Brazilian commercial calendar for the year, product cost, price and margin (including margin after coupon), competitor benchmark (price per unit), influencer / UGC / affiliate control with coupon ROI, partnership rules and affiliate tiers, content requests, ad creative briefs, ad creative performance (CTR, CPA, ROAS), CRM journey catalog (cadastral, transactional, relational, promotional, seasonal), events and activations budget, giveaway stock and waitlist. Interviews the person briefly, fills what it can (products, costs, competitors, team, launch dates) and explains how to run each tab. Also reviews an existing growth spreadsheet and points out gaps. Use when someone asks for a growth spreadsheet, growth planning, launch plan, go-to-market tracker, influencer control sheet, pricing and margin sheet, commercial calendar, CRM journey list or marketing task tracker (e.g. monta minha planilha de growth, planilha para lançamento da marca, controle de influenciadores, precificação e margem, calendário comercial do ano)."
---

# Planilha de Growth

Entrega: **uma planilha .xlsx pronta para o time de growth usar no dia a dia**, com as abas que a marca precisa,
fórmulas, listas de opções e alertas, já preenchida com o que a pessoa contou.
Siga as fases na ordem. Leia o arquivo de `references/` indicado em cada fase ANTES de executá-la.

## 5 regras
1. **Nunca invente número.** Custo, preço, imposto, comissão, meta: se a pessoa não disse, deixe a célula vazia
   para ela preencher e liste no fim o que falta.
2. **Só as abas que fazem sentido.** Marca sem influenciadores não precisa da aba de influenciadores. Pergunte.
3. **Planilha para gente, não para robô.** Nomes de abas e colunas em português simples; células de preencher em
   creme, células de fórmula em cinza; alertas em vermelho.
4. **Dados pessoais fora.** Não coloque CPF, endereço ou telefone de pessoas na planilha geral (LGPD). Se a pessoa
   enviar uma planilha antiga com esses dados, não copie para a nova.
5. **Fórmulas testadas.** Gere a planilha com o script, recalcule e confira que nenhuma célula dá erro antes de entregar.

## Fase 1 — Entender a marca (no máximo 6 perguntas, de uma vez)
1. Nome da marca, o que vende e em quais canais (site próprio, marketplace, varejo, revenda).
2. Em que momento está: pré-lançamento, lançamento ou já vendendo.
3. Quais frentes o time toca: conteúdo e redes, mídia paga, influenciadores e UGC, CRM, eventos e ativações.
4. Produtos com custos (se tiver) e preço de venda (se já tiver).
5. Quem está no time (para as listas de responsável) e datas importantes (lançamento, aniversário da marca).
6. Concorrentes que querem acompanhar.

Se a pessoa mandar uma planilha que já usa: leia, entenda as abas e use como ponto de partida (modo **Revisão**,
na Fase 4). Se mandar material solto (planilha de custos, lista de influenciadores), aproveite os números e a estrutura.

## Fase 2 — Escolher as abas
Leia `references/abas.md`. Monte a lista de abas a partir das respostas. Padrão para marca em lançamento: todas.

| Chave no config | Aba |
|---|---|
| `tarefas` | Tarefas por frente |
| `calendario` | Calendário comercial do ano |
| `custos_preco` | Custo do produto + Preço e margem |
| `concorrentes` | Comparação com concorrentes |
| `influenciadores` | Influenciadores, UGC e afiliados |
| `regras_parceria` | Regras de parceria e programa de afiliados |
| `demandas` | Demandas de conteúdo e peças |
| `briefing` | Briefing de criativos |
| `criativos` | Desempenho dos criativos |
| `reguas` | Réguas de CRM |
| `eventos` | Eventos e ativações |
| `brindes` | Brindes, estoque de envios e lista de espera |

## Fase 3 — Gerar a planilha
1. Escreva o `config.json` (modelo em `examples/config-exemplo.json`) com: `empresa`, `ano`, `abas`,
   `responsaveis`, `produtos` (custos por unidade e `preco_final`, quando houver), `imposto`, `margem_minima`,
   `espaco_cupom`, `cupom_padrao`, `concorrentes`, `eventos_internos`, e, se quiser, `tarefas` e `afiliados`
   próprios. Campo que a pessoa não informou fica fora.
2. Rode: `python3 scripts/montar_planilha.py config.json "Planilha de Growth - <Marca>.xlsx"` (precisa de `openpyxl`).
3. Recalcule e confira (com LibreOffice, quando houver):
   `soffice --headless --calc --convert-to xlsx --outdir conferida/ "<arquivo>.xlsx"`, depois leia com
   `openpyxl` (`data_only=True`) e confirme que nenhuma célula começa com `#` (erro).
4. Veja a aba Preço e margem: se algum produto ficou vermelho (margem com cupom abaixo da mínima), avise a pessoa.
   Detalhes do cálculo em `references/preco-e-margem.md`.

## Fase 4 — Entregar e ensinar a usar
Entregue o arquivo e uma mensagem curta com:
- **O que tem em cada aba**, uma linha por aba.
- **O que já veio preenchido** e **o que falta ela preencher** (lista objetiva).
- **Alertas encontrados** (ex.: "com cupom de 15%, a Granola Cacau fica com 48,6% de margem, abaixo dos 50%").
- **Ritmo sugerido:** Tarefas toda semana; Criativos e Influenciadores a cada 15 dias; Preço e margem a cada
  mudança de custo; Calendário um mês antes de cada data.

Modo **Revisão** (a pessoa mandou a planilha que já usa): compare com `references/abas.md` e diga o que falta
(abas, colunas, fórmulas, alertas), o que está duplicado ou abandonado, e ofereça gerar a versão nova já com os
dados úteis migrados (sem dados pessoais).

Para orientar o uso de cada frente, use `references/influenciadores-e-criativos.md` e `references/reguas-e-calendario.md`.

Termine oferecendo: *"Quer que eu ajuste alguma aba, acrescente uma frente nova ou analise os números quando a planilha estiver preenchida?"*

## Referências
| Arquivo | Quando ler |
|---|---|
| `references/abas.md` | Fase 2 e modo Revisão |
| `references/preco-e-margem.md` | Fase 3 e quando falar de preço |
| `references/influenciadores-e-criativos.md` | Fase 4, para orientar influenciadores, conteúdo e mídia |
| `references/reguas-e-calendario.md` | Fase 4, para orientar CRM e datas |
| `scripts/montar_planilha.py` | Fase 3 |
| `examples/config-exemplo.json` | Modelo de configuração (marca fictícia) |

---
Skill criada por **Jaqueline Amaro** (https://www.linkedin.com/in/jaquelineamaro/). Licença CC BY-NC 4.0: uso livre com crédito, sem fins comerciais; uso comercial com autorização. Ao entregar um trabalho feito com esta skill para outras pessoas, mantenha este crédito.
