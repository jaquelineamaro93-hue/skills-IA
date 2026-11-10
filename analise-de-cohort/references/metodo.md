# Método: definições e fórmulas

## Aba Dados Cohorts (uma linha por safra x mês)
| Coluna | Fórmula | O que é |
|---|---|---|
| cohort | mês da 1ª receita > 0 do cliente | a safra |
| mes | mês do calendário | |
| mes_indice | meses desde a entrada (0, 1, 2...) | |
| clientes_ativos | clientes da safra com receita > 0 no mês | |
| clientes_cohort | clientes da safra no mês 0 | base fixa |
| retencao | clientes_ativos ÷ clientes_cohort | |
| qtd | pedidos / uso no mês (opcional) | |
| qtd_por_cliente | qtd ÷ clientes_ativos | frequência |
| receita_mes | soma da receita da safra no mês | |
| margem | receita_mes × margem % (Premissas) | |
| receita_acum | soma corrida da receita desde o mês 0 | |
| margem_acum | soma corrida da margem | |
| ticket_medio | receita_mes ÷ qtd (ou ÷ clientes ativos, sem qtd) | |
| receita_por_ativo | receita_mes ÷ clientes_ativos | quanto deixa quem ficou |
| receita_por_adquirido | receita_mes ÷ clientes_cohort | já desconta quem saiu |
| ltv | receita_acum ÷ clientes_cohort | |
| ltv_margem | margem_acum ÷ clientes_cohort | |
| cac | investimento da safra ÷ clientes_cohort | aba Investimento |
| ltv_cac | ltv ÷ cac | |
| ltv_cac_margem | ltv_margem ÷ cac | ≥ 1 = cliente já pagou a aquisição |

As matrizes (Clientes, Retenção, Receita, Receita Acumulada, Ticket Médio, Receita por Ativo, Receita por Adquirido,
LTV, LTV (margem), LTV-CAC, LTV-CAC (margem)) apontam para essas colunas: safra nas linhas, mês 0, 1, 2... nas
colunas. Mudar a margem em Premissas ou o investimento atualiza tudo.

## Payback
Primeiro mês em que **LTV-CAC (margem) ≥ 1** na linha da safra (a matriz pinta de verde). É quanto tempo o cliente
leva para devolver o custo de conquistá-lo.

## Retenção ponderada (Resumo)
Para o mês N: soma dos clientes ativos no mês N de todas as safras que já chegaram ao mês N ÷ soma dos clientes
dessas safras. Safras recentes, que ainda não viveram o mês N, ficam fora da conta.

## Cortes por grupo (Por Canal, Por Plano, Por Faixa de Ticket)
- Cada cliente fica no grupo da sua primeira informação (canal da entrada, plano inicial).
- Faixa de ticket: pelo maior valor mensal (pico) do cliente.
- Retenção mês a mês do grupo: todas as safras juntas; a base de cada mês só tem quem já teve tempo de chegar nele.
- Grupos com menos de 10 clientes: leia como sinal, não como conclusão.

## Testes da Auditoria
1. Receita total da base = receita total do modelo.
2. Clientes com receita na base = soma dos clientes das safras.
3. Receita do último mês confere.
4. Retenção nunca acima de 100%.
5. Cada cliente em uma única safra.
6. Mês 0 com 100% dos clientes de cada safra.
Teste que falha = parar e investigar antes de qualquer conclusão.

## Recorrente x pedidos
- **Recorrente (assinatura/SaaS):** cliente ativo = pagou no mês. Retenção cai em degraus (cancelamentos).
- **Pedidos (e-commerce):** cliente ativo = comprou no mês. A retenção mensal costuma ser baixa (pouca gente compra
  todo mês); para e-commerce, olhe também a recompra acumulada (quantos já voltaram pelo menos uma vez até o mês N)
  e use janelas maiores (trimestre) se o ciclo de compra for longo.
