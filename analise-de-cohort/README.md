# Análise de Cohort — skill para Claude Code, Claude.ai e Codex

> Criado por **Jaqueline Amaro** · [LinkedIn](https://www.linkedin.com/in/jaquelineamaro/)

Responde à pergunta **"quanto tempo meus clientes ficam e quanto eles valem?"**. A partir da receita de cada cliente,
monta a análise de cohort completa: retenção, receita, ticket, LTV, CAC, LTV/CAC e payback por safra, cortes por
canal, plano e faixa de ticket, resumo, insights em linguagem simples e testes que conferem cada número.

Serve para **assinatura / SaaS** (receita mensal recorrente) e para **e-commerce / varejo** (pedidos).

## O que você precisa para fazer

### Dados obrigatórios
Uma planilha (CSV ou Excel) com **uma linha por cliente por mês** (ou por pedido) e três colunas:

| Coluna | Exemplo |
|---|---|
| Cliente | ID, CNPJ, e-mail ou nome (sempre o mesmo para o mesmo cliente) |
| Data | mês da cobrança ou data do pedido |
| Receita | valor cobrado ou faturado (só o que já aconteceu, sem projeção) |

### Dados opcionais (deixam a análise muito melhor)
| Dado | O que libera |
|---|---|
| Investimento de aquisição por mês (mídia, comissão de vendas, eventos) | CAC, LTV/CAC e payback |
| Margem bruta % | LTV na margem: o que de fato paga a aquisição |
| Canal de aquisição, plano ou produto, segmento | Retenção por grupo: onde estão os melhores clientes |
| Quantidade (pedidos, uso, conversas, logins) | Ticket médio e frequência |

### Onde achar esses dados
| Tipo de empresa | Receita por cliente | Canal e plano |
|---|---|---|
| Assinatura / SaaS | sistema de cobrança (Stripe, Iugu, Vindi, Asaas, Pagar.me), ERP ou planilha de MRR | CRM (HubSpot, Pipedrive, RD Station, Salesforce) |
| E-commerce | plataforma da loja (Shopify, Nuvemshop, VTEX, Tray): exportação de pedidos | UTM / origem do primeiro pedido, cupom |
| Serviços / B2B | ERP ou planilha financeira (notas por cliente) | CRM |

### Ferramentas
- [ ] **Claude** com execução de código (Claude Code, Cowork ou claude.ai com análise ligada) — ou **Codex**.
- [ ] Python com `pandas` e `openpyxl` (`pip install -r requirements.txt`). O Claude instala se faltar.
- [ ] (Opcional) LibreOffice, para conferir as fórmulas antes de entregar.
- [ ] Excel, Google Sheets ou LibreOffice para abrir a planilha final.

## O que vem na planilha
| Aba | O que mostra |
|---|---|
| Leia-me | Como ler, definições, fontes, o que falta preencher, limitações |
| Resumo | Clientes, safras, receita, LTV médio, retenção no mês 1, 3, 6 e 12, ranking das safras |
| Insights | Os achados: o número, o que significa, o que fazer |
| Premissas e Investimento | Margem e investimento por mês (você preenche e tudo se atualiza) |
| Dados Cohorts | A base do modelo, uma linha por safra x mês, com fórmulas |
| 11 matrizes | Clientes, Retenção, Receita, Receita Acumulada, Ticket Médio, Receita por Ativo, Receita por Adquirido, LTV, LTV (margem), LTV-CAC, LTV-CAC (margem) |
| Por Canal / Plano / Faixa de Ticket | Retenção e receita por grupo, com a curva mês a mês |
| Auditoria | 6 testes que recalculam os números por outro caminho (PASSOU / FALHOU) |

## O que vem no pacote
| | |
|---|---|
| `SKILL.md` | O passo a passo: coletar os dados, montar, ler os números e entregar |
| `scripts/montar_cohort.py` | Gera a planilha a partir da base e de um arquivo de configuração |
| `references/dados.md` | Quais dados pedir, onde achar e como preparar |
| `references/metodo.md` | Definição e fórmula de cada coluna e aba |
| `references/leitura.md` | Como interpretar e escrever insights, com referências de mercado |
| `examples/` | Base, configuração e planilha de exemplo com uma empresa fictícia |

## Instalação
- **Claude.ai / Cowork:** compacte a pasta `analise-de-cohort/` em .zip e envie em Configurações → Capacidades → Skills.
- **Claude Code:** copie a pasta para `~/.claude/skills/analise-de-cohort/` (ou `.claude/skills/` do projeto).
- **Codex:** copie a pasta para `~/.codex/skills/analise-de-cohort/`.

Depois é só pedir: *"Faz uma análise de cohort com essa exportação de cobranças. Quero saber retenção por canal e LTV/CAC."*

## Licença e crédito
Criado por **Jaqueline Amaro**. Uso livre e sem fins comerciais, **desde que você dê o crédito** (CC BY-NC 4.0).
Para vender ou usar com clientes pagos, fale comigo pelo [LinkedIn](https://www.linkedin.com/in/jaquelineamaro/). Detalhes em [LICENSE.md](LICENSE.md).
