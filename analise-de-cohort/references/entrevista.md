# Entrevista antes do cohort

Não existe cohort genérico. O que é "cliente", "entrou", "está ativo" e "usou" muda de negócio para negócio.
Faça esta entrevista **antes de pedir qualquer arquivo**. Em blocos curtos, no máximo 6 perguntas por vez.

## Bloco 1 — O negócio
1. O que a empresa vende e como cobra? (mensalidade, contrato com prazo, pedido avulso, por uso, comissão)
2. Quem é o cliente: empresa (CNPJ), pessoa, conta, unidade? Um cliente pode ter mais de um contrato, conta ou plano?

## Bloco 2 — As 4 definições (as mais importantes)
| Definição | Pergunta | Exemplos |
|---|---|---|
| **Entrada** | Quando um cliente "nasce"? | primeira cobrança, início do primeiro contrato, primeira compra, primeira viagem |
| **Ativo no mês** | O que precisa acontecer para contar como ativo? | pagou; tem contrato vigente; comprou; usou pelo menos 1 vez |
| **Receita** | Qual valor conta? | mensalidade cobrada, valor do pedido sem frete, comissão, prêmio |
| **Uso / atividade** | Qual número mostra que o cliente está usando? Pode ter mais de um | conversas, pedidos, logins, viagens, km, passagens, contratos vigentes |

Escreva as quatro definições e **confirme com a pessoa** antes de montar. Elas vão para a aba Leia-me.

## Bloco 3 — Período e fontes
3. De que mês até que mês os dados são reais? Há meses projetados ou contratados que devem ficar fora?
4. Onde está cada dado? (cobrança, ERP, CRM, banco de dados, planilha) Quem consegue exportar?
5. Existe investimento de aquisição por mês? E a margem bruta?
6. Quais cortes importam? (canal, plano, produto, região, segmento, faixa de ticket, vendedor)

## Bloco 4 — Para depois do cohort
7. O que vocês querem decidir com isso? (onde investir em aquisição, onde está o churn, como montar onboarding,
   o que oferecer para quem fica)
8. Quais etapas o cliente vive hoje depois da compra? Quem cuida de cada uma? (alimenta a Jornada, Fase 5)

## Exemplos de como as definições mudam (modelos de negócio, sem nomes)
| Modelo | Entrada | Ativo no mês | Receita | Uso / atividade | Formato da base |
|---|---|---|---|---|---|
| Software de atendimento com IA | 1º mês com mensalidade | pagou a mensalidade | MRR | conversas atendidas, usuários | linha por cliente x mês |
| Seguro-fiança / garantia de aluguel | início do 1º contrato | tem contrato vigente | mensalidade ou prêmio | contratos vigentes ao mesmo tempo, meses de cobertura | contratos (início, fim, valor) |
| Transporte / viagens | 1ª viagem paga | viajou no mês | valor das passagens | passagens, km rodados, trechos | linha por cliente x viagem |
| E-commerce | 1º pedido | comprou no mês | valor do pedido sem frete | pedidos, itens | linha por pedido |
| Assinatura de produto | 1ª cobrança | assinatura paga | mensalidade | caixas entregues, pausas | linha por cliente x mês |
| Serviços B2B / consultoria | 1ª nota emitida | teve nota no mês (ou contrato vigente) | valor faturado | horas, projetos | notas ou contratos |
| Marketplace / app | 1ª transação | transacionou no mês | receita da plataforma (take rate) | transações, GMV | linha por transação |

## Como isso vira configuração
| Resposta | Campo no `config.json` |
|---|---|
| Base é de contratos com início e fim | `"formato": "contratos"` + `colunas.inicio`, `colunas.fim` |
| Ativo é "usou", não "pagou" | `"ativo_por": "<nome da métrica>"` (ex.: `"passagens"`) |
| Métricas de uso | `"metricas": {"passagens": "coluna_passagens", "km": "coluna_km"}` |
| Quantidade para o ticket médio | `colunas.quantidade` |
| Definições confirmadas | `"definicao_entrada"`, `"definicao_ativo"` (texto para o Leia-me) |
| Último mês real | `"ate": "AAAA-MM-01"` |

Com `"formato": "contratos"`, a métrica `contratos_ativos` é criada sozinha: mostra se os clientes que ficam
passam a ter mais de um contrato.
