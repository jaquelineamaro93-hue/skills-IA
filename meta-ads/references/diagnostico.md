# Modo 3: diagnóstico de campanhas

## Como exportar do Gerenciador de Anúncios
1. Escolha o nível: campanha, conjunto ou anúncio. Para achar desperdício, comece por **conjunto**; para criativo, **anúncio**.
2. Período: últimos 7 a 30 dias. Menos que 7 dias quase nunca tem dado suficiente.
3. Colunas: nome, valor usado, impressões, alcance, frequência, cliques no link, resultados (ou compras / leads) e, se for e-commerce, valor de conversão de compras.
4. Exportar → CSV. O script aceita português ou inglês, vírgula ou ponto e vírgula.

## CPA máximo (o alvo de verdade)
Sem alvo, o script usa a mediana da conta. Isso só diz quem está pior que a média, não quem dá prejuízo. Calcule:

- **Venda única:** `CPA máximo = margem de contribuição por venda × fração que você aceita investir` (ex.: margem R$ 200 × 50% = R$ 100).
- **Cliente que volta:** use a margem do LTV de 12 meses no lugar da margem por venda, se houver caixa para esperar o retorno.
- **Lead:** `custo máximo por lead = CPA máximo × taxa de conversão de lead em venda` (ex.: R$ 100 × 10% = R$ 10).
- **ROAS mínimo para empatar:** `1 ÷ margem percentual` (margem de 40% → ROAS 2,5).

Passe o resultado no `--cpa-alvo` ou `--roas-alvo`.

## Regras de decisão (as do script)
| Decisão | Quando |
|---|---|
| CORTAR | Gastou 3× o CPA de referência sem nenhum resultado, ou CPA acima de 1,5× a referência (ROAS abaixo de 0,65× o alvo) |
| AJUSTAR | CPA entre 1,2× e 1,5× (ROAS entre 0,65× e 0,85×). Troque criativo ou público antes de cortar |
| MANTER | CPA até 1,2× (ROAS a partir de 0,85×) |
| ESCALAR | CPA até 0,8× (ROAS 1,25×+), com 5+ resultados e sem fadiga |
| AGUARDAR | Gastou menos de 2× a referência e tem menos de 3 resultados |

Os cortes são pontos de partida. Ajuste se o negócio pedir (ex.: lançamento com prazo curto aceita CPA maior).

## Alertas (independentes da decisão)
- **Fadiga:** frequência acima de 3 em prospecção (`--freq-max`). Em remarketing, frequência maior é normal; use `--freq-max 6` ao analisar só remarketing.
- **Criativo fraco:** CTR de link abaixo de 0,8% (`--ctr-min`). Se o CTR é bom e o CPA é ruim, o problema está depois do clique: página, oferta ou preço (Modo 5).
- **Público caro:** CPM acima de 1,5× a mediana da conta. Público pequeno demais ou muito disputado.

## Leitura que o número sozinho não dá
- **Fase de aprendizado:** o Meta precisa de cerca de 50 eventos de otimização por conjunto em 7 dias para estabilizar. Conjunto em aprendizado oscila; evite julgar ou editar muito nessa fase.
- **Edição reinicia o aprendizado:** mudanças grandes de orçamento, público ou criativo zeram a fase. Ao escalar, prefira aumentos graduais (prática comum: cerca de 20% a cada 2 ou 3 dias) ou duplicar o conjunto.
- **Atribuição:** o padrão é 7 dias após o clique e 1 dia após a visualização. Compare sempre na mesma janela.
- **Advantage+ e campanhas automáticas** concentram verba no que performa; "conjunto com pouco gasto" ali não é problema.
- **O Meta conta o evento, não a venda boa.** Se a meta é lead, cruze com o CRM (Modo 4) antes de escalar.

## Como entregar
1. Quanto da verba está em itens para cortar (o script imprime). Esse é o número que abre a resposta.
2. Lista CORTAR e ESCALAR com o motivo de cada um.
3. AJUSTAR com a hipótese (criativo, público ou página) e o teste.
4. Próximos 3 passos em ordem.
