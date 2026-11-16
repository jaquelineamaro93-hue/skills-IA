# Calibração: validar antes de decidir

Um score não calibrado é um palpite com cara de número. Antes de usar a faixa para priorizar atendimento, faça estes três passos.

## 1. Separação com histórico
- Pegue clientes que saíram e clientes que renovaram nos últimos 6 a 12 meses.
- Calcule o score de cada um como estava 2 a 3 meses antes do desfecho.
- Compare a distribuição de faixas e a média dos vetores.
- Se os dois grupos não se separam, o modelo está errado. Ajuste pesos, critérios ou vetores e refaça.

Sinal de que está bom: quem saiu concentra mais vermelho e quem renovou concentra mais verde. Não precisa ser perfeito; precisa ser melhor que a intuição do time.

## 2. Paralelo com a percepção do time
- Por um ou dois ciclos, a pessoa que conhece o cliente dá a própria faixa antes de ver o score.
- Compare. Quando discordarem, investigue:
  - O modelo viu algo que a pessoa não viu? Então o score está ajudando.
  - Falta um sinal no modelo? Então adicione o sinal, com evidência.
  - O dado está atrasado ou incompleto? Então corrija a fonte.

## 3. Notas com evidência
Para cada nível de cada vetor, escreva um exemplo concreto. Ex.: "P1 = 2 em Uso: entre 3 e 7 dias ativos nos últimos 28 dias". Sem exemplo, duas pessoas dão notas diferentes para o mesmo cliente.

## Só depois disso
Ligue o score a rituais de gestão: priorização da carteira, alertas de risco, metas de expansão. Antes disso, ele fica como lista de conferência.

## Alertas de honestidade
- Score recém-criado, sem histórico de desfecho, não é validado. Diga isso no relatório.
- Clientes em trial, cortesia ou desconto devem ter o score lido separadamente de pagantes.
- Nunca mude o histórico para caber no modelo novo. Recalcule o passado com o modelo novo e guarde os dois.
