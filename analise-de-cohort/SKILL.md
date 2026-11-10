---
name: analise-de-cohort
description: "Builds a complete customer cohort analysis spreadsheet (.xlsx) from revenue per customer: subscription/SaaS (monthly recurring revenue) or e-commerce/retail (orders). Groups customers by the month of their first revenue, then builds retention, revenue, cumulative revenue, average ticket, revenue per active and per acquired customer, LTV, LTV on margin, CAC, LTV/CAC and payback matrices with live formulas; retention and revenue cuts by channel, plan, segment and ticket range; a summary, written insights (what the number is, what it means, what to do), a read-me with definitions and data sources, and validation tests that recheck every key number by an independent path. Also tells the person exactly which data to collect and from where, and explains how to read the results. Use when someone asks for a cohort analysis, retention analysis, churn by cohort, LTV, LTV/CAC, payback, safra de clientes, curva de retenção, or sends a revenue/orders export asking how customers are retaining (e.g. faz uma análise de cohort, quanto meus clientes ficam, qual meu LTV, retenção por canal)."
---

# Análise de Cohort

Entrega: **uma planilha de cohort pronta**, com fórmulas vivas, cortes por canal/plano/faixa, resumo, insights e
testes de conferência, mais uma leitura em linguagem simples do que os números mostram.
Siga as fases na ordem. Leia o arquivo de `references/` indicado em cada fase ANTES de executá-la.

## O que é preciso para fazer
**Dados (obrigatório):** uma base com **uma linha por cliente por mês** (ou por pedido) contendo:
| Coluna | Exemplo | Observação |
|---|---|---|
| Cliente | ID, CNPJ, e-mail ou nome | sempre o mesmo identificador para o mesmo cliente |
| Data | mês da cobrança ou data do pedido | o modelo agrupa por mês |
| Receita | valor cobrado/faturado | só receita reconhecida, sem projeção |

**Dados (opcional, deixam a análise muito melhor):**
| Dado | Libera |
|---|---|
| Investimento de aquisição por mês (mídia, comissão, eventos) | CAC, LTV/CAC e payback |
| Margem bruta % | LTV (margem): o que de fato paga a aquisição |
| Canal de aquisição, plano/produto, segmento | retenção por grupo: onde estão os melhores clientes |
| Quantidade (pedidos, uso, conversas, logins) | ticket médio e frequência |
| Status/motivo de churn | conferência e explicação das saídas |

**Ferramentas:** Claude com execução de código (Claude Code, Cowork ou claude.ai com análise ligada) ou Codex;
Python com `pandas` e `openpyxl` (o Claude instala se faltar); LibreOffice opcional, para conferir as fórmulas.
**Onde achar os dados:** ver `references/dados.md` (sistema de cobrança, ERP, plataforma de e-commerce, CRM, planilha financeira).

## 5 regras
1. **Só receita real.** Meses projetados, contratados ou em negociação ficam fora. Diga até que mês vai o horizonte.
2. **Um critério de entrada para todos:** o cohort é o mês da primeira receita maior que zero.
3. **Nunca invente número.** Sem investimento, CAC fica em branco; sem margem real, avise que a margem é premissa.
4. **Confira antes de concluir.** Rode os testes de auditoria e conte o que passou e o que precisa de confirmação.
5. **Dados de clientes são confidenciais.** Nomes de clientes não vão para exemplos, apresentações públicas ou
   material de terceiros. Use IDs quando a planilha for circular fora do time.

## Fase 1 — Coletar e entender a base
Leia `references/dados.md`. Peça a base (CSV ou XLSX) e as informações opcionais da tabela acima. Leia os arquivos
e mostre um diagnóstico curto: período, número de clientes, formato (linha por mês ou por pedido), colunas que serão
usadas, problemas (clientes duplicados com grafias diferentes, meses sem valor, valores negativos, meses futuros).
Se a base vier em formato de grade (clientes nas linhas, meses nas colunas), transforme em formato longo antes.

## Fase 2 — Montar a planilha
Leia `references/metodo.md`. Escreva o `config.json` (modelo em `examples/config-exemplo.json`): `empresa`, `tipo`
(`recorrente` ou `pedidos`), `base`, `colunas`, `segmentos`, `faixas_ticket`, `margem`, `investimento`, `ate`
(último mês real), `fontes`, `limitacoes`. Rode:
`python3 scripts/montar_cohort.py config.json "Analise de Cohort - <Empresa>.xlsx"`
Recalcule e confira com LibreOffice quando houver
(`soffice --headless --calc --convert-to xlsx --outdir conferida/ "<arquivo>.xlsx"`, depois `openpyxl` com
`data_only=True`): nenhuma célula pode começar com `#` ou `Err:`. Todos os testes da aba Auditoria devem passar;
se algum falhar, investigue antes de seguir.

## Fase 3 — Ler os números e escrever os insights
Leia `references/leitura.md`. Encontre de 3 a 6 achados, cada um com **o número**, **o que significa** e
**o que fazer**. Procure sempre: onde a curva de retenção quebra, quais safras são melhores e por quê, qual canal /
plano / faixa retém mais, LTV/CAC e payback (se houver investimento), concentração de receita em poucos clientes,
e as lacunas da base. Coloque os achados no campo `insights` do config e gere a planilha de novo.

## Fase 4 — Entregar
Entregue o arquivo e uma mensagem com:
- Os 3 números principais (ex.: retenção no mês 6, LTV, LTV/CAC).
- Os achados (curtos), em linguagem simples.
- O que falta preencher (investimento, margem) e o que precisa de confirmação (clientes com dado estranho).
- Como atualizar: substituir a base, rodar o script de novo; ou preencher Investimento e Premissas direto na planilha.

Termine oferecendo: *"Quer que eu aprofunde algum corte, compare safras específicas ou monte uma apresentação com esses achados?"*

## Referências
| Arquivo | Quando ler |
|---|---|
| `references/dados.md` | Fase 1: quais dados, onde achar, como preparar |
| `references/metodo.md` | Fase 2: definições e fórmulas de cada coluna e aba |
| `references/leitura.md` | Fase 3: como interpretar e escrever os insights |
| `scripts/montar_cohort.py` | Fase 2 |
| `examples/` | Base e configuração de exemplo (empresa fictícia) |

---
Skill criada por **Jaqueline Amaro** (https://www.linkedin.com/in/jaquelineamaro/). Licença CC BY-NC 4.0: uso livre com crédito, sem fins comerciais; uso comercial com autorização. Ao entregar um trabalho feito com esta skill para outras pessoas, mantenha este crédito.
