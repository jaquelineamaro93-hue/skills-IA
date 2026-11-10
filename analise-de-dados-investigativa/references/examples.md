# Exemplos de Analise — Input/Output

Estes exemplos calibram o nivel de profundidade, tom e estrutura esperados. Use como referencia para todas as analises.

---

## Exemplo 1: Planilha de Leads de Campanha (Modo Focado)

### Input do usuario
> "Tenho uma planilha com 1.200 leads gerados nos ultimos 3 meses por 4 canais diferentes (Google Ads, Meta, Indicacao, Organico). Colunas: nome, telefone, canal, cidade, data de entrada, status (novo, qualificado, proposta, fechado, perdido), valor do deal. Quero entender por que a conversao caiu no ultimo mes."

### Output esperado

**Enquadramento:**
> "Tipo principal: Explicacao (por que a conversao caiu). Tipo secundario: Oportunidade (o que podemos recuperar)."

**Fase 1 — Reconhecimento:**
> "Dataset com 1.200 registros, 8 variaveis. Periodo: Jan-Mar/2026. Completude: 98% (24 registros sem 'valor do deal' — todos com status 'perdido', faz sentido). Distribuicao por canal: Google Ads 520 (43%), Meta 380 (32%), Organico 210 (18%), Indicacao 90 (7%). Granularidade: por lead individual, com timestamp de entrada."

**Fase 2 — Base:**
> Taxa de conversao geral: 11.2%. Ticket medio: R$4.800. Evolucao mensal: Jan 13.5%, Fev 12.1%, Mar 8.0%. A queda de marco e real — 5.5pp abaixo de janeiro.

**Achados nao-convencionais (selecao):**

> **Achado 1 — Sinal Fraco (Lente 1):** O canal "Indicacao" tem apenas 90 leads (7%) mas taxa de conversao de 31% vs. 11% geral. Em marco, Indicacao caiu de 12 leads/mes para 5 — coincidindo com a saida de um vendedor senior que gerava a maioria das indicacoes. A queda de conversao geral pode ser parcialmente explicada pela perda desse micro-canal de alta performance.
> - Confianca: Moderada (N pequeno mas padrao consistente em 3 meses)
> - Decisao sugerida: Investigar se ha programa de indicacao formal. Se nao, criar um e testar por 30 dias.

> **Achado 2 — Inversao (Lente 2):** 15 leads de Google Ads marcados como "perdido" tinham valor de deal >R$10.000 (2.5x o ticket medio). Todos entraram as sextas-feiras apos 17h e tiveram primeiro contato apenas na segunda-feira. Hipotese: leads de alto valor que entram no fim de semana esfriam em 48h.
> - Confianca: Moderada (15 casos, mas padrao temporal claro)
> - Decisao sugerida: Testar atendimento automatizado imediato (WhatsApp) para leads que entram sexta >17h. Custo baixo, impacto potencial alto.

**Sintese em 3 camadas:**
> Camada 1: Conversao caiu 5.5pp em marco. Google Ads e Meta sao responsaveis por 85% da queda.
> Camada 2: Dois fatores convergentes — perda do canal de indicacao (vendedor) + aumento de leads de baixa qualidade no Meta (CTR subiu 40% mas conversao caiu 60%, indicando mudanca de publico).
> Camada 3: Oportunidade oculta — leads de fim de semana com alto valor estao sendo perdidos por tempo de resposta. Recuperar esses 15 leads/mes a 30% de conversao = +R$45k/mes potencial.

**TL;DR:**
> - Queda de conversao explicada por dois fatores: perda do canal Indicacao (-1 vendedor) e degradacao de qualidade no Meta. Decisao: auditar campanha Meta e criar programa de indicacao.
> - Leads de alto valor (>R$10k) entram sexta a noite e sao atendidos so na segunda — 48h de delay mata a conversao. Decisao: testar resposta automatizada imediata.
> - Canal Indicacao converte 3x mais que a media com 7% do volume. Decisao: escalar indicacoes como canal estrategico, nao como acidente.

---

## Exemplo 2: Logs de Conversa de Chatbot (Modo Focado)

### Input do usuario
> "Tenho 200 conversas exportadas do bot de vendas no WhatsApp. Quero saber por que so 12% estao chegando ate a proposta."

### Output esperado

**Enquadramento:**
> "Tipo principal: Diagnostico (onde estao perdendo). Tipo secundario: Explicacao (por que perdem nesses pontos)."

**Fase 1 — Reconhecimento:**
> "200 conversas, periodo de 30 dias. Media de 8.3 mensagens por conversa. Distribuicao por desfecho: 24 (12%) chegaram a proposta, 89 (44.5%) abandonaram na qualificacao, 52 (26%) abandonaram na saudacao, 35 (17.5%) transferidos para humano."

**Achado (Lente 4 — Quali-Quanti):**
> Analisando as 24 conversas que chegaram a proposta vs. as 89 que abandonaram na qualificacao: a palavra "preco" aparece em 71% das que abandonaram, mas apenas em 25% das que avancaram. Nas conversas bem-sucedidas, o lead pergunta "como funciona" antes de perguntar "quanto custa". Hipotese: leads que entendem o valor antes de ver o preco convertem 3x mais.
> - Confianca: Alta (N razoavel, padrao linguistico claro e consistente)
> - Decisao sugerida: Reestruturar o fluxo do bot para apresentar beneficios/cases antes do preco. Testar 2 semanas e comparar taxa de proposta.

**Achado (Lente 6 — Lacunas):**
> Das 52 conversas que abandonaram na saudacao, 31 (60%) aconteceram entre 22h e 7h. O bot responde, mas a mensagem e generica. Zero conversas noturnas chegaram a proposta. Hipotese: perfil noturno e diferente (mais pesquisa, menos compra imediata).
> - Confianca: Moderada (padrao claro mas sem dados de perfil para confirmar)
> - Decisao sugerida: Criar mensagem noturna diferenciada ("Vi que esta pesquisando sobre [produto]. Posso te mandar um resumo rapido?") e medir impacto.

---

## Exemplo 3: Modo Rapido (Dataset Simples)

### Input do usuario
> "Da uma olhada rapida nessa planilha de vendas do mes passado."

### Output esperado

> **Enquadramento:** Monitoramento (como foi o mes).
>
> **Reconhecimento rapido:** 340 registros, marco/2026. 12 vendedores, 5 produtos, 8 cidades. Completude: 100%.
>
> **TL;DR:**
> - Vendedor Carlos responde por 28% da receita total com apenas 15% dos deals — ticket medio 2x maior que a equipe. Decisao: entender e replicar seu processo.
> - Produto X tem volume alto mas margem 40% menor que a media. Decisao: revisar pricing ou reposicionar.
> - Cidade Y cresceu 180% vs. mes anterior com apenas 2 vendedores cobrindo. Decisao: alocar mais recursos antes que a demanda esfrie.
>
> Quer que eu aprofunde algum desses achados?

---

## O que NAO fazer

- **Nao liste estatisticas sem interpretacao.** "A media de mensagens e 8.3" nao e um insight. "Conversas com >12 mensagens convertem 2x mais, sugerindo que engajamento profundo e preditor de compra" e um insight.
- **Nao apresente todos os achados com o mesmo peso.** Priorize os 3-5 mais impactantes. O resto vai para nota ou apendice.
- **Nao alucine numeros.** Se os dados nao suportam, diga: "Os dados sugerem X, mas com N=15 nao e possivel confirmar estatisticamente."
- **Nao ignore o pedido original.** Se o usuario perguntou "por que a conversao caiu", a resposta principal deve ser sobre isso. Oportunidades nao-convencionais sao bonus, nao substituto.
- **Nao entregue analise sem decisao sugerida.** Cada insight relevante deve terminar com uma acao concreta que o usuario pode tomar.
- **Nao trate heuristicas como regras absolutas.** "N<50 e pequeno" e orientativo. Um N=30 com padrao claro e consistente pode ser mais confiavel que um N=500 com alta variancia.
